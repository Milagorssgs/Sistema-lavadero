# 1. Introducción y Objetivos

## 1.1. Planteamiento del Problema
En la actualidad, gran parte de los lavaderos de vehículos administran sus operaciones diarias mediante registros físicos (cuadernos, planillas) o herramientas ofimáticas básicas que no están diseñadas específicamente para el rubro. Esta gestión manual y descentralizada genera diversos problemas operativos:
* **Desorganización en la agenda:** La falta de validaciones automáticas facilita la superposición de turnos, causando demoras, acumulación de vehículos y malestar en los clientes.
* **Trazabilidad deficiente:** Resulta complejo llevar un historial unificado que asocie a un cliente con sus distintos vehículos, turnos pasados y pagos pendientes.
* **Pérdida de oportunidades comerciales:** Al no ofrecer un canal digital para reservas, el establecimiento limita su alcance comercial a contactos telefónicos o visitas presenciales, medios que requieren atención humana constante.
* **Falta de métricas y control financiero:** Los dueños o gerentes encuentran dificultades para obtener reportes precisos en tiempo real sobre los ingresos, los servicios más demandados y el desempeño del local.

## 1.2. Propósito del Sistema
El presente proyecto tiene como propósito principal proveer una solución tecnológica integral y centralizada a través de una aplicación web, diseñada para la gestión, control y optimización de las operaciones diarias de un lavadero de autos. 

El sistema busca digitalizar el ciclo completo de servicio, desde que el cliente solicita un turno (sea de forma presencial o a través del módulo de reservas online públicas) hasta la finalización del lavado y la emisión del comprobante de pago. Su diseño arquitectónico basado en roles permite que dueños, administradores y empleados interactúen con la información pertinente a sus funciones, garantizando seguridad, integridad de los datos y eficiencia en el flujo de trabajo.

## 1.3. Objetivos del Proyecto

### 1.3.1. Objetivo General
Desarrollar e implementar un sistema de gestión web escalable, seguro y de alta disponibilidad que automatice la administración de turnos, clientes, vehículos y pagos del lavadero, optimizando la toma de decisiones mediante un panel de control en tiempo real.

### 1.3.2. Objetivos Específicos
* **Digitalizar el padrón de clientes y vehículos:** Implementar una base de datos relacional (SQLite) que asocie de manera unívoca a los clientes con sus respectivos vehículos y su historial operativo.
* **Optimizar la gestión de turnos:** Desarrollar un módulo de agenda que valide la disponibilidad horaria en tiempo real para evitar la superposición, tanto para los turnos registrados internamente como para los solicitados vía web.
* **Controlar accesos mediante roles:** Diseñar un sistema de autenticación seguro que distinga las capacidades del Administrador, el Dueño y los Empleados operativos.
* **Facilitar la autogestión de clientes:** Incorporar una interfaz pública (`Frontend` responsivo) donde los usuarios puedan solicitar reservas online de manera intuitiva y directa.
* **Administrar el catálogo de servicios:** Brindar herramientas para gestionar de forma dinámica los tipos de lavado, duraciones estimadas y listas de precios.
* **Mejorar el control financiero:** Implementar el registro detallado de transacciones, cobros parciales/totales y emitir reportes gerenciales automáticos accesibles desde el *Dashboard* del sistema.
