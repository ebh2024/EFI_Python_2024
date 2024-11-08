# Sistema de Gestión de Equipos

## Descripción

Este proyecto es una API de gestión de usuarios que permite Crear, Leer, Actualizar y Eliminar usuarios.

## Características

- CRUD (Crear, Leer, Actualizar, Eliminar) para usuarios.


## Instalación

1. Clona el repositorio:\
   git clone https://github.com/ebh2024/EFI_Python_2024.git
   
2. Crea y activa un entorno virtual:   \
     python -m venv .venv\
     source .venv/bin/activate

3. Instala las dependencias:\
      pip install -r requirements.txt

4. Configura la base de datos en config.py. Asegúrate de que la URI de la base de datos sea correcta:\
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/<tu-base-de-datos>'

5. Inicializa la base de datos:\
   flask db init\
   flask db migrate -m "Initial migration"\
   flask db upgrade

6. Ejecuta la aplicación:\
   flask run

