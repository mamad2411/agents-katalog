---
name: coop-coep-isolation
description: >
  Design, audit, and remediate Cross-Origin-Opener-Policy (COOP) and
  Cross-Origin-Embedder-Policy (COEP) for browser cross-origin isolation
  (crossOriginIsolated, SharedArrayBuffer, Spectre mitigations). Use when enabling
  or debugging COOP/COEP/CORP, SAB availability, opener nulling, require-corp vs
  credentialless, or process isolation on owned apps — deploy steps also in
  coop-coep-deploy-checklist.
---

# COOP / COEP Isolation

## Scope And Authorization

- **In scope:** owned web applications and authorized header reviews.
- **Out of scope:** breaking isolation on third-party sites; Spectre exploitation.
- Isolation is a **security and capability** boundary — understand embed trade-offs.
- Pair with deploy checklist skill for phased rollout.

## When To Use

- Need `crossOriginIsolated` for SharedArrayBuffer / `performance.measureUserAgentSpecificMemory` etc.
- Auditing opener-based XS-Leaks mitigations via COOP.
- Debugging why SAB is undefined or embeds blank after headers.
- Tokens: COOP, COEP, CORP, crossOriginIsolated, credentialless, same-origin-allow-popups.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Step-by-step rollout checklist | `coop-coep-deploy-checklist` |
| CSP | `content-security-policy-design` |
| Clickjacking | `clickjacking` family |
| Permissions-Policy | feature policy skill / platform docs |

## Header Semantics

### Cross-Origin-Opener-Policy (COOP)

| Value | Effect |
| --- | --- |
| `unsafe-none` (default) | Can retain opener relationships |
| `same-origin` | Isolate from cross-origin openers; new browsing context group |
| `same-origin-allow-popups` | Like same-origin but friendlier to popups you open |

Mitigates some cross-origin window attacks / XS-Leaks via opener.

### Cross-Origin-Embedder-Policy (COEP)

| Value | Effect |
| --- | --- |
| `unsafe-none` | Default |
| `require-corp` | Cross-origin subresources need CORP or CORS approval |
| `credentialless` | Cross-origin no-cors requests without credentials; easier migration sometimes |

### Cross-Origin-Resource-Policy (CORP)

Set on **resources** (images, scripts, documents):

| Value | Who can load |
| --- | --- |
| `same-origin` | Only same origin |
| `same-site` | Same site |
| `cross-origin` | Any (explicit) |

COEP `require-corp` depends on CORP/CORS correctness.

## Isolation Condition

Roughly: **COOP same-origin-ish + COEP active** → `crossOriginIsolated === true` (browser details apply).

```javascript
console.log(crossOriginIsolated);
console.log(typeof SharedArrayBuffer);
```

## Workflow

### 1. Define goals

1. Capability need (SAB) vs security-only COOP.
2. Acceptable breakage for third parties.
3. Success: isolated true **and** product flows work.

### 2. Audit current headers

```bash
curl -sI https://app.example.com/ | rg -i "cross-origin"
# Check subresource responses too (JS/CSS/img CDN)
```

### 3. Design policy set

| Goal | Policy sketch |
| --- | --- |
| Full isolation | COOP same-origin + COEP require-corp + CORP on assets |
| Easier third-party images | COEP credentialless |
| OAuth popups | COOP same-origin-allow-popups |
| No SAB needed | Maybe COOP alone for opener isolation |

### 4. Fix application loading

1. Self-host critical scripts/fonts when CDN lacks CORP.
2. Add `crossorigin` attributes where CORS is used deliberately.
3. Workers/worklets must also comply.
4. Frames: nested documents need compatible policies.

### 5. Verify security properties

1. Cross-origin opener cannot script your window (as designed).
2. Unapproved cross-origin resources blocked under COEP.
3. No accidental `unsafe-none` on HTML entry while APIs assume isolation.

### 6. Report / audit findings

| Finding | Severity theme |
| --- | --- |
| Claimed SAB but not isolated | Functional/security mismatch |
| COEP without CORP → broken app | Availability |
| Missing COOP on sensitive app | Residual opener risk |

### 7. Hand off

1. Use `coop-coep-deploy-checklist` for production phases.
2. Document why isolation is required for future tag managers.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Design | Goal-driven headers | Copy headers from blog without CORP |
| Third parties | Inventory + proxy/self-host | Infinite exceptions |
| Verify | `crossOriginIsolated` | Assume header string enough |
| Popups | Explicit allow-popups choice | Broken IdP login |
| Security | COOP on auth apps | Opener left open “for debug” |

## Output Checklist

- [ ] Isolation goal documented (SAB vs opener)
- [ ] COOP/COEP/CORP values chosen
- [ ] Subresources audited for CORP/CORS
- [ ] Popup/OAuth strategy decided
- [ ] `crossOriginIsolated` verified in target browsers
- [ ] Sensitive flows tested
- [ ] Audit findings or deploy checklist linked
- [ ] Residual non-isolated routes listed

## Rules

- Owned apps only for enforcement.
- Isolation is incomplete without correct subresource policies.
- Prefer evidence from browser APIs over header presence alone.
- Design/audit skill; phased deploy checklist is the sibling.
