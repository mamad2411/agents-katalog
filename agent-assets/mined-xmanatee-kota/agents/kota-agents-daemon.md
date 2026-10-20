# Daemon Core

Owns the daemon lifecycle, control plane, sessions, channels, scheduling,
scope hosting, and live state.

## Boundaries

- Autonomous execution belongs in `src/core/workflow/`; process-manager and
  operator CLI behavior belongs in the daemon-ops module.
- Modules extend the control plane through `KotaModule.controlRoutes`. Built-in
  and contributed routes use one `ControlRouteRegistration` table, one matcher,
  and loud collision detection.
- Module routes obtain workflow dispatch, metrics, and definitions through the
  registered provider seams rather than a `DaemonControlHandle`.
- Per-request signed routes may declare `bypassAuth`; other routes use the
  daemon request authorizer's bearer or dashboard-session authentication.
  Dashboard cookies require a request guard for mutations and control-capability
  reads; query tokens do not authenticate daemon requests.
- The shared server-layer route error boundary wraps the entire dispatcher,
  including built-in and contributed routes and protocol-shaped auth denials.
  Authorization and scope selection stay with this host.
- The unauthenticated health route exposes stable component state and timing
  only. Free-form agent and module diagnostics stay on authenticated operator
  or retained runtime-evidence surfaces.
- Clients use typed daemon wrappers for URLs, decoding, authentication,
  polling, and live updates. They never read daemon runtime files directly.
- Health diagnostics are observational; they do not become workflow state or
  control triggers.

## Lifecycle

Normal stop and failed start share `runDaemonShutdown`.

Lifecycle inspection and collection share one serialized, coalescing sweep.
Shutdown drains it before releasing stores. Historical metadata and journal
preparation use the shared blocking-operation worker; recursive sizing and Git
use asynchronous I/O. Retention selects candidates before sizing, and targeted
sweeps measure only their run. Recheck live ownership after asynchronous reads
before destructive effects. Directory reclamation detaches the selected path
before yielding; journal replacement preserves a bounded concurrent append tail
or defers to a later sweep.

Integrated changes to the executing KOTA installation enter the existing restart
drain only after terminal publication is durable. The drain closes global
admission without changing persistent operator pauses or provider backoff. Runtime
revision state retains the requested target through shutdown and startup; readiness
confirms activation for each process after revalidating even previously active
targets against its loaded revision. Built installations retain their build revision and fail
activation visibly if a restart still loads an older build, without retrying that
same target automatically. Workflow recovery remains the owner of queued and held
contracts.

Supervised children borrow an authenticated parent-held instance reservation;
their shutdown removes their control identity while the supervisor retains the
reservation across replacements. Standalone hosts own and release their own lock.

## Capabilities And Identity

Capability readiness comes from typed module-contributed sources. Each stable
capability id reports ready, unavailable, or initialization failure; duplicate
ids and probe exceptions fail loudly. Workflow triggering is daemon-owned and
is reported by the daemon itself.

Client identity combines scope and daemon identity with dashboard readiness.
Clients render dashboard controls only when that typed capability is available.

## Scope Runtime

Scope ids are canonical for both the global root and directory-backed scopes.
Config seeds the registry and `ScopeLifecycleService` mutates it. Persist before
activation, compensate on failure, and recheck live-resource blockers before
removal. Trust and policy changes are atomic; untrust quarantines control work,
aborts workflows, and restarts before repository authority changes.

External directory onboarding uses one `ScopeOnboardingService` inspect/plan/apply
transaction. Prepared runtimes retain validated definitions for readiness but
stay dispatch-closed until scope state and machine authority commit. Retry and
cancel recover incomplete operations without quarantining pre-existing scopes.
Compensation restores unpublished authority while dispatch is closed; it does
not invoke live trust-revocation restart.

Filesystem effects are write-ahead claimed. Runtime-directory creation and
staging use an anchored root descriptor with atomic no-follow, beneath-root
operations; hosts lacking that primitive fail closed. Rollback releases claims
without deleting scope contents. Retry reuses only directories verified by the
accepted operation. Task/inbox directories remain lazily owned by repo-tasks.
Git-backed onboarding accepts repository top-levels because that is the writer
sandbox and publication boundary.

One continuous-improvement posture resolves to existing autonomy and write
policy. Observe is repository-free. Proposals require a Git-backed isolated
writer and allowed task-queue authority. Autonomous builds additionally require
the dispatcher, builder, active harness/provider and allowed writable roots.
Readiness checks the complete selected production chain; optional module setup
gaps remain visible without blocking it. Confirmation or denial stays an
explainable blocker. Already-hosted confirmation-required scopes resolve to
observe behavior.

Routes, typed clients, terminal commands and UI actions use that same service.
Successful onboarding publishes initial improvement through write-ahead intent
and stable dispatch identity, so retries reuse admission. The scope-improvement
authority provider owns live configuration and task/build decisions; disabled
improvement parks activation. Completed operations project later authority
changes without replaying accepted choices. Durable operation migration occurs
at the store boundary and must never widen autonomy or write authority.

Directory-backed store selection belongs to the daemon scope owner. Modules
use its live selector for explicit, active, and default resolution and typed
unknown-scope rejection; store construction and cache lifetimes stay module-owned.
Registered store providers remain bound to their original directory scope;
changing the registry default changes selection, not provider ownership.
Host-bound selectors retain their provider lookup rather than consulting another
host's registry when a provider is absent.

Scope-owned handlers resolve the live runtime through the runtime-scope
provider. Invalid selectors fail without cwd/default fallback. The daemon owns
one runtime module loader; sessions borrow it without replacing its provider or
event authority.

## Decision Record Persistence

Approval and owner-decision repositories share anchored record I/O. That boundary
owns private directory and single-link record identity, canonical ancestor
containment, isolated helper invocation, and file/directory durability. Repository
owners retain their own paths, schemas, signatures, and lifecycle authority.
Filesystem fault and substitution proof belongs to the shared storage owner;
domain tests cover authenticated transitions, replay, and recovery.

## Recoverability

The daemon is authoritative for live state. New state must either reconstruct
from a durable checkpoint after a crash or be explicitly disposable.

Durable state includes:

- daemon lifecycle state and stop reason;
- workflow admission, attempts, resources, processes, external effects, and
  terminal publications in `RunStateDatabase`;
- schedules, approvals, owner decisions, owner questions, and task files;
- conversation history plus daemon chat session bindings; and
- serve-owned session registrations, which re-register after daemon identity
  changes.

Run artifacts are execution evidence, never a second queue. Startup recovery
fences the prior daemon epoch, terminates verified owned processes, releases
attempt resources, and requeues the same run. Ambiguous process ownership puts
the run in `needs_attention` and pauses admission; recovery never broadcasts
synthetic workflow inputs or repairs a shared checkout.

Disposable state includes the live SSE reconnect window, quiet-hours digest
buffer, metric and health caches, subscriptions, and sweep timers. Clients
reconnect, durable event replay comes from the journal, and caches rebuild on
their next read or probe.
