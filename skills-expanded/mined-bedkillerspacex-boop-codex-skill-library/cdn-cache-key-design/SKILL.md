---
name: cdn-cache-key-design
description: >
  Design CDN cache keys for owned properties: include/exclude query params, headers
  (Vary), cookies, device classes, normalization, and auth content separation. Use when
  CDN cache key, CloudFront/Fastly/Cloudflare cache key, query string whitelist, or
  preventing cache fragmentation and data leaks.
---

# Cdn Cache Key Design

## Scope And Authorization

- **In scope:** CDN configurations and origins you operate.
- **Out of scope:** Poisoning or probing third-party CDN caches without authorization.
- Miskeyed caches can leak personalized content — treat as security-sensitive.
- Pair with `caching-strategies`, `cdn-waf-bypass-awareness`, `code-quality-standards`.

## When To Use

- Configuring which query strings/headers/cookies enter the cache key.
- Fixing low hit ratio from over-fragmentation or wrong content from under-keying.
- Separating authenticated vs anonymous content safely.
- Normalizing keys (`/` vs `/index.html`, case, duplicate params).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General multi-layer caching | `caching-strategies` |
| WAF/CDN bypass testing awareness | `cdn-waf-bypass-awareness` |
| Stampede at app layer | `cache-stampede-defense` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Key component | Include when | Risk if wrong |
| --- | --- | --- |
| Scheme/host/path | Always (normalized) | Collisions |
| Selected query params | Param changes body | Serve wrong variant / miss storm |
| `Accept-Encoding` | Compressed variants | Broken encoding |
| `Accept-Language` | True language variants | Fragmentation if unused |
| `Authorization` / cookies | Rarely in **shared** cache | **User A sees user B** if mishandled |
| Custom headers | API versioning | Fragmentation |

## Workflow

### 1. Confirm scope and success criteria

1. CDN vendor, properties, public vs private content, hit-ratio targets.
2. Success: documented key policy; no cross-user leaks; hit ratio improved without wrong variants.
3. List personalization mechanisms (cookies, auth headers, geo).

### 2. Inventory current key behavior

```bash
# Observe what CDN varies on
curl -sI "https://www.example.com/p?a=1&b=2" | rg -i "cache|age|vary|x-cache|cf-cache|x-served"
curl -sI "https://www.example.com/p?b=2&a=1" | rg -i "age|x-cache"
```

1. Export CDN cache key settings (CloudFront policies, Fastly VCL/Compute, Cloudflare Cache Rules).
2. Measure cardinality of query params in logs.
3. Find accidental `Vary: *` or cookie-keyed HTML.

### 3. Classify content

| Class | Cache | Key notes |
| --- | --- | --- |
| Immutable static | Long public | Path + encoding only; ignore junk QS |
| Public pages | Public short TTL | Whitelist marketing QS (`utm_*` often **exclude**) |
| Personalized HTML | Private / bypass | Do not store in shared cache |
| API JSON public | Careful | Version header/param in key |
| API authed | no-store / private | Never shared key by cookie session |

### 4. Design query string policy

**Prefer allowlist** of query params that affect content:

```text
# Include in key
id, page, sort, lang
# Exclude from key (and optionally strip at edge)
utm_source, utm_medium, fbclid, gclid, _ga
```

1. Excluding tracking params raises hit ratio without content change.
2. If app uses unknown params to change content, fix app — don’t key on all params forever.
3. Normalize order and encoding so `?a=1&b=2` == `?b=2&a=1` when both included.

### 5. Headers and cookies

1. **Do not** put session cookies into shared cache keys.
2. If logged-in HTML differs, `Cache-Control: private, no-store` or split cookie-less bare site vs app.
3. `Vary: Accept-Encoding` typically required; add `Vary: Accept-Language` only if HTML truly varies.
4. Device keys: prefer Client Hints carefully or separate m-dot only if needed — high fragmentation.

**Auth leak anti-pattern:**

```text
BAD: shared cache key = URL only; origin returns personalized body based on Cookie
→ User B receives User A cached page
FIX: never cache personalized responses on shared CDN; or include auth in key AND ensure not shared across users (essentially private)
```

### 6. Implement on CDN (patterns)

| Vendor concepts | Direction |
| --- | --- |
| CloudFront | Cache policy: query allowlist; headers; cookies none |
| Cloudflare | Cache Rules; Query String; eligible headers |
| Fastly | `req.url` normalization in VCL; `Vary` |
| Akamai | Cache ID modification / include params |

```text
# Normalization sketch
- lowercase host
- strip default ports
- drop fragment
- sort allowlisted query params
- strip session query tokens
```

### 7. Verify and hand off

```bash
# Same content keys collide positively
curl -sI "https://cdn.example/p?id=1&utm_source=x" 
curl -sI "https://cdn.example/p?id=1&utm_source=y"
# Expect second HIT if utm excluded

# Personalization leak test (two sessions)
# Must not share private HTML
```

1. Hit ratio and origin offload dashboards.
2. Alert on sudden drop (rule misdeploy) or rise in 4xx from bad key.
3. Document policy in runbook; apply `code-quality-standards` to IaC CDN configs.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| QS | Allowlist content params | Key on all query strings |
| Tracking | Strip utm from key | Millions of utm variants |
| Auth | private/no-store personalized | Cookie-based body on public cache URL key |
| Vary | Minimal true variants | `Vary: User-Agent` whole browser zoo |
| Normalize | Sorted params | Order-sensitive keys |
| Docs | Policy table | Tribal edge rules |

## Output Checklist

- [ ] Content classes mapped
- [ ] Current key/Vary inventory done
- [ ] Query allowlist/denylist defined
- [ ] Cookie/header policy safe for auth
- [ ] Normalization rules specified
- [ ] CDN config applied via reviewable IaC
- [ ] Hit ratio + leak tests executed
- [ ] Runbook updated
- [ ] `code-quality-standards` applied

## Rules

- Never serve personalized content from a shared cache key that ignores identity.
- Prefer query allowlists; exclude tracking noise.
- Minimize `Vary` cardinality.
- Authorized CDN configs only.
- Broader cache strategy → `caching-strategies`.
