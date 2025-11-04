# CRUSH Development Guide

## Build/Test Commands
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm install
npm run dev

# Docker Compose (recommended)
docker-compose up --build

# Tests
cd backend
pytest tests/
```

## Code Style Guidelines

### General Principles
- Use descriptive variable and function names
- Keep functions small and focused (single responsibility)
- Write self-documenting code; avoid unnecessary comments
- Use consistent indentation (2 spaces for JS/TS, 4 for Python)

### Error Handling
- Handle errors explicitly, don't ignore them
- Use appropriate error types for the language
- Log errors with sufficient context for debugging

### Imports/Dependencies
- Group imports: standard library, third-party, local
- Use absolute imports when possible
- Only import what you need

### Testing
- Write tests for new features and bug fixes
- Use descriptive test names that explain the scenario
- Follow AAA pattern: Arrange, Act, Assert

## Project Structure

### Backend (FastAPI)
- `app/api/` - API route handlers
- `app/core/` - Configuration and security
- `app/models/` - SQLAlchemy database models
- `app/repositories/` - Data access layer (repository pattern)
- `app/llm/` - LLM provider abstraction
- `app/services/` - Business logic services

### Frontend (React)
- `src/pages/` - Page components
- `src/components/` - Reusable components
- `src/hooks/` - Custom React hooks
- `src/services/` - API service layer

## Key Features
- Google OAuth2 authentication
- Audio recording with chunk streaming
- LLM-based transcription
- Repository pattern for database abstraction
- Bearer token authentication
- Notes functionality for recordings