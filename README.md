# Trust Management Portal

A full-stack Trust/Home Management Portal for residents in a trust, orphanage,
old-age home, or shelter home.

## Stack

- Frontend: React, React Router, Tailwind CSS, Axios, Recharts, Lucide icons
- Backend: FastAPI, SQLAlchemy, JWT auth, bcrypt password hashing
- Database: SQLite for development, ready to point at MySQL/PostgreSQL with `DATABASE_URL`

## Quick Start

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.db.seed
uvicorn app.main:app --reload
```

The API docs will be available at `http://127.0.0.1:8000/docs`.

Seeded administrator:

- Username: `admin`
- Password: `admin123`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://127.0.0.1:5173`.

## Features

- Secure administrator login with JWT protected routes
- Responsive dashboard with summary cards and charts
- Attendance portal with member search, statuses, filters, and history
- Member management with personal, government, medical, contact, address, trust,
  document, QR code, and print ID card controls
- Staff and visitor management
- Reports endpoint with JSON plus export mode placeholders for PDF, Excel, CSV
- Settings for password changes, admin creation, backup and restore workflow
- Dark mode, activity logs, seed data, and API documentation via FastAPI

## Production Notes

- Change `SECRET_KEY` before deployment.
- Use PostgreSQL or MySQL by setting `DATABASE_URL`.
- Replace the development table creation flow with Alembic migrations.
- Store uploads in a managed object store or protected file volume.
- Put the API behind HTTPS and configure CORS for the production frontend origin.
