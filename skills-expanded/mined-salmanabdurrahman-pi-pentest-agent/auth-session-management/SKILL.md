---
name: auth-session-management
description: Session lifecycle security review — validate session creation, rotation, invalidation, cookie attributes, concurrent-session handling, remember-me tokens, and logout enforcement on authorized applications.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# Session management — lifecycle security review

Use this skill to validate session creation, rotation, invalidation, cookie attributes, concurrent-session handling, remember-me tokens, device tracking, and logout enforcement. Every test must use test-owned accounts. Never hijack, replay, or persist real user sessions.

## Required inputs

- Written scope naming the target application, authorized test accounts (minimum two per role tier), allowed session validation methods, and explicit permission for session manipulation testing.
- User-owned or project-approved test accounts only. Never use borrowed, harvested, shared, or customer accounts.
- Valid authorization cache. Separate explicit permission required for MFA, password reset, OAuth, JWT, and tenant-isolation validation.
- Known rate limits, session creation limits, testing window, and escalation contact.
- Session technology inventory: server-side sessions with opaque IDs, client-side sessions (JWT or encrypted cookie), or hybrid. Cookie name, domain, path, and expected flags.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview when catalog tools are useful.
5. `pentest_agent_execute_tool` for execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — cookie attribute audit

Inspect session cookies on the test account:

1. Record all cookies set after login. For each: name, value length and apparent format (opaque hex/base64, JWT, or plaintext), domain, path, expires/max-age, and flags.
2. Check `Secure` flag: is it set on all session cookies? If absent over HTTPS, the cookie can be leaked over an accidental HTTP request.
3. Check `HttpOnly` flag: is it set? If absent, JavaScript (XSS) can read the session cookie directly.
4. Check `SameSite` attribute: `Strict` (best), `Lax` (acceptable), `None` (requires Secure), or absent (treated as Lax in modern browsers but vulnerable in older).
5. Check `__Host-` or `__Secure-` prefix usage: `__Host-` prefix enforces Secure + Path=/ + no Domain attribute (cookie is origin-bound). If the session cookie doesn't use this prefix, test for subdomain cookie injection.
6. Check Domain attribute: is the cookie scoped to `.example.com`? If so, any subdomain can read it — `test.example.com` or a compromised `cdn.example.com` can steal the session.
7. Check Path attribute: is it scoped to `/` or a specific path? Session cookies should be Path=/.
8. Check Expires/Max-Age: is the session cookie persistent (survives browser close) or session-only? Persistent session cookies are vulnerable to theft from disk.

### Phase 2 — session creation and login security

1. Log in as Test-Account-1. Record the pre-login session ID (if any) and the post-login session ID. The session ID MUST change (rotation on authentication). If the same session ID is used before and after login, the application is vulnerable to session fixation.
2. Session fixation test: obtain a pre-auth session ID. Construct a URL that sets this session ID. Have Test-Account-2 click this URL (or simulate the flow). After Test-Account-2 logs in, check if the same session ID now grants access to Test-Account-2's account. If so, session fixation confirmed.
3. Check whether the session ID is set via cookie only, or also appears in URLs, POST bodies, or response headers. Session IDs in URLs leak to browser history, server logs, and Referer headers.
4. Check whether login sets any additional security cookies: device fingerprint, CSRF token, or context-specific session markers.

### Phase 3 — session rotation and invalidation

Test whether sessions are properly rotated and invalidated on privilege-level changes:

1. **Logout invalidation**: log in as Test-Account-1. Record the session cookie. Log out. Use the old session cookie. If the server accepts it, session is not invalidated on logout.
2. **Password change invalidation**: log in as Test-Account-1. Record the session cookie. Change the password. Use the old session cookie. If accepted, sessions survive password change — a stolen session cannot be revoked.
3. **Role change invalidation**: if the application has role-based access, log in as Test-Account-1. Record the session. Have an admin change Test-Account-1's role. Check if the old session reflects the new role (expected), or retains old privileges (session role cached, not revalidated).
4. **Concurrent session handling**: log in from Device-A and Device-B as the same test account. Check whether both sessions work simultaneously. If the application claims to limit concurrent sessions, log in from Device-C and check which session is terminated.
5. **Session ID rotation on privilege elevation**: if Test-Account-1 performs a step-up (re-authentication, MFA, admin mode), the session ID should rotate. If not, the session's privilege level is not bound to authentication freshness.
6. **Session timeout**: record the session token. Wait for the configured idle timeout (or 30 minutes if unknown). Use the token. If still valid, session timeout may be too long for sensitive applications.

### Phase 4 — remember-me and persistent authentication

If the application offers "Remember Me":
1. Check whether the remember-me token is separate from the session cookie or the same cookie with a longer expiry.
2. Capture a remember-me token. Log out. Use the remember-me token to re-authenticate. If the token works after explicit logout, logout is cosmetic for remember-me users.
3. Check whether the remember-me token is rotated on each use. If a remember-me token is reusable, a stolen token grants indefinite access.
4. Check remember-me token entropy: if the token is `base64(username + timestamp)`, it is predictable. If the token is a short numeric code, it is brute-forceable.
5. Check whether the user can view and revoke active remember-me sessions from a security dashboard.

### Phase 5 — cross-context and subdomain isolation

1. If the session cookie is scoped to `.example.com`, set up a test subdomain or inspect sibling subdomains. Check whether a cookie set by `app.example.com` is sent to `api.example.com` (expected for `.example.com` scope) and whether cross-origin requests leak the session.
2. Test for session injection across subdomains: if `cdn.example.com` has user-controlled content, can an attacker set a session cookie that overwrites the legitimate one on `app.example.com`?
3. Test cookie tossing: if the application sets multiple cookies with the same name but different paths, check which one the server reads. Cookie tossing can confuse session selection.
4. Check CORS configuration: if CORS is misconfigured (Access-Control-Allow-Origin: * with credentials), a malicious site can make authenticated cross-origin requests.

### Phase 6 — logout completeness

1. Log in as Test-Account-1. Note all cookies, local storage keys, and session storage keys set by the application.
2. Click logout. Check which cookies, local storage entries, and session storage entries are cleared. Any that remain are residual authentication material.
3. After logout, attempt to access authenticated endpoints with the old cookies and any residual tokens. If any grant access, logout is incomplete.
4. If the application uses federated logout (OIDC end_session_endpoint), check whether the identity provider session is also terminated. Log out of the application. Open the identity provider in a new tab. If still authenticated, single-logout is incomplete.

## Decision points

- **Stop at session fixation**: confirmed session fixation is a high finding. Stop and report.
- **Escalate on missing rotation**: no session rotation after login, password change, or logout → high.
- **Escalate on missing Secure/HttpOnly flags**: cookie theft via MITM or XSS is possible → high (Secure missing) or medium (HttpOnly missing).
- **Escalate on cross-subdomain cookie injection**: if user-controlled subdomain can set session cookies for the parent → high.
- **Downgrade on long timeout alone**: 8-hour idle timeout is a medium finding if other controls are strong.

## Prohibited behavior

- Stealing, replaying, or persisting real user sessions.
- Session hijacking via XSS, MITM, or social engineering.
- Brute-forcing session IDs or remember-me tokens against live systems.
- Testing cookie injection on subdomains you do not own or control.
- Storing session cookies, session IDs, remember-me tokens, or device fingerprint data in raw evidence.

## Stop conditions

- Session fixation confirmed → stop.
- Session not invalidated after password change → stop.
- Remember-me token reusable after explicit logout → stop.
- Cross-subdomain cookie injection confirmed → stop.
- Account lockout or session creation limit reached.

## Evidence — session posture matrix

Record per test vector:

```text
Target: <app name>
Session technology: <server-side opaque ID | JWT | encrypted cookie | hybrid>
Test vector: <cookie flags — Secure missing | session fixation | session not rotated on password change | remember-me token not rotated | logout incomplete | ...>
Test account: <Test-Account-1>
Expected: <Secure set | session ID rotated | old session rejected | token single-use | all cookies cleared>
Observed: <Secure absent | session ID unchanged | old session accepted | token reusable | residual cookies remain>
Impact: <cookie exposed to MITM | session fixation → ATO | stolen session irrevocable | persistent access after logout>
Confidence: <confirmed | likely | needs-review>
```

Aggregate into a session security posture summary:
- cookie attribute hygiene;
- session lifecycle (creation, rotation, invalidation, timeout);
- remember-me token handling;
- cross-subdomain and CORS isolation;
- logout completeness.

Never store: session cookies, session IDs, remember-me tokens, CSRF tokens, device fingerprint data, local storage content, or PII.

## Report handoff

When a finding is confirmed:
1. `pentest_agent_record_finding` with affected session vector, minimal proof, CVSS estimate (7.0–8.0 for session fixation or missing rotation, 5.0–6.0 for missing Secure/HttpOnly flags, 4.0–5.0 for long timeout or incomplete logout), and remediation guidance.
2. Reference the session posture matrix.
3. Recommend: session ID rotation on every authentication event (login, logout, password change, role change, step-up), Secure + HttpOnly + SameSite=Lax + __Host- prefix for session cookies, session invalidation server-side on logout, short idle timeout with absolute timeout, remember-me tokens as separate opaque tokens with rotation, device/session management dashboard for users, and CSRF protection on all state-changing endpoints.
