# Watch Me Build A PDF Invoice Parsing Flow In Minutes

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What this does

Reads a list of PDF invoice URLs from a CSV, extracts the raw text from each PDF using PDF.co, then passes that text to GPT-4o to pull out three structured fields: total amount, line items, and sender address. Writes the enriched rows back out to `data/output.csv`.

This is the Python translation of the "Parse Invoice -> Add to Sheet" Make scenario: same logic, same prompt, no OAuth needed by default.

## When to trigger this

- You have a batch of invoice PDFs (as URLs) and want to extract structured data without manually opening each one
- You're building an accounts-payable or expense-tracking automation and need clean totals + line items
- You want to see how PDF text extraction + LLM parsing work together in a real pipeline

## Required env vars

```
PDFCO_API_KEY=your_pdf_co_key
OPENAI_API_KEY=your_openai_key
```

Set these in your `.env` or export them before running.

## Input CSV format

`data/input.csv` — one row per invoice, one column:

| invoice_url |
|---|
| https://example.com/invoice-001.pdf |

Rows with an empty `invoice_url` are skipped.

## Step-by-step procedure

1. Add your invoice URLs to `data/input.csv` (one URL per row under the `invoice_url` header).
2. Set `PDFCO_API_KEY` and `OPENAI_API_KEY` in your environment.
3. Run the pipeline:
   ```
   python scripts/parse_invoices.py
   ```
4. Results land in `data/output.csv` with columns: `invoice_url`, `total`, `line_items`, `from_address`.
5. If a PDF fails to convert or GPT returns malformed JSON, that row gets `error` logged and the script continues — you won't lose the whole batch.

## Node map (source Make scenario -> this skill)

| Make node | Module | Maps to |
|---|---|---|
| 5 | `google-sheets:filterRows` | `io_store.read_rows("data/input.csv")` |
| 6 | `pdf-co:PDFToAnything` (toTextSimple, inline) | `scripts/parse_invoices.py` → PDF.co `/v1/pdf/convert/to/text` |
| 7 | `openai-gpt-3:CreateCompletion` (gpt-4o) | `scripts/parse_invoices.py` → OpenAI chat completions |
| 8 | `json:ParseJSON` | `json.loads()` on GPT response |
| 10 | `util:SetVariables` (strippedTotal) | `float()` cast on total string |
| 9 | `google-sheets:updateRow` | `io_store.write_rows("data/output.csv")` |

**Conditional page logic** (source node 6): if the URL contains `"canadapost"`, only page 0 is extracted. This is preserved as-is in `parse_invoices.py`.
