from fastapi import APIRouter, Depends, status
from supabase import Client

from app import crud
from app.database import get_supabase
from app.models.schemas import CitaCreate, CitaUpdate

router = APIRouter(prefix="/citas", tags=["Citas"])
TABLE = "cita"


@router.get("", summary="Listar citas")
def listar_citas(skip: int = 0, limit: int = 100, db: Client = Depends(get_supabase)):
    return crud.list_rows(db, TABLE, skip, limit)


@router.get("/{cita_id}", summary="Obtener una cita por id")
def obtener_cita(cita_id: str, db: Client = Depends(get_supabase)):
    return crud.get_row(db, TABLE, cita_id)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Crear cita")
def crear_cita(cita: CitaCreate, db: Client = Depends(get_supabase)):
    return crud.create_row(db, TABLE, cita)


@router.put("/{cita_id}", summary="Actualizar cita")
def actualizar_cita(
    cita_id: str, cita: CitaUpdate, db: Client = Depends(get_supabase)
):
    return crud.update_row(db, TABLE, cita_id, cita)


@router.delete("/{cita_id}", summary="Eliminar cita")
def eliminar_cita(cita_id: str, db: Client = Depends(get_supabase)):
    return crud.delete_row(db, TABLE, cita_id)
