---
name: machine-payments-protocol
description: >-
  Machine Payments Protocol (MPP): add and consume HTTP 402 payments with the "Payment" HTTP
  authentication scheme of draft-httpauth-payment-01 (individual Internet-Draft, build posture):
  WWW-Authenticate Payment challenges with id, realm, method, intent and request, HMAC challenge
  binding over JCS-serialized requests, Authorization or Payment-Authorization credentials,
  Payment-Receipt receipts, Accept-Payment negotiation, RFC 9457 problem types and 402 versus 401
  and 403. Covers the charge and subscription intents, method-defined session intents, OpenAPI
  price discovery (x-payment-info), the JSON-RPC and MCP transport (-32042) and reconciliation. Use when an API, MCP server or agent must
  charge per request, meter usage or bill a subscription over HTTP 402, or pay such a service as
  a client. Triggers: MPP, Machine Payments Protocol, Payment auth scheme, paymentauth,
  Payment-Receipt, Accept-Payment, mppx, Tempo, Stripe machine payments, agent payments, HTTP 402.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Machine Payments Protocol (MPP)

The Machine Payments Protocol, co-authored by Tempo and Stripe and launched on 18 March 2026, gives HTTP 402 Payment Required concrete semantics through the "Payment" HTTP authentication scheme. A server answers an unpaid request with 402 and one or more `WWW-Authenticate: Payment` challenges; the client pays with a registered payment method, retries with a Payment credential, and gets the resource with a `Payment-Receipt`. The core is the Internet-Draft `draft-httpauth-payment`; intents, discovery, transports and payment methods are companion specifications published on paymentauth.org. With this skill the agent builds a paying client or a charging server.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. "core §" refers to `draft-httpauth-payment-01`, "charge §" to `draft-payment-intent-charge-00`, "subscription §" to `draft-payment-intent-subscription-00`, "discovery §" to `draft-payment-discovery-01` and "mcp §" to `draft-payment-transport-mcp-00`. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

Draft posture: **build**. The core is a complete individual Internet-Draft with registries, security considerations and production SDKs; implement the pinned revision exactly. It is not adopted by an IETF working group, and the companion intent, discovery and transport documents are published only on paymentauth.org, so re-check both before relying on a field.

## Inputs (fill in, or ask before starting)

- Role: server (resource that charges), client (agent or app that pays), or both.
- Intent: `charge` (one-time), `subscription` (fixed amount per period), or a method-defined `session` (metered pay-as-you-go).
- Payment methods: the registered method identifiers to offer or accept (for example `tempo`, `stripe`, `lightning`), each with its own method specification.
- Transport: plain HTTP, or JSON-RPC and MCP (`tools/call`, `resources/read`, `prompts/get`).
- Authentication: whether the resource also needs ordinary authentication in `Authorization`, which decides the `header` parameter.
- Discovery: whether to publish an OpenAPI document with `x-payment-info`.
- Target version: draft-httpauth-payment-01 (default, posture build: implement it). No other line exists; earlier revisions are compatible predecessors, not lines. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revisions in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources), check the datatracker page for a newer revision, WG adoption or replacement, check paymentauth.org and the `mpp-specs` repository for new intent, discovery or transport revisions, and update the pins.

## Invariants

1. **402 always carries a Payment challenge.** A server MUST NOT return 402 without at least one `WWW-Authenticate: Payment` challenge, and every payment failure (malformed, unknown, used, expired or unverifiable credential) returns 402 with a fresh challenge (core § 4.2, § 4.4.2). 401 is for authentication failures unrelated to payment; 403 means payment verified but policy denies access (core § 4.3).
2. **A challenge has `id`, `realm`, `method`, `intent` and `request`.** `id` is non-empty, `method` is lowercase letters, `intent` is registered, and `request` is base64url without padding of JCS-serialized JSON (core § 5.1.1, § 6.1; RFC 8785).
3. **The `id` binds the challenge.** Servers MUST bind `id` to realm, method, intent and request, plus expires, digest, opaque and header when present, and MUST reject a credential whose echoed parameters do not match; the recommended binding is HMAC-SHA256 over seven fixed pipe-joined slots, with an eighth only when `header` is present (core § 5.1.2.1, § 5.1.2.1.1).
4. **The credential goes in the field the challenge selects.** No `header` parameter means `Authorization: Payment <base64url JSON>`; `header="Payment-Authorization"` means that field and no other. A credential in any other field MUST NOT satisfy the challenge (core § 5.1.2, § 5.2).
5. **The credential echoes the challenge unchanged** in its `challenge` object, adds a method-specific `payload`, and MAY add `source` (a DID is recommended) (core § 5.2).
6. **Receipts only on success.** `Payment-Receipt` is base64url JSON with `status` `"success"`, `method`, `timestamp` and `reference`, and MUST NOT appear on error responses (core § 5.3, § 5.3.1).
7. **Proofs are single-use and settlement is atomic.** Each credential works once per challenge; concurrent use yields at most one settlement and one delivery; no side effects before payment; a charge gives no partial access, including streamed bytes or started tool calls (core § 11.3 to § 11.5; charge § 4.4, § 6.2).
8. **Clients verify before paying.** Amount, recipient, currency and validity window, never the `description` (core § 11.6; charge § 8.1, § 8.2). The 402 challenge is authoritative over `Accept-Payment` preferences and discovery metadata (core § 7.4; discovery § 5).
9. **Caching and secrecy.** 402 responses carry `Cache-Control: no-store`; receipt responses carry `private`; responses to `Payment-Authorization` requests carry `private` or `no-store`; credentials, receipts and the binding secret are never logged (core § 11.2.1, § 11.2.2, § 11.8, § 11.10).
10. **TLS only.** No challenges or credentials over unencrypted HTTP; TLS 1.2 or later, 1.3 recommended (core § 11.2).
11. **No accounts required.** Servers MUST NOT require user accounts for payment (core § 11.7).

