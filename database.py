"""
database.py
Gestión de conexiones a bases de datos y modelos ORM.
"""
import os
from typing import Dict, Any, Optional, List
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

from error_handling import ConfigurationError
from security import validate_environment

# Obtener configuración
try:
    env_vars = validate_environment()
    DB_MODE = env_vars["NEOPROYECTTO_DB_MODE"]
    
    if DB_MODE == "postgres":
        DB_URL = env_vars["NEOPROYECTTO_POSTGRES_URL"]
    elif DB_MODE == "sqlite":
        DB_URL = "sqlite:///neoproyectto.db"
    else:
        raise ConfigurationError(f"Modo de base de datos no soportado: {DB_MODE}")
        
    ENGINE = create_engine(DB_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
    Base = declarative_base()
    
except Exception as e:
    raise ConfigurationError(f"Error configurando la base de datos: {str(e)}")

# Modelos
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    portfolios = relationship("Portfolio", back_populates="owner")

class Portfolio(Base):
    __tablename__ = "portfolios"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    capital_total = Column(Float)
    moneda = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="portfolios")
    assets = relationship("Asset", back_populates="portfolio")

class Asset(Base):
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    sector = Column(String, index=True)
    tipo = Column(String, index=True)
    asignacion = Column(Float)
    porcentaje = Column(Float)
    rendimiento_simulado = Column(Float, default=0.0)
    riesgo = Column(String, default="moderado")
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    portfolio = relationship("Portfolio", back_populates="assets")

# Función para inicializar la base de datos
def init_db():
    Base.metadata.create_all(bind=ENGINE)

# Obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    print("Inicializando base de datos...")
    init_db()
    print("Base de datos inicializada correctamente.")