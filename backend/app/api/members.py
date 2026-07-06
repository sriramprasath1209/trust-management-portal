from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.db.session import get_db
from app.models.entities import ActivityLog, Admin, Member
from app.schemas.common import MemberCreate, MemberRead
from app.services.ids import next_code


router = APIRouter(prefix="/members", tags=["Members"], dependencies=[Depends(get_current_admin)])


@router.get("", response_model=list[MemberRead])
def list_members(
    q: str | None = None,
    limit: int = Query(default=100, le=500),
    offset: int = 0,
    db: Session = Depends(get_db),
):
    query = db.query(Member)
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(Member.name.ilike(like), Member.member_id.ilike(like), Member.aadhaar_no.ilike(like))
        )
    return query.order_by(Member.id.desc()).offset(offset).limit(limit).all()


@router.get("/{member_id}", response_model=MemberRead)
def get_member(member_id: str, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.member_id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.post("", response_model=MemberRead)
def create_member(
    payload: MemberCreate,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    data = payload.model_dump()
    data["member_id"] = data["member_id"] or next_code(db, Member, "member_id", "MEM")
    member = Member(**data)
    db.add(member)
    db.add(ActivityLog(admin_username=admin.username, action=f"Created member {member.member_id}", entity="Member"))
    db.commit()
    db.refresh(member)
    return member


@router.put("/{member_id}", response_model=MemberRead)
def update_member(
    member_id: str,
    payload: MemberCreate,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    member = db.query(Member).filter(Member.member_id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    for key, value in payload.model_dump(exclude={"member_id"}).items():
        setattr(member, key, value)
    db.add(ActivityLog(admin_username=admin.username, action=f"Updated member {member_id}", entity="Member"))
    db.commit()
    db.refresh(member)
    return member


@router.delete("/{member_id}")
def delete_member(
    member_id: str,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    member = db.query(Member).filter(Member.member_id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    db.delete(member)
    db.add(ActivityLog(admin_username=admin.username, action=f"Deleted member {member_id}", entity="Member"))
    db.commit()
    return {"message": "Member deleted"}
