from enum import Enum
from sqlalchemy import Enum as SqlEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SqlEnum(UserRole), default=UserRole.EMPLOYEE, nullable=False)
    manager_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    manager = relationship("User", remote_side=[id], backref="team_members")
    attendance_records = relationship("Attendance", back_populates="user", cascade="all, delete")
    leave_requests = relationship("LeaveRequest", back_populates="user", cascade="all, delete")
