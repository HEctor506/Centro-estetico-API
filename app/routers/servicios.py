from fastapi import APIRouter, Depends, status
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


@router.put("/{servicio_id}", summary="Actualizar servicio")
def actualizar_servicio(
    servicio_id: str, servicio: ServicioUpdate, db: Client = Depends(get_supabase)
):
    return crud.update_row(db, TABLE, servicio_id, servicio)


@router.delete("/{servicio_id}", summary="Eliminar servicio")
def eliminar_servicio(servicio_id: str, db: Client = Depends(get_supabase)):
    return crud.delete_row(db, TABLE, servicio_id)
