from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.dependencies import get_current_user, get_optional_user
from app.services.groq_service import get_code_review
from app.services.supabase_service import get_supabase
import json
from pathlib import Path

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, user=Depends(get_optional_user)):
    return templates.TemplateResponse(request=request, name="landing.html", context={"user": user})

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse(request=request, name="index.html", context={"user": user})


@router.post("/api/review")
async def create_review(
    request: Request, 
    code: str = Form(...), 
    detected_language: str = Form(default="unknown"),
    user=Depends(get_current_user)
):
    if not code or len(code.strip()) < 10:
        raise HTTPException(status_code=400, detail="Please paste at least 10 characters of code.")
        
    try:
        # 1. Get review from Groq
        review_data = await get_code_review(code, detected_language)
        
        # 2. Save to Supabase
        supabase = get_supabase()
        warning = None
        try:
            supabase.table("reviews").insert({
                "user_id": user.id,
                "detected_language": review_data.get("language_detected", detected_language),
                "code": code,
                "review_json": review_data,
                "quality_score": review_data.get("quality_score", 0)
            }).execute()
        except Exception as e:
            print(f"Failed to save to Supabase: {e}")
            warning = "Review generated but couldn't be saved to history."
            
        response_data = {"review": review_data}
        if warning:
            response_data["warning"] = warning
            
        return JSONResponse(content=response_data)
        
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": "Something went wrong. Please try again."})
