from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.recording import Recording, RecordingChunk, RecordingStatus


class MySQLRecordingRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_recording(self, user_id: str) -> Recording:
        recording = Recording(user_id=user_id, status=RecordingStatus.active)
        self.db.add(recording)
        self.db.commit()
        self.db.refresh(recording)
        return recording
    
    def get_recording(self, recording_id: str) -> Optional[Recording]:
        return self.db.query(Recording).filter(Recording.id == recording_id).first()
    
    def list_recordings(self, user_id: str) -> List[Recording]:
        return self.db.query(Recording).filter(Recording.user_id == user_id).order_by(Recording.created_at.desc()).all()
    
    def add_chunk(self, recording_id: str, chunk_path: str, index: int, duration: Optional[float]) -> RecordingChunk:
        chunk = RecordingChunk(
            recording_id=recording_id,
            chunk_index=index,
            audio_blob_path=chunk_path,
            duration_seconds=duration
        )
        self.db.add(chunk)
        self.db.commit()
        self.db.refresh(chunk)
        return chunk
    
    def mark_paused(self, recording_id: str) -> Optional[Recording]:
        recording = self.get_recording(recording_id)
        if recording:
            recording.status = RecordingStatus.paused
            self.db.commit()
            self.db.refresh(recording)
        return recording
    
    def mark_ended(self, recording_id: str, full_audio_path: str, transcription: str) -> Optional[Recording]:
        recording = self.get_recording(recording_id)
        if recording:
            recording.status = RecordingStatus.ended
            recording.audio_file_path = full_audio_path
            recording.transcription_text = transcription
            self.db.commit()
            self.db.refresh(recording)
        return recording
    
    def update_notes(self, recording_id: str, notes: str) -> Optional[Recording]:
        recording = self.get_recording(recording_id)
        if recording:
            recording.notes = notes
            self.db.commit()
            self.db.refresh(recording)
        return recording
