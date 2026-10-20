# Tools

Core owns the agent/session tool pipeline, guardrails, daemon coordination and
module lifecycle. General-purpose capabilities belong in modules.

## Ownership

- `index.ts` installs core tool declarations. Implementations consume
  `tool-registry.ts`; registry reads do not initialize implementations. Registrations return exact
  disposers; module labels are metadata, not cleanup authority.
- `tool-runner` owns admission, input/output validation, approvals and execution.
  It enforces invocation-local read scope, agent write scope and isolated output
  roots before filesystem access, failing closed on opaque targets. Nested calls
  inherit its permissions, scope and session context; module callbacks alone
  grant no tool authority.
- Delegation settings belong to the owning session and effective harness invocation.
  Generic delegates and named handoffs share `delegation-runtime`; direct callers
  supply explicit runtime configuration. Async initialization never publishes
  session settings process-wide.
- `tool-middleware` provides one continuation per invocation. Retry and caching
  belong to the capability that knows an operation's effects and resource identity.
- `guardrails-config.ts` owns configuration decoding and policy snapshots;
  `guardrails.ts` and `guardrails-classify.ts` assess execution risk.
- `audit-store` owns audit records and approval-review redaction.
  `protected-scope-paths` owns the credential boundary shared by filesystem
  tools and native CLI sandboxes. Conversation stores in the canonical scope
  and workspace remain protected through resolved aliases, independently of
  the execution directory.
- `session-environment` owns live session/scope credential overlays. Registration
  owns teardown; stale approvals cannot recreate an ended session's overlay.
- Filesystem read and mutation targets come from the registered tool's pure
  `resolveFilesystemTargets` declaration using the runner's execution context.
  Declare every destination, including derived paths and ancillary mutations;
  Network operations declare ancillary download destinations through the same
  contract. A declaration of no ancillary writes never exempts a local write effect;
  opaque execution and unresolved dynamic target sets remain unknown and are
  denied under bounded write policies. Generic input fields grant no authority.
- Executable approvals snapshot the registry generation, declaration, resolved
  effect, inputs, execution roots and targets, including opaque operations.
  Preflight leases that exact definition and runner;
  dispatch rejects operation drift. Nested runner overrides cannot borrow the
  registered operation's authority.

## Core capabilities

- `agent_status`: inspect runtime tools, modules, providers, groups and config.
- `approval`: review and resolve the daemon's queued tool calls.
- `ask_user`: interactive terminal input. `ask_owner`: asynchronous escalation.
- `confirm`: session confirmation for high-stakes actions.
- `delegate`: sub-agent execution through the harness protocol.
- `checkpoint`: track and undo session file changes.
- `todo`: provider-backed task state contributed to session context.
- `module_factory`: edits saved manifests. Discovery, trust, activation and
  unload belong to `ModuleLoader`; saved files do not imply live registration.

## Owner questions

`ask_owner` validates through the review gate, enqueues a question and returns
its id immediately. It does not hold the agent loop open or poll for an answer.

Workflow callers use `askOwnerSteps` from `#core/workflow/ask-owner-step.js`:
ask, wait for `owner.question.resolved` matched by question id, then consume the
queue's terminal result and screen its content. The workflow runtime persists
that wait under the run's `awaits/` directory and restores it after restart.
Interactive sessions use `ask_user` for direct input and `ask_owner` for an
answer that may arrive after the current turn ends.

## Autonomy

Every session boundary declares its autonomy mode. `resolveAutonomyGate` runs
before per-tool guardrails:

- `passive`: deny non-safe tools.
- `supervised`: queue non-safe tools for operator approval.
- `autonomous`: apply the configured guardrail policy.

Workflow steps translate mode into neutral harness options (`permissionMode`,
`allowedTools`, `disallowedTools`). Passive mode uses `permissionMode: "default"`
and a read-only tool set because subprocess harnesses cannot see this pipeline.
Autonomous mode leaves the neutral permission mode unset; each adapter owns its
mapping, including Claude's guarded `default` mode. Explicit per-harness
options follow the contract in `src/core/agent-harness/AGENTS.md`.

Only the operator control API changes mode. Session user messages and untrusted
tool/web output cannot escalate it; injection defense screens external content.
The loop reads current mode each tool batch, so changes apply to future calls,
not work already in flight. Per-tool approval does not change session mode.
Clients omitting an explicit mode use `config.serve.defaultAutonomyMode`; other
session boundaries have no hidden compile-time fallback.

## Code execution

Manifest-defined tools declare Python or Node.js code. Core owns
schemas, validation, persistence and conversion to `KotaModule`; executor
modules implement the neutral `CodeRunner` protocol in `code-runner.ts`.
They register on load and deregister on unload. `runCode(language, code,
params, timeoutMs?)` delegates parameter wrapping, timeout defaults and output
truncation to that runner.

Without a registered runner, invocation returns an explicit error. Loading a manifest does not execute it. Core never imports an
executor implementation.
