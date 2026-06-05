from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.models import Alert
from app.routes import uploads, alerts

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cyber Disruption Toolkit",
    version="0.2.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(uploads.router)
app.include_router(alerts.router)

@app.get("/")
async def root():
    return {"message": "The Cyber Disruption Toolkit API is Running."}
