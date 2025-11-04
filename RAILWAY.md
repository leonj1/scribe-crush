# Railway Deployment Guide

## Services Required

This project requires 3 services on Railway:

1. **MySQL Database**
2. **Backend API**
3. **Frontend**

## Setup Instructions

### 1. Create MySQL Database Service

- Add a new service → Database → MySQL
- Note the connection details (Railway will provide these as environment variables)

### 2. Deploy Backend Service

Create a new service from this repo and set the following environment variables:

```
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
LLM_API_KEY=your_llm_api_key
MYSQL_URL=${{MySQL.DATABASE_URL}}
AUDIO_STORAGE_PATH=/app/audio_storage
JWT_SECRET=your_secure_random_jwt_secret
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=10080
FRONTEND_URL=${{Frontend.RAILWAY_PUBLIC_DOMAIN}}
PORT=8000
```

Root directory: `/backend`

### 3. Deploy Frontend Service

Create a new service from this repo and set the following environment variables:

```
VITE_API_URL=${{Backend.RAILWAY_PUBLIC_DOMAIN}}
PORT=3000
```

Root directory: `/frontend`

Build command: `npm install && npm run build`
Start command: `npm run preview -- --host 0.0.0.0 --port $PORT`

## Environment Variables Reference

### Backend
- `GOOGLE_CLIENT_ID` - Google OAuth client ID
- `GOOGLE_CLIENT_SECRET` - Google OAuth client secret
- `LLM_API_KEY` - API key for LLM provider
- `MYSQL_URL` - MySQL connection string (use Railway's reference variable)
- `AUDIO_STORAGE_PATH` - Path for audio file storage
- `JWT_SECRET` - Secret key for JWT token generation
- `FRONTEND_URL` - Frontend URL for CORS (use Railway's reference variable)

### Frontend
- `VITE_API_URL` - Backend API URL (use Railway's reference variable)

## Notes

- Railway will automatically detect the Nixpacks configuration
- Make sure to set up the MySQL database first before deploying the backend
- Use Railway's reference variables (e.g., `${{MySQL.DATABASE_URL}}`) to link services
- Generate a secure random string for `JWT_SECRET`
