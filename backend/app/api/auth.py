from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.models import get_db
from app.repositories.user_repository import MySQLUserRepository
from app.services.auth_service import oauth
from app.core.security import create_access_token
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/google/login")
async def google_login(request: Request):
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")
    
    user_info = token.get('userinfo')
    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to get user info")
    
    google_id = user_info.get('sub')
    email = user_info.get('email')
    display_name = user_info.get('name', email)
    avatar_url = user_info.get('picture')
    
    user_repo = MySQLUserRepository(db)
    user = user_repo.get_user_by_google_id(google_id)
    
    if not user:
        user = user_repo.create_user(
            google_id=google_id,
            email=email,
            display_name=display_name,
            avatar_url=avatar_url
        )
    
    access_token = create_access_token(data={"sub": user.id})
    
    redirect_url = f"{settings.FRONTEND_URL}/dashboard?token={access_token}"
    return RedirectResponse(url=redirect_url)
