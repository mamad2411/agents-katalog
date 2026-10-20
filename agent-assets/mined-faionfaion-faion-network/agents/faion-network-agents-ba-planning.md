# BA Planning

## Summary

**One-sentence:** Pre-elicitation 6-step framework: select plan-driven/change-driven/hybrid, name stakeholders, schedule elicitation, define deliverables, set governance approver + change process + escalation path.

**One-paragraph:** Pre-elicitation 6-step framework: select plan-driven/change-driven/hybrid, name stakeholders, schedule elicitation, define deliverables, set governance approver + change process + escalation path. Captured as a versioned artefact downstream agents and reviewers consume without re-deriving rationale. Mechanism: typed input → bounded transformation → contract-checked output.

**Ефективно для:**

- Pre-elicitation phase коли scope і governance not yet defined.
- Multi-month engagement initiation.
- Cross-team / cross-vendor projects з multi-stakeholder governance.
- Audit-required engagement (regulated, public sector).

## Applies If (ALL must hold)

- Engagement starts (kickoff already happened).
- Stakeholders are nameable (≥1 sponsor + ≥1 approver).
- Approach choice (plan-driven / change-driven / hybrid) is open.
- Deliverables list expected at end of plan stage.

## Skip If (ANY kills it)

- Engagement in flight where plan already exists — extend, do not duplicate.
- 1-week spike with no governance needs.
- Solo BA with full scope autonomy — overhead exceeds value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Recent task context (30 days) | Markdown / tracker | BA |
| Write access to artefact store | repo / wiki | engagement manager |
| Named downstream owner | stakeholder list | BA |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[ba-onboarding-week-one-template]] | Companion / upstream methodology |
| [[decision-analysis]] | Sibling artefact in the same lifecycle |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + examples | 800 |
| `content/03-failure-modes.xml` | essential | Antipatterns | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Mechanical template fill. |
| `synthesize_decision` | sonnet | Per-instance bounded judgment. |
| `review_for_compliance` | opus | Cross-input synthesis on high-stakes outputs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ba-planning.json` | Skeleton artefact with required fields |
| `templates/_smoke-test.json` | Minimum viable filled artefact |
| `templates/ba-activity-plan.md.j2` | Weekly BA activity plan — daily elicitation activities, actual-vs-planned effort, dependencies, blockers, stakeholder-register diff. |
| `templates/ba-activity-plan.md` | Weekly BA activity plan — daily elicitation activities, actual-vs-planned effort, dependencies, blockers, stakeholder-register diff. Generated from `templates/ba-activity-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/ba-approach-document.md.j2` | BA approach document — analysis approach, stakeholder list, elicitation plan, deliverables, governance, replan triggers. |
| `templates/ba-approach-document.md` | BA approach document — analysis approach, stakeholder list, elicitation plan, deliverables, governance, replan triggers. Generated from `templates/ba-approach-document.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ba-planning.py` | Validate artefact against output-contract | After subagent returns; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ba-onboarding-week-one-template]]
- [[decision-analysis]]
- [[business-process-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. Routes on artefact-state signal to the active rule.
