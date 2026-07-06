# Database Migrations

This project is ready for Alembic migrations. For development, FastAPI creates the
SQLite tables on startup. For production, initialize Alembic and point it at
`app.db.session.Base.metadata`.

Recommended commands:

```bash
alembic init migrations
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```
