from fastapi import APIRouter, Depends, status
from supabase import Client

from app import crud
from app.database import get_supabase
from app.models.schemas import HistorialCitaCreate, HistorialCitaUpdate

router = APIRouter(prefix="/historial-citas", tags=["Historial de citas"])
TABLE = "historial_cita"


@router.get("", summary="Listar historial de citas")
def listar_historial(
    skip: int = 0, limit: int = 100, db: Client = Depends(get_supabase)
):
    return crud.list_rows(db, TABLE, skip, limit)


@router.get("/{historial_id}", summary="Obtener un registro de historial por id")
def obtener_historial(historial_id: str, db: Client = Depends(get_supabase)):
    return crud.get_row(db, TABLE, historial_id)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Crear registro de historial")
def crear_historial(
    historial: HistorialCitaCreate, db: Client = Depends(get_supabase)
):
    return crud.create_row(db, TABLE, historial)


@router.put("/{historial_id}", summary="Actualizar registro de historial")
def actualizar_historial(
    historial_id: str,
    historial: HistorialCitaUpdate,
    db: Client = Depends(get_supabase),
):
    return crud.update_row(db, TABLE, historial_id, historial)


@router.delete("/{historial_id}", summary="Eliminar registro de historial")
def eliminar_historial(historial_id: str, db: Client = Depends(get_supabase)):
    return crud.delete_row(db, TABLE, historial_id)
