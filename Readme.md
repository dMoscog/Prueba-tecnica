# Prueba Técnica - Django (Rick and Morty API)

Proyecto backend desarrollado en Django con integración a MySQL y consumo de la API pública de Rick and Morty mediante un comando personalizado de Django.

## Requisitos Previos

* Python 3.13 o superior instalado.
* MySQL Server (versión 8.0 o compatible) instalado localmente.
* Git instalado.

---

## Configuración del Entorno y Base de Datos (MySQL)

1. Configurar las Variables de Entorno:
   * Duplica el archivo de ejemplo de variables de entorno y renómbralo exactamente a `.env`:
     ```bash
     copy .env.example .env
     ```
   * Importante: Abre el archivo `.env` recién creado y configura tus credenciales reales de MySQL (nombre de la base de datos, usuario, contraseña, host y puerto) para el correcto funcionamiento del sistema.

2. Crear la Base de Datos en MySQL:
   Abre tu gestor de MySQL y ejecuta el siguiente comando para crear la base de datos con el soporte de codificación correcto:
   ```sql
   CREATE DATABASE rick_morty_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
---
## Nota para el Evaluador (Usuarios)
Para probar los roles de Administrador y Editor solicitados en la prueba:
1. Ejecuta `python manage.py createsuperuser` para crear tu cuenta de Administrador.
2. Ingresa al panel de administración (`/admin/`) con ese superusuario y crea un segundo usuario con los permisos limitados para probar el rol de Editor.
----
## Configuración del Entorno Local

1. Clonar el repositorio:
   ```bash
   git clone "https://github.com/dMoscog/Prueba-tecnica.git"
   cd Prueba-tecnica