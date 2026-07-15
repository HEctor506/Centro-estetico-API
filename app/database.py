"""
Configuración de la conexión con Supabase.

La API usa el esquema `beauty_api` (no `public`), por lo que todas las
consultas se hacen con `client.schema(SCHEMA).table(...)`.

Recuerda exponer el esquema `beauty_api` en Supabase:
  Dashboard -> Project Settings -> API -> Data API -> Exposed schemas
"""
import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY")
SCHEMA = "beauty_api"

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "Faltan las variables de entorno NEXT_PUBLIC_SUPABASE_URL / "
        "NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY"
    )

# Esquema de seguridad: se envía el JWT en el header Authorization: Bearer <token>
security = HTTPBearer(
    description="Pega aquí el access_token obtenido en POST /auth/login"
)


def get_supabase(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Client:
    """
    Crea un cliente de Supabase autenticado con el JWT del usuario.

    Las políticas RLS del proyecto exigen un usuario autenticado, por lo que
    todos los endpoints protegidos dependen de esta función.
    """
    token = credentials.credentials
    try:
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        client.postgrest.auth(token)
        return client
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de Supabase inválido o expirado",
        )
