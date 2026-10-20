# Agent Replay Harness Cookbook

## Summary

**One-sentence:** Concrete cookbook for wiring deterministic replay into an existing Claude Agent SDK or LangGraph stack — stubs, seeds, clocks, and recorded traces that make agent failures reproducible.

**One-paragraph:** Agents that depend on live LLMs, network calls, and wall-clock cannot be debugged with rerun-it-again. This cookbook walks an operator through capturing every nondeterministic dependency (LLM completion, tool result, time, randomness) as a typed trace, then swapping each one for a replay stub that returns the recorded value when seeded. The output is a runnable replay harness plus a one-page deviation log. Two adapters are provided (Claude Agent SDK and LangGraph); each names which class to subclass and where to inject the stub.

**Ефективно для:** Команд, у яких агент іноді ламається в проді, ніхто не може його повторити локально, і кожен дебаг — це новий запуск з іншим результатом; cookbook за пів дня дає працюючий replay-стек, після якого падіння реплеїться 1-в-1.

## Applies If (ALL must hold)

- Agent stack already runs in production or staging (not greenfield design).
- Failures have been observed but are not reliably reproducible locally.
- Trace storage (S3, sqlite, jsonl) is available with at least 7-day retention.
- Owner can hold a 2-hour pairing session for the harness wire-in.
- Tool wrappers can be subclassed (no closed-source binaries in the hot path).

## Skip If (ANY kills it)

- Agent has no production traffic yet — record at least one real failure first.
- Tool calls are out-of-process binaries with no stubbable surface.
- Trace recording would violate user-data residency rules and no scrubber is available.
- Failures are caused by infra-layer bugs (k8s, network) that the agent layer cannot replay.

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Production agent code | git ref or path | Repo |
| Sample failure trace | jsonl / langfuse / langsmith export | Observability stack |
| Tool registry | JSON `{name, args_schema, side_effect_class}` | Tool catalogue |
| Storage URL | s3:// or file:// path | Ops |
| Named owner | handle/email | Operator |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/autonomous-agents/AGENTS.md` | Provides agent loop vocabulary referenced by stubs. |
| `geek/ai/ai-agents/chaos-eval-fault-injection/AGENTS.md` | Sibling — chaos eval runs on top of replay harness. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: capture-everything, deterministic-seeds, stub-by-type, named-owner, deviation-log | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the replay-harness manifest (stubs + seeds + traces) | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns (missing fields, vague signals, orphan playbook, write-only log, unspecified output location) | ~900 |
| `content/04-procedure.xml` | deep | 7-step procedure from trace capture to replay-green run | ~1300 |
| `content/05-examples.xml` | medium | Worked example: Claude Agent SDK harness for a failing research agent | ~1100 |
| `content/06-decision-tree.xml` | essential | Decision tree: capturable? → stubbable? → reproducible? → adopt / split / escalate | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `parse_failure_trace` | haiku | Structured extraction of tool calls and LLM completions. |
| `synthesize_stubs` | sonnet | Per-tool stub authoring with type-correct returns. |
| `author_harness_manifest` | sonnet | Composes the manifest JSON. |
| `review_for_pii` | opus | Sensitive when traces include user data; high stakes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the replay-harness manifest. |
| `templates/harness-manifest.example.json` | Filled minimal valid example. |
| `templates/replay-stub.py.tmpl` | Python skeleton showing the stub pattern. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate the harness manifest against the JSON Schema. | After subagent emits manifest, before harness is invoked. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- peer: [[chaos-eval-fault-injection]] — fault injection rides on top of replay.
- peer: [[agent-trajectory-eval-method]] — trajectory evals consume replay traces.
- external refs: Datadog harness-first agents post; SakuraSky deterministic-replay series.

## Decision tree

See `content/06-decision-tree.xml`. The tree asks: (1) is the failure already captured in a trace? (2) is every nondeterministic dependency stubbable? (3) does the replayed run reproduce the failure bit-for-bit? Leaves point to "adopt harness", "split — capture more state first", or "escalate — non-stubbable infra dependency".
