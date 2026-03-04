from datetime import date

from pydantic import BaseModel, Field


class LeaveCreate(BaseModel):
    from_date: date
    to_date: date
    reason: str = Field(min_length=5, max_length=1000)


class LeaveStatusUpdate(BaseModel):
    status: str


class LeaveOut(BaseModel):
    id: int
    user_id: int
    from_date: date
    to_date: date
    reason: str
    status: str

    class Config:
        from_attributes = True
