from fastapi import APIRouter

from app.database import SessionLocal
from app.models import Alert

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/")
def get_alerts():
    db = SessionLocal()

    alerts = db.query(Alert).all()

    db.close()

    return alerts