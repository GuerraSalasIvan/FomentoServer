# FomentoServer
Esta es la api Fomento.

Seguridad:

Existen 3 tipos de usuarios, cliente, entrenador y admin.

- Admin:
Tiene todos los permisos asignados

- Entrenador:
Puede añadir y consultar cuelquier modelo de la app, pero no puede ni modificarlos ni eliminarlos.

- Cliente:
Puede ver todos los modelos y crear usuarios, aparte de poder crear usuarios, no puede realizar ninguna otra operación.

## Cargar fixtures
python manage.py loaddata app/fixtures/datos.json

###Para crear usuario desde angular local a django local

pip install django-cors-headers


INSTALLED_APPS = [
    # ...
    'corsheaders',
    # ...
]

MIDDLEWARE = [
    # ...
    'corsheaders.middleware.CorsMiddleware',
    # ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
]

