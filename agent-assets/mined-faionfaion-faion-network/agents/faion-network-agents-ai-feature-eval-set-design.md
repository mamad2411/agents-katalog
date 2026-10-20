# AI Feature Eval Set Design

## Summary

**One-sentence:** Concrete spec for a shipping AI feature's regression eval set: gold rows, adversarial rows, drift-watch rows, judge selection, versioning, CI wiring.

**One-paragraph:** Most teams ship AI features with a 5-row spreadsheet and call it an eval. The result: every prompt tweak, every model bump, every dependency change is a guess. This methodology specifies a regression eval set fit for a shipping feature: ≥30 gold rows covering the canonical happy paths, ≥10 adversarial rows for known failure modes, ≥5 drift-watch rows that mirror production sampling, a judge (LLM-as-judge with structured rubric OR rule-based matcher), a frozen eval-set version tag, and a CI wiring that gates PRs. Output is a spec.md the team can implement and a row-stats schema the validator enforces.

**Ефективно для:**

- PM/QA інженер, які не ML-фахівці — конкретний шаблон, що robocho скласти за день.
- Команди, які shipплять AI feature і отримують flaky-quality звіти від користувачів — eval ловить регресії.
- Model swap (Sonnet 4.5 → 4.6 / 4.7) — без eval це shot in the dark.
- Prompt-tweak iteration: eval розрізняє покращення від ілюзії.

## Applies If (ALL must hold)

- An AI feature is in production (not a prototype).
- Quality regressions are user-visible (chat, summarization, classification, extraction).
- Engineering owns the prompt or model selection and can wire CI gates.

## Skip If (ANY kills it)

- Single-prompt one-off demo with no ongoing maintenance.
- Pure-deterministic pipeline (no model in the loop).
- Eval coverage already exists with ≥50 gold + ≥10 adversarial rows.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature spec | Markdown | PM / product docs |
| Production traffic log | JSONL (input + output) | trace store / DB |
| Known failure-mode list | Markdown bullet list | support tickets / postmortems |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| none | This methodology is self-contained; no upstream artefact required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: min-row-counts, structured-judge-rubric, frozen-eval-version, drift-watch-from-production, ci-gate-on-regression | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `harvest-cases` | haiku | Mechanical sampling + labeling. |
| `choose-judge` | sonnet | Light judgment between LLM/rule-based. |
| `wire-ci-gate` | haiku | YAML template filling. |

## Templates

| File | Purpose |
|------|---------|
| `templates/eval-spec.md.j2` | Markdown spec template (eval_set_id, version, rows, judge, ci_gate) |
| `templates/eval-spec.md` | Markdown spec template (eval_set_id, version, rows, judge, ci_gate) Generated from `templates/eval-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-feature-eval-set-design.py` | Validate the spec artefact against the schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[trajectory-eval-otel]]
- [[two-pass-reason-then-extract]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, eval scores, stakes, noise ratio, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
