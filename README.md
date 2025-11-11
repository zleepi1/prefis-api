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
```

**2. Configura la Base de Datos:**

  * Asegúrate de que tu servidor MariaDB esté corriendo.
  * Crea una base de datos (ej. `Proyect_PREFIS`).
  * Importa el esquema inicial usando el archivo `Proyect_PREFIS.sql` que se encuentra en el repositorio.

**3. Configura las Variables de Entorno:**
Este proyecto usa un archivo `.env` para manejar los secretos.

  * Crea un archivo llamado `.env` en la raíz del proyecto.
  * Copia y pega el siguiente contenido, **ajustando la `DATABASE_URL`** con tu usuario, contraseña y nombre de base de datos.

<!-- end list -->

```ini
# .env
# Configuración de la Base de Datos
DATABASE_URL="mysql+pymysql://tu_usuario:tu_contraseña@localhost/Proyect_PREFIS"

# Configuración de Seguridad de la API
SECRET_KEY="una-clave-secreta-muy-larga-y-aleatoria-aqui"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

**Importante:** Asegúrate de añadir `.env` a tu archivo `.gitignore` para no subir tus secretos a GitHub.

### 3\. Instalación de Dependencias (requirements.txt)

Este proyecto usa un **entorno virtual** (`venv`) para aislar sus dependencias, lo cual es la mejor práctica en Python.

**1. Crea el entorno virtual:**

```bash
python -m venv .venv
```

**2. Activa el entorno virtual:**

  * **En Windows (CMD/PowerShell):**
    ```bash
    .\.venv\Scripts\activate
    ```
  * **En macOS/Linux:**
    ```bash
    source .venv/bin/activate
    ```

(Verás `(.venv)` al inicio de tu terminal si funcionó).

**3. Instala los paquetes:**
El archivo `requirements.txt` es una lista de todas las librerías de Python que el proyecto necesita. El siguiente comando las instala todas de una vez:

```bash
pip install -r requirements.txt
```

### 4\. Ejecutar el Servidor de Desarrollo

Con tu entorno activado y las dependencias instaladas, puedes iniciar el servidor:

```bash
uvicorn main:app --reload
```

  * `uvicorn`: Es el servidor ASGI que ejecuta tu aplicación.
  * `main:app`: Le dice a Uvicorn que busque el archivo `main.py` y, dentro de él, el objeto `app = FastAPI()`.
  * `--reload`: ¡Muy útil\! Reinicia el servidor automáticamente cada vez que guardas un cambio en cualquier archivo `.py`.

Tu API ahora estará corriendo en: `http://127.0.0.1:8000`

-----

## 🚀 Cómo Usar la API

FastAPI genera automáticamente una documentación interactiva.

**Abre tu navegador y ve a: `http://127.0.0.1:8000/docs`**

Verás la documentación de **Swagger UI**, desde donde puedes:

  * Ver todos los *endpoints* disponibles.
  * Ver los *schemas* (la forma) de los datos que la API espera y devuelve.
  * Probar la API directamente desde el navegador.

### Flujo de Autenticación

Para usar los endpoints protegidos (los que tienen un candado 🔒), debes seguir este flujo:

1.  **Regístrate:** Usa el endpoint `POST /usuarios/` para crear una nueva cuenta.
2.  **Inicia Sesión:** Usa el endpoint `POST /token` (con el `username` y `password` de tu cuenta) para obtener un `access_token`.
3.  **Autorízate:** Haz clic en el botón verde **`Authorize`** en la parte superior derecha de la página `/docs`.
4.  En la ventana, introduce tu `username` y `password` en los campos del formulario `OAuth2PasswordBearer` y haz clic en "Authorize".
5.  ¡Listo\! Swagger guardará el token por ti. Todas tus futuros intentos desde esa página usarán tu token y podrás acceder a los endpoints protegidos.

<!-- end list -->

```

---

¡Espero que ahora sí esté completo!

Ya que tu API está 100% funcional y tu frontend está en marcha, ¿te gustaría que hablemos sobre el siguiente gran paso, como **desplegar esta API de FastAPI** en un servicio gratuito como Railway o Render para que tu app de React pueda acceder a ella desde cualquier lugar?
```
