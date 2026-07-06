from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.session import get_db
from app.models.entities import ActivityLog, Admin
from app.schemas.common import AdminCreate, AdminRead, Token


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.username == form.username).first()
    if not admin or admin.status != "Active" or not verify_password(form.password, admin.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    admin.last_login = datetime.now(timezone.utc)
    db.add(ActivityLog(admin_username=admin.username, action="Logged in", entity="Admin"))
    db.commit()
    db.refresh(admin)
    return Token(access_token=create_access_token(admin.username, {"role": admin.role}), admin=admin)


@router.get("/me", response_model=AdminRead)
def me(admin: Admin = Depends(get_current_admin)):
    return admin


@router.post("/admins", response_model=AdminRead)
def create_admin(
    payload: AdminCreate,
    db: Session = Depends(get_db),
    current: Admin = Depends(get_current_admin),
):
    if db.query(Admin).filter(Admin.username == payload.username).first():
        raise HTTPException(status_code=409, detail="Username already exists")
    admin = Admin(
        username=payload.username,
        password_hash=get_password_hash(payload.password),
        role=payload.role,
        status=payload.status,
    )
    db.add(admin)
    db.add(ActivityLog(admin_username=current.username, action=f"Created admin {payload.username}", entity="Admin"))
    db.commit()
    db.refresh(admin)
    return admin


@router.get("/admins", response_model=list[AdminRead])
def list_admins(db: Session = Depends(get_db), _: Admin = Depends(get_current_admin)):
    return db.query(Admin).order_by(Admin.created_at.desc()).all()
