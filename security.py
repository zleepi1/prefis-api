# security.py
import bcrypt
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import schemas
import crud
from sqlalchemy.orm import Session
from database import SessionLocal

# --- Configuración de Seguridad ---
# ¡CAMBIA ESTO por una cadena aleatoria y secreta en producción!
SECRET_KEY = "MI_CLAVE_SECRETA_MUY_DIFICIL_DE_ADIVINAR"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # Token válido por 1 día


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña plana contra un hash de bcrypt."""
    # bcrypt necesita comparar bytes, no strings
    plain_password_bytes = plain_password.encode("utf-8")
    hashed_password_bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)


def get_password_hash(password: str) -> str:
    """Hashea una contraseña usando bcrypt."""
    # bcrypt necesita hashear bytes
    password_bytes = password.encode("utf-8")

    # Generar el salt y hashear
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)

    # Devolver como string (para guardarlo en la BD)
    return hashed_bytes.decode("utf-8")


# --- Autenticación JWT ---
# "tokenUrl" le dice a FastAPI qué endpoint usar para el login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Por defecto, 15 minutos si no se especifica
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# --- Dependencia para obtener la sesión de BD ---
# (Necesaria aquí para la validación de tokens)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Dependencia para obtener el usuario actual ---
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Decodifica el token JWT para obtener el usuario actual.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # ----- CAMBIO 1: Aceptar que 'email' puede ser None -----
        email: str | None = payload.get("sub")  # "sub" es el email del usuario

        if email is None:
            raise credentials_exception

        # (Quitamos la creación de token_data, no es necesaria aquí)

    except JWTError:
        raise credentials_exception

    # ----- CAMBIO 2: Usar 'email' directamente -----
    # En este punto, Pylance sabe que 'email' SÍ es un 'str'
    # porque ya pasó el 'if email is None'
    user = crud.get_user_by_email(db, email=email)

    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: schemas.Usuario = Depends(get_current_user)):
    """
    Dependencia que obtiene el usuario actual y verifica si está activo.
    """
    if not current_user.esta_activo:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return current_user


def get_current_admin_user(
    current_user: schemas.Usuario = Depends(get_current_active_user),
):
    """
    Dependencia que verifica si el usuario actual es un administrador.
    """
    if current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operación no permitida. Se requieren permisos de administrador.",
        )
    return current_user
