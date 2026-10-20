# Agent Drift Detection (Statistical)

## Summary

**One-sentence:** Produces a statistical drift-detection spec: pass-rate control chart with CUSUM, KL divergence on output distributions, judge-score regression with confidence intervals — gates production decisions...

**One-paragraph:** Eval scores drift across model upgrades, retrieval-index updates, prompt edits. No methodology defines the statistical machinery: per-eval pass-rate control charts, KL-divergence on output distributions, judge-score regression with confidence intervals. Without it P7 ships and prays. This produces the detector spec + alert thresholds + a re-test policy keyed to drift severity.

**Ефективно для:** production agents with daily eval runs; teams making deploy/rollback/freeze decisions on numeric evidence; pre-GA agents stabilizing across model upgrades.

## Applies If (ALL must hold)

- You are stabilizing or comparing AI feature behavior across model, prompt, or retrieval versions
- A ground-truth set ≥30 examples exists OR can be assembled in one work-cycle
- Eval results gate at least one production decision (deploy, rollback, freeze)
- Cost ceiling per eval run is defined before the first run

## Skip If (ANY kills it)

- Pre-MVP exploration where output quality is judged by founders eyeballing
- Features so niche that authoring a ground-truth set takes longer than 3 sprints
- Cost-prohibitive evals when cheaper proxies (regression of intermediate metric) cover risk

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Eval suite ≥30 examples | JSONL + judge rubric | eval owner |
| Baseline scores from green run | table | eval owner |
| Cost-per-eval-run estimate | USD | finance |
| Output distribution sampler | trace stream | observability |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[agent-eval-harness-bootstrap-recipe]]` | Harness to run evals on schedule |
| `[[agent-observability-stack-blueprint]]` | Trace stream for distribution analysis |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale and source | ~550 |
| `content/02-output-contract.xml` | essential | JSON-schema output shape + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 6-step procedure with input/action/output per step | ~900 |
| `content/05-examples.xml` | medium | worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Compute baseline | sonnet | Mechanical. |
| Tune CUSUM thresholds | opus | Trade-off across false-alarm vs detection delay. |
| Author runbook | sonnet | Composition. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cusum.py.tmpl` | CUSUM detector implementation. |
| `templates/kl-detector.py.tmpl` | KL divergence detector. |
| `templates/regression-test.py.tmpl` | Paired t-test with Bonferroni. |
| `templates/_smoke-test.py` | Smoke test wiring all three detectors. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agent-drift-detection-statistical.py` | Validates an output document against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- `[[agent-eval-harness-bootstrap-recipe]]`
- `[[agent-eval-test-set-curation]]`
- `[[agent-postmortem-template]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether agent-drift-detection-statistical applies: root question — "Does the team gate prod decisions on eval scores?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip:` conclusion when it does not.
