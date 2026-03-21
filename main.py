"""
TruthScan AI - Fake News & Scam Detector
Main entry point for the FastAPI application

Tech Stack:
- FastAPI (Python web framework)
- Groq AI with Llama 3.3 70B (NLP analysis)
- MySQL + SQLAlchemy (database)
- Twilio (WhatsApp integration)
"""

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import APP_HOST, APP_PORT
from app.database import engine, Base
from app.routes import router

# this will create all the tables in mysql if they don't exist yet
Base.metadata.create_all(bind=engine)

# initialize the fastapi app
app = FastAPI(
    title="TruthScan AI",
    description="Fake News & Scam Detector powered by Groq AI",
    version="1.0.0",
)

# serve css, js files from the static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# register all our API routes under /api prefix
app.include_router(router, prefix="/api")


@app.get("/")
def home():
    """Serve the main frontend page"""
    return FileResponse("static/index.html")


# run the server
if __name__ == "__main__":
    print("Starting TruthScan AI server...")
    uvicorn.run("main:app", host=APP_HOST, port=APP_PORT, reload=True)
