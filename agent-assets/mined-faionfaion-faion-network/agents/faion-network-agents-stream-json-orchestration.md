# Stream-JSON Orchestration

## Summary

**One-sentence:** Wrap the agent CLI as a subprocess and react to its `stream-json` events line by line — budget, safety, hand-off — instead of waiting for the final answer.

**One-paragraph:** Produces a Python (or Node) orchestrator that spawns `claude -p --output-format stream-json --allowedTools ... --max-turns N` (or the equivalent Codex / opencode flags), reads stdout line-by-line, parses each JSON event (`system/init`, `assistant`, `user/tool_result`, `result`), and applies budget caps, safety vetoes, conditional chaining, and telemetry export — all mid-run. Defence-in-depth includes `--max-turns`, `--allowedTools`, closed stdin, and an event-log file for replay.

**Ефективно для:** довгих агентських тасків (≥30 сек) у production-orchestrator, де треба телеметрію, budget cap або safety veto в реальному часі — а не post-mortem після того, як CLI вже допрацював.

## Applies If (ALL must hold)

- Orchestrator spawns a coding-agent CLI (`claude`, `codex`, `aider`, `opencode`) as a subprocess.
- Task is expected to run ≥30 seconds or cost ≥$0.10 — long enough for mid-run reaction to matter.
- The orchestrator process can read stdout incrementally (Python `bufsize=1`, Node `readline`).
- The agent CLI supports a stream-json output mode (Claude Code does; opencode/codex have equivalents).
- Budget cap, safety veto, or conditional hand-off is a real requirement, not a nice-to-have.

## Skip If (ANY kills it)

- One-shot tasks under 5 seconds — parsing overhead exceeds value.
- The SDK is available and exposes the same hooks (in-process is cleaner; see Anthropic Agent SDK).
- Output is piped directly to a human in a terminal — pretty-print mode is more readable.
- The CLI does not have a stream-json mode (some forks omit it).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Agent CLI binary | executable on `$PATH` | `which claude` |
| Allowed tools list | comma-separated | risk-assessment per task |
| Per-task budget cap | float USD | product policy |
| Persistent log dir | filesystem path | infra (`runs/`) |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/headless-cli-four-guards` | Defines the four mandatory CLI flags this methodology consumes. |
| `geek/ai/ai-agents/subagent-as-context-firewall` | Stream-per-subagent pattern uses this orchestrator. |
| `geek/ai/ai-agents/trajectory-eval-otel` | Stream events feed OTel spans per the GenAI conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules: stream-json mandate, line-buffered read, allowedTools+max-turns, JSON-decode guard, result-event mandatory, replay log, stderr separate | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the run report: session_id, events_count, total_cost_usd, kill_reason, replay_path | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: buffered output, regex-on-plain-text, missing backpressure, no max-turns, ignoring result event | ~700 |
| `content/04-procedure.xml` | medium | Step-by-step: spawn → consume → dispatch → budget → safety veto → replay → finalize | ~900 |
| `content/05-examples.xml` | medium | 5 worked cases: Discord live UI, $0.50 cost cap, file-delete veto, conditional hand-off, OTel telemetry | ~600 |
| `content/06-decision-tree.xml` | essential | Picks the orchestrator shape from task length, budget cap, safety requirements | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Generate the spawn-and-parse skeleton | sonnet | Boilerplate code, deterministic. |
| Map events → OTel spans | sonnet | Mechanical translation. |
| Design the safety-veto rule set | opus | Risk judgement; opus weighs which tool calls to block. |
| Diagnose a hung stream | sonnet | Pattern-matching against known failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/stream_handler.py` | Reference Python class consuming `claude -p --output-format stream-json` with budget cap, allowlist, and replay log. |
| `templates/stream-handler.node.mjs` | Same pattern in Node.js using `child_process.spawn` + `readline`. |
| `templates/jq-filter.sh` | Bash one-liner extracting only assistant messages from a stream-json file for grepping. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stream-json-orchestration.py` | Validates a run report against `02-output-contract.xml` schema. | After each orchestrator run; called by the post-run hook before persisting the report. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[headless-cli-four-guards]] — the four flags (-p, --allowedTools, --max-turns, stream-json) this methodology operationalises.
- [[subagent-as-context-firewall]] — each subagent gets its own stream; this methodology is the pipe.
- [[trajectory-eval-otel]] — stream events → OTel spans.
- [[semantic-field-naming]] — orchestrator code sees field names from the agent's tool calls; renaming pays off here too.

## Decision tree

The tree at `content/06-decision-tree.xml` picks the orchestrator shape from three observables: task length, hard budget cap, and safety-veto requirement. Tasks ≥30s with a budget cap need the full Python class + cost tracker; tasks ≥30s without a budget but with safety vetoes need the event-dispatcher pattern; sub-5-second tasks bypass this methodology entirely and use direct SDK calls.
