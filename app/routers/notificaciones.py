from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Form, status
from supabase import Client

from app import crud
from app.database import get_supabase
from app.models.schemas import (
    EstadoNotificacion,
    NotificacionCreate,
    NotificacionUpdate,
    TipoNotificacion,
)

router = APIRouter(prefix="/notificaciones", tags=["Notificaciones"])
TABLE = "notificacion"


@router.get("", summary="Listar notificaciones")
def listar_notificaciones(
    skip: int = 0, limit: int = 100, db: Client = Depends(get_supabase)
):
    return crud.list_rows(db, TABLE, skip, limit)


@router.get("/{notificacion_id}", summary="Obtener una notificación por id")
def obtener_notificacion(notificacion_id: str, db: Client = Depends(get_supabase)):
    return crud.get_row(db, TABLE, notificacion_id)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Crear notificación")
def crear_notificacion(
    notificacion: NotificacionCreate, db: Client = Depends(get_supabase)
):
    return crud.create_row(db, TABLE, notificacion)


@router.post(
    "/form",
    status_code=status.HTTP_201_CREATED,
    summary="Crear notificación (formulario)",
)
def crear_notificacion_form(
    cita_id: Annotated[UUID, Form()],
    tipo: Annotated[TipoNotificacion, Form()],
    estado: Annotated[EstadoNotificacion, Form()] = EstadoNotificacion.pendiente,
    db: Client = Depends(get_supabase),
):
    notificacion = NotificacionCreate(cita_id=cita_id, tipo=tipo, estado=estado)
    return crud.create_row(db, TABLE, notificacion)


@router.put("/{notificacion_id}", summary="Actualizar notificación")
def actualizar_notificacion(
    notificacion_id: str,
    notificacion: NotificacionUpdate,
    db: Client = Depends(get_supabase),
):
    return crud.update_row(db, TABLE, notificacion_id, notificacion)


@router.delete("/{notificacion_id}", summary="Eliminar notificación")
def eliminar_notificacion(notificacion_id: str, db: Client = Depends(get_supabase)):
    return crud.delete_row(db, TABLE, notificacion_id)
