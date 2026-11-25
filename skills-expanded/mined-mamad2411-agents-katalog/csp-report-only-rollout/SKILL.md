---
name: csp-report-only-rollout
description: >
  Roll out Content-Security-Policy-Report-Only safely: report-to/report-uri,
  owned collectors, violation triage, noise filtering, gradual directive
  tightening, canary then enforce. Use when staging CSP without blocking
  production, cutting report floods, or dual-header CSP migrations on owned apps.
---

# CSP Report-Only Rollout

## Scope And Authorization

- **In scope:** Web apps and report collectors you own; authorized production canaries.
- **Out of scope:** Flooding third-party report endpoints; collecting violation reports that include sensitive URLs without retention policy.
- Prefer org-owned collectors over random public SaaS without DPA.
- Pair enforcement end-state with `csp-nonce-rotation` and XSS skills.

## When To Use

- First CSP deployment on a brownfield app.
- Tightening directives without user-facing breakage.
- Measuring third-party script inventory via violation noise.
- Migrating Report-Only → enforcing `Content-Security-Policy`.
- Dual headers: enforce baseline + report-only stricter policy.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Per-request nonces | `csp-nonce-rotation` |
| XSS proof of concept | `xss-cross-site-scripting` |
| CSP bypass research | content-security-policy-bypass (external/catalog) |
| COOP headers | `cross-origin-opener-policy` |
| Implementation quality baseline | `code-quality-standards` |

## Rollout stages

```text
0. Inventory assets → 1. Report-Only wide → 2. Triage/fix → 3. Tighten RO →
4. Canary enforce → 5. Full enforce → 6. Continuous reports
```

| Stage | Header | Goal |
| --- | --- | --- |
| Discover | `Content-Security-Policy-Report-Only` | Collect violations only |
| Dual | RO strict + weak enforce | Protect something while learning |
| Enforce | `Content-Security-Policy` | Block violations |

## Workflow

### 1. Confirm scope and success criteria

1. Document hosts, SPA vs MPA, third parties (analytics, chat, payments).
2. Success: report volume understood; false positives fixed; enforce without Sev-1; residual exceptions ticketed.

### 2. Stand up reporting

```http
Reporting-Endpoints: csp-endpoint="https://csp-reports.example.corp/r/csp"
Content-Security-Policy-Report-Only: default-src 'self'; script-src 'self'; report-to csp-endpoint
```

Legacy:

```http
Content-Security-Policy-Report-Only: default-src 'self'; script-src 'self'; report-uri https://csp-reports.example.corp/r/csp
```

Collector requirements:

1. AuthN between edge and collector if needed; rate limit.
2. Schema validation; store `document-uri`, `effective-directive`, `blocked-uri` (redact query tokens).
3. Retention limits; access control for engineers.

### 3. Ship initial Report-Only policy

Start looser than final target but still informative:

```text
default-src 'self';
script-src 'self' 'unsafe-inline' https://cdn.example.com;
style-src 'self' 'unsafe-inline';
img-src 'self' data: https:;
connect-src 'self' https://api.example.com;
object-src 'none';
base-uri 'self';
frame-ancestors 'self'
```

```bash
curl -sSI 'https://app.example.local/' | rg -i 'content-security-policy|reporting-endpoints'
```

### 4. Triage violations

| Pattern | Action |
| --- | --- |
| Known CDN blocked | Add host or self-host |
| Extension noise (`chrome-extension:`) | Filter in collector |
| Inline script | Nonce/hash plan (`csp-nonce-rotation`) |
| Unexpected domain | Investigate malware/XSS/supply chain |
| `eval` | Remove or isolate |

Dashboards: top `blocked-uri`, top pages, trend after deploys.

### 5. Tighten and canary enforce

1. Remove `'unsafe-inline'` in RO once nonces ready; watch reports.
2. Enforce on canary cohort (header at edge for % traffic or separate host).
3. Monitor error rates, support tickets, conversion funnels.
4. Full enforce; keep RO for **stricter** next policy if desired.

```http
Content-Security-Policy: default-src 'self'; script-src 'nonce-…' 'strict-dynamic'; object-src 'none'; base-uri 'self'
Content-Security-Policy-Report-Only: …stricter future policy…
```

### 6. Control report floods

1. Sample if volume extreme (edge sampling).
2. Dedupe by fingerprint `(directive, blocked, document path)`.
3. Alert on **new** blocked hosts, not raw count alone.
4. Fix misconfigured loops (collector URL must not recurse CSP noise).

### 7. Hand off

1. Document final enforcing policy in security headers standard.
2. Owner for weekly violation review (time-boxed).
3. Link XSS bugs found during triage to app teams.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| First prod step | Report-Only | Enforce strict blind |
| Collector | Owned + redaction | Public dump with cookies in URLs |
| Noise | Filter extensions | Chase every chrome-extension report |
| Dual header | Baseline enforce + strict RO | Two conflicting enforces accidentally |
| Success | Stable enforce + low new domains | “CSP header present” checkbox |

## Output Checklist

- [ ] Asset/third-party inventory
- [ ] Reporting endpoints live and access-controlled
- [ ] Report-Only header verified via curl
- [ ] Triage process + dashboards
- [ ] Noise filters applied
- [ ] Nonce/hash plan for inline
- [ ] Canary enforce metrics reviewed
- [ ] Full enforce shipped or scheduled
- [ ] Retention/redaction policy documented
- [ ] Residual exceptions with owners/expiry

## Rules

- Report-Only is a means to **enforce**, not a permanent home.
- Do not put secrets in report URLs; redact query strings in storage.
- Authorized apps only; focus on **CSP Report-Only → enforce rollout**.
