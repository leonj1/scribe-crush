from typing import Protocol


class LLMProvider(Protocol):
    def transcribe_audio(self, audio_path: str) -> str:
        ...
