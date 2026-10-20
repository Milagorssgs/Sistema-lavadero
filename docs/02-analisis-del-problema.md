# 2. Análisis del Problema y del Dominio

## 2.1. Descripción del Dominio del Negocio
El dominio en el que se enmarca el proyecto corresponde a la prestación de servicios automotores, específicamente el lavado y acondicionamiento estético de vehículos. Las entidades centrales que interactúan en este dominio son:
* **El Cliente:** Persona física o jurídica que solicita un servicio para uno o más vehículos de su propiedad.
* **El Vehículo:** Bien material sobre el cual recae el servicio (clasificado por tipo: Auto, Camioneta, Moto, etc.).
* **El Servicio:** Tarea específica que ofrece el establecimiento (Ej: Lavado simple, Lavado completo, Encerado), caracterizada por un precio y una duración estimada.
* **El Turno:** La asignación temporal (fecha y hora) acordada entre el cliente y el establecimiento para la realización del servicio.

## 2.2. Análisis de los Flujos de Trabajo (Situación Actual vs. Propuesta)

### 2.2.1. Situación Actual (Manual / Analógica)
1. **Recepción del pedido:** El cliente contacta por teléfono o se presenta en el local.
2. **Gestión de Agenda:** El encargado revisa una libreta física para encontrar un espacio libre. Existe alto riesgo de error humano (anotaciones ilegibles, pérdida del registro o doble agendamiento).
3. **Recepción del vehículo:** No se cuenta con un registro histórico rápido del cliente o del vehículo (no se identifican clientes frecuentes).
4. **Ejecución y Cobro:** El pago se registra en papel o en una caja registradora estándar, sin vincular directamente el ingreso económico con el historial del vehículo y el tipo de servicio realizado.

### 2.2.2. Situación Propuesta (Sistematizada)
1. **Autogestión o Recepción Rápida:** El cliente puede reservar online de forma pública (`/reserva_online`) o, en su defecto, el encargado registra el turno telefónico directamente en el software.
2. **Agenda Inteligente:** El sistema consulta la base de datos y bloquea las franjas horarias ocupadas, garantizando una disponibilidad real.
3. **Recepción del vehículo:** El empleado asocia rápidamente la patente al cliente registrado, accediendo de forma instantánea a su historial.
4. **Ejecución y Cobro:** Se finaliza el turno desde el panel de control, procesando el pago (total o parcial) y emitiendo un ticket. El monto ingresa automáticamente a los reportes de facturación, actualizando el *Dashboard* financiero.

## 2.3. Justificación del Desarrollo del Software
El desarrollo de este sistema se justifica técnica y económicamente por:
* **Reducción de tiempos muertos:** La organización eficiente de los turnos permite atender más vehículos por día sin demoras.
* **Fidelización del cliente:** Ofrecer un módulo de reservas online 24/7 moderniza la imagen de la empresa y facilita el acceso al servicio.
* **Seguridad y Auditoría:** Al digitalizar la información y separar los accesos por roles (Administrador, Dueño, Empleado), se evita la alteración de precios o el borrado de registros de pago, garantizando el control sobre la caja y las operaciones.
