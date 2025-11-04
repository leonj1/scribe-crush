import os
import shutil
from pathlib import Path
from typing import List
from app.core.config import settings


class AudioService:
    def __init__(self):
        self.storage_path = Path(settings.AUDIO_STORAGE_PATH)
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def save_chunk(self, recording_id: str, chunk_index: int, chunk_data: bytes) -> str:
        recording_dir = self.storage_path / recording_id
        recording_dir.mkdir(parents=True, exist_ok=True)
        
        chunk_path = recording_dir / f"chunk_{chunk_index:04d}.webm"
        with open(chunk_path, "wb") as f:
            f.write(chunk_data)
        
        return str(chunk_path)
    
    def assemble_chunks(self, recording_id: str, chunk_paths: List[str]) -> str:
        recording_dir = self.storage_path / recording_id
        final_path = recording_dir / "full_audio.webm"
        
        with open(final_path, "wb") as outfile:
            for chunk_path in sorted(chunk_paths):
                with open(chunk_path, "rb") as infile:
                    shutil.copyfileobj(infile, outfile)
        
        return str(final_path)
    
    def cleanup_chunks(self, chunk_paths: List[str]):
        for chunk_path in chunk_paths:
            try:
                os.remove(chunk_path)
            except OSError:
                pass
