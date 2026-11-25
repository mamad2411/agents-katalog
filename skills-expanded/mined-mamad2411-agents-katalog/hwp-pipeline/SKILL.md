---
name: hwp-pipeline
description: "Read, convert, and edit Korean Hangul documents (.hwp/.hwpx) without Hancom Office. HWP to JSON/Markdown/HTML conversion, HWP to HWPX conversion, HWPX editing with template filling and placeholder replacement."
license: MIT
tools:
  - Bash
  - Read
  - Write
  - Edit
metadata:
  category: documents
  locale: ko-KR
---

# hwp-pipeline

Read, convert, and edit Korean Hangul documents (`.hwp` / `.hwpx`) without Hancom Office.

## What this skill does

Three capabilities in one skill:

1. **Read HWP**: Convert `.hwp` to JSON, Markdown, or HTML via `@ohah/hwpjs` (Node.js)
2. **Convert HWP to HWPX**: Transform `.hwp` to editable `.hwpx` via `hwp2hwpx` (Java)
3. **Edit HWPX**: Create, modify, and template-fill `.hwpx` documents via `python-hwpx`

## When to use

- "Convert this HWP file to Markdown"
- "Extract images from a Hangul document"
- "Fill in this government form template (.hwp)"
- "Replace placeholders in this HWPX document"
- "Create a new HWPX document with tables"

## When not to use

- The file is `.docx` or `.pdf` (use the appropriate tool)
- OCR or scanned PDF recovery is needed

## Prerequisites

| Capability | Requires |
|-----------|----------|
| Read HWP (JSON/MD/HTML) | Node.js 18+ |
| Convert HWP to HWPX | Java 11+, Maven |
| Edit HWPX | Python 3.10+, `python-hwpx`, `lxml` |

Run `setup.sh` to install all dependencies automatically.

## Quick decision tree

1. **Extract text from HWP** → Use `@ohah/hwpjs` (Section A)
2. **Convert HWP to Markdown/HTML/JSON** → Use `@ohah/hwpjs` (Section A)
3. **Edit or fill an HWP form** → Convert to HWPX first (Section B), then edit (Section C)
4. **Extract text from HWPX** → Use `scripts/text_extract.py` (Section C)
5. **Replace placeholders in HWPX** → Use `scripts/zip_replace_all.py` (Section C)
6. **Create a new HWPX document** → Use `python-hwpx` directly (Section C)

---

## Section A: Read HWP

Uses `@ohah/hwpjs` (Node.js CLI). Works on macOS, Linux, and Windows.

### Install

```bash
npm install -g @ohah/hwpjs
export NODE_PATH="$(npm root -g)"
```

### Convert to JSON

```bash
hwpjs to-json document.hwp -o output.json --pretty
```

### Convert to Markdown

```bash
hwpjs to-markdown document.hwp -o output.md --include-images
# or save images separately:
hwpjs to-markdown document.hwp -o output.md --images-dir ./images
```

### Convert to HTML

```bash
hwpjs to-html document.hwp -o output.html
```

### Extract images only

```bash
hwpjs extract-images document.hwp -o ./images
```

### Batch processing

```bash
hwpjs batch ./documents -o ./output --format json --recursive
```

---

## Section B: Convert HWP to HWPX

Uses `hwp2hwpx` (Java, Apache 2.0 by neolord0). Converts binary `.hwp` to ZIP-based `.hwpx` so it can be edited with `python-hwpx`.

### First-time setup

```bash
bash setup.sh
```

This clones `hwp2hwpx`, patches the compiler version, builds a fat JAR, and installs `python-hwpx`.

### Convert

```bash
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"  # or set to skill install path
java -jar "$SKILL_DIR/java/hwp2hwpx-fat.jar" input.hwp output.hwpx
```

If the fat JAR is not available, use the classpath method:

