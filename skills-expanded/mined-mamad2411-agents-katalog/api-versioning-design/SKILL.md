---
name: api-versioning-design
description: >
  Design and evolve HTTP/RPC API versions: URL path vs header vs media-type versioning,
  compatibility rules, deprecation, sunset, and client migration. Use when API versioning,
  接口版本, v1/v2 paths, API-Version header, breaking change policy, or deprecation timelines.
  Not for offensive API recon alone.
---

# API Versioning Design

## Scope And Authorization

- **In scope:** Public/partner/internal APIs your organization publishes.
- **Out of scope:** Breaking third-party APIs; using versioning notes to attack legacy endpoints without auth.
- Version changes need product + engineering governance.
- Pair with `api-documentation-writing` and `code-quality-standards`.

## When To Use

- Introducing v1/v2 or header-based versions.
- Writing breaking-change and deprecation policy.
- Migrating clients off legacy shapes.
- Avoiding “stealth breaks” that strand partners.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| OpenAPI writing quality | `api-documentation-writing` |
| API recon of legacy paths | `api-recon-and-docs` |
| Gateway routing only | `api-gateway-authz-patterns` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Strategy | Example | Pros | Cons |
| --- | --- | --- | --- |
| Path | `/v1/orders` | Very visible | URL sprawl |
| Header | `API-Version: 2024-01-01` | Clean paths | Less discoverable |
| Media type | `Accept: application/vnd.example.v2+json` | HTTP-native | Harder for some clients |
| Date versions | Stripe-like | Fine-grained | Many concurrent versions |

**Breaking vs non-breaking:** additive fields usually OK; renames/removals/meaning changes are breaking.

## Workflow

### 1. Confirm policy and success criteria

1. Who consumes API (mobile, partners, internal)?
2. Success: published compatibility rules; one clear versioning scheme; deprecation timeline SLA; metrics of version usage.
3. Choose **one** primary strategy for new APIs.

### 2. Write compatibility rules

| Change | Classification | Action |
| --- | --- | --- |
| Add optional field | Non-breaking | Document |
| Add required field | Breaking | New version |
| Remove field | Breaking | New version + deprecation |
| Change type/meaning | Breaking | New version |
| New endpoint | Non-breaking | Same version |
| Error code change clients branch on | Often breaking | Careful |

### 3. Implement routing

```text
# Path style
/v1/* -> service handlers v1
/v2/* -> service handlers v2

# Header style
API-Version: 2  -> negotiate
default version documented if header missing
```

```nginx
# Conceptual
location /v1/ { proxy_pass http://api_v1; }
location /v2/ { proxy_pass http://api_v2; }
```

1. Shared auth/rate-limit across versions when possible.
2. Avoid silent default flips that break old mobile apps.

### 4. Deprecation and sunset

```http
Deprecation: true
Sunset: Sat, 01 Nov 2026 00:00:00 GMT
Link: <https://docs.example.com/migrate-v2>; rel="successor-version"
```

1. Announce: changelog, email partners, portal banner.
2. Minimum support window (e.g. 6–12 months) per policy.
3. Metrics: request % by version; chase stragglers.

### 5. Documentation and examples

1. Separate OpenAPI per major version or clear version selector.
2. Migration guide: field mapping table, sample diffs.
3. SDKs pin versions explicitly.

### 6. CI and contract tests

```bash
# Example: spectral lint both specs
npx spectral lint openapi.v1.yaml
npx spectral lint openapi.v2.yaml
# Contract tests for each supported version in CI
```

1. Prevent accidental breaking changes in “stable” version via tests.
2. Canary: reject PRs that remove fields from v1 without process.

### 7. Hand off

1. Version policy page linked from docs root.
2. Owners for each major version.
3. Kill plan for versions below traffic threshold after sunset.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Scheme | One clear approach | Mix path+header randomly per team |
| Breaks | New version + guide | Quiet field removal Friday night |
| Sunset | Headers + dates + metrics | Eternal unmaintained v0 |
| Defaults | Stable documented default | Mobile breaks on server default change |

## Output Checklist

- [ ] Versioning strategy chosen and documented
- [ ] Breaking change definition published
- [ ] Routing implemented consistently
- [ ] Deprecation/sunset process defined
- [ ] Migration guides for active breaks
- [ ] Usage metrics by version
- [ ] Contract tests protect stable versions
- [ ] Docs/SDKs aligned
- [ ] `code-quality-standards` applied

## Rules

- Owned APIs only.
- Prefer additive evolution; version when breaking.
- Communicate early; measure adoption.
- Do not keep infinite versions without owners.
- Security fixes may need backport policy to supported versions.
