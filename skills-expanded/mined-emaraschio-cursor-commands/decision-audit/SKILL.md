---
name: decision-audit
description: >-
  Post-build decision ledger and pride gate: list meaningful agent choices and
  assumptions after work has landed, with why, alternatives, and confidence;
  flag debt and edge cases; do not change code until the user says revise now.
  Use when the user invokes /decision-audit or asks for a post-execution
  decision audit or choice autopsy.
disable-model-invocation: true
user-invocable: false
---
# Decision audit

## Role

You produce a **post-execution decision ledger** for work already completed in scope. You surface meaningful choices and assumptions the agent made, not a line-by-line code review. You end with a **pride gate** and a **halt**: do not change code, commit, or open a PR in the same turn. Ledger approval is not revise permission; wait for **revise now** (with targets).

## When to use

Use when the user invokes `/decision-audit`, asks for a decision audit, choice ledger, or pride gate after a build, or wants a judgment autopsy of what the agent chose. For productivity and value accounting, use `agent-work-receipt`. For diff quality before approve, use `code-review` or `light-review-existing-diffs`. For pre-build assumption surfacing, use `blind-spot-pass` or `define-agent-goal`.

## Audit charter

> Audit judgment after the agent has already chosen. List meaningful decisions only. Do not invent choices without evidence. Do not change code until revise now.

## Workflow

Run phases in order. Do not publish the ledger until evidence is gathered. Do not revise code in this turn.

### Phase 0: Intake

1. Parse a **scope hint** from the user message (e.g. "decision audit for the auth refactor on branch-1").
2. If no scope hint, default to the **full session** or **current branch** when a repo is present.
3. If the user invokes mid-task with **no finished work** yet, say so and **stop or ask whether to wait**. Do not hallucinate a ledger of completed decisions.

### Phase 1: Evidence

Gather read-only evidence:

- **Conversation**: what the user asked for, what the agent chose, what was rejected or deferred
- **Git** (when a repo is present): `git status`, `git diff`, `git log` to ground landed choices
- **Files**: only artifacts in scope that still reflect the chosen design

Do not invent decisions that have no support in conversation or diff. Prefer "none recorded" for alternatives when the session never considered them.

### Phase 2: Ledger

List **meaningful** choices only. Include architecture, API shape, library picks, error-handling strategy, naming that locks an API, skipped tests, deferred work, and similar judgment calls. Skip trivial formatting noise and mechanical renames unless they lock a public contract.

For each choice, populate:

| Field | Content |
|-------|---------|
| Decision | What was chosen |
| Why | Short rationale grounded in evidence |
| Alternatives | What else was considered, or **none recorded** |
| Confidence | **high** / **med** / **low** |
| Locality | **example-local** (fits this case only) or **generalizable** |

Keep the ledger short enough to review. Prefer fewer high-leverage rows over a dump of every micro-choice.

### Phase 3: Debt and edges

From the same evidence, list:

- **Known debt** tied to the choices (TODOs left in, shortcuts, missing tests)
- **Unhandled edge cases** the choices imply
- **Blast notes** (what else might break or need follow-up if these choices stand)

Do not invent facts. If nothing is known, say so explicitly.

### Phase 4: Pride gate

Ask the human two explicit yes/no questions. Do not soft-sell ship readiness:

1. Are you **proud** of this branch (or scoped work)?
2. Would you **stand behind it in production** as it is?

Record that answers are for the human; do not answer for them.

### Phase 5: Halt

End with this handshake (adapt wording only if needed; keep the meaning):

> Approve or edit this ledger before I revise. Ledger approval is not revise permission. Say **revise now** (with targets) to change code.

Do not start edits, commits, destructive git, or PR creation in this turn. If the user says "just fix it" without **revise now**, stay on the audit contract and remind them of the halt phrase.

## Deliverable template

```markdown
# Decision audit

## 1. Decision ledger

| Decision | Why | Alternatives | Confidence | Locality |
|----------|-----|--------------|------------|----------|
| ... | ... | none recorded / ... | high/med/low | example-local / generalizable |

## 2. Debt and edge cases

- Known debt: ...
- Unhandled edges: ...
- Blast notes: ...

## 3. Pride gate

1. Proud of this branch / scoped work? (yes/no for the human)
2. Stand behind it in production as it is? (yes/no for the human)

## 4. Halt

Approve or edit this ledger before I revise. Ledger approval is not revise permission. Say **revise now** (with targets) to change code.
```

Populate every section. Prefer a compact table or short bullets over vague prose.

## Safety

- Audit only: no new implementation, commits, PR creation, or destructive commands unless the user explicitly says **revise now** (with targets) in a follow-up that authorizes changes.
- No secrets, tokens, PII, or PHI in the ledger body; redact if present in context.
- Do not invent decisions or debt without evidence.

## Distinction from other commands

- **`agent-work-receipt`**: productivity, time estimates, and value tiers after a session. This skill audits **judgment** (choices, confidence, pride gate), not output accounting.
- **`code-review`** / **`light-review-existing-diffs`**: diff quality and approve/reject signals. This skill is a **choice autopsy**, not a line-by-line review.
- **`blind-spot-pass`**: pre-build four-quadrant fog map of the ask. This skill runs **after** execution.
- **`define-agent-goal`**: forward six-part Goal before autonomous work. This skill is **backward** decision review after work.

## Guardrails

- **Ledger of choices, not a line-by-line review.** List meaningful choices (architecture, API shape, libraries, deferred work) with why, alternatives, and confidence.
- **Stay audit-only until revise now.** Deliver the audit and wait for an explicit **revise now** (with targets).
- **Ground decisions in evidence.** Cite session or git evidence, or mark confidence low / none recorded.
- **Always ask the pride gate.** Ask whether the human is proud of the branch and would stand behind it in production.
- **Stop when nothing has landed.** State nothing finished, stop or ask whether to wait; do not hallucinate a ledger.
