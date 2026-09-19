# Documentación Técnica del Proyecto - Catálogo Rick & Morty (Django & MySQL)

## 1. Introducción y Arquitectura
Este proyecto es una aplicación web desarrollada como solución a la prueba técnica para la posición de Desarrollador Junior. Está construida bajo el patrón MVT (Modelo-Vista-Template) del framework Django y utiliza MySQL como motor de base de datos relacional para garantizar la persistencia de la información obtenida desde la API pública de Rick and Morty.

La estructura del repositorio se divide en aplicaciones modulares:
* `core/`: Contiene la configuración global del proyecto (`settings.py`, rutas principales `urls.py`, configuración WSGI/ASGI).
* `catalog/`: Aplicación principal encargada del modelado de datos, lógica de negocio, comandos de sincronización, vistas, formularios y control de acceso.

---

## 2. Modelado de Base de Datos Relacional
La base de datos utiliza codificación `utf8mb4` para asegurar la correcta compatibilidad con caracteres especiales. Se implementaron tres entidades principales con las siguientes relaciones:

* `Location` (Ubicación): Almacena los lugares del universo de la serie (nombre, tipo, dimensión).
* `Episode` (Episodio): Contiene los datos de los capítulos (nombre, código de episodio, fecha de emisión).
* `Character` (Personaje): Entidad central que almacena los atributos del personaje (nombre, estado, especie, género, imagen).
  * Relación Uno a Muchos (ForeignKey): Cada personaje está asociado a una ubicación de origen y/o ubicación actual (`Location`).
  * Relación Muchos a Muchos (ManyToManyField): Un personaje puede aparecer en múltiples episodios, y un episodio cuenta con múltiples personajes (`Episode`).

---

## 3. Mecanismo de Sincronización de Datos
Para cumplir con el requerimiento de almacenar al menos 200 personajes, ubicaciones y episodios de manera automatizada sin duplicados, se desarrolló un comando personalizado de Django:

* Comando:
  ```bash
  python manage.py sync_rickmorty