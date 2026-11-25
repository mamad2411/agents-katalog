---
name: prd-new
description: Create an extremely in-depth PRD from scratch through structured discovery. Use when the user wants to write a new PRD, product spec, or requirements document for a feature or product idea.
license: MIT
metadata:
  author: andrewr303
  version: "2.0"
---

Create a complete, in-depth PRD from an idea — through structured discovery, not a form-filling exercise.

**Supporting files** (in this skill's directory unless installed as a plugin, in which case under `templates/` at the plugin root):
- `templates/prd-template.md` — the PRD structure to produce
- `templates/question-bank.md` — discovery questions by wave
- `templates/review-rubric.md` — quality bar the final PRD must meet

**Input**: An idea, feature description, or problem statement. May be one sentence or a full brief.

## Steps

### 1. Establish context

- Read `templates/prd-template.md` and `templates/question-bank.md`.
- If working inside a codebase, spend a few minutes grounding yourself: what product is this, what patterns exist, does anything similar already exist? Reference reality, don't theorize.
- Ask where the PRD should be written. Default: `docs/prd/<kebab-case-name>.md` (create the directory if needed). Derive the kebab-case name from the idea.

### 2. Discovery — interview in waves

Use the question bank. Rules:
- Ask **3–5 questions per wave**, via the AskUserQuestion tool where available — one focused question at a time, with preset options when answers are predictable.
- Skip questions already answered by the user's brief or the codebase. Never ask what you can find out yourself.
- After each wave, decide: do remaining unknowns still change the PRD materially? If not, stop asking.
- Wave 1 (problem/evidence/metrics) is **mandatory** — never skip it.
- If the user says "just draft it" or is unavailable: proceed, but make every guess explicit — mark it `[assumed]` in the Evidence section and add an entry to Open Questions.

Run a **pre-mortem** before drafting: "It's 6 months post-launch and this failed — why?" Feed the answers into Risks.

### 3. Draft the PRD

Write the full document following `templates/prd-template.md`. Non-negotiables:

- **Every section present.** Use "N/A — <reason>" rather than deleting Security, Privacy, Rollout, or Risks.
- **Requirements**: SHALL/MUST language, stable IDs (FR-1, NFR-1, ...), priority tags (P0/P1/P2), every FR has ≥1 WHEN/THEN scenario **including at least one error/edge scenario** for P0s.
- **Metrics**: at least one primary + one guardrail, each with baseline (or an instrumentation task), target, timeframe, and source.
- **Traceability**: every goal maps to ≥1 metric; every metric maps to a goal; non-goals contradict nothing in scope.
- **Label evidence** as [verified] / [inferred] / [assumed].
- **No ambiguity words** in normative text (see the rubric's word list). Replace "fast" with a number, "handle gracefully" with the actual behavior.
- Delete all template comments from the final output.

### 4. Self-review before presenting

Score your draft against `templates/review-rubric.md`. Time-box an attempt to break it: check every automatic CRITICAL trigger. Fix everything CRITICAL and any dimension below 6 **before** showing the user. Do not present the scorecard unless asked — present a PRD you already stand behind.

### 5. Deliver

Summarize for the user:
- File path and one-paragraph gist
- The 3–5 most consequential decisions made and assumptions taken
- Open questions that need their input, in priority order
- Offer next steps: "Want me to refine any section, run a formal review (`/ultimate-sdd:review`), or explode this PRD into EPICs + REQs (`/ultimate-sdd:project`)?"

## Guardrails

- Never invent evidence, metrics baselines, or user research. Unknown data is `[assumed]` + Open Question, not fabricated numbers.
- Never write implementation-level detail (class names, library choices) into requirements — behavior contracts only. Technical constraints go in §8.
- If the idea is actually multiple products/features, say so and propose splitting before writing one bloated PRD.
- If a PRD for this already exists, stop and suggest `prd-improve` instead.
- Depth is the point, but padding is not: every sentence must inform a decision someone will make. Cut boilerplate that doesn't.
