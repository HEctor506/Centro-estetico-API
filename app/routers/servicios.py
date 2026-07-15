from decimal import Decimal
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Form, status
from supabase import Client

from app import crud
from app.database import get_supabase
from app.models.schemas import ServicioCreate, ServicioUpdate

router = APIRouter(prefix="/servicios", tags=["Servicios"])
TABLE = "servicio"


@router.get("", summary="Listar servicios")
def listar_servicios(
    skip: int = 0, limit: int = 100, db: Client = Depends(get_supabase)
):
    return crud.list_rows(db, TABLE, skip, limit)


@router.get("/{servicio_id}", summary="Obtener un servicio por id")
def obtener_servicio(servicio_id: str, db: Client = Depends(get_supabase)):
    return crud.get_row(db, TABLE, servicio_id)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Crear servicio")
def crear_servicio(servicio: ServicioCreate, db: Client = Depends(get_supabase)):
    return crud.create_row(db, TABLE, servicio)


@router.post(
    "/form",
    status_code=status.HTTP_201_CREATED,
    summary="Crear servicio (formulario)",
)
def crear_servicio_form(
    nombre: Annotated[str, Form(max_length=100)],
    duracion_minutos: Annotated[int, Form(gt=0)],
    precio: Annotated[Decimal, Form(ge=0)],
    descripcion: Annotated[Optional[str], Form()] = None,
    db: Client = Depends(get_supabase),
):
    servicio = ServicioCreate(
        nombre=nombre,
        descripcion=descripcion or None,
        duracion_minutos=duracion_minutos,
        precio=precio,
    )
    return crud.create_row(db, TABLE, servicio)


@router.put("/{servicio_id}", summary="Actualizar servicio")
def actualizar_servicio(
    servicio_id: str, servicio: ServicioUpdate, db: Client = Depends(get_supabase)
):
    return crud.update_row(db, TABLE, servicio_id, servicio)


@router.delete("/{servicio_id}", summary="Eliminar servicio")
def eliminar_servicio(servicio_id: str, db: Client = Depends(get_supabase)):
    return crud.delete_row(db, TABLE, servicio_id)
