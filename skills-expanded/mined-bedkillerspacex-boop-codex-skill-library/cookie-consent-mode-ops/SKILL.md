---
name: cookie-consent-mode-ops
description: >
  Operate cookie consent and Google Consent Mode (v2) with a CMP: default denied
  states, update on user choice, tag firing rules, region behavior (EEA/UK), and
  verification that ads/analytics cookies respect consent. Use for owned marketing
  stacks and privacy compliance engineering — not for circumventing consent or
  dark-pattern “accept all” traps. Pair with cookie-security-flags for auth cookies.
---

# Cookie Consent Mode Ops

## Scope And Authorization

- **In scope:** sites/tags you own; CMP contracts your org controls.
- **Out of scope:** bypassing consent on third-party sites; falsifying consent signals.
- Coordinate legal/privacy for lawful bases; this skill is technical ops.
- Redact consent IDs if tied to personal data in tickets.
- Auth session cookies are **not** marketing tags — see `cookie-security-flags`.

## When To Use

- Implementing **Consent Mode** + CMP (OneTrust, Cookiebot, custom, etc.).
- Fixing tags that fire before consent.
- Tokens: Consent Mode v2, ad_storage, analytics_storage, CMP, TC string, gtag consent.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Session Secure/HttpOnly/SameSite | `cookie-security-flags` |
| CHIPS / Partitioned | `cookie-partitioned-chips` |
| Cookie name prefixes | `cookie-prefix-host-secure` |
| Clear-Site-Data logout | `clear-site-data-api` |

## Consent Mode Signals (Google ecosystem)

| Signal | Controls (typical) |
| --- | --- |
| `ad_storage` | Ads cookies |
| `analytics_storage` | Analytics cookies |
| `ad_user_data` | User data sent to ads (v2) |
| `ad_personalization` | Personalized ads (v2) |
| `functionality_storage` / `personalization_storage` / `security_storage` | Optional finer categories |

Default in EEA often **denied** until update.

## Workflow

### 1. Confirm scope and success

1. Sites, regions, CMP vendor, GTM/gtag presence, legal requirements.
2. Success: before accept → no non-essential cookies from tags; after accept → expected tags; withdraw works.
3. Map essential vs non-essential cookies (document owners).

### 2. Inventory tags and cookies

```bash
# Browser DevTools Application → Cookies; Network for Set-Cookie from third parties
# GTM preview mode: which tags fire on load vs consent events
```

1. List cookies set on first landing without interaction.
2. Identify tags not consent-aware.

### 3. Default deny + CMP wiring

```javascript
// Conceptual gtag defaults BEFORE CMP loads
gtag("consent", "default", {
  ad_storage: "denied",
  analytics_storage: "denied",
  ad_user_data: "denied",
  ad_personalization: "denied",
  wait_for_update: 500,
});
// On CMP accept:
gtag("consent", "update", {
  ad_storage: "granted",
  analytics_storage: "granted",
  ad_user_data: "granted",
  ad_personalization: "granted",
});
```

1. Load CMP early; block marketing tags until update.
2. Region-specific defaults if policy requires (EEA vs Americas).
3. Respect prior consent storage (CMP cookie) on return visits — still allow withdraw.

### 4. GTM configuration patterns

1. Consent Overview: require appropriate checks per tag.
2. Additional consent checks for custom HTML tags.
3. Avoid injecting raw marketing scripts outside GTM without consent gates.

### 5. Verify

| Scenario | Expect |
| --- | --- |
| Fresh EU user, no click | No ads/analytics storage cookies from Google tags |
| Accept all | Tags fire; cookies appear as designed |
| Reject all | Stay denied; advanced/modeled measurement only if product policy allows |
| Withdraw | Cookies cleared/not renewed per CMP; signals denied |

```text
Tools: GTM Preview, Tag Assistant, browser empty profile, DevTools cookie jar
```

### 6. Operate

1. Change control for new tags — consent category required in request form.
2. Monitor CMP downtime: fail **closed** (stay denied), not open.
3. Audit quarterly cookie inventory vs policy.
4. Document data processing with vendors (DPA).

### 7. Hand off

1. Runbook: add tag, debug premature fire, CMP outage.
2. Owners: marketing eng + privacy + web platform.
3. Do not weaken auth cookie security while tuning marketing consent.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Default | Denied in regulated regions | Granted until opt-out only where unlawful |
| Tags | Consent-aware in GTM | Hard-coded pixels in HTML head always |
| UX | Clear reject equal ease | Dark patterns (illegal/unethical) |
| Outage | Fail closed | Fail open “for revenue” |
| Auth cookies | Separate essential path | Stuffing session into marketing CMP |

## Output Checklist

- [ ] Cookie/tag inventory complete
- [ ] Consent defaults set before tags
- [ ] CMP update path wired
- [ ] GTM consent checks on marketing tags
- [ ] Accept/reject/withdraw verified in clean browser
- [ ] Region behavior documented
- [ ] Fail-closed on CMP failure
- [ ] Quarterly audit scheduled
- [ ] Legal/privacy sign-off noted where required

## Rules

- Owned stacks only; do not defeat user consent.
- Fail closed for non-essential processing when uncertain.
- Essential auth cookies ≠ marketing consent toys.
- Focus on **consent mode ops**; cookie security flags are sibling skills.
