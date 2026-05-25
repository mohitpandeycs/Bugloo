from fastapi import APIRouter, Request, Form, Response, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.supabase_service import get_supabase
from app.utils.error_mapper import map_auth_error

router = APIRouter(tags=["Auth"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/auth", response_class=HTMLResponse)
async def get_auth_page(request: Request):
    # If user already has a token, we might want to verify and redirect, 
    # but for simplicity, just show auth page. 
    # If they are valid, they shouldn't be here typically, but we let them be or redirect.
    token = request.cookies.get("access_token")
    if token:
        try:
            supabase = get_supabase()
            user = supabase.auth.get_user(token)
            if user:
                return RedirectResponse(url="/dashboard", status_code=303)
        except Exception:
            pass
            
    return templates.TemplateResponse("auth.html", {"request": request, "error": None})

@router.post("/auth/login", response_class=HTMLResponse)
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    supabase = get_supabase()
    try:
        auth_response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if auth_response.session:
            response = RedirectResponse(url="/dashboard", status_code=303)
            # 7 days max age
            response.set_cookie(key="access_token", value=auth_response.session.access_token, httponly=True, max_age=604800, samesite="lax")
            return response
    except Exception as e:
        error_msg = map_auth_error(str(e))
        return templates.TemplateResponse("auth.html", {"request": request, "error": error_msg, "is_signup": False, "email": email})

@router.post("/auth/signup", response_class=HTMLResponse)
async def signup(request: Request, email: str = Form(...), password: str = Form(...)):
    supabase = get_supabase()
    try:
        auth_response = supabase.auth.sign_up({"email": email, "password": password})
        # Note: If email confirmations are disabled, session is returned immediately
        if auth_response.session:
            response = RedirectResponse(url="/dashboard", status_code=303)
            response.set_cookie(key="access_token", value=auth_response.session.access_token, httponly=True, max_age=604800, samesite="lax")
            return response
        else:
            return templates.TemplateResponse("auth.html", {"request": request, "error": "Sign up successful but no session returned. Please log in.", "is_signup": True})
    except Exception as e:
        error_msg = map_auth_error(str(e))
        return templates.TemplateResponse("auth.html", {"request": request, "error": error_msg, "is_signup": True, "email": email})

@router.get("/auth/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/auth", status_code=303)
    response.delete_cookie("access_token")
    return response