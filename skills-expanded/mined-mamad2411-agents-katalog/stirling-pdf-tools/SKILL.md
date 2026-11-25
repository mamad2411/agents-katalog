---
name: stirling-pdf-tools
description: Comprehensive PDF toolkit with Stirling PDF
version: 1.0.0
tags: [pdf, documents, ocr, conversion]
---

# Stirling PDF – Self-Hosted PDF Toolkit

Stirling PDF is a locally hosted, Docker-based web application for
performing various operations on PDF files — merge, split, convert,
OCR, sign, watermark, and more.

- **GitHub**: github.com/Stirling-Tools/Stirling-PDF (60 000+ ⭐)
- **License**: MIT
- **Security**: Self-contained Docker image. No external calls. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{STIRLING_URL}}` | Base URL of the Stirling PDF instance |

## Usage Examples

### Merge PDFs

```bash
curl -s -X POST "{{STIRLING_URL}}/api/v1/general/merge-pdfs" \
  -F "fileInput=@file1.pdf" \
  -F "fileInput=@file2.pdf" \
  -o merged.pdf
```

### Convert PDF to images

```bash
curl -s -X POST "{{STIRLING_URL}}/api/v1/convert/pdf/img" \
  -F "fileInput=@document.pdf" \
  -F "imageFormat=png" \
  -o images.zip
```

### OCR a scanned PDF

```bash
curl -s -X POST "{{STIRLING_URL}}/api/v1/misc/ocr-pdf" \
  -F "fileInput=@scanned.pdf" \
  -F "languages=eng" \
  -o ocr_result.pdf
```

## AI Agent Tips

- All processing happens locally — no data leaves the server.
- Supports 30+ PDF operations via API endpoints.
- OCR uses Tesseract; supports multiple languages.
- Deploy with Docker for zero-config operation.
