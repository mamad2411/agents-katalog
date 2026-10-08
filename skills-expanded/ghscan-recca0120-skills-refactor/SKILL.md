---
name: processing-documents
description: "Processes various document formats and extracts content. Use when user asks to process documents, extract text, or convert file formats."
---

# Document Processor

Processes documents and extracts content.

> See [workflow-diagram.md](../shared/workflow-diagram.md)

> See [reference-resources.md](../shared/reference-resources.md)

## Steps

1. Read the input document
2. Detect the format
3. Extract content
4. Output in requested format

## Output Format

| Field | Type | Description |
|-------|------|-------------|
| content | string | Extracted text |
| format | string | Original format |
| pages | number | Page count |
