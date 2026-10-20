from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 12)
        self.cell(0, 10, 'PRACTICA PROFESIONAL', align='C')
        self.ln(5)
        self.set_font('helvetica', '', 12)
        self.cell(0, 10, '2026', align='L')
        self.ln(5)
        self.cell(0, 10, 'Carpeta Proyecto Final', align='L')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', '', 10)
        self.cell(0, 10, 'Gsell Milagros', align='L')
        self.set_x(0)
        self.cell(0, 10, str(self.page_no()), align='R')

data = [
    ["F-01", "Iniciar sesion", "app.py", "login()", "Implementado", ""],
    ["F-02", "Cerrar sesion (logout)", "app.py", "logout()", "Implementado", ""],
    ["F-03", "Crear usuarios", "app.py", "usuario_nuevo()", "Implementado", ""],
    ["F-04", "Editar y eliminar usuarios", "-", "-", "No implementado", "Fuera de alcance"],
    ["F-05", "Diferenciar roles", "app.py", "admin_required()", "Implementado", ""],
    ["F-06", "Registrar nuevos clientes", "app.py", "cliente_nuevo()", "Implementado", ""],
    ["F-07", "Editar datos de cliente", "app.py", "cliente_editar()", "Implementado", ""],
    ["F-08", "Eliminar clientes", "app.py", "cliente_eliminar()", "Implementado", ""],
    ["F-09", "Buscar clientes", "app.py", "clientes()", "Implementado", ""],
    ["F-10", "Guardar telefono", "app.py", "cliente_nuevo()", "Implementado", ""],
    ["F-11", "Tipo de vehiculo", "app.py", "vehiculo_nuevo()", "Implementado", ""],
    ["F-12", "Registrar vehiculos con datos", "app.py", "vehiculo_nuevo()", "Implementado", ""],
    ["F-13", "Asociar vehiculos a cliente", "app.py", "vehiculo_nuevo()", "Implementado", ""],
    ["F-14", "Editar vehiculo", "-", "-", "No implementado", "Prioridad menor"],
    ["F-15", "Historial", "app.py", "cliente_detalle()", "Implementado", ""],
    ["F-16", "Crear servicios", "app.py", "servicio_nuevo()", "Implementado", ""],
    ["F-17", "Editar servicios", "app.py", "servicio_editar()", "Implementado", ""],
    ["F-18", "Eliminar servicios", "app.py", "servicio_eliminar()", "Implementado", ""],
    ["F-19", "Asignar precios", "app.py", "servicio_nuevo()", "Implementado", ""],
    ["F-20", "Listar servicios", "app.py", "servicios()", "Implementado", ""],
    ["F-21", "Crear turnos", "app.py", "turno_nuevo()", "Implementado", ""],
    ["F-22", "Modificar turnos", "-", "-", "No implementado", "Cancelar y crear nuevo"],
    ["F-23", "Cancelar turnos", "app.py", "turno_id_estado()", "Implementado", ""],
    ["F-24", "Ver agenda", "app.py", "turnos()", "Implementado", ""],
    ["F-25", "Evitar superposicion", "app.py", "turno_nuevo()", "Implementado", ""],
    ["F-26", "Asignar cliente/vehiculo", "app.py", "turno_nuevo()", "Implementado", ""],
    ["F-27", "Asignar servicio", "app.py", "turno_nuevo()", "Implementado", ""],
    ["F-28", "Registrar pago", "app.py", "pago_nuevo()", "Implementado", ""],
    ["F-29", "Metodo de pago", "app.py", "pago_nuevo()", "Implementado", ""],
    ["F-30", "Historial pagos", "app.py", "pagos()", "Implementado", ""],
    ["F-31", "Estado pago", "app.py", "pago_nuevo()", "Implementado", ""],
    ["F-32", "Ingresos diarios", "app.py", "dashboard()", "Implementado", ""],
    ["F-33", "Ingresos mensuales", "app.py", "reportes()", "Parcial", "Solo ultimos 7 dias"],
    ["F-34", "Autos atendidos", "app.py", "dashboard()", "Implementado", ""],
    ["F-35", "Servicios mas usados", "app.py", "dashboard()", "Implementado", ""],
    ["F-36", "Resumen", "app.py", "dashboard()", "Implementado", ""],
    ["F-37", "Recordatorios", "-", "-", "No implementado", "Falta integracion externa"],
    ["F-38", "Avisos turno", "-", "-", "No implementado", "Falta integracion externa"],
    ["F-39", "Cancelaciones", "app.py", "dashboard()", "Parcial", "Solo visual en dashboard"],
    ["F-40", "Generar ticket", "app.py", "comprobante_pago()", "Implementado", ""],
    ["F-41", "Detalle servicio", "app.py", "comprobante_pago()", "Implementado", ""],
    ["F-42", "Imprimir", "app.py", "comprobante_pago()", "Parcial", "Usa impresion web"],
    ["F-43", "Buscar turnos", "app.py", "turnos()", "Parcial", "Solo filtros basicos"],
    ["F-44", "Filtrar cliente", "app.py", "clientes()", "Implementado", ""],
    ["F-45", "Filtrar servicio", "-", "-", "No implementado", "No es necesario aun"],
    ["F-46", "Buscar patente", "app.py", "vehiculos()", "Implementado", ""],
    ["F-47", "Horarios", "app.py", "configuracion()", "Implementado", ""],
    ["F-48", "Precios", "app.py", "configuracion()", "Implementado", ""],
    ["F-49", "Tipos servicios", "app.py", "configuracion()", "Implementado", ""],
    ["F-50", "Duracion servicios", "app.py", "configuracion()", "Implementado", ""]
]

