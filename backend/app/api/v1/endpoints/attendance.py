from datetime import datetime
import io

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.core.config import settings
from app.db.session import get_db
from app.models.attendance import Attendance
from app.models.user import User, UserRole
from app.schemas.attendance import AttendanceOut
from app.services.attendance_service import current_time, get_or_create_today_record, monthly_summary

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/check-in", response_model=AttendanceOut)
def check_in(current_user: User = Depends(require_roles(UserRole.EMPLOYEE, UserRole.MANAGER, UserRole.ADMIN)), db: Session = Depends(get_db)):
    record = get_or_create_today_record(db, current_user.id)
    if record.check_in:
        raise HTTPException(status_code=400, detail="Already checked in today")
    now = current_time()
    late_time = datetime.strptime(settings.LATE_CHECKIN_TIME, "%H:%M").time()
    record.check_in = now
    record.status = "late" if now.time() > late_time else "present"
    db.commit()
    db.refresh(record)
    return record


@router.post("/check-out", response_model=AttendanceOut)
def check_out(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = get_or_create_today_record(db, current_user.id)
    if not record.check_in:
        raise HTTPException(status_code=400, detail="Please check in first")
    if record.check_out:
        raise HTTPException(status_code=400, detail="Already checked out")
    record.check_out = current_time()
    db.commit()
    db.refresh(record)
    return record


@router.get("/history", response_model=list[AttendanceOut])
def my_history(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.scalars(select(Attendance).where(Attendance.user_id == current_user.id).offset(skip).limit(limit)).all()


@router.get("/all", response_model=list[AttendanceOut])
def all_attendance(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=500),
    _: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    return db.scalars(select(Attendance).offset(skip).limit(limit)).all()


@router.get("/team", response_model=list[AttendanceOut])
def team_attendance(
    manager: User = Depends(require_roles(UserRole.MANAGER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    team_ids = [member.id for member in manager.team_members]
    if not team_ids:
        return []
    return db.scalars(select(Attendance).where(Attendance.user_id.in_(team_ids))).all()


@router.get("/report/monthly")
def report(month: int, year: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return monthly_summary(db, current_user.id, month, year)


@router.get("/export")
def export_csv(
    _: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    rows = db.scalars(select(Attendance)).all()
    data = [
        {
            "id": r.id,
            "user_id": r.user_id,
            "date": r.date,
            "check_in": r.check_in,
            "check_out": r.check_out,
            "status": r.status,
        }
        for r in rows
    ]
    df = pd.DataFrame(data)
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    buf.seek(0)
    return StreamingResponse(iter([buf.getvalue()]), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=attendance.csv"})
