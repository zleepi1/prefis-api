# models.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DECIMAL,
    Date,
    TIMESTAMP,
    ForeignKey,
    BigInteger,
)
from sqlalchemy.orm import relationship
from database import Base
import datetime

# --- Tablas Principales ---


class Usuario(Base):
    __tablename__ = "USUARIOS"
    usuario_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    fecha_registro = Column(Date, nullable=False, default=datetime.date.today)
    rol = Column(String(20), nullable=False, default="investigador")
    esta_activo = Column(Boolean, nullable=False, default=True)

    # Relación: Un Usuario puede tener muchos Registros de Cálculo
    calculos = relationship("RegistroCalculo", back_populates="usuario")


class ModeloAnalisis(Base):
    __tablename__ = "MODELO_ANALISIS"
    modelo_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)
    activo_web = Column(Boolean, nullable=False)
    activo_movil = Column(Boolean, nullable=False)

    # Relaciones: Un Modelo puede tener muchos...
    documentacion = relationship(
        "DocumentacionTeorica", back_populates="modelo", cascade="all, delete-orphan"
    )
    recursos = relationship(
        "RecursoAnsys", back_populates="modelo", cascade="all, delete-orphan"
    )
    calculos = relationship("RegistroCalculo", back_populates="modelo")


class Geometria(Base):
    __tablename__ = "GEOMETRIA"
    geometria_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    imagen_url = Column(String(255), nullable=True)

    # Relación: Una Geometría puede estar en muchos Registros de Cálculo
    calculos = relationship("RegistroCalculo", back_populates="geometria")


# --- Tablas de Relación / Contenido ---


class RegistroCalculo(Base):
    __tablename__ = "REGISTRO_CALCULO"
    registro_id = Column(BigInteger, primary_key=True, index=True)
    valor_entrada_grieta = Column(DECIMAL(10, 4), nullable=False)
    valor_salida_esfuerzo = Column(DECIMAL(10, 4), nullable=False)
    plataforma = Column(String(10), nullable=False)
    fecha_calculo = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now)
    esta_activo = Column(Boolean, nullable=False, default=True)

    # Claves Foráneas (FK)
    usuario_id = Column(Integer, ForeignKey("USUARIOS.usuario_id"))
    modelo_id = Column(Integer, ForeignKey("MODELO_ANALISIS.modelo_id"))
    geometria_id = Column(Integer, ForeignKey("GEOMETRIA.geometria_id"))

    # Relaciones (Lado "muchos" de la relación)
    usuario = relationship("Usuario", back_populates="calculos")
    modelo = relationship("ModeloAnalisis", back_populates="calculos")
    geometria = relationship("Geometria", back_populates="calculos")


class DocumentacionTeorica(Base):
    __tablename__ = "DOCUMENTACION_TEORICA"
    teoria_id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    contenido_html = Column(Text, nullable=False)

    # Clave Foránea (FK)
    modelo_id = Column(Integer, ForeignKey("MODELO_ANALISIS.modelo_id"))

    # Relación
    modelo = relationship("ModeloAnalisis", back_populates="documentacion")


class RecursoAnsys(Base):
    __tablename__ = "RECURSO_ANSYS"
    recurso_id = Column(Integer, primary_key=True, index=True)
    nombre_archivo = Column(String(100), nullable=False)
    enlace_descarga = Column(String(255), nullable=False)

    # Clave Foránea (FK)
    modelo_id = Column(Integer, ForeignKey("MODELO_ANALISIS.modelo_id"))

    # Relación
    modelo = relationship("ModeloAnalisis", back_populates="recursos")
