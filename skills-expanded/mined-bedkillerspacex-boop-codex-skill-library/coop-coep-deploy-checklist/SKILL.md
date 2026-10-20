---
name: coop-coep-deploy-checklist
description: >
  Deploy Cross-Origin-Opener-Policy and Cross-Origin-Embedder-Policy for cross-origin
  isolation (SharedArrayBuffer, precise timers) without breaking embeds: phased
  headers, CORP on subresources, credentialless option, and verification of
  crossOriginIsolated. Use on owned web apps — conceptual design in coop-coep-isolation.
---

# COOP/COEP Deploy Checklist

## Scope And Authorization

- **In scope:** owned web apps needing cross-origin isolation or opener isolation.
- **Out of scope:** forcing isolation headers on third-party properties without ownership.
- Isolation breaks many third-party embeds — inventory first; use staging.
- Pair with `coop-coep-isolation` for design detail and `code-quality-standards` for app fixes.

## When To Use

- Enabling `window.crossOriginIsolated === true` for SAB / high-res timers.
- Rolling out COOP/COEP/CORP with a release checklist.
- Tokens: COOP deploy, COEP require-corp, CORP, credentialless, isolation rollout.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Design/audit semantics | `coop-coep-isolation` |
| CSP | `content-security-policy-design` |
| Clickjacking frame-ancestors | `clickjacking-defense-checklist` |
| Cookie flags | `cookie-security-flags` |

## Target Headers (typical isolation)

```http
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
# Every cross-origin subresource needs CORP or CORS that satisfies COEP
```

Alternative COEP:

```http
Cross-Origin-Embedder-Policy: credentialless
```

## Deployment Checklist

### Phase 0 — Inventory

- [ ] Why isolation? (SAB, security, Spectre mitigations)
- [ ] Third-party scripts, images, fonts, frames, workers listed
- [ ] Popups/opener flows (OAuth) documented
- [ ] CDN/static origins identified for CORP

### Phase 1 — CORP on static assets

- [ ] First-party static: `Cross-Origin-Resource-Policy: same-origin` or `cross-origin` as needed
- [ ] CDN images/fonts load under COEP rules
- [ ] User uploads domain CORP policy decided

```http
Cross-Origin-Resource-Policy: cross-origin
```

### Phase 2 — COOP (often safer alone first)

- [ ] `COOP: same-origin` or `same-origin-allow-popups` as product requires
- [ ] OAuth popups tested (`allow-popups` variant if needed)
- [ ] `window.opener` nulling acceptable

### Phase 3 — COEP Report-Only / soft

- [ ] Enable COEP in reporting/report-only if available for your stack
- [ ] Fix blocked resources (add CORP, proxy first-party, or remove)

### Phase 4 — Enforce isolation

- [ ] `COEP: require-corp` or `credentialless`
- [ ] `crossOriginIsolated` true in production browsers under test
- [ ] SAB feature works
- [ ] No critical third-party breakage (or accepted)

### Phase 5 — Operate

- [ ] Synthetic check for headers on HTML documents
- [ ] Alert on sudden embed error rates
- [ ] Process for new third-party tags under isolation

## Verification Commands

```bash
curl -sI https://app.example.com/ | rg -i "cross-origin-opener-policy|cross-origin-embedder-policy|cross-origin-resource-policy"
```

Browser console:

```javascript
crossOriginIsolated  // expect true when fully isolated
```

## Common Breakages → Fixes

| Breakage | Fix |
| --- | --- |
| Image/CDN blocked | Send CORP: cross-origin on CDN |
| Frame third-party | Needs CORP + frame permissions; may be impossible — drop or proxy |
| OAuth popup | COOP `same-origin-allow-popups` |
| Analytics script | Replace with isolation-compatible load or first-party proxy |
| Fonts from Google | Self-host fonts with CORP |

## Workflow Summary

1. Confirm need and inventory embeds.
2. CORP on assets → COOP → COEP staged → verify `crossOriginIsolated`.
3. Document exceptions; prefer credentialless when require-corp too strict for partners.
4. Hand off monitoring and change process.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Rollout | Phased checklist | All headers Friday untested |
| Assets | CORP planned | Only set COEP on HTML |
| OAuth | Explicit popup policy | Broken login ignored |
| Verify | `crossOriginIsolated` | Headers present ≠ isolated |
| New tags | Review gate | Marketing injects blocking script |

## Output Checklist

- [ ] Inventory complete
- [ ] CORP on required subresources
- [ ] COOP set and popup flows OK
- [ ] COEP enforced
- [ ] `crossOriginIsolated === true` verified
- [ ] Critical UX (login, pay, edit) tested
- [ ] Monitoring/process for new third parties
- [ ] Residual unisolated pages listed if any

## Rules

- Owned apps only; stage aggressively.
- Headers without CORP on subresources will fail silently in UX.
- Use this as **deploy checklist**; deep semantics in `coop-coep-isolation`.
