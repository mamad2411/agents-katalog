---
name: captcha-bypass-research
description: >
  Authorized CAPTCHA and bot-challenge control research: when challenges bind, client-trust
  gaps, reusable tokens, logic skips, accessibility/alternate paths, and rate-limit
  interplay. Use for labs, CTFs, and scoped assessments measuring control effectiveness —
  not fraud, credential stuffing, ticket scalping, or CAPTCHA-farm abuse.
---

# Captcha Bypass Research

## Scope And Authorization

- **In scope:** CAPTCHA/bot challenges on systems you own, lab apps, CTFs, or written-scope assessments measuring **your** control quality.
- **Out of scope:** Bypassing CAPTCHAs on third-party sites for fraud, account takeover, scraping-for-sale, scalping, or operating CAPTCHA-solving farms.
- Goal is **defense improvement evidence**, not weaponized bypass kits.
- Redact site keys/secrets; never publish live production secret keys.
- Pair with `rate-limit-bypass-testing`, `bot-management-signal-fusion`, `captcha-enterprise-integration`.

## When To Use

- Validating that server-side verification is mandatory and non-replayable.
- Finding logic skips: endpoints that omit challenge checks.
- Testing token binding (action, hostname, IP/session, one-time use).
- Assessing alternate paths (a11y, partner API, mobile) for weaker enforcement.
- Purple-team exercises on owned bot defense.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Installing vendor CAPTCHA | `captcha-enterprise-integration` |
| Accessibility balance design | `captcha-accessibility-balance` |
| Signal taxonomy | `bot-management-signals` |
| General bug bounty process | `bug-bounty-methodology` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Control question | Why it matters |
| --- | --- |
| Where enforced? | Client-only checks are not controls |
| Token one-time? | Reuse = automation scale |
| Bound to action? | Login token used on transfer |
| Hostname/sitekey match? | Dev keys on prod or vice versa |
| Fail open? | Vendor outage → unrestricted |
| Rate limits behind? | CAPTCHA without limits still spammable |
| Alternate APIs | Mobile/BFF missing verify |

## Workflow

### 1. Confirm authorization and success criteria

1. Written scope, allowed accounts, rate limits on testing, data handling.
2. Success: findings with repro on owned staging; remediations ticketed; no production abuse.
3. Stop rules: no bulk credential stuffing; no paid solver services against third parties.

### 2. Map challenge placement

```text
Browser widget → client token → server verify with secret → business action
                 ↘ missing verify on some routes?
```

```bash
# Owned staging only — find verify endpoints and client sites
rg -n "siteverify|recaptcha|hcaptcha|turnstile|captcha" -g '*.{py,js,ts,go,java,rb}'
```

1. List all state-changing routes that should require challenges.
2. Identify mobile/public API variants.

### 3. Baseline legitimate flow

1. Complete challenge as a normal user; capture token (redact in notes).
2. Observe server request: verify call to vendor or crypto check.
3. Record TTL and whether token appears single-use.

### 4. Authorized test cases (defensive checklist)

| ID | Test | Expected secure result |
| --- | --- | --- |
| T1 | Omit token field | Reject |
| T2 | Empty / garbage token | Reject |
| T3 | Replay same token twice | Second reject |
| T4 | Token from action A on action B | Reject |
| T5 | Token issued for host A on host B | Reject |
| T6 | Old expired token | Reject |
| T7 | Forge client field `captchaPassed=true` | Ignore client; reject |
| T8 | Hit alternate API without CAPTCHA | Same policy as web or stronger |
| T9 | Complete widget only; block server verify (lab) | Action fails closed |
| T10 | High-rate attempts after pass | Rate limit still applies |

1. Document exact requests (sanitized) and responses.
2. Prefer staging site keys; never extract production secrets for “ease”.

### 5. Analyze residual bypass classes (for fixing)

| Class | Remediation direction |
| --- | --- |
| Missing server verify | Enforce verify middleware on all mutating routes |
| Shared secret in client | Impossible for real verify — use server secret |
| Replayable tokens | One-time store (nonce) + short TTL |
| Unbound tokens | Verify action/hostname claims from vendor response |
| Fail-open on vendor 500 | Fail closed or constrained allowlist + rate limit |
| Solver economics | Risk-based + rate limit + device signals; not CAPTCHA alone |

### 6. Report for defenders

1. Severity by abuse scalability (account creation spam, login stuffing assist, etc.).
2. Evidence: single-account minimal PoC.
3. Fix verification steps for developers.
4. Do **not** ship a public “universal bypass” tutorial for third-party sites.

### 7. Retest and hand off

1. After fix, re-run T1–T10.
2. Add automated contract tests for omit/replay/unbind.
3. Link a11y path testing so fixes do not brick assistive users.
4. Apply `code-quality-standards` on middleware changes.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Intent | Improve owned controls | CAPTCHA farm against random sites |
| PoC | Staging, one token replay | Mass account creation |
| Client trust | Prove `passed=true` ignored | “Widget UI is enough” |
| Scope | Written RoE | Assumed public program allows solvers |
| Reporting | Fix-oriented | Sell bypass to criminals |
| Limits | CAPTCHA + rate limit | CAPTCHA as only control |

## Output Checklist

- [ ] Authorization documented
- [ ] Challenge map + routes complete
- [ ] Baseline legitimate verify observed
- [ ] T1–T10 (or subset) executed with evidence
- [ ] Findings severity + remediations filed
- [ ] Retest after fix
- [ ] Automated regression tests added
- [ ] No production secrets published
- [ ] Rate-limit and a11y interactions noted

## Rules

- Defense measurement and authorized assessment only — not fraud enablement.
- Minimal impact PoCs; respect rate limits and data privacy.
- Never recommend CAPTCHA-solving services for unauthorized targets.
- Server-side verification is the control; UI widgets are not.
- Integration how-to lives in `captcha-enterprise-integration`.
