---
name: standard-webhooks
description: >-
  Standard Webhooks 1.0: sign, send and verify webhooks with the webhook-id,
  webhook-timestamp and webhook-signature headers, plus delivery, payload and
  security guidance. Targets the Standard Webhooks 1.0 specification (Version
  1.0.0, repository release v1.0.2). Use when building a webhook producer or a
  receiver, reviewing a webhook handler, or migrating a bespoke webhook scheme:
  the signed content msg_id.timestamp.payload, symmetric HMAC-SHA256 signatures
  (v1, whsec_ secrets), asymmetric ed25519 signatures (v1a, whpk_ and whsk_
  keys), space-delimited multiple signatures for zero-downtime key rotation,
  timestamp tolerance and replay protection, constant-time comparison,
  verifying the raw body, idempotency with webhook-id, retries with exponential
  backoff and jitter, 2xx success, 410 Gone and disabling endpoints, 15 to 30
  second timeouts, retry-after, event types such as user.created, the type,
  timestamp and data payload, thin versus full payloads, SSRF, HTTPS and static
  source IPs.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Standard Webhooks

Standard Webhooks is a community specification, guided by a technical steering committee and published on GitHub, for sending webhooks securely, consistently and interoperably. It fixes the metadata headers, the signature scheme and the secret formats, and recommends payload, delivery and security practices. With this skill the agent builds a producer that signs and delivers webhooks, a consumer that verifies them, or a review of either.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. The specification has no section numbers, so rules cite its heading name (for example "Signature scheme"). Most of the specification is recommendation ("should", "recommended"); the invariants below are the parts a compatible implementation needs. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer (sender), consumer (receiver), or both; or a gateway that verifies on behalf of a consumer.
- Signature scheme: symmetric (`v1`, HMAC-SHA256 with a `whsec_` secret) or asymmetric (`v1a`, ed25519 with `whpk_` and `whsk_` keys), or both.
- Payload format: JSON (recommended) or another content type; thin or full payloads.
- Target version: Standard Webhooks 1.0 (current, the default and only line). No earlier line with different headers exists and no preview is published. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources) (specification text "Version: 1.0.0" at repository tag v1.0.2), unless the user names another.
- Sources refresh: when refreshing this skill or when a rule looks out of date, re-read the specification on `main`, compare it with the pinned tag (`git log -- spec/`), check the releases page for a new tag and the specification's `Version:` line for a new version, and update the pins.

## Invariants

1. **Three headers, exact names.** Send `webhook-id` (the unique message identifier), `webhook-timestamp` (integer Unix seconds of this attempt) and `webhook-signature` with the payload in the body of an HTTP POST (Webhook headers).
2. **Sign `msg_id.timestamp.payload`.** The signed content is the id, the timestamp and the exact body bytes, joined with full stops. The id and timestamp must not be user controlled, or at least must not contain `.` (Signature scheme).
3. **Sign and verify the exact bytes sent.** The body that is sent is the body that was signed; a consumer verifies the raw body, never a re-serialized parse of it (Signature scheme).
4. **Versioned signatures.** Each signature is the identifier, a comma, then the base64 signature: `v1,` for HMAC-SHA256 and `v1a,` for ed25519 (Signature scheme).
5. **Secret formats.** Symmetric secrets are random, 24 to 64 bytes, base64 encoded and shown as `whsec_…`; asymmetric keys are a standard ed25519 key pair, base64 encoded as `whsk_…` (secret) and `whpk_…` (public) (Signature scheme).
6. **The signature header is a space-delimited list.** A consumer accepts the message when any one listed signature verifies; this is how keys rotate with no downtime (Webhook headers).
7. **Constant-time comparison.** Symmetric signatures are compared with a constant-time function; asymmetric ones are checked with a maintained cryptographic library (Verifying signatures).
8. **Timestamp tolerance.** The consumer rejects a `webhook-timestamp` outside an allowed tolerance of its clock, to prevent replay (Verifying signatures).
9. **Trusted keys only.** Consumers keep a trust list of public keys and schemes, and never trust a key read from the request itself (Signature scheme, Additional considerations).
10. **The id is stable across retries; the timestamp is not.** `webhook-id` stays the same for every attempt of one event and serves as the idempotency key; `webhook-timestamp` is updated on each attempt (Webhook metadata).
11. **Only `2xx` is success.** Every other outcome, including `3xx`, timeouts and connection resets, is a failed delivery (Delivery success and failure).

## Workflow

1. **Pick the version.** Use Standard Webhooks 1.0, at the pinned revision.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target is recorded as Standard Webhooks 1.0 and the pinned specification revision.
2. **Choose the scheme and keys.** Pick `v1`, `v1a` or both; generate one key per endpoint (symmetric) or per endpoint or customer (asymmetric); plan key distribution and rotation.
   -> [`references/signing-and-verifying.md`](references/signing-and-verifying.md)
   ✓ Each endpoint has its own secret or key pair in the right serialized format, and consumers have a trust list.
3. **Design the payload.** Define event types (`user.created` style), one schema per type, and a `type`, `timestamp`, `data` body; decide thin or full; keep it small.
   -> [`references/payloads-and-security.md`](references/payloads-and-security.md)
   ✓ Every event type has an example and a formal schema (JSON Schema or OpenAPI), and payloads stay small (usually under 20 kB).
4. **Sign and send** (producer). Build `msg_id.timestamp.payload` from the serialized body, sign with every active key, and send the three headers on a POST.
   -> [`references/signing-and-verifying.md`](references/signing-and-verifying.md)
   ✓ A reference library or a test vector verifies the produced headers against the sent bytes.
