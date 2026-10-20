# Trajectory Evaluation with OTel GenAI Spans

## Summary

**One-sentence:** Score agent runs across outcome / trajectory / resources axes using OTel GenAI spans + tool child spans, validated by a per-run eval-report schema and gated in CI.

**One-paragraph:** Two agents can both succeed but burn 11x different resources and walk 7x different path lengths. Outcome-only eval ("% correct") hides cost and step regressions until the monthly bill arrives. This methodology forces OpenTelemetry GenAI semantic conventions on every LLM call, child spans on every tool dispatch, prompt content stored by SHA-256 hash with a side store, and a three-axis rubric (outcome, trajectory, resources) baked into the eval-report schema. CI gates PRs on regressions &gt; 25% on any axis. Replay-based debugging becomes trivial: spans carry enough state to re-run a failed call against a sandbox.

**Ефективно для:**

- Production-агенти з регресіями cost'у після model-bump'а — три-axis eval ловить ще до monthly bill'у.
- A/B prompts/моделей: outcome equal, але trajectory або resources показують справжній winner.
- Compliance / audit: replay-based debugging з spans = повне відтворення прод-помилки за хвилини.
- Subagent-architecture: span-nesting depth — рання попередження про неконтрольований fan-out.

## Applies If (ALL must hold)

- Agent runs in production or staging where regressions matter (cost, latency, correctness all observable).
- An OTLP backend exists or can be provisioned (Langfuse / Phoenix / Datadog / Helicone / open-source).
- An eval set of ≥50 representative tasks with ground-truth answers exists.

## Skip If (ANY kills it)

- One-shot personal scripts where instrumentation cost exceeds the run cost.
- Hard-PII contexts where redaction at the span boundary is not feasible (use a privacy-preserving collector first).
- Latency-critical sub-millisecond inference paths where even 1ms span overhead matters.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Application source | Python / TS / Go | repo |
| OTLP endpoint | URL + auth | observability backend |
| Eval set | 50+ task prompts + ground-truth answers | recorded user requests / synthetic set |
| Baseline scores | JSON | first eval run committed to repo |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[terse-default-tool-output]] | Verbose tool outputs are the most common cause of resource-axis regressions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: three-axis, otel-genai-semconv, tool-span, hash-not-paste, ci-eval-gate | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for eval-report (run_id, scores, raw, verdict, deltas) | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: outcome-only, ad-hoc-span-attrs, tool-blind-trace, inline-prompt-storage | 800 |
| `content/04-procedure.xml` | essential | 5-step setup: wire-tracer → instrument → rubric → run → ci-gate | 800 |
| `content/06-decision-tree.xml` | essential | Branches on regression class + loops + cache-hit drop | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `wire_otel_tracer` | haiku | Boilerplate SDK setup; deterministic. |
| `instrument_llm_tools` | haiku | Wrapper-template application. |
| `outcome_judge` | sonnet | LLM-as-judge needs reasoning when ground truth is open-ended. |
| `regression_analyst` | opus | Cross-axis correlation + root-cause synthesis at release-gate time. |

## Templates

| File | Purpose |
|------|---------|
| `templates/python-instrument-anthropic.py` | OTel-instrumented Anthropic call with full `gen_ai.*` attribute set |
| `templates/python-instrument-tool.py` | Tool dispatcher wrapped in `agent.tool.&lt;name&gt;` child span |
| `templates/langfuse-decorator.py` | `@observe()` shortcut for Langfuse-OTel bridge |
| `templates/subagent-span-nesting.py` | Parent-agent → subagent span hierarchy pattern |
| `templates/eval-rubric.py` | Pydantic model for the 3-axis rubric + LLM-as-judge structured output |
| `templates/ci-eval-gate.yml` | GitHub Actions workflow gating PRs on the eval report |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-trajectory-eval-otel.py` | Validate an eval-report JSON against the schema | CI on each eval run; pre-commit on baseline updates |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[terse-default-tool-output]] — resource-axis regressions usually trace to verbose tool outputs.
- [[tool-description-as-prompt]] — trajectory regressions often correlate with description drift.

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on which axis regressed &gt; 25% (outcome / trajectory / resources). For trajectory, it asks whether loops are present (same tool + args ≥3 times). For resources, it checks whether the cache hit ratio dropped (prompt-prefix change) or stayed flat (tool-verbosity growth). Each leaf references a rule from `01-core-rules.xml`.
