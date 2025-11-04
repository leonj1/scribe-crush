# Audio Transcription Service

A secure platform for healthcare professionals to record and transcribe patient notes.

## Features

- Google OAuth2 authentication
- Long audio recording with chunk streaming
- Automatic transcription via LLM provider
- Dashboard to manage recordings
- Notes functionality for recording sessions
- HIPAA-compliant design

## Architecture

### Backend (FastAPI)
- Google OAuth2 authentication
- Bearer token-based sessions
- MySQL database with SQLAlchemy ORM
- Repository pattern for data access
- Abstracted LLM provider interface
- Audio chunk assembly and storage

### Frontend (React + Ant Design)
- Landing page with Google login
- Dashboard with recording management
- Real-time audio recording with pause/resume
- Chunk streaming to backend
- Transcription viewing and notes

## Setup

### Prerequisites
- Docker and Docker Compose
- Google OAuth2 credentials
- LLM API key (RequestYAI)

### Environment Variables

Create a `.env` file in the root directory:

```bash
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
LLM_API_KEY=your_llm_api_key
JWT_SECRET=your_jwt_secret_key
```

### Running with Docker Compose

```bash
docker compose up --build
```

Services will be available at:
- Frontend: http://localhost:9501
- Backend API: http://localhost:9500
- Backend Swagger Docs: http://localhost:9500/docs
- MySQL: localhost:3307

### Managing Services

Use the Makefile:

```bash
# Start all services
make start

# Stop all services
make stop

# Restart all services
make restart

# View logs
make logs

# Check status
make status
```

Or use the management script:

```bash
# Start all services
./manage.sh start

# Stop all services
./manage.sh stop

# Restart all services
./manage.sh restart

# View logs
./manage.sh logs

# Check status
./manage.sh status
```

Or use docker compose directly:

```bash
# Start services
docker compose up -d

# Stop services
docker compose stop

# Stop and remove containers
docker compose down

# View logs
docker compose logs -f

# Check status
docker compose ps
```

### Development Setup

#### Backend

```bash
cd backend
cp .env.example .env
# Edit .env with your credentials
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

### Authentication
- `GET /auth/google/login` - Initiate Google OAuth2 login
- `GET /auth/google/callback` - Handle OAuth2 callback

### Recordings
- `POST /recordings` - Create new recording session
- `GET /recordings` - List user's recordings
- `GET /recordings/{id}` - Get recording details
- `POST /recordings/{id}/chunks` - Upload audio chunk
- `PATCH /recordings/{id}/pause` - Pause recording
- `POST /recordings/{id}/finish` - Finish and transcribe
- `PATCH /recordings/{id}/notes` - Update recording notes

## Testing

```bash
cd backend
pytest tests/
```

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Config and security
│   │   ├── llm/          # LLM provider interface
│   │   ├── models/       # Database models
│   │   ├── repositories/ # Data access layer
│   │   └── services/     # Business logic
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

## Security

- All API endpoints (except auth) require Bearer token authentication
- Audio data stored with encryption at rest
- HTTPS/TLS required for production
- HIPAA-compliant design principles

## License

Proprietary
