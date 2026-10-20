---
name: bot-management-signals
description: >
  Design bot-management signal pipelines: signal taxonomy, collection points, risk
  scoring inputs, action thresholds (allow / challenge / throttle / block), feedback
  loops, privacy, and false-positive controls. Use when bot score design, device or
  TLS fingerprints as risk signals, bot management rules, challenge step-up policy,
  or anti-automation signal architecture for owned applications and authorized assessments.
---

# Bot Management Signals

## Scope And Authorization

- **In scope:** Designing and reviewing bot signals on applications you own or are authorized to test.
- **Out of scope:** Building evasion tooling against third-party sites, CAPTCHA farms, or credential stuffing kits.
- Use synthetic automation you control in staging for signal QA.
- Redact raw fingerprints, IPs, and account IDs in external docs.
- Hand multi-signal decision engines to `bot-management-signal-fusion`; CAPTCHA products to enterprise/a11y skills.

## When To Use

- Standing up a first bot-management program or vendor integration inputs.
- Defining **what** is collected (taxonomy) and **where** (edge, CDN, app, client).
- Mapping signals to preliminary risk bands before fusion complexity.
- Privacy/DPIA inputs for device fingerprinting and behavioral analytics.
- Debugging why good users get challenged (signal quality, not fusion math).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Multi-signal score fusion / decision engine | `bot-management-signal-fusion` |
| CAPTCHA vendor install | `captcha-enterprise-integration` |
| Authorized bypass research on your controls | `captcha-bypass-research` |
| Rate-limit mechanics | rate-limit skills / `rate-limit-bypass-testing` |
| Accessibility of challenges | `captcha-accessibility-balance` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Layer | Example signals | Spoofability |
| --- | --- | --- |
| Network/edge | IP, ASN, geo, rate, TLS JA3/JA4, HTTP/2 fingerprints | Medium |
| Vendor bot score | Managed rules, known bad bots, ML score | Vendor-dependent |
| Client JS | WebGL, fonts, automation `navigator.webdriver`, events | High alone |
| Application | Account age, password fail velocity, payment velocity | Lower if server-side |
| Challenge | CAPTCHA/passkey step-up success | Low if verified server-side |
| Outcome labels | Chargeback, ATO confirm, unlock true-positive | Labels for training |

## Workflow

### 1. Confirm scope and success criteria

1. List protected endpoints and abuse cases (credential stuffing, scraping, carding, spam accounts).
2. Success: written taxonomy; collection map; retention; preliminary thresholds; FP budget.
3. Name privacy owner for fingerprint retention and user disclosure.

### 2. Build signal taxonomy

| ID | Name | Entity key | Freshness | Storage |
| --- | --- | --- | --- | --- |
| S1 | Edge bot score | request | real-time | log 30d |
| S2 | IP velocity | ip/24 + path | 1m windows | redis |
| S3 | Account fail rate | user_id | 10m | redis |
| S4 | TLS fingerprint rarity | ja4 | daily stats | analytics |
| S5 | Device cookie trust | server cookie | session | redis/db |
| S6 | Challenge pass | token id | one-time | ephemeral |

1. Prefer **server-issued** device cookies over pure client fingerprints for trust elevation.
2. Document correlation risk (same signal counted thrice under different names).
3. Mark each signal PII/personal data classification.

### 3. Map collection points

```text
Client page → JS agent (optional) → origin headers
     ↓
CDN/WAF → bot score, TLS, IP rules → forward signed headers
     ↓
API gateway / app middleware → velocity + auth context
     ↓
Risk log / SIEM → offline analytics + threshold tuning
```

```bash
# Staging: inspect which bot headers your edge injects (names vary by vendor)
curl -sI "https://staging.example/login" | sed -n '1,40p'
# Confirm clients cannot set the same header on a direct-to-origin path
```

1. Close direct-origin bypasses so clients cannot skip edge signals.
2. Sign or mTLS edge→origin if bot headers are trusted.
3. Ensure APIs (mobile, partners) have signal plans — not only web.

### 4. Define preliminary actions per surface

| Surface | Low risk | Medium | High |
| --- | --- | --- | --- |
| Login | Allow | Challenge / MFA | Block + lock heuristics |
| Sign-up | Soft challenge | Hard challenge | Block disposable patterns |
| Search/API | Rate limit | Stricter quota | Block |
| Checkout | Allow + fraud ML | 3DS / review | Block |

1. User messaging must not reveal exact signal thresholds (oracle prevention).
2. Provide support runbooks for enterprise shared IPs.
3. Accessibility: always define non-visual path (`captcha-accessibility-balance`).

### 5. Instrument and baseline

1. Log: `request_id`, surface, signal bag (hashed/bucketed), decision, latency.
2. Dashboards: challenge rate, block rate, login success, support contacts tagged “bot false positive”.
3. Cohort slices: mobile app, privacy browser, country, ASN, logged-in vs anonymous.

```text
# Minimum metrics
bot_challenge_total{surface,reason}
bot_block_total{surface,reason}
bot_signal_missing_total{signal_id}   # detect agent outages
login_success_rate{cohort}
```

### 6. Quality-control signals

| Failure mode | Detection | Mitigation |
| --- | --- | --- |
| JS agent blocked | Spike `signal_missing` | Server-only path + challenge |
| Vendor score shift | Distribution drift alert | Shadow thresholds |
| NAT mega-users | One IP many good accounts | Account/device keys |
| Automation spoofing webdriver | Over-reliance on one flag | Multi-signal |
| Header spoof | Direct origin hits | Network policy |

1. Regularly replay authorized synthetic bots and known-good monitors.
2. Never ship debug endpoints that echo full fingerprint JSON publicly.

### 7. Hand off to fusion and operations

1. Freeze v1 taxonomy; version signal schemas (`signal_schema_version`).
2. Pass stable feature list to `bot-management-signal-fusion` for composite decisions.
3. Document retention, deletion, and legal contact.
4. Apply `code-quality-standards` to collection middleware.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Taxonomy | Versioned IDs + entity keys | Ad-hoc log fields per engineer |
| Trust | Edge signed scores | Trust `X-Forwarded-Bot: false` from client |
| Coverage | Web + mobile API | Only homepage JS widget |
| Privacy | Retention + purpose limit | Infinite raw canvas hashes |
| Ops | Missing-signal alerts | Silent empty scores → allow all |
| Thresholds | Cohort-aware | Global block on one IP reputation list |

## Output Checklist

- [ ] Abuse cases and surfaces listed
- [ ] Signal taxonomy table complete with retention
- [ ] Collection points and origin-bypass checks done
- [ ] Action matrix draft per surface
- [ ] Logging/metrics for decisions and missing signals
- [ ] Privacy/legal review triggered if needed
- [ ] Synthetic good/bad validation plan
- [ ] Handoff notes to fusion skill
- [ ] `code-quality-standards` for implementation

## Rules

- Defense design and authorized testing only.
- Treat client signals as adversarial inputs.
- Prefer graduated controls over permanent IP bans for ambiguous medium risk.
- Do not claim “undetectable bots” or teach third-party evasion.
- This skill owns taxonomy/collection; fusion owns composite decisions.
