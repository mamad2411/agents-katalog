---
name: document-processing
description: Parse, clean, validate, and convert PDFs, spreadsheets, CSVs, and documents into structured data.
origin: AI Dev Kit
---

# Document Processing

Parse, clean, validate, and convert documents (PDF, Excel, CSV, DOCX) into structured data.

## When to Use

- Extracting data from PDFs, invoices, reports, forms
- Processing Excel/CSV files with Pandas
- Converting DOCX to structured text
- Validating document schemas
- Building data ingestion pipelines

## PDF Processing

### Text Extraction

```python
import pdfplumber

def extract_text_from_pdf(path: str) -> str:
    """Extract all text from a PDF file."""
    with pdfplumber.open(path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def extract_tables_from_pdf(path: str) -> list[pd.DataFrame]:
    """Extract all tables from a PDF as DataFrames."""
    tables = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables() or []:
                if table:
                    header = table[0]
                    rows = table[1:]
                    tables.append(pd.DataFrame(rows, columns=header))
    return tables
```

### OCR for Scanned PDFs

```python
from pdf2image import convert_from_path
import pytesseract

def ocr_pdf(path: str) -> str:
    """Extract text from scanned PDFs using Tesseract OCR."""
    images = convert_from_path(path, dpi=300)
    return "\n".join(pytesseract.image_to_string(img) for img in images)
```

### LLM-Based Document Extraction

```python
from pydantic import BaseModel, Field
from openai import OpenAI

class InvoiceData(BaseModel):
    invoice_number: str
    date: str
    vendor: str
    total: float
    line_items: list[dict]

def extract_invoice(text: str) -> InvoiceData:
    """Extract structured invoice data from document text."""
    client = OpenAI()
    resp = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Extract invoice data. Return null for unknown fields."},
            {"role": "user", "content": text},
        ],
        response_format=InvoiceData,
    )
    return resp.choices[0].message.parsed
```

## Excel Processing

### Read with Validation

```python
import pandas as pd
from pydantic import BaseModel, ValidationError

class Row(BaseModel):
    id: int
    name: str
    email: str
    amount: float
    date: str

def process_excel(path: str, sheet: str | None = None) -> tuple[list[Row], list[dict]]:
    """Process Excel file, return valid rows and errors."""
    df = pd.read_excel(path, sheet_name=sheet or 0)
    valid = []
    errors = []
    for idx, row in df.iterrows():
        try:
            valid.append(Row(**row.to_dict()))
        except ValidationError as e:
            errors.append({"row": idx + 2, "error": str(e)})
    return valid, errors
```

### Write with Formatting

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

def write_excel(path: str, data: list[dict], headers: list[str]):
    """Write data to Excel with header styling."""
    wb = Workbook()
    ws = wb.active
    ws.append(headers)

    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4472C4", fill_type="solid")
    for cell in ws[1]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center")

    for row in data:
        ws.append([row.get(h) for h in headers])

    wb.save(path)
```

## CSV Processing

### Stream Processing for Large Files

```python
import csv

def process_large_csv(path: str, chunk_size: int = 10000):
    """Process large CSV files in chunks to avoid memory issues."""
    chunk = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            chunk.append(row)
            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk

def clean_csv(input_path: str, output_path: str, required_cols: list[str]):
    """Clean CSV: remove empty rows, validate columns, strip whitespace."""
    with open(input_path) as fin, open(output_path, "w", newline="") as fout:
        reader = csv.DictReader(fin)
        writer = csv.DictWriter(fout, fieldnames=required_cols)
        writer.writeheader()
        for row in reader:
            if all(row.get(c, "").strip() for c in required_cols):
                writer.writerow({c: row[c].strip() for c in required_cols})
```

### Pandas CSV with Type Coercion

```python
def load_csv_typed(path: str, schema: dict) -> pd.DataFrame:
    """Load CSV with explicit type coercion."""
    df = pd.read_csv(path)
    for col, dtype in schema.items():
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")
        df[col] = pd.to_numeric(df[col], errors="coerce") if dtype in (int, float) else df[col].astype(str)
    return df.dropna(subset=schema.keys())
```

## DOCX Processing

```python
from docx import Document

def extract_docx(path: str) -> dict:
    """Extract text, tables, and headings from DOCX."""
    doc = Document(path)
    return {
        "paragraphs": [p.text for p in doc.paragraphs if p.text.strip()],
        "tables": [[cell.text for cell in row.cells] for table in doc.tables for row in table.rows],
        "headings": [p.text for p in doc.paragraphs if p.style.name.startswith("Heading")],
    }
```

## Data Validation Pipeline

```python
from pydantic import BaseModel, field_validator
import pandas as pd

class DataRecord(BaseModel):
    id: str
    email: str
    amount: float
    status: str

    @field_validator("email")
    @classmethod
    def valid_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("invalid email")
        return v.lower()

    @field_validator("amount")
    @classmethod
    def positive_amount(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("amount must be positive")
        return round(v, 2)

def validate_records(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split DataFrame into valid and invalid records with error details."""
    valid = []
    invalid = []
    for idx, row in df.iterrows():
        try:
            DataRecord(**row.to_dict())
            valid.append(row)
        except Exception as e:
            invalid.append({**row.to_dict(), "_error": str(e), "_row": idx})
    return pd.DataFrame(valid), pd.DataFrame(invalid)
```

## Ingestion Pipeline Pattern

```python
from pathlib import Path
import hashlib

class IngestionPipeline:
    """Process documents with deduplication and audit trail."""

    def __init__(self, output_dir: str, processed_log: str):
        self.output = Path(output_dir)
        self.log = Path(processed_log)

    def _fingerprint(self, data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def is_duplicate(self, path: Path) -> bool:
        fp = self._fingerprint(path.read_bytes())
        if self.log.exists():
            return fp in self.log.read_text()
        return False

    def process(self, path: Path) -> dict:
        if self.is_duplicate(path):
            return {"status": "skipped", "reason": "duplicate"}
        result = self._extract(path)
        self._log(path)
        return result

    def _extract(self, path: Path) -> dict:
        # Dispatch based on file extension
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            return extract_text_from_pdf(str(path))
        elif suffix == ".xlsx":
            return {"sheets": pd.ExcelFile(path).sheet_names}
        elif suffix == ".csv":
            return pd.read_csv(path).to_dict(orient="records")
        elif suffix == ".docx":
            return extract_docx(str(path))
        raise ValueError(f"Unsupported format: {suffix}")

    def _log(self, path: Path):
        fp = self._fingerprint(path.read_bytes())
        with open(self.log, "a") as f:
            f.write(f"{fp}\n")
```

## Verification

- Test each extractor with valid and invalid documents
- Validate schema coercion catches bad types
- Confirm deduplication skips already-processed files
- Check error reporting includes row numbers and field names
- Benchmark memory usage for large files (>100MB)
