"""
Funciones CRUD genéricas sobre el esquema beauty_api.

Centralizan el acceso a Supabase, la serialización de tipos
(UUID, Decimal, datetime, time) y el manejo de errores/respuestas HTTP,
para que cada router quede corto y legible.
"""
from typing import Any

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from supabase import Client

from app.database import SCHEMA


def _table(client: Client, table: str):
    return client.schema(SCHEMA).table(table)


def _clean(payload: dict, *, exclude_unset: bool = False) -> dict:
    """Convierte tipos de Pydantic (UUID, Decimal, datetime...) a JSON."""
    return jsonable_encoder(payload)


def list_rows(client: Client, table: str, skip: int = 0, limit: int = 100) -> list:
    try:
        resp = _table(client, table).select("*").range(skip, skip + limit - 1).execute()
        return resp.data
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al consultar '{table}': {exc}",
        )


def get_row(client: Client, table: str, row_id: str) -> dict:
    try:
        resp = _table(client, table).select("*").eq("id", row_id).execute()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al consultar '{table}': {exc}",
        )
    if not resp.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un registro en '{table}' con id {row_id}",
        )
    return resp.data[0]


def create_row(client: Client, table: str, data: Any) -> dict:
    payload = jsonable_encoder(data)
    try:
        resp = _table(client, table).insert(payload).execute()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudo crear el registro en '{table}': {exc}",
        )
    if not resp.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudo crear el registro en '{table}' "
            f"(revisa las políticas RLS o los datos enviados)",
        )
    return resp.data[0]


def update_row(client: Client, table: str, row_id: str, data: Any) -> dict:
    payload = jsonable_encoder(data, exclude_none=True)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes enviar al menos un campo para actualizar",
        )
    try:
        resp = _table(client, table).update(payload).eq("id", row_id).execute()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudo actualizar '{table}': {exc}",
        )
    if not resp.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un registro en '{table}' con id {row_id}",
        )
    return resp.data[0]


def delete_row(client: Client, table: str, row_id: str) -> dict:
    # Verifica existencia primero para devolver 404 correctamente
    get_row(client, table, row_id)
    try:
        _table(client, table).delete().eq("id", row_id).execute()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudo eliminar el registro de '{table}': {exc}",
        )
    return {"mensaje": f"Registro {row_id} eliminado de '{table}' correctamente"}
