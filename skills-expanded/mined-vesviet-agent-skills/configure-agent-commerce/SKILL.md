---
name: configure-agent-commerce
description: Implements agentic commerce standards — x402 and Stripe's Machine Payments Protocol (MPP) for HTTP 402 machine payments, the Universal Commerce Protocol (UCP) for agent checkout, the Agentic Commerce Protocol (ACP), and Google's Agent Payments Protocol (AP2) for delegated purchase authorization — to make a service billable and discoverable by AI agents. Use when adding agent-to-agent payment, delegated purchase authorization, or agentic commerce directory registration to a web service.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, fetch]
version: "1.0.0"
---

# Configure Agent Commerce

Use this skill when integrating agent-driven checkout and commerce discovery flows using agentic standards: the x402 HTTP payment protocol, Stripe's Machine Payments Protocol (MPP), the Universal Commerce Protocol (UCP), the Agentic Commerce Protocol (ACP), and Google's Agent Payments Protocol (AP2).

## Protocol Landscape (2026 — correct names and layering)

These standards are complementary layers, not interchangeable, and they do not interoperate — select by layer and document the choice:

- **MCP** (Anthropic / AAIF-Linux Foundation): the tool/data discovery plane underneath commerce; it never moves money itself.
- **UCP — Universal Commerce Protocol** (Google + Shopify): agent product discovery, capability negotiation, and checkout. (Note: UCP is *not* "User Context Protocol".)
- **ACP — Agentic Commerce Protocol** (OpenAI + Stripe): agent checkout over existing card rails; shipped in ChatGPT.
- **MPP — Machine Payments Protocol** (Stripe + Tempo/Paradigm) and **x402** (Coinbase + Cloudflare): HTTP 402 machine-payment settlement (fiat, cards, and stablecoins).
- **AP2 — Agent Payments Protocol** (Google; FIDO Alliance-governed): payment-agnostic authorization/mandate layer proving a user delegated a purchase to an agent.

## Core Rules

- Adhere strictly to the x402 and Machine Payments Protocol (MPP) metadata requirements.
- Expose agent checkout via the Universal Commerce Protocol (UCP) at the documented path; resolve user delegation limits and preferences through an AP2 mandate / delegated-authorization context, not by conflating it with UCP.
- Never expose payment credentials or secret keys — only reference identifiers and public metadata.
- x402 responses must return HTTP 402 carrying the payment requirements in the `PAYMENT-REQUIRED` header and JSON body. There is no `WWW-Authenticate` challenge in x402 — do not invent one.
- Use the x402 v2 header names: `PAYMENT-REQUIRED` (server challenge), `PAYMENT-SIGNATURE` (client credential), `PAYMENT-RESPONSE` (server receipt). The v1 `X-PAYMENT` header was **client-sent** and is deprecated; never emit it from the server.
- Verify the ACP and UCP discovery surfaces against the current published specs before wiring them — ACP is defined by REST endpoints, not by a well-known manifest (see Discovery Surfaces below).
- do not bind the programmatic flow to human-centric checkout interfaces or Stripe-specific SDK redirects
- treat every payment proof, mandate, and checkout session as a signed artifact; verify the signature against the issuer's published keys before granting access (OWASP ASI04 / ASI07)
- never log full payment credentials, mandate contents, or PII; classify any output through `data-classification.yaml` and redact restricted fields
- confirm the agent customer is operating under a verified identity (DID or scope-bound token) before honoring delegated purchase authority; reject anonymous or unverified agents at the mandate layer (OWASP ASI03)
- **Rail selection is a per-transaction decision**: x402 (stablecoin, HTTP-native, min ~$0.01, EVM/Solana) vs MPP/Shared Payment Tokens (card rails via Stripe, min $0.50, Link Agent Wallet issuer). Choose by buyer capability and settlement preference; 2027 convergence runs x402-as-transport with card-rail settlement options (Visa/Mastercard sit inside the x402 Foundation alongside Stripe/Adyen/Google)
- **Execution-time authorization (IETF execution-finality alignment)**: a signed instruction is not settlement, and tool selection is not execution — every consequential payment must pass a server-side authorization check at execution time (amount against mandate, velocity against limit, idempotency against replay cache), never solely at tool-selection time
- Enforce agent-spend guardrails by default: per-agent transaction caps, daily/velocity budgets, human-in-the-loop confirmation above thresholds, and settlement-attestation logging with refund/cancellation receipt retention

