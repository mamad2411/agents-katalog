---
name: cloudflare-stream
description: Design, implement, review, or troubleshoot Cloudflare Stream video-on-demand and live-video integrations, including uploads, playback, access control, webhooks, analytics, operations, limits, pricing, and product trade-offs. Use for Cloudflare Stream work; do not use for generic Cloudflare CDN, R2, Images, or Media Transformations tasks that do not involve Stream.
metadata:
  author: code-dimension
  version: 1.0
---

# Cloudflare Stream

Build the smallest Stream integration that satisfies the product contract. Treat Stream as an asynchronous managed video pipeline: the application owns authorization and business metadata; Cloudflare owns ingestion, encoding, storage, and delivery.

## Before changing code

1. Inspect the repository's existing Cloudflare client, configuration, domain model, webhook handling, player, and tests before adding anything.
2. Identify the actual mode: on-demand upload, direct creator upload, playback, live, analytics, or lifecycle operations.
3. Fetch current Cloudflare Stream documentation through Context7 before relying on endpoint schemas, limits, pricing, beta status, or SDK syntax. Prefer the [official Stream docs](https://developers.cloudflare.com/stream/) and [API reference](https://developers.cloudflare.com/api/resources/stream/). Never invent an endpoint or field.
4. Read only the references needed for the task:
   - Product fit and architecture: [decision-guide.md](references/decision-guide.md)
   - Authentication, API conventions, and video lifecycle: [api-lifecycle.md](references/api-lifecycle.md)
   - Uploads and media preparation: [uploads.md](references/uploads.md)
   - Playback, privacy, captions, and downloads: [playback-security.md](references/playback-security.md)
   - Live streaming: [live.md](references/live.md)
   - Webhooks, analytics, costs, limits, and operations: [operations.md](references/operations.md)

## Non-negotiable boundaries

- Keep API tokens, signing keys, webhook secrets, live input keys, and account identifiers needed for privileged operations on trusted server infrastructure. Never return them to a browser or mobile client.
- For user uploads, issue a constrained, expiring Direct Creator Upload URL from the backend; upload media directly from the client to Stream.
- Treat upload acceptance as pending, not success. Persist the Stream video UID, then transition business state from a verified webhook or explicit status reconciliation.
- Verify webhook signatures against the untouched raw body, reject stale timestamps, use constant-time comparison, and make processing idempotent.
- Require signed URLs for private or paid content. `allowedOrigins` is defense in depth against embedding, not viewer authorization.
- Use short-lived playback tokens and authorize each issuance against the application's current user/resource policy. Never log tokens or place them in durable storage.
- Handle deletion deliberately: remove or tombstone the application record and Stream asset consistently; design retries so partial failure is recoverable.
- Do not promise DRM, forensic watermarking, guaranteed prevention of screen capture, frame-accurate editing, arbitrary rendition control, or permanent source-file archival unless a separately verified product capability provides it.

## Implementation shape

- Reuse the installed Cloudflare SDK when it already covers the required API; otherwise use the REST API with one small server-side adapter. Do not add a second Cloudflare client abstraction.
- Store Stream identifiers and business metadata in the application's database. Do not use Stream `meta` as the system of record.
- Model only states the product needs, mapping Cloudflare's richer processing status at the integration boundary.
- Prefer the built-in player for the least maintenance. Use HLS/DASH with a custom player only for requirements the built-in player cannot satisfy.
- Add one focused runnable check for each non-trivial flow: upload provisioning constraints, webhook signature/idempotency, playback authorization, or live key handling.

## Completion evidence

Report the selected upload/playback mode, security controls, asynchronous state transition, cleanup behavior, verified docs date, and checks run. Separate locally verified behavior from actions that require a real Cloudflare account.
