"""
Centro Estético API
====================

REST API construida con FastAPI para la gestión de un centro estético:
usuarios, estilistas, clientes, servicios, citas, notificaciones e historial.
Los datos se almacenan en Supabase (PostgreSQL) sobre el esquema `beauty_api`,
protegido con Row Level Security.

Documentación interactiva (Swagger):  /docs
Documentación alternativa (ReDoc):     /redoc
"""
from fastapi import FastAPI

from app.routers import (
    auth,
    citas,
    clientes,
    estilistas,
    historial,
    notificaciones,
    servicios,
    usuarios,
)

app = FastAPI(
    title="Centro Estético API",
    description=(
        "API REST para la gestión de un centro estético (clientes, estilistas, "
        "servicios, citas, notificaciones e historial), con almacenamiento en "
        "Supabase.\n\n"
        "**Cómo probar:**\n"
        "1. Ejecuta `POST /auth/login` con tu correo y contraseña de Supabase.\n"
        "2. Copia el `access_token` de la respuesta.\n"
        "3. Pulsa **Authorize** (candado, arriba a la derecha) y pega el token.\n"
        "4. Ya puedes consumir el resto de endpoints."
    ),
    version="1.0.0",
    contact={"name": "Centro Estético API"},
)


@app.get("/", tags=["Inicio"], summary="Mensaje de bienvenida")
def read_root():
    return {
        "message": "Centro Estético API en funcionamiento",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health", tags=["Inicio"], summary="Estado del servicio")
def health_check():
    return {"status": "ok"}


# Registro de routers (cada recurso con su CRUD completo)
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(estilistas.router)
app.include_router(clientes.router)
app.include_router(servicios.router)
app.include_router(citas.router)
app.include_router(notificaciones.router)
app.include_router(historial.router)
