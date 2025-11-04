from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.models import get_db
from app.repositories.recording_repository import MySQLRecordingRepository
from app.core.security import get_current_user_id
from app.services.audio_service import AudioService
from app.llm.requestyai_provider import RequestYaiProvider

router = APIRouter(prefix="/recordings", tags=["recordings"])


class RecordingResponse(BaseModel):
    id: str
    status: str
    created_at: str
    transcription_text: str = None
    notes: str = None
    
    class Config:
        from_attributes = True


class NotesUpdate(BaseModel):
    notes: str


@router.post("", response_model=RecordingResponse)
async def create_recording(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    repo = MySQLRecordingRepository(db)
    recording = repo.create_recording(user_id)
    return RecordingResponse(
        id=recording.id,
        status=recording.status.value,
        created_at=recording.created_at.isoformat(),
        transcription_text=recording.transcription_text,
        notes=recording.notes
    )


@router.get("", response_model=List[RecordingResponse])
async def list_recordings(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    repo = MySQLRecordingRepository(db)
    recordings = repo.list_recordings(user_id)
    return [
        RecordingResponse(
            id=r.id,
            status=r.status.value,
            created_at=r.created_at.isoformat(),
            transcription_text=r.transcription_text,
            notes=r.notes
        )
        for r in recordings
    ]


@router.get("/{recording_id}", response_model=RecordingResponse)
async def get_recording(
    recording_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    repo = MySQLRecordingRepository(db)
    recording = repo.get_recording(recording_id)
    
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    if recording.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return RecordingResponse(
        id=recording.id,
        status=recording.status.value,
        created_at=recording.created_at.isoformat(),
        transcription_text=recording.transcription_text,
        notes=recording.notes
    )


@router.post("/{recording_id}/chunks")
async def upload_chunk(
    recording_id: str,
    chunk_index: int = Form(...),
    audio_chunk: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    repo = MySQLRecordingRepository(db)
    recording = repo.get_recording(recording_id)
    
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    if recording.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    audio_service = AudioService()
    chunk_data = await audio_chunk.read()
    chunk_path = audio_service.save_chunk(recording_id, chunk_index, chunk_data)
    
    repo.add_chunk(recording_id, chunk_path, chunk_index, None)
    
    return {"status": "success", "chunk_index": chunk_index}


@router.patch("/{recording_id}/pause")
async def pause_recording(
    recording_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    repo = MySQLRecordingRepository(db)
    recording = repo.get_recording(recording_id)
    
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    if recording.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo.mark_paused(recording_id)
    return {"status": "paused"}


@router.post("/{recording_id}/finish")
async def finish_recording(
    recording_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    repo = MySQLRecordingRepository(db)
    recording = repo.get_recording(recording_id)
    
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    if recording.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    chunk_paths = [chunk.audio_blob_path for chunk in sorted(recording.chunks, key=lambda c: c.chunk_index)]
    
    audio_service = AudioService()
    full_audio_path = audio_service.assemble_chunks(recording_id, chunk_paths)
    
    llm_provider = RequestYaiProvider()
    transcription = llm_provider.transcribe_audio(full_audio_path)
    
    repo.mark_ended(recording_id, full_audio_path, transcription)
    
    audio_service.cleanup_chunks(chunk_paths)
    
    return {"status": "completed", "transcription": transcription}


@router.patch("/{recording_id}/notes")
async def update_notes(
    recording_id: str,
    notes_data: NotesUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    repo = MySQLRecordingRepository(db)
    recording = repo.get_recording(recording_id)
    
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    if recording.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo.update_notes(recording_id, notes_data.notes)
    return {"status": "success"}
