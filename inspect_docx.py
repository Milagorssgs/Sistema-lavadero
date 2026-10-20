import docx

doc = docx.Document("proyecto_gsell.docx")

for i, p in enumerate(doc.paragraphs):
    if p.text.strip():
        print(f"{i}: {p.text[:50]} (Style: {p.style.name})")
