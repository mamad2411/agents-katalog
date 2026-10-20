# Inbound Signals Module

This module owns the typed daemon event contract and declarative routing
dispatcher for external platform signals that should wake bounded workflows.

- Adapters authenticate provider traffic, normalize source/account/actor
  metadata, attach scope identity, validate the payload, and emit
  `inbound.signal.received`.
- The module's routing table decides which normalized sources are eligible for
  downstream workflow processing. Workflows decide what an accepted routed
  signal means: task capture or update, memory or knowledge capture, reply,
  owner-question escalation, approval posture, retry, audit, or explicit no-op.
- Keep provider-specific planning out of channel and webhook modules. Provider
  modules may map their native delivery into this contract, but they should not
  decide downstream automation.
- Blocked, archived, or ignored sources still produce routed audit events, but
  the dispatcher does not start processing workflows unless the route explicitly
  opts into dispatching those statuses.
- `inbound.signal.received` and `inbound.signal.routed` are audit events, not
  workflow dispatch paths. The dispatcher admits each configured workflow once
  with the non-emitted `inbound.signal.workflow-targeted` trigger label, so the
  routed audit fact can never dispatch the same work a second time.
- Keep this contract provider-neutral. Provider-specific fields belong inside
  the normalized action payload or in the consuming workflow's parser.
