---
name: retrofit
description: "Bring an existing project up to the retainer kit with a phased WPS/mypy ratchet when a strict gate yields a flood of violations. Deferred items go into the RATCHET journal. Trigger words (RU+EN): ретрофит, вал нарушений, ратчет, подключить к коробке / retrofit, flood of violations, ratchet, adopt into the kit."
disable-model-invocation: true
---

# Retrofitting an existing project

A new project gets full strictness out of the box for free (`retainer new`, ADR-0002). But EXISTING
code, written without WPS/mypy strict, yields **hundreds** of violations — "fix it all at once" is
unrealistic and unnecessary. This is the case ADR-0002 keeps a fallback for: **a ratchet for a large
retrofit**. retainer runs INSIDE the project (its agents/gate/guard work with the project context
natively), not from the engine's own repository.

## Step 0 — measure the blast radius (read-only)

```bash
bin/blast-radius.sh [code-directories]        # RETAINER_LINT_VENV=path, if strict tools are absent
```
Gives numbers by the strict box (ruff / format / WPS / mypy) and a WPS breakdown by category.
- **Few (≤ ~40)** → fix at once, turn the full box on immediately. Beyond that not by this skill.
- **A flood** → ratchet by phases (below). `ruff` is usually **0** and format is pennies: adopt
  immediately.

## Step 1 — adopt the cheap NOW (full strictness where there is no debt)

`ruff` (a wide select) · `ruff format` · `codespell` · `import-linter` (a contract skeleton) ·
`pytest`+coverage · the `[rigor]` regulators · git hooks · CI · the `scripts/gate.sh` structure.
Usually passes on the first format fix. ⛔ `gate.sh`/`pyproject.toml`/`.retainer/**` are under the
guard — the owner applies them by a key in the terminal.

## Step 2 — WPS by phases, by category

`setup.cfg` enables WPS not wholesale but by an explicit list of the current phase's codes. The
order is **bugs/complexity first, style later**:

| Phase | WPS categories | Why in this order |
|---|---|---|
| 1 | **WPS4xx practices** (bug smells: a mutable constant, a `for` leak, an implicit `.get`…) + **WPS2xx complexity** (Jones/cognitive/a long try) | they catch real defects and over-complexity |
| 2 | **WPS3xx consistency** | dangerous inconsistencies |
| 3 | **WPS1xx names** + the remaining style | cosmetics last |

Each phase: add its codes to `extend-select`, fix the violations, **a green gate**, a commit, the
next phase. Do not open a new phase until the current one is closed.

**Some codes are a PERMANENT ratchet, not a "fix".** Example: `WPS421` (print) in a CLI collector —
print is appropriate; keep it in `extend-ignore` forever with a rationale, not rewrite it to
logging. The decision "fix vs ignore forever" is by the code, with the owner.

## Step 3 — mypy gradually

mypy strict is monolithic and falls on annotations (`no-untyped-def`, `type-arg`). Phases:
1. First the **real type bugs** without the strict annotation flags: `[assignment]`/`[arg-type]`/
   `[no-any-return]` (turn on the base checks, not `disallow_untyped_defs`).
2. Then the annotations — per module (per-module `disallow_untyped_defs`) or by directories.

## Step 3.5 — distill practices FROM the code

The distill procedure — how `<project>/.retainer/practices.md` is filled from the code, and in what
form — lives in [[task-cycle]] (the practices paragraph of the plan step), where practices are read on
every code task and the skill is not held behind `disable-model-invocation`. Retrofit only names the
trigger: a flood on legacy is the moment to distill the whole layer at once. The record form itself is
held by the `practices_form` gate step, not by this prose.

## Step 4 — the RATCHET journal (in `tooling.md`)

Each deferred phase/code is a LINE in the debt journal: what is deferred, why, the lift condition.
The journal **shrinks** as phases close. The gate is green at every stage, but new debt does not
pass: the active phase's WPS codes are already strict, and a new file must be clean by the enabled
categories.

## The invariant

Retrofit is the only place where a project is temporarily BELOW the new-project baseline (a
deliberate debt recorded in RATCHET). New projects are still full-strict from scratch. The ratchet is
up only: a phase's code, once enabled, is not turned back off without a line in the journal and the
owner's key.

## When NOT to apply

A new project — NOT here: it is full-strict out of the box (`retainer new`, ADR-0002), a ratchet is
unneeded and harmful. An existing one with FEW violations (≤~40) — fix at once, also not a phased
ratchet. retrofit is only "a flood on legacy".

Related: [[gate]], [[task-cycle]] (RATCHET/DoD), ADR-0002 (the large-retrofit fallback).
