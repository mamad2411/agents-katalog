---
name: clear-client-hints
description: >
  Control Client Hints privacy on owned sites: Accept-CH / Critical-CH / Permissions-Policy
  allowlists, high-entropy hints (UA-CH, device-memory, viewport-width), and reducing
  passive fingerprinting. Use when tightening Client Hints delegation, third-party
  access, or migrating from frozen User-Agent — not for fingerprinting users without consent.
---

# Clear Client Hints

## Scope And Authorization

- **In scope:** web properties you own; privacy hardening and feature design under org policy.
- **Out of scope:** maximizing fingerprint entropy against users; injecting hints on third-party sites.
- Prefer staging to validate layout/CDN behavior when changing Critical-CH.
- Redact raw high-entropy hint values from public tickets when unnecessary.
- Pair header config with `code-quality-standards` and privacy review.

## When To Use

- Configuring **Accept-CH**, **Critical-CH**, **Permissions-Policy** for Client Hints.
- Migrating logic off legacy User-Agent strings to **UA Client Hints** (`Sec-CH-UA-*`).
- Reducing third-party / iframe access to high-entropy hints.
- Tokens: Client Hints, Accept-CH, Critical-CH, Sec-CH-UA, device-memory, DPR, viewport-width, Permissions-Policy.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Clear-Site-Data on logout | `clear-site-data-api` |
| Cookie security flags | `cookie-security-flags` |
| CSP design | `content-security-policy-design` |
| COOP/COEP isolation | `coop-coep-isolation` |
| Generic privacy program | org privacy / compliance skill |

## Hint Classes (practical)

| Class | Examples | Guidance |
| --- | --- | --- |
| Low entropy / common | `Sec-CH-UA`, `Sec-CH-UA-Mobile`, `Sec-CH-UA-Platform` | Often enough for analytics feature detection |
| High entropy | `Sec-CH-UA-Model`, full version lists, `Device-Memory`, `Viewport-Width`, `DPR` | Request only if product-critical; document purpose |
| Network | `Downlink`, `ECT`, `RTT`, `Save-Data` | Adaptive loading; avoid long-term profiling storage |
| Delegated | hints available to cross-origin subresources | Use Permissions-Policy / feature policy carefully |

## Workflow

### 1. Confirm scope and success criteria

1. Sites/apps in scope, CDN/edge owner, legal/privacy constraints (GDPR/CCPA).
2. Success: only needed hints requested; third parties cannot freely read high-entropy hints; features still work.
3. Rollback: previous Accept-CH set via CDN config.

### 2. Inventory current Client Hints usage

```bash
curl -sI https://www.example.com/ | rg -i "accept-ch|critical-ch|permissions-policy|document-policy"
# Browser DevTools → Network → request headers Sec-CH-*
```

1. List which **Sec-CH-*** headers clients actually send today.
2. Grep app code/CDN for `navigator.userAgentData`, `getHighEntropyValues`, Accept-CH injection.
3. Map third-party scripts that may consume hints (tags, fraud, ads).

### 3. Baseline privacy and product needs

1. For each hint: purpose, retention, and whether low-entropy alternative exists.
2. Note critical first-paint needs (may justify **Critical-CH** — use sparingly; can add latency).
3. Record any consent requirements before high-entropy collection.

### 4. Apply allowlist configuration

**Minimal first-party pattern (edge/app headers):**

```http
Accept-CH: Sec-CH-UA, Sec-CH-UA-Mobile, Sec-CH-UA-Platform
Permissions-Policy: ch-ua-model=(), ch-device-memory=(), ch-viewport-width=(self)
```

**If a specific high-entropy value is required:**

```http
Accept-CH: Sec-CH-UA, Sec-CH-UA-Mobile, Sec-CH-UA-Platform, Sec-CH-UA-Model
Critical-CH: Sec-CH-UA-Model
Permissions-Policy: ch-ua-model=(self)
```

**Application-side (feature detection preference):**

```javascript
// Prefer UA-CH over legacy UA string parsing
const ua = navigator.userAgentData;
if (ua) {
  const { brands, mobile, platform } = ua;
  // Request high entropy only with need + preferably after consent policy
  // const high = await ua.getHighEntropyValues(["model", "platformVersion"]);
}
```

1. **Default deny** high-entropy: do not Accept-CH everything “just in case”.
2. Use Permissions-Policy to block cross-origin frames/scripts from ch-* features where unsupported use is risky.
3. Avoid storing raw model/viewport fingerprints indefinitely; aggregate if analytics only.
4. Coordinate with CDN: some POPs strip or cache vary on CH — set **Vary** correctly when responses differ by hints.

### 5. Verify with evidence

```bash
curl -sI https://www.example.com/ | rg -i "accept-ch|critical-ch|permissions-policy|vary"
# Chrome: chrome://flags not required on modern stable — use DevTools
# Confirm third-party origin does NOT receive high-entropy Sec-CH-* on subrequests
```

1. First navigation vs subsequent: Accept-CH takes effect on later requests unless Critical-CH used.
2. Iframe third-party: confirm restricted hints absent.
3. Feature tests: responsive images / adaptive bitrate still acceptable without excess hints.

### 6. Observe and harden

1. Monitor breakage (wrong asset quality) vs privacy metrics (fewer high-entropy fields logged).
2. Review tag manager changes that re-enable broad Accept-CH.
3. Document data processing for any retained CH-derived fields.

### 7. Hand off

1. Publish allowlist of permitted hints + owners.
2. CDN/app config in Git; pair with privacy DPIA if required.
3. Apply `code-quality-standards` to any JS using `getHighEntropyValues`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Accept-CH | Minimal set for product | Accept-CH: *everything* |
| Critical-CH | Rare, justified | Critical on many hints (latency) |
| Third parties | Policy deny by default | Full CH delegation to ads |
| Logging | Coarse buckets | Store raw model+viewport forever |
| Migration | UA-CH brands API | Fragile UA regex only |

## Output Checklist

- [ ] Sites and privacy constraints recorded
- [ ] Current Sec-CH / Accept-CH inventory done
- [ ] Per-hint purpose documented
- [ ] Allowlist headers deployed (Accept-CH, Permissions-Policy)
- [ ] Critical-CH used only if justified
- [ ] Third-party access verified restricted
- [ ] Vary/caching behavior checked at CDN
- [ ] Retention of CH-derived data reviewed
- [ ] Rollback path documented

## Rules

- Owned sites only; do not use this skill to improve covert tracking.
- Prefer least hints necessary; evidence of need over speculative collection.
- Coordinate privacy + performance when using Critical-CH.
- Focus on Client Hints control; cookie/CSP/logout clearing are separate skills.
