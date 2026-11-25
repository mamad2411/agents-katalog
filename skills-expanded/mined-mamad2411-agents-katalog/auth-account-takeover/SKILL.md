---
name: auth-account-takeover
description: Account takeover chain validation — assess password reset, session, OAuth, MFA, email-change, and support-flow weaknesses with strict test-account limits.
disable-model-invocation: true
risk: caution
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# Account takeover — chain validation

Use this skill to validate account takeover (ATO) chains across password reset, session management, email change, OAuth linking, MFA bypass, and support-flow pathways. Every step must use test-owned accounts only. Validate one low-risk link at a time; stop when sufficient proof of a takeover chain is established. Never take over real accounts.

## Required inputs

- Written scope naming the target application, identity provider, authorized test accounts (minimum two per role tier), allowed ATO chain paths, and explicit permission for account-impact validation.
- User-owned or project-approved test accounts only. Never use borrowed, harvested, shared, or customer accounts.
- Valid authorization cache. Separate explicit permission required for MFA bypass, password reset, session manipulation, OAuth linking, and support-flow testing.
- Known rate limits, lockout thresholds, notification flood controls, testing window, and rollback/escalation contact.
- Account recovery mechanism: can locked or modified test accounts be restored without contacting production support?

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — chain mapping

Map every pathway that could lead from no access to account control:
- **Password reset**: email reset, SMS reset, security-question reset, support-assisted reset, social-login recovery.
- **Email change**: change email without re-authentication, change email without verifying new address, change email then trigger password reset to new email.
- **Session management**: session fixation, session not invalidated after password change, session not rotated after login, long-lived sessions without activity timeout, cookie reuse across subdomains.
- **OAuth linking**: link attacker-controlled OAuth provider to victim account, missing state parameter in OAuth flow, redirect_uri manipulation stealing authorization code.
- **MFA bypass**: MFA not required for email/password change, MFA not required for OAuth linking, MFA reset via support without identity verification.
- **Support/social**: support flow that resets MFA or password with weak identity check, support agent can change email without additional verification.

### Phase 2 — password reset validation

For each reset pathway (email, SMS, security questions):
1. Initiate reset for Test-Account-1; capture the reset token or link format.
2. Check token properties: length (< 20 chars is weak), entropy (sequential, timestamp-based, predictable), expiry (> 1 hour is risky), one-time-use (token reusable after first use?).
3. Check token delivery: is it in URL (leaks via Referer header), in email body (leaks if email is forwarded), or in SMS (leaks if SIM-swapped)?
4. Test cross-account token use: reset for Test-Account-1, use the token to change Test-Account-2's password. If the token is not bound to the requesting account, the reset flow is broken.
5. Test post-reset session: after reset, is the old session invalidated? If not, the old session holder still has access.
6. Check notification: does the account owner get notified of the reset? Is the notification clear and timely?

### Phase 3 — email change and takeover chain

Test the classic ATO chain: change victim email → trigger password reset to attacker email → log in:
1. As Test-Account-1, attempt to change email to `attacker@test-mail.com` (a test email you own).
2. Check whether email change requires: current password, MFA, email verification to new address, notification to old address, cooling-off period.
3. If email changes without verification, trigger password reset. If reset email goes to the new address, full ATO chain is complete.
4. Check whether the old email receives a "your email was changed" notification with an undo link.

### Phase 4 — session takeover

Test session-related ATO vectors:
1. **Session fixation**: obtain a pre-auth session ID. Send a link to Test-Account-2 that sets this session ID. After Test-Account-2 logs in, use the same session ID as Test-Account-1 to access Test-Account-2's account.
2. **Session not rotated**: log in as Test-Account-1. Record the session token. Log out. Check if the same token still works (session not invalidated). Log in again. Change password. Check if old session tokens still work.
3. **Cookie scope**: if the session cookie is scoped to `.example.com`, check whether `subdomain.example.com` can read or set it.
4. **JWT as session**: if sessions are JWTs, check whether the JWT contains a session ID that can be revoked (stateless JWT logout is impossible without a blocklist).

