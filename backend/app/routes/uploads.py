import csv
import io

from fastapi import APIRouter, UploadFile, File, HTTPException

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
        alerts = run_detections(events)

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