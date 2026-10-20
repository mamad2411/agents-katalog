---
name: auth-mfa-bypass
description: MFA enforcement validation — test enrollment, challenge, reset, remember-device, recovery-code, and fallback paths with strict test-account isolation and account-impact safeguards.
disable-model-invocation: true
risk: caution
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# MFA bypass — enforcement posture review

Use this skill to validate MFA enforcement across enrollment, challenge, reset, recovery-code, remember-device, push-notification, and fallback pathways. Every test must use test-owned accounts only. Never prompt, fatigue, social-engineer, or intercept real users. Stop at the first confirmed MFA bypass — do not chain with other ATO vectors from this skill.

## Required inputs

- Written scope naming the target application, identity provider, authorized test accounts (minimum two per MFA tier: no-MFA, TOTP, push, hardware key), allowed MFA validation methods, and explicit permission for account-impact checks.
- User-owned or project-approved test accounts only. Never use borrowed, harvested, shared, or customer accounts.
- Valid authorization cache. Separate explicit permission required for password reset, session manipulation, OAuth linking, and support-flow testing.
- Known rate limits, lockout thresholds, MFA challenge flood limits, testing window, and rollback/escalation contact.
- MFA factor inventory: which factors are enrolled (TOTP, SMS, push, hardware token, backup codes), which are mandatory for which actions, and how recovery works when the primary factor is lost.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview when catalog tools are useful.
5. `pentest_agent_execute_tool` for execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — MFA enrollment mapping

Map the full MFA surface before any active test:
1. Enumerate the MFA enrollment flow: which factor types are offered (TOTP, SMS, push, hardware key, backup codes), whether enrollment is mandatory or skippable, whether the setup key (TOTP seed) is exposed in the UI or API response.
2. Check whether MFA enrollment is required immediately after registration, after first login, or can be deferred indefinitely. A "remind me later" option that can be dismissed forever is a finding.
3. Check whether MFA enrollment can be completed without verifying the factor (e.g., entering a TOTP code before the seed is confirmed). If enrollment succeeds without a valid challenge response, the factor is not actually bound.
4. Enumerate the MFA management page: can MFA be disabled, reset, or changed? What authentication is required to access this page (password, existing MFA, both)?
5. Map all recovery pathways: what happens when the user clicks "lost my device" or "can't access my authenticator"? Is the fallback weaker than the MFA it replaces?

### Phase 2 — MFA enforcement on sensitive actions

For each sensitive action, verify whether MFA is required or can be skipped:
- **Login from new device/browser**: is MFA required on first login from an unrecognized device? Is the "remember this device" flag set without MFA?
- **Password change**: is MFA required before changing the password? If not, a session hijacker can lock out the real user.
- **Email change**: is MFA required before changing the account email? If not, ATO via email change → password reset chain is possible.
- **MFA disable**: is MFA required to disable MFA? If password alone is sufficient, the second factor is cosmetic.
- **MFA reset**: is MFA required to reset MFA? If recovery codes or support flow bypass MFA, the effective security is the weakest recovery path.
- **API key/view**: is MFA required to view or create API keys, OAuth tokens, or application secrets?
- **OAuth linking**: is MFA required to link a new OAuth provider? If not, a session hijacker can add persistent access.
- **Account deletion**: is MFA required to delete the account?

### Phase 3 — challenge-response validation

Test MFA challenge integrity with test-owned accounts:

**TOTP validation:**
1. Record the TOTP setup seed during enrollment (if exposed). Can the seed be retrieved later from the MFA management page?
2. Test whether expired TOTP codes are accepted. Generate a code, wait 60+ seconds, submit.
3. Test whether future TOTP codes are accepted. Generate a code for timestamp + 30 minutes, submit.
4. Test whether the same TOTP code is accepted twice (replay). Submit a valid code, immediately submit it again for another action.
5. Test TOTP window: if the server accepts codes from ±2 windows, the effective entropy is reduced by 5x.

**SMS/voice validation:**
1. Check whether SMS MFA can be bypassed via SIM-swap (out of scope for app testing, but note the risk).
2. Check whether the SMS code is short (4-6 digits) and has a long expiry window. Rate-limit the SMS challenge endpoint.
3. Check whether the voice call MFA reads the code back to the caller (if tested with consent on a test-owned number).

**Push notification validation:**
1. Never test push flooding or MFA fatigue against real users.
2. With a test account, verify whether push notifications require biometric confirmation or can be approved with a single tap.
3. Check whether "deny" on a push notification is treated differently from "ignore/timeout." Does deny lock the account?

### Phase 4 — recovery code and backup pathway

1. Obtain or generate backup/recovery codes for a test account.
2. Check recovery code properties: length (< 8 chars is weak), format (numeric-only has low entropy), quantity (fewer than 8 codes increases risk), single-use enforcement (can a code be used twice?).
3. After using a recovery code, check whether: the user is notified, other sessions are invalidated, MFA is still considered enabled, and the used code is no longer valid.
4. Test whether recovery codes bypass MFA entirely (expected) and whether they also bypass other security controls like IP restrictions or device fingerprinting.
5. Check whether recovery codes can be regenerated without MFA. If regeneration only requires password, MFA is cosmetic.

