"""
Modelos Pydantic (validación de entrada/salida) para cada recurso
del esquema beauty_api.

Por cada recurso se define:
  - <Recurso>Create : campos requeridos para crear (POST)
  - <Recurso>Update : todos los campos opcionales para actualizar (PUT)
"""
from datetime import datetime, time
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


# --------------------------------------------------------------------------- #
#  Enumeraciones (reflejan los CHECK de la base de datos)
# --------------------------------------------------------------------------- #
class RolUsuario(str, Enum):
    admin = "Admin"
    estilista = "Estilista"


class EstadoCita(str, Enum):
    pendiente = "Pendiente"
    confirmada = "Confirmada"
    cancelada = "Cancelada"
    completada = "Completada"


class TipoNotificacion(str, Enum):
    recordatorio = "Recordatorio"
    confirmacion = "Confirmacion"
    cancelacion = "Cancelacion"


class EstadoNotificacion(str, Enum):
    pendiente = "Pendiente"
    enviado = "Enviado"


class AccionHistorial(str, Enum):
    modificacion = "Modificacion"
    cancelacion = "Cancelacion"


# --------------------------------------------------------------------------- #
#  Usuario
# --------------------------------------------------------------------------- #
class UsuarioCreate(BaseModel):
    id: UUID = Field(..., description="Debe coincidir con auth.users.id (auth.uid())")
    rol: RolUsuario
    activo: bool = True


class UsuarioUpdate(BaseModel):
    rol: Optional[RolUsuario] = None
    activo: Optional[bool] = None


# --------------------------------------------------------------------------- #
#  Estilista
# --------------------------------------------------------------------------- #
class EstilistaCreate(BaseModel):
    usuario_id: UUID
    nombre: str = Field(..., max_length=150)
    especialidad: Optional[str] = Field(None, max_length=100)
    hora_entrada: time
    hora_salida: time


class EstilistaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=150)
    especialidad: Optional[str] = Field(None, max_length=100)
    hora_entrada: Optional[time] = None
    hora_salida: Optional[time] = None


# --------------------------------------------------------------------------- #
#  Cliente
# --------------------------------------------------------------------------- #
class ClienteCreate(BaseModel):
    nombre_completo: str = Field(..., max_length=150)
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    observaciones: Optional[str] = None


class ClienteUpdate(BaseModel):
    nombre_completo: Optional[str] = Field(None, max_length=150)
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    observaciones: Optional[str] = None


# --------------------------------------------------------------------------- #
#  Servicio
# --------------------------------------------------------------------------- #
class ServicioCreate(BaseModel):
    nombre: str = Field(..., max_length=100)
    descripcion: Optional[str] = None
    duracion_minutos: int = Field(..., gt=0)
    precio: Decimal = Field(..., ge=0, max_digits=10, decimal_places=2)


class ServicioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    duracion_minutos: Optional[int] = Field(None, gt=0)
    precio: Optional[Decimal] = Field(None, ge=0, max_digits=10, decimal_places=2)


# --------------------------------------------------------------------------- #
#  Cita
# --------------------------------------------------------------------------- #
class CitaCreate(BaseModel):
    cliente_id: UUID
    estilista_id: UUID
    servicio_id: UUID
    fecha_hora: datetime
    estado: EstadoCita = EstadoCita.pendiente


class CitaUpdate(BaseModel):
    cliente_id: Optional[UUID] = None
    estilista_id: Optional[UUID] = None
    servicio_id: Optional[UUID] = None
    fecha_hora: Optional[datetime] = None
    estado: Optional[EstadoCita] = None


# --------------------------------------------------------------------------- #
#  Notificacion
# --------------------------------------------------------------------------- #
class NotificacionCreate(BaseModel):
    cita_id: UUID
    tipo: TipoNotificacion
    estado: EstadoNotificacion = EstadoNotificacion.pendiente


class NotificacionUpdate(BaseModel):
    tipo: Optional[TipoNotificacion] = None
    estado: Optional[EstadoNotificacion] = None


# --------------------------------------------------------------------------- #
#  Historial de cita
# --------------------------------------------------------------------------- #
class HistorialCitaCreate(BaseModel):
    cita_id: UUID
    accion_realizada: AccionHistorial
    usuario_responsable: UUID


class HistorialCitaUpdate(BaseModel):
    accion_realizada: Optional[AccionHistorial] = None
    usuario_responsable: Optional[UUID] = None


# --------------------------------------------------------------------------- #
#  Auth
# --------------------------------------------------------------------------- #
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
