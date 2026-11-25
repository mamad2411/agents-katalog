---
name: account-lockout-design
description: >
  Design account lockout and progressive auth-failure controls: attempt counters,
  lock duration, dual keys (account + IP), unlock paths, enumeration-safe UX, and
  lockout vs soft rate limits. Use when login lockout policy, failed-attempt thresholds,
  temporary ban after N passwords, progressive delay, or lockout vs rate-limit design
  for owned applications — not for attacking third-party login forms.
---

# Account Lockout Design

## Scope And Authorization

- **In scope:** authentication systems you own or are authorized to harden/test.
- **Out of scope:** using lockout knowledge to DoS third-party accounts; credential stuffing against unowned targets.
- Validate policy changes in staging; lockout misconfiguration can lock all users or enable easy DoS.
- Redact usernames, IPs, and session identifiers from public tickets when required.
- Pair implementation with `code-quality-standards` and rate-limit skills as needed.

## When To Use

- Designing or reviewing login / MFA / password-reset attempt controls.
- Choosing **hard lockout** vs **progressive delay** vs **pure rate limit**.
- Fixing account enumeration via lockout timing or messages.
- Preventing lockout-as-DoS (attacker locks victim by spamming bad passwords).
- Aligning support unlock workflows and audit logs.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| HTTP API rate-limit design (general) | `api-rate-limit-design` |
| Authorized rate-limit bypass testing | `rate-limit-bypass-testing` |
| Full ATO methodology | `account-takeover-methodology` |
| Password-reset token / Host poisoning | `password-reset-poisoning` |
| CAPTCHA / bot challenges | `captcha-bypass-research` (authorized control research) |
| Session fixation | `session-fixation-management` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Control | Behavior | Trade-off |
| --- | --- | --- |
| Soft rate limit | Throttle by IP / device / route | Weak vs distributed stuffing |
| Progressive delay | 2^n backoff after failures | UX friction; still allows slow attacks |
| Account lockout | Block auth for principal after N failures | DoS against victim usernames |
| Dual-key lockout | Thresholds on **account** and **IP/device** | Complexity; better anti-DoS |
| CAPTCHA / proof-of-work | Challenge after risk score | Accessibility and farm costs |
| MFA step-up | Extra factor after anomalies | Needs solid MFA enrollment |

**Enumeration-safe UX:** same generic error and comparable timing for unknown user vs bad password (within reason); avoid “account locked” only for existing users unless product accepts that signal.

## Workflow

### 1. Confirm threats and success criteria

1. Record assets (password login, OTP, recovery codes), user types, compliance needs.
2. Threats: online password guessing, credential stuffing, **lockout DoS**, support social engineering for unlock.
3. Success: brute force impractical online; honest users rarely locked; unlock path audited; no new enumeration oracle.

### 2. Inventory current controls

```bash
# Application / IdP config (examples — adapt to stack)
# - Redis keys for attempts: login:fail:user:{id}, login:fail:ip:{ip}
# - IdP policy (Okta/Auth0/Cognito/Keycloak) lockout settings
redis-cli --scan --pattern 'login:fail:*' | head
```

1. Note counters, TTLs, lock duration, whether counters clear on success.
2. Chart every auth surface: `/login`, `/mfa`, `/token`, `/forgot-password`, mobile grant.
3. Check logging: are failures SIEM-visible without logging raw passwords?

### 3. Choose policy parameters

| Parameter | Starting point (tune with data) | Notes |
| --- | --- | --- |
| Failed attempts before lock | 5–10 per account / window | Lower for admin |
| Lock duration | 15–30 min soft; or exponential | Offer support unlock |
| IP threshold | Higher than account (e.g. 50–100/h) | NAT-friendly |
| Progressive delay | After 3 fails: 1s, 2s, 4s… cap 30s | Server-side enforced |
| Counter store | Redis/Memcached with TTL | Multi-instance safe |
| Admin accounts | Stricter + alert | Never silent infinite |

Document dual-key example:

```text
ON password_failure(user, ip):
  incr user_fail[user] TTL 15m
  incr ip_fail[ip] TTL 15m
  if user_fail[user] >= U_MAX: set user_lock[user] = until
  if ip_fail[ip] >= I_MAX: set ip_throttle[ip] = until
ON password_success(user, ip):
  delete user_fail[user]   # optional: decay instead of delete
  # do not clear ip_fail entirely if shared NAT abuse suspected
```

### 4. Anti-DoS and unlock design

1. Prefer **progressive delay + CAPTCHA/risk** before long account locks for consumer apps.
2. If hard lockout: require unlock via email magic link, MFA, or support with ticket — never unlock via knowledge of only email if email is public.
3. Rate-limit **unlock** and **forgot-password** themselves.
4. Support tooling: break-glass unlock with MFA’d admin, full audit, reason code.
5. For high-value accounts, alert on lock events; consider step-up instead of multi-hour lock.

### 5. Enumeration, timing, and messaging

| Bad | Better |
| --- | --- |
| “User not found” vs “Bad password” | “Invalid email or password” |
| “Account locked” only if user exists | Generic “Try again later” + identical code path cost |
| Faster 404 user path | Constant-time-ish remote checks (best-effort) |

1. Uniform JSON error codes for clients.
2. Do not reveal remaining attempts if that enables optimal attack pacing (product decision; often omit).

### 6. Implement and verify

```bash
# Staging harness (authorized): N bad passwords then observe status
for i in $(seq 1 12); do
  curl -sS -o /dev/null -w "%{http_code}\n" -X POST 'https://staging.example/login' \
    -H 'Content-Type: application/json' \
    -d '{"email":"victim@example.com","password":"wrong"}'
done
# Expect throttling/lock without confirming account existence via unique body
```

**Test matrix:**

| Case | Expected |
| --- | --- |
| N-1 failures then success | Login OK; counter reset/decay |
| N failures | Lock/throttle; no password success |
| Failures from many IPs on one account | Dual-key still protects |
| Failures on many accounts from one IP | IP throttle without locking all victims forever |
| Unlock path | Works once; audited |
| Unknown user | Same client-visible behavior as bad password |

### 7. Observe and hand off

1. Metrics: `auth_failures_total`, `lockouts_total`, unlocks, false lock rate.
2. Alerts: spike in lockouts (stuffing), spike on single account (targeted/DoS).
3. Runbook for support; document policy in security.md for the product.
4. Revisit thresholds after launch using real failure distributions.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Policy | Dual-key + progressive delay | Permanent lock after 3 fails, no unlock |
| DoS | CAPTCHA/risk before hard lock | Attacker locks any email at will |
| UX | Generic errors | Oracle via lock message |
| Storage | Distributed counter with TTL | In-process dict on one of 20 pods |
| Ops | Audited support unlock | Shared “unlock all” SQL without logs |

## Output Checklist

- [ ] Threats and auth surfaces inventoried
- [ ] Thresholds, TTLs, dual keys documented
- [ ] Anti-DoS and unlock paths designed
- [ ] Enumeration-safe messaging/timing reviewed
- [ ] Staging tests for lock, success reset, IP throttle
- [ ] Metrics/alerts defined
- [ ] Support runbook + audit requirements
- [ ] Interaction with MFA/reset rate limits considered
- [ ] `code-quality-standards` on implementation

## Rules

- Authorized design and testing only; do not weaponize lockout against third parties.
- Balance security and availability — lockout is a blunt instrument.
- Enforce delays/locks **server-side**; client-side delays are not controls.
- Never log passwords or full session tokens in lockout telemetry.
- Route pure API quota design and ATO chains to their primary skills.
