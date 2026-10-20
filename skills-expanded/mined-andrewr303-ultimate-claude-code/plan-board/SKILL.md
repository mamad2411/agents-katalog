---
name: plan-board
description: >
  Show the Plan / Build / Published board and the SPEC tree — readiness
  label, effort, blockers, selected acceptance criteria, ready-count.
  Use when the user asks for status, the board, the spec tree, what's
  next, or runs /ultimate-sdd:board.
license: MIT
metadata:
  author: andrewr303
  version: "2.1"
---

Render the plan as a tree and a board.

**Supporting files:** `references/model.md`, `references/readiness.md`, `templates/index-template.md`, `scripts/plan.py`.

```
python <plugin>/scripts/plan.py board --root docs/plan --write
python <plugin>/scripts/plan.py status --root docs/plan --json
python <plugin>/scripts/plan.py next --root docs/plan --json
```

Prefer the script's Next over a remembered one.

## Steps

1. Read every artifact under the plan root, including `context/CATALOG.md`.
2. Derive labels from readiness (1–2 rough, 3 shaping, 4–5 ready).
3. Rebuild INDEX: spec tree, Plan / Build / Published, active Changes, Next, ready-count (`k of n` REQs with label ready and not cancelled).
4. Run `validate_plan.py`.

## Output

**Context sidebar** — CATALOG grouped Company / Project / Plan.

**Spec tree** (Plansmith):

```
SPEC-1  <epic>                               shaping · high
  SPEC-2  REQ-1 · <title>                    ready   · low
  SPEC-3  REQ-2 · <title>                    ready   · med
    SPEC-4  REQ-3 · <title>                  rough   · low    needs first: SPEC-3
```

Indent children by `blocked_by`. Show `k of n specs Ready`.

**Selected spec** — if the user named a SPEC/REQ, print its AC checklist under the tree (unchecked until verify).

**Changes** — active CHANGE-n rows (slug, status, domains, linked REQs). Archived changes stay out of the active table.

**Board columns** — Plan / Build / Published as before. Tabs: Plan is default; Prototype is only listed if a prototype artifact exists (do not invent one).

**Next** — one imperative sentence + command.

## Mutations

Status moves need evidence. Keep blockers mutual. After a conversation answer that changes a SPEC, rewrite the tree and re-score that REQ in the same turn.

## Guardrails

- Board is derived. Do not specify or implement here.
- SPEC is an alias. Canonical ID stays REQ/EPIC. CHANGE-n is packaging, not a SPEC.
