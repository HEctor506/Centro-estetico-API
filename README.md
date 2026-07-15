# Centro Estético API

REST API construida con **FastAPI** para la gestión de un centro estético.
Los datos se almacenan en **Supabase** (PostgreSQL) sobre el esquema
`beauty_api`, protegido con Row Level Security (RLS).

Cumple con las fases de **Implementación** (CRUD, validación, manejo de
excepciones y respuestas HTTP) y está lista para el **Despliegue** en
FastAPI Cloud desde GitHub.

---

## Recursos y endpoints

Cada recurso expone un CRUD completo (GET, POST, PUT, DELETE):

| Recurso            | Prefijo             | Operaciones           |
| ------------------ | ------------------- | --------------------- |
| Usuarios           | `/usuarios`         | GET · POST · PUT · DELETE |
| Estilistas         | `/estilistas`       | GET · POST · PUT · DELETE |
| Clientes           | `/clientes`         | GET · POST · PUT · DELETE |
| Servicios          | `/servicios`        | GET · POST · PUT · DELETE |
| Citas              | `/citas`            | GET · POST · PUT · DELETE |
| Notificaciones     | `/notificaciones`   | GET · POST · PUT · DELETE |
| Historial de citas | `/historial-citas`  | GET · POST · PUT · DELETE |
| Autenticación      | `/auth/login`       | POST                  |

Documentación interactiva generada automáticamente:

- **Swagger UI:** `/docs`
- **ReDoc:** `/redoc`

---

## Estructura del proyecto

```text
.
├── main.py                 # Punto de entrada (app FastAPI, registra routers)
├── app/
│   ├── database.py         # Conexión a Supabase + dependencia de autenticación (JWT)
│   ├── crud.py             # Operaciones CRUD genéricas + manejo de errores HTTP
│   ├── models/
│   │   └── schemas.py      # Modelos Pydantic (validación de entrada/salida)
│   └── routers/            # Un router por recurso
│       ├── auth.py
│       ├── usuarios.py
│       ├── estilistas.py
│       ├── clientes.py
│       ├── servicios.py
│       ├── citas.py
│       ├── notificaciones.py
│       └── historial.py
├── beauty_api.sql          # Esquema, RLS y datos de ejemplo (ejecutado en Supabase)
├── requirements.txt
├── pyproject.toml          # Entrypoint para FastAPI Cloud (main:app)
└── .env                    # Variables de entorno (NO se sube a GitHub)
```

---

## Requisitos previos en Supabase

1. Ejecutar `beauty_api.sql` en el editor SQL de Supabase (ya realizado).
2. **Exponer el esquema `beauty_api`** para la Data API:
   `Project Settings → API → Data API → Exposed schemas` → agregar `beauty_api`.
3. Tener al menos un usuario en **Authentication → Users** para poder iniciar sesión.

---

## Instalación y ejecución local

```bash
# 1. Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / macOS

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
#    Copia .env.example a .env y coloca tus credenciales de Supabase

# 4. Ejecutar
fastapi dev main.py
# o bien:  uvicorn main:app --reload
```

La API queda disponible en `http://127.0.0.1:8000` y Swagger en
`http://127.0.0.1:8000/docs`.

---

## Cómo probar los endpoints (Swagger)

1. Ejecuta **`POST /auth/login`** con tu `email` y `password` de Supabase.
2. Copia el `access_token` de la respuesta.
3. Pulsa el botón **Authorize** (candado, arriba a la derecha), pega el token
   y confirma.
4. Ya puedes ejecutar el resto de endpoints (están protegidos por RLS y
   requieren un usuario autenticado).

---

## Variables de entorno

| Variable                              | Descripción                          |
| ------------------------------------- | ------------------------------------ |
| `NEXT_PUBLIC_SUPABASE_URL`            | URL del proyecto Supabase            |
| `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`| Publishable key (anon) del proyecto  |

---

## Despliegue en FastAPI Cloud

1. Sube el proyecto a un repositorio en **GitHub** (el `.env` queda excluido
   por `.gitignore`).
2. En **FastAPI Cloud**, conecta el repositorio.
3. Configura las variables de entorno (`NEXT_PUBLIC_SUPABASE_URL` y
   `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`) en el panel del proyecto.
4. El entrypoint está definido en `pyproject.toml` como `main:app`.
5. Realiza el despliegue y verifica la URL pública en `/docs`.

---

## Manejo de errores y respuestas HTTP

| Código | Situación                                                    |
| ------ | ------------------------------------------------------------ |
| 200    | Consulta / actualización correcta                            |
| 201    | Recurso creado                                               |
| 401    | Falta el token o es inválido / expirado                      |
| 404    | El recurso solicitado no existe                              |
| 422    | Datos de entrada inválidos (validación Pydantic)             |
| 400    | Error al crear/actualizar (datos o políticas RLS)            |
| 500    | Error interno al consultar la base de datos                  |
