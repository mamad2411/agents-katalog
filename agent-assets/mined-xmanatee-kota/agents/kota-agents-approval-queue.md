# Approval-Queue Module

Owns the `kota approval` CLI and HTTP surfaces. Core daemon owns the shared
`ApprovalQueue` lifecycle used by the tool-runner and workflow code.

- Provides operator CLI subcommands and
  HTTP route handlers for approvals on both surfaces: the public
  `/api/approvals*` routes contributed via `KotaModule.routes` and the
  daemon-control `/approvals*` routes contributed via
  `KotaModule.controlRoutes`. `routes.ts` is the public module surface; the
  shared handler family and registration wrappers live in focused
  `route-*` siblings so the wire contract stays local without one oversized
  file.
- Route registrations resolve the daemon scope provider through their
  `ModuleContext`; the runtime loader's provider registry is the authority,
  not the legacy process-global registry.
- `supervised` session autonomy is the main producer: the tool-runner queues
  every non-safe tool for this mode regardless of the tool's guardrail policy.
  Operators resolve queued approvals through this module's CLI and routes.
- Approval records have one required kind: executable `tool_call` or
  non-executable `workflow_gate`. Approval routes return a typed resolution
  for either tool execution or gate approval; clients must render that
  resolution instead of inferring execution from a label or optional field.
- Treat scope-local approval storage as an adversarial boundary. The queue
  accepts only daemon-owned real directories and single-link regular records;
  reads are no-follow and status rewrites stay bound to the verified no-follow
  descriptor through mutation and final identity validation. Terminal records
  carry an HMAC from a live queue's daemon-held key. File-backed `get`/`list`
  remain inspection surfaces; code that authorizes workflow continuation or a
  later side effect must use `getWithAuthenticatedResolution`, which fails
  closed on tampering and when a prior daemon lifetime's key is unavailable.
  The live queue also binds each original pending snapshot in daemon-held HMAC
  state; automatic expiry must verify that binding before it can sign a timeout
  resolution. Unverifiable stale records stay pending and are reported as
  blocked; the daemon sweep logs that fail-closed state without terminating
  after pending-file edits or restart.
- Approval events and autonomy mode are orthogonal operator surfaces. Do not
  extend approval endpoints to change a session's mode — mode changes go
  through the daemon control session endpoint (`PATCH /sessions/:id`) owned by
  daemon-ops. A single approval represents a single tool call; a mode change
  affects how future tool calls are gated.
- Local tool-call approvals bind the queue-time registry generation and
  declaration/effect/input/execution-root/target fingerprint. Opaque destinations
  still bind the working directory and scope root. Preflight resolves targets with the
  execution context, rejects drift, and leases the exact definition and runner
  execution must use, even if the mutable registry changes after preflight.
  Local clients and routes select scope authority; each queued local call
  restores its reviewed working directory for both preflight and dispatch.
  Explicit execution-root overrides still undergo fingerprint checks.
- Every local and route execution registers queue-owned activity before async
  preflight and releases it only after tool execution and resource-lease cleanup,
  so scope drain can block on approved work that is no longer pending.

CLI checks consume authored typed client responses and verify review, argument
forwarding, terminal safety, wording, and exit status. They do not simulate a
queue or execute tools. Single and bulk commands share the result renderer;
queue transitions, execution leases, and receipts stay with their owners.

Route checks share only HTTP ports and review-receipt construction. Daemon-control
checks retain the real HTTP registration/authentication boundary; queue filtering
belongs to core, while route checks prove query forwarding and safe projections.
Keep effect and replay observations with the shared approval mutation path;
control-route checks need representative body decoding and dispatch, not another
queue transition or redaction matrix. Client checks own wire decoding and scope
forwarding; typed status catalogs do not need enumeration through every adapter.
MCP and scope-execution scenarios retain their distinct execution and isolation
oracles. Group scenarios by behavior, with fixture lifecycle owned by that suite.
