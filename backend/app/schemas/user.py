from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole = UserRole.EMPLOYEE
    manager_id: int | None = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    role: UserRole | None = None
    manager_id: int | None = None


class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True
