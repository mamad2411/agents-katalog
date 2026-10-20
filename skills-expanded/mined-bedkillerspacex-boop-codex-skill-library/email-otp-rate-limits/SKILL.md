---
name: email-otp-rate-limits
description: >
  Design and review rate limits for email one-time passwords: send/resend
  cooldowns, per-destination and dual keys (IP + email), verify attempt budgets,
  enumeration-safe UX, and mail-provider cost controls. Use when email OTP
  throttle, resend cooldown, magic-code limits, inbox flood prevention, or
  verify N for email OTP on owned apps.
---

# Email OTP Rate Limits

## Scope And Authorization

- **In scope:** Auth/notification systems you own; load tests only in non-prod or approved windows.
- **Out of scope:** Flooding third-party inboxes or using OTP endpoints to harass users.
- OTP codes are secrets—never log them; rate-limit keys may hash emails.
- Prefer fail-closed or soft-fail with global caps when Redis is down (document choice).
- Pair with `email-header-injection-defenses` and generic `rate-limit-bypass-testing` for dual-key abuse cases.

## When To Use

- Implementing email OTP / magic code login or step-up verification.
- Stopping inbox flooding, ESP bill shock, or online OTP brute force.
- Reviewing resend buttons and “send code” APIs.
- Fixing user enumeration via differential rate-limit messages or timing.
- Designing Redis/token-bucket keys for auth.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Generic API rate limit framework | `rate-limit-bypass-testing` / rate limit skills |
| Header injection | `email-header-injection-defenses` |
| DMARC ops | `email-dmarc-reporting-ops` |
| SMS OTP specifics | SMS/auth skills if present |
| Account takeover chaining | `account-takeover-methodology` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Send limit | Per email + per IP + global safety cap |
| Resend | Cooldown (e.g. 30–60s) + daily max per destination |
| Verify | Lockout/budget after N wrong codes; progressive delay |
| UX | Same response for unknown emails when anti-enum required |
| Storage | Atomic INCR with TTL; no racey read-modify-write |
| Code | High entropy; short TTL; single use |

## Workflow

### 1. Confirm scope and success criteria

1. Flows: signup, login, passwordless, sensitive action step-up.
2. Success: attacker cannot spray sends or brute codes within budget; legit user can still recover with support path.

### 2. Inventory endpoints and current limits

```bash
rg -n "otp|one.time|verification_code|magic.?link|sendCode|resend" -i --glob '!node_modules'
```

1. Note store (Redis, DB, ESP native limits).
2. Capture current HTTP status on limit (429 vs 200 with generic body).

### 3. Baseline abuse math

| Attack | Without limits |
| --- | --- |
| Send flood to victim email | Harassment + ESP cost |
| Send flood many emails | Account enum + spam |
| Verify brute 6-digit | 1e6 space / online guesses |
| IP rotation | Bypass IP-only throttle |

1. Decide OTP length/entropy (prefer 6–8 digits only with tight verify budgets, or longer alphanumeric).
2. Prefer shorter TTL (5–10 minutes).

### 4. Design dual keys and budgets

```text
send:email:<hmac(email)>   → max 5 / hour, 10 / day
send:ip:<ip>               → max 20 / hour
send:global                → emergency brake
resend:email:<hmac>        → min interval 45s
verify:email:<hmac>        → max 5 failures / code lifetime
verify:ip:<ip>             → max 30 failures / hour
```

```python
# Pseudocode — atomic budget
def allow(key, limit, window_sec):
    n = redis.incr(key)
    if n == 1:
        redis.expire(key, window_sec)
    return n <= limit
```

1. Hash or HMAC emails in keys if raw email in Redis is a privacy concern.
2. On verify success: invalidate code and clear failure counter.
3. On resend: invalidate previous code (or allow only last N) to reduce confusion and window.

### 5. Enumeration-safe responses

1. **Send:** Always return 200 with “if the account exists, a code was sent” when product requires anti-enum—**still enforce** per-email limits only when you accept the send path, or use constant-time dummy work.
2. Avoid “user not found” vs “code sent” splits on OTP login.
3. Captcha after threshold (pair with captcha research skill if needed).

### 6. Verify with evidence

```bash
# Staging only
for i in $(seq 1 10); do
  curl -s -o /dev/null -w "%{http_code}\n" -X POST "$BASE/auth/otp/send" \
    -H 'Content-Type: application/json' \
    -d '{"email":"lab-user@example.com"}'
done
# Expect eventual 429 / error code with Retry-After
```

1. Unit tests for atomic counters and code single-use.
2. Confirm wrong-code budget locks before online brute becomes practical.
3. Chaos: Redis down behavior matches documented policy.

### 7. Hand off

1. Metrics: send count, 429 rate, verify fail rate (no raw codes).
2. Support runbook: unlock legitimate user after lockout.
3. ESP webhook: suppress bounces/complaints feedback loop.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Keys | email + IP + global | IP only |
| Verify | 5 tries / code | Unlimited guesses |
| Resend | 45s cooldown | Instant unlimited resend |
| Logging | event + email hash | Log OTP plaintext |
| Fail mode | Documented soft/hard | Silent open when Redis dies |

## Output Checklist

- [ ] Send/resend/verify budgets defined with TTLs
- [ ] Dual keys implemented atomically
- [ ] Anti-enum UX decided and consistent
- [ ] OTP entropy/TTL/single-use documented
- [ ] Staging burst tests show 429/Retry-After
- [ ] Redis failure mode documented
- [ ] Metrics and support unlock path
- [ ] Residual risk (distributed botnets) noted

## Rules

- Owned apps only; no real inbox abuse.
- Never log or return OTP codes in API errors.
- Rate limits are mandatory for email OTP—not optional polish.
- Prefer short-lived single-use codes with verify budgets.
- Broader ATO → `account-takeover-methodology`.
