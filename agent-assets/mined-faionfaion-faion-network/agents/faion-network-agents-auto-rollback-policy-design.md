# Auto Rollback Policy Design

## Summary

**One-sentence:** Quality-score-based auto-rollback policy for AI features: thresholds + window + traffic ratio + manual override; replaces ad-hoc on-call decisions with a deterministic config.

**One-paragraph:** Model swaps and prompt updates are deployed under on-call pressure with ad-hoc rollback decisions. This methodology specifies a quality-score-based auto-rollback policy: per-axis thresholds (outcome / trajectory / resources), time window for rolling average, traffic-ratio gate for canary, manual override path, and a post-rollback runbook. Output is a YAML config consumed by the deploy pipeline + alerting wire; CI validates the config against the schema on every PR. Replaces fire-drill rollbacks with measurable, debate-free decisions.

**Ефективно для:**

- Model migration (4.5 → 4.6 / 4.7) — auto-rollback ловить regressions без on-call судження.
- Prompt swap у production: канарковий ratio + auto-rollback при quality drop &gt; 5pp.
- RAG chunking changes — quality-score gate видаляє debate з deploy decision.
- ML-ops команди, які хочуть SLO-style guarantees на AI feature reliability.

## Applies If (ALL must hold)

- AI feature has measurable quality score (eval rubric from trajectory-eval-otel or ai-feature-eval-set-design).
- Deploy pipeline supports canary or traffic-shift rollout.
- On-call team is the bottleneck during rollouts (ad-hoc rollback decisions take &gt; 30 min).

## Skip If (ANY kills it)

- Quality score is unmeasurable in real-time (no scoring pipeline within 10 min of inference).
- Single-tenant on-prem deploy where rollback is a manual restart.
- Experimental / pre-launch features where rollback semantics don't apply yet.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Quality-score pipeline | function: trace → score (0-1) | from trajectory-eval-otel or feature-eval |
| Deploy pipeline | canary / traffic-shift support | infra |
| Baseline score | JSON with score per axis | first eval run |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[trajectory-eval-otel]] | upstream context required for this methodology |
| [[ai-feature-eval-set-design]] | upstream context required for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: per-axis-thresholds, rolling-window-required, canary-ratio-and-baseline, manual-override-logged, post-rollback-runbook | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for config + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `calibrate-noise-floor` | haiku | Statistical math over baseline window. |
| `design-canary-ladder` | sonnet | Light judgment on risk vs speed. |
| `wire-threshold-check` | haiku | Template-based config wiring. |
| `wire-runbook` | sonnet | Cross-team workflow design. |

## Templates

| File | Purpose |
|------|---------|
| `templates/post-rollback-runbook.md.j2` | 4-step post-rollback runbook |
| `templates/post-rollback-runbook.md` | 4-step post-rollback runbook Generated from `templates/post-rollback-runbook.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-auto-rollback-policy-design.py` | Validate the config artefact against the schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[trajectory-eval-otel]]
- [[ai-feature-eval-set-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, eval scores, stakes, noise ratio, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
