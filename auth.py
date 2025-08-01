"""
auth.py
Sistema de autenticación y autorización para Neoproyectto.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db, User
from security import validate_environment
from error_handling import ValidationError
from logger import NeoproyecttoLogger

# Inicializar logger
logger = NeoproyecttoLogger("neoproyectto.auth")

# Obtener variables de entorno
env_vars = validate_environment()
SECRET_KEY = env_vars["NEOPROYECTTO_SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuración de seguridad para contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 con Bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Modelos para autenticación
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    
class UserInDB(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str
    is_active: bool
    is_admin: bool
    created_at: datetime

def verify_password(plain_password, hashed_password):
    """Verifica si la contraseña coincide con el hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Genera un hash seguro para una contraseña."""
    return pwd_context.hash(password)

def get_user(db: Session, username: str):
    """Obtiene un usuario de la base de datos por nombre de usuario."""
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    """Autentica un usuario con sus credenciales."""
    user = get_user(db, username)
    if not user:
        logger.warning(f"Intento de login con usuario inexistente: {username}")
        return False
    if not verify_password(password, user.hashed_password):
        logger.warning(f"Intento de login fallido para usuario: {username}")
        return False
    logger.info(f"Login exitoso para usuario: {username}")
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crea un token JWT de acceso."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Verifica y decodifica el token JWT para obtener el usuario actual.
    
    Args:
        db: Sesión de base de datos.
        token: Token JWT.
        
    Returns:
        Usuario autenticado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        logger.warning("Error decodificando token JWT", data={"token": token[:10] + "..."})
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        logger.warning(f"Usuario {token_data.username} no encontrado en la base de datos")
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    Verifica que el usuario está activo.
    
    Args:
        current_user: Usuario autenticado.
        
    Returns:
        Usuario activo.
    """
    if not current_user.is_active:
        logger.warning(f"Intento de acceso con cuenta inactiva: {current_user.username}")
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return current_user

async def get_current_admin_user(current_user: User = Depends(get_current_active_user)):
    """
    Verifica que el usuario es un administrador.
    
    Args:
        current_user: Usuario activo.
        
    Returns:
        Usuario administrador.
    """
    if not current_user.is_admin:
        logger.warning(f"Intento de acceso a recursos admin por usuario no autorizado: {current_user.username}")
        raise HTTPException(status_code=403, detail="Se requieren privilegios de administrador")
    return current_user

def create_user(db: Session, user_create: UserCreate):
    """
    Crea un nuevo usuario en la base de datos.
    
    Args:
        db: Sesión de base de datos.
        user_create: Datos del usuario a crear.
        
    Returns:
        User: Usuario creado.
    """
    # Verificar si el usuario ya existe
    existing_user = db.query(User).filter(User.username == user_create.username).first()
    if existing_user:
        raise ValidationError("El nombre de usuario ya está en uso", {"field": "username"})
    
    # Verificar si el email ya está en uso
    existing_email = db.query(User).filter(User.email == user_create.email).first()
    if existing_email:
        raise ValidationError("El email ya está registrado", {"field": "email"})
    
    # Crear el nuevo usuario
    hashed_password = get_password_hash(user_create.password)
    new_user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password,
        is_active=True,
        is_admin=False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"Usuario creado: {user_create.username}")
    return new_user