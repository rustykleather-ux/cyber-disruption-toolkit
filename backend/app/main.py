from fastapi import FastAPI

from app.database import Base, engine
from app.models import Alert
from app.routes import uploads, alerts

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cyber Disruption Toolkit",
    version="0.2.0"
)

app.include_router(uploads.router)
app.include_router(alerts.router)

@app.get("/")
async def root():
    return {"message": "The Cyber Disruption Toolkit API is Running."}
