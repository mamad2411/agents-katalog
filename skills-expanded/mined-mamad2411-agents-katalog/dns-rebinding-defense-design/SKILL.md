---
name: dns-rebinding-defense-design
description: >
  Defend browser-facing and local apps against DNS rebinding: Host/SNI allowlists, rejecting
  private IP targets, DNS pinning, authentication on localhost services, CORS/CSRF hardening,
  and browser/network controls. Use when hardening owned internal tools, local admin UIs,
  WebViews, or public apps against rebinding — not for building rebinding attack services.
---

# DNS Rebinding Defense Design

## Scope And Authorization

- **In scope:** Applications, local agents, and network policies you own.
- **Out of scope:** Disabling users’ security to facilitate attacks; unauthorized testing of third parties.
- Prefer defense-in-depth; no single control is perfect across all browsers.
- Redact internal host inventories in public docs.
- Pair with `dns-rebinding-attacks` (authorized test), `django-csrf-middleware-tuning` / web auth skills, and `code-quality-standards`.

## When To Use

- Shipping a local companion app (127.0.0.1 HTTP).
- Internal admin tools reachable from browsers with weak auth.
- Public SaaS that must not treat DNS trust as authorization.
- Remediation after a rebinding finding.
- Hardening IoT/router-style web UIs you manufacture.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Authorized rebinding tests | `dns-rebinding-attacks` |
| Classic SSRF | `ssrf-server-side-request-forgery` |
| CSRF cookie apps | framework CSRF skills |
| DNS ops latency | `dns-latency-triage` |
| Code quality baseline | `code-quality-standards` |

## Defense layers

| Layer | Control |
| --- | --- |
| Application auth | Local services require auth token/password/mTLS—not “localhost = trusted” |
| Host validation | Allowlist expected `Host` headers; reject unknown |
| Address policy | Server refuses to bind/process as if private IP from rebind without auth |
| DNS pinning | Client libraries cache first resolution for origin (where platform allows) |
| Browser | Keep updated; Prefer isolation features |
| Network | Block outbound to external DNS for sensitive segments if policy fits; split DNS carefully |
| CORS | Do not reflect arbitrary origins with credentials |

## Workflow

### 1. Confirm scope and success criteria

1. Apps: public web, local agent, desktop WebView, internal tools.
2. Success: unauthenticated private-IP access via rebind blocked; Host allowlist enforced; local services authenticated; tests pass.
3. Threat model includes malicious website visited by employee/user.

### 2. Inventory risky components

```bash
rg -n "127\\.0\\.0\\.1|localhost|0\\.0\\.0\\.0|Host.*header|ALLOWED_HOSTS" .
# Local listeners on developer machines (owned host)
# netstat / ss -lntp | findstr 127.0.0.1
```

1. Flag metrics, debug, printers, admin panels without auth.
2. Note any “security” based only on source being browser same-origin.

### 3. Authenticate local and internal HTTP

1. Local companion: generate install-time random token; require header on every request.
2. Bind to `127.0.0.1` not `0.0.0.0` when remote access not needed.
3. Prefer OS IPC / native messaging over open HTTP where possible.
4. Internal tools: SSO + CSRF; no anonymous LAN trust alone.

### 4. Host header and absolute URL allowlists

```python
# Conceptual Django/Flask-style check
ALLOWED = {"app.example.com", "localhost:7234"}
def validate_host(host: str) -> bool:
    return host.split(":")[0] in {h.split(":")[0] for h in ALLOWED}  # simplify carefully
```

1. Frameworks: `ALLOWED_HOSTS` (Django), equivalent hard reject 400.
2. Reject `Host: 127.0.0.1` on public app servers when not expected.
3. Do not trust `X-Forwarded-Host` from untrusted clients.

### 5. Server-side and client-side DNS discipline

1. **Browsers** own rebinding mitigations inconsistently—do not rely on them alone.
2. App-level fetchers (not browser): pin IPs after first resolve; block RFC1918/link-local/metadata IPs for untrusted URLs (`ssrf` skill).
3. Short-TTL external names pointing to private ranges: treat as suspicious in monitoring.

### 6. Web platform hardening

1. CORS: explicit origins; never `*` with credentials.
2. CSRF on cookie sessions.
3. `SameSite` cookies appropriately.
4. Content-Security-Policy reduces some script abuse (not a full rebind fix).
5. For sensitive desktops: discourage unnecessary local HTTP servers.

### 7. Verify and hand off

1. Authorized retest via `dns-rebinding-attacks` methodology against canaries.
2. Unit tests: invalid Host → 400; local API without token → 401.
3. Document local token storage and rotation.
4. SOC: optional detection of internal hosts receiving odd Host headers from proxies.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Localhost API | Token + 127.0.0.1 bind | Open unauth on 0.0.0.0 |
| Host check | Strict allowlist | Any Host accepted |
| Trust | AuthZ decisions | “Same hostname = safe” |
| SSRF client | Block private IPs | Follow DNS freely |
| Fix | Multi-layer | “Browsers fixed it” only |
| Scope | Owned apps | Break others’ tools |

## Output Checklist

- [ ] Risky local/internal HTTP inventoried
- [ ] Auth required on local services
- [ ] Bind addresses minimized
- [ ] Host allowlists enforced
- [ ] CORS/CSRF reviewed for browser apps
- [ ] Private IP policies for server-side fetches
- [ ] Tests for Host/token failures
- [ ] Authorized retest clean or residual risk filed
- [ ] Developer guidance for new local agents
- [ ] `code-quality-standards` applied

## Rules

- Localhost is not an authentication factor.
- Defense in depth: Host checks + auth + bind + client IP policies.
- Do not claim perfect browser-only protection.
- Authorized defensive engineering only.
- Assessment details live in the attacks neighbor skill.
