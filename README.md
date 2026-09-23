# Sistema de Gestión para Lavadero de Autos

Este proyecto es un sistema de gestión web diseñado para un lavadero de autos, desarrollado en Python con Flask y SQLite. Está pensado para cubrir requerimientos académicos de Práctica Profesional (2do año de Analista de Sistemas).

## Tecnologías Utilizadas

- **Backend:** Python, Flask
- **Base de Datos:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript (Vainilla)
- **Plantillas:** Jinja2

## Funcionalidades Principales

1. **Gestión de Usuarios y Roles:** (Administrador, Empleado, Dueño).
2. **Gestión de Clientes y Vehículos:** Registro, búsqueda, historial y asociación.
3. **Catálogo de Servicios:** Creación y modificación de servicios con precios y duración.
4. **Agenda de Turnos:** Gestión visual para evitar superposición de horarios.
5. **Reservas Online:** Página pública para que los clientes soliciten turnos.
6. **Módulo de Pagos y Comprobantes:** Registro de pagos (totales y parciales) y generación de recibos imprimibles.
7. **Reportes:** Visualización de ingresos, vehículos atendidos y servicios más solicitados.

## Estructura del Proyecto

```text
sistema-lavadero/
├── app.py                 # Lógica principal y rutas de Flask
├── requirements.txt       # Dependencias de Python
├── README.md              # Documentación del proyecto
├── database.db            # Base de datos (generada automáticamente)
├── database/
│   └── init_db.py         # Script para crear tablas y datos de prueba
├── static/
│   ├── css/style.css      # Estilos generales del sistema
│   └── js/script.js       # Scripts para interacción en cliente
└── templates/             # Plantillas HTML (Jinja2)
    ├── base.html          # Layout base
    ├── login.html         # Pantalla de inicio de sesión
    ├── dashboard.html     # Panel de control
    ├── ...                # Demás vistas (clientes, turnos, etc.)
```

## Instrucciones de Instalación y Ejecución

Sigue estos pasos en tu computadora (Windows) para ejecutar el proyecto.

### 1. Clonar o descomprimir el proyecto
Asegúrate de estar en la carpeta raíz del proyecto (`C:\Users\Usuario\Desktop\Sistema-lavadero`).

### 2. Crear y activar el Entorno Virtual (Opcional pero recomendado)
Abre PowerShell y ejecuta:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar las dependencias
Ejecuta el siguiente comando para instalar Flask y Werkzeug:
```powershell
pip install -r requirements.txt
```

### 4. Inicializar la Base de Datos
Si la base de datos `database.db` no existe, créala y llénala con datos de prueba ejecutando:
```powershell
python database\init_db.py
```

### 5. Iniciar la aplicación
Levanta el servidor web local ejecutando:
```powershell
python app.py
```

### 6. Acceder al sistema
Abre tu navegador de internet y entra a la siguiente dirección:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

## Usuarios por Defecto

El sistema incluye 3 usuarios creados para pruebas, cada uno con un rol distinto:

- **Administrador**
  - **Usuario:** `admin`
  - **Contraseña:** `admin123`
- **Empleado**
  - **Usuario:** `empleado`
  - **Contraseña:** `empleado123`
- **Dueño**
  - **Usuario:** `dueno`
  - **Contraseña:** `dueno123`

## Detalles Técnicos y Decisiones de Diseño

- **Simplicidad:** Todo el backend está centralizado en `app.py` para facilitar la lectura, comprensión y explicación a nivel académico.
- **Sin superposición de turnos:** Al crear un turno (administrativo) o reserva (online), el sistema busca en la base de datos si ya existe un registro con la misma fecha y hora. Si es así, bloquea el registro mostrando una alerta.
- **Seguridad:** Las contraseñas en la base de datos están encriptadas mediante `werkzeug.security` (hash). Las rutas internas se protegen con un decorador `login_required`.
