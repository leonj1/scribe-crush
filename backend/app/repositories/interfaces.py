from typing import Protocol, List, Optional
from app.models.user import User
from app.models.recording import Recording, RecordingChunk


class UserRepository(Protocol):
    def create_user(self, google_id: str, email: str, display_name: str, avatar_url: Optional[str]) -> User:
        ...
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        ...
    
    def get_user_by_google_id(self, google_id: str) -> Optional[User]:
        ...
    
    def update_user(self, user_id: str, **kwargs) -> Optional[User]:
        ...


class RecordingRepository(Protocol):
    def create_recording(self, user_id: str) -> Recording:
        ...
    
    def get_recording(self, recording_id: str) -> Optional[Recording]:
        ...
    
    def list_recordings(self, user_id: str) -> List[Recording]:
        ...
    
    def add_chunk(self, recording_id: str, chunk_path: str, index: int, duration: Optional[float]) -> RecordingChunk:
        ...
    
    def mark_paused(self, recording_id: str) -> Optional[Recording]:
        ...
    
    def mark_ended(self, recording_id: str, full_audio_path: str, transcription: str) -> Optional[Recording]:
        ...
    
    def update_notes(self, recording_id: str, notes: str) -> Optional[Recording]:
        ...
