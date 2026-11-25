---
name: vuln-http-smuggling
description: HTTP request smuggling validation — detect CL.TE, TE.CL, TE.TE, and H2.CL desync with timing probes and differential responses; confirm access-control bypass or cache poisoning only with maintainer approval and safe canary traffic.
disable-model-invocation: true
risk: aggressive
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# HTTP request smuggling — desync validation

Use this skill to validate HTTP request smuggling on an authorized, in-scope target. Detect front-end/back-end desynchronization where servers disagree on HTTP request boundaries. Confirm the desync type (CL.TE, TE.CL, TE.TE, H2.CL) using timing probes and differential responses. Do not smuggle requests that poison shared caches, hijack real user sessions, or access other users' data.

## Required inputs

- Written scope naming the target origin, the specific endpoints authorized for smuggling testing, and explicit permission for desync detection. Separate explicit permission required for access-control bypass validation, cache poisoning testing, or session-hijack demonstration — these are outside default smuggling detection scope.
- Valid authorization cache. Aggressive risk class: request smuggling can affect all users sharing the same front-end/back-end connection pool. Testing must be coordinated with the target's operations team.
- A controlled, isolated testing environment. Smuggling tests contaminate the connection pool — other testers or real users may receive queued smuggled responses. Use a dedicated origin or a staging environment when available.
- Known infrastructure: CDN/reverse proxy (Cloudflare, Fastly, Akamai, AWS ALB, Nginx, Varnish, HAProxy) and back-end server (Apache, Nginx, Tomcat, Node.js, Gunicorn, IIS). This determines which desync type to test first.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for execution with aggressive-risk approval — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — infrastructure fingerprinting

Determine which HTTP parsing engine the front-end and back-end use:
1. Send a request with `Transfer-Encoding: chunked` and observe whether it is forwarded or stripped.
2. Send a request with both `Content-Length` and `Transfer-Encoding` headers — which one takes precedence? (Front-end may use CL, back-end may use TE → CL.TE vulnerability.)
3. Check for `Via`, `Server`, `X-Powered-By`, `X-Served-By`, and `CF-Ray` headers to identify proxies.
4. Test HTTP/2 support: does the target accept H2 connections? If so, H2.CL and H2.TE downgrade smuggling may apply.

Record: front-end technology (if identifiable), back-end technology (if identifiable), whether both `Content-Length` and `Transfer-Encoding` are accepted, and HTTP/2 support status.

### Phase 2 — CL.TE detection

CL.TE: front-end uses `Content-Length`, back-end uses `Transfer-Encoding`. The back-end sees the body as chunked, consuming part of the *next* request.

Timing probe:
```http
POST / HTTP/1.1
Host: TARGET
Content-Length: 6
Transfer-Encoding: chunked

3\r\n
abc\r\n
X
```

Explanation: front-end sends a 6-byte body (`3\r\nabc\r\n`). Back-end reads the first chunk (3 bytes: `abc`), then waits for the terminating `0\r\n\r\n` chunk. The trailing `X` is never consumed as part of this request — it hangs waiting. If response time exceeds 10 seconds → CL.TE desync likely.

Repeat 3-5 times against different endpoints to confirm consistency. A single timeout may be a network artifact; repeated timeouts on the same endpoint indicate desync.

### Phase 3 — TE.CL detection

TE.CL: front-end uses `Transfer-Encoding`, back-end uses `Content-Length`. The front-end sends the full chunked body, but the back-end reads only CL bytes.

Timing probe:
```http
POST / HTTP/1.1
Host: TARGET
Content-Length: 3
Transfer-Encoding: chunked

1\r\n
Z\r\n
0\r\n
\r\n
```

Explanation: front-end process the full chunked body (5 bytes of chunk encoding). Back-end reads only 3 bytes (`1\r\n`) and treats the rest as the start of the next request. If the next request to the same connection returns a 400 or unexpected response → TE.CL desync likely.

### Phase 4 — TE.TE obfuscation

When both servers support `Transfer-Encoding` but can be confused via header obfuscation:

```text
Variants to test (one per request):
Transfer-Encoding: xchunked           — unknown TE value
Transfer-Encoding : chunked           — space before colon
Transfer-Encoding: chunked\r\n        — trailing CRLF
Transfer-Encoding: x                  — random short value
Transfer-Encoding:\tchunked           — tab before value
Transfer-Encoding:\n chunked          — newline folding (obsolete)
X: X\r\nTransfer-Encoding: chunked   — header injection via preceding header
```

Send each variant with both `Content-Length` and the obfuscated `Transfer-Encoding`. If one variant produces a timeout or different response → TE.TE desync confirmed.

