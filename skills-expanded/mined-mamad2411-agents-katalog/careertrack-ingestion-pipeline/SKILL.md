---
name: careertrack-ingestion-pipeline
description: Use this skill when building, extending, or debugging any part of the CareerTrack placement portal — especially the multi-source ingestion pipeline (WhatsApp .txt export parsing, Excel/Forms import, Gmail offer-letter OCR), the LLM-based field extraction step, schema normalization, fuzzy matching, and Union-Find student-record merging. Trigger on mentions of "CareerTrack", "ingestion pipeline", "student record merge", "identity resolution", "fuzzy match students", "merge conflict", or when adding a new placement data source or a new extracted field.
---

# CareerTrack ingestion pipeline — build guide

This skill packages the conventions and gotchas for the ingestion + identity-resolution module described in `specsheet.md` (architecture, algorithms) and `spreadsheet.md` (schema, task breakdown, roadmap). Read those two files first if they're in the repo — this file is the "how to actually write the code" layer on top of them.

## What this module does, in one sentence

Takes messy records from three sources (Excel/Forms, WhatsApp `.txt`, Gmail PDFs), extracts structured fields via an LLM call, normalizes them to one schema, and merges duplicate students into one canonical record using fuzzy similarity + Union-Find — never silently overwriting a conflict.

## Directory structure (recommended)

```
/backend
  /ingestion
    parsers/          # one file per source type: excel_parser, whatsapp_parser, gmail_parser
    extraction/        # LLM prompt + schema validation
    normalization/      # unit conversion, casing, date parsing
    matching/           # similarity scoring + union-find
    conflicts/           # conflict detection + resolution endpoints
  /core                # students, placements, documents, auth
  /smart               # readiness score, eligibility engine
  /trust               # anomaly detection, reports, consent
```

Keep `ingestion/` self-contained — the rest of the app should only ever talk to it through `raw_ingested_records` and the merge output, never reach into its internals.

## Conventions

- **LLM extraction calls always use a fixed system prompt and a fixed JSON schema.** Never let the model free-write. Set `temperature: 0`. Validate the response against the schema before writing anywhere — if validation fails, retry once, then route to a manual-review queue. Never guess a missing field.
- **Every extracted record carries provenance.** `source_type` and `source_ref` are mandatory, non-nullable fields on every `raw_ingested_records` row. If you can't answer "which source did this value come from," you've built it wrong.
- **Confidence scores are mandatory, not optional.** Both the extraction step and the matching step should output a confidence value. Anything below the threshold (default 0.82 for matching — see `specsheet.md` §7.1) goes to the conflict/review queue, not straight into `students`.
- **Never auto-resolve a field conflict.** If two sources disagree on a value for the same merged student, create a row in `merge_conflicts` and leave the field unset (or keep the highest-confidence value as a placeholder, clearly marked unverified) until a faculty member resolves it.
- **Ingestion is async.** A file upload endpoint returns a job ID immediately; the actual parse → extract → normalize → merge pipeline runs in a background worker (Redis queue). Don't block a request on an LLM call plus OCR — it will time out and it will look broken in a live demo.
- **Idempotency:** re-uploading the same file should not create duplicate `raw_ingested_records` rows. Hash the file content or use a source-specific dedup key (WhatsApp message timestamp+sender+text; Excel row hash; Gmail message ID).

## Adding a new ingestion source (step-by-step)

1. Write a parser in `parsers/` that turns the raw file into a list of plain-text or semi-structured "chunks" — one chunk per candidate record. Do not call the LLM inside the parser.
2. Feed each chunk through the shared extraction function (`extraction/extract.py` or equivalent) — do not write a source-specific extraction prompt; the whole point is one schema, one prompt, many sources.
3. Confirm the normalization layer already handles any new units/formats this source introduces; add a rule if not.
4. Run the matching step unchanged — it should not need to know which source a record came from.
5. Add a test case with a realistic sample file for this source (see QA checklist in `spreadsheet.md` §6).

## Adding a new extracted field

1. Add the field to the shared JSON schema used in the extraction prompt.
2. Add a normalization rule if the field needs unit/format conversion.
3. Add the field to the similarity function in `matching/` **only if** it should influence merge decisions (most new fields shouldn't — only identity-bearing fields like name/roll_no/email should).
4. Migrate the `students` table and update the `spreadsheet.md` schema table to keep docs in sync.

## Do / don't

**Do:**
- Log every merge decision (who/what merged, on what confidence, at what timestamp) — this is required for DPDP-related auditability, not optional polish.
- Cache LLM extraction results keyed by content hash — re-processing the same file during dev/demo shouldn't burn API calls.
- Write the reconciliation summary ("N processed, M merged, K flagged") as a first-class API response, not an afterthought — it's the single most demo-convincing part of this feature.

**Don't:**
- Don't let the LLM extraction step also make the merge decision. Extraction and matching are separate, independently testable steps.
- Don't silently pick "the most recent source" to resolve a conflict. That's exactly the behavior that erodes faculty trust in the system.
- Don't block the UI thread on OCR or LLM calls.
- Don't hardcode the similarity threshold in multiple places — one config value, referenced everywhere.

## Testing checklist for this module

- A WhatsApp export with emoji/mixed language content parses without crashing (malformed lines should be skipped and logged, not fatal).
- Two different students with similar names (e.g. "Pavan K" vs "Pavan S") are NOT merged.
- The same student appearing in all three sources merges into exactly one canonical record.
- A genuinely conflicting field (different CTC in two sources) produces a `merge_conflicts` row, not a silent overwrite.
- Re-uploading an already-processed file does not create duplicate records.

## Vibe-coding prompts that work well for this module

When delegating a task on this module to an AI coding agent, give it the specific sub-piece, not the whole pipeline at once:

- "Write the WhatsApp `.txt` parser: input is raw export text, output is a list of `{timestamp, sender, raw_text}` dicts. Skip malformed lines and log them, don't crash."
- "Write the LLM extraction function. It takes a raw text chunk and a source_type, calls the Claude API with the fixed system prompt in `extraction/prompt.md`, validates the JSON response against `extraction/schema.json`, and retries once on validation failure before raising."
- "Write the similarity scoring function per the weights in `specsheet.md` §7.2 — pure function, no I/O, so it's easy to unit test with hardcoded record pairs."
- "Write the Union-Find merge given a list of records and a similarity function — see the pseudocode in `specsheet.md` §7.1."

Keep each request scoped to one function/module. This pipeline has clean seams (parse → extract → normalize → match → merge) specifically so it can be built and tested one seam at a time rather than as one big-bang feature.
