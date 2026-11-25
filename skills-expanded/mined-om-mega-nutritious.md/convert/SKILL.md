---
name: convert
description: Convert PDF, Word, PowerPoint, Excel, HTML, or audio files to clean Markdown before analysis. Use whenever the user uploads or references a document file, or asks to "convert", "extract text from", or "read" a non-text file.
---

# Nutritious.md — Document to Markdown Converter

When the user references a file that isn't plain text (.pdf, .docx, .pptx,
.xlsx, .xls, .html, audio), run:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/setup_env.sh
${CLAUDE_PLUGIN_ROOT}/.venv/bin/python ${CLAUDE_PLUGIN_ROOT}/scripts/convert.py "<file path>"
```

Parse the returned JSON's `markdown` field and use it as the document's
content going forward. If the JSON contains a `warning` field about empty
text extraction, tell the user the file may be a scanned/image-only document
and no OCR is available. If the JSON contains an `error` field, tell the
user the conversion failed and report the error message.