## Workflow

1. **Pick the version and parts.** Use draft-httpauth-payment-01 with the companion revisions in Sources; list the intents and payment methods in scope.
   -> [`references/versions.md`](references/versions.md)
   ✓ Every document the integration relies on is pinned, and each method identifier has a method specification.
2. **Design the challenge** (server). Choose the intent's request fields (amount in base units as a string, currency, recipient, `externalId`, `methodDetails`), `expires`, `digest` for bodies, `opaque` for processor correlation, and `header` if `Authorization` is taken (core § 5.1; charge § 5).
   -> [`references/protocol.md`](references/protocol.md)
   ✓ The request JSON is JCS-serialized, base64url without padding, and the challenge stays under 8 KB (core § 9.4).
3. **Bind and issue** (server). Compute `id` (HMAC-SHA256 over the slot string, or stateful storage), send 402 with one challenge per method and intent offered, `Cache-Control: no-store` and an RFC 9457 problem body (core § 5.1.2.1.1, § 7.3, § 8.1).
   -> [`references/protocol.md`](references/protocol.md)
   ✓ Recomputing the binding from the echoed parameters reproduces `id`; changing any bound field breaks it.
4. **Negotiate and pay** (client). Optionally send `Accept-Payment`; parse every Payment challenge, drop unknown intents and unsupported `header` values, verify amount, recipient, currency and expiry, pay with the method, and send exactly one credential in the selected field (core § 5.2, § 7.3, § 7.4, § 11.6, Appendix B.4).
   -> [`references/protocol.md`](references/protocol.md)
   ✓ The client never pays an expired challenge, never trusts `description`, and never sends two credentials.
5. **Verify and settle** (server). Check the binding, expiry, body digest and single use; verify the proof, amount and recipient with the method; settle atomically; then respond 200 with `Payment-Receipt` and `Cache-Control: private` (core § 5.1.3, § 11.5, § 11.10; charge § 7).
   -> [`references/protocol.md`](references/protocol.md)
   ✓ Parallel replays of one credential produce one settlement; failures return 402 with a fresh challenge and the right problem type.
6. **Add intents, discovery and transports.** Implement subscription lifecycle state, a method's session intent, `/openapi.json` with `x-payment-info`, or the JSON-RPC/MCP mapping as needed (subscription § 7; discovery § 4; mcp § 6 to § 8).
   -> [`references/intents-and-discovery.md`](references/intents-and-discovery.md)
   ✓ Subscriptions charge at most once per period and never accumulate missed periods; discovery prices match the runtime 402.
7. **Reconcile.** Record `externalId`, `opaque`, the challenge `id`, the receipt `reference` and the subscription identifier so every settlement maps back to an order (charge § 5.1.2; core § 5.1.2, § 5.3; subscription § 7.3).
   -> [`references/intents-and-discovery.md`](references/intents-and-discovery.md)
   ✓ Each receipt joins to exactly one order or billing period.
8. **Review security.** Rate limits, secret rotation, idempotency keys for non-idempotent methods, intermediary handling of 402, and explicit user confirmation in browser wallets (core § 11.2.2, § 11.4, § 11.9, § 11.11, § 11.12).
   -> [`references/protocol.md`](references/protocol.md)
   ✓ No log, error or analytics path contains a credential, receipt or binding secret.

## Verify before done

- [ ] Every 402 has at least one `WWW-Authenticate: Payment` challenge with non-empty `id`, `realm`, lowercase `method`, registered `intent` and JCS base64url `request` (core § 4.4.2, § 5.1.1).
- [ ] The server rejects a credential whose echoed challenge differs from the binding, and one sent in a field the challenge did not select (core § 5.1.2.1, § 5.2).
- [ ] Malformed, unknown, used, expired and failed credentials each return 402, a fresh challenge and the matching problem type (core § 4.2, § 8.2).
- [ ] Receipts appear only on 2xx, with `status` `"success"` (core § 5.3.1).
- [ ] `Cache-Control` is `no-store` on 402 and `private` on receipts (core § 11.10).
- [ ] Amounts are base-unit integer strings and the client checks amount, recipient, currency and expiry before paying (charge § 5.1.1; core § 11.6).
- [ ] No side effect, partial body or stream byte is produced before payment verifies (core § 11.4; charge § 4.4).
- [ ] Discovery and capability advertisement are treated as hints; the runtime challenge wins (discovery § 5; mcp § 5).

