# API Overview

Base URL: `/api/v1`

## Auth
- `POST /auth/login`

## Users
- `POST /users/register`
- `GET /users`
- `PATCH /users/{user_id}`
- `DELETE /users/{user_id}`
- `GET /users/me`

## Attendance
- `POST /attendance/check-in`
- `POST /attendance/check-out`
- `GET /attendance/history`
- `GET /attendance/all`
- `GET /attendance/team`
- `GET /attendance/report/monthly?month=..&year=..`
- `GET /attendance/export`

## Leave
- `POST /leave-requests`
- `GET /leave-requests/mine`
- `GET /leave-requests/team`
- `PATCH /leave-requests/{leave_id}`

Use FastAPI Swagger for full request/response schema at `/docs`.
