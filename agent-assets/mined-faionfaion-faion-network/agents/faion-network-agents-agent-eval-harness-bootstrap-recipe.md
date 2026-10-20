# Agent Eval Harness Bootstrap Recipe

## Summary

**One-sentence:** Produces a CI-gated eval harness in one engineer-week: wires trajectory-eval-otel + llm-judge-rubric + record-replay + chaos-eval + behavioral-evals + llm-as-judge into a single runnable harness.

**One-paragraph:** Atomized methodologies exist (`trajectory-eval-otel`, `llm-judge-rubric-evidence-first`, `record-replay-debugging`, `chaos-eval-fault-injection`, `behavioral-evals-adversarial`, `llm-as-judge-harness`). Missing: the wiring playbook that turns those 6 into a working CI gate in one engineer-week. Right now P7 reinvents the integration for every agent.

**Ефективно для:** engineering teams shipping a new agent who need a working CI gate within one sprint; teams migrating ad-hoc eval scripts into a single harness; ML-platform builders standardising eval across multiple agents.

## Applies If (ALL must hold)

- Team has an agent + ≥30 trajectory examples
- CI exists and can run a Python or TS harness in a job
- Owner exists for harness maintenance
- Budget allows one engineer-week of bootstrap effort

## Skip If (ANY kills it)

- Existing harness already passes the 6-capability test — extension, not bootstrap
- No trajectory data — collect first via observability
- n<3 instances — gut feel is faster

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| ≥30 trajectory examples (golden set) | JSONL | eval owner |
| Judge rubric (1-5 anchors per criterion) | Markdown | domain expert |
| OTel trace ingest | tracing backend | observability |
| LLM API access (judge + agent) | keys | ML platform |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[agent-eval-test-set-curation]]` | Curated test set |
| `[[agent-observability-stack-blueprint]]` | Trace ingest path |
| `[[agent-eval-cost-budget-policy]]` | Cadence policy this harness implements |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale and source | ~550 |
| `content/02-output-contract.xml` | essential | JSON-schema output shape + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 6-step procedure with input/action/output per step | ~900 |
| `content/06-decision-tree.xml` | essential | decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Author rubric anchors | opus | Domain reasoning. |
| Implement runner | sonnet | Template application. |
| Tune CI thresholds | opus | Trade-off across false-positive vs detection. |

## Templates

| File | Purpose |
|------|---------|
| `templates/runner.py.tmpl` | Harness runner: replay → judge → score → CI exit. |
| `templates/_smoke-test.py` | Smoke test that runs harness against 3 trajectories. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agent-eval-harness-bootstrap-recipe.py` | Validates an output document against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- `[[agent-eval-test-set-curation]]`
- `[[agent-eval-cost-budget-policy]]`
- `[[agent-drift-detection-statistical]]`
- `[[agent-observability-stack-blueprint]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether agent-eval-harness-bootstrap-recipe applies: root question — "Does the team have ≥30 trajectories AND a CI pipeline?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip:` conclusion when it does not.
