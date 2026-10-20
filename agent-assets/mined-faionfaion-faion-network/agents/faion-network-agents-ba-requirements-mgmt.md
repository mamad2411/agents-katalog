# BA Requirements Management

## Summary

**One-sentence:** Produces a requirements-management register (change-control, traceability, approval thresholds) governing how requirements evolve through the SDLC.

**One-paragraph:** Produces a requirements-management register (change-control, traceability, approval thresholds) governing how requirements evolve through the SDLC. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- Команда має requirements baselined у Jira/Confluence та потребує chain-of-custody при змінах.
- Compliance audit (ISO 27001, SOC2, медичні стандарти) вимагає traceability з підписами.
- Cross-team initiative (≥3 squads), де зміни requirement розходяться у дизайн, код, тести.
- Тендерний/контрактний проект із чітко зафіксованим scope і CR-driven evolution.

## Applies If (ALL must hold)

- A backlog or requirements set exists and needs governed evolution (change-requests, approval routing, traceability) across releases.
- Multiple stakeholders submit changes that must be batched, scored, and approved before refinement.
- Audit or compliance requires versioned requirement history with timestamps and approvers.
- Cross-team initiative where requirement changes ripple into design, code, and test artefacts.

## Skip If (ANY kills it)

- Solo dev with no external stakeholders — change-control overhead exceeds the change rate.
- Throwaway prototype where requirements are discarded weekly.
- Continuous-discovery product where change-requests are not gated.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing requirements baseline | Jira / Confluence / GitHub Issues | BA team |
| Stakeholder list with approvers | Markdown / CSV | T2 of ba-planning |
| Change-request template | Markdown / form | PMO |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[ba-planning]] | T3 governance defines who approves changes |
| [[requirements-traceability]] | downstream consumer of the CR audit trail |

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
| `classify-change-request` | haiku | Mechanical categorisation: scope / clarification / defect. |
| `score-impact` | sonnet | Cross-reference downstream artefacts; estimate effort and risk. |
| `approve-or-reject` | opus | Final judgement under conflicting stakeholder pressure. |

## Templates

| File | Purpose |
|------|---------|
| `templates/change-request.md.j2` | CR form skeleton with classification, impact, approval. |
| `templates/change-request.md` | CR form skeleton with classification, impact, approval. Generated from `templates/change-request.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/requirements-register.md.j2` | Master register linking each requirement to its CR history. |
| `templates/requirements-register.md` | Master register linking each requirement to its CR history. Generated from `templates/requirements-register.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ba-requirements-mgmt.py` | Validate the artefact JSON against the output contract schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ba-planning]]
- [[requirements-traceability]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
