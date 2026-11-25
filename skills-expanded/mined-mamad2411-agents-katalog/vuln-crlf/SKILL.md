---
name: vuln-crlf
description: CRLF injection validation — test HTTP header injection, response splitting, and cookie injection via carriage-return/line-feed sequences without poisoning caches or hijacking real user sessions.
disable-model-invocation: true
risk: caution
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# CRLF injection — HTTP header-splitting validation

Use this skill to validate CRLF (`\r\n`) injection on an authorized, in-scope target. Confirm that user input reaching HTTP response headers allows header injection, response splitting, or cookie manipulation. Focus on injectable parameters — URL redirect targets, query parameters reflected in headers, and request-header values echoed in responses. All tests use benign injected headers with engagement-specific markers; never deploy header injections that affect real users.

## Required inputs

- Written scope naming the target origin, authorized injection parameters (redirect URLs, callback URLs, filename headers, custom header echo endpoints), and explicit permission for CRLF testing.
- Valid authorization cache. Caution risk class: header injection can affect caching intermediaries and downstream consumers — ensure the testing window is coordinated.
- Engagement-specific marker string (e.g., `X-Pentest-Marker: <engagement-id>`) for all injected headers. This makes injected headers distinguishable from production traffic.
- Known CDN, reverse proxy, or WAF in front of the target — these may normalize or strip CRLF sequences.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview when catalog tools are useful.
5. `pentest_agent_execute_tool` for execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — parameter surface mapping

Identify all parameters that might be reflected in HTTP response headers:
- **Redirect parameters**: `?redirect=`, `?url=`, `?next=`, `?return=`, `?callback=`, `?goto=`, `?continue=`, `?target=`.
- **Filename parameters**: `?file=`, `?filename=`, `?download=`, `?attachment=`. These often influence `Content-Disposition` headers.
- **Content-type parameters**: `?format=`, `?type=`, `?output=`. These may influence `Content-Type` headers.
- **Custom header echo**: any endpoint that takes a value and returns it in a response header (e.g., `X-Request-ID` echo, language negotiation).
- **Cookie-setting endpoints**: login, session create, tracking, or analytics endpoints that set cookies based on user input.

For each parameter, record the endpoint, the affected header (if known), and the reflection context (full header value, partial, or attribute).

### Phase 2 — basic CRLF detection

Test whether `\r\n` sequences are passed through to the response:

```text
Marker: X-Pentest-CRLF: <engagement-id>

URL-encoded CRLF sequences:
%0d%0aX-Pentest-CRLF: <engagement-id>       — CRLF + injected header
%0aX-Pentest-CRLF: <engagement-id>          — LF only (some platforms accept bare LF)
%0dX-Pentest-CRLF: <engagement-id>          — CR only (rare, mainly legacy Mac)
```

For each parameter:
1. Append each CRLF sequence with the marker header.
2. Inspect the raw response headers (use `curl -sI` or equivalent with verbose output).
3. If `X-Pentest-CRLF: <engagement-id>` appears as a distinct header in the response → CRLF injection confirmed.
4. If the injected header appears concatenated or partially escaped, record the transformation.

### Phase 3 — response splitting verification

When header injection is confirmed, test whether response body injection is possible:

```text
Payload: %0d%0a%0d%0a<html><body>CRLF-BODY-INJECTED</body></html>
```

This injects two CRLF sequences to terminate headers and begin a response body. If the response body contains `CRLF-BODY-INJECTED` before the legitimate content → response splitting confirmed. This is higher severity: the attacker can craft an entirely fake HTTP response.

Rules:
- Use a unique, harmless body marker — never inject JavaScript, phishing content, or credential-harvesting forms.
- Response splitting typically requires the injection point to be in the first response header. If headers after the status line are injected, the split may not work.
- Some CDNs and WAFs detect and block response splitting specifically. If blocked, note the CDN/WAF protection and stop.

### Phase 4 — cookie injection assessment

When CRLF injection is confirmed on a path that sets cookies:

