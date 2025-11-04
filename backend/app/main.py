from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.api import auth, recordings
from app.core.config import settings
from app.models import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Audio Transcription Service")

app.add_middleware(SessionMiddleware, secret_key=settings.JWT_SECRET)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(recordings.router)


@app.get("/")
async def root():
    return {"message": "Audio Transcription Service API"}


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "scribe-crush"}
