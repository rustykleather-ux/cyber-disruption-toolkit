import csv
import io
from fastapi import APIRouter, File, UploadFile
from app.detection_engine import run_detections

router = APIRouter(prefix="/uploads", tags=["uploads"])

@router.post("/csv")
async def upload_csv(file: UploadFile = File(...)):
    content = await file.read()
    decoded_content = content.decode("utf-8")

    reader = csv.DictReader(io.StringIO(decoded))
    events = [row for row in reader]

    alerts = run_detections(events)

    return{
        "filename": file.filename,
        "events_processed": len(events),
        "alerts_found": len(alerts),
        "alerts": alerts
        
    }