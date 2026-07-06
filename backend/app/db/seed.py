from datetime import date, datetime, timedelta, timezone

from app.core.security import get_password_hash
from app.db.session import Base, SessionLocal, engine
from app.models.entities import Admin, Attendance, Member, Staff, Visitor


def run_seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        admin = db.query(Admin).filter(Admin.username == "admin").first()
        if admin:
            admin.password_hash = get_password_hash("admin123")
            admin.role = "Super Admin"
            admin.status = "Active"
        else:
            db.add(
                Admin(
                    username="admin",
                    password_hash=get_password_hash("admin123"),
                    role="Super Admin",
                    status="Active",
                )
            )
        if not db.query(Member).first():
            members = [
                Member(
                    member_id="MEM001",
                    name="Ananya Raman",
                    father_name="Raman K",
                    mother_name="Meena Raman",
                    dob=date(2013, 7, 18),
                    gender="Female",
                    age=12,
                    aadhaar_no="123456789012",
                    blood_group="O+",
                    phone="9876543210",
                    emergency_name="Raman K",
                    emergency_phone="9876543210",
                    relationship="Father",
                    room_number="A-101",
                    admission_date=date.today() - timedelta(days=5),
                    education="Grade 7",
                    current_status="Active",
                ),
                Member(
                    member_id="MEM002",
                    name="Karthik Selvam",
                    father_name="Selvam R",
                    mother_name="Lakshmi S",
                    dob=date(2011, 3, 8),
                    gender="Male",
                    age=15,
                    aadhaar_no="789456123012",
                    blood_group="B+",
                    phone="9876500011",
                    emergency_name="Lakshmi S",
                    emergency_phone="9876500011",
                    relationship="Mother",
                    room_number="B-204",
                    admission_date=date.today() - timedelta(days=45),
                    education="Grade 9",
                    current_status="Active",
                ),
            ]
            db.add_all(members)
            db.add_all(
                [
                    Attendance(member_id="MEM001", date=date.today(), time="09:00", status="Present"),
                    Attendance(member_id="MEM002", date=date.today(), time="09:05", status="Absent", remarks="Family visit"),
                ]
            )
        if not db.query(Staff).first():
            db.add_all(
                [
                    Staff(staff_id="STF001", name="Priya Nair", position="Warden", phone="9000011111", salary=32000, attendance="Present"),
                    Staff(staff_id="STF002", name="Suresh Kumar", position="Nurse", phone="9000022222", salary=28000, attendance="Present"),
                ]
            )
        if not db.query(Visitor).first():
            db.add(
                Visitor(
                    visitor_name="Mohan Das",
                    phone="9444412345",
                    purpose="Donor visit",
                    member_id="MEM001",
                    entry_time=datetime.now(timezone.utc),
                    remarks="Brought stationery",
                )
            )
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
