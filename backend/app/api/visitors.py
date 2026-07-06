from datetime import date, datetime, time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.db.session import get_db
from app.models.entities import ActivityLog, Admin, Visitor
from app.schemas.common import VisitorCreate, VisitorRead


router = APIRouter(prefix="/visitors", tags=["Visitors"], dependencies=[Depends(get_current_admin)])


@router.get("", response_model=list[VisitorRead])
def list_visitors(today: bool = False, db: Session = Depends(get_db)):
    query = db.query(Visitor)
    if today:
        start = datetime.combine(date.today(), time.min)
        end = datetime.combine(date.today(), time.max)
        query = query.filter(Visitor.entry_time >= start, Visitor.entry_time <= end)
    return query.order_by(Visitor.entry_time.desc()).all()


@router.post("", response_model=VisitorRead)
def create_visitor(payload: VisitorCreate, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    data = payload.model_dump()
    if data["entry_time"] is None:
        data.pop("entry_time")
    visitor = Visitor(**data)
    db.add(visitor)
    db.add(ActivityLog(admin_username=admin.username, action=f"Created visitor {visitor.visitor_name}", entity="Visitor"))
    db.commit()
    db.refresh(visitor)
    return visitor


@router.put("/{visitor_id}", response_model=VisitorRead)
def update_visitor(visitor_id: int, payload: VisitorCreate, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    visitor = db.get(Visitor, visitor_id)
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(visitor, key, value)
    db.add(ActivityLog(admin_username=admin.username, action=f"Updated visitor {visitor_id}", entity="Visitor"))
    db.commit()
    db.refresh(visitor)
    return visitor


@router.delete("/{visitor_id}")
def delete_visitor(visitor_id: int, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    visitor = db.get(Visitor, visitor_id)
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    db.delete(visitor)
    db.add(ActivityLog(admin_username=admin.username, action=f"Deleted visitor {visitor_id}", entity="Visitor"))
    db.commit()
    return {"message": "Visitor deleted"}
