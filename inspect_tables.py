import docx

doc = docx.Document("proyecto_gsell.docx")

for i, table in enumerate(doc.tables):
    print(f"Table {i} style: {table.style.name}")
    for j, row in enumerate(table.rows[:2]):
        print(f"  Row {j}: {[cell.text[:20] for cell in row.cells]}")
