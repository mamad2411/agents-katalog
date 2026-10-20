---
name: cross-origin-opener-policy
description: >
  Assess and implement Cross-Origin-Opener-Policy (COOP) for browsing-context
  isolation: same-origin, same-origin-allow-popups, unsafe-none, pairing with
  COEP for crossOriginIsolated / SharedArrayBuffer, and popup/OAuth breakage.
  Use when hardening window.opener isolation, Spectre-era cross-origin isolation,
  or verifying COOP+COEP on owned apps — hand framing to clickjacking skills,
  links to coop-noopener-links, CORS to cors-credentialed-requests.
---

# Cross-Origin-Opener-Policy (COOP)

## Scope And Authorization

- **In scope:** Web applications and edge header configs you own or are authorized to harden/test.
- **Out of scope:** Forcing COOP on third-party sites; breaking partner OAuth without coordination.
- Validate in staging: COOP breaks some popup `window.opener` / `postMessage` flows.
- Pair with `coop-noopener-links` for `rel=noopener` on anchors; `code-quality-standards` for app changes.

## When To Use

- Setting `Cross-Origin-Opener-Policy` on app shells, auth pages, or admin UIs.
- Enabling `crossOriginIsolated` (needs COOP + COEP) for `SharedArrayBuffer` / high-res timers.
- Reducing residual process-sharing / opener-based attacks beyond `rel=noopener`.
- Debugging OAuth/SSO popups broken after security headers rollout.
- Reviewing interaction with `Cross-Origin-Embedder-Policy` and `Cross-Origin-Resource-Policy`.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| `rel=noopener` on links only | `coop-noopener-links` |
| Clickjacking / frame-ancestors | clickjacking / CSP frame skills |
| Credentialed CORS | `cors-credentialed-requests` |
| nginx header inventory broadly | `nginx-security-headers` |
| Implementation quality baseline | `code-quality-standards` |

## Header values

| COOP value | Effect (summary) |
| --- | --- |
| `unsafe-none` | Default; may retain opener relationships |
| `same-origin` | Cross-origin popups/windows severed from opener; strongest isolation |
| `same-origin-allow-popups` | Isolates document but allows it to retain references to popups it opens (common for OAuth) |

Related:

| Header | Role |
| --- | --- |
| COEP `require-corp` / `credentialless` | Cross-origin subresources must explicitly allow embedding |
| CORP | Resource-side permission for embedding |
| CSP | Orthogonal content controls |

`window.crossOriginIsolated === true` typically requires COOP `same-origin` (+ appropriate COEP).

## Workflow

### 1. Confirm scope and success criteria

1. List top-level documents (SPA shell, login, static marketing).
2. Inventory popup flows: OAuth, payments, print, support chat.
3. Success: chosen COOP deployed; critical popups work; isolation level meets threat model; documented exceptions.

### 2. Baseline headers and opener behavior

```bash
curl -sSI 'https://app.example.local/' | rg -i 'cross-origin-opener|cross-origin-embedder|cross-origin-resource|content-security'
```

Browser:

1. Open DevTools → Application / frame tree; check `crossOriginIsolated`.
2. From a test page, `window.open` cross-origin URL; inspect whether `opener` is null under current policy.

### 3. Choose policy

| App type | Starting recommendation |
| --- | --- |
| High-security app shell without popups | `same-origin` |
| App with OAuth popup needing handle | `same-origin-allow-popups` |
| Gradual rollout / unknown third parties | Report-Only if available in your stack, or stage first |
| Needs SharedArrayBuffer | `same-origin` + COEP plan |

### 4. Implement (examples)

```nginx
add_header Cross-Origin-Opener-Policy "same-origin-allow-popups" always;
# Only when ready for isolation + COEP:
# add_header Cross-Origin-Opener-Policy "same-origin" always;
# add_header Cross-Origin-Embedder-Policy "require-corp" always;
```

```js
// Express
res.setHeader('Cross-Origin-Opener-Policy', 'same-origin-allow-popups');
```

COEP rollout often requires `crossorigin` attributes and CORP on CDNs — treat as a multi-week project.

### 5. Test breakage matrix

| Flow | Test |
| --- | --- |
| OAuth popup | Login completes; tokens/`postMessage` received |
| `window.closed` polling | Still functions as designed |
| External `target=_blank` links | No functional need for opener; pair with noopener skill |
| Embedded admin in portal | May open browsing context groups differently — verify |
| BFCache | Note COOP can affect cache eligibility in some browsers |

### 6. Verify isolation goals

```bash
curl -sSI 'https://app.example.local/app' | rg -i 'cross-origin-opener-policy'
```

In console on app origin:

```js
console.log(self.crossOriginIsolated);
console.log(document.featurePolicy || 'n/a');
```

### 7. Hand off and monitor

1. Document why `allow-popups` was chosen if not full `same-origin`.
2. Coordinate CDN/cache: headers must not be stripped.
3. Monitor auth failure rates after enablement.
4. Link noopener link defaults separately — COOP does not replace them for all cases.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| OAuth | `same-origin-allow-popups` tested | `same-origin` blind in prod |
| Isolation goal | Explicit threat model | Copy headers from blog without COEP plan |
| SAB enablement | COOP+COEP staged | COEP require-corp without CORP on assets |
| Marketing site | May use weaker COOP | Same strict policy breaking partners unnecessarily |
| Evidence | curl + popup test checklist | Header present ⇒ “secure” |

## Output Checklist

- [ ] Documents and popup flows inventoried
- [ ] Baseline headers captured
- [ ] COOP value selected with rationale
- [ ] Staging verification of auth/popups
- [ ] COEP/CORP plan if isolation required
- [ ] Production headers verified via curl
- [ ] CDN preserves headers
- [ ] Exceptions documented
- [ ] Link/noopener work tracked or done
- [ ] Residual Spectre/isolation limits understood

## Rules

- COOP is not clickjacking protection (use CSP frame-ancestors / XFO).
- Coordinate identity providers before enforcing strict COOP on login hosts.
- Authorized apps only.
- Focus on **COOP (and isolation pairing)**; route CORS and link rel elsewhere.
