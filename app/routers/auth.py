from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from app.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, REDIRECT_URI
import requests

router = APIRouter()

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

@router.get("/login")
def login():
    """Redirect the user to Google's OAuth 2.0 endpoint."""
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
    }
    url = f"{GOOGLE_AUTH_URL}?{requests.compat.urlencode(params)}"
    return RedirectResponse(url)

@router.get("/auth/callback")
def auth_callback(request: Request):
    """Handle Google's OAuth 2.0 response."""
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not found")

    # Exchange authorization code for access token
    token_data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }
    token_response = requests.post(GOOGLE_TOKEN_URL, data=token_data)
    token_response_data = token_response.json()

    if "error" in token_response_data:
        raise HTTPException(status_code=400, detail=token_response_data["error"])

    access_token = token_response_data["access_token"]

    # Retrieve user info
    headers = {"Authorization": f"Bearer {access_token}"}
    userinfo_response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
    userinfo = userinfo_response.json()

    return {"userinfo": userinfo}
