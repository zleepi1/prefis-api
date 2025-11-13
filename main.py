# main.py
from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware

# Importa todo de tus otros archivos
import models
import schemas
import crud
import security
from database import SessionLocal, engine

# Crea las tablas en la base de datos (solo si no existen)
# En producción, podrías usar una herramienta de migración como Alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Proyect_PREFIS API",
    description="API para gestionar modelos, cálculos y usuarios del proyecto PREFIS.",
    version="1.0.0",
)

# 2. DEFINE LOS ORÍGENES PERMITIDOS
origins = [
    "http://localhost",
    "http://localhost:5173",  # El origen de tu app de React
    "0.0.0.0"
]

# 3. AÑADE EL MIDDLEWARE A TU APP
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)


# --- Dependencia de la Base de Datos ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- 1. ENDPOINTS DE AUTENTICACIÓN Y USUARIOS ---


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Endpoint de Login.
    Recibe un 'username' (que es el email) y 'password' en un form-data.
    Devuelve un token JWT.
    """
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.password_hash): # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post(
    "/usuarios/", response_model=schemas.Usuario, status_code=status.HTTP_201_CREATED
)
def register_user(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario en la base de datos.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    return crud.create_user(db=db, user=user)


@app.get("/usuarios/me/", response_model=schemas.Usuario)
def read_users_me(
    current_user: schemas.Usuario = Depends(security.get_current_active_user),
):
    """
    Obtiene la información del usuario actualmente autenticado. (Protegido)
    """
    return current_user


# --- 2. ENDPOINTS DE MODELO_ANALISIS ---


@app.post(
    "/modelos/",
    response_model=schemas.ModeloAnalisis,
    status_code=status.HTTP_201_CREATED,
)
def create_modelo_analisis(
    modelo: schemas.ModeloAnalisisBase,
    db: Session = Depends(get_db),
    # Protegido: Solo un administrador puede crear modelos.
    admin_user: schemas.Usuario = Depends(security.get_current_admin_user),
):
    """
    Crea un nuevo modelo de análisis. (Protegido - Solo Admin)
    """
    return crud.create_modelo(db=db, modelo=modelo)


@app.get("/modelos/", response_model=list[schemas.ModeloAnalisis])
def read_modelos_analisis(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtiene una lista de todos los modelos de análisis. (Público)
    """
    modelos = crud.get_modelos(db, skip=skip, limit=limit)
    return modelos


@app.get("/modelos/{modelo_id}", response_model=schemas.ModeloAnalisis)
def read_modelo_analisis(modelo_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un modelo de análisis específico por su ID. (Público)
    """
    db_modelo = crud.get_modelo(db, modelo_id=modelo_id)
    if db_modelo is None:
        raise HTTPException(status_code=404, detail="Modelo no encontrado")
    return db_modelo


# --- 3. ENDPOINTS DE GEOMETRIA ---


@app.post(
    "/geometrias/",
    response_model=schemas.Geometria,
    status_code=status.HTTP_201_CREATED,
)
def create_geometria(
    geometria: schemas.GeometriaBase,
    db: Session = Depends(get_db),
    # Protegido: Solo un administrador puede crear geometrías.
    admin_user: schemas.Usuario = Depends(security.get_current_admin_user),
):
    """
    Crea una nueva geometría. (Protegido - Solo Admin)
    """
    return crud.create_geometria(db=db, geometria=geometria)


@app.get("/geometrias/", response_model=list[schemas.Geometria])
def read_geometrias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene una lista de todas las geometrías. (Público)
    """
    geometrias = crud.get_geometrias(db, skip=skip, limit=limit)
    return geometrias


# --- 4. ENDPOINTS DE REGISTRO_CALCULO ---


@app.post(
    "/calculos/",
    response_model=schemas.RegistroCalculo,
    status_code=status.HTTP_201_CREATED,
)
def create_calculo(
    calculo: schemas.RegistroCalculoCreate,
    db: Session = Depends(get_db),
    # Protegido: Un usuario debe estar logueado para registrar un cálculo.
    current_user: schemas.Usuario = Depends(security.get_current_active_user),
):
    """
    Guarda un nuevo registro de cálculo. (Protegido)
    El cálculo se asocia automáticamente al usuario autenticado.
    """
    return crud.create_registro_calculo(
        db=db, calculo=calculo, usuario_id=current_user.usuario_id
    )


@app.get("/calculos/me/", response_model=list[schemas.RegistroCalculo])
def read_my_calculos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    # Protegido: Solo el usuario logueado puede ver sus cálculos.
    current_user: schemas.Usuario = Depends(security.get_current_active_user),
):
    """
    Obtiene la lista de todos los cálculos realizados por el usuario
    actualmente autenticado. (Protegido)
    """
    return crud.get_calculos_by_user(
        db=db, usuario_id=current_user.usuario_id, skip=skip, limit=limit
    )


@app.put("/calculos/{registro_id}/deactivate", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_calculo_propio(
    registro_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.Usuario = Depends(security.get_current_active_user),
):
    """
    Desactiva (borrado lógico) un registro de cálculo.
    Solo el propietario puede desactivar su cálculo.
    """
    db_calculo = crud.get_calculo_by_id_and_owner(
        db=db, registro_id=registro_id, usuario_id=current_user.usuario_id
    )

    if db_calculo is None:
        raise HTTPException(status_code=404, detail="Registro de cálculo no encontrado")

    # ¡Llama a la nueva función de CRUD!
    crud.deactivate_calculo(db=db, db_calculo=db_calculo)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post(
    "/calculos/batch",
    response_model=list[schemas.RegistroCalculo],
    status_code=status.HTTP_201_CREATED,
)
def create_batch_calculos(
    calculos: list[schemas.RegistroCalculoCreate],  # <-- Acepta una LISTA de cálculos
    db: Session = Depends(get_db),
    current_user: schemas.Usuario = Depends(security.get_current_active_user),
):
    """
    Guarda un lote de nuevos registros de cálculo.
    Todos se asocian al usuario autenticado.
    """
    # (En producción, deberías validar que todos los modelo_id y geometria_id
    # de la lista sean válidos antes de intentar el commit)

    return crud.create_batch_calculos(
        db=db, calculos=calculos, usuario_id=current_user.usuario_id
    )


# --- 5. ENDPOINTS DE CONTENIDO (Documentación y Recursos) ---


@app.get(
    "/modelos/{modelo_id}/documentacion",
    response_model=list[schemas.DocumentacionTeorica],
)
def read_documentacion_por_modelo(modelo_id: int, db: Session = Depends(get_db)):
    """
    Obtiene toda la documentación teórica asociada a un modelo específico. (Público)
    """
    db_modelo = crud.get_modelo(db, modelo_id=modelo_id)
    if db_modelo is None:
        raise HTTPException(status_code=404, detail="Modelo no encontrado")

    return crud.get_documentacion_by_modelo(db=db, modelo_id=modelo_id)


@app.get("/modelos/{modelo_id}/recursos", response_model=list[schemas.RecursoAnsys])
def read_recursos_por_modelo(modelo_id: int, db: Session = Depends(get_db)):
    """
    Obtiene todos los recursos ANSYS asociados a un modelo específico. (Público)
    """
    db_modelo = crud.get_modelo(db, modelo_id=modelo_id)
    if db_modelo is None:
        raise HTTPException(status_code=404, detail="Modelo no encontrado")

    return crud.get_recursos_by_modelo(db=db, modelo_id=modelo_id)
