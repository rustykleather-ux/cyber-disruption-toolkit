import csv
import io

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.mitre_mapper import enrich_alert
from app.database import SessionLocal
from app.models import Alert
from app.detection_engine import run_detections


router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("/csv")
async def upload_csv(file: UploadFile = File(...)):
    try:
        content = await file.read()

        if not content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        decoded = content.decode("utf-8-sig")

        reader = csv.DictReader(io.StringIO(decoded))

        if not reader.fieldnames:
            raise HTTPException(status_code=400, detail="CSV file has no headers.")

        events = list(reader)
        alerts = [enrich_alert(alert) for alert in run_detections(events)]

        db = SessionLocal()

        for alert in alerts:
            db_alert = Alert(
    title=alert["title"],
    severity=alert["severity"],
    risk_score=alert["risk_score"],
    host=alert["host"], 
    user=alert["user"],
    source_ip=alert["source_ip"],
    mitre_technique=alert["mitre_technique"],
    technique_name=alert["technique_name"],
    tactic=alert["tactic"],
    description=alert["description"],
    recommended_action=alert["recommended_action"],
)
            

            db.add(db_alert)

        db.commit()
        db.close()

        return {
            "filename": file.filename,
            "headers": reader.fieldnames,
            "events_processed": len(events),
            "alerts_found": len(alerts),
            "alerts": alerts,
        }

    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Could not decode file. Please upload a UTF-8 CSV file.",
        )