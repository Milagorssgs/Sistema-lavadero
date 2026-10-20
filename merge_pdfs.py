from pypdf import PdfWriter

merger = PdfWriter()

merger.append("proyecto_gsell.pdf")
merger.append("6.3_Tabla_de_Trazabilidad_Lavadero_v2.pdf")

merger.write("proyecto_gsell_final.pdf")
merger.close()
