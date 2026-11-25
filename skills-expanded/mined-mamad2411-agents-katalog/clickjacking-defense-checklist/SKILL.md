---
name: clickjacking-defense-checklist
description: >
  Implementation checklist to deploy clickjacking defenses across owned web apps:
  CSP frame-ancestors, X-Frame-Options, embed allowlists, CSRF/SameSite layering,
  path coverage, CDN consistency, and regression tests. Use when rolling out or
  auditing defenses org-wide after assessment — not for offensive PoC (use clickjacking).
---

# Clickjacking Defense Checklist

## Scope And Authorization

- **In scope:** owned web properties and authorized hardening projects.
- **Out of scope:** weakening third-party framing protections; unauthorized testing.
- Roll out in staging first when changing embed allowlists (partner break risk).
- Pair with `clickjacking` for validation methodology and `content-security-policy-design` for full CSP.

## When To Use

- Engineering ticket: “stop clickjacking” / enable frame-ancestors everywhere.
- Audit: ensure all sensitive routes have anti-framing controls.
- Designing intentional embed matrix (who may frame what).
- Tokens: frame-ancestors, X-Frame-Options, embed allowlist, defense checklist.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Offensive assessment / PoC | `clickjacking` |
| JS frame-buster details | `clickjacking-frame-busting` |
| Deep UI redress variants | `clickjacking-ui-redress-deep` |
| Full CSP beyond framing | `content-security-policy-design` |
| Cookie flags | `cookie-security-flags` |

## Defense Layers (use together)

| Layer | Control | Notes |
| --- | --- | --- |
| 1 | CSP `frame-ancestors` | Primary modern control |
| 2 | `X-Frame-Options` | Legacy browsers / defense in depth |
| 3 | CSRF + SameSite | Reduces impact of framed POSTs |
| 4 | Re-auth / step-up | High-risk actions |
| 5 | UX confirms | Not sufficient alone |

## Workflow

### 1. Scope matrix

1. List hostnames and “sensitive” route prefixes (account, admin, billing, OAuth).
2. List **required** framers (if any): parent origins for widgets.
3. Owner per app + CDN/edge team.

### 2. Choose policy per class

| App class | Policy |
| --- | --- |
| No embeds ever | `frame-ancestors 'none'` + `X-Frame-Options: DENY` |
| Same-origin frames only | `frame-ancestors 'self'` + `XFO: SAMEORIGIN` |
| Named partners | `frame-ancestors https://a.example https://b.example` |
| Public marketing only | May allow broader framing; keep **auth app** deny |

### 3. Implement consistently

```http
Content-Security-Policy: frame-ancestors 'none'
X-Frame-Options: DENY
```

```nginx
add_header Content-Security-Policy "frame-ancestors 'none'" always;
add_header X-Frame-Options "DENY" always;
```

1. Apply on **HTML document** responses for app UI (and error pages that host actions).
2. Ensure API JSON responses do not need framing — still fine to send anti-frame headers.
3. Verify CDN/WAF does not strip CSP on cache hits.
4. Merge with existing CSP carefully (one policy or consistent nonces — see CSP skill).

### 4. Checklist execution

- [ ] Sensitive routes listed and classified
- [ ] Embed allowlist documented with owners
- [ ] CSP frame-ancestors set on all app entry HTML
- [ ] X-Frame-Options aligned (DENY/SAMEORIGIN)
- [ ] No obsolete ALLOW-FROM
- [ ] Staging PoC: hostile origin cannot frame
- [ ] Partner embed regression passed
- [ ] CSRF tokens present on state-changing POSTs
- [ ] Session cookies SameSite documented
- [ ] Step-up auth on destructive actions (as required)
- [ ] CI/header scan job for regressions
- [ ] Runbook for adding a new trusted framer

### 5. Automated verification

```bash
# CI-style header check
for u in $SENSITIVE_URLS; do
  echo "== $u"
  curl -sI "$u" | rg -i "content-security-policy|x-frame-options"
done
```

Playwright/Cypress: attempt iframe load from evil test origin → expect block/empty.

### 6. Exceptions

1. Every `frame-ancestors` exception: ticket, owner, expiry/review date, partner contact.
2. Prefer dedicated embed subdomain with minimal privileges over framing full admin app.

### 7. Hand off

1. Publish embed matrix in security wiki.
2. Link findings closed with before/after headers.
3. Schedule quarterly header scan review.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Coverage | All auth UI paths | Only homepage |
| Embeds | Explicit origin allowlist | `*` framing |
| Ops | CI header check | One-time manual curl |
| Exceptions | Time-boxed | Forever partner unknown |
| Depth | CSP + XFO + CSRF | XFO only on one server |

## Output Checklist

- [ ] Scope matrix and embed allowlist complete
- [ ] Policies chosen per app class
- [ ] Headers deployed edge+origin consistently
- [ ] Hostile framing blocked (evidence)
- [ ] Legit embeds verified
- [ ] CSRF/SameSite layer reviewed
- [ ] CI regression in place
- [ ] Exceptions tracked with owners
- [ ] Residual risk documented

## Rules

- Owned apps only for enforcement changes.
- Prefer CSP frame-ancestors; do not rely on JS busting as primary (`clickjacking-frame-busting`).
- Evidence via headers + browser tests.
- This skill is the **rollout checklist**; offensive method stays in `clickjacking`.
