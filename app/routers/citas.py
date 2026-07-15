from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Form, status
from supabase import Client

from app import crud
from app.database import get_supabase
from app.models.schemas import CitaCreate, CitaUpdate, EstadoCita

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


@router.post(
    "/form",
    status_code=status.HTTP_201_CREATED,
    summary="Crear cita (formulario)",
)
def crear_cita_form(
    cliente_id: Annotated[UUID, Form()],
    estilista_id: Annotated[UUID, Form()],
    servicio_id: Annotated[UUID, Form()],
    fecha_hora: Annotated[datetime, Form()],
    estado: Annotated[EstadoCita, Form()] = EstadoCita.pendiente,
    db: Client = Depends(get_supabase),
):
    cita = CitaCreate(
        cliente_id=cliente_id,
        estilista_id=estilista_id,
        servicio_id=servicio_id,
        fecha_hora=fecha_hora,
        estado=estado,
    )
    return crud.create_row(db, TABLE, cita)


@router.put("/{cita_id}", summary="Actualizar cita")
def actualizar_cita(
    cita_id: str, cita: CitaUpdate, db: Client = Depends(get_supabase)
):
    return crud.update_row(db, TABLE, cita_id, cita)


@router.delete("/{cita_id}", summary="Eliminar cita")
def eliminar_cita(cita_id: str, db: Client = Depends(get_supabase)):
    return crud.delete_row(db, TABLE, cita_id)
