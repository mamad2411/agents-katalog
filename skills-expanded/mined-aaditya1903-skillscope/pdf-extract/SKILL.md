---
name: pdf-extract
description: Extract text, tables and form field values from PDF files, including scanned pages that need optical character recognition. Use when information is trapped in a PDF and needs to become structured data.
license: MIT
compatibility: Requires a PDF text layer, or an OCR engine for scanned pages.
allowed-tools: Read Bash
metadata:
  category: documents
---

# PDF extraction

Turn a PDF into structured data without guessing at content the file does not
actually contain.

## Deciding the approach

First determine whether the PDF has a text layer. If it does, extract directly.
If it does not, the pages are images and need OCR, which introduces character
errors that must be reported rather than hidden.

## Extracting tables

Table extraction is the least reliable part of any PDF pipeline. Extract the
candidate table, then verify the row and column counts against the rendered
page before using the values.

## Reporting confidence

Record which pages used OCR and which used the text layer, so a reader knows
which values may contain recognition errors.
