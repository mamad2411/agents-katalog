---
name: agent-api-contract-designer
description: >-
  Design secure, contract-first platform APIs for AI agents and machine
  consumers using OpenAPI, tolerant versioning, consumer-driven tests,
  recoverable errors, BFF boundaries, and STRIDE-based threat modeling. Use
  for agent-friendly APIs, OpenAPI review, REST maturity, breaking-change and
  deprecation policy, Pact-style tests, OAuth2 versus API keys, error schemas,
  prompt-injected callers, or an API contract beneath an MCP tool surface.
---

# Agent API Contract Designer

## Purpose
Agents are the highest-volume, lowest-judgment API consumers an organization will ever have: they retry aggressively, parallelize freely, follow documentation literally, and propagate any ambiguity into action. An API that humans tolerate through tribal knowledge will fail agents constantly — and an ADP stands on its platform APIs. This skill produces agent-consumable contracts: explicit, versioned, recoverable, and threat-modeled with the agent on the untrusted side of the boundary. The MCP tool layer (`mcp-platform-api-author`) is only as good as the contract underneath it.

## Core model to hold in your head

### Contract-first, and where on the spectrum
Write the OpenAPI document before the implementation; the spec is the artifact agents' tooling generates clients, validators, and tool schemas from. Contracts live on a **spectrum from strict to loose**:
- Strict (typed schemas, required fields, enums) — certainty and machine-verifiability, tighter coupling.
- Loose (name-value pairs, permissive objects) — maximal decoupling, sacrificed fidelity.
- **For agent consumers, sit strict**: an agent cannot ask a teammate what a field "really" means — the schema is its whole epistemology. Where flexibility is needed, recover fidelity with consumer-driven contracts (below) rather than loosening the schema.
- Avoid **stamp coupling** — passing giant documents where consumers use one field. It bloats agent context windows, widens the blast radius of every schema change, and leaks data the caller shouldn't see: over-fetch is an exposure problem when the caller is an agent that echoes context.

### Richardson maturity as the API maturity scale
Use the ladder as a scoring rubric for existing platform APIs:
- **L0** — one URI, one verb, RPC-over-POST tunneling.
- **L1** — distinct resources/URIs.
- **L2** — HTTP verbs + status codes used correctly: GET safe/cacheable, PUT idempotent, status codes carry meaning agents branch on. **The target for platform APIs.**
- **L3** — hypermedia controls. Optional; well-structured "next actions" in responses deliver most of the agent-facing benefit without full HATEOAS ceremony.

Below L2, agents cannot infer idempotency or retry-safety from the contract, so every recovery decision needs bespoke prompt engineering.

### Versioning for uncoupled consumers
You will not coordinate deploys with your consumers — especially not with agents pinned to cached tool schemas. The discipline:
- **Expansion changes only** within a major version: add endpoints, add optional fields, add enum values (documented as open sets) — never rename, remove, retype, or change semantics.
- **Tolerant reader** as a published consumer obligation: read what you need, ignore unknown fields, don't bind to structure you don't use. State it in the spec so agent client generators comply.
- **Semver the contract**: minor = expansion, major = breaking; run majors side by side (URI or header versioning — pick one, document it) with explicit deprecation windows and sunset headers agents' owners can monitor.
- **Consumer-driven contracts as CI fitness functions**: each consumer (each agent class, the portal, the MCP layer) contributes executable expectations of the fields and behaviors it relies on; the provider's CI runs all of them on every change. This converts "will this break an agent?" from a review-time guess into a build-time fail — loose coupling with governed integration. Register these in `platform-fitness-functions` as holistic, triggered fitness functions.

### Error design for agent recovery
Agents branch on errors mechanically; design the error contract as carefully as the success contract:
- Machine-readable error-code taxonomy (stable strings, enumerated in the spec) with a **retryability class** per code: `retryable_after`, `not_retryable`, `retryable_with_change`, `escalate_to_human`.
- Actionable remediation in-band: which constraint was violated and what a corrected call looks like (`INVALID_GPU_COUNT: max 4 for tier=research; retry with gpus<=4`).
- Correct HTTP semantics: 400-class = fix the request, don't retry as-is; 409 = state conflict, re-read then decide; 429 with `Retry-After` (agents WILL hammer without it); 500-class = backoff and retry idempotent calls only.
- Idempotency keys on all mutating endpoints — agent retries after timeouts are a certainty, not an edge case.
- **Non-leaking**: troubleshootable via error ID + log reference, never via internals (see checklist item 4 below).

