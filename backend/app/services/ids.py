from sqlalchemy.orm import Session


def next_code(db: Session, model, field: str, prefix: str) -> str:
    value = db.query(model).order_by(model.id.desc()).with_entities(getattr(model, field)).first()
    if not value:
        return f"{prefix}001"
    digits = "".join(ch for ch in value[0] if ch.isdigit())
    return f"{prefix}{int(digits or 0) + 1:03d}"
