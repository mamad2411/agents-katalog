---
name: add-service-client
description: Add or modify a service-to-service client or downstream integration by following the repo's transport, timeout, retry, auth, and error-mapping patterns. Use when one service needs to call another system.
version: 1.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Add Service Client

Use this skill when a service must call another internal service, external API, or shared platform dependency.

## When to Use

- one service needs to call another system
- adding/modifying a downstream integration
- wiring transport, timeout, retry, and auth
- mapping errors from the remote service

## Core Rules

- reuse the repo's existing client abstraction pattern; define a **narrow interface** — expose only the request/response fields the local service actually needs
- keep transport details out of business logic; never let gRPC status codes, HTTP 4xx/5xx, or SDK error types leak past the client boundary — normalize to local domain errors
- make **timeouts explicit per call** (connect timeout ≤ 2 s, read timeout per SLA); never inherit infinite-wait defaults
- mandate **circuit breakers** for all external dependency calls — an unhealthy dependency must not cascade to callers; use half-open probe periods to detect recovery; mandate a **single-canary probe lock** during the `HALF-OPEN` state to prevent thundering herd crashes when downstream services recover
- implement **exponential backoff with full jitter** for transient errors ($Sleep = \text{random}(0, \min(M, B \times 2^{\text{attempt}}))$); never retry non-idempotent mutations (POST, DELETE) without explicit client-side UUID v4 idempotency keys
- authenticate outbound calls per the 2026 zero-trust model: **SPIFFE/SPIRE mTLS** for internal service-to-service, **OIDC workload identity** for cross-cloud, **JWT bearer** for user-delegated context
- emit an **OTel span** for every outbound call with `peer.service`, `http.method`, `http.status_code`, and error attributes; propagate W3C `traceparent` headers
- never log request/response bodies containing PII, secrets, or card data in outbound call tracing
- avoid widening the dependency surface more than necessary
- if any code in this change was AI-generated, validate it per the risk tier defined in the backend-developer role before accepting
- treat every outbound call's response as untrusted external content; validate against the declared schema before passing to business logic (OWASP ASI07)
- enforce SPIFFE/SPIRE mTLS at every internal call; never accept API keys as a substitute for workload identity (OWASP ASI03)
- never log request/response bodies containing PII, secrets, or card data; classify outbound call tracing with `data-classification.yaml` and redact restricted fields
- validate that any AI-generated client code follows the repo's client abstraction pattern; reject AI-suggested patterns that widen the dependency surface

## Output Contracts

