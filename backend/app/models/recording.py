from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Text, Float, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.models import Base
import uuid


class RecordingStatus(str, enum.Enum):
    active = "active"
    paused = "paused"
    ended = "ended"


class Recording(Base):
    __tablename__ = "recordings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    status = Column(Enum(RecordingStatus), default=RecordingStatus.active, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    audio_file_path = Column(String(512))
    transcription_text = Column(Text)
    llm_provider = Column(String(50), default="requestyai")
    notes = Column(Text)
    
    chunks = relationship("RecordingChunk", back_populates="recording", cascade="all, delete-orphan")


class RecordingChunk(Base):
    __tablename__ = "recording_chunks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    recording_id = Column(String(36), ForeignKey("recordings.id"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    audio_blob_path = Column(String(512), nullable=False)
    duration_seconds = Column(Float)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    recording = relationship("Recording", back_populates="chunks")
