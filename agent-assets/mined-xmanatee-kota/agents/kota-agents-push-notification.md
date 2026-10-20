# Push-Notification Module

Owns the entire Expo-push delivery surface for KOTA: the
`<scopeRoot>/.kota/push-tokens.json` store, the `POST /push-tokens`
daemon-control registration route, the Expo Push API HTTP call, and the
bus subscriptions that drive delivery.

The module contributes the route through `KotaModule.controlRoutes`
(`control` capability scope) and subscribes to the bus in `onLoad`,
returning an activation disposer that unsubscribes the exact listeners. The wire contract — JSON body
`{ token, deviceId }`, `400 { error: "Invalid JSON body" }` on parse
failure, `400 { error: "token and deviceId are required" }` on missing
fields, `200 { ok: true }` on success — matches what the mobile client's
`DaemonControlClient.registerPushToken` expects.

## Subscriptions

- `approval.requested` → push payload with stable shared-graph
  `surfaceId: "approvals"` and the matching dynamic approval action id.
  The mobile notification listener resolves both ids against the live bundle.
- `workflow.daily.digest` → push payload `data: { surfaceId: "daily-digest" }` with
  the title `KOTA daily digest` and a short preview drawn from the rendered
  digest text.
- `workflow.attention.digest` → targets the shared `inbox` surface with a
  distinct attention-posture title (`KOTA needs your attention`).

The push payload deliberately does not embed the digest body itself — the
shared surface graph refreshes from the daemon when opened, which
keeps the push under Expo's 4 KB limit and keeps the digest body in one
source of truth.

Quiet-hours suppression lives upstream in the runtime's notification gate;
the push module only sees events that are meant to be delivered.

## Recoverability

`<scopeRoot>/.kota/push-tokens.json` is rewritten on every registration.
Tokens survive daemon crashes; the in-flight Expo Push API call does not
(by design — see below).

The token store owns a versioned decoder and migration from the legacy token
map. Malformed or future-version files produce an explicit store error and are
left unchanged; successful registrations replace the file atomically.

## Delivery Posture

Expo deliveries are intentionally fire-and-forget. SSE is the
authoritative real-time path for clients with the app open; a missed push
is recovered by SSE on next reconnect. We deliberately do not reuse the
`notification` module's `postWithRetry` helper — retrying an Expo failure
would build a queue with no consumer, extend the wake-up path past the
best-effort hint contract, and grow unbounded if a device was uninstalled.
Expo HTTP errors are surfaced through `ctx.log.warn(...)` and dropped.

The same posture applies to the digest delivery path: each emission of
`workflow.daily.digest` or `workflow.attention.digest` produces one fan-out;
no debounce, no retry queue, no persistence beyond the existing tokens
file. The push payload is operator-facing only — neither the body nor the
data field is exposed to autonomy agents.
