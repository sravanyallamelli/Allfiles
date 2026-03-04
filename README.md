# Attendance Management System (Web + Mobile + Backend)

This repository contains a complete starter implementation for an attendance management platform:
- **Backend**: FastAPI + SQLAlchemy + JWT + PostgreSQL
- **Web App**: React (Vite)
- **Mobile App**: React Native (Expo)

## 1) Backend-first delivery (step-by-step)

### Step 1: Start PostgreSQL
```bash
docker compose up -d db
```

### Step 2: Configure backend
```bash
cd backend
cp .env.example .env
pip install -r requirements.txt
```

### Step 3: Run backend
```bash
uvicorn app.main:app --reload
```
Swagger: `http://localhost:8000/docs`

### Step 4: Run web app
```bash
cd web
npm install
npm run dev
```

### Step 5: Run mobile app
```bash
cd mobile
npm install
npm run start
```

## API Modules
- `/api/v1/auth/login`
- `/api/v1/users` and `/api/v1/users/me`
- `/api/v1/attendance/*`
- `/api/v1/leave-requests/*`

## Roles and Permissions
- **Admin**: full user CRUD, full attendance view/export, reports
- **Manager**: team attendance + leave review
- **Employee**: check-in/check-out, own history, leave apply

## Database schema
Defined in SQLAlchemy models:
- `users`
- `attendance`
- `leave_requests`

See `docs/database_schema.sql` for SQL DDL.

## Deployment
- Dockerized backend (`backend/Dockerfile`)
- Root-level `docker-compose.yml`

