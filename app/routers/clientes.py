from fastapi import APIRouter, Depends, status
from supabase import Client

from app import crud
from app.database import get_supabase
from app.models.schemas import ClienteCreate, ClienteUpdate

router = APIRouter(prefix="/clientes", tags=["Clientes"])
TABLE = "cliente"


@router.get("", summary="Listar clientes")
def listar_clientes(
    skip: int = 0, limit: int = 100, db: Client = Depends(get_supabase)
):
    return crud.list_rows(db, TABLE, skip, limit)


@router.get("/{cliente_id}", summary="Obtener un cliente por id")
def obtener_cliente(cliente_id: str, db: Client = Depends(get_supabase)):
    return crud.get_row(db, TABLE, cliente_id)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Crear cliente")
def crear_cliente(cliente: ClienteCreate, db: Client = Depends(get_supabase)):
    return crud.create_row(db, TABLE, cliente)


@router.put("/{cliente_id}", summary="Actualizar cliente")
def actualizar_cliente(
    cliente_id: str, cliente: ClienteUpdate, db: Client = Depends(get_supabase)
):
    return crud.update_row(db, TABLE, cliente_id, cliente)


@router.delete("/{cliente_id}", summary="Eliminar cliente")
def eliminar_cliente(cliente_id: str, db: Client = Depends(get_supabase)):
    return crud.delete_row(db, TABLE, cliente_id)
