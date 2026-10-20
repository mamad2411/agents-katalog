# Server

This directory owns the HTTP server layer plus the typed `KotaClient`
contract every CLI subcommand uses for daemon-or-local access.

## HTTP server scope

- Transport, session, and event-stream infrastructure live here.
- Public HTTP session ids bind to the shared conversation owner before returning
  creation. Cache eviction or host replacement recovers that same scoped owner;
  an unknown resume id never creates a new conversation.
- Both HTTP hosts wrap their production dispatcher in the shared route error
  boundary. Direct routes, contributions, and auth-failure handlers return or
  await request work so synchronous throws and rejections reach that boundary.
  Domain error envelopes and stream lifecycle remain with their handlers.
- Serve owns CORS/preflight and token checks on `/api/`: bearer headers and
  GET query tokens are accepted, while signed routes can bypass host auth.
  Daemon bearer/dashboard policy belongs to the daemon authorizer; shared
  invocation does not make these authority policies interchangeable.
- Capability-specific routes belong in the owning module and are
  contributed through `KotaModule.routes`.
- Do not read `.kota/` files to infer live daemon state when the daemon
  control API can provide it.
- Do not import server session-pool code back into daemon runtime code.

## KotaClient contract

`KotaClient` (generated at `src/client/kota-client.generated.ts`) is the single
typed surface CLI code imports for daemon-or-local access. Its namespace graph
lives in `scripts/daemon-contract-graph.mjs`; namespace interfaces remain with
their domain-owning modules. Two implementors realize it:

- `DaemonControlClient` — talks to a running daemon over the HTTP
  control API.
- `LocalKotaClient` — assembled from per-namespace local handlers
  registered by modules during load.

A single selector (`client-selector.ts`) resolves the active client once
per CLI invocation and stores it in `client-holder.ts`. CLI subcommands
read it through `ModuleContext.client` and never re-decide the
daemon-vs-local policy.

`KotaClient.forScope(scopeId)` is the sole scoping primitive. Namespaces,
handlers, and callers use the same scope terminology; vendor-specific project
concepts stay inside their adapters and never enter this contract.

## Conventions

- Add a namespace interface in its domain owner and register its name, type,
  module import, and transport metadata once in the authored contract graph.
  Regenerate bindings; do not add aggregate fields or assignments by hand.
- The owning module exposes its local handler through a top-level
  `localClient(ctx)` factory on its `KotaModule` definition, returning
  `{ <namespace>: handler }`. The loader always invokes this factory
  during module load — including the CLI's `commandsOnly` path — so
  handler registration does not depend on `onLoad`. The selector
  validates that every namespace has a registered handler when no daemon
  is reachable; missing handlers are a load-time failure with no silent
  fallback.
- The owning module exposes its daemon-side handler through a top-level
  `daemonClient(link)` factory on its `KotaModule` definition, symmetric
  with `localClient(ctx)`. The factory takes the resolved
  `DaemonTransport` (typed link from `daemon-transport.ts`) and returns
  `{ <namespace>: handler }`. The loader registers contributed factories
  during module load; the selector invokes them with the live transport
  and overlays the result on top of the core stub in `daemon-client.ts`.
  A namespace contributed by a module overrides the same namespace in
  the stub. As each namespace migrates to its owning module, its closure
  is removed from the core stub. Missing handlers (no contributor and no
  stub) fail loudly at construction.
- The owning module also contributes any HTTP routes the daemon-side
  client calls (under `KotaModule.routes`). Add routes to the same
  module that owns the underlying state.
- CLI subcommands consume `ctx.client.<namespace>.<method>()`. They must
  not import stores, run direct filesystem reads under `.kota/`, or
  resolve providers from `provider-registry` for capabilities the
  contract already covers.
- Existing daemon HTTP routes (`/api/memory`, `/api/tasks`, `/api/secrets`,
  approvals, workflow runs) are the daemon-side surface. Their request
  and response shapes are part of the public protocol.
- Bootstrap subcommands that legitimately must run before any client is
  resolved — `init`, `registry`, `completion`, `daemon-ops install` —
  are the explicit exception. They may read `.kota/` directly during
  setup. Document the exemption in the owning module's local AGENTS.md
  if a new bootstrap command is added.

## Adding a new namespace

Define one small typed namespace at the client contract, contribute its daemon
and local handlers from the owning module, and migrate callers to that
namespace. Keep request and response types with the contract or domain owner.
Use package boundaries and type completeness as the conformance mechanism;
tests cover distinct daemon/local observable behavior rather than file
placement or namespace catalogs.

## Anti-patterns

- A second public client surface alongside `DaemonControlClient`.
- Per-subcommand "is daemon up?" checks that bypass the selector.
- Local handlers reaching back through HTTP to the same daemon they run
  inside.
- A namespace whose daemon-side and local-side return different data
  shapes — both implementors share one type per method.

## Non-namespace transport surface

Keep raw transport methods private to server bridging that genuinely must
preserve streaming or body semantics. Operator-facing commands and module code
use typed namespaces. Before adding a raw method, prove that it cannot have a
coherent domain owner; if a typed caller later needs it, promote it and remove
the raw path.
