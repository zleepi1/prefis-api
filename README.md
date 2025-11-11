# Proyecto PREFIS - API Backend

Esta es la API del backend para el proyecto PREFIS, construida con **FastAPI** y **SQLAlchemy**. Provee una interfaz RESTful segura para gestionar usuarios, modelos de análisis, geometrías y registros de cálculos de ingeniería.

## 🚀 Características Principales

* **Framework Moderno:** Construido con [FastAPI](https://fastapi.tiangolo.com/) para un alto rendimiento.
* **Autenticación Segura:** Manejo de usuarios con hashing de contraseñas (`bcrypt`) y autenticación basada en tokens JWT (`python-jose`).
* **Base de Datos Relacional:** Usa [SQLAlchemy](https://www.sqlalchemy.org/) como ORM para comunicarse con una base de datos MariaDB/MySQL.
* **Validación de Datos:** Utiliza [Pydantic](https://pydantic-docs.helpmanual.io/) para la validación automática de datos de entrada y salida.
* **Documentación Automática:** Genera documentación interactiva de la API (Swagger UI y ReDoc) de forma automática.
* **Manejo de Lotes:** Endpoints optimizados (ej. `/calculos/batch`) para ingesta de múltiples registros en una sola petición.

## 🛠️ Stack Tecnológico

* [Python 3.10+](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/) - El framework de la API.
* [Uvicorn](https://www.uvicorn.org/) - El servidor ASGI.
* [SQLAlchemy](https://www.sqlalchemy.org/) - El ORM para la base de datos.
* [PyMySQL](https://github.com/PyMySQL/PyMySQL) - El driver de la base de datos.
* [Bcrypt](https://pypi.org/project/bcrypt/) - Para hashing de contraseñas.
* [Python-JOSE](https://github.com/mpdavis/python-jose) - Para la creación de tokens JWT.
* [Pydantic](https://pydantic-docs.helpmanual.io/) - Para la configuración y validación.

---

## ⚙️ Guía de Instalación y Puesta en Marcha

Sigue estos pasos para configurar y ejecutar el proyecto en tu máquina local.

### 1. Prerrequisitos

* Tener **Python 3.10** o superior instalado.
* Tener **Git** instalado.
* Tener una instancia de **MariaDB** (o MySQL) corriendo.

### 2. Configuración del Proyecto

**1. Clona el repositorio:**
```bash
git clone [URL_DE_TU_REPOSITORIO]
cd [NOMBRE_DE_LA_CARPETA]