pdf = PDF()
pdf.add_page()
pdf.set_font("helvetica", "B", 16)
pdf.cell(0, 10, "6.3 Tabla de trazabilidad", ln=True)
pdf.ln(5)

pdf.set_font("helvetica", "", 11)
pdf.multi_cell(0, 7, "A continuacion, se detalla el estado actual de los requerimientos funcionales definidos en el punto 5.7, con su correspondiente nivel de implementacion en el sistema.")
pdf.ln(5)

pdf.set_font("helvetica", "B", 8)
col_widths = [10, 48, 22, 33, 23, 54]
headers = ["Req", "Descripcion", "Archivo", "Funcion", "Estado", "Observacion"]

for i in range(len(headers)):
    pdf.cell(col_widths[i], 8, headers[i], border=1)
pdf.ln()

pdf.set_font("helvetica", "", 7)
for row in data:
    pdf.cell(col_widths[0], 6, row[0], border=1)
    pdf.cell(col_widths[1], 6, row[1][:38], border=1)
    pdf.cell(col_widths[2], 6, row[2], border=1)
    pdf.cell(col_widths[3], 6, row[3], border=1)
    pdf.cell(col_widths[4], 6, row[4], border=1)
    pdf.cell(col_widths[5], 6, row[5][:55], border=1)
    pdf.ln()

pdf.ln(10)
pdf.set_font("helvetica", "B", 12)
pdf.cell(0, 10, "Repositorio del proyecto:", ln=True)
pdf.set_font("helvetica", "", 12)
pdf.set_text_color(0, 0, 255)
repo_link = "https://github.com/Milagorssgs/Sistema-lavadero"
pdf.cell(0, 10, repo_link, link=repo_link, ln=True)
pdf.set_text_color(0, 0, 0)
pdf.ln(5)

pdf.set_font("helvetica", "B", 14)
pdf.cell(0, 10, "Indice de la Carpeta (Estado)", ln=True)
pdf.set_font("helvetica", "", 12)

indice = [
    ("1. Caratula", "Terminado"),
    ("2. Indice", "Terminado"),
    ("3. Titulo", "Terminado"),
    ("4. Resumen del sistema", "Terminado"),
    ("5. Analisis", "Terminado"),
    ("   5.1. Introduccion", "Terminado"),
    ("   5.2. Descripcion General", "Terminado"),
    ("   5.3. Justificacion", "Terminado"),
    ("   5.4. Objetivos Generales", "Terminado"),
    ("   5.5. Objetivos Especificos", "Terminado"),
    ("   5.6. Limites del Sistema", "Terminado"),
    ("   5.7. Requerimientos del Sistema", "Terminado"),
    ("   5.8. Casos de uso", "Terminado"),
    ("   5.9. Estudio de Factibilidad", "Terminado"),
    ("   5.10. Cronograma", "Terminado"),
    ("   5.11. Presupuesto", "Terminado"),
    ("6. Diseno", "En desarrollo"),
    ("   6.1. Diagrama Entidad-Relacion", "En desarrollo"),
    ("   6.2. Frontend / Prototipo", "Terminado"),
    ("   6.3. Tabla de trazabilidad", "Terminado"),
    ("7. Conclusion sobre el Proyecto", "En desarrollo"),
    ("8. Bibliografia", "Sin iniciar"),
    ("9. Glosario de palabras tecnicas", "Sin iniciar")
]

pdf.set_font("helvetica", "B", 10)
pdf.cell(100, 7, "Punto del Indice", border=1)
pdf.cell(40, 7, "Estado", border=1)
pdf.ln()

pdf.set_font("helvetica", "", 10)
for item, estado in indice:
    pdf.cell(100, 6, item, border=1)
    pdf.cell(40, 6, estado, border=1)
    pdf.ln()

pdf.output("6.3_Tabla_de_Trazabilidad_Lavadero_v2.pdf")