```bash
cd "$SKILL_DIR/java"
CP=".:target/hwp2hwpx-1.0.0.jar:$(find ~/.m2/repository/kr/dogfoot -name '*.jar' | tr '\n' ':')"
java -cp "$CP" Convert input.hwp output.hwpx
```

### Limitations

- `hwpparser` (Python) is NOT supported: it loses table structure during conversion.
- Polaris Office cannot produce HWPX output.

---

## Section C: Edit HWPX

Uses `python-hwpx` (MIT by airmang). Full API reference: [`references/api.md`](references/api.md).

### Install

```bash
pip install -U python-hwpx lxml
```

### Extract text from HWPX

```bash
python3 scripts/text_extract.py input.hwpx
python3 scripts/text_extract.py input.hwpx --include-nested --format json
```

### Create a new HWPX document

```python
from hwpx import HwpxDocument

doc = HwpxDocument.new()
doc.add_paragraph("Document title")

table = doc.add_table(2, 2)
table.set_cell_text(0, 0, "Name")
table.set_cell_text(0, 1, "Value")

doc.save_to_path("output.hwpx")
```

See [`examples/01_create_and_save.py`](examples/01_create_and_save.py).

### Replace placeholders (including table cells)

```bash
python3 scripts/zip_replace_all.py template.hwpx output.hwpx \
  --replace "{name}=John" "{date}=2026-01-01" --auto-fix-ns
```

See [`examples/03_template_replace.py`](examples/03_template_replace.py) for the full pipeline.

### Style-based search and replace

```python
with HwpxDocument.open("input.hwpx") as doc:
    doc.replace_text_in_runs("TODO", "DONE", text_color="#FF0000")
    doc.save_to_path("output.hwpx")
```

### Fix namespaces after ZIP-level edits

```bash
python3 scripts/fix_namespaces.py input.hwpx --inplace --backup
```

---

## Workflow patterns

### Pattern 1: Fill a government/institutional HWP form

```
input.hwp → [hwp2hwpx] → template.hwpx → [zip_replace_all.py] → filled.hwpx
```

1. Convert HWP to HWPX: `java -jar java/hwp2hwpx-fat.jar form.hwp form.hwpx`
2. Identify placeholders: `python3 scripts/text_extract.py form.hwpx --include-nested`
3. Replace placeholders: `python3 scripts/zip_replace_all.py form.hwpx filled.hwpx --replace "{field}=value" --auto-fix-ns`

### Pattern 2: Extract and analyze HWP content

```
input.hwp → [hwpjs] → output.json or output.md
```

### Pattern 3: Create a new structured HWPX

```python
doc = HwpxDocument.new()
# Add paragraphs, tables, memos
doc.save_to_path("output.hwpx")
```

## Unstable areas

- `set_header_text()` and `set_footer_text()` may produce inconsistent layouts depending on the document version. If headers/footers cause problems, fix them in the template and only automate body, tables, and memos.
- Always verify output files after automated processing.

## Bundled resources

- [`references/api.md`](references/api.md) — python-hwpx API signatures and usage notes
- [`scripts/text_extract.py`](scripts/text_extract.py) — One-command text extraction CLI
- [`scripts/zip_replace_all.py`](scripts/zip_replace_all.py) — Global placeholder replacement including table cells
- [`scripts/fix_namespaces.py`](scripts/fix_namespaces.py) — XML namespace normalization after ZIP-level edits
- [`examples/01_create_and_save.py`](examples/01_create_and_save.py) — Create a new document with paragraphs and tables
- [`examples/02_extract_and_inspect.py`](examples/02_extract_and_inspect.py) — Extract text and inspect document structure
- [`examples/03_template_replace.py`](examples/03_template_replace.py) — Full pipeline: placeholder replacement + namespace fix

## Done when

- Requested conversion output exists and is valid
- Template placeholders are replaced and verified
- Batch processing count matches input count
- Output file opens correctly (verify with text extraction)
