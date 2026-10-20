# Scope Improver Workflow

Owns scope-local improvement discovery from explicit requests, initial
onboarding, cited systemic handoffs, and material durable guidance or policy changes.

- Read scoped guidance and the machine-owned resolved policy snapshot. Do not
  infer typed domains from directory names or use schedules, failures, or build
  volume as improvement evidence.
- Guidance content reads, including fingerprinting, use the shared anchored
  filesystem boundary. Only scope-relative evidence references without traversal
  select guidance; other citations remain opaque evidence. Links never authorize
  guidance reads. Unsafe reads fail collection before inputs or instruction
  excerpts can be published.
- Resolve scope-improvement posture from authoritative scope policy into the
  module's runtime config. Observe posture converts task proposals into owner
  questions; only build posture permits dispatcher to admit builder work.
- Domain state records consumed and pending semantic fingerprints. It is an
  admission watermark for automatic inputs, not a workflow queue, run owner, or
  repository lock; `RunStateDatabase` owns durable run admission and resources.
- Disabled configuration and task-writer policy denial publish a deferred
  semantic disposition. Dispatcher leaves that fingerprint parked until the
  authoritative configuration or policy fingerprint changes, then redelivers
  it with the next delivery attempt.
- Confirmation-required task-write policy resolves the effective posture to
  observe/ask. It may create an owner question, but neither the review nor its
  isolated writer may create a task file until live authority resolves to allow.
- Explicit requests remain lossless. Consumption records each explicit source
  run independently, so out-of-order completion is distinct from replay.
  Consuming an older request does not authorize replacing a newer disposition
  for the same signature or overriding canonical task state.
  Automatic inputs use their typed latest
  semantic boundary and are rechecked against current guidance at execution.
- Explicit reasons requiring judgment go to progress-reviewer in the consumption
  transaction. Returned systemic handoffs materialize here without another review.
- The review workflow is repository-free, reads the canonical scope root, and
  can therefore observe non-Git directories. Task proposals delegate to the
  `scope-improvement-actions` writer workflow; `RunLifecycle` owns its isolation
  and resources, and `IntegrationQueue` validates and publishes its changes.
  The writer re-resolves enabled state, effective posture, and task-write
  authority from its own live step snapshot before changing the task queue.
- Non-Git observe scopes still compare durable guidance and policy fingerprints
  after onboarding. Git cleanliness gates only repository-writing postures.
- Scope-owned improvement config is a strict boundary. Malformed explicit
  fields park automation; they never inherit permissive defaults.
- Scope improvement is proposal-only for product source. Use normal task
  creation or owner questions; builder implements accepted source changes.
- Artifacts record the trigger, fingerprint, evidence, recommendations, actions,
  and semantic consumption disposition. The original run's success finalizer
  updates the domain watermark and idempotent owner-question effects after
  delegated repository work integrates.
- A systemic handoff keeps its shared topic signature and goes through the
  same posture-aware proposal lifecycle as local guidance candidates. Record the
  handed-off evidence fingerprint with its topic disposition: unchanged evidence
  stays consumed across restart, while new evidence can revise the same proposal.
- Recommendations translate into shared generated-work proposals for repository
  staging and owner-effect publication. The shared lifecycle owns task/question
  disposition; this workflow owns posture authorization and action projection.
- Observe questions publish alongside existing tasks without retiring or
  editing them; semantic freshness still protects consumed requests and newer
  signature observations.
- Semantic freshness gates new owner questions. Integrated task changes retain
  their paired owner effects across delayed publication. Canonical task state
  and the retirement disposition recorded in archived tasks prevent a delayed
  publication from undoing a later disposition.
- Test semantic admission and observable actions without treating the domain
  fingerprint JSON as the run queue or duplicating runtime lifecycle tests.
