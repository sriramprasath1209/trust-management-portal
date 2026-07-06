from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.db.session import get_db
from app.models.entities import Attendance, Member, Staff, Visitor
from app.schemas.common import DashboardStats


router = APIRouter(prefix="/dashboard", tags=["Dashboard"], dependencies=[Depends(get_current_admin)])


@router.get("/stats", response_model=DashboardStats)
def stats(db: Session = Depends(get_db)):
    today = date.today()
    week_start = today - timedelta(days=7)
    total_members = db.query(Member).count()
    present_today = db.query(Attendance).filter(Attendance.date == today, Attendance.status == "Present").count()
    absent_today = db.query(Attendance).filter(Attendance.date == today, Attendance.status == "Absent").count()
    visitors_today = db.query(Visitor).filter(func.date(Visitor.entry_time) == today.isoformat()).count()
    staff_count = db.query(Staff).count()
    new_members = db.query(Member).filter(Member.admission_date >= week_start).count()
    upcoming_birthdays = db.query(Member).filter(extract("month", Member.dob) == today.month).count()

    statuses = dict(
        db.query(Attendance.status, func.count(Attendance.id))
        .filter(Attendance.date >= week_start)
        .group_by(Attendance.status)
        .all()
    )
    admissions = [
        {"month": str(month), "count": count}
        for month, count in db.query(extract("month", Member.admission_date), func.count(Member.id))
        .group_by(extract("month", Member.admission_date))
        .all()
    ]
    blood_groups = dict(
        db.query(Member.blood_group, func.count(Member.id))
        .filter(Member.blood_group.is_not(None))
        .group_by(Member.blood_group)
        .all()
    )

    return DashboardStats(
        total_members=total_members,
        present_today=present_today,
        absent_today=absent_today,
        visitors_today=visitors_today,
        staff_count=staff_count,
        new_members=new_members,
        upcoming_birthdays=upcoming_birthdays,
        attendance_summary=statuses,
        monthly_admissions=admissions,
        blood_group_distribution=blood_groups,
    )
