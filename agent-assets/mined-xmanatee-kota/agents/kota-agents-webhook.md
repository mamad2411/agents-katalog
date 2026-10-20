# Webhook Module

This directory owns:

- The generic inbound HTTP→bus event-trigger surface used by external
  systems (CI, ad-hoc curl, non-GitHub webhooks) to fire a typed bus
  event by name with a JSON payload.
- The signature-validated workflow-trigger surface external systems use
  to fire a specific KOTA workflow with a JSON payload, gated by
  per-workflow HMAC and an in-memory sliding-window rate limit.
- The outbound webhook notification channel that POSTs event payloads
  to configured operator endpoints.
- The CLI commands for managing inbound webhook trigger secrets stored
  in `.kota/config.json`.

## Inbound event-trigger surface

- One route, contributed through `KotaModule.routes`:
  `POST /api/events/:name` with a JSON body.
- The route is bearer-token-protected by the server's standard `/api/*`
  auth — there is no `bypassAuth` here and no per-route signature
  verification. (For HMAC-validated GitHub deliveries, see
  `github-webhook/`. For per-workflow signed triggers, see the
  workflow-trigger surface below.)
- The handler reaches the bus through `ctx.events.emit` rather than
  importing the core event bus directly. The response echoes the event
  name and the current listener count (`listeners`), useful for ad-hoc
  smoke checks of trigger wiring.
- When the event name is `inbound.signal.received`, the route validates the
  payload against the shared inbound-signal contract, injects scope identity and
  receive time from the daemon context, and emits the typed module event. It
  should not interpret or plan the downstream automation.
- Event names are URL-decoded; an event name must be 1–256 characters
  after decoding. Malformed percent-encoding returns 400.

## Signature-validated workflow-trigger surface

- One route, contributed through `KotaModule.controlRoutes`:
  `POST /webhooks/:name` with a JSON body. Path-segment names must
  match `[a-zA-Z0-9_-]+`; anything else returns 404.
- Auth uses the workflow-scoped secret in
  `KotaConfig.webhooks[<name>].secret`. Every delivery must use
  `X-Kota-Webhook-Signature:
  sha256-v2=<hex>` over `<timestamp>.<rawBody>`, plus
  `X-Kota-Webhook-Timestamp` as Unix milliseconds. Missing, tampered, or stale
  timestamps outside the ±5-minute window return 401, as do body-only
  `sha256=<hex>` and bare-hex signatures. The route opts out of daemon Bearer
  auth via `ControlRouteRegistration.bypassAuth: true`.
- Payload threaded through to the workflow run carries `body`, `headers`,
  `timestamp`, and a hashed `idempotencyKey`: `body` is parsed as JSON when the
  raw body is non-empty (falling back to the original string on parse
  failure); `idempotencyKey` comes only from signed body material (a body
  `idempotencyKey`/`externalId`, then the raw body), while unsigned request
  idempotency headers are ignored; `headers` excludes the webhook signature,
  timestamp, raw idempotency-key headers, and common secret-bearing request
  headers; `timestamp` is the daemon's ISO receive time.
- Per-workflow rate limiting is enforced before enqueueing. The
  workflow's `webhookRateLimit.maxPerMinute` (looked up via the
  `workflow-definitions` provider seam) caps deliveries in a sliding
  60-second window owned by this module's in-memory state. Exhaustion
  responds 429 with `Retry-After: <seconds>` and a JSON body
  `{ error, retryAfterSec }`. The window is reset on daemon restart.
- After validation, the handler enqueues the run through the
  `workflow-dispatcher` provider seam's `enqueueWebhookRun(name,
  payload)`. Status codes: `200 { runId }` on success, `404` for
  unknown workflows or workflows without a webhook trigger, `409`
  when the workflow is already running, and `503` when the workflow
  runtime providers are not registered.

## Outbound notifications

- POST event payloads to configured operator endpoints.
- Optional event filters must not suppress urgent owner/approval
  escalation notifications (`approval.requested`,
  `owner.question.asked`).
- Uses `postWithRetry` from the `notification` module for delivery with
  exponential-backoff retry.

## CLI

- `kota webhook list`, `kota webhook secret generate`,
  `kota webhook secret remove` manage inbound webhook trigger secrets
  used by the signature-validated `/webhooks/<workflow>` route.
- These subcommands route through `ctx.client.webhook.<method>()`. The
  shared logic lives in `webhook-operations.ts` so the daemon-control
  routes (`GET /webhooks`, `POST /webhooks/:workflow/secret`,
  `DELETE /webhooks/:workflow/secret`, all under bearer auth) and the
  local-side `localClient` factory cannot diverge on what gets persisted
  to `.kota/config.json`.

## Boundaries

- Owns the generic `POST /api/events/:name` inbound surface. Does not
  own provider-specific inbound webhook receivers — `github-webhook/`
  owns GitHub deliveries; future provider-specific receivers belong in
  their own modules.
- For typed inbound automation signals, this module is only the generic
  adapter. Workflows decide whether a signal creates or updates tasks, captures
  knowledge, asks the owner, replies, retries, audits, or no-ops.
- Owns the signature-validated `POST /webhooks/:name` daemon-control
  route, including timestamp-bound HMAC authentication and the per-workflow
  rate-limit window state. The
  daemon-control core no longer carries a webhook handler.
- Does not own Slack or Telegram notification (those belong in
  `slack/` and `telegram/`) or retry logic (that lives in `notification`).
- Event-trigger tests supply scope identity and event ports to the production
  route. Keep payload rejection and typed-event delivery oracles without
  fabricating a module host.
