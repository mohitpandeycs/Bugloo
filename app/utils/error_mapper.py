def map_auth_error(error_msg: str) -> str:
    msg_lower = error_msg.lower()
    if any(term in msg_lower for term in ["connection", "network", "timeout", "offline", "cannot connect", "failed to connect", "unreachable"]):
        return "Authentication service is unavailable. Please try again shortly."
    if "invalid login credentials" in msg_lower or "invalid_credentials" in msg_lower:
        return "Incorrect email or password. Please try again."
    if "already registered" in msg_lower or "user_already_exists" in msg_lower:
        return "An account with this email already exists. Try logging in."
    if "weak_password" in msg_lower or "password should be at least" in msg_lower:
        return "Password must be at least 8 characters."
    if "invalid_email" in msg_lower or "valid email" in msg_lower:
        return "Please enter a valid email address."
    return "Something went wrong. Please try again."

def map_groq_error(status_code: int, error_msg: str) -> dict:
    if status_code == 400:
        return {"status": 400, "message": "Please paste at least 10 characters of code."}
    elif status_code == 504:
        return {"status": 504, "message": "The AI took too long to respond. Please try again."}
    elif status_code == 429:
        return {"status": 429, "message": "You've hit the rate limit. Please wait 30 seconds and try again."}
    elif status_code == 503:
        return {"status": 503, "message": "Couldn't reach the AI service. Check your connection and retry."}
    else:
        return {"status": 500, "message": "Internal configuration error. Please contact the admin."}