---
name: auth-workflow
description: Authentication flow mapping and validation — review login, registration, logout, account linking, re-authentication, and trust boundaries across the full auth surface with test-account isolation.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# Authentication workflow — surface mapping and validation

Use this skill to map and validate the complete authentication surface: login, registration, logout, account linking, re-authentication, step-up auth, and credential recovery. Identify trust boundaries, enumerate negative paths, and verify that each control behaves as documented. Every test must use test-owned accounts. Never brute-force, enumerate real users, or harvest credentials.

## Required inputs

- Written scope naming the target application, identity provider(s), authorized test accounts (minimum two per role tier), allowed auth flow validation methods, and explicit permission for account-impact checks.
- User-owned or project-approved test accounts only. Never use borrowed, harvested, shared, or customer accounts.
- Valid authorization cache. Separate explicit permission required for MFA, password reset, session, OAuth, JWT, and tenant-isolation validation.
- Known rate limits, lockout thresholds, testing window, and escalation contact.
- Auth technology stack: authentication library/framework, identity provider type, MFA technology, session technology, and password policy.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview when catalog tools are useful.
5. `pentest_agent_execute_tool` for execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — auth surface mapping

Build a complete map of the authentication surface before any active testing:

1. Enumerate all entry points: primary login page, API login endpoint, mobile login, social login (Google, Facebook, Apple, GitHub), SSO/SAML login, registration page, account recovery page, MFA challenge page.
2. Map the normal login flow end-to-end: what requests are sent, what parameters are required, what responses are returned, which cookies are set, which headers are expected.
3. Identify trust boundaries: where does the application hand off to an identity provider? Where does it accept tokens from external systems? Where does it manage its own session vs delegating to an IdP?
4. Map the negative path: what happens on wrong password, wrong MFA code, expired token, locked account, disabled account, unverified email? Record response codes, error messages, timing, and any information leakage.
5. Map registration: is registration open or invite-only? What fields are required? Is email verification required before login? Are there role/tenant defaults that could be exploited?

### Phase 2 — login endpoint validation

Test the login endpoint for common weaknesses:

**Default and weak credentials:**
1. Against test accounts, test whether the application ships with default credentials (`admin:admin`, `test:test`, etc.). This is common in appliances, IoT, and enterprise software. Only test on systems where you have confirmed these exist.
2. Check password policy enforcement at login: are short passwords accepted? Are known breached passwords accepted? Does the application enforce password complexity at login?

**User enumeration:**
1. Submit login with a valid email + wrong password. Submit login with an invalid email + any password. Compare: HTTP status codes, response body text, response length, response time (timing attack), and whether the application returns a different message ("password incorrect" vs "account not found").
2. If the application returns a consistent "invalid credentials" message regardless of whether the email exists, user enumeration is mitigated.
3. Check enumeration via registration endpoint (does registering with an existing email produce "email already taken"?), password reset endpoint (does "reset email sent" differ for existing vs non-existing accounts?), and account lookup APIs.

**Rate limiting and lockout:**
1. Submit multiple failed login attempts (5, 10, 20) for Test-Account-1. Check whether the account is locked, throttled, or CAPTCHA-gated. Record the lockout threshold and lockout duration.
2. Test whether lockout is per-account or global. If global, an attacker can lock all accounts simultaneously.
3. Test whether lockout can be bypassed by varying the case of the email, adding `+` aliases, or using different IP addresses.
4. After lockout, check whether the reset flow still works (lockout should not block legitimate recovery).

**Credential transport:**
1. Check whether the login endpoint is served over HTTPS. If not, credentials are transmitted in cleartext.
2. Check whether credentials are sent in the request body (POST), URL query string (GET — leaks to logs and Referer), or headers (unusual but acceptable if encrypted).
3. Check whether the password is logged by the server or client-side analytics. Examine response bodies, error pages, and client-side scripts for password reflection.

### Phase 3 — registration validation

1. Register new test accounts through the normal flow. Map the exact sequence: form submission, email verification, profile creation, initial session.
2. Check whether email verification is required before login. If the application allows login without verified email, test for account pre-hijacking: register with another user's email, if email verification is not enforced, the account is yours but the email is theirs.
3. Check for parameter pollution during registration: can the role, permissions, tenant, or plan be set via `role=admin` in the registration request? Can `is_admin=true` be added?
4. Check for excessive data collection: does the registration form ask for data beyond what's necessary? Is the password collected over HTTPS? Are there weak password requirements (minimum length < 8, no complexity, no breach check)?
5. Test duplicate registration: register with the same email twice. The second attempt should fail. If it succeeds, the application may have duplicate account handling issues.

### Phase 4 — re-authentication and step-up auth

1. Identify actions that should require re-authentication: viewing/editing sensitive profile fields, changing email/password, disabling MFA, viewing API keys, initiating money transfers, deleting account.
2. For each, check whether the application prompts for password or MFA before allowing the action. If password change doesn't require the old password, this is a finding.
3. Check whether the re-authentication prompt has CSRF protection, rate limiting, and lockout independent of the main login.
4. If the application uses step-up authentication (admin mode, sudo mode), check whether the step-up session has a shorter timeout than the primary session.

### Phase 5 — logout and session termination

1. Perform a login → logout sequence. Map the exact requests. Check what is terminated: application session, identity provider session (federated logout), remember-me tokens, device tokens, OAuth tokens.
2. Check whether logout requires a CSRF token or can be triggered by GET request. If GET-based logout with no token, an attacker can log users out forcibly (annoyance but low severity) or use logout as a CSRF vector.
3. Check whether logout redirects to an external URL without validation. If `logout?redirect=https://attacker.com` works, this is an open redirect finding.
4. After logout, check the browser's back button: can the user navigate back to an authenticated page? If the page is served from the browser cache, this is a caching issue (not strictly auth, but note it).

### Phase 6 — cross-identity-provider and multi-tenant auth

1. If the application supports multiple identity providers, test whether account linking between providers requires authentication on both sides. Can an attacker link their own social login to a victim's account?
2. Test SAML/OIDC federation boundaries: if the application trusts an external IdP, test whether assertions from that IdP are properly validated (signature, expiration, audience, issuer).
3. Test multi-tenant isolation: log in as Test-Account-1 in Org-A. Change the tenant ID in the request to Org-B. If the session is accepted, tenant isolation is broken — critical finding.
4. Test whether the same email can have accounts in multiple tenants with the same password. If so, password reuse across tenants is a risk.

## Decision points

- **Escalate on user enumeration**: user enumeration alone is typically low/medium, but combined with weak password policy or credential spraying it enables targeted attacks.
- **Escalate on missing account lockout**: no lockout after 20+ failed attempts is high — enables online brute force.
- **Escalate on tenant isolation failure**: cross-tenant session acceptance is critical.
- **Escalate on registration parameter pollution**: role/privilege injection during registration is critical.
- **Downgrade on cosmetic issues**: GET-based logout without CSRF is low unless chainable.

## Prohibited behavior

- Brute-forcing passwords, enumerating real user accounts, or credential stuffing.
- Harvesting credentials during login, registration, or recovery flows.
- Social engineering or phishing for credentials.
- Testing SAML/OIDC federation against identity providers not explicitly in scope.
- Storing passwords, credentials, or authentication tokens in raw evidence.

## Stop conditions

- Account lockout on a test account → stop brute-force testing.
- Tenant isolation failure confirmed → critical finding, stop.
- Registration parameter pollution enables privilege escalation → critical finding, stop.
- Identity provider not in scope → stop, do not probe external IdP.
- Evidence would include real credentials or PII → redact and stop.

## Evidence — auth surface matrix

Record per test vector:

```text
Target: <app name>
Auth surface element: <login endpoint | registration | password reset | logout | step-up auth | IdP federation>
Test vector: <user enumeration — timing | missing lockout | registration role injection | GET-based logout | tenant isolation | ...>
Test account: <Test-Account-1>
Expected: <consistent error message | lockout after N failures | role ignored | POST logout with CSRF | tenant scope enforced>
Observed: <different error for existing email | no lockout after 50 failures | admin role accepted | GET logout works | cross-tenant session accepted>
Impact: <user enumeration only | brute force possible | privilege escalation | tenant isolation bypass>
Confidence: <confirmed | likely | needs-review>
```

Aggregate into an auth surface posture summary:
- full auth entry point inventory;
- credential transport and storage hygiene;
- user enumeration risk;
- rate limiting and lockout posture;
- registration and account lifecycle controls;
- re-authentication and step-up auth posture;
- logout and session termination completeness;
- multi-tenant and federation boundaries.

Never store: passwords, credentials, password hashes, authentication tokens, session cookies, CSRF tokens, identity provider assertions, or PII.

## Report handoff

When a finding is confirmed:
1. `pentest_agent_record_finding` with affected auth surface element, minimal proof, CVSS estimate (9.0–10.0 for tenant isolation bypass or registration privilege injection, 7.0–8.0 for missing lockout, 5.0–6.0 for user enumeration, 3.0–4.0 for GET-based logout), and remediation guidance.
2. Reference the auth surface matrix.
3. Recommend: consistent error messages with no timing differences, account lockout after N failed attempts with per-account locking, email verification required before login, role/permission assignment server-side only (never accept from client), re-authentication for all account-modifying actions, CSRF-protected POST logout, tenant scope enforced at session level, federated logout when identity provider is used, and auth security tests in CI pipeline.
