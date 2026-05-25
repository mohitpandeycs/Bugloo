from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.dependencies import get_current_user
from app.services.supabase_service import get_supabase

router = APIRouter(tags=["History"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/history", response_class=HTMLResponse)
async def get_history(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("history.html", {"request": request, "user": user})

@router.get("/api/history")
async def fetch_history_api(user=Depends(get_current_user)):
    try:
        supabase = get_supabase()
        response = supabase.table("reviews").select("*").eq("user_id", user.id).order("created_at", desc=True).execute()
        return {"data": response.data}
    except Exception as e:
        print(f"Error fetching history: {e}")
        return {"error": "Couldn't load your history. Please refresh."}
