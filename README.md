# cb-base-backend

Repositorio base de backend para ConsiliumBots, con un par de modelos de ejemplo y capacidad de login.

## Prerequisitos
- Seteo y configuración de AWS CLI. Leer https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html
- Tener una base postgres disponible.
- Tener la consola de kubernetes (kubectl)


## Pasos a seguir

### 1. Cambios en proyecto

Es necesario hacer unos cambios al proyecto para poder utilizarlo. Cosas a necesarias a cambiar:
- Cambiar cada instancia de <project> al nombre del projecto. Por ejemplo, <project> -> project.

### 2. Instalación librerías

Es necesario instalar librerías de requirements.txt. Se puede hacer con `pip install -r requirements.txt`.

### 3. Pasos admin
Es necesario que un administrador haga un par de pasos:
- Generación de ECR en AWS
- Generación de dos secretos en AWS, `<project>/staging` y `<project>/production`.
- Aplicación de deployments

## Uso

Una vez que está todo lo anterior listo, hay que conectar con la base de datos. Luego, correr:
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py runserver`

## Organización
- models: Modelos de datos.
- serializers: Serializadores de datos.
- viewsets: vistas (por modelo) de datos.
- views: vistas (otras).
- tests: tests.
- factories: creadores de objetos.
- migration
