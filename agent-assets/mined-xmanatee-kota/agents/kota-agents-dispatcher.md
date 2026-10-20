# Dispatcher Workflow

Runs on `runtime.idle`, assesses repo state, and emits condition-based events.
This is the only autonomy workflow that listens to `runtime.idle`.

Queue shape comes from the shared autonomy queue policy; task eligibility
comes from the repo-tasks work-supply projection, including runtime ownership.
Replenish one capacity-sized queued batch, preserving priority without reserving
the entire backlog ahead of feedback or newly discovered work.
Independent exploration uses a capacity-sized reserve of available tasks;
retained runs and unrelated dependency waits never count as spare supply. Ordinary
steps retain inspection evidence in the run directory. The finalization decision
artifact records staged intents; durable run success/outbox remains publication
authority. Owner-decision
observations use the scoped core repository, never a second JSON reader.

Keep routing decisions semantic: emit events that describe repo conditions, not
which workflow should run next. The event catalog lives in code.

Progress reflection retains a coalesced window of committed task transitions,
agent outcomes and owner decisions until the review revision is consumed.
Comparative outcomes and owner feedback admit assessment even with a delivery
backlog; ordinary delivery-only reflection yields to builders and source growth
alone stays pending. One pending
revision owns the decision until publication or durable output rejection,
including across restart.
Idle reconciliation also releases accepted handoff evidence once its intervention
is terminal, independently of agent-review admission. Shared synchronous finalization
reads fresh consumption, scope and security state, then stages reservations,
evidence receipts and delivery in the success transaction. No long-lived
publication resource protects these rows. Superseded observations preserve current
authority and leave newer evidence for the next ordinary idle inspection.
Generated proposal retirements remain context, not fresh disposition signals.
Compare outcome yield against the last consumed cohort for the same workflow;
recovery can admit review in spare capacity even when success is already known,
while continued healthy outcomes do not repeatedly reuse historical failures.
Automatic and explicit requests remain separate. Scope reflection
compares durable guidance with the authoritative resolved scope-policy
snapshot, never raw scope config. The onboarding reservation owner reconciles eligible pre-existing scopes.
A queued onboarding run re-reads current
inputs instead of adding a replacement; deferred pending input resumes only
after cleanup, and later changes emit through their own latest-only event.
Repository-free observe scopes retain this reflection even when Git inspection
is unavailable; postures that can write remain parked without a clean Git root.
Dispatcher therefore declares `repository: "none"` and reads canonical scope
state. Builder events bind immutable task digests that writers revalidate, and
semantic reservations use runtime-owned compare-and-set state.

Research retry is routed by `autonomy.blocked-research.attemptable`, not by
generic actionable queue availability. Emit it only when blocked research
resources are currently attemptable; missing browser capability and unchanged
retry fingerprints should stay quiet.

Builder dispatch requires the complete resolved scope-policy decision to allow
autonomous repository writes. Observe/ask, proposed-task, disabled improvement,
and denied or confirmation-required builder authority keep tasks visible
without admitting builder runs. Path-bounded policies are evaluated against
their projected writable roots rather than the enclosing scope root.

Security observations publish through revisioned state before their due events.
Observed boundary identity is distinct from completed coverage, so a failed review
or later removal of scanner keywords cannot silently erase outstanding work.