## Reference index

- **`references/versions.md`**: the single current line, the draft lineage from `draft-ryan-httpauth-payment-00`, what each revision added, and the posture. Load for step 1.
- **`references/protocol.md`**: status codes, challenge parameters, the HMAC binding slots, credential and receipt formats, `Accept-Payment`, problem types, versioning rules, and security and caching. Load for steps 2 to 5 and 8.
- **`references/intents-and-discovery.md`**: the charge and subscription intents, session intents, OpenAPI discovery, the JSON-RPC and MCP transport, reconciliation fields, and how MPP relates to x402. Load for steps 6 and 7.

## Related skills

- `x402` for the other HTTP 402 payment protocol for agents, with its own headers and facilitator model: `npx skills add ScaleDockHQ/scaledock-skills --skill x402`.
- `mcp` for the Model Context Protocol that the MCP transport extends: `npx skills add ScaleDockHQ/scaledock-skills --skill mcp`.
- `problem-details` for RFC 9457 error bodies: `npx skills add ScaleDockHQ/scaledock-skills --skill problem-details`.
- `json-canonicalization` for RFC 8785 JCS, used for `request` and `opaque`: `npx skills add ScaleDockHQ/scaledock-skills --skill json-canonicalization`.
- `openapi` for the discovery document: `npx skills add ScaleDockHQ/scaledock-skills --skill openapi`.
- `ap2` for agent payment mandates, a different layer of agent commerce: `npx skills add ScaleDockHQ/scaledock-skills --skill ap2`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [draft-httpauth-payment-01: The "Payment" HTTP Authentication Scheme](https://www.ietf.org/archive/id/draft-httpauth-payment-01.txt): individual Internet-Draft (no working group), intended Standards Track, -01 (9 September 2026), posture build, checked 2026-10-09.
- [draft-httpauth-payment datatracker page](https://datatracker.ietf.org/doc/draft-httpauth-payment/): Active, I-D Exists, latest revision -01, expires 13 March 2027, checked 2026-10-09.
- Earlier core revisions, compared while writing: [draft-httpauth-payment-00](https://www.ietf.org/archive/id/draft-httpauth-payment-00.txt) (19 June 2026), [draft-ryan-httpauth-payment-01](https://www.ietf.org/archive/id/draft-ryan-httpauth-payment-01.txt) (18 March 2026) and [draft-ryan-httpauth-payment-00](https://www.ietf.org/archive/id/draft-ryan-httpauth-payment-00.txt) (15 February 2026): individual drafts, superseded, checked 2026-10-09.
- [Machine Payments Protocol Specifications (paymentauth.org)](https://paymentauth.org): specification index generated from `tempoxyz/mpp-specs`, build of commit 50309c8 (5 October 2026), checked 2026-10-09.
- [draft-payment-intent-charge-00: Charge Intent for HTTP Payment Authentication](https://paymentauth.org/draft-payment-intent-charge-00.txt): Internet-Draft format, intended Informational, published on paymentauth.org only, -00 (5 October 2026), checked 2026-10-09.
- [draft-payment-intent-subscription-00: Subscription Intent for HTTP Payment Authentication](https://paymentauth.org/draft-payment-intent-subscription-00.txt): Internet-Draft format, intended Informational, published on paymentauth.org only, -00 (5 October 2026), checked 2026-10-09.
- [draft-payment-discovery-01: Service Discovery for HTTP Payment Authentication](https://paymentauth.org/draft-payment-discovery-01.txt): Internet-Draft format, intended Informational, published on paymentauth.org only, -01 (5 October 2026), checked 2026-10-09.
- [draft-payment-transport-mcp-00: Payment Authentication Scheme: JSON-RPC & MCP Transport](https://paymentauth.org/draft-payment-transport-mcp-00.txt): Internet-Draft format, intended Informational, published on paymentauth.org only, -00 (5 October 2026), checked 2026-10-09.
- [draft-tempo-session-00: Tempo Session Intent for HTTP Payment Authentication](https://paymentauth.org/draft-tempo-session-00.txt): payment method specification, intended Informational, -00 (5 October 2026), read for the session intent only, checked 2026-10-09.
- [tempoxyz/mpp-specs](https://github.com/tempoxyz/mpp-specs): specification source repository, commit 50309c8e (5 October 2026), checked 2026-10-09.
- [Machine Payments Protocol documentation (mpp.dev)](https://mpp.dev/): protocol site with overview, governance and the x402 comparison, informative, checked 2026-10-09.
- [Introducing the Machine Payments Protocol](https://stripe.com/blog/machine-payments-protocol): Stripe announcement, 18 March 2026, informative, checked 2026-10-09.
- [Stripe docs: Accept machine payments with MPP](https://docs.stripe.com/payments/machine/mpp): vendor documentation, informative, checked 2026-10-09.
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110): RFC (Internet Standard), STD 97, checked 2026-10-09.
- [RFC 8785: JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785): RFC (Informational), RFC 8785, checked 2026-10-09.
- [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457): RFC (Proposed Standard), RFC 9457, checked 2026-10-09.
