from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    admin: "AdminRead"


class AdminBase(BaseModel):
    username: str
    role: str = "Administrator"
    status: str = "Active"


class AdminCreate(AdminBase):
    password: str


class AdminRead(AdminBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_login: datetime | None = None
    created_at: datetime


class MemberBase(BaseModel):
    member_id: str | None = None
    name: str
    father_name: str | None = None
    mother_name: str | None = None
    dob: date | None = None
    gender: str | None = None
    age: int | None = None
    aadhaar_no: str | None = None
    pan_no: str | None = None
    blood_group: str | None = None
    allergies: str | None = None
    medical_conditions: str | None = None
    disability: str | None = None
    medications: str | None = None
    phone: str | None = None
    emergency_name: str | None = None
    emergency_phone: str | None = None
    relationship: str | None = None
    plot_number: str | None = None
    street: str | None = None
    area: str | None = None
    village: str | None = None
    taluk: str | None = None
    district: str | None = None
    state: str | None = None
    pincode: str | None = None
    room_number: str | None = None
    guardian: str | None = None
    admission_date: date | None = None
    education: str | None = None
    occupation: str | None = None
    current_status: str = "Active"
    photo: str | None = None
    aadhaar_copy: str | None = None
    medical_certificate: str | None = None
    other_documents: str | None = None
    notes: str | None = None


class MemberCreate(MemberBase):
    pass


class MemberRead(MemberBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_id: str


class AttendanceBase(BaseModel):
    member_id: str
    date: date
    time: str | None = None
    status: str
    remarks: str | None = None


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceRead(AttendanceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    member: MemberRead | None = None


class StaffAttendanceBase(BaseModel):
    staff_id: str
    date: date
    time: str | None = None
    status: str
    remarks: str | None = None


class StaffAttendanceCreate(StaffAttendanceBase):
    pass


class StaffAttendanceRead(StaffAttendanceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    staff: StaffRead | None = None


class StaffBase(BaseModel):
    staff_id: str | None = None
    name: str
    position: str
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    joining_date: date | None = None
    salary: float | None = None
    attendance: str = "Present"


class StaffCreate(StaffBase):
    pass


class StaffRead(StaffBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    staff_id: str


class VisitorBase(BaseModel):
    visitor_name: str
    phone: str | None = None
    purpose: str | None = None
    member_id: str | None = None
    entry_time: datetime | None = None
    exit_time: datetime | None = None
    remarks: str | None = None


class VisitorCreate(VisitorBase):
    pass


class VisitorRead(VisitorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    entry_time: datetime


class DashboardStats(BaseModel):
    total_members: int
    present_today: int
    absent_today: int
    visitors_today: int
    staff_count: int
    new_members: int
    upcoming_birthdays: int
    attendance_summary: dict[str, int]
    monthly_admissions: list[dict[str, int | str]]
    blood_group_distribution: dict[str, int]


Token.model_rebuild()
