# crud.py
from sqlalchemy.orm import Session
import models
import schemas
import security
import datetime

# --- CRUD de USUARIOS ---


def get_user_by_email(db: Session, email: str): 
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()


def create_user(db: Session, user: schemas.UsuarioCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.Usuario(
        email=user.email,
        nombre=user.nombre,
        password_hash=hashed_password,
        fecha_registro=datetime.date.today(),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# --- CRUD de MODELO_ANALISIS ---


def get_modelo(db: Session, modelo_id: int):
    return (
        db.query(models.ModeloAnalisis)
        .filter(models.ModeloAnalisis.modelo_id == modelo_id)
        .first()
    )


def get_modelos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ModeloAnalisis).offset(skip).limit(limit).all()


def create_modelo(db: Session, modelo: schemas.ModeloAnalisisBase):
    db_modelo = models.ModeloAnalisis(**modelo.dict())
    db.add(db_modelo)
    db.commit()
    db.refresh(db_modelo)
    return db_modelo


# --- CRUD de GEOMETRIA ---


def get_geometrias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Geometria).offset(skip).limit(limit).all()


def create_geometria(db: Session, geometria: schemas.GeometriaBase):
    db_geometria = models.Geometria(**geometria.dict())
    db.add(db_geometria)
    db.commit()
    db.refresh(db_geometria)
    return db_geometria


# --- CRUD de REGISTRO_CALCULO ---


def create_registro_calculo(
    db: Session, calculo: schemas.RegistroCalculoCreate, usuario_id: int
):
    # **calculo.dict() expande el Pydantic model a kwargs para el SQLAlchemy model
    db_calculo = models.RegistroCalculo(**calculo.dict(), usuario_id=usuario_id)
    db.add(db_calculo)
    db.commit()
    db.refresh(db_calculo)
    return db_calculo


def get_calculos_by_user(db: Session, usuario_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.RegistroCalculo)
        .filter(models.RegistroCalculo.usuario_id == usuario_id)
        .order_by(models.RegistroCalculo.fecha_calculo.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_calculo_by_id_and_owner(db: Session, registro_id: int, usuario_id: int):
    """
    Busca un cálculo específico, pero solo si le pertenece al usuario_id.
    Esto previene que un usuario borre los cálculos de otro.
    """
    return (
        db.query(models.RegistroCalculo)
        .filter(
            models.RegistroCalculo.registro_id == registro_id,
            models.RegistroCalculo.usuario_id == usuario_id,
        )
        .first()
    )


def delete_calculo(db: Session, db_calculo: models.RegistroCalculo):
    """
    Elimina un registro de cálculo de la base de datos.
    """
    db.delete(db_calculo)
    db.commit()
    return db_calculo


# --- CRUD de Contenido (Documentacion y Recursos) ---


def get_documentacion_by_modelo(db: Session, modelo_id: int):
    return (
        db.query(models.DocumentacionTeorica)
        .filter(models.DocumentacionTeorica.modelo_id == modelo_id)
        .all()
    )


def get_recursos_by_modelo(db: Session, modelo_id: int):
    return (
        db.query(models.RecursoAnsys)
        .filter(models.RecursoAnsys.modelo_id == modelo_id)
        .all()
    )


def create_batch_calculos(
    db: Session, calculos: list[schemas.RegistroCalculoCreate], usuario_id: int
):
    """
    Toma una LISTA de objetos de cálculo, les asigna el ID de usuario,
    y los guarda todos en la base de datos en una sola transacción.
    """
    db_calculos = []

    # 1. Convierte todos los schemas de Pydantic a modelos de SQLAlchemy
    for calculo in calculos:
        db_calculo = models.RegistroCalculo(
            **calculo.dict(),  # Desempaqueta el objeto: modelo_id, geometria_id, etc.
            usuario_id=usuario_id
        )
        db.add(db_calculo)
        db_calculos.append(db_calculo)

    # 2. Confirma (commit) todos los cambios a la vez
    try:
        db.commit()
    except Exception as e:
        db.rollback()  # Si uno falla, ninguno se guarda
        raise e

    # 3. Refresca todos los objetos para obtener sus nuevos IDs de la BD
    for db_calculo in db_calculos:
        db.refresh(db_calculo)

    return db_calculos
