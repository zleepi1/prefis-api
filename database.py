from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ACTUALIZA ESTA LÍNEA con tu usuario, contraseña y host de la base de datos
# Formato: "mysql+pymysql://USUARIO:CONTRASEÑA@HOST/NOMBRE_DB"
DATABASE_URL = "mysql+pymysql://root:@localhost/proyect_prefis"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
