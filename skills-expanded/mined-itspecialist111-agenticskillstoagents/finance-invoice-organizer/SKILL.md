# finance/invoice-organizer — skill payload

> Machine-readable contract: [`../invoice-organizer.manifest.json`](../invoice-organizer.manifest.json).

## What this skill does

Walks a folder of mixed invoice files (PDFs, scanned images), extracts
the supplier / invoice number / invoice date from each via
`finance/invoice-extract`, then moves each file into a
`<supplier>/<YYYY-MM>/` subfolder using the canonical filename
`YYYY-MM_<supplier>_<number>.<ext>`. Writes a CSV index mapping
original path → new path → extracted fields, so the move is fully
reversible.

## When to use it

- A bookkeeper has dumped a month's invoices into one folder and wants
  them filed.
- You're migrating an AP archive into a structured tree.

## When **not** to use it

- The folder contains anything *other than* invoices — files that fail
  extraction are left in place, but for cleanliness pre-filter.
- The target system is a DMS (SharePoint, M-Files) — use its API, don't
  rename on disk.

## Determinism and risk

Determinism: **medium** — depends on extractor accuracy. Risk: **medium**
— moves files. Mitigations: CSV reversal manifest, dry-run mode, skips
files where extraction confidence is below threshold.

## How it composes

Hard dependency on `invoice.extract` (calls `finance/invoice-extract`
per file). Output CSV is the natural input to a downstream
"reconcile-with-ERP" workflow.
