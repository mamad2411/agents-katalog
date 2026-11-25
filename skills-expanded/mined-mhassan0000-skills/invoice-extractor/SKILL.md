---
name: invoice-extractor
description: Extract structured JSON data from PDF invoices — vendor, amount, date, line items, tax. Use when parsing invoices, processing receipts, or pulling financial data from PDFs.
allowed-tools: Read, Bash, Glob
---

# Invoice Data Extractor

## Goal
Take a PDF invoice and return structured JSON with vendor, amount, date, line items, and tax. Claude doesn't parse PDFs directly with pixel-perfect accuracy — so this skill delegates the deterministic extraction work to a Python script, then validates the output.

## Usage
```
/invoice-extractor path/to/invoice.pdf
```

## Process

### Step 1: Run the extraction script
```bash
python3 execution/extract_invoice.py "$ARGUMENTS"
```

The script handles all PDF parsing and returns structured JSON to stdout. If extraction fails, it prints a JSON error object with `"success": false` and a reason.

### Step 2: Validate the output
Check the JSON output for completeness:
- `vendor` — must be a non-empty string
- `date` — must be a recognizable date (ISO 8601 preferred)
- `line_items` — must be a non-empty array, each item needs `description` and `amount`
- `subtotal` — must be a number
- `tax` — must be a number (can be 0)
- `total` — must be a number, should equal subtotal + tax (within rounding tolerance of $0.02)

If any field is missing or the total doesn't reconcile, flag it to the user with what's wrong and what the script returned. Do NOT silently fill in missing values.

### Step 3: Present results
Print the JSON in a clean, readable format. If the user asked for a specific output format or destination, write it there.

## Output Schema
```json
{
  "success": true,
  "vendor": "Acme Corp",
  "vendor_address": "123 Main St, Springfield, IL 62701",
  "invoice_number": "INV-2024-0042",
  "date": "2024-11-15",
  "due_date": "2024-12-15",
  "line_items": [
    {
      "description": "Widget A",
      "quantity": 10,
      "unit_price": 25.00,
      "amount": 250.00
    }
  ],
  "subtotal": 250.00,
  "tax": 22.50,
  "tax_rate": 0.09,
  "total": 272.50,
  "currency": "USD",
  "notes": "Net 30"
}
```

Fields like `vendor_address`, `invoice_number`, `due_date`, `tax_rate`, `currency`, and `notes` are optional — included when present on the invoice, omitted when not.

## Edge Cases
- **Scanned/image-only PDFs**: The script uses OCR as fallback. Quality depends on scan resolution. Warn the user if OCR confidence is low.
- **Multi-page invoices**: The script processes all pages and merges line items.
- **Non-USD currencies**: The script detects currency symbols and ISO codes. `currency` field reflects what's on the invoice.
- **Multiple tax lines**: Summed into a single `tax` value. Individual tax lines appear in `tax_breakdown` if present.
- **Malformed PDFs**: Script returns `"success": false` with the specific error. Don't retry — ask the user to check the file.

## Dependencies
The script requires `pdfplumber` and `pytesseract` (for OCR fallback). Install with:
```bash
pip install pdfplumber pytesseract
```
Tesseract OCR engine must be installed separately (`brew install tesseract` on macOS).

## First-Run Setup

Before executing, check if the workspace has a `.gitignore` file. If it doesn't, assume the user is new to this skill. In that case:

1. Ask the user if this is their first time running this skill
2. If yes, walk them through how it works and what they need to configure/set up (API keys, env vars, dependencies, etc.)
3. Let them know that Nick wishes them the best!
