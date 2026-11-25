---
name: prd-review
description: Review and score a PRD against a 10-dimension rubric with CRITICAL/WARNING/SUGGESTION findings and concrete fixes. Use when the user wants a PRD critiqued, reviewed, scored, or checked for readiness before engineering handoff.
license: MIT
metadata:
  author: andrewr303
  version: "1.0"
---

Review a PRD like a rigorous, kind staff-level reviewer: score it, find what will actually hurt during build and launch, and give concrete fixes — without rewriting the document (that's `prd-improve`).

**Supporting files** (under `templates/` at the plugin root):
- `templates/review-rubric.md` — dimensions, weights, CRITICAL triggers, report format

**Input**: Path to a PRD (or pasted content). If missing, search for candidates and ask the user to confirm.

## Steps

### 1. Read adversarially

- Read the PRD from disk and `templates/review-rubric.md`.
- First pass: understand what's being proposed. Second pass: **try to break it** — your job for this pass is to make the PRD fail:
  - Simulate the engineer: pick 3 requirements and ask "could two reasonable engineers build different things from this?" If yes → CRITICAL ambiguity.
  - Simulate launch day: walk the rollout plan; what's unaccounted for?
  - Simulate 6 months later: which quiet, costly, late-detected failure does this PRD not defend against?
- Check every automatic CRITICAL trigger from the rubric.
- Scan normative text for the ambiguity word list; each occurrence is a finding.
- Build the traceability map (goals ↔ metrics ↔ requirements ↔ non-goals); orphans and contradictions are findings.
- If a codebase is present, sanity-check technical claims (§8) and feasibility against reality — a PRD requiring capabilities the architecture can't offer is a CRITICAL finding.

### 2. Score

Score all 10 rubric dimensions with one-line justifications. Compute the weighted overall. Verdict thresholds: **Launch-ready** ≥ 8.0 with no dimension < 6 and zero CRITICALs; **Needs revision** ≥ 5.5; else **Needs rework**.

### 3. Report

Use the exact report format from the rubric. Rules:
- Every finding cites a section (§) and includes a **concrete fix** — for ambiguities, write the corrected sentence; for gaps, name the missing content. "Consider clarifying" is banned.
- Order findings by severity, then by cost-of-being-wrong (quiet/costly/late first).
- Include the "What's strong" section — 2–4 genuine strengths.
- Cap SUGGESTIONs at ~10; a review drowning in nitpicks buries the CRITICALs.

### 4. Offer follow-up

End with: "Want me to apply these fixes (`/prd:improve`), or re-review after your edits?"

## Guardrails

- **Review only — do not edit the PRD.** Not even typo fixes.
- Judge the document, not the idea. If you doubt the product strategy, put ONE clearly-labeled "Strategy note" at the end — findings stay about PRD quality.
- Don't punish intentional brevity twice: if a team keeps a lightweight format, score honestly but note which gaps are conventions vs. defects.
- When uncertain about severity, prefer the lower: SUGGESTION over WARNING, WARNING over CRITICAL. False alarms erode trust.
- If the document is not a PRD at all (design doc, tech spec), say so and point to the right skill rather than force-scoring it.
