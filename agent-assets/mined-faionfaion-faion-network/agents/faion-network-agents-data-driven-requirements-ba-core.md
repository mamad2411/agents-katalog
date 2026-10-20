# Data-Driven Requirements

## Summary

**One-sentence:** Produces a requirements set derived from observed data signals (analytics, telemetry, support tickets) with explicit evidence trails per requirement.

**One-paragraph:** Produces a requirements set derived from observed data signals (analytics, telemetry, support tickets) with explicit evidence trails per requirement. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- Existing product з аналітикою/телеметрією, де sponsor хоче data-evidence перед написанням requirement'ів.
- Conversion/retention initiative, де треба викинути guess-driven scope і триматись funnel-метрик.
- Conflict-arbitration: два stakeholder'и протиставлені, потрібен emprical arbiter.
- Compliance/a11y програма з instrumentation gap'ами, що драйвлять scope.

## Applies If (ALL must hold)

- Existing product with analytics, telemetry, or support data signals to mine.
- Stakeholders contradict each other and need empirical arbitration.
- Conversion / funnel / retention improvement initiative where guessing scope wastes cycles.
- Compliance or accessibility programme where instrumented gaps drive scope.

## Skip If (ANY kills it)

- Pre-launch / pre-data product — no signal exists yet.
- Decision is irreversibly political — evidence will not move it.
- Data quality is too low (noise > signal) to trust derived requirements.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Analytics access (GA4, PostHog, Amplitude, internal) | API / dashboard | data team |
| Telemetry stream (errors, performance) | Sentry / Datadog / internal | engineering |
| Support ticket export | CSV / API | CX team |
| Hypothesis log | Markdown | BA / PM |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[requirements-documentation]] | downstream consumer of evidence-trailed requirements |
| [[requirements-prioritization]] | evidence trail feeds RICE / WSJF scoring |

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
| `pull-data-signals` | haiku | Mechanical extraction from configured sources. |
| `correlate-and-cluster` | sonnet | Group signals into themes; tag with evidence weight. |
| `draft-requirements` | opus | Convert clusters into requirement statements with rationale. |

## Templates

| File | Purpose |
|------|---------|
| `templates/evidence-trail.md.j2` | Per-requirement evidence trail: signal → metric → requirement. |
| `templates/evidence-trail.md` | Per-requirement evidence trail: signal → metric → requirement. Generated from `templates/evidence-trail.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/data-driven-spec.md.j2` | Full spec.md skeleton with evidence column per requirement. |
| `templates/data-driven-spec.md` | Full spec.md skeleton with evidence column per requirement. Generated from `templates/data-driven-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[requirements-documentation]]
- [[requirements-prioritization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
