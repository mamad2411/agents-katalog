# Outbound HTTP

This directory owns the runtime-wide outbound HTTP policy boundary shared by
core protocols and module adapters.

- Every request selects one closed profile from `profiles.ts`; protocol
  adapters keep provider-specific payload and response semantics above this
  boundary.
- Target validation, redirect handling, credential stripping, timeouts,
  response limits, retry classification, redaction, and transport telemetry
  belong here.
- Only `dispatcher.ts` may call the host's global `fetch`. Public-untrusted
  traffic uses the DNS-pinned Node dispatcher instead.
- Keep browser automation out of this boundary. Rendered and authenticated
  browsing remains module-owned by `browser`.
- Inject an `OutboundHttpDispatcher` and resolver for deterministic tests; do
  not add per-consumer fetch hooks.
- Streaming responses stay profile-bounded by default. A long-lived protocol
  stream may select the typed caller-managed mode only when its consumer keeps
  frames and in-progress buffers bounded.
