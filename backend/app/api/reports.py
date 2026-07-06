from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.db.session import get_db
from app.models.entities import Attendance, Member, Staff, Visitor


def serialize(row):
    return {key: value for key, value in row.__dict__.items() if not key.startswith("_")}


router = APIRouter(prefix="/reports", tags=["Reports"], dependencies=[Depends(get_current_admin)])


@router.get("/{report_type}")
def report(report_type: str, export: str = "json", db: Session = Depends(get_db)):
    models = {
        "attendance": Attendance,
        "members": Member,
        "visitors": Visitor,
        "staff": Staff,
        "blood-group": Member,
        "birthday-list": Member,
        "admission": Member,
    }
    model = models.get(report_type)
    if not model:
        return {"rows": [], "export": export, "message": "Unknown report type"}
    rows = db.query(model).limit(500).all()
    return {
        "report": report_type,
        "export": export,
        "rows": [serialize(row) for row in rows],
    }
