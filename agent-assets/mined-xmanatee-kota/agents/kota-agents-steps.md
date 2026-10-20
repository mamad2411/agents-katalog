# Step Executors

This directory owns step execution strategies and context construction.

- `step-executor.ts` is the entry point: it dispatches to the correct step type
  handler and exports shared helpers (`shouldRunStep`, `resolveValue`,
  `executeCodeStep`).
- Each `step-executor-<type>.ts` implements one step type strategy (agent,
  approval, branch, foreach, parallel, retry classification, trigger).
- `step-context.ts` constructs `WorkflowStepContext`; workflow-owned judges,
  reviewers, and resolvers use `ctx.runAgentHarness` for scope-owned backoff
  admission, cancellation, workflow tracing, live scope authority, and
  canonical prompt/outcome evidence under the owning step. Direct native
  harness calls carry that authority into fail-closed capability preflight
  before process launch.
- Code-step subprocesses use `ctx.runCommand`; the runtime binds cancellation,
  bounded output, timeout, process-group termination, and durable process
  registration through the shared process supervisor.
- `ctx.runTool` applies the shared tool middleware before journaling results, so
  recovered effects retain their screened output without repeating execution.
  It returns tool error results for the consumer to interpret;
  declarative tool steps and repair checks reject them, while collectors can
  retain source-level failure evidence. Runtime policy and cancellation still
  reject the call and must not be treated as a recoverable source observation.

New step types add a new strategy file here and a dispatch case in `step-executor.ts`.

## Per-Phase Files Inside `step-executor-agent.ts`

The agent orchestrator owns attempt orchestration, classified retries, and the
whole-step writeScope contract. New internals land in co-located phase files;
phase-only helpers stay local. Native cancellation and restrictive-policy
invalidation use the shared agent-harness lifecycle described in
`src/core/agent-harness/AGENTS.md`.

## Per-Run Emitted-Events Log

`createStepContext` wraps `ctx.emit` so every emission a step makes appends
a `{event, schemaRef, payload, emittedAt}` entry to
`<runDir>/emitted-events.jsonl`.
This is the authoritative per-run bus-event trace: the bus itself does not
retain history, and step output only captures emissions the step chose to
list in its returned summary. The eval-harness `run-emits-event` and
`run-omits-event` predicates inspect this file directly. Callers that need
to assert on what a workflow emitted should read the log, not the step's
self-report.

## Agent writeScope: declare → enforce → fail

Every `AgentDef` declares a `writeScope` of allowed repo paths. `[]` means
unrestricted; `"deny-all"` means read-only. Silence never means write-anywhere.

Restricted and deny-all scopes compare content-and-index-aware pre/post
snapshots, including paths already dirty before the step. Unrestricted scope
uses lightweight mutation-path attribution because it has no rejection
boundary. An out-of-scope mutation throws `AgentWriteScopeViolationError` and
records the paths in the step artifact. This hard failure consumes no retry.
Deny-all restores the exact pre-step index and workspace. Other scope
violations fail inside the run-owned sandbox; `RunLifecycle` owns the resulting
run disposition and cleanup.

This enforcement lives in the core executor, not in per-workflow prompts or
repair checks. Workflows declare scope honestly on their agent definitions
and let the runtime reject out-of-scope writes uniformly.

## Session ownership

Agent-step repair retains the original runtime-owned continuity key when routed
through `ctx.runAgentHarness`; nested judges receive a separate scoped identity.
Foreach supplies a stable item index for agent and nested code-step conversations,
including equal-valued items. Retries reuse that item owner; step-only session
result projections cannot choose a foreach conversation.

## Per-Step Harness-Specific Options

The neutral `WorkflowAgentStep` shape has no harness-specific fields. A step
that needs a non-default posture on a particular harness declares the
carve-out through the generic `harnessOptions` passthrough:

```ts
{ type: "agent", harness: "claude-agent-sdk",
  harnessOptions: { "claude-agent-sdk": { /* adapter-private fragment */ } },
  ... }
```

The block is a single-key record whose key must equal the step's resolved
harness name; the value is opaque to core and validated by that harness's
registered `validateStepOptions` method. The validated fragment travels to
the adapter at runtime through `AgentHarnessRunOptions.harnessOverrides`.
The core validator rejects mismatched keys, unknown harnesses, and harnesses
that declare no per-step options. See `src/core/agent-harness/AGENTS.md` for
the protocol surface.

## Resolved Harness And Model On Agent Step Results

Every successful agent step records the harness identifier the registry
actually returned (`resolveAgentHarness(step.harness).name`) and the model
the adapter ran with (`resolveAgentModel(step, agentConfig)`) on the
top-level `WorkflowStepResult`. These fields are populated only for agent
steps — non-agent step results omit them. The static `workflow.json` step
config keeps `model`/`effort` for pre-run introspection; consumers
surfacing harness identity (CLI run readouts, tracing) should prefer the
runtime values on the step result over re-deriving them from the static
config.

## Structured Agent Output

`outputSchema` is the single contract for JSON agent output. The core prompt
renders it, harnesses may enforce it through native structured-output support,
and the executor validates the normalized result. Prompts must not duplicate
schema fields or default missing fields. External or agent-authored exposed
text declares `exposedOutputTrust: "untrusted"` for screened, escaped rendering.

## Agent-Step Retry and Error Classification

Every agent step inherits `DEFAULT_AGENT_STEP_RETRY` from
`step-executor-retry.ts`. Add a per-step `retry:` override only when a step
has a genuinely different requirement and justify it with a comment.

Retries consume attempts only for classified transient failures (rate-limit,
auth, provider 5xx/timeouts, socket errors), JSON output extraction errors
(missing fence or invalid JSON), and JSON-schema validation errors. Runaway-agent
subtypes (`error_max_turns`, `error_max_tokens`), malformed tool calls, and
other deterministic mistakes are **unclassified**: the step fails on the first
attempt without burning budget or triggering agent-dispatch backoff.

Classification is driven by structured signals (SDK result subtype, HTTP
status, Node error codes, and narrow SDK-specific text markers). See
`classifyAgentRuntimeFailure` for the full signal table. Do not add broad
fuzzy string matches to the classifier. The same classifier governs autonomy
agent judges; see `src/modules/autonomy/AGENTS.md` for the judge-wrapper rule
that separates unavailable review from rejected repository behavior.

The workflow harness runner applies this classifier to every workflow-owned
agent call. A classified provider result activates `AgentBackoffManager`
immediately, so repair agents and code-step judges cannot launch an internal
retry during the same incident.

Local invocation and required-evidence failures stop the owning run without shared
backoff. Repair checks propagate unavailable invocations instead of treating them
as a substantive rejection that can request source repair. Only classified runtime
incidents carry shared backoff; wrappers must preserve that distinction.
