---
name: sdd-architect
description: Use when a consumer wants a whole-codebase architecture opportunity scan—shallow modules, seam friction, or mud-ball concerns—outside the delivery loop. Optional satellite; not delivery review or pre-ship audit.
---

# SDD Architect

## Goal

Surface behavior-preserving architecture deepening opportunities in a conversation without replacing `sdd-review` or entering product implementation.

This is an **opportunity scan**, not greenfield system design and not delivery review of a diff.

## When to Use

Use when the user asks to deepen architecture, reduce mud-ball structure, find shallow modules, or explore seam friction across modules or packages — **before** a behavior spec exists for that work.

Use when `using-sdd` routes here for pre-spec architecture opportunity scanning.

Skip when the task is **delivery review** of a defined diff — use `sdd-review` (defects in this increment, not repo-wide opportunities).

Skip when goals, boundaries, or trade-offs are still unclear — use `sdd-grill`.

Skip when the user only needs a **territory map** (modules, callers, domain vocabulary) without refactor recommendations — use **`sdd-zoom`**.

Skip when the user only needs a behavior contract for a known slice — use `sdd-spec`.

This is an **optional satellite**. It is not part of the mandatory core loop before `sdd-ship`.

## Prerequisites

Read repository guidance, relevant code, and existing SDD artifacts (`docs/sdd/*-spec.md`, `*-plan.md`) when present.

When the consumer repo has optional domain docs, read them before proposing candidates:

- `CONTEXT.md` or linked domain glossary files referenced from repository guidance
- `docs/adr/` for decisions that constrain refactoring

When those files are absent, continue from code and SDD artifacts only. Do not require or create them in this skill.

## Process

1. Explore the codebase for architectural friction: shallow modules, leaky seams, pass-through layers, or poor test surfaces.
2. Apply the **deletion test** to suspected shallow modules: if deleting the module would scatter complexity across callers, it may be earning its keep; if complexity vanishes, it may be pass-through noise.
3. Use **depth** and **seam** language in plain terms:
   - **Depth** — useful behavior behind a small interface.
   - **Shallow** — interface nearly as complex as the implementation.
   - **Seam** — a place behavior can change without editing every caller.
4. Report candidates in the conversation. For each candidate include:
   - affected area (modules, paths, or concepts)
   - problem (why current structure causes friction)
   - proposed deepening direction (plain language, not file-by-file steps)
   - expected leverage or testability benefit
   - recommendation strength: `Strong`, `Worth exploring`, or `Speculative`
5. When no credible candidate exists, say so explicitly instead of inventing churn.
6. When a candidate contradicts an existing ADR, mark the conflict and recommend ADR or spec follow-up rather than overriding the ADR silently.
7. End with one next-step recommendation through **`using-sdd`**. When the user selects a candidate that needs acceptance criteria, state that **`sdd-spec`** is the default next stage unless trade-offs remain open (`sdd-grill`).

Do not write HTML reports, OS temp files, product code, tests, spec, plan, CONTEXT, or ADR in this skill.

## Red Flags

- Treating this skill as mandatory before every ship.
- Duplicating `sdd-review` on a scoped diff.
- Requiring subagents, HTML, or Mermaid deliverables.
- Creating or editing CONTEXT, ADR, spec, plan, or product code.
- Auto-invoking `sdd-spec`, `sdd-grill`, or `sdd-build`.

## Verification

Confirm each candidate names a problem and a deepening direction with a clear recommendation strength, or confirm none were found with evidence from exploration.

## Output

Deliver a conversation report listing candidates (or an explicit none-found statement) and a top recommendation when multiple candidates exist.

Default durable artifact: **none**. Do not require an architect report file on disk.

## Stop Conditions

Stop after the conversation deliverable and one routing recommendation.

Recommend **`using-sdd`** only; do not invoke the next skill automatically.

When the user picks a candidate that needs a behavior contract, note that **`sdd-spec`** is the usual next stage after routing.
