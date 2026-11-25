---
name: quality-strong
description: Extracts line items from PDF invoices into CSV files. Use when the user asks to pull invoice tables out of PDF documents. Do not use for scanned images without a text layer.
allowed-tools: Read, Bash(pdftotext:*)
---

# Invoice line items

Convert the invoice to text, then parse the table rows into CSV.

## Example

```bash
pdftotext -layout invoice.pdf invoice.txt
```

On Windows the tool is usually installed here:

```powershell
C:\Tools\pdftotext.exe -layout invoice.pdf invoice.txt
```

The column layout is described in [the format notes](references/FORMAT.md).