### Phase 5 — OAuth ATO vectors

1. **Missing state parameter**: initiate OAuth flow; check if `state` parameter is present and validated. If missing, CSRF-based account linking is possible.
2. **Redirect_uri manipulation**: try `redirect_uri=https://target.com/callback%40attacker.com` or `redirect_uri=https://target.com.attacker.com/callback`. If the authorization code is sent to an attacker-controlled URI, ATO via code theft.
3. **OAuth account linking without verification**: link a new OAuth provider to Test-Account-1. If linking does not require password or MFA, a session hijacker can link their own OAuth provider and gain persistent access.
4. **Scope escalation**: request additional OAuth scopes during linking. Check if the application blindly accepts elevated scopes.

### Phase 6 — MFA bypass and recovery

1. **MFA not enforced on sensitive actions**: change email, change password, link OAuth, view API keys — are all of these MFA-gated?
2. **MFA reset flow**: how does a user reset MFA if they lose their device? Is the reset flow weaker than the MFA it replaces?
3. **Backup code reuse**: are backup codes single-use? Can they be brute-forced (usually short, numeric)?
4. **MFA fatigue**: if push-based MFA is used, can repeated pushes trick the user into approving? Never test this against real users.

## Decision points

- **Stop at one confirmed chain**: a single end-to-end ATO chain (no access → account control) is a critical finding. Do not chain further steps to "see how bad it gets."
- **Escalate on privilege impact**: if the ATO chain affects an admin or privileged test account, the impact is amplified.
- **Downgrade on isolated weakness**: a weak reset token alone (without chainable steps) is a medium finding; an unverified email change alone (without password reset chaining) is medium.

## Prohibited behavior

- Taking over or accessing real user accounts — even for "verification."
- Credential stuffing, password spraying, MFA fatigue, social engineering, token theft, session hijacking from real users.
- Triggering password reset emails, SMS, or push notifications at high volume.
- Account lockout, password reset flooding, role changes, tenant data access, or persistence.
- Using harvested credentials, tokens, or session cookies from passive recon.
- Storing passwords, cookies, bearer tokens, JWTs, authorization codes, refresh tokens, recovery links, or PII in raw evidence.

## Stop conditions

- Any account lockout or unexpected MFA prompt storm on a test account.
- Password reset email/SMS sent to a real user address.
- Tenant boundary crossing (Org-A account reset affects Org-B account).
- OAuth validation would require forging tokens, attacking signing keys, or altering live identity-provider configuration.
- Evidence requires raw secrets; redact and stop.

## Evidence — chain-step matrix

Record each tested step as a link in the chain:

```text
Step: <password reset token weakness | email change without verification | session fixation | ...>
Test account: <Test-Account-1>
Expected: <token bound to account | email change rejected | session invalidated | ...>
Observed: <token reusable | email changed without MFA | old session still valid | ...>
Chainable: <yes — enables step X | no>
Impact: <isolated weakness | partial ATO chain | full ATO chain>
Confidence: <confirmed | likely | needs-review>
```

Aggregate into an ATO chain map showing:
- each tested pathway and its step results;
- which steps chain together into a full ATO;
- which isolated weaknesses are present but not chainable;
- reproduction boundary: where the chain stops or completes.

Never store: raw reset tokens, session cookies, JWTs, OAuth authorization codes, refresh tokens, recovery links, passwords, or PII.

## Report handoff

When a finding is confirmed:
1. `pentest_agent_record_finding` with the ATO chain path, affected flow, minimal proof, CVSS estimate (8.0–9.8 for full ATO, 5.0–7.0 for isolated weaknesses), and remediation guidance.
2. Reference the chain-step matrix.
3. Recommend: reset token entropy/expiry/one-time-use enforcement, email change requiring password+MFA+verification+notification+cooling-off, session rotation on privilege change, OAuth state parameter enforcement, MFA on all account-modifying actions, and ATO chain detection rules.