5. **Verify** (consumer). Read the raw body, check the timestamp tolerance, recompute or verify each listed signature, compare in constant time, then de-duplicate on `webhook-id` and return `2xx` quickly.
   -> [`references/signing-and-verifying.md`](references/signing-and-verifying.md)
   ✓ A tampered body, a stale timestamp, an unknown key and a replayed id are each rejected or ignored.
6. **Deliver reliably** (producer). Retry failures on a multi-day exponential schedule with jitter, honour `retry-after`, `410`, `429`, `502` and `504`, time out after 15 to 30 seconds, and disable and notify on persistent failure.
   -> [`references/delivery.md`](references/delivery.md)
   ✓ The retry schedule, status handling and disable policy are written down and tested.
7. **Secure the sender.** Route deliveries through an SSRF-filtering proxy in an isolated subnet, prefer HTTPS endpoints, and publish static source IPs if consumers need them.
   -> [`references/payloads-and-security.md`](references/payloads-and-security.md)
   ✓ A webhook URL pointing at an internal or metadata address cannot be reached.
8. **Upgrade** (only when asked). Migrate a bespoke webhook scheme by adding the Standard Webhooks headers next to the existing ones, then optionally migrate payloads.
   -> [`references/versions.md`](references/versions.md)
   ✓ Existing consumers keep working, and a Standard Webhooks library verifies the new headers.

## Verify before done

- [ ] Header names are exactly `webhook-id`, `webhook-timestamp` and `webhook-signature`, and the timestamp is integer seconds (Webhook headers).
- [ ] The signed content is `msg_id.timestamp.payload` over the exact bytes sent; the id and timestamp contain no `.` (Signature scheme).
- [ ] Signatures carry `v1,` or `v1a,`; secrets and keys carry `whsec_`, `whsk_` or `whpk_` (Signature scheme).
- [ ] Consumers verify the raw body, accept any one valid signature in the list, compare in constant time, and enforce a timestamp tolerance (Verifying signatures).
- [ ] `webhook-id` is unchanged across retries and used for de-duplication (Webhook metadata, Verifying signatures).
- [ ] Only `2xx` counts as success; `3xx` is not followed; `410` disables the endpoint (Delivery success and failure).
- [ ] Retries use exponential backoff with jitter; persistent failure disables the endpoint and notifies the owner (Deliverability and reliability).
- [ ] Outbound requests cannot reach internal networks (Server side request forgery).

## Reference index

- **`references/versions.md`**: the Standard Webhooks 1.0 line, how the specification and the library tags relate, editorial history, and migrating from a bespoke scheme. Load for steps 1 and 8.
- **`references/signing-and-verifying.md`**: headers, signed content, `v1` and `v1a`, secret and key formats, multiple signatures and rotation, verification steps, timestamp tolerance, idempotency, reference library behaviour and common mistakes. Load for steps 2, 4 and 5.
- **`references/delivery.md`**: retries and the example schedule, status code handling, `retry-after`, timeouts, disabling endpoints, event-type filtering, fanout, manual replay and endpoint management. Load for step 6.
- **`references/payloads-and-security.md`**: payload structure, event types, thin and full payloads, size, formal schemas (JSON Schema, OpenAPI), SSRF, HTTPS and static IPs. Load for steps 3 and 7.

## Related skills

- `http-message-signatures` for RFC 9421 signatures, a separate general-purpose HTTP signing scheme the Standard Webhooks README lists as a related effort: `npx skills add ScaleDockHQ/scaledock-skills --skill http-message-signatures`.
- `cloudevents` for a common event envelope: `npx skills add ScaleDockHQ/scaledock-skills --skill cloudevents`.
- `asyncapi` for describing event-driven interfaces: `npx skills add ScaleDockHQ/scaledock-skills --skill asyncapi`.
- `openapi` for the formal payload schema and OpenAPI `webhooks` descriptions: `npx skills add ScaleDockHQ/scaledock-skills --skill openapi`.
- `http-semantics` for status codes, `Retry-After` and POST semantics: `npx skills add ScaleDockHQ/scaledock-skills --skill http-semantics`.
- `owasp-api-security` for API7:2023 Server Side Request Forgery: `npx skills add ScaleDockHQ/scaledock-skills --skill owasp-api-security`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Standard Webhooks specification](https://github.com/standard-webhooks/standard-webhooks/blob/v1.0.2/spec/standard-webhooks.md): Specification, "Version: 1.0.0" (the README calls the file the latest draft and the source of truth), at tag v1.0.2 (2026-02-18); text unchanged on `main` since 2025-02-16, checked 2026-10-05.
- [Standard Webhooks README](https://github.com/standard-webhooks/standard-webhooks/blob/main/README.md): Repository README, `main` at 7537d2a (2026-08-31), checked 2026-10-05.
- [Standard Webhooks releases](https://github.com/standard-webhooks/standard-webhooks/releases): Released, v1.0.2 (2026-02-18), latest tag, checked 2026-10-05.
- [Standard Webhooks libraries](https://github.com/standard-webhooks/standard-webhooks/tree/main/libraries): Reference implementations, `main` at 7537d2a (2026-08-31), checked 2026-10-05.
- [Reference JavaScript library source](https://github.com/standard-webhooks/standard-webhooks/blob/main/libraries/javascript/src/index.ts): Reference implementation, `standardwebhooks` 1.1.1 on `main` at 7537d2a, checked 2026-10-05.
- [standardwebhooks.com](https://www.standardwebhooks.com): Project website, checked 2026-10-05.
- [OWASP API Security Top 10, API7:2023 Server Side Request Forgery](https://owasp.org/API-Security/editions/2023/en/0xa7-server-side-request-forgery/): OWASP Top 10, 2023 edition, cited by the specification, checked 2026-10-05.
