# 4. Requisitos del Sistema

Con base en el análisis de las operaciones del lavadero y la implementación desarrollada, los requisitos se dividen en Funcionales (qué debe hacer el sistema) y No Funcionales (cómo debe operar el sistema).

## 4.1. Requisitos Funcionales (RF)

Los requisitos funcionales se extraen directamente de la matriz de trazabilidad del código fuente y dictan el comportamiento esperado de cada módulo.

### Módulo de Seguridad y Accesos
* **RF-01:** El sistema debe permitir iniciar sesión y cerrar sesión a los usuarios registrados.
* **RF-02:** El sistema debe diferenciar niveles de acceso mediante roles: Administrador, Empleado y Dueño.
* **RF-03:** El Administrador debe poder crear nuevos usuarios en el sistema.

### Módulo de Clientes y Vehículos
* **RF-04:** El sistema debe permitir registrar, editar y eliminar los datos personales de los clientes.
* **RF-05:** El sistema debe permitir registrar vehículos asociándolos a un cliente existente mediante su número de patente.
* **RF-06:** El sistema debe proveer una herramienta de búsqueda para localizar clientes y vehículos (por nombre o patente).
* **RF-07:** El sistema debe mantener un historial de servicios vinculados a cada cliente.

### Módulo de Servicios y Configuración
* **RF-08:** El sistema debe permitir la creación, edición y eliminación de los servicios ofrecidos.
* **RF-09:** A cada servicio se le debe poder asignar un nombre, precio y duración estipulada.
* **RF-10:** El sistema debe poseer un panel de configuración global para establecer horarios de apertura y cierre.

### Módulo de Turnos y Agenda
* **RF-11:** El personal debe poder crear turnos internos asignando cliente, vehículo, servicio y fecha/hora.
* **RF-12:** El sistema debe poseer un módulo público de reserva online para clientes no registrados.
* **RF-13:** El sistema **debe bloquear obligatoriamente** la creación de turnos si existe superposición de fechas y horarios para el mismo recurso.
* **RF-14:** El sistema debe permitir cancelar turnos y cambiar sus estados (Pendiente, Confirmado, Finalizado, Cancelado).

### Módulo de Pagos y Reportes
* **RF-15:** El sistema debe permitir registrar el pago de un turno indicando el método y monto abonado.
* **RF-16:** El sistema debe admitir pagos parciales, llevando registro del saldo deudor.
* **RF-17:** Al finalizar un pago total, se debe generar un comprobante imprimible.
* **RF-18:** El sistema debe mostrar un Dashboard (Panel de Control) con indicadores de ingresos diarios/mensuales y autos atendidos.

---

## 4.2. Requisitos No Funcionales (RNF)

Determinan la arquitectura, la experiencia de usuario y las restricciones de calidad tecnológica del sistema.

### Usabilidad y Diseño
* **RNF-01 (Interfaz Web):** La interfaz de usuario debe estar desarrollada mediante tecnologías web estándar (HTML5, CSS3, JavaScript) basadas en plantillas Jinja2.
* **RNF-02 (Responsividad):** La interfaz pública de reserva online debe ser Responsive, adaptándose a dispositivos móviles.

### Seguridad
* **RNF-03 (Cifrado):** Todas las contraseñas de los usuarios deben almacenarse de forma cifrada mediante hashes en la base de datos (Ej: `werkzeug.security`).
* **RNF-04 (Protección de Rutas):** Las rutas internas de la aplicación no deben ser accesibles si no existe un token o cookie de sesión válida.

### Rendimiento y Escalabilidad
* **RNF-05 (Tiempo de respuesta):** El sistema debe procesar las reservas y cruces de agenda en un tiempo menor a 3 segundos bajo carga normal.
* **RNF-06 (Base de datos):** La arquitectura de datos inicial estará montada sobre SQLite, pero debe estar diseñada mediante consultas SQL estándar que permitan su futura migración.
