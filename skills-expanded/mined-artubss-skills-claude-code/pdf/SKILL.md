---
name: pdf
description: "Kit de ferramentas para manipulação de PDF. Extrair texto/tabelas, criar PDFs, mesclar/dividir, preencher formulários, para processamento e análise de documentos programática."
license: Proprietary. LICENSE.txt has complete terms
---

# Guia de Processamento de PDF

## Visão Geral

Extrair texto/tabelas, criar PDFs, mesclar/dividir arquivos, preencher formulários usando bibliotecas Python e ferramentas de linha de comando. Aplique essa habilidade para processamento e análise de documentos programática. Para recursos avançados ou preenchimento de formulários, consulte reference.md e forms.md.

## Aprimoramento Visual com Esquemas Científicos

**Ao criar documentos com essa habilidade, sempre considere adicionar diagramas científicos e esquemas para aprimorar a comunicação visual.**

Se seu documento ainda não contém esquemas ou diagramas:
- Use a habilidade **scientific-schematics** para gerar diagramas de qualidade para publicação alimentados por IA
- Simplesmente descreva seu diagrama desejado em linguagem natural
- Nano Banana Pro gerará, revisará e refinará o esquema automaticamente

**Para novos documentos:** Esquemas científicos devem ser gerados por padrão para representar visualmente conceitos-chave, workflows, arquiteturas ou relacionamentos descritos no texto.

**Como gerar esquemas:**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

A IA gerará automaticamente:
- Imagens de qualidade para publicação com formatação apropriada
- Revisão e refinamento através de múltiplas iterações
- Garantia de acessibilidade (amigável para daltônicos, alto contraste)
- Salvamento dos resultados no diretório figures/

**Quando adicionar esquemas:**
- Diagramas de workflow de processamento de PDF
- Flowcharts de manipulação de documentos
- Visualizações de processamento de formulários
- Diagramas de pipeline de extração de dados
- Qualquer conceito complexo que se beneficie de visualização

Para orientação detalhada sobre criação de esquemas, consulte a documentação da habilidade scientific-schematics.

---

## Início Rápido

```python
from pypdf import PdfReader, PdfWriter

# Ler um PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extrair texto
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## Bibliotecas Python

### pypdf - Operações Básicas

#### Mesclar PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

#### Dividir PDF
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

#### Extrair Metadados
```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
```

#### Rotacionar Páginas
```python
reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # Rotacionar 90 graus no sentido horário
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### pdfplumber - Extração de Texto e Tabelas

#### Extrair Texto Preservando Layout
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

#### Extrair Tabelas
```python
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

#### Extração Avançada de Tabelas
```python
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:  # Check if table is not empty
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# Combinar todas as tabelas
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

### reportlab - Criar PDFs

#### Criação Básica de PDF
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter

# Adicionar texto
c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "This is a PDF created with reportlab")

# Adicionar uma linha
c.line(100, height - 140, 400, height - 140)

# Salvar
c.save()
```

#### Criar PDF com Múltiplas Páginas
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Adicionar conteúdo
title = Paragraph("Report Title", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

body = Paragraph("This is the body of the report. " * 20, styles['Normal'])
story.append(body)
story.append(PageBreak())

# Página 2
story.append(Paragraph("Page 2", styles['Heading1']))
story.append(Paragraph("Content for page 2", styles['Normal']))

# Construir PDF
doc.build(story)
```

## Ferramentas de Linha de Comando

### pdftotext (poppler-utils)
```bash
# Extrair texto
pdftotext input.pdf output.txt

# Extrair texto preservando layout
pdftotext -layout input.pdf output.txt

# Extrair páginas específicas
pdftotext -f 1 -l 5 input.pdf output.txt  # Pages 1-5
```

### qpdf
```bash
# Mesclar PDFs
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Dividir páginas
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf --pages . 6-10 -- pages6-10.pdf

# Rotacionar páginas
qpdf input.pdf output.pdf --rotate=+90:1  # Rotate page 1 by 90 degrees

# Remover senha
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

### pdftk (se disponível)
```bash
# Mesclar
pdftk file1.pdf file2.pdf cat output merged.pdf

# Dividir
pdftk input.pdf burst

# Rotacionar
pdftk input.pdf rotate 1east output rotated.pdf
```

## Tarefas Comuns

### Extrair Texto de PDFs Digitalizados
```python
# Requer: pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path

# Converter PDF em imagens
images = convert_from_path('scanned.pdf')

# OCR em cada página
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

### Adicionar Marca d'água
```python
from pypdf import PdfReader, PdfWriter

# Criar marca d'água (ou carregar existente)
watermark = PdfReader("watermark.pdf").pages[0]

# Aplicar em todas as páginas
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

### Extrair Imagens
```bash
# Usar pdfimages (poppler-utils)
pdfimages -j input.pdf output_prefix

# Isto extrai todas as imagens como output_prefix-000.jpg, output_prefix-001.jpg, etc.
```

### Proteção por Senha
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# Adicionar senha
writer.encrypt("userpassword", "ownerpassword")

with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

## Referência Rápida

| Tarefa | Melhor Ferramenta | Comando/Código |
|--------|-------------------|----------------|
| Mesclar PDFs | pypdf | `writer.add_page(page)` |
| Dividir PDFs | pypdf | Uma página por arquivo |
| Extrair texto | pdfplumber | `page.extract_text()` |
| Extrair tabelas | pdfplumber | `page.extract_tables()` |
| Criar PDFs | reportlab | Canvas ou Platypus |
| Mesclar linha de comando | qpdf | `qpdf --empty --pages ...` |
| OCR em PDFs digitalizados | pytesseract | Converter em imagem primeiro |
| Preencher formulários PDF | pdf-lib ou pypdf (consulte forms.md) | Consulte forms.md |

## Próximas Etapas

- Para uso avançado de pypdfium2, consulte reference.md
- Para bibliotecas JavaScript (pdf-lib), consulte reference.md
- Se você precisar preencher um formulário PDF, siga as instruções em forms.md
- Para guias de solução de problemas, consulte reference.md