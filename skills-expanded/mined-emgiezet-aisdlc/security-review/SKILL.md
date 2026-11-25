---
name: security-review
description: >
  The lens a reviewer applies to a diff to find security findings — trust boundaries, the ten
  review lenses, what counts as a finding and what does not. Use when reviewing a PR that touches
  authentication, authorization, session handling, secrets, input validation, or external requests.
---

# Security Review

The most common security defects are not in the crypto library; they appear at the boundaries where
trust assumptions change silently and no check is added on the far side. A reviewer who cannot name
the entry point, the path, and the sink has not found a finding — they have found a worry.

## What this skill is not

The severity scale, verdict tokens, and finding format belong to the `code-review` skill — read it
first. Deterministic per-language rules belong to the AP-AUTH-* and AP-AGENT-* catalogues in
slop-guard; those rules are enforced pre-write by slop-guard hooks, not by this reviewer. The
`/secure-review` command (`plugins/slop-guard/skills/secure-review`) runs a read-only subagent over
session findings. This skill decides what to look at and what counts as a finding.

## Trust boundaries first

Authorization is re-checked at every boundary, never inherited from the caller.

| Boundary | What crosses it | What must be re-checked on the far side |
|---|---|---|
| Unauthenticated HTTP edge | Any request from the public internet | Identity established, CSRF token validated |
| Authenticated user → other user's data | User-supplied identifier, filter, or cursor | Object-level authorization on the resolved record |
| Service → service | Internal bearer token, mTLS certificate | Audience matches; token was issued for this service |
| Job/queue consumer | Message payload from a queue or topic | Payload origin validated; no assumed caller identity |
| Third-party webhook | Inbound HTTP from an external system | Signature verified before payload is read |
| Browser → API | Requests from client-side JavaScript | Same-origin or CORS allow-list enforced; no secret in the URL |

## The lenses

| Lens | Question the reviewer answers | Typical finding |
|---|---|---|
| Authentication | Does the endpoint verify identity before acting? Do the hash algorithm (AP-AUTH-003) and token format (AP-AUTH-005) meet the rules? Is the OAuth2 flow using state and PKCE (AP-AUTH-010)? | Login endpoint accepts JWTs with `alg: none`; password stored with MD5 |
| Session lifecycle | Is a session rotated on privilege change (AP-AUTH-004)? Is it invalidated after a password reset (AP-AUTH-007)? | Session id unchanged after login; no absolute expiry |
| Account recovery and takeover | Is the reset token single-use with a short TTL (AP-AUTH-002)? Is re-authentication required for credential change (AP-AUTH-006)? Are OTP attempts bounded (AP-AUTH-011)? | Reset link reusable; e-mail change requires no password confirmation |
| Authorization and object access | Is every data-layer query scoped to the authenticated tenant or user? Are mass-assignment patterns gated? | `GET /invoices/{id}` fetches by id without a tenant filter; `PUT /user` binds all request fields to the model |
| Token and secret handling | Is secret entropy sufficient (AP-AUTH-001)? Do any tokens appear in logs, URLs, or error responses? | Signed token appears in a query string; 8-byte random reset token |
| Input reaching an interpreter | Does user input reach SQL, shell, template engines, or deserializers without sanitisation? | String concatenation in a query; `yaml.load` without safe_load |
| Outbound requests | Does the code fetch a caller-supplied URL? Is there an allow-list for redirects? | SSRF via unchecked `fetch(req.url)`; open redirect on the login callback |
| Rate limiting and abuse | Is there a per-identity or per-IP rate limit on credential attempts (AP-AUTH-008)? Does error messaging avoid account enumeration (AP-AUTH-009)? | No limit on password-reset requests; distinct messages for unknown user vs wrong password |
| Data exposure in responses and logs | Do responses or log statements include PII, stack traces, or internal paths? | `500` response body contains a SQL error with a table schema |
| Dependency and supply-chain changes | Is a new package necessary, pinned, and free of known CVEs? | Unpinned version range; package with a published CVE |

## What counts as a finding

A security finding names the entry point, the sink, and the impact, and shows the path between
them from the diff. A pattern with no reachable path from the diff is a note, not a finding.

"This looks unsafe" without a path is not a review finding.

A missing control on an unauthenticated endpoint is a finding even when no exploit has been written.

| Evidence present | Verdict |
|---|---|
| Entry point → path → sink, all in the diff | Finding — name the severity |
| Pattern present, but path not reachable from the diff | Note — state what additional change would make it reachable |
| Control absent on a reachable unauthenticated path | Finding — the missing control is the evidence |

## Severity, without a second scale

Definitions belong to `code-review`. The table maps the security question to those severities.

| Security question | Severity |
|---|---|
| Authentication or authorization bypass; account takeover path; secret disclosure; remote code execution | `blocker` |
| Missing rate limit (AP-AUTH-008/009); weak credential storage with no direct bypass; absent OTP limit (AP-AUTH-011) | `major` |
| Defence-in-depth gap; missing second factor where one is expected; CSRF on a low-value state change | `minor` |
| Naming or wording that weakens a security comment without changing behaviour | `nit` |

## Reviewing an auth change specifically

When the diff touches login, registration, reset, MFA, session, or token code:

| Must appear in the diff | Must appear in the tests |
|---|---|
| Session rotation on login and privilege change | Test that the session id before and after login are different |
| Old session invalidated on password or e-mail change | Test that the old session returns 401 after reset |
| Account owner notified of credential changes | Test that the notification is sent |
| Re-authentication gate before sensitive field change | Test that the gate rejects a request without re-auth |
| Rate limit or lockout on credential endpoints | Test that the limit fires, and that the counter resets correctly |

## Non-negotiable

1. Never approve a diff that widens an authorization boundary without a test that exercises the new boundary.
2. Never accept a fix that hides the symptom — catching the exception, suppressing the finding, or returning a neutral response while the vulnerable path remains.
3. Never treat a linter's silence as evidence that a path is safe.
4. Never permit a secret to move from source code to a log line; that is not a fix.
5. Never let "internal only" stand in for an authorization check — networks change, and so do trust relationships.
6. Never allow a diff to produce distinguishably different responses for a valid account vs an invalid one unless the existing API already does so (AP-AUTH-009).

## Review checklist

- [ ] Every boundary in the diff is identified; authorization is re-checked on the far side of each
- [ ] Authentication lens applied: identity verified before action; hash and token algorithms checked
- [ ] Session lifecycle lens applied: rotation on login, bounded lifetime, invalidation on reset
- [ ] Account recovery lens applied: reset token TTL and single-use, re-auth on credential change
- [ ] Authorization lens applied: every data query scoped to the authenticated tenant; no mass assignment
- [ ] Token and secret lens applied: no token in logs, URLs, or error bodies
- [ ] Input-to-interpreter paths checked: no raw user input in SQL, shell, templates, or deserializers
- [ ] Outbound-request lens applied: no caller-supplied URLs fetched without an allow-list
- [ ] Rate-limit lens applied: credential and OTP endpoints have per-identity limits; no enumeration
- [ ] Data-exposure lens applied: no PII, stack traces, or internal paths in responses or logs
- [ ] Every finding names the entry point, the sink, and the path; patterns without reachable paths are notes
- [ ] Auth-change checklist applied when the diff touches login, session, reset, MFA, or token code
- [ ] Dependency changes reviewed: package pinned, no known CVE, necessity established
