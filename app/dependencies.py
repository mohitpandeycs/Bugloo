from fastapi import Request, HTTPException, status, Depends
from app.services.supabase_service import get_supabase
from supabase import Client
import traceback

def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    
    supabase = get_supabase()
    try:
        # Verify token by fetching user
        user_resp = supabase.auth.get_user(token)
        if not user_resp or not user_resp.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        return user_resp.user
    except Exception as e:
        print(f"Auth error: {str(e)}")
        # If token is invalid or expired
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired",
        )

def get_optional_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    
    supabase = get_supabase()
    try:
        user_resp = supabase.auth.get_user(token)
        if user_resp and user_resp.user:
            return user_resp.user
    except Exception:
        pass
    return None

