from fastapi import FastAPI
from app.routes import uploads, alerts

app =FastAPI(
    title="Cyber Disruption Toolkit",
    description="A toolkit for simulating cyber disruptions in a controlled environment.",
    version="0.1.0" \
    "This API allows users to upload files, manage alerts, and simulate cyber disruptions for testing and training purposes.",
    
)

app.include_router(uploads.router)
app.include_router(alerts.router)

@app.get("/")
async def root():
    return {"message": "The Cyber Disruption Toolkit API is Running."}
