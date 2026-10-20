# 3. Alcance y Límites del Proyecto

## 3.1. Alcance del Sistema (In-Scope)
El sistema a desarrollar contempla exclusivamente los procesos básicos y críticos de la gestión operativa de un lavadero de vehículos. Se incluyen los siguientes módulos y capacidades funcionales:

* **Gestión de Identidad y Roles:** Sistema de inicio de sesión con encriptación, diferenciando accesos entre Administrador, Dueño y Empleado.
* **Módulo de Reservas y Turnos:** Control de agenda con validaciones de superposición, turnos generados internamente y reservas públicas vía web.
* **Gestión de Entidades Core:** Altas, bajas, modificaciones y consultas (ABMC) de Clientes y Vehículos, manteniendo la relación de pertenencia.
* **Catálogo de Servicios y Precios:** Parametrización de los tipos de lavados, costos asociados y duraciones requeridas.
* **Gestión de Cobros y Tickets:** Registro de pagos (con cálculo de saldos pendientes y finalización automática de turnos) y visualización de tickets en formato web imprimible.
* **Reportes e Indicadores (Dashboard):** Visualización de ingresos diarios, semanales, histórico de autos atendidos, ranking de servicios y cancelaciones a nivel visual en la plataforma.
* **Configuración Global:** Panel para definir horarios de atención y datos de contacto de la empresa.

## 3.2. Límites y Restricciones (Out-of-Scope)
Las siguientes características quedan expresamente fuera del alcance de esta versión del sistema (consideradas para futuras iteraciones o por decisiones de arquitectura):

* **Notificaciones externas:** No se incluyen envíos de SMS, integraciones con WhatsApp API ni correos electrónicos para recordatorios de turnos (Requisitos F-37 y F-38 catalogados como "No implementados").
* **Facturación electrónica fiscal (AFIP/IRS):** El sistema emite un comprobante o ticket de control interno y para el cliente, pero no funciona como un facturador homologado por entidades fiscales.
* **Gestión de Stock e Inventario:** No se contabiliza el uso de insumos (champú, ceras, rejillas) por cada lavado.
* **Pasarelas de Pago Electrónico:** No se integra MercadoPago, Stripe u otros procesadores de tarjetas de crédito. El registro del pago es meramente administrativo (efectivo/transferencia declarada por el cajero).
* **Gestión Avanzada de Empleados (RRHH):** El sistema permite crear usuarios empleados, pero no liquida sueldos, no controla fichadas por reloj biométrico ni gestiona comisiones por auto lavado.

## 3.3. Restricciones Técnicas y Operativas
* **Despliegue Local (On-Premise):** Inicialmente, el sistema está concebido para ejecutarse en un entorno local (servidor Flask en localhost y base de datos SQLite) dentro de la red del negocio, o en un alojamiento web básico.
* **Dependencia de Conectividad:** Si bien el sistema es local para el personal administrativo, el módulo de "Reserva Online" requiere que la aplicación sea expuesta a Internet.
* **Base de datos:** Se utiliza SQLite por su ligereza y facilidad académica. Si la carga concurrente de usuarios escala masivamente, existirá una restricción de rendimiento que obligará a migrar a PostgreSQL o MySQL.
