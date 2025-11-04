import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.models.user import User
from app.models.recording import Recording, RecordingStatus
from app.repositories.user_repository import MySQLUserRepository
from app.repositories.recording_repository import MySQLRecordingRepository


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


def test_create_user(db_session):
    repo = MySQLUserRepository(db_session)
    user = repo.create_user(
        google_id="123456",
        email="[email protected]",
        display_name="Test User",
        avatar_url="https://example.com/avatar.jpg"
    )
    
    assert user.id is not None
    assert user.google_id == "123456"
    assert user.email == "[email protected]"


def test_get_user_by_google_id(db_session):
    repo = MySQLUserRepository(db_session)
    user = repo.create_user(
        google_id="123456",
        email="[email protected]",
        display_name="Test User",
        avatar_url=None
    )
    
    found_user = repo.get_user_by_google_id("123456")
    assert found_user is not None
    assert found_user.id == user.id


def test_create_recording(db_session):
    user_repo = MySQLUserRepository(db_session)
    user = user_repo.create_user(
        google_id="123456",
        email="[email protected]",
        display_name="Test User",
        avatar_url=None
    )
    
    recording_repo = MySQLRecordingRepository(db_session)
    recording = recording_repo.create_recording(user.id)
    
    assert recording.id is not None
    assert recording.user_id == user.id
    assert recording.status == RecordingStatus.active


def test_mark_recording_ended(db_session):
    user_repo = MySQLUserRepository(db_session)
    user = user_repo.create_user(
        google_id="123456",
        email="[email protected]",
        display_name="Test User",
        avatar_url=None
    )
    
    recording_repo = MySQLRecordingRepository(db_session)
    recording = recording_repo.create_recording(user.id)
    
    updated = recording_repo.mark_ended(
        recording.id,
        "/path/to/audio.webm",
        "Test transcription"
    )
    
    assert updated.status == RecordingStatus.ended
    assert updated.audio_file_path == "/path/to/audio.webm"
    assert updated.transcription_text == "Test transcription"