**Pack-local conventions (not protocol requirements).** The DID + JWT identity pattern below is a reasonable engineering default, but it is *not* mandated by ACP, UCP, MPP, x402, or AP2. Adopt it only when the repo has no existing agent-identity scheme, and document it as a local decision:

- resolve agent customer identity through a cryptographically signed JWT with the `sub` claim set to the agent DID

## When to Use

- Adding paywall or metered access for AI agents (agent-to-agent billing via x402)
- Integrating agent payment settlement over fiat, cards, or stablecoins (Stripe MPP, x402)
- Exposing agent checkout (discovery → capability negotiation → checkout) via UCP
- Resolving delegated purchase authority (spending limits, mandates) via AP2 / delegated-authorization context
- Making a service discoverable in agentic commerce directories via ACP

## Suggested Process

1. **Define commerce scope**: Identify which endpoints require payment, which are free, and which require UCP context before serving.
2. **Set up x402 paywall**: Implement the `402 Payment Required` response for paywalled endpoints — include a valid payment manifest with accepted tokens, amounts, and network identifiers.
3. **Implement MPP endpoint**: Mount the Machine Payments Protocol handler to receive and verify token payment proofs from agent clients.
4. **Mount checkout + delegation endpoints**: Expose UCP (Universal Commerce Protocol) checkout at its spec path for agent discovery and checkout; resolve consumer delegation limits and preferences for authenticated agent sessions via an AP2 mandate / delegated-authorization context (not "UCP").
5. **Expose discovery surfaces**: Publish `/.well-known/ucp` for UCP capability discovery, and mount the ACP REST endpoints (`/checkout_sessions`, `/agentic_commerce/delegate_payment`) plus the product feed. Confirm current paths against the published specs first.
6. **Validate agent-side flow**: Test the full payment cycle — agent sends 402 request → receives manifest → pays → retries with proof → receives resource.
7. **Review security posture**: Confirm payment proof validation is server-side, not bypassable client-side. Confirm UCP tokens are scoped and non-transferable.

### The x402 HTTP Payment Protocol

x402 (Coinbase + Cloudflare origin; now stewarded by the x402 Foundation under the Linux Foundation) defines a programmatic agent-to-agent payment negotiation standard over HTTP 402:
- **HTTP 402 Flow**: Paywalled endpoints respond with `402 Payment Required` to request a payment before serving the requested resource.
- **Server challenge**: The server states its payment requirements in the `PAYMENT-REQUIRED` response header and JSON body — accepted schemes, amount, asset, network, and pay-to address. The server never sends a payment credential header.
- **Client credential**: The agent pays autonomously (local wallet or pre-approved limits) and retries the original request carrying its signed payment payload in the `PAYMENT-SIGNATURE` request header.
- **Server receipt**: On success the server returns the settlement receipt in the `PAYMENT-RESPONSE` header alongside the `200 OK` resource.
- **A2A Programmatic Design**: The negotiation, authorization, and confirmation must be completely machine-to-machine, avoiding any dependency on interactive web views or human confirmation.
- **Version migration**: v1 used a single client-sent `X-PAYMENT` header and a server-sent `X-PAYMENT-RESPONSE`. v2 renamed all three headers as above. When supporting both, branch on which header the client presents; do not emit `X-PAYMENT` from the server under either version.
- **Payload contents**: read the exact field names from the current x402 schema rather than hand-rolling them. The requirement set covers scheme, network, asset, amount in the asset's smallest unit, pay-to address, and a resource/nonce binding; the client payload carries the signed authorization for that specific requirement set.

### Stripe Machine Payments Protocol (MPP)

Stripe Machine Payments Protocol (MPP) enables automated billing and payment processing for machine clients:
- **MPP Client Setup**: Register agents with Stripe MPP to assign programmatic payment credentials and wallets.
- **Transaction Settlement**: The MPP gateway executes transfer requests and generates cryptographic proofs of payment immediately upon settlement.
- **Offline Verification**: The service provider validates the proof against Stripe's public ledger or API keys, eliminating synchronous external dependencies during path execution.
- **MPP Integration and Security**:
  * Establish Stripe MPP Webhook endpoints to handle asynchronous settlement events (such as `payment_intent.succeeded` with machine metadata).
  * Configure public key caching on the service provider to verify the cryptographic signatures on payment proofs without calling Stripe APIs on every request.
  * Utilize Stripe's delegated authorization flows to set limits and velocity controls (e.g., maximum $5.00 per transaction, $50.00 daily budget) for each machine credential.