### Phase 5 — confirmation via differential response

When a desync type is suspected, confirm with a smuggled request that produces a differential response:

**Smuggled request for CL.TE confirmation**:
```http
POST / HTTP/1.1
Host: TARGET
Content-Length: 85
Transfer-Encoding: chunked

0

GET /nonexistent-404-test HTTP/1.1
Host: TARGET
X-Smuggled: true


```

If the next "normal" request to the same connection receives the 404 from the smuggled `GET /nonexistent-404-test` → smuggling confirmed. Use a canary URL that is guaranteed to return a distinctive status code (404, or a specific endpoint that returns a known response).

Rules:
- The smuggled path must be a non-existent or benign canary endpoint — never `/admin`, `/api/users`, or any endpoint that accesses data.
- The `X-Smuggled: true` header serves as a trace marker.
- Immediately stop testing on that connection pool after confirmation. Do not send multiple smuggled requests.

### Phase 6 — impact assessment (requires separate approval)

These impact tests require explicit maintainer approval beyond smuggling detection:

- **Access-control bypass**: smuggle a request to an endpoint the front-end normally blocks. Use a canary test endpoint only — never production admin panels.
- **Cache poisoning**: smuggle a response that the cache stores and serves to other users. Requires cache-deception scope approval.
- **Session hijack demonstration**: smuggle a prefix that captures the next real user's request into a comment/reflection field. Only test in a staging environment with simulated victim traffic.

Without separate approval, document "desync confirmed — further impact assessment requires maintainer approval" and stop.

## Decision points

- **Stop at first confirmed desync**: one clean timing probe or differential response confirming CL.TE, TE.CL, or TE.TE → finding confirmed. Do not enumerate all desync types.
- **Stop at timing probe only**: if desync is confirmed via timing but no differential response is tested (scope limitation), document the desync type with timing evidence.
- **Escalate on access-control bypass**: if a smuggled canary request reaches a blocked endpoint → high severity.
- **Refuse production session hijack**: do not demonstrate session hijacking on production, even with approval — this requires a staging environment.

## Prohibited behavior

- Smuggling requests that access other users' data, admin endpoints, or internal services.
- Smuggling requests that modify server state (POST/PUT/DELETE with side effects).
- Poisoning shared caches — CDN, proxy, or browser — with malicious content.
- Capturing or reflecting real user requests (session hijack on production).
- Overloading the connection pool with repeated smuggled requests — each test request contaminates the pool.
- Using smuggling to bypass IP allowlists, rate limits, or WAF rules protecting internal services.

## Stop conditions

- Timing probe timeout ≥10 seconds on multiple attempts → CL.TE or TE.CL confirmed, stop testing that connection.
- Differential response from smuggled canary request → smuggling confirmed, stop.
- All desync probes return consistent normal responses → no desync detected, negative result.
- Front-end consistently rejects requests with both CL and TE → protected, document.
- WAF/CDN blocks smuggling probes, rate limiting, or detection-team contact.

## Evidence — desync matrix

For each tested endpoint/connection, record:

```text
Target endpoint: <URL>
Front-end: <Cloudflare | AWS ALB | Nginx | unknown>
Back-end: <Apache | Tomcat | Gunicorn | Node.js | unknown>
HTTP/2 support: <yes | no>
CL.TE probe result: <timeout (N seconds) | normal | blocked>
TE.CL probe result: <timeout (N seconds) | 400 | normal | blocked>
TE.TE obfuscation result: <variant that worked | none>
Smuggled canary 404 request: <received by normal req | not received | not tested>
Desync type confirmed: <CL.TE | TE.CL | TE.TE | H2.CL | none>
Impact: <none | desync confirmed | access-control bypass | not assessed>
Confidence: <confirmed | likely | needs-review>
```

Aggregate into a desync-type matrix per front-end/back-end pairing. Include both positive and negative results. Never store: full HTTP request dumps containing session cookies, smuggled-request traces that capture real user data, or canary responses from endpoints that leak internal information.

## Report handoff

When a finding is confirmed:
1. `pentest_agent_record_finding` with affected endpoint, desync type, CVSS estimate (6.5–7.5 for confirmed desync without demonstrated impact, 8.5–9.5 for access-control bypass or cache poisoning), and remediation guidance.
2. Reference the desync matrix.
3. Recommend: normalize HTTP requests at the front-end (reject ambiguous CL/TE combinations), use HTTP/2 end-to-end to avoid downgrade smuggling, configure back-end to reject requests with both CL and TE, disable connection pooling reuse between front-end and back-end if smuggling is being exploited, run desync tests in CI, and apply latest security patches for HTTP parsing engines.
