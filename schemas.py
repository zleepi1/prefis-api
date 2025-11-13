# schemas.py
from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List


# --- Esquemas para GEOMETRIA ---
class GeometriaBase(BaseModel):
    nombre: str
    imagen_url: Optional[str] = None


class Geometria(GeometriaBase):
    geometria_id: int

    class Config:
        orm_mode = True


# --- Esquemas para MODELO_ANALISIS ---
class ModeloAnalisisBase(BaseModel):
    nombre: str
    descripcion: str
    activo_web: bool
    activo_movil: bool


class ModeloAnalisis(ModeloAnalisisBase):
    modelo_id: int

    class Config:
        orm_mode = True


# --- Esquemas para DOCUMENTACION_TEORICA ---
class DocumentacionTeoricaBase(BaseModel):
    titulo: str
    contenido_html: str
    modelo_id: int


class DocumentacionTeorica(DocumentacionTeoricaBase):
    teoria_id: int

    class Config:
        orm_mode = True


# --- Esquemas para RECURSO_ANSYS ---
class RecursoAnsysBase(BaseModel):
    nombre_archivo: str
    enlace_descarga: str
    modelo_id: int


class RecursoAnsys(RecursoAnsysBase):
    recurso_id: int

    class Config:
        orm_mode = True


# --- Esquemas para USUARIOS ---
# Este es el esquema base, usado para leer
class UsuarioBase(BaseModel):
    email: EmailStr
    nombre: str


# Esquema para crear un usuario (incluye contraseña)
class UsuarioCreate(UsuarioBase):
    password: str


# Esquema para leer un usuario de la BD (NO incluye contraseña)
class Usuario(UsuarioBase):
    usuario_id: int
    fecha_registro: date
    rol: str
    esta_activo: bool

    class Config:
        orm_mode = True

# Esquema para cambiar el nombre de un usuario
class UserUpdate(BaseModel):
    nombre: str


# --- Esquemas para REGISTRO_CALCULO ---
# Esquema para crear un nuevo registro
class RegistroCalculoCreate(BaseModel):
    modelo_id: int
    geometria_id: int
    valor_entrada_grieta: Decimal
    valor_salida_esfuerzo: Decimal
    plataforma: str  # "web" o "movil"


# Esquema para leer un registro (respuesta de la API)
class RegistroCalculo(BaseModel):
    registro_id: int
    fecha_calculo: datetime
    valor_entrada_grieta: Decimal
    valor_salida_esfuerzo: Decimal
    plataforma: str

    # ¡Aquí está la magia!
    # En lugar de solo IDs, anidamos los esquemas completos.
    usuario: Usuario
    modelo: ModeloAnalisis
    geometria: Geometria

    class Config:
        orm_mode = True


# --- Esquemas para Autenticación (Paso Siguiente) ---
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