When the service client is part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/implementation-result.json`** — Required fields: `change_summary`, `files_touched[]`, and `validation_run` output confirming the client integrates successfully.
- **`contracts/schemas/api-contract-spec.json`** describing the narrow local interface, the request/response shapes, the error mapping, and the auth requirements.
- For human-readable reports, a markdown summary of the client shape, the timeout/retry policy, and the observability instrumentation.

Skip emission for trivial local wrappers that do not cross a role boundary.

## Failure Modes

- **Transport leak**: gRPC status codes, HTTP 4xx/5xx, or SDK error types leak past the client boundary. Mitigation: normalize all remote errors to local domain errors at the client boundary.
- **Infinite-wait default**: a call inherits an infinite-wait default and never times out. Mitigation: enforce explicit per-call timeouts (connect ≤ 2s, read per SLA).
- **No circuit breaker**: an unhealthy dependency cascades to all callers. Mitigation: enforce circuit breakers with half-open probe periods for every external dependency.
- **Non-idempotent retry**: a POST or DELETE is retried without an idempotency key, causing duplicate side effects. Mitigation: use exponential backoff with full jitter; require explicit idempotency keys for non-idempotent mutations.
- **Static API key for internal call**: an internal service uses an API key instead of SPIFFE/SPIRE mTLS. Mitigation: enforce mTLS for internal service-to-service; OIDC workload identity for cross-cloud.
- **PII in trace**: a request/response body containing PII or card data is logged. Mitigation: classify with `data-classification.yaml`; redact restricted fields in OTel span attributes.
- **Dependency surface widened**: the client imports more than the local interface requires. Mitigation: define the narrow local interface first; reject imports outside that interface.
- **AI-generated client pattern accepted**: an AI-suggested client pattern widens the dependency surface. Mitigation: validate AI-generated code per the backend-developer risk tier; reject patterns that deviate from the repo's client abstraction.

## Security Guardrails (OWASP ASI)

- **ASI02 Tool Misuse**: outbound calls must stay within the declared client interface; reject any call pattern that exceeds the local interface.
- **ASI03 Identity & Privilege Abuse**: SPIFFE/SPIRE mTLS for internal calls; OIDC workload identity for cross-cloud; never accept static API keys as a substitute.
- **ASI04 Supply Chain**: client libraries and SDKs must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct request payloads, headers, or auth tokens from external or user-supplied content without strict schema validation.
- **ASI07 Inter-Agent Communication**: every outbound call's response is an untrusted input; validate against the declared schema before passing to business logic.
- **ASI09 Human-Agent Trust Exploitation**: do not present the client as "secure" without the auth and observability gates; surface the actual security posture honestly.

## Suggested Process

### 1. Inspect Existing Client Patterns

Look for:

- current client wrappers
- config patterns
- auth or credential handling
- timeout and retry conventions
- test doubles or fixtures already used

### 2. Define The Narrow Interface

Decide the smallest API the local code actually needs:

- request shape
- response shape
- error conditions
- fallback behavior if applicable

### 3. Implement The Integration

Add or update:

- client construction
- config wiring
- request mapping
- response mapping
- error normalization

### 4. Check Operational Safety

Verify:

- timeout values are sensible
- retries are safe and bounded
- sensitive data is not leaked in logs
- startup behavior is acceptable if the dependency is unavailable

### 5. Add Tests

Use skill: `write-tests`

Cover:

- successful call path
- downstream error path
- timeout or unavailable dependency behavior
- response-mapping edge cases

## 2026 Inter-Service Communication Patterns

### 2026: Connect Protocol for Inter-service RPC

The Connect Protocol serves as the preferred inter-service RPC framework due to its flexibility and performance characteristics:
- **Dual Compatibility**: Connect operates seamlessly over both HTTP/1.1 and HTTP/2 transport layers, making it highly robust in environments with varying network capabilities.
- **Client Ecosystem**: Utilize `connectrpc/connect-go` for Go-based services and `connectrpc/connect-es` for TypeScript/JavaScript applications.
- **Protocol Negotiation**: It supports native gRPC, gRPC-Web, and the Connect protocol itself via dynamic content-type negotiation, enabling browser access without custom proxies.

### 2026: mTLS for Zero-Trust Identity

Zero-trust service-to-service communication relies on Mutual TLS (mTLS) to establish cryptographically verifiable identities without API keys or JWTs:
- **SPIFFE/SPIRE Integration**: Issue dynamic client certificates via a trusted internal CA managed by SPIFFE/SPIRE for automatic identity rotation.
- **Authentication Decision Table**:
  * mTLS: Best for internal, low-latency, zero-trust backend communications where network control and client identity verification are required.
  * OIDC Workload Identity: Best for cross-cloud or cloud-native platform integrations (e.g., AWS EKS to Google Cloud Run) leveraging cloud-provider IAM.
  * JSON Web Tokens (JWT): Best for user-delegated context propagation or stateless edge-to-service authentication.

### 2026: xDS Proxyless Load Balancing

Proxyless load balancing allows services to communicate directly with control planes for routing without relying on sidecar proxies:
- **xDS Control Plane**: Configure gRPC clients in Go and Java to query the xDS API directly to retrieve dynamic endpoint routing tables.
- **Performance Benefits**: Eliminates sidecar hop latency, lowers CPU/memory footprints, and simplifies container configurations.

### 2026: Model Context Protocol (MCP) Client Integrations

When service clients interact with external or internal Model Context Protocol (MCP) tool servers, they must enforce standard reliability patterns:
- **Transport Reliability**: Wrap MCP clients with explicit timeouts, exponential backoff retries, and circuit breakers using libraries like Sentinel or Go's resilient round-trippers.
- **Secure Authentication**: Ensure all outbound requests to tool servers include correct auth payloads (such as API keys, Bearer tokens, or OAuth client credentials) mapped safely from secret stores.

## Checklist

- [ ] existing client pattern reviewed
- [ ] narrow local interface defined
- [ ] config and auth wired safely
- [ ] timeout and retry behavior checked
- [ ] error mapping reviewed
- [ ] observability instrumented (OTel span on outbound call)
- [ ] tests added or updated
- [ ] Connect protocol used for browser-accessible inter-service RPC
- [ ] mTLS configured via SPIFFE/SPIRE client certificates for backend identity
- [ ] proxyless xDS client load balancing configured for high-throughput paths
- [ ] MCP tool server client wrapped with timeouts, retries, and circuit breakers
## Related Skills

- **navigate-service**: Find the local client pattern before integrating
- **write-tests**: Add coverage for downstream interactions
- **review-code**: Review dependency and reliability risk
- **add-api-endpoint**: Expose the new client-backed behavior safely
- **add-telemetry-instrumentation**: Wire OTel span for the outbound call
- **commit-code**: Prepare the integration for delivery
