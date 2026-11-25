---
name: cookie-partitioned-chips
description: >
  Implement CHIPS (Cookies Having Independent Partitioned State): Partitioned
  attribute with Secure, cross-site embed scenarios, migration from unpartitioned
  third-party cookies, and debugging partition keys. Use for owned embeds/widgets
  that need state under third-party cookie restrictions — not for tracking users
  across unrelated sites without consent/legal basis.
---

# Cookie Partitioned State (CHIPS)

## Scope And Authorization

- **In scope:** first-party and embed scenarios you own (widgets, payment iframes you control).
- **Out of scope:** designing covert cross-site tracking; testing on sites without authorization.
- Coordinate privacy/legal when third-party cookies are involved.
- Pair with `cookie-security-flags` and `cookie-prefix-host-secure`.

## When To Use

- Your site is embedded cross-site and needs cookies **scoped to top-level site partition**.
- Migrating off unrestricted third-party cookies (browser phaseouts).
- Tokens: CHIPS, Partitioned, partition key, third-party cookie, embed state.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General Secure/HttpOnly/SameSite | `cookie-security-flags` |
| `__Host-` / `__Secure-` prefixes | `cookie-prefix-host-secure` |
| Consent Mode / CMP | `cookie-consent-mode-ops` |
| Clear-Site-Data | `clear-site-data-api` |

## What Partitioned Means

```http
Set-Cookie: widget_session=abc; Secure; Path=/; SameSite=None; Partitioned
```

| Aspect | Behavior |
| --- | --- |
| Requirement | `Secure` required with `Partitioned` |
| Often with | `SameSite=None` for cross-site subrequests |
| Scope | Cookie keyed by **(top-level site, cookie site)** partition |
| Effect | Embed on a.com does not share cookie state with embed on b.com |

## Workflow

### 1. Confirm need

1. Is the cookie for **cross-site embed** UX (logged-in widget) vs first-party app only?
2. First-party-only → prefer host-only Lax/Strict without Partitioned.
3. Success: embed works on partner sites; no leak of cookie across partners.

### 2. Inventory third-party cookie use

```bash
# DevTools → Network → Set-Cookie; Application → Cookies (partition shown in modern Chrome)
curl -sI https://widget.example.com/embed | rg -i set-cookie
```

1. List cookies with `SameSite=None; Secure` today.
2. Note breakage reports under third-party cookie blocking.

### 3. Implement Partitioned

**Server sketch:**

```http
Set-Cookie: __Host-widget=...; Secure; Path=/; HttpOnly; SameSite=None; Partitioned
```

Note: `__Host-` forbids Domain attribute; good for host-only embeds on exact host.

1. Must be HTTPS (`Secure`).
2. JavaScript `document.cookie` write must include `Partitioned` where supported if client-set (prefer HttpOnly server-set).
3. Storage: ensure backend doesn’t assume one global third-party cookie for all sites if product needs isolation — CHIPS enforces isolation.

### 4. Related platform features

| Feature | Relation |
| --- | --- |
| Storage Access API | User-gesture path for unpartitioned access when allowed |
| Related Website Sets | Org-defined related sites — separate design |
| First-party sets legacy | Prefer current browser docs |

### 5. Verify

1. Load embed on two different parent sites → distinct partitions (different cookie jars).
2. With third-party cookies blocked, Partitioned cookies still function for embed use cases per browser support.
3. Missing `Secure` → cookie rejected.
4. First-party navigation to widget origin still behaves as designed.

### 6. Migrate

1. Dual-write transition if needed (careful size limits).
2. Monitor auth failures on embeds after deploy.
3. Document partners that must be on HTTPS.

### 7. Hand off

1. Matrix: cookie name → partitioned? → purpose → retention.
2. Privacy review for embed analytics cookies.
3. Link general flag hardening skill for session cookies on primary app.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Use case | Embed session isolation | Using Partitioned to “fix” consent |
| Flags | Secure + Partitioned | Partitioned over HTTP |
| Scope | Intentional cross-site widget | First-party app cookies unnecessarily None+Partitioned |
| Evidence | Two-parent partition test | Assumed works |
| Privacy | Minimal data in embed cookie | Full profile in third-party embed cookie |

## Output Checklist

- [ ] Cross-site need confirmed
- [ ] Candidate cookies listed
- [ ] Partitioned+Secure implemented
- [ ] SameSite chosen deliberately (often None)
- [ ] Dual-parent isolation verified
- [ ] HTTPS partners only
- [ ] Privacy/legal reviewed if required
- [ ] Residual browser support gaps noted

## Rules

- Owned embeds only; respect consent and privacy law.
- Prefer first-party cookies when embed is not required.
- Evidence from partitioned jar tests.
- CHIPS-focused; general cookie flags and prefixes are siblings.