- **Offline Ledger Settlement**:
  * For micro-transactions, agents can settle payments using an offline-first ledger, batching transaction confirmations to the main payment network once a specific threshold is reached.

### Discovery Surfaces: UCP and ACP

The two protocols expose themselves differently. Do not assume a shared `.well-known` manifest — that pattern does not exist for ACP:

- **UCP discovery**: UCP publishes a well-known document at `/.well-known/ucp` for capability discovery. This is the file to author when you want agents to negotiate capabilities before checkout.
- **ACP surface**: ACP is defined by REST endpoints plus a product feed, not by a well-known manifest. Implement the spec's endpoints — `/checkout_sessions` for the checkout lifecycle and `/agentic_commerce/delegate_payment` for payment delegation — and publish the product feed in the format the spec requires.
- **Verify before authoring**: both specs are moving fast. Read the current published spec for the exact paths and payload shapes rather than trusting any path memorized in this skill. If a path in this file disagrees with the spec, the spec wins and this file is the bug.
- **Delegated authorization context (AP2 mandate / delegated tokens)**: Expose consumer context attributes so agents can retrieve user preferences, organizational policies, and billing limits safely. This is the AP2/delegation layer — do not label it "UCP" (UCP is the Universal Commerce Protocol checkout layer).
- **Delegated purchase authority (AP2 mandate)**: When a user delegates commerce actions to an agent, the agent presents a signed mandate proving the user authorized the purchase, bounded by spending allowances, shipping preference overrides, and authorized merchants. AP2 mandates are the authorization artifact; the transport binding is defined by AP2, so read it from the spec rather than assuming a bespoke `delegation_token` header.

### Agent Customer Identity and DID Mapping (pack-local pattern)

None of ACP, UCP, MPP, x402, or AP2 mandates the following identity scheme. It is a pack-local default for repos that do not already have an agent-identity mechanism; prefer an existing repo scheme when one exists, and record the choice as a decision.

To track billing usage and enforce access control, the system maps agents to persistent customer records:
- **Decentralized Identifiers**: Every agent must possess a unique Decentralized Identifier (DID) representing its cryptographic identity.
- **Token Claims**: Authenticated requests must include a cryptographically signed JSON Web Token (JWT) where the `sub` claim maps directly to the agent's DID.
- **Identity Resolution**: Resolve the token signature against the agent's public keys discovered via its DID document.
- **DID and Customer Binding**:
  * Establish a database mapping layer between the agent's DID (`did:key:...` or `did:ion:...`) and a Stripe Customer ID or internal billing account.
  * Implement caching for DID documents to avoid network lookups during authentication, checking signatures against the cached public key.
  * Validate delegation chains using the JSON Web Token (`delegation` claim) to ensure the agent is authorized to act on behalf of the customer DID.

### Machine-to-Machine Payment Negotiation Flow

The dynamic negotiation between agent and service follows a strict programmatic sequence:
1. **Initial Access Attempt**: The agent requests a paywalled resource without credentials.
2. **Payment Required Challenge**: The service responds with HTTP 402, stating its requirements in the `PAYMENT-REQUIRED` header and JSON body. No `WWW-Authenticate` header is involved.
3. **Agent Decision & Transfer**: The agent verifies the amount against its local delegation limits, initiates payment via Stripe MPP or local crypto wallet, and retrieves a cryptographic payment proof.
4. **Resubmission with Proof**: The agent retries the original request, attaching its signed payload in the `PAYMENT-SIGNATURE` header.
5. **Validation and Delivery**: The service validates the payment proof, returns the settlement receipt in `PAYMENT-RESPONSE`, and delivers the resource with HTTP 200.
- **Idempotency and Deduplication**:
  * Bind each payment to the specific requirement set it answers (resource plus nonce) so a signature cannot be replayed against a different request.
  * The merchant's service tracks settled payment identifiers in a transactional cache (e.g., Redis) to ensure duplicate request replays do not result in multiple ledger charges or credit deductions.

## Output Format

