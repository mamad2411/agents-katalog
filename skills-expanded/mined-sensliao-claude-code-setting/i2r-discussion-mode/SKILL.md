---
name: i2r-discussion-mode
description: Enforces blocking-only clarification discipline — the root orchestrator asks the user only questions whose answers would materially change FR/NFR/scope. Internal I2R authoring mode.
when_to_use: When `i2r-orchestrator` is deciding whether to pause a run and surface questions to the user, specifically at Checkpoint A (post-intake) and Checkpoint B (post-scope). Subagents never invoke this mode directly; all user-facing questions route through the orchestrator.
user-invocable: false
---

# i2r-discussion-mode

## Purpose

I2R produces requirements, not conversations. This mode enforces the discipline that separates questions that **must** be asked (blocking — the answer materially changes the output) from questions that **must not** be asked (non-blocking — the agent proceeds with a documented assumption instead).

Sources: Anthropic doc-coauthoring (context gathering discipline); Spec Kit clarify pattern.

**Vendor-not-install:** implemented as I2R-local rules; no runtime calls to external skills.

---

## The blocking test (single rule)

> **A question is blocking if and only if: missing the answer would cause the agent to write a materially different set of FRs, NFRs, or scope boundaries.**

Everything else is non-blocking. Non-blocking unknowns are resolved with an explicit `assumed[]` entry — never surfaced to the user.

Full policy and examples: `references/blocking-question-policy.md`.

---

## The two checkpoints

### Checkpoint A — after `01-intake.json` is written

Trigger: `i2r-orchestrator` reads `01-intake.json` and checks `open_questions[]`.

**Ask if:** any open question has `requires_discussion: "blocking"` (set by elicitation-mode when importance:high + evidence:low).

**Typical blocking signals at A:**
- Actor identity ambiguity: "users" not broken into a specific actor list (different actors → different auth/permission FRs)
- Outcome ambiguity: the core job-to-be-done is unclear enough that two plausible readings produce different requirement sets
- Hard constraint missing: a constraint that would fence the entire scope is absent and cannot be assumed with medium+ evidence

**Do NOT ask at A:** feature wish-list questions, aesthetic preferences, technology choices, non-core edge cases.

### Checkpoint B — after `03-scope.json` is written

Trigger: `i2r-orchestrator` reads `03-scope.json` and checks `requires_discussion` signals.

**Ask if:** any `in_scope` or `out_of_scope` item carries `requires_discussion: "blocking"` due to an unresolved boundary that risks `SCOPE_LEAK` or `CONFLICT` downstream.

**Typical blocking signals at B:**
- In/out boundary is contested (scope-debate mode may already have flagged this)
- A "deferred" item is blocking because its absence changes whether a `MUST` FR is achievable
- Contradictory constraints were found between `01-intake.json` and `03-scope.json`

**Do NOT ask at B:** clarifications already resolved at A, nice-to-have scope items, implementation choices.

---

## Question format rules

See `references/clarification-patterns.md` for reader-oriented question templates.

Quick rules:
1. **One question per blocking issue** — do not batch unrelated questions into one ask.
2. **State the decision impact** — the question must name what changes if the answer goes one way vs the other.
3. **Offer a default** — if the agent has a reasonable assumption, state it: "I'll assume X unless you tell me otherwise."
4. **Never chit-chat** — no "Just to make sure I understand..." preambles. No validation-seeking. State the question, state the impact, offer the default.

---

## Subagent rule (hard)

**Subagents (`i2r-intake-clarifier`, `i2r-context-analyst`, etc.) NEVER ask the user directly.**

They surface blocking signals via:
- `open_questions[]` in their stage output (with `requires_discussion: "blocking"`)
- `assumed[]` entries with `risk: high`

The **root orchestrator** reads these and decides at Checkpoint A or B whether to pause and ask. This ensures the user sees exactly one consolidated ask per checkpoint, not fragmented questions from multiple agents.

---

## What this mode does NOT do

- Does not author requirements or scope (those are downstream stages).
- Does not resolve scope debates (that is `i2r-scope-mode` + debate mode).
- Does not manage the full run flow (that is `i2r-orchestrator`).
- Never produces chit-chat, check-ins, or "just confirming" questions.
