from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.db.session import get_db
from app.models.entities import ActivityLog, Admin, Attendance, Member
from app.schemas.common import AttendanceCreate, AttendanceRead


router = APIRouter(prefix="/attendance", tags=["Attendance"], dependencies=[Depends(get_current_admin)])


def range_for_filter(name: str) -> tuple[date | None, date | None]:
    today = date.today()
    if name == "today":
        return today, today
    if name == "yesterday":
        yesterday = today - timedelta(days=1)
        return yesterday, yesterday
    if name == "weekly":
        return today - timedelta(days=7), today
    if name == "monthly":
        return today.replace(day=1), today
    return None, None


@router.get("/search-members", response_model=list[dict])
def search_members(q: str, db: Session = Depends(get_db)):
    like = f"%{q}%"
    members = (
        db.query(Member)
        .filter(or_(Member.name.ilike(like), Member.member_id.ilike(like), Member.aadhaar_no.ilike(like)))
        .limit(10)
        .all()
    )
    return [
        {"photo": m.photo, "name": m.name, "member_id": m.member_id, "room_number": m.room_number}
        for m in members
    ]


@router.get("", response_model=list[AttendanceRead])
def list_attendance(
    q: str | None = None,
    filter: str = "today",
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Attendance).join(Member)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Member.name.ilike(like), Member.member_id.ilike(like), Member.aadhaar_no.ilike(like)))
    start, end = (start_date, end_date) if filter == "custom" else range_for_filter(filter)
    if start:
        query = query.filter(Attendance.date >= start)
    if end:
        query = query.filter(Attendance.date <= end)
    return query.order_by(Attendance.date.desc(), Attendance.id.desc()).all()


@router.post("", response_model=AttendanceRead)
def save_attendance(
    payload: AttendanceCreate,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    if not db.query(Member).filter(Member.member_id == payload.member_id).first():
        raise HTTPException(status_code=404, detail="Member not found")
    existing = (
        db.query(Attendance)
        .filter(Attendance.member_id == payload.member_id, Attendance.date == payload.date)
        .first()
    )
    if existing:
        for key, value in payload.model_dump().items():
            setattr(existing, key, value)
        attendance = existing
    else:
        attendance = Attendance(**payload.model_dump())
        db.add(attendance)
    db.add(ActivityLog(admin_username=admin.username, action=f"Saved attendance {payload.member_id}", entity="Attendance"))
    db.commit()
    db.refresh(attendance)
    return attendance


@router.put("/{attendance_id}", response_model=AttendanceRead)
def update_attendance(
    attendance_id: int,
    payload: AttendanceCreate,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    attendance = db.get(Attendance, attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    for key, value in payload.model_dump().items():
        setattr(attendance, key, value)
    db.add(ActivityLog(admin_username=admin.username, action=f"Updated attendance {attendance_id}", entity="Attendance"))
    db.commit()
    db.refresh(attendance)
    return attendance


@router.delete("/{attendance_id}")
def delete_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    attendance = db.get(Attendance, attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    db.delete(attendance)
    db.add(ActivityLog(admin_username=admin.username, action=f"Deleted attendance {attendance_id}", entity="Attendance"))
    db.commit()
    return {"message": "Attendance deleted"}
