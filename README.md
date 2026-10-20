#  Sistema de Gestión para Lavadero de Autos

Una aplicación web pensada para que un lavadero deje atrás el cuaderno de turnos, los recibos en papel y las anotaciones sueltas, y pase a tener toda su operación diaria en un solo lugar.

Este proyecto nació como **Práctica Profesional (Ciclo Lectivo 2026)** en el **IPET 1308**, a partir de un relevamiento real de cómo trabaja un lavadero: turnos que se superponían, clientes que había que buscar a mano y cobros difíciles de seguir cuando alguien pagaba en partes.

---

##  ¿Qué resuelve?

| Antes | Con el sistema |
| :--- | :--- |
| Turnos anotados en papel y horarios superpuestos | Agenda diaria que **impide reservar dos turnos en el mismo horario** |
| Datos de clientes dispersos | Ficha de cada cliente con sus vehículos e historial de servicios |
| Clientes que llamaban para pedir turno | **Reserva online pública**, desde la compu o el celular |
| Cobros parciales difíciles de controlar | Registro de pagos con **descuentos, recargos y saldo pendiente** |
| Presupuestos hechos a mano | Presupuestos con varios servicios y total calculado automáticamente |
| Sin visión del negocio | Panel con métricas del día, gráfico de ingresos y servicios más pedidos |

---

##  Funcionalidades

- **Inicio de sesión con roles**: administrador, empleado y dueño. Las contraseñas se guardan cifradas (hash), nunca en texto plano.
- **Dashboard**: turnos del día, autos atendidos, ingresos, pagos pendientes, próximos turnos, últimas reservas y gráfico de ingresos de los últimos 7 días.
- **Clientes**: alta, edición, baja, búsqueda por nombre/apellido/teléfono e historial completo.
- **Vehículos**: registro asociado a cada cliente, con patente única y búsqueda por dominio.
- **Servicios**: catálogo editable con precio y duración estimada.
- **Turnos**: agenda por fecha y cambio de estado (`Pendiente`, `En Proceso`, `Finalizado`, `Cancelado`).
- **Reserva online**: formulario público, sin necesidad de cuenta, que también valida la disponibilidad.
- **Pagos y comprobantes**: efectivo, transferencia o tarjeta; pagos parciales; comprobante listo para imprimir o guardar como PDF desde el navegador.
- **Presupuestos**: cotización de varios servicios para un vehículo, con vista para imprimir.
- **Reportes**: total recaudado, vehículos atendidos y ranking de servicios.
- **Usuarios y configuración** *(solo administrador/dueño)*: alta de operadores, nombre del lavadero y horarios de atención.
- **Modo claro / oscuro** y diseño adaptable a celulares.

---

##  Tecnologías

| Capa | Herramienta |
| :--- | :--- |
| Backend | Python 3 + [Flask](https://flask.palletsprojects.com/) 3.0 |
| Plantillas | Jinja2 |
| Base de datos | SQLite (un único archivo, sin servidor aparte) |
| Seguridad | Werkzeug (hash de contraseñas) y sesiones de Flask |
| Frontend | HTML5, CSS propio con variables (modo oscuro) y JavaScript |
| Recursos externos | Font Awesome (íconos), Chart.js (gráficos) y Google Fonts (Inter) |

> Los íconos, los gráficos y la tipografía se cargan desde internet (CDN). Sin conexión el sistema funciona igual, pero esos elementos pueden no verse.

---

##  Estructura del proyecto

```text
Sistema-lavadero/
├── app.py                 # Aplicación Flask: rutas, permisos y lógica de cada módulo
├── database.db            # Base de datos SQLite con datos de ejemplo
├── database/
│   └── init_db.py         # Script que crea las tablas, los índices y los datos iniciales
├── static/
│   ├── css/style.css      # Estilos, paleta de colores y modo oscuro
│   └── js/script.js       # Interacciones del lado del cliente
├── templates/             # Vistas HTML (base.html + una plantilla por pantalla)
└── requirements.txt       # Dependencias de Python
```

---

##  Cómo ejecutarlo

**Requisitos:** Python 3.10 o superior.

```bash
# 1. Clonar el repositorio
git clone https://github.com/Milagorssgs/Sistema-lavadero.git
cd Sistema-lavadero

# 2. Crear y activar un entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux / macOS

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Iniciar la aplicación
python app.py
```

Después abrí **http://127.0.0.1:5000** en el navegador.

La reserva online para clientes está en **http://127.0.0.1:5000/reserva_online**.

> [!NOTE]
> El repositorio ya incluye `database.db` con datos de ejemplo, así que no hace falta crear la base para probar el sistema.
> Si querés generarla desde cero (o actualizar una base anterior), ejecutá `python database/init_db.py`. El script crea las tablas que falten y agrega columnas nuevas sin borrar los datos existentes.

---

##  Usuarios de prueba

| Rol | Usuario | Contraseña | Acceso |
| :--- | :--- | :--- | :--- |
| Administrador | `admin` | `admin123` | Todo el sistema |
| Dueño | `dueno` | `dueno123` | Todo el sistema |
| Empleado | `empleado` | `empleado123` | Operación diaria (sin usuarios ni configuración) |

> [!WARNING]
> Son credenciales de demostración. Antes de usar el sistema con datos reales, cambiá estas contraseñas y la `secret_key` definida en `app.py`.

---

##  Modelo de datos

La base está normalizada y usa claves foráneas entre sus tablas principales:

```text
clientes ──< vehiculos
clientes ──< turnos >── vehiculos
servicios ──< turnos ──< pagos
servicios ──< reservas
clientes ──< presupuestos ──< presupuesto_detalle >── servicios
usuarios      configuracion   (tablas independientes)
```

Para consultas frecuentes (patentes, turnos por fecha y estado, pagos, reservas) se crearon índices que mantienen el sistema ágil a medida que crecen los datos.

---

##  Próximos pasos

Algunas mejoras que quedaron planificadas para futuras versiones:

- Recordatorios automáticos de turnos por WhatsApp.
- Descarga directa del comprobante en PDF.
- Integración con pagos electrónicos.

---

##  Autora

**Milagros Yaquelin Gsell**
Práctica Profesional — IPET 1308 — Ciclo Lectivo 2026

Proyecto desarrollado con fines académicos.
