from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import attendance, auth, dashboard, members, reports, settings, staff, visitors
from app.core.config import get_settings
from app.db.session import Base, engine


settings_obj = get_settings()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings_obj.app_name, version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings_obj.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(members.router, prefix="/api")
app.include_router(attendance.router, prefix="/api")
app.include_router(staff.router, prefix="/api")
app.include_router(visitors.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
app.include_router(settings.router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok", "app": settings_obj.app_name}
