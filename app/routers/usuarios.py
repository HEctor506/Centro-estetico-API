from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Form, status
from supabase import Client

from app import crud
from app.database import get_supabase
from app.models.schemas import RolUsuario, UsuarioCreate, UsuarioUpdate

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
TABLE = "usuario"


@router.get("", summary="Listar usuarios")
def listar_usuarios(
    skip: int = 0, limit: int = 100, db: Client = Depends(get_supabase)
):
    return crud.list_rows(db, TABLE, skip, limit)


@router.get("/{usuario_id}", summary="Obtener un usuario por id")
def obtener_usuario(usuario_id: str, db: Client = Depends(get_supabase)):
    return crud.get_row(db, TABLE, usuario_id)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Crear usuario")
def crear_usuario(usuario: UsuarioCreate, db: Client = Depends(get_supabase)):
    return crud.create_row(db, TABLE, usuario)


@router.post(
    "/form",
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario (formulario)",
)
def crear_usuario_form(
    id: Annotated[UUID, Form(description="Debe coincidir con auth.users.id")],
    rol: Annotated[RolUsuario, Form()],
    activo: Annotated[bool, Form()] = True,
    db: Client = Depends(get_supabase),
):
    usuario = UsuarioCreate(id=id, rol=rol, activo=activo)
    return crud.create_row(db, TABLE, usuario)


@router.put("/{usuario_id}", summary="Actualizar usuario")
def actualizar_usuario(
    usuario_id: str, usuario: UsuarioUpdate, db: Client = Depends(get_supabase)
):
    return crud.update_row(db, TABLE, usuario_id, usuario)


@router.delete("/{usuario_id}", summary="Eliminar usuario")
def eliminar_usuario(usuario_id: str, db: Client = Depends(get_supabase)):
    return crud.delete_row(db, TABLE, usuario_id)
