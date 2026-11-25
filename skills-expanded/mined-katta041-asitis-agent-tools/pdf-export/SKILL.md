---
name: pdf-export
description: Export a markdown report to PDF with the house template. Use when the user asks for a PDF, a client-ready report or a printable version.
allowed-tools: Read Bash(pandoc:*)
---
# PDF export

1. Read the report with the Read tool.
2. Run `pandoc report.md -o report.pdf --template=house.tex`.
3. Tell the user where the PDF is.

See [the template notes](reference.md).