### Phase 5 — step-skip and parameter tampering

Test API-level MFA bypass vectors on test-owned accounts using the MFA challenge endpoint:

**Response manipulation:**
1. Capture the response after submitting a correct MFA code. Identify the success indicator: HTTP status, JSON field (`verified: true`), redirect target, or session cookie set.
2. Submit an incorrect MFA code. Intercept the response and replace it with the success response. If the server accepts the modified response and issues a valid session, MFA is client-side only.
3. Test with missing MFA code: submit the MFA form with an empty `code` parameter, or omit the `code` field entirely.
4. Test with null/boolean MFA code: submit `code=null`, `code=true`, `code=false`, `code=0`.
5. Test parameter pollution: `code=123456&code=`, `code[]=123456`.

**Step skip:**
1. After completing MFA enrollment flow step 1 (username+password), note the URL for step 2 (MFA challenge). Directly request the post-login dashboard URL. If the server doesn't enforce that step 2 was completed, MFA can be skipped entirely.
2. After completing MFA for one session, open a new browser. Log in with the same credentials. Stop at the MFA prompt. Use the session cookie from the first browser to access the account. If the cookie works without MFA in the new session, sessions are not properly scoped.

### Phase 6 — cross-account and tenant validation

1. Initiate MFA enrollment for Test-Account-1. During enrollment, switch the account identifier to Test-Account-2. If completion succeeds, MFA was enrolled for the wrong account.
2. If MFA enrollment uses a setup token in the URL or API response, test whether that token can be reused for a different account or reveals the account identity.
3. Test whether disabling MFA on Test-Account-1 in Org-A has any effect on Test-Account-2 in Org-A, or on any account in Org-B (tenant isolation).

## Decision points

- **Stop at confirmed bypass**: a single confirmed MFA bypass (step skip, response manipulation, missing enforcement on sensitive action) is a high/critical finding. Do not continue chaining.
- **Escalate on missing MFA enforcement**: if password change, email change, MFA disable, or API key viewing does not require MFA, the finding is critical because it enables full account takeover from session hijack.
- **Escalate on recovery weakness**: if recovery codes are short, reusable, regenerable without MFA, or the support flow bypasses MFA entirely, the finding is high.
- **Downgrade on non-chainable weaknesses**: a 6-digit numeric-only recovery code with no other weaknesses is medium; a long TOTP window with no replay acceptance is medium.

## Prohibited behavior

- MFA fatigue, push bombing, or push flooding against any user account (test or real).
- Social engineering support staff, SIM-swapping, or intercepting real SMS/voice calls.
- Brute-forcing TOTP codes, SMS codes, or recovery codes at scale against live systems.
- Credential stuffing, password spraying, token theft, or session hijacking from real users.
- Triggering SMS/voice/push floods that incur cost or degrade service.
- Storing TOTP seeds, recovery codes, SMS codes, push tokens, or biometric data in raw evidence.

## Stop conditions

- Account lockout from MFA challenge failures.
- SMS/push/voice flood threshold reached — stop immediately to avoid cost or alarm.
- Recovery code exhaustion on a test account.
- Tenant boundary crossing: MFA action in Org-A affects Org-B.
- Evidence would include TOTP seeds, recovery codes, or MFA setup tokens in cleartext → redact and stop.

## Evidence — MFA posture matrix

Record per test vector:

```text
Target: <app name | identity provider>
MFA factor: <TOTP | SMS | push | hardware key | recovery code>
Test vector: <step skip | response manipulation | missing enforcement on email change | code replay | ...>
Test account role: <user | admin | no-MFA | MFA-enrolled>
Expected: <MFA required | code rejected | session not issued>
Observed: <MFA skipped | code accepted | session issued without MFA>
Impact: <no bypass | partial bypass | full MFA bypass>
Chainable: <yes — enables session takeover | yes — enables ATO via email change | no>
Confidence: <confirmed | likely | needs-review>
```

Aggregate into an MFA enforcement posture summary:
- enrollment requirements and factor types supported;
- which sensitive actions are MFA-gated and which are not;
- any confirmed bypass (step skip, response manipulation, parameter tampering);
- recovery pathway weaknesses;
- remediation priority per finding.

Never store: TOTP seeds, recovery codes, SMS codes, push tokens, MFA setup tokens, session cookies, or PII.

## Report handoff

When a finding is confirmed:
1. `pentest_agent_record_finding` with affected MFA vector, minimal proof, CVSS estimate (8.0–9.0 for full MFA bypass enabling ATO, 5.0–7.0 for missing MFA on email change without chain, 3.0–4.0 for non-chainable weaknesses), and remediation guidance.
2. Reference the MFA posture matrix.
3. Recommend: require MFA for all account-modifying actions, short TOTP window with replay prevention, high-entropy single-use recovery codes, MFA required to disable/reset/change MFA, MFA required for OAuth linking and API key access, step enforcement server-side (never rely on client redirect), rate-limit MFA challenges per account and per IP, notify users on MFA change/disable events.
