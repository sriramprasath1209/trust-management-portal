from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.db.session import get_db
from app.models.entities import ActivityLog, Admin, Staff, StaffAttendance
from app.schemas.common import StaffAttendanceCreate, StaffAttendanceRead


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


@router.get("/search-staff", response_model=list[dict])
def search_staff(q: str, db: Session = Depends(get_db)):
    like = f"%{q}%"
    staff = (
        db.query(Staff)
        .filter(or_(Staff.name.ilike(like), Staff.staff_id.ilike(like), Staff.position.ilike(like)))
        .limit(10)
        .all()
    )
    return [{"name": item.name, "staff_id": item.staff_id, "position": item.position} for item in staff]


@router.get("/staff", response_model=list[StaffAttendanceRead])
def list_staff_attendance(
    q: str | None = None,
    filter: str = "today",
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(StaffAttendance).join(Staff)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Staff.name.ilike(like), Staff.staff_id.ilike(like), Staff.position.ilike(like)))
    start, end = (start_date, end_date) if filter == "custom" else range_for_filter(filter)
    if start:
        query = query.filter(StaffAttendance.date >= start)
    if end:
        query = query.filter(StaffAttendance.date <= end)
    return query.order_by(StaffAttendance.date.desc(), StaffAttendance.id.desc()).all()


@router.get("", response_model=list[StaffAttendanceRead])
def list_attendance(
    q: str | None = None,
    filter: str = "today",
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):
    return list_staff_attendance(q=q, filter=filter, start_date=start_date, end_date=end_date, db=db)


@router.post("/staff", response_model=StaffAttendanceRead)
def save_staff_attendance(
    payload: StaffAttendanceCreate,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    if not db.query(Staff).filter(Staff.staff_id == payload.staff_id).first():
        raise HTTPException(status_code=404, detail="Staff not found")

    existing = (
        db.query(StaffAttendance)
        .filter(StaffAttendance.staff_id == payload.staff_id, StaffAttendance.date == payload.date)
        .first()
    )
    if existing:
        for key, value in payload.model_dump().items():
            setattr(existing, key, value)
        attendance = existing
    else:
        attendance = StaffAttendance(**payload.model_dump())
        db.add(attendance)

    db.add(ActivityLog(admin_username=admin.username, action=f"Saved staff attendance {payload.staff_id}", entity="Attendance"))
    db.commit()
    db.refresh(attendance)
    return attendance


@router.post("", response_model=StaffAttendanceRead)
def save_attendance(
    payload: StaffAttendanceCreate,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    return save_staff_attendance(payload=payload, db=db, admin=admin)


@router.put("/staff/{attendance_id}", response_model=StaffAttendanceRead)
def update_staff_attendance(
    attendance_id: int,
    payload: StaffAttendanceCreate,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    attendance = db.get(StaffAttendance, attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    for key, value in payload.model_dump().items():
        setattr(attendance, key, value)
    db.add(ActivityLog(admin_username=admin.username, action=f"Updated staff attendance {attendance_id}", entity="Attendance"))
    db.commit()
    db.refresh(attendance)
    return attendance


@router.put("/{attendance_id}", response_model=StaffAttendanceRead)
def update_attendance(
    attendance_id: int,
    payload: StaffAttendanceCreate,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    return update_staff_attendance(attendance_id=attendance_id, payload=payload, db=db, admin=admin)


@router.delete("/staff/{attendance_id}")
def delete_staff_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    attendance = db.get(StaffAttendance, attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    db.delete(attendance)
    db.add(ActivityLog(admin_username=admin.username, action=f"Deleted staff attendance {attendance_id}", entity="Attendance"))
    db.commit()
    return {"message": "Attendance deleted"}


@router.delete("/{attendance_id}")
def delete_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    return delete_staff_attendance(attendance_id=attendance_id, db=db, admin=admin)
