---
name: waf-review
description: MUST USE for edge security — Cloudflare WAF, rate limits, bot fight, TLS, Workers auth, geo rules. Triggers on DDoS, credential stuffing, scraping abuse, or CDN/WAF config changes.
---

# WAF Review

The edge is your **volume filter** — stop brute force, scanners, and bots before they hit app CPU. Layer WAF rules with app auth (`auth-review`); neither alone is sufficient.

## When This Skill Applies

- Launching public API or login-heavy app
- Spike in 401/403/429 or origin load
- Cloudflare/Fastly/AWS WAF rule changes
- Workers acting as BFF or auth gateway
- Compliance need for geo block or IP allowlist

## Severity Model

| Level | Signal | Gate |
|-------|--------|------|
| **W0** | No rate limit on login; WAF bypass to admin; SSL mode flexible on auth | Fix immediately |
| **W1** | Missing bot management on auth; no TLS 1.2+; origin IP exposed | Before marketing push |
| **W2** | Over-broad block rules; no logging to SIEM | Sprint |
| **W3** | Cache rules suboptimal | Backlog |

Cross-ref: `auth-review` for account lockout; `harden-vps` if origin reachable directly; `secrets-audit` for leaked origin IPs in DNS history.

## Phase 0 — Traffic Map

| Hostname | Path | Auth? | Cache? | Origin |
|----------|------|-------|--------|--------|

Identify login, signup, password reset, webhooks, API keys.

## Phase 1 — TLS & Origin Protection

- [ ] Full (strict) SSL; valid cert; HSTS with preload consideration
- [ ] Origin only accepts Cloudflare IPs or mTLS — not public internet direct
- [ ] `True-Client-IP` / `CF-Connecting-IP` trusted only at edge-validated hop
- [ ] No sensitive headers forwarded from client unvalidated

```bash
curl -sI https://app.example.com | grep -i strict-transport
# Origin probe (should fail if orange-cloud correct)
curl -sI http://ORIGIN_IP/ -H "Host: app.example.com"
```

## Phase 2 — Rate Limiting & Auth Endpoints

- [ ] `/login`, `/signup`, `/reset` — per-IP + per-path limits (e.g. 10/min/IP)
- [ ] Stricter on failure burst; captcha/Turnstile after threshold
- [ ] API keys: per-key limits at gateway or app
- [ ] Webhooks: verify signature before heavy work — rate limit by sender id

Cloudflare example concepts: Rate Limiting rules, WAF custom rules, Bot Fight Mode / Super Bot Fight.

## Phase 3 — WAF Rules (OWASP-Oriented)

- [ ] Managed rulesets enabled (OWASP, CVE) — tune false positives in log mode first
- [ ] Block common paths (`/.env`, `/wp-admin` on non-WP)
- [ ] SQLi/XSS signals on query/body — log → block progression
- [ ] Geo block only with business justification

## Phase 4 — Workers & Edge Logic (2025–2026)

- [ ] JWT validation at edge only if keys rotated and short-lived — else app remains source of truth
- [ ] No secrets in Worker code git — use secrets store
- [ ] KV/Durable Objects for session/rate limit state — document consistency
- [ ] Observability: Workers analytics + logpush (`observability`)

Cross-ref Cloudflare plugin rules file for Workers patterns.

## Phase 5 — Logging & Response

- [ ] WAF events to SIEM; retain enough for incident replay
- [ ] Custom 429/403 pages — no stack traces
- [ ] Runbook: disable rule id X if false positive during incident

## Output Template

```markdown
## WAF Review: [zone/app]

**Provider:** | **Verdict:** ✅ / 🔶 / ❌

### Edge posture
| Check | Status | Notes |

### Rate limits
| Path | Rule | Limit | Action |

### Gaps
| ID | Sev | Issue | Recommended rule |

### Test results
- Login flood simulated: ...
- Origin direct access: blocked/ exposed

### Follow-ups
- [ ] `auth-review` — account-level throttling
```

## Anti-Patterns

- **WAF only** — no app authz still IDOR
- **Flexible SSL** — MITM risk
- **Block entire country** without product sign-off
- **Rate limit by UA only** — trivially spoofed
- **Logging full Authorization headers**

## Cross-References

| Skill | Use when |
|-------|----------|
| `auth-review` | Credential stuffing at app layer |
| `dependency-audit` | CVE until patched |
| `threat-model` | New public surface |

## Cursor Kit Templates

- `cloudflare`, `anti-bot` — Turnstile, WAF baselines

## Extended Playbook — Cloudflare Rule Patterns

| Pattern | Expression idea | Action |
|---------|-----------------|--------|
| Admin path lock | URI starts with `/admin` AND not IP in allowlist | Block |
| Login rate | URI path equals `/login` | Rate limit 10/min |
| Bot scrape | User agent empty AND path `/api/` | Managed challenge |
| Geo block | Country in {XX} AND not paid tier | Block (document legal) |

Start new rules in **Log** mode 24–48h before **Block**.

## Extended Playbook — Rate Limit Math

Estimate: `peak_login_rps × 60 × generous_factor`. If legitimate peak unknown, measure from access logs:

```bash
# Example log parse (adapt format)
awk '$7 ~ /login/ {print $4}' access.log | cut -d: -f1-2 | sort | uniq -c | sort -rn | head
```

Set threshold above p99 legitimate burst to avoid customer lockout.

## Extended Playbook — Workers Security Checklist

- [ ] `export` routes validate JWT or mTLS
- [ ] KV keys namespaced per tenant
- [ ] No `fetch(userSuppliedUrl)` without SSRF guard (`secure-coding`)
- [ ] Secrets via Wrangler secrets / dashboard — not git
- [ ] CORS on worker API explicit origins

## Extended Playbook — Bot Management Layers

1. **Managed rules** — baseline OWASP/bots
2. **Super Bot Fight / Bot Fight** — login and signup
3. **Turnstile** — human proof at form submit
4. **App layer** — account lockout (`auth-review`)

Document which layer stopped which attack class in runbook.

## Extended Playbook — TLS & HSTS Detail

- Minimum TLS 1.2; prefer 1.3-only where clients allow
- HSTS `max-age` ≥ 31536000 after confident HTTPS everywhere
- Certificate transparency monitoring for rogue certs on your domain

```bash
curl -sI https://app.example.com | grep -i strict-transport-security
openssl s_client -connect app.example.com:443 -servername app.example.com </dev/null 2>/dev/null | openssl x509 -noout -dates
```

## Extended Playbook — Incident Response at Edge

During attack spike:

1. Enable "I'm under attack" or equivalent if available
2. Tighten rate limits temporarily — schedule rollback time
3. Preserve logs to object storage for postmortem
4. Communicate status — don't silently block paying users

Cross-ref: `incident-response`.

## Extended Playbook — False Positive Tuning

When legitimate client blocked:

- Capture rule ID from `cf-ray` support bundle
- Add exception narrower than disable entire rule
- Re-test from client ASN/country

Track false positive rate weekly — high rate means rule too broad.

## Extended Playbook — API vs HTML Posture

| Surface | Edge focus |
|---------|------------|
| Browser HTML | CSRF, cookies, Turnstile on forms |
| JSON API | Token auth, per-key rate limits, no CF cache on auth |
| Webhooks inbound | Signature verify at app; edge rate only |

## Extended Playbook — Verification Matrix

| Test | Expected |
|------|----------|
| Login flood script | 429/challenge before app meltdown |
| Direct origin IP | connection refused or 403 |
| TLS scan | no weak ciphers |
| Admin from non-allow IP | block |

Record results in audit output template.
