# Trunk-Based Challenges & Diagnostics

## Summary

**One-sentence:** Produces a diagnostic report when trunk breaks repeatedly, applying an ordered checklist (gates → CI speed → flags → PR size → review SLA) and recommending the first failing fix before touching downstream symptoms.

**One-paragraph:** Broken trunk is never caused by trunk-based development itself — it is caused by missing gates. This methodology produces a structured report given a frequency of trunk breaks. It applies an ordered checklist: (1) Are all merges gated by passing CI? (2) Is CI under 10 minutes? (3) Are incomplete features behind flags? (4) Are PRs under 200 lines? (5) Is review SLA under 4 hours? The first failing check is the fix priority; downstream symptoms are not addressed until the upstream gate is in place. The report names the broken practice, not the practice of trunk-based itself.

**Ефективно для:**

- Trunk breaks more than once per week and the team is considering abandoning trunk-based development.
- Code review is the bottleneck; PRs sit for days.
- CI takes longer than 10 minutes and developers are batching pushes.
- Long-lived branches are creeping back in with 'this feature is too big' justifications.

## Applies If (ALL must hold)

- Team has adopted trunk-based development and is now experiencing pain.
- Trunk has broken more than once per week for the last month OR PRs queue > 8 hours.
- Leadership is asking 'should we drop trunk-based development?'
- Data available: CI logs, PR sizes, review times, flag inventory.

## Skip If (ANY kills it)

- Teams that have not yet adopted trunk-based development (different methodology).
- Mobile/desktop release-branch projects where trunk-based development is not appropriate.
- Compliance projects with mandated release-cut points (different mode).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| CI logs covering last 2-4 weeks | build status export | CI provider |
| PR metadata (size, time-to-merge, time-to-first-review) | JSON / CSV | git host API |
| Feature flag inventory | table of flag → status → owner | flag provider |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[trunk-based-dev-patterns]] | patterns being audited |
| [[trunk-based-ci-gates]] | the gates that should already exist |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure | 900 |
| `content/05-examples.xml` | essential | Worked end-to-end example | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-data` | haiku | pull CI + PR + flag data from APIs |
| `apply-ordered-checklist` | sonnet | walk the five checks; identify first failure |
| `write-report` | sonnet | emit structured report with recommendation |

## Templates

| File | Purpose |
|------|---------|
| `templates/report.md.j2` | Diagnostic report skeleton |
| `templates/report.md` | Diagnostic report skeleton Generated from `templates/report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/artefact.json` | Sample artefact metadata for validator |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-trunk-based-challenges.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[trunk-based-ci-gates]]
- [[trunk-based-dev-patterns]]
- [[trunk-based-branch-by-abstraction]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.
