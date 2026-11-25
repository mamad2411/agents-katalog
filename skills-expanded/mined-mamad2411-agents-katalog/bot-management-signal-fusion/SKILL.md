---
name: bot-management-signal-fusion
description: >
  Fuse multi-source bot-management signals without sole client trust: server-side
  aggregation of device/TLS/IP/behavior/challenge results, score calibration, action
  policies, feedback loops, and false-positive controls. Use when combining bot scores,
  signal fusion, risk engines, or multi-vendor bot signals on owned applications —
  not for building CAPTCHA farms or attacking third-party defenses.
---

# Bot Management Signal Fusion

## Scope And Authorization

- **In scope:** Bot defense design and evaluation on apps you own or are authorized to assess.
- **Out of scope:** Evading third-party bot defenses for fraud, credential stuffing, scraping bans, or CAPTCHA solving services.
- Prefer staging traffic replay and synthetic bots you control for calibration.
- Redact device IDs, IPs, and account identifiers in reports.
- Pair with `bot-management-signals` for taxonomy; `captcha-bypass-research` only for authorized control testing; `rate-limit-bypass-testing` for attempt budgets.

## When To Use

- Multiple raw signals exist (WAF bot score, JS signals, TLS JA3/JA4, IP reputation, velocity, login outcomes) and need a **single decision**.
- Client-provided “I am human” tokens are over-trusted today.
- High false positives on mobile, corporate NAT, privacy browsers, or accessibility paths.
- Building or reviewing a risk engine that outputs allow / challenge / throttle / block.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Individual signal design / taxonomy | `bot-management-signals` |
| CAPTCHA vendor integration | `captcha-enterprise-integration` |
| Authorized challenge effectiveness tests | `captcha-bypass-research` |
| Pure rate-limit design | `rate-limit-bypass-testing` or rate-limit skills |
| Accessibility of challenges | `captcha-accessibility-balance` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Guidance |
| --- | --- |
| Server authority | Final decision **only** on server with secrets; client scores are inputs |
| Fusion | Weighted / model ensemble of independent signals; avoid double-counting correlated features |
| Calibration | Thresholds from labeled traffic (known good apps, known bad tools you run) |
| Actions | Graduated: allow → soft challenge → hard challenge → throttle → block |
| Feedback | Mark confirmed fraud/ATO and false positives to retrain thresholds |
| Privacy | Minimize persistent cross-site IDs; document legal basis for fingerprints |

## Workflow

### 1. Confirm scope and success criteria

1. Record app surfaces (login, checkout, search, API), regions, SLOs for false-positive rate (FPR) and fraud catch rate.
2. Success: documented fusion formula/policy; no single client field can force allow; FPR under target on holdout.
3. List compliance constraints (GDPR/CCPA fingerprinting notices if applicable).

### 2. Inventory signals and trust boundaries

| Signal | Source | Trust | Notes |
| --- | --- | --- | --- |
| WAF/bot vendor score | Edge | Medium | Vendor opacity; version changes |
| TLS fingerprint | Edge/proxy | Medium | NAT collisions; library churn |
| IP/ASN/reputation | Edge | Low–Med | CGNAT, VPN users |
| JS / device signals | Browser | Low alone | Spoofable; good as corroboration |
| Behavioral velocity | App/server | High-ish | Needs good entity keys |
| Challenge result | Vendor + server verify | High if server-validated | Replay rules matter |
| Auth outcome / ATO labels | App | High labels | Delayed feedback |

```text
# Sketch trust flow
Client headers/cookies → untrusted inputs
Edge signals → semi-trusted
App business events → authoritative labels
Fusion service (server) → decision + reason codes
```

### 3. Baseline current decisions

1. Sample 24–72h of decisions with reason codes (or reconstruct from logs).
2. Measure FPR proxies: challenge rate on known good cohorts (SSO employees, logged-in high-trust).
3. Measure miss proxies: successful credential stuffing patterns, card testing spikes (authorized analytics only).
4. Identify “allow because client said so” paths (hidden fields, localStorage flags, disabled JS).

### 4. Design fusion policy

**Principles:**

