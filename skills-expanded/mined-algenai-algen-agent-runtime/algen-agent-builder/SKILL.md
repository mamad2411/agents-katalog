---
name: algen-agent-builder
description: Create or update an Algen-compatible single-agent or multi-agent project that uses Runtime manifests, governance, tests, and Studio-importable packaging.
---

# Build an Algen agent project

Start by choosing the smallest topology that fits: one agent for a single governed conversation, or
a Runtime `WorkflowManifest` for coordination. Scaffolding is available via the CLI:
`algen-agent-runtime new <name> [--template agent|approval|workflow]`. Read `references/project-shape.md`;
for a workflow, also read `references/workflows.md`. Use `$algen-agent-connector` when external tools,
safe starter tools (`algen_agent_runtime.tools.starter`), databases, retrieval, MCP, or remote APIs are part
of the request.

Prefer configuration for provider routing, policies, memory, retrieval, storage, telemetry, and
workflow topology. Keep only domain-specific payload builders, validators, schemas, predicates, and
deterministic handlers in the project's hook provider. Never implement a second scheduler or a
Studio-specific workflow dialect. For automated CI and headless evaluation, use non-interactive workflow
options (`--approve-all`, `--reject-all`, `--answers-file PATH`).

Produce an importable project with secret references, bounded execution, deterministic offline
tests, documented optional dependencies, and a small runnable entry point. Depend on
`algen-agent-runtime[service]` only when the project serves the HTTP API or exports OTLP
telemetry; an embedded library use needs no extra. A project intended for
Studio must keep its Runtime configuration and `WorkflowManifest` authoritative. Studio sees only
what the settings declare, never constructor arguments, so:

- Every name an agent uses (`enabled_tools`, `planning_strategy`, `response_composer`, `verification_policy.verifiers`,
  `context_builder`, `guardrail_policy.policies`, provider types) must come from the Runtime,
  the settings (`http_tools`,
  `mcp_servers`, `providers`, `retrieval`) or a plugin listed in `domain_plugins`. Register code
  components from a declared plugin, never through `build_container(additional_tools=...)`; see
  `docs/plugins.md`.
- Credentials only through `env://` references; list a plugin's variables in `PluginManifest.env`.
- If the project runs its own server, workers or approval flow, say plainly that Studio runs only
  the Runtime contract, not that code.
- `build_container` fails on any name no source registered and suggests the closest one; fix the
  name or its registration, never switch `runtime.component_check` to `warn` to hide it.
- A project that runs its own host (not Studio) checks with
  `algen-agent-runtime check agent.yaml --path src --profile standalone`, which leaves out the
  Studio-only warnings but keeps every error.
- Before calling a project Studio-importable, run `algen-agent-runtime check agent.yaml --path src`.
  It must report no errors; read every warning to the user, since each names code Studio will not
  run or cannot see. `algen-agent-runtime describe --path src` shows the full inventory, and
  `docs/studio-compatibility.md` lists what Studio can and cannot see.
- Write tools as typed functions with `@tool` or a `Toolkit` and a preset (`docs/tool-authoring.md`),
  and test each with `assert_tool_contract`.

An agent that makes many tool calls or changes state should use the Runtime's own guards rather than
rules in its instructions or plugin code: prechecks, refusal limits, the repeat guard and call
limits, the wrap-up notice, shortened older tool results, the partial answer at a limit
(`budget.on_limit: summarize`, read `RunResult.partial`) and the cut of an oversized tool result
(`context_policy.oversized_tool_result`, on by default). An agent that needs a larger context
budget than the builder's 16,000 tokens sets `context_policy.max_context_tokens` instead of
registering its own context builder. Screen retrieved evidence from corpora
others can write to with `guardrail_policy.retrieval_injection`. A tool that must act as the signed-in
user reads the caller's credentials from `ToolContext.credentials`. For several users, give each
user their own `session_id`, grant `approvals:decide` to people who approve other users' runs, and
let an agent delegate with `core.subagent` only to the agents in its `delegates` list (off unless
`runtime.subagent.enabled`); a delegate's approval or question pauses the caller and is decided
there. Since 0.2.0b4 a delegate may enable only tools its caller enables too (apart from
`core.working_state_update`, `core.skills_load` and `core.context_read`), runs with its caller's
approval requirements and guardrails added, counts against its caller's budget, and one run tree
starts at most `runtime.subagent.max_descendants` (64) child runs. An agent that must ask the user
mid-task enables `core.ask_user`; the answer passes the run's `input` policies. Streamed text is
redacted before it is sent (`guardrail_policy.stream_text`, default `redacted`; `off` sends no
deltas), and a UI discards text a `model.delta.retracted` withdraws. Follow a whole turn,
through its pauses, with `client.follow(run_id)` or `?through_pauses=true`. See "Tool-heavy and
acting agents" in `references/project-shape.md`.

Validate YAML by loading it through the current Runtime model rather than relying on syntax alone.
Run the project smoke test and relevant Runtime tests. Do not publish to a marketplace or deploy
unless the user explicitly requests that external action.