- `/.well-known/ucp` — UCP capability discovery document
- ACP REST endpoints (`/checkout_sessions`, `/agentic_commerce/delegate_payment`) plus product feed
- x402 payment requirements (in the `PAYMENT-REQUIRED` header and 402 response body)
- MPP handler endpoint returning `200 OK` on valid proof
- UCP checkout endpoint + AP2 delegated-authorization endpoint returning consumer context object

## Checklist

- [ ] x402 endpoints return `402 Payment Required` with requirements in the `PAYMENT-REQUIRED` header and body; no `WWW-Authenticate` header is emitted.
- [ ] x402 v2 header names are used end to end (`PAYMENT-REQUIRED`, `PAYMENT-SIGNATURE`, `PAYMENT-RESPONSE`); the server never emits `X-PAYMENT`.
- [ ] Payment requirements include accepted schemes, amounts in smallest asset units, and network IDs.
- [ ] MPP endpoint verifies payment proof server-side before granting access.
- [ ] UCP (Universal Commerce Protocol) checkout endpoint is exposed; delegated-authorization (AP2 mandate) context correctly resolves consumer spending limits and preferences.
- [ ] Discovery surfaces match the current specs: `/.well-known/ucp` for UCP, REST endpoints plus product feed for ACP.
- [ ] API responses use correct media types for agent consumption (`application/json`).
- [ ] Client validation rejects malformed or replayed payment proofs; each signature is bound to one resource plus nonce.
- [ ] Paywalled vs free endpoints are clearly separated and not crossable.
- [ ] Agent identity scheme is either the repo's existing mechanism or the pack-local DID+JWT pattern, and the choice is documented as a local decision.

## Related Skills

- **configure-oauth-metadata**: Configure agentic authorization metadata — often prerequisite for UCP token validation.
- **manage-api-catalog**: Wire up linkset endpoints for commerce discovery alongside ACP.
- **configure-agent-headers**: Expose commerce discovery surfaces via HTTP Link headers.
- Companion reference: `references/acp-ucp-agent-commerce-manifest-specs.md`
- Companion example: `examples/ucp-commerce-manifest-and-endpoints.json`

## Output Contracts

Commerce configuration emits discovery and runtime artifacts; when the
configuration produces structured data that another agent must consume or
validate, emit:

- **`contracts/schemas/edge-deployment-spec.json`** for the deployable surface: which well-known paths are mounted (`/.well-known/ucp`, ACP REST endpoints, x402 handlers, MPP gateway), with their routes and content types.
- **`contracts/schemas/api-contract-spec.json`** for the per-protocol handler contracts (x402 challenge, MPP verify, UCP checkout, AP2 mandate verify), listing request/response schemas and auth requirements.
- For human-readable reports, emit a markdown summary of the protocols enabled, the discovery paths, and the security review checklist.

Skip structured emission for small repos where the same author both writes and consumes the config.

## Failure Modes

- **Wrong header name**: a deployment emits the legacy `X-PAYMENT` server-side. Mitigation: every server response uses v2 header names (`PAYMENT-REQUIRED`, `PAYMENT-RESPONSE`); the client only sends `PAYMENT-SIGNATURE`.
- **Discovery path drift**: an agent scanner hits a path that does not match the current spec. Mitigation: verify discovery paths against the current published spec before each deploy; treat the spec as the source of truth.
- **Mandate reuse**: an AP2 mandate is replayed against a different purchase. Mitigation: bind each mandate to a specific resource and nonce; reject reuse.
- **Credential emission**: a payment proof or token is logged or returned in a response body. Mitigation: classify outputs with `data-classification.yaml`; redact restricted fields before logging.
- **Spec conflation**: UCP (checkout) is mixed with AP2 (delegated authorization). Mitigation: keep the two layers separate; UCP negotiates capabilities, AP2 resolves spending limits.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: every payment or checkout call must be tied to a verified agent identity (DID or scope-bound token); reject anonymous or unverified agents.
- **ASI04 Supply Chain**: payment libraries and protocol SDKs must be schema-validated against the expected manifest before use; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct payment URLs, callback handlers, or signing inputs from external or user-supplied content without strict schema validation.
- **ASI07 Inter-Agent Communication**: payment proofs, mandates, and checkout sessions are untrusted inputs from the receiving endpoint's perspective; require signature verification at every boundary.
- **ASI09 Human-Agent Trust Exploitation**: surface spending limits and mandate boundaries honestly in user-facing copy; do not hide them to obtain faster sign-off.