### BFF per agent class
The backend-for-frontend pattern, re-aimed: different consumer classes get tailored facades over the same domain services — a portal BFF for humans, and **per-agent-class BFFs** for machine consumers (e.g., an experiment-runner agent BFF exposing job/quota/dataset operations; a CI remediation agent BFF exposing deploy/rollback). Each BFF:
- Trims payloads to what that class needs (anti-stamp-coupling, context-window-friendly).
- Enforces that class's scopes, rate limits, and quotas.
- Versions independently of other consumer classes.

The MCP server for a given agent class (`mcp-platform-api-author`) typically fronts exactly one BFF — the pairing keeps scopes, schemas, and ownership aligned. Don't multiply BFFs beyond real consumer classes with genuinely different needs.

### Security: STRIDE pass + the seven-point API threat checklist
Treat the agent as untrusted — it may be prompt-injected, running a compromised model, or fed poisoned context; its requests are attacker input with valid credentials. Run **STRIDE-per-element** over the API's data-flow diagram (agent → gateway → BFF → services, with a trust boundary at every hop), then apply the seven-point API checklist adapted to agent callers:

| # | Check | Agent-caller adaptation |
|---|---|---|
| 1 | Perform ALL security checks inside the trust boundary | Host-side/tool-schema validation is usability, not security; the server re-validates everything, plus authn/authz/revocation per call |
| 2 | Copy-then-validate (TOCTOU) | Snapshot request payloads before validation; never re-read agent-supplied references (URLs, dataset paths) between check and use |
| 3 | Validate for purpose | Validate against what the field is FOR (a dataset ID resolves AND the caller may read it), not just shape; reject semantic nonsense that schemas pass |
| 4 | Errors enable troubleshooting without giving away secrets | Error ID + log pointer; no connection strings, internal hostnames, other tenants' jobs, or policy internals an attacker can map — agents repeat errors verbatim into logs, PRs, and chats |
| 5 | Document checks performed AND caller obligations | Explicit contract: what the API validates, what the caller must do (tolerant reader, idempotency keys, backoff); undocumented assumptions become agent behavior |
| 6 | Constant-time cryptographic operations | Token/signature comparisons constant-time; agents retry at machine speed, making timing oracles practically exploitable |
| 7 | Handle the API's unique security demands | Agent-specific classes: quota exhaustion via runaway loops (hard per-identity limits), confused deputy via forwarded credentials (claims propagation per `agent-identity-engineer`), data exfiltration via over-broad reads into context |

Auth mechanics: OAuth2 **client credentials** for machine-to-machine (scoped, short-lived, attributable) over static API keys (unscoped, unexpiring, unattributable — acceptable only for low-risk read-only telemetry, if ever). Enforce at the **gateway** (edge: authn, rate limits, quotas, schema validation) and the **mesh** (interior: mTLS, service-to-service policy) — complementary layers, not alternatives.

## Workflow
1. **Inventory and score.** For [YOUR ORGANIZATION / CLIENT], list the platform APIs agents will consume; score each on the Richardson ladder and against the versioning discipline; note current error-contract quality and auth mechanism.
2. **Define consumer classes** (human portal, each agent class, the MCP layer) and decide the BFF topology.
3. **Design contract-first:** OpenAPI per BFF — strict schemas, enums, idempotency keys, error-code taxonomy with retryability classes, documented caller obligations.
4. **Set the versioning policy:** expansion-only rule, semver, deprecation window, side-by-side majors; write it into the spec repo as policy-as-code review gates.
5. **Wire consumer-driven contracts** into provider CI for every consumer class; a failing contract is a failed build.
6. **Threat model:** DFD with trust boundaries, STRIDE-per-element table, then the seven-point checklist with evidence per row; fix or file every gap.
7. **Output.** Contract pack: Richardson scorecard, BFF topology, OpenAPI spec(s) or review deltas, error taxonomy, versioning policy, CDC test plan, and the threat-model table with the seven-point checklist scored.

## Guardrails
- No API ships to agent consumers below Richardson L2 or without a machine-readable error taxonomy — that's the floor, not the goal.
- Never trust client-side or tool-schema validation as a security control; checklist #1 is non-negotiable.
- Breaking changes without a deprecated side-by-side period are defects, even "small" ones — agents don't read announcements.
- Reject stamp-coupled mega-payloads to agent callers; over-fetch is exposure when the consumer echoes context.
- Rate limits and quotas per agent identity are part of the contract, not ops afterthoughts — agents retry at machine speed.
- The security posture assumes a compromised agent with valid credentials; if a design is only safe when the agent behaves, it is not safe.
- Contract design here; credential/identity engineering → `agent-identity-engineer`; the MCP layer above → `mcp-platform-api-author`.

## Suggested effort
Medium-high — scorecard and threat model in a day; a full contract pack for a platform API set is a multi-day artifact.
