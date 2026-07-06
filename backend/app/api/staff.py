from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.db.session import get_db
from app.models.entities import ActivityLog, Admin, Staff
from app.schemas.common import StaffCreate, StaffRead
from app.services.ids import next_code


router = APIRouter(prefix="/staff", tags=["Staff"], dependencies=[Depends(get_current_admin)])


@router.get("", response_model=list[StaffRead])
def list_staff(db: Session = Depends(get_db)):
    return db.query(Staff).order_by(Staff.id.desc()).all()


@router.post("", response_model=StaffRead)
def create_staff(payload: StaffCreate, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    data = payload.model_dump()
    data["staff_id"] = data["staff_id"] or next_code(db, Staff, "staff_id", "STF")
    staff = Staff(**data)
    db.add(staff)
    db.add(ActivityLog(admin_username=admin.username, action=f"Created staff {staff.staff_id}", entity="Staff"))
    db.commit()
    db.refresh(staff)
    return staff


@router.put("/{staff_id}", response_model=StaffRead)
def update_staff(staff_id: str, payload: StaffCreate, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    staff = db.query(Staff).filter(Staff.staff_id == staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    for key, value in payload.model_dump(exclude={"staff_id"}).items():
        setattr(staff, key, value)
    db.add(ActivityLog(admin_username=admin.username, action=f"Updated staff {staff_id}", entity="Staff"))
    db.commit()
    db.refresh(staff)
    return staff


@router.delete("/{staff_id}")
def delete_staff(staff_id: str, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    staff = db.query(Staff).filter(Staff.staff_id == staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    db.delete(staff)
    db.add(ActivityLog(admin_username=admin.username, action=f"Deleted staff {staff_id}", entity="Staff"))
    db.commit()
    return {"message": "Staff deleted"}
