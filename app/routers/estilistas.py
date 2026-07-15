from fastapi import APIRouter, Depends, status
from supabase import Client

from app import crud
from app.database import get_supabase
from app.models.schemas import EstilistaCreate, EstilistaUpdate

router = APIRouter(prefix="/estilistas", tags=["Estilistas"])
TABLE = "estilista"


@router.get("", summary="Listar estilistas")
def listar_estilistas(
    skip: int = 0, limit: int = 100, db: Client = Depends(get_supabase)
):
    return crud.list_rows(db, TABLE, skip, limit)


@router.get("/{estilista_id}", summary="Obtener un estilista por id")
def obtener_estilista(estilista_id: str, db: Client = Depends(get_supabase)):
    return crud.get_row(db, TABLE, estilista_id)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Crear estilista")
def crear_estilista(estilista: EstilistaCreate, db: Client = Depends(get_supabase)):
    return crud.create_row(db, TABLE, estilista)


@router.put("/{estilista_id}", summary="Actualizar estilista")
def actualizar_estilista(
    estilista_id: str, estilista: EstilistaUpdate, db: Client = Depends(get_supabase)
):
    return crud.update_row(db, TABLE, estilista_id, estilista)


@router.delete("/{estilista_id}", summary="Eliminar estilista")
def eliminar_estilista(estilista_id: str, db: Client = Depends(get_supabase)):
    return crud.delete_row(db, TABLE, estilista_id)
