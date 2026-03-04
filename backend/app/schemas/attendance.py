from datetime import date, datetime

from pydantic import BaseModel


class AttendanceOut(BaseModel):
    id: int
    user_id: int
    date: date
    check_in: datetime | None = None
    check_out: datetime | None = None
    status: str

    class Config:
        from_attributes = True
