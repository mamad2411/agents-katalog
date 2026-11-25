---
name: i2r-gsd-projection-mode
description: Markdown out/-package projection — documents the shape i2r_render.py / i2r.py assemble emits for the full out/ Markdown package
when_to_use: Preloaded into i2r-orchestrator (assemble step) and i2r-completeness-critic (Reader Test Gate check); describes the complete out/ package shape the assemble script deterministically emits
user-invocable: false
---

# i2r-gsd-projection-mode

Owned by: `i2r.py assemble` + `i2r_render.py` ($0, no LLM). Consumed by: `i2r-orchestrator`
(assemble step), `i2r-completeness-critic` (Reader Test Gate — CONTRACT §11).

Output: the complete `out/` Markdown package (all 11 documents + `decisions/ADR-*.md`).
Internal machine artifacts (`internal/requirements.json`, `internal/traceability-matrix.json`, etc.)
are deterministic projections of the stage JSONs — they are NOT primary reading artifacts.

## What this mode documents

This mode is the authoritative shape reference for everything `i2r.py assemble` writes under `out/`.
`i2r_render.py` is a pure function: it takes already-loaded stage data + `lang` and returns
`{filename: content}` strings. `i2r.py` owns file I/O. The Markdown rendering is independently
testable and < 800 lines.

## The out/ package — reading layer

| File | Primary reader | What it conveys |
|---|---|---|
| `out/README.md` | Humans + downstream AI (entry point) | Status, reading order, what the package is, what it does NOT do |
| `out/PRD.md` | Product/engineering teams + downstream AI | Executive Summary, structured Goals, Non-Goals, Scope, Actors/JTBD, Requirements overview, links to sibling docs |
| `out/REQUIREMENTS.md` | Engineers, PMs, QA | Narrative per-requirement sections — FR + NFR detail |
| `out/ACCEPTANCE.md` | QA, PMs, stakeholders | Per-scenario Gherkin + plain-language explanation + observable evidence |
| `out/DECISIONS.md` | All readers | Locked decisions overview + ADR index |
| `out/CONSTRAINTS.md` | All readers | Hard limits — product / quality / decision |
| `out/GLOSSARY.md` | All readers | Terms, ambiguity resolutions |
| `out/QUESTIONS.md` | Lead + stakeholders | Open questions + carried-forward assumptions |
| `out/READINESS.md` | Lead + team | Human-readable gate verdict (written by `gate.check`) |
| `out/TRACEABILITY.md` | Lead + QA | Source→requirement→acceptance trace for humans |
| `out/CHANGELOG.md` | All readers | Per-run change notes |
| `out/decisions/ADR-*.md` | Architecture / team | One locked decision per file |

The same `out/` Markdown is read by **humans AND downstream AI orchestration**. There is no separate
GSD-specific instruction artifact. Downstream reads what humans read.

## Hard rules

- `out/` is **Markdown-only**. No `.json` or `.yaml` in `out/`. Any JSON/YAML in `out/` → gate
  BLOCKER (`out_markdown_only`, CONTRACT §8).
- **MUST NOT emit downstream orchestration commands** (`/gsd:*`, `plan-phase`, `ingest-docs`,
  `next_command_hint`, `consumer_contract_version`, `handoff.gsd.json`). Any such string in any
  `out/*.md` → gate BLOCKER (`DOWNSTREAM_COMMAND_LEAK`, CONTRACT §7 + §8).
- `PRD.md` MUST begin with `## Executive Summary`. Missing → gate MAJOR (`prd_has_executive_summary`).
- `REQUIREMENTS.md` must have per-requirement narrative sections, not just a table dump →
  gate MAJOR (`requirements_are_narrative`).
- Every Gherkin block in `ACCEPTANCE.md` must be followed by a plain-language explanation →
  gate MAJOR (`acceptance_has_plain_language`).
- `READINESS.md`, `TRACEABILITY.md`, `CONSTRAINTS.md`, `QUESTIONS.md` must be present and non-empty
  → gate BLOCKER if missing.
- WHAT/WHY only — NEVER HOW. Stack-swap test (CONTRACT §1): if swapping DB/framework forces a
  PRD.md edit → HOW leaked → fix before assemble.
- No phases, roadmap, sprints, tasks, architecture, API routes, UI components, database schemas,
  file structures.
- `[CAT]-NN` IDs in `PRD.md` must match FR IDs from `04-functional.json` exactly.
- `NFR-ISOCAT-NN` IDs must match `05-nfr.json` exactly.
- Locked decisions come from `raw/` or a recorded human decision — never fabricated.
- Reader Test Gate (CONTRACT §11): a fresh critic receives ONLY the `out/` package, must infer
  goals / scope boundary / constraints / acceptance / readiness / no HOW leakage. Fail →
  `READER_TEST_FAIL` → BLOCKED.

## Paths (runtime, under the active run)

```
.i2r/runs/<slug>/<run-id>/
  out/                    ← this mode's output domain
    README.md
    PRD.md
    REQUIREMENTS.md
    ACCEPTANCE.md
    DECISIONS.md
    CONSTRAINTS.md
    GLOSSARY.md
    QUESTIONS.md
    READINESS.md          ← written by gate.check, not assemble
    TRACEABILITY.md
    CHANGELOG.md
    decisions/ADR-*.md
  internal/stages/        ← source stage JSONs (input to assemble)
    01-intake.json  02-context.json  03-scope.json
    04-functional.json  05-nfr.json  06-acceptance.json  …
  audit/
    gate-result.yaml      ← machine gate verdict
    gate-result.md        ← human-readable gate explanation
```

## References (depth lives here)

- `references/prd-shape.md` — full out/ package shape (all 11 docs + ADR; authoritative)
- `references/gsd-handoff-rules.md` — output package rules; what I2R must NOT emit
- `references/PRD_TEMPLATE.md` — empty PRD.md skeleton (new shape with Executive Summary)
- `references/GOOD_PRD.md` — correct new-shape example
- `references/BAD_PRD.md` — PRD that leaks HOW + emits downstream commands + fails Reader Test

Sources: CONTRACT.md §1 §8 §11 §18 §20; `i2r_render.py` render_prd(); Anthropic doc-coauthoring
(Reader Test); PM Skills templates; product-on-purpose anchoring.

## Minimal execution flow (assemble step)

```
1. Confirm all required stage JSONs are schema-valid (i2r.py validate --stage all)
2. i2r.py assemble reads: 01-intake, 02-context, 02b-evidence, 03-scope, 03b-scope-debate,
   04-functional, 05-nfr, 06-acceptance, (07-review for DECISIONS/QUESTIONS)
3. i2r_render.py renders each out/ Markdown file (pure, no LLM, zh/en i18n)
4. i2r.py writes out/ files; if ADR projection ON: writes decisions/ADR-*.md
5. i2r.py also writes internal/requirements.json, internal/traceability-matrix.json,
   internal/claim-ledger.json, internal/quality-report.json (machine artifacts, NOT reading layer)
6. i2r.py gate.check → audit/gate-result.yaml + audit/gate-result.md + out/READINESS.md
7. Reader Test Gate: completeness-critic receives ONLY the out/ package — must independently
   infer goals / scope / constraints / acceptance / readiness / no HOW (CONTRACT §11)
8. gate.check records reader_test result; FAIL → BLOCKED
```
