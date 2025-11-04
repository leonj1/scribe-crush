import httpx
from app.core.config import settings


class RequestYaiProvider:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.LLM_API_KEY
        self.base_url = "https://api.requestyai.com/v1"
    
    def transcribe_audio(self, audio_path: str) -> str:
        with open(audio_path, "rb") as audio_file:
            files = {"file": audio_file}
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            with httpx.Client(timeout=300.0) as client:
                response = client.post(
                    f"{self.base_url}/transcribe",
                    files=files,
                    headers=headers
                )
                response.raise_for_status()
                result = response.json()
                return result.get("transcription", "")
