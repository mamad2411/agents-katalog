---
name: owasp-review
description: Review a code diff against the current OWASP Top 10; report findings keyed to file:line with severity (high/medium/low) and a fix recommendation.
---

# owasp-review

> Pair with `polymath-engineering:code-review` on the security axis. Output is findings, not a tutorial.

## When to use

- A workflow's `reviewPR` invokes this as a fanout sibling.
- The diff touches AuthN/AuthZ, input parsing, file I/O, network calls, or DB queries.
- The user says "security review this".

## Inputs

- The diff (current `git diff` or PR diff).
- The PRD if available (gives intended trust boundary).

## OWASP Top 10 lens

Walk the diff under each category. Cite the OWASP year you used.

| # | Category | Diff signals to look for |
| - | -------- | ------------------------ |
| A01 | Broken Access Control | Missing AuthZ check on new endpoint; permission strings checked client-side; IDOR (user-supplied IDs unfiltered). |
| A02 | Cryptographic Failures | Hardcoded secrets; rolling-your-own crypto; predictable IVs; weak hashes for passwords. |
| A03 | Injection | String-concatenated SQL / shell / LDAP / XPath; HTML built without escaping; template injection. |
| A04 | Insecure Design | Missing rate limit on auth; trust-on-first-use; secrets stored in logs. |
| A05 | Security Misconfig | Permissive CORS; debug endpoints in prod; default credentials; verbose error pages. |
| A06 | Vulnerable & Outdated Components | New dependency pinned to a known-vulnerable version; transitive bumps without justification. |
| A07 | Identification & AuthN Failures | Session tokens predictable; missing MFA path; brute-force-able credential flow. |
| A08 | Software & Data Integrity Failures | Untrusted deserialization; missing signature on update artifacts; CI fetches unsigned binaries. |
| A09 | Security Logging & Monitoring | Sensitive data logged; AuthN failures not logged; no audit trail for AuthZ-relevant changes. |
| A10 | Server-Side Request Forgery | Outbound HTTP from user-supplied URL/host; missing allow-list; no DNS rebinding mitigation. |

## Procedure

1. Read the diff.
2. For each category above, scan for the listed signals.
3. For every hit:
   - Cite file:line.
   - Classify severity: **high** (exploitable now), **medium** (requires another precondition), **low** (defense-in-depth nit).
   - Propose a concrete fix.

## Output

```text
OWASP review (Top 10, 2021):

A03 Injection (high)
  - api/search.py:42 — query built via f-string with user input.
    Fix: use parameterized SQL.

A01 Broken Access Control (medium)
  - api/refund.py:18 — /refund/<order_id> reads any order; no
    ownership check.
    Fix: verify order.user_id == request.user_id before reading.

(No findings: A02, A04, A05, A06, A07, A08, A09, A10.)
```

## Quality bar

- No finding without a file:line citation.
- No category without a verdict — either a finding or an explicit "no findings" line.
- "Fix" is concrete, not a link to the OWASP wiki.
