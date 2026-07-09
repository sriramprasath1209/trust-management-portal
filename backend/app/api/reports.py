import csv
import io
import json
from datetime import date, datetime

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.db.session import get_db
from app.models.entities import Attendance, Member, Staff, Visitor


def serialize(row):
    data = {}
    for key, value in row.__dict__.items():
        if key.startswith("_"):
            continue
        if isinstance(value, (datetime, date)):
            data[key] = value.isoformat()
        else:
            data[key] = value
    return data


def build_csv(rows, report_type: str) -> bytes:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0].keys()) if rows else [])
    if rows:
        writer.writeheader()
        writer.writerows(rows)
    return output.getvalue().encode("utf-8")


def escape_pdf_text(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)").replace("\n", "\\n")


def build_pdf(rows, report_type: str) -> bytes:
    lines = [f"{report_type.upper()} REPORT", ""]
    for index, row in enumerate(rows, start=1):
        lines.append(f"{index}. " + ", ".join(f"{key}: {value}" for key, value in row.items()))
    content = "\\n".join(escape_pdf_text(line) for line in lines)
    pdf_text = (
        "%PDF-1.4\n"
        "1 0 obj\n"
        "<< /Type /Catalog /Pages 2 0 R >>\n"
        "endobj\n"
        "2 0 obj\n"
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>\n"
        "endobj\n"
        "3 0 obj\n"
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\n"
        "endobj\n"
        "4 0 obj\n"
        "<< /Length 0 >>\n"
        "stream\n"
        "BT\n"
        "/F1 11 Tf\n"
        "72 760 Td\n"
        f"({content}) Tj\n"
        "ET\n"
        "endstream\n"
        "endobj\n"
        "5 0 obj\n"
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\n"
        "endobj\n"
        "xref\n"
        "0 6\n"
        "0000000000 65535 f \n"
        "0000000010 00000 n \n"
        "0000000062 00000 n \n"
        "0000000119 00000 n \n"
        "0000000208 00000 n \n"
        "0000000303 00000 n \n"
        "trailer\n"
        "<< /Size 6 /Root 1 0 R >>\n"
        "startxref\n"
        "0\n"
        "%%EOF\n"
    )
    return pdf_text.encode("latin-1", "ignore")


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
        payload = {"rows": [], "export": export, "message": "Unknown report type"}
        return Response(
            content=json.dumps(payload),
            media_type="application/json",
            headers={"Content-Disposition": f'attachment; filename="{report_type}.json"'},
        )

    rows = db.query(model).limit(500).all()
    serialized_rows = [serialize(row) for row in rows]
    export_name = (export or "json").lower()
    filename = f"{report_type}.{export_name if export_name in {'json', 'csv', 'pdf'} else 'xls'}"

    if export_name == "csv":
        return Response(
            content=build_csv(serialized_rows, report_type),
            media_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    if export_name == "pdf":
        return Response(
            content=build_pdf(serialized_rows, report_type),
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    if export_name == "excel":
        return Response(
            content=build_csv(serialized_rows, report_type),
            media_type="application/vnd.ms-excel",
            headers={"Content-Disposition": f'attachment; filename="{report_type}.xls"'},
        )

    return Response(
        content=json.dumps({"report": report_type, "export": export_name, "rows": serialized_rows}, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
