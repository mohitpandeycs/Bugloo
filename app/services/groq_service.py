import json
import httpx
from app.config import settings
from fastapi import HTTPException

GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

SYSTEM_PROMPT = """You are a senior software engineer performing a thorough code review.
The user will provide code. Your job is to:
1. If the language is "unknown", detect it yourself.
2. Analyze the code for bugs, style issues, and improvements.
3. Respond ONLY with a valid JSON object — no markdown, no explanation outside the JSON.

JSON format (all keys required):
{
  "language_detected": "<language name, e.g. Python>",
  "bugs": ["<bug description>", ...],
  "style_issues": ["<issue>", ...],
  "improvements": ["<suggestion>", ...],
  "quality_score": <integer 1-10>,
  "score_rationale": "<one sentence why>",
  "explanation": "<plain English: what does this code do?>"
}"""


def _extract_candidate_text(data: dict) -> str:
    candidates = data.get("candidates") or []
    if not candidates:
        return ""
    content = candidates[0].get("content") or {}
    parts = content.get("parts") or []
    if not parts:
        return ""
    return parts[0].get("text") or ""


def _clean_json_text(raw: str) -> str:
    if not raw:
        return ""
    cleaned = raw.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    start_idx = cleaned.find("{")
    end_idx = cleaned.rfind("}")
    if start_idx != -1 and end_idx != -1:
        cleaned = cleaned[start_idx:end_idx + 1]
    return cleaned


async def get_code_review(code: str, detected_language: str) -> dict:
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        raise HTTPException(status_code=500, detail="Gemini API Key missing.")

    url = f"{GEMINI_ENDPOINT}?key={api_key}"
    headers = {
        "Content-Type": "application/json"
    }

    user_prompt = f"Language hint: {detected_language}\nReview this code:\n\n{code}"
    payload = {
        "contents": [
            {
                "parts": [{"text": user_prompt}]
            }
        ],
        "systemInstruction": {
            "parts": [{"text": SYSTEM_PROMPT}]
        },
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.2
        }
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=20.0)

        if response.status_code == 429:
            raise HTTPException(status_code=429, detail="You've hit the rate limit. Please wait 30 seconds and try again.")
        if response.status_code == 401 or response.status_code == 403:
            raise HTTPException(status_code=500, detail="AI service rejected the API key.")
        if response.status_code >= 500:
            raise HTTPException(status_code=503, detail="Couldn't reach the AI service. Check your connection and retry.")
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Internal configuration error. Please contact the admin.")

        data = response.json()
        raw_content = _extract_candidate_text(data)
        cleaned = _clean_json_text(raw_content)
        if not cleaned:
            raise HTTPException(status_code=500, detail="Unexpected response format from AI service.")

        review_json = json.loads(cleaned)
        return review_json
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="The AI took too long to respond. Please try again.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Review parsing failed. Showing raw response below.\n" + raw_content)
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Couldn't reach the AI service. Check your connection and retry.")
