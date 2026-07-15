"""
Autenticación contra Supabase Auth.

El endpoint /auth/login devuelve el access_token (JWT) que luego se usa
en el botón "Authorize" de Swagger para consumir el resto de endpoints.
"""
import requests
from fastapi import APIRouter, HTTPException, status

from app.database import SUPABASE_KEY, SUPABASE_URL
from app.models.schemas import LoginRequest

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", summary="Iniciar sesión y obtener JWT")
def login(credenciales: LoginRequest):
    url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"
    headers = {"apikey": SUPABASE_KEY, "Content-Type": "application/json"}
    payload = {"email": credenciales.email, "password": credenciales.password}

    resp = requests.post(url, json=payload, headers=headers, timeout=15)
    if resp.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas en Supabase",
        )

    data = resp.json()
    return {
        "access_token": data.get("access_token"),
        "token_type": "bearer",
        "refresh_token": data.get("refresh_token"),
        "expires_in": data.get("expires_in"),
    }
