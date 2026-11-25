---
name: prd-improve
description: Improve an existing PRD - deepen thin sections, fix ambiguities, add missing scenarios and metrics, restructure to a rigorous format. Use when the user has a PRD, spec, or requirements doc that needs to be strengthened or updated.
license: MIT
metadata:
  author: andrewr303
  version: "2.0"
---

Improve an existing PRD: diagnose weaknesses against a rigorous rubric, then fix them surgically while preserving the author's intent and voice.

**Supporting files** (under `templates/` at the plugin root):
- `templates/prd-template.md` — target structure
- `templates/review-rubric.md` — scoring dimensions and CRITICAL triggers
- `templates/question-bank.md` — questions for filling gaps

**Input**: Path to an existing PRD (or pasted content). If no path given, search for likely candidates (`docs/**/*prd*.md`, `*.prd.md`, files titled "PRD"/"Product Requirements") and ask the user to confirm — never guess.

## Steps

### 1. Diagnose

- Read the PRD **from disk** (not from conversation memory — it may have changed).
- Read `templates/review-rubric.md` and score all 10 dimensions. Check every automatic CRITICAL trigger.
- Scan for every ambiguity word from the rubric's word list in normative text.
- Build a traceability map: goals ↔ metrics ↔ requirements ↔ non-goals. Note orphans and contradictions.
- Classify each finding CRITICAL / WARNING / SUGGESTION.

### 2. Agree on scope of surgery

Present a compact diagnosis: scorecard, top findings, and a proposed fix plan grouped into:
1. **Fix silently** — mechanical: ambiguity words → concrete values you can infer, missing IDs, format normalization, scenario formatting.
2. **Fix with assumptions** — content gaps you can fill from the codebase or reasonable inference, each marked `[assumed]`.
3. **Needs the author** — decisions only they can make (metrics targets, scope calls, priorities).

Ask the user (AskUserQuestion where available): "Full rewrite to the template structure, or in-place improvement preserving your structure?" Default to **in-place** — respect the existing document unless it's structurally beyond saving (overall score < 4).

For category 3, ask the questions — in waves of 3–5, highest-leverage first, using `templates/question-bank.md` for phrasing. If the user is unavailable, convert each to an Open Questions entry rather than guessing.

### 3. Improve

Apply fixes with the discipline of a code refactor:
- **Preserve stable IDs.** Never renumber existing FR/NFR/M/R/Q IDs; only append. If the doc has no IDs, add them.
- **Preserve intent.** When rewording for precision, keep the author's meaning; if a sentence is so vague its meaning is uncertain, that's a category-3 question, not a rewrite.
- **Deepen, don't pad**: add missing WHEN/THEN scenarios (especially error paths), baselines/targets/guardrails to metrics, edge-case table entries, kill-switch/rollback story, and NFR coverage (or explicit "N/A — reason").
- **Record the change**: bump the version in Document Control and add a changelog row summarizing the revision.
- If restructuring, map old sections → template sections and carry over ALL content; anything that fits nowhere goes to the Appendix, never deleted silently.

### 4. Verify and deliver

- Re-score against the rubric. Target: ≥ 8.0 overall, no dimension below 6, zero CRITICAL triggers. Iterate until met or blocked on category-3 answers.
- Deliver a before/after summary:
  - Scorecard: old → new per dimension
  - List of substantive changes (not formatting noise)
  - Assumptions introduced (all marked `[assumed]` in-doc)
  - Remaining open questions for the author, in priority order
  - Offer `/ultimate-sdd:project` once the PRD is launch-ready — explode it into EPICs + REQs

## Guardrails

- Never delete the author's content without flagging it — move disputed material to the Appendix or an "Under discussion" note.
- Never fabricate data to fill an evidence gap — `[assumed]` + Open Question instead.
- Don't impose the full template on a lightweight doc the team intentionally keeps small — raise it, let them choose.
- Keep a clean separation between your findings (review) and your edits (improvement) so the author can audit both.
