from datetime import date, datetime

from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from app.models.attendance import Attendance


def get_or_create_today_record(db: Session, user_id: int) -> Attendance:
    today = date.today()
    record = db.scalar(select(Attendance).where(and_(Attendance.user_id == user_id, Attendance.date == today)))
    if not record:
        record = Attendance(user_id=user_id, date=today)
        db.add(record)
        db.flush()
    return record


def monthly_summary(db: Session, user_id: int, month: int, year: int) -> dict:
    total_days = db.scalar(
        select(func.count(Attendance.id)).where(
            Attendance.user_id == user_id,
            func.extract("month", Attendance.date) == month,
            func.extract("year", Attendance.date) == year,
        )
    )
    late_days = db.scalar(
        select(func.count(Attendance.id)).where(
            Attendance.user_id == user_id,
            Attendance.status == "late",
            func.extract("month", Attendance.date) == month,
            func.extract("year", Attendance.date) == year,
        )
    )
    return {"total_days": total_days or 0, "late_days": late_days or 0, "year": year, "month": month}


def current_time() -> datetime:
    return datetime.utcnow()
