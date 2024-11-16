# Proyecto de Programación Web - Duoc UC

## Descripción

Este proyecto es parte del curso de Programación Web en Duoc UC. El objetivo del proyecto es crear una aplicación web funcional utilizando Django, un framework de desarrollo web en Python. La aplicación permite a los usuarios registrarse, iniciar sesión, y agregar servicios a un carrito de compras.

## Características

- Registro de usuarios
- Inicio de sesión de usuarios
- Actualización de la información del perfil del usuario
- Agregar servicios a un carrito de compras
- Validación de formularios en el cliente y en el servidor

## Requisitos

- Python 3.12
- Django 5.0.6

## Instalación

Sigue estos pasos para configurar el proyecto en tu máquina local:

1. Clona el repositorio:

    ```sh
    git clone https://github.com/tu-usuario/tu-proyecto.git
    cd tu-proyecto
    ```

2. Crea un entorno virtual:

    ```sh
    python -m venv venv
    ```

3. Activa el entorno virtual:

    - En Windows:
    
      ```sh
      venv\Scripts\activate
      ```

    - En macOS/Linux:
    
      ```sh
      source venv/bin/activate
      ```

4. Instala las dependencias:

    ```sh
    pip install -r requirements.txt
    ```

5. Realiza las migraciones de la base de datos:

    ```sh
    python manage.py migrate
    ```

6. Crea un superusuario (opcional, para acceder al admin de Django):

    ```sh
    python manage.py createsuperuser
    ```

## Uso

1. Inicia el servidor de desarrollo de Django:

    ```sh
    python manage.py runserver --insecure
    ```

2. Abre tu navegador y navega a `http://127.0.0.1:8000` para ver la aplicación en funcionamiento.

## Estructura del Proyecto

- **myapp/**: Directorio principal de la aplicación Django.
  - **models.py**: Definición de los modelos de la base de datos.
  - **views.py**: Definición de las vistas.
  - **urls.py**: Definición de las rutas de la aplicación.
  - **forms.py**: Definición de los formularios.
  - **templates/**: Directorio que contiene las plantillas HTML.
  - **static/**: Directorio que contiene archivos estáticos (CSS, JS, imágenes).
- **taller/**: Configuración principal del proyecto Django.
  - **settings.py**: Configuración del proyecto.
  - **urls.py**: Rutas principales del proyecto.
- **manage.py**: Archivo de gestión de Django.

## Validaciones

### Formulario de Registro

- Todos los campos son obligatorios.
- El correo electrónico debe tener un formato válido.
- La contraseña debe tener al menos 6 caracteres, incluyendo una letra mayúscula y un número.
- La confirmación de la contraseña debe coincidir con la contraseña.

### Formulario de Actualización de Información

- Al menos un campo debe estar lleno.
- Si se proporciona una nueva contraseña, debe cumplir con los requisitos y coincidir con la confirmación de la contraseña.

## Problemas Comunes

### Error `DoesNotExist`

Si encuentras un error `DoesNotExist` al intentar agregar un servicio al carrito, verifica que el servicio exista en la base de datos. Puedes manejar este error en la vista `agregar_al_carrito` con una excepción.

## Contribuciones

Si deseas contribuir al proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama para tu funcionalidad (`git checkout -b nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -m 'Agregar nueva funcionalidad'`).
4. Sube tus cambios a tu rama (`git push origin nueva-funcionalidad`).
5. Abre un Pull Request.
Este README proporciona una guía completa para configurar, usar y contribuir al proyecto de programación web para el curso en Duoc UC. Puedes ajustarlo según las necesidades específicas de tu proyecto.
