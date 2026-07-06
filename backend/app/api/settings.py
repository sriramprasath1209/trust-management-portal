from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.security import get_password_hash, verify_password
from app.db.session import get_db
from app.models.entities import ActivityLog, Admin


router = APIRouter(prefix="/settings", tags=["Settings"], dependencies=[Depends(get_current_admin)])


class PasswordChange(BaseModel):
    current_password: str
    new_password: str


@router.post("/change-password")
def change_password(payload: PasswordChange, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    if not verify_password(payload.current_password, admin.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    admin.password_hash = get_password_hash(payload.new_password)
    db.add(ActivityLog(admin_username=admin.username, action="Changed password", entity="Settings"))
    db.commit()
    return {"message": "Password changed"}


@router.post("/backup")
def backup_database():
    return {"message": "SQLite database file can be copied from backend/trust_portal.db in development."}


@router.post("/restore")
def restore_database():
    return {"message": "Restore endpoint stubbed for guarded production workflow."}
