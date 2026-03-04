from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.leave_request import LeaveRequest
from app.models.user import User, UserRole
from app.schemas.leave_request import LeaveCreate, LeaveOut, LeaveStatusUpdate

router = APIRouter(prefix="/leave-requests", tags=["Leave Requests"])


@router.post("", response_model=LeaveOut)
def apply_leave(payload: LeaveCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    leave = LeaveRequest(
        user_id=current_user.id,
        from_date=payload.from_date,
        to_date=payload.to_date,
        reason=payload.reason,
    )
    db.add(leave)
    db.commit()
    db.refresh(leave)
    return leave


@router.get("/mine", response_model=list[LeaveOut])
def my_leaves(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.scalars(select(LeaveRequest).where(LeaveRequest.user_id == current_user.id).offset(skip).limit(limit)).all()


@router.get("/team", response_model=list[LeaveOut])
def team_leaves(manager: User = Depends(require_roles(UserRole.MANAGER, UserRole.ADMIN)), db: Session = Depends(get_db)):
    team_ids = [member.id for member in manager.team_members]
    if not team_ids:
        return []
    return db.scalars(select(LeaveRequest).where(LeaveRequest.user_id.in_(team_ids))).all()


@router.patch("/{leave_id}", response_model=LeaveOut)
def review_leave(
    leave_id: int,
    payload: LeaveStatusUpdate,
    manager: User = Depends(require_roles(UserRole.MANAGER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    leave = db.get(LeaveRequest, leave_id)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")

    if manager.role == UserRole.MANAGER and leave.user.manager_id != manager.id:
        raise HTTPException(status_code=403, detail="Not in your team")

    if payload.status not in {"approved", "rejected", "pending"}:
        raise HTTPException(status_code=400, detail="Invalid status")

    leave.status = payload.status
    db.commit()
    db.refresh(leave)
    return leave
