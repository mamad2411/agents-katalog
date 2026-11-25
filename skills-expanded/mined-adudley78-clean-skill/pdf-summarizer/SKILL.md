---
name: pdf-summarizer
version: 1.0.0
description: Summarize a PDF file into 5 bullet points.
tools:
  - read_file
allowed_hosts: []
---

# PDF Summarizer

Given a path to a PDF, extract the text and return a concise 5-bullet summary.
Do not make network calls. Respect user-supplied page ranges.
