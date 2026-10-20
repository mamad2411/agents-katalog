# Acceptance Criteria

## Summary

**One-sentence:** Produces stable, testable acceptance criteria (Given/When/Then or rule-based) with cross-reference IDs (AC-FEATURE-NN) tying spec, test-plan, and CI report.

**One-paragraph:** Produces stable, testable acceptance criteria (Given/When/Then or rule-based) with cross-reference IDs (AC-FEATURE-NN) tying spec, test-plan, and CI report. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- SDD spec.md authoring перед coding subagent'ом — AC треба stable + testable.
- Freeform user story → testable criteria translation.
- Regression scenarios from bug reports — definition-of-done gate перед merge.
- Story-slicing signal: AC count > 7 — час ділити.
- Gherkin → Cucumber/Behave/Playwright wiring, де BA review і CI ділять один артефакт.

## Applies If (ALL must hold)

- Authoring AC for SDD spec.md files before a coding subagent picks up the task.
- Translating a freeform user story or stakeholder note into testable criteria.
- Generating regression scenarios from a bug report so the fix has a definition-of-done gate before merge.
- Splitting an oversized story: when AC count exceeds 7 per story, that is the slicing signal.
- Wiring AC to executable specs (Gherkin to Cucumber / Behave / Playwright) so BA review and CI share one artefact.

## Skip If (ANY kills it)

- Pure spike / research tasks where the outcome is a learning, not a behaviour.
- Throwaway prototypes or demos with a lifespan under one sprint.
- UX-only changes where verification is subjective (visual polish, brand tone).
- Operational runbook changes (server tweaks, cron edits) — use smoke checks instead.
- Negotiation-heavy external contracts where AC ossify before scope is stable.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| User story / requirement | Markdown / Jira / spec.md | BA / PM |
| Domain glossary | Markdown | BA team |
| Test framework decision (Cucumber / Behave / Playwright / Jest) | ADR | engineering |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[requirements-documentation]] | requirements feed AC authoring |
| [[requirements-traceability]] | AC IDs feed RTM |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology guard | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → conclusion refs to rule ids | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-ac-shape` | haiku | Pick BDD (Gherkin) vs rule-based. |
| `author-ac` | sonnet | Write testable AC with stable IDs. |
| `review-ac-quality` | sonnet | Audit independence + atomicity + testability. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ac-bdd.md.j2` | Given/When/Then BDD template with stable AC ID. |
| `templates/ac-bdd.md` | Given/When/Then BDD template with stable AC ID. Generated from `templates/ac-bdd.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/ac-rule-based.md.j2` | Rule-based AC template for system constraints. |
| `templates/ac-rule-based.md` | Rule-based AC template for system constraints. Generated from `templates/ac-rule-based.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/prompt-authoring.xml` | LLM prompt for AC authoring. |
| `templates/prompt-verification.xml` | LLM prompt for AC quality review. |
| `templates/ac-coverage.sh` | Shell helper computing AC coverage across stories. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[requirements-documentation]]
- [[requirements-traceability]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