```text
Payload: %0d%0aSet-Cookie: pentest-crlftest=<engagement-id>; Path=/; HttpOnly
```

1. Send the request with the CRLF + `Set-Cookie` payload.
2. Inspect the response: does `Set-Cookie: pentest-crlftest=<engagement-id>` appear?
3. If yes → cookie injection confirmed. An attacker could overwrite session cookies, fixate a known session, or inject tracking cookies.
4. If the original response also sets a cookie, the injected cookie may appear before or after — both are valid injection positions.

### Phase 5 — SSRF and log-injection boundaries

These are distinct vulnerability classes that may chain with CRLF but require separate authorization:
- **SSRF via CRLF**: injecting `Host:` or `Authorization:` headers into an HTTP client call to redirect requests. Test only if SSRF scope is explicitly authorized.
- **Log injection**: injecting newlines into log entries via CRLF in User-Agent, Referer, or form fields. This is a log-forging finding, not CRLF header injection. Document separately.
- **Cache poisoning**: injected headers cached by a CDN. Test only if cache-deception scope is explicitly authorized.

If SSRF, log injection, or cache poisoning are not in scope, note the boundary and do not test.

## Decision points

- **Stop at first confirmed header injection**: one parameter showing injected `X-Pentest-CRLF` header is sufficient proof. Do not enumerate all parameters.
- **Escalate on response splitting**: if the `%0d%0a%0d%0a` payload injects a response body, the finding is high severity.
- **Escalate on cookie injection**: if `Set-Cookie` injection works on a session-cookie path, the finding is high severity.
- **Downgrade on CDN normalization**: if the CDN strips `\r\n` before reaching the origin, document the CDN protection and stop.
- **Refuse cache poisoning crossover**: CRLF injection can be used for cache poisoning, but this is a separate attack class requiring separate authorization.

## Prohibited behavior

- Injecting headers that affect real user sessions: session cookie overwrite, logout triggers, or tracking cookies that persist beyond the test.
- Injecting `Location:`, `Refresh:`, or other navigation headers that could redirect real users.
- Injecting `Content-Security-Policy`, `Access-Control-Allow-Origin`, or security headers that weaken the target's security posture.
- Deploying response-splitting bodies with active content (JavaScript, forms, iframes).
- Using CRLF injection to poison shared caches (CDN, proxy, browser cache).

## Stop conditions

- Injected marker header appears in response → injection confirmed, stop testing that parameter.
- Response splitting confirmed → critical finding, stop testing that endpoint class.
- Cookie injection confirmed on session path → high severity finding, stop.
- CDN/WAF consistently strips CRLF → negative result, document protection.
- Rate limiting or detection-team contact.

## Evidence — CRLF injection matrix

For each tested parameter, record:

```text
Parameter: <parameter name> | endpoint: <URL>
Reflected header: <Location | Set-Cookie | Content-Disposition | Content-Type | X-...>
CRLF sequence tested: <CR+LF | LF only>
Injected header confirmed: <yes | no | partially escaped>
Response splitting confirmed: <yes | no>
Cookie injection confirmed: <yes | no>
CDN/WAF transformation: <none | stripped | encoded | blocked>
Impact: <none | header injection | response splitting | cookie injection>
Confidence: <confirmed | likely | needs-review>
```

Aggregate into a parameter × injection-type matrix. Include both positive and negative results. Never store: raw response bodies with injected content that could be replayed, Set-Cookie headers with session-affecting values, or CRLF payloads that include redirect targets or active content.

## Report handoff

When a finding is confirmed:
1. `pentest_agent_record_finding` with affected parameter, injection type, CVSS estimate (5.3–6.5 for header injection, 7.5–8.5 for response splitting or cookie injection), and remediation guidance.
2. Reference the CRLF injection matrix.
3. Recommend: strip or percent-encode `\r` and `\n` characters in all user-controlled input before reflection in headers, validate redirect URLs against an allowlist, use parameterized header-setting APIs that prevent raw newline injection, and test CRLF vectors in CI with automated header inspection.
