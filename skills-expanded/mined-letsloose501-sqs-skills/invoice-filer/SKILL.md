---
name: invoice-filer
description: Renames an incoming invoice to the supplier and date it carries and files it under the quarter. Use when an invoice PDF arrives, when the user asks where a supplier's paperwork went, or when the quarter has to be closed and the folder is still unsorted.
version: 1.2.0
allowed-tools: Read, Write, Bash
---

# Invoice filer

1. Read the supplier name and the issue date off the invoice.
2. Rename the file to `<supplier>-<YYYY-MM-DD>.pdf`.
3. Move it under `invoices/<year>-Q<quarter>/`.
4. Run `scripts/reindex.sh` so the quarter's index picks the new file up.
5. Print the path you wrote.
