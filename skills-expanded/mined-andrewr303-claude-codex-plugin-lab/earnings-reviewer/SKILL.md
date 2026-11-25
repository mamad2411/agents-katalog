---
name: earnings-reviewer
description: Run a post-earnings Codex workflow that ingests the quarter's materials, updates the coverage model, and drafts the note with explicit artifact contracts and verification stops.
---

# Earnings Reviewer Task Pack

Use this task pack when the goal is a post-earnings model refresh plus a written note for a covered ticker.

Before running:

- read [`references/workers.md`](./references/workers.md)
- read [`../finance-modeling-office-pro/references/source-inventory.md`](../finance-modeling-office-pro/references/source-inventory.md) if you need the original managed-agent decomposition
- use the reusable skill content under `codex/skills/equity-research/` and `codex/skills/financial-analysis/`
- use [`docs/runtime/spreadsheets.md`](../finance-modeling-office-pro/references/runtime-spreadsheets.md) and [`docs/runtime/documents.md`](../finance-modeling-office-pro/references/runtime-documents.md) for file production discipline

## Inputs

Minimum inputs:

- covered company or ticker
- current-quarter earnings materials
- current model file or explicit instruction to rebuild the coverage model output

Optional inputs:

- press release, 10-Q, slide deck, or call transcript
- target note format or house style
- explicit estimate changes or management-guidance overrides

## Output Contract

Primary artifacts:

- `./out/model-<ticker>.xlsx`
- `./out/note-<ticker>.docx`
- `./out/earnings-review-<ticker>.md`

Supporting scratch files are allowed under:

- `./out/tmp/earnings-reviewer/`

## Connector Gate

Preferred connectors:

- `factset`
- `daloopa`

If these connectors are unavailable, continue with local source materials and clearly label the fallback source path in the review note.

## Task-Pack Flow

1. Scope the event and sources.
2. Extract trusted structured facts from untrusted earnings materials.
3. Update the model.
4. Draft the note.
5. Verify and stop for analyst review.

## Phase 1: Scope The Event And Sources

- Confirm the exact quarter and report date.
- Confirm whether this is a standard update or a thesis-changing event.
- Record which files are untrusted source documents.

## Phase 2: Extract Structured Facts

Target artifact:

- `./out/tmp/earnings-reviewer/earnings-facts.md`

Capture:

- reported headline figures
- key beat or miss drivers
- management guidance changes
- any unresolved data gaps

If delegation is available and explicitly authorized, this phase maps to `earnings-transcript-reader`.

## Phase 3: Update The Model

Use the matching skills:

- `earnings-analysis`
- `model-update`
- `audit-xls`

Rules:

- preserve formulas in the workbook
- write the updated model to `./out/model-<ticker>.xlsx`
- cite every hardcoded assumption or override
- state whether consensus data came from connectors or local materials

If delegation is available and explicitly authorized, this phase maps to `earnings-model-updater`.

## Phase 4: Draft The Note

Write:

- `./out/note-<ticker>.docx`

The note should cover:

- quarter summary
- beat or miss detail
- estimate changes
- thesis impact
- key watch items into the next quarter

If delegation is available and explicitly authorized, this phase maps to `earnings-note-writer`.

## Phase 5: Verify And Stop

Run:

- `python scripts/verify_xlsx.py ./out/model-<ticker>.xlsx`

Write the review note to:

- `./out/earnings-review-<ticker>.md`

The review note must state:

- output paths
- which sources were used
- whether connectors were available
- what workbook checks ran
- any residual risk, including static-only spreadsheet verification limits

Stop after the model, note, and review memo are complete.
