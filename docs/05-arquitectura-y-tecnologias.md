# 5. Arquitectura y Tecnologías

El sistema adopta una arquitectura de software de tipo **Monolítica Modular** con un enfoque de enrutamiento del lado del servidor (Server-Side Rendering). Está diseñado siguiendo los lineamientos técnicos de simplicidad requeridos para la Práctica Profesional.

## 5.1. Stack Tecnológico

La solución tecnológica se ha construido ensamblando los siguientes lenguajes, frameworks y bibliotecas:

### Backend (Lógica de Negocio)
* **Lenguaje:** Python 3.x
* **Micro-Framework:** Flask
* **Enrutamiento y Controladores:** Centralizados en `app.py`.
* **Manejo de Sesiones:** Módulo nativo `flask.session`.
* **Seguridad (Hashing):** `werkzeug.security` para el cifrado seguro de las contraseñas de usuario.

### Frontend (Interfaz de Usuario)
* **Estructuración:** HTML5 y plantillas dinámicas **Jinja2** (integradas directamente con Flask).
* **Estilos y Diseño:** CSS3 (Vanilla) y frameworks CSS compatibles en los templates.
* **Interactividad Cliente:** JavaScript (Vanilla JS) centralizado en `static/js/script.js`.
* **Manejo de rutas estáticas:** Servidas a través de la carpeta nativa `/static/` (hojas de estilo e imágenes).

### Capa de Datos (Persistencia)
* **Motor de Base de Datos:** SQLite 3 (ligero, embebido y sin requerimientos de configuración de servidor).
* **Drivers / Conexión:** Módulo nativo `sqlite3` de Python.
* **Administración Inicial:** Archivo `database/init_db.py` encargado de construir el esquema (DDL) y poblar datos iniciales (Data Seeding).

## 5.2. Arquitectura de Componentes

La arquitectura lógica de la aplicación se estructura según un modelo de tipo *MVC (Modelo - Vista - Controlador)* simplificado:

1. **El Cliente (Navegador):** Solicita recursos HTTP a las rutas definidas.
2. **El Controlador (app.py):**
   * Recibe la petición HTTP (GET, POST).
   * Valida la autenticación mediante decoradores (`@login_required`).
   * Procesa la lógica de negocio.
   * Realiza las consultas SQL a la base de datos `database.db`.
3. **El Modelo (SQLite):**
   * Retorna los datos solicitados.
   * La estructura de base de datos asegura la integridad referencial (ej: Patentes únicas, dependencias entre Turno-Cliente-Servicio).
4. **La Vista (Jinja2 Templates):**
   * `app.py` inyecta las variables de datos resultantes en los templates HTML ubicados en la carpeta `templates/`.
   * El servidor renderiza el HTML y lo devuelve al cliente.

## 5.3. Modelo de Datos Simplificado (Core Entities)
Las tablas principales sobre las cuales opera la base de datos son:
* `usuarios`: Almacena credenciales y el nivel de acceso (rol).
* `clientes`: Mantiene la información de contacto personal.
* `vehiculos`: Asocia una patente, marca y modelo con una `cliente_id`.
* `servicios`: Catálogo maestro de productos ofrecidos.
* `turnos`: Relaciona `cliente_id`, `vehiculo_id`, `servicio_id`, fechas, horas y su estado actual.
* `pagos`: Entidad transaccional vinculada a un `turno_id` que asienta la recaudación.
