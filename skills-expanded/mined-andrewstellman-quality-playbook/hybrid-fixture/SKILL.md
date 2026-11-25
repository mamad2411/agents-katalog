# Receipt Reconciler (Hybrid classifier fixture)

A skill plus Python orchestrator that helps a small business reconcile
expense receipts against their bookkeeping ledger. Used by
`bin/tests/test_classify_project.py` as a known-Hybrid target for the
v1.5.3 project-type classifier: SKILL.md at fixture root AND substantial
code under `bin/`.

The fixture is a synthetic skill, not a real one in production use. Its
SKILL.md prose is shorter than its code LOC; the heuristic should classify
it as Hybrid (the band where SKILL.md exists alongside dominant code).

## Overview

Receipts arrive as photos, PDFs, or paper that has been scanned. The
ledger is a CSV exported from the bookkeeping system. The skill's job is
to match each receipt to a ledger entry, flag mismatches, and produce a
reconciliation report the operator can hand to their accountant.

The skill is hybrid because the matching itself is mechanical (CSV parsing,
fuzzy string matching, date arithmetic) but the judgment calls — is this
$24.99 charge from the same coffee shop as that $25.04 charge in the
ledger, or two separate visits — need a model to decide.

## Phase 1 — Receipt ingestion

The orchestrator's `bin/ingest.py` walks the receipts folder, OCRs anything
that needs OCR, and emits a normalized JSON record per receipt: vendor,
date, amount, last-four-of-card. The JSON is the contract between the
mechanical layer and the skill prose.

The skill's role in Phase 1 is to verify the OCR output: when the OCR
confidence is below the configured threshold, the skill is asked to look
at the original image and either correct the field or flag it as unread-
able. Unreadable receipts go into a manual-review queue.

## Phase 2 — Ledger ingestion

The orchestrator's `bin/ledger.py` parses the bookkeeping CSV, normalizes
column names, and emits a JSON record per ledger entry. No skill involvement
in Phase 2 — the CSV format is fixed, parsing is mechanical.

## Phase 3 — Matching

The orchestrator's `bin/matcher.py` proposes candidate matches: for each
receipt, the top-K ledger entries by combined date proximity and amount
similarity. The skill is asked to confirm or reject each proposed match,
with an explanation when a match is rejected.

The skill's confirmations and rejections are written back through the
orchestrator's API so the orchestrator can track which receipts have been
matched and which still need human review.

## Phase 4 — Reconciliation report

The orchestrator's `bin/report.py` consolidates matched receipts, unmatched
receipts, and unmatched ledger entries into a single report. The skill is
asked to write the report's narrative summary: which categories had clean
reconciliation, which had problems, what the operator should look at first
when reviewing.

## Anti-patterns

The skill explicitly does not categorize expenses against tax categories,
estimate deductibility, or otherwise act as a tax advisor. Those decisions
are out of scope and the skill points the operator at their accountant.