1. **No sole client trust:** a perfect client score cannot zero out server velocity anomalies alone.
2. **Independence:** prefer combining edge TLS + server velocity + challenge, not three JS vendor clones.
3. **Explainability:** store top contributing signals for support appeals.
4. **Fail mode:** if fusion service down — documented fail-open (with rate limits) or fail-closed per surface risk.

**Example decision table (illustrative):**

| Composite risk | Login | Search API | Checkout |
| --- | --- | --- | --- |
| Low | Allow | Allow | Allow |
| Medium | Step-up MFA / soft CAPTCHA | Throttle | Soft challenge |
| High | Hard challenge + throttle | Block automation ASNs | Block + review |
| Critical | Block + alert | Block | Block + freeze |

**Pseudo fusion (document real weights in eng design):**

```text
risk = w1*norm(bot_score)
     + w2*norm(velocity_anomaly)
     + w3*norm(ip_risk)
     + w4*norm(tls_rare)
     + w5*(1 - challenge_pass)
     - w6*trusted_session_age
# Cap influence of any single term (e.g. max 0.35)
# Override: confirmed session + device binding may floor risk for step-up instead of block
```

1. Map reason codes to user-visible outcomes (generic messages; no oracle).
2. Ensure CAPTCHA/pass tokens validated **server-side** with one-time semantics (`captcha-enterprise-integration`).
3. Align accessibility alternatives so fusion does not brick a11y users (`captcha-accessibility-balance`).

### 5. Implement server-side enforcement

```text
# Request path checklist
1. Collect edge headers / bot score (strip spoofable client copies of the same)
2. Compute velocity keys: ip, ip+ua, account_id, device_cookie (server-issued)
3. Lookup reputation / prior challenges
4. Fuse → decision + ttl
5. Enforce: block/challenge/allow at gateway or app middleware
6. Log: request_id, decision, top signals, user_id hash — no raw secrets
```

1. Reject client-supplied `X-Bot-Score` unless cryptographically from your edge (signed hop).
2. Bind challenge tokens to action, IP prefix / session, and expiry.
3. Rate-limit challenge issuance to stop solver economics on owned systems.

### 6. Calibrate and verify

```bash
# Authorized load of synthetic good/bad traffic in staging
# Example: k6 or internal bot harness hitting staging only
k6 run staging_bot_fusion_test.js
# Compare decision distributions and FPR dashboards
```

1. Shadow mode: log fusion decision without enforcing; compare to production rules.
2. A/B enforce on low-risk surface first.
3. Support playbook: how to whitelist enterprise NAT ranges temporarily with expiry.

### 7. Feedback loop and handoff

1. Feed confirmed fraud and confirmed false positives weekly into threshold review.
2. Alert on sudden score distribution shifts (vendor model change).
3. Document owners for weights, vendor configs, and appeal process.
4. Apply `code-quality-standards` to fusion service code.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Trust | Server fusion owns decision | `if (body.isHuman) allow` |
| Signals | Diverse layers | Only JS fingerprint |
| Actions | Graduated responses | Binary block for all medium risk |
| FP control | Cohort dashboards + appeals | Ignore mobile WebView users |
| Tokens | One-time server verified | Reusable CAPTCHA tokens |
| Outage | Documented degrade path | Silent open with no rate limit |

## Output Checklist

- [ ] Surfaces, SLOs (FPR/catch), legal constraints recorded
- [ ] Signal inventory with trust levels
- [ ] Baseline decision metrics captured
- [ ] Fusion policy + reason codes documented
- [ ] Server enforcement rejects spoofed client scores
- [ ] Challenge tokens bound and verified server-side
- [ ] Shadow/A-B calibration plan executed
- [ ] Feedback loop and owners assigned
- [ ] Accessibility and fail-mode documented
- [ ] `code-quality-standards` applied if code shipped

## Rules

- Authorized defense and assessment only — not fraud enablement.
- Never trust client-only assertions as the sole allow criterion.
- Minimize and protect biometric/fingerprint-like data; follow privacy policy.
- Prefer explainable reason codes over opaque hard blocks without support paths.
- Keep taxonomy work in `bot-management-signals`; this skill is the fusion/decision layer.
