# PDF Processor Skill

## Skill Name
`pdf-processor`

## Description
Skill for processing and extracting text from PDF files, with support for Polish language and diacritical characters.

## Capabilities
- Extracting text from PDF files
- OCR support for scanned documents
- Detecting Polish diacritical characters
- Text cleaning and normalization

## Usage
```yaml
skill: pdf-processor
options:
  ocr: true
  language: "pol"
  output-format: "markdown"
  preserve-layout: false
```

## Scripts
- `scripts/extract.py` - Main PDF extraction script
- `scripts/clean.py` - Text cleaning utilities

## Output
Returns cleaned text in Markdown or plain text format.
