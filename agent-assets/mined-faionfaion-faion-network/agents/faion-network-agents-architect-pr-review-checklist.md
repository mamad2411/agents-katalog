# Architect PR Review Checklist

## Summary

**One-sentence:** Tier-appropriate PR review checklist for the architectural surface; also serves as the solo dev's self-review checklist for AI-generated code.

**One-paragraph:** Six review sections every architectural PR MUST be checked against: contract, dependency direction, error model, observability, security, and ADR conformance. Caps review at 15 minutes per PR; if violations would take longer, escalate or split. Output is a PR review report referencing the rules from 01-core-rules.xml plus a ship/block verdict.

**Ефективно для:**

- паст-готова основа для повторюваної задачі 'architect PR review' — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф звіту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- PR touches architectural surface (public API, module boundary, ADR-relevant code).
- Reviewer or author wants a structured rubric (especially for AI-generated code).
- Repo has at least one ADR establishing constraints the PR may violate.

## Skip If (ANY kills it)

- PR is a typo/formatting-only change.
- PR is auto-generated dependency bump with no architecture impact.
- PR is a docs-only change to non-architectural docs.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| PR diff | git diff | GitHub PR |
| ADR index for the repo | directory listing | repo ADR folder |
| Module boundary map | dependency graph or doc | architect |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/architecture-decision-records` | Provides the ADRs the PR is checked against. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the review report + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure: classify → 6-section walk → block-or-ship → write report → escalate | ~700 |
| `content/05-examples.xml` | medium | Worked example: a PR review report with block + 3 violations | ~600 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `walk-sections` | sonnet | Per-section rubric check. |
| `draft-review-report` | sonnet | Template-driven report assembly. |
| `cross-pr-trend-audit` | opus | Repeated-violation pattern detection. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pr-review-report.md.j2` | Six-section PR review report with ship/block verdict. |
| `templates/pr-review-report.md` | Six-section PR review report with ship/block verdict. Generated from `templates/pr-review-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-architect-pr-review-checklist.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[architecture-decision-records]]
- [[adr-reversibility-tagging]]
- [[c4-model]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
