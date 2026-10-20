# GitHub Webhook Module

This directory owns the GitHub webhook ingestion module — receives GitHub webhook deliveries and emits typed bus events.

- Registers its HTTP route through the module route system and validates each
  delivery's GitHub HMAC signature before emitting normalized bus events.
- Requires a configured secret. The route is not registered when the secret is
  missing.
- Invalid signatures and non-object JSON deliveries are rejected before event
  emission; unrecognized event types are acknowledged and ignored.
- Signature validation uses `timingSafeEqual` to prevent timing attacks.
- Pull-request events and issue-comment mention signals own actor-integrity
  normalization at this boundary. Preserve the distinction between webhook
  authenticity, mention detection, normalized actor trust metadata, and
  downstream prompt-injection labeling.
- Issue-comment mention deliveries map into the shared
  `inbound.signal.received` contract. Keep that adapter thin: authenticate the
  GitHub delivery, normalize scope/source/account/actor metadata, emit the
  typed scope-scoped event, and leave task capture, replies, owner questions,
  retries, and no-op decisions to workflows.
- Pull requests and comments share the actor-trust decision. The adapter supplies
  the actor identity and required provenance; blocked actors take precedence over
  missing metadata and association trust. Emitted mentions preserve the resolved
  trust level for downstream admission.

## GitHub Setup

On GitHub, configure a repository webhook to point at the KOTA-hosted route and
use the same secret as the module config. Keep accepted delivery types and
normalized payload fields in code and tests.

## Boundaries

- Does not own GitHub API calls or PR/issue tools (those belong in `github/`).
- Does not own inbound webhook routing for other services (other webhook modules are separate).
- Does not own outbound HTTP notification delivery (that belongs in `webhook/`).
