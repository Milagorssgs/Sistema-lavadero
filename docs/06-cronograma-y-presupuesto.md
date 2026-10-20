# 6. Cronograma y Presupuesto

> **Nota aclaratoria:** Este documento presenta una estimación formal de tiempos y costos basada en metodologías tradicionales de ingeniería de software adaptadas a proyectos académicos/profesionales de pequeña a mediana escala.

## 6.1. Fases del Proyecto y Cronograma (Estimación en semanas)

El proyecto se planificó y estructuró a lo largo de un ciclo de vida clásico, desglosado en las siguientes etapas operativas:

| Etapa | Actividades Principales | Duración Estimada | Entregables |
| :--- | :--- | :---: | :--- |
| **Fase 1: Relevamiento y Análisis** | Entrevistas con stakeholders, levantamiento de requerimientos, análisis de flujos manuales actuales. | 1 Semana | Documento de Especificación de Requisitos (SRS), Matriz de trazabilidad. |
| **Fase 2: Diseño del Sistema** | Diseño de arquitectura lógica, diagramado de base de datos (DER), wireframes/prototipos de interfaces web. | 1 Semana | Documentos de arquitectura, Script `init_db.py`, Prototipos visuales. |
| **Fase 3: Desarrollo Backend y Base de Datos** | Creación de base de datos SQLite, desarrollo del servidor Flask (`app.py`), rutas, módulos de seguridad e interacción con DB. | 2 Semanas | Código fuente funcional (Lógica interna). |
| **Fase 4: Desarrollo Frontend e Integración** | Creación de las plantillas Jinja2, estilos CSS, integración de scripts JS y renderizado en cliente. Módulo reserva online. | 2 Semanas | Interfaces operativas vinculadas con backend. |
| **Fase 5: Pruebas y Aseguramiento de Calidad** | Testing de flujos principales (superposición de turnos, generación de cobros), auditoría de seguridad y validación funcional. | 1 Semana | Proyecto depurado, `README.md`, manual de instrucciones. |
| **Fase 6: Despliegue y Documentación Final** | Instalación local en el entorno del cliente, pruebas en producción, documentación técnica final (`docs/`). | 1 Semana | Repositorio documentado (`proyecto_gsell_final_v3.docx`), sistema en producción. |

**Duración Total Estimada:** 8 Semanas (2 meses de desarrollo calendario).

---

## 6.2. Presupuesto del Proyecto

El presupuesto se calcula con base en las horas de desarrollo técnico y la infraestructura mínima requerida. Se toma como referencia un proyecto *On-Premise* sin costos de licencias en la nube recurrentes en esta etapa.

### 6.2.1. Costos de Desarrollo (Recursos Humanos)
Se asume el rol de un Desarrollador Full-Stack / Analista de Sistemas trabajando de manera *freelance* o por proyecto.

* **Relevamiento, Análisis y Diseño:** 30 horas.
* **Desarrollo Backend y Frontend:** 80 horas.
* **Testing, Documentación y Despliegue:** 20 horas.
* **Total Horas de Ingeniería:** 130 horas.
* *Costo estimado por hora (promedio local)*: $15 USD (Sujeto a moneda local)
* **Subtotal Desarrollo:** $1,950 USD

### 6.2.2. Costos de Infraestructura y Herramientas (Capex / Opex)
Al utilizar una arquitectura de código abierto, se minimizan los costos operativos de licencias.

* **Software de desarrollo y Frameworks:** (Python, Flask, SQLite, Bootstrap) - $0 USD (Open Source).
* **Entorno de ejecución (Hardware local):** Asumiendo que el cliente provee una computadora estándar PC/Notebook comercial en el local - Costo Hundido ($0 para el proyecto).
* **Mantenimiento y Soporte Técnico (Opcional - Primeros 3 meses):** $150 USD/mes.

### 6.2.3. Presupuesto Total Estimado
| Concepto | Costo Estimado |
| :--- | :--- |
| Servicios Profesionales de Ingeniería de Software | $ 1,950.00 |
| Capacitación de personal y entrega (Setup Fee) | $ 200.00 |
| **Total Inversión Inicial (Lanzamiento)** | **$ 2,150.00** |

*El módulo de reservas online requeriría adicionalmente de un dominio y alojamiento web básico (Hosting + VPS pequeño), estimado en $15 USD/mes que será afrontado posteriormente por el negocio en caso de despliegue en la nube.*
