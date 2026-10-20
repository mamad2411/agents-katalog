# Codex Agent Harness Module

Adapter module that registers the `codex` harness. The harness shells out to
the installed Codex CLI (`codex exec --json`) instead of calling
`@openai/agents` directly. This is load-bearing: Codex CLI is the surface that
honors `codex login` and ChatGPT-plan subscription access, while the OpenAI
Agents SDK requires API-key auth.

Use the `codex` preset, default harness config, or a per-step `harness` to
route a run through this adapter.

## Provider Routing

Models are passed to `codex exec --model` verbatim. The shipped Codex preset
maps fast, balanced, and capable work to GPT-5.6 Luna, Terra, and Sol. The
adapter projects shared native executable/locale state, the Codex login locator,
and the trusted native upstream-proxy setting. The shared native sandbox consumes
that setting to chain provider egress and removes it before launching the CLI.
`OPENAI_API_KEY` and unrelated daemon credentials do not enter
the child, so exported keys cannot take priority over local Codex login.

KOTA supports Codex CLI `0.144.1` or newer for this GPT-5.6 integration.

Account quota inspection uses the installed CLI's app-server account RPC,
with no agent turns or reset-credit consumption. Normalize only the weekly
Codex account bucket; never substitute Spark, five-hour limits, or run usage.

Reasoning effort maps to Codex CLI's `model_reasoning_effort` config:

- `low` -> `low`
- `medium` -> `medium`
- `high` -> `high`
- `xhigh` -> `xhigh`
- `max` -> `max`

## Loop Shape

The adapter runs one non-interactive CLI process per KOTA harness call:

1. Compose the KOTA system prompt, workflow rails, and task prompt into one
   stdin prompt for `codex exec -`.
2. Spawn a strict-config `codex exec --json` process with user
   plugins and hooks disabled and the selected model. Codex owns the single
   tool sandbox through an invocation-generated permission profile: model
   shell tools stay offline, writes follow the projected scope, project and provider
   credentials are denied, and approvals fail closed. KOTA owns the isolated
   runtime, provider proxy, process lifecycle, and live-policy abort.
3. Parse JSONL events from stdout. Completed commands and native web searches are projected
   into neutral tool-call/result evidence, while `item.completed` agent-message
   events are streamed to the optional `AgentHarnessWriter` and collected as
   final text.
4. Read the final `turn.completed` usage event for token counts and return the
   neutral `AgentHarnessResult`.

Cancellation terminates the CLI process group so spawned tools cannot outlive
the CLI, and the run-local quarantine barrier stays pending until the group
leader has closed. The barrier also covers prelaunch validation so rejected
options release ownership without claiming that a process launched.

`passive` is rejected because the adapter cannot classify and deny every
non-safe native shell/tool invocation before it runs. `supervised` is rejected
because this non-interactive CLI path cannot route approvals through KOTA's
approval queue. Autonomous writes remain bounded by the effective scope policy.

## Capability Boundary

Codex CLI owns its tool runtime and sandbox. This adapter does not expose
KOTA's tool registry, MCP servers, `allowedTools`, `disallowedTools`, `canUseTool`, or
scope-policy evaluator to the model. It declares `toolControl: "native"` and
rejects unsupported neutral options before Codex CLI starts. The generated
permission profile enforces scope independently of the prompt, and a stricter
live policy revision aborts the process.
Provider-hosted live web search is enabled only when the resolved scope policy
allows external-network reads. Missing, denied, or confirmation-required authority
disables it. This does not grant shell networking or KOTA module access. Search
completion events retain queries; source results remain in the native conversation
and cited findings, not fabricated tool-result bodies.
`askOwnerToolName` is therefore `null`, so workflow prompts do not advertise a
fake `ask_owner` tool. Workflows that need owner escalation should use the
deterministic `askOwnerSteps` recipe outside the agent step.

Workspace configuration uses existing workspace read access. Configuration
symlinks confer no authority over external targets; shared configurations
require independent runtime-owned read grants supplied in harness run options.
The adapter carries those grants through the launcher into the generated tool
permission profile; scope configuration and prompts cannot supply them.

The adapter still carries KOTA's shared native workflow rails in the prompt:
agents treat Git metadata as read-only, leave workspace changes unstaged for
runtime-owned commits, and must not stop or control the daemon that launched
them. Post-step workflow checks remain responsible for validating repo state.
It uses a fresh `CODEX_HOME` and explicitly disables plugins and hooks, so
operator-global extensions cannot affect daemon-launched workflow steps;
Codex auth is copied into the provider-only per-invocation runtime home.
Tool permissions deny both the original login credential and the runtime home,
preserving lexical and resolved identities over overlapping grants. Runtime-supplied
scratch and artifact roots remain writable independently of the repository write
scope, as in the other native adapters.
Trusted host isolation may replace `HOME`; the adapter projects only the
resolved `CODEX_HOME` locator so local login remains available without
restoring the operator home environment. Contained eval launches use the adapter's
single-file login declaration; the eval owner snapshots it outside the candidate
workspace and supplies a read-only container login directory. The same native
permission profile denies the mounted credential and disposable runtime home to
tools. Credential readability is not proof of a valid login or model entitlement.
Native and contained provider policies share the adapter-owned endpoint declaration
so login renewal and inference require the same allowlist.

## Session storage

Core binds one native thread to each logical conversation. `thread.started`
checkpoints identity immediately; continuation uses `exec resume <uuid>` and
never `--last`. Each invocation receives fresh authentication and permissions in
its disposable `CODEX_HOME`. Only native rollout directories point into the
protected, scope-owned conversation store, so home or worktree cleanup cannot
erase them. Explicitly declined preservation uses `--ephemeral`. Missing or
corrupt owned rollout metadata produces an evidenced successor through core;
provider/authentication failures keep the original identity. Histories produced
by older ephemeral launches cannot be reconstructed.
