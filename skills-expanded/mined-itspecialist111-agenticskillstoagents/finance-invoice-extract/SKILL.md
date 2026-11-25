# finance/invoice-extract — skill payload

> This file is rendered by an MCP agent when it asks for
> `skill://finance/invoice-extract/SKILL.md`. The manifest at
> [`../invoice-extract.manifest.json`](../invoice-extract.manifest.json)
> is the machine-readable contract; this file is the *narrative* a host
> LLM reads before deciding to invoke the skill.

## What this skill does

Pulls structured fields (supplier, invoice number, line items, totals,
tax) out of a single invoice document (PDF, image, or scanned page).
Returns an `InvoiceFields` record that downstream skills can consume —
notably `finance/po-match` for three-way reconciliation.

## When to use it

- The user has an invoice and wants to do *anything* programmatic with
  its contents.
- A composed workflow needs `InvoiceFields` as input.
- You already have raw OCR text but need it structured into named fields.

## When **not** to use it

- The document is not an invoice (use a general document-parse skill).
- You need multi-document batch processing (this skill is single-doc;
  call it in a loop or look for an `invoice.batch-extract` capability).
- The data classification is `restricted` or higher — this skill is
  certified up to `confidential` only.

## Inputs and outputs

| | Type | Notes |
|---|---|---|
| **Input** | `InvoiceDocument` | PDF, JPG, PNG; <20 MB |
| **Output** | `InvoiceFields` | See [`assets/output-schema.json`](assets/output-schema.json) |
| **Preconditions** | `document.readable` | The blob must be fetchable and OCR-able |

## Determinism and risk

Determinism score: **0.7** — same input, same output ≥ 70% of the time
on the validation set. Risk: **low** — read-only, no side effects on
external systems. Safe to call speculatively.

## How it composes

`document.parse` → `invoice.extract` → (downstream) `invoice.match`
→ `po.reconcile`. See the ontology graph at
[`prototype/out/ontology.mmd`](../../../prototype/out/ontology.mmd).
