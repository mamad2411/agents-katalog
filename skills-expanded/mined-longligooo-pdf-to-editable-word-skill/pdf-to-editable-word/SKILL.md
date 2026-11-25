---
name: pdf-to-editable-word
description: Convert PDF to Word or PDF to DOCX while preserving the original page layout and keeping text editable, searchable, and selectable. Use for PDF-to-Word conversion, editable DOCX creation, fixed-layout documents, table-heavy PDFs, vertical text, resumable long-document conversion, or output validation. Works as a portable Agent Skill for Codex, Claude Code, and other agents that can run the CLI. Do not use for scanned PDFs without a text layer unless OCR is available.
---

# PDF to Editable Word Skill

Create a visually faithful DOCX by combining cleaned page backgrounds with editable, absolutely positioned text boxes. Run the deterministic CLI for every conversion; do not recreate the OOXML manually.

## Workflow

1. Resolve this skill directory and use `scripts/pdf2word.py` as the command wrapper.
2. Inspect the source before converting:

```bash
python scripts/pdf2word.py inspect INPUT.pdf --json
```

3. Stop and report the limitation when `conversion_ready` is false. Read [compatibility.md](references/compatibility.md) for the relevant failure mode.
4. Convert into a dedicated work directory:

```bash
python scripts/pdf2word.py convert INPUT.pdf OUTPUT.docx --work-dir WORK_DIR --dpi 144
```

5. If conversion is interrupted, rerun the same command with `--resume`. Never reuse a work directory for a different PDF or page range.
6. Validate the output against the source:

```bash
python scripts/pdf2word.py validate OUTPUT.docx --pdf INPUT.pdf --json
```

7. Treat validation failure as conversion failure. Do not deliver the DOCX merely because the file exists.
8. For high-stakes output, open the result in Microsoft Word and inspect the first, middle, and last pages plus pages with unusual layouts.

## Delivery

Report the output path, page count, editable text-box count, background-image count, validation result, and any compatibility warnings. State clearly that text is editable while non-text graphics remain in the page background.

Do not claim that tables, diagrams, or images are semantically editable. Do not claim support for OCR, mixed page sizes, or LibreOffice fidelity in v0.1.
