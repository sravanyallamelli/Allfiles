from fastapi import APIRouter

from app.api.v1.endpoints import attendance, auth, leave_requests, users

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(attendance.router)
api_router.include_router(leave_requests.router)
