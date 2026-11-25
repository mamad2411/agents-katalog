---
name: pdf-tools
description: Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.
license: Apache-2.0
compatibility: Requires Python 3.11+ and pypdf
metadata:
  author: skillforge-team
  version: "1.0"
allowed-tools: Bash(python:*) Read
---

# PDF tools

1. Identify the operation: extract, fill, or merge.
2. For extraction run `scripts/extract.py <file>`.
3. See [the reference guide](references/REFERENCE.md) for form field names.
