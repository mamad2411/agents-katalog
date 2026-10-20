---
name: cloudflare-r2-public-access
description: >
  Control Cloudflare R2 public access: private buckets by default, public bucket URL
  vs custom domain, token/ACL least privilege, signed URLs/Workers gateways, CORS, and
  preventing accidental data exposure. Use on owned R2 buckets — not for scanning
  others’ buckets or weakening object storage on systems out of scope.
---

# Cloudflare R2 Public Access

## Scope And Authorization

- **In scope:** R2 buckets and CF accounts you own.
- **Out of scope:** enumerating third-party buckets; uploading malware; unauthorized data access.
- Prefer private buckets + controlled exposure; review legal/privacy before public objects.
- Redact access key IDs/secrets and account IDs in tickets.
- Pair with `cloudflare-workers-bindings` for Worker-mediated access.

## When To Use

- Publishing static assets via R2 public access or custom domain.
- Locking down a bucket that was mistakenly public.
- Designing presigned/Worker-authenticated downloads for private objects.
- Tokens: R2, public bucket, custom domain, S3-compatible API, presign, CORS.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Workers bindings | `cloudflare-workers-bindings` |
| D1 databases | `cloudflare-d1-basics` |
| Access Zero Trust for apps | `cloudflare-access-policies` |
| AWS S3 OAC/CloudFront | `cloudfront-origin-access-control` |
| Generic secrets | `secrets-management-hygiene` |

## Access Modes

| Mode | Use | Risk |
| --- | --- | --- |
| Private (default) | Sensitive data, backups | Lowest public risk |
| Public bucket URL | Truly public assets | Any object readable if key known/listed |
| Custom domain + public | CDN-friendly public assets | Same + cache/CDN config |
| Worker gateway | Authz, signed links, transforms | Code bugs = exposure |
| S3 API tokens | Server-side tools | Long-lived keys if leaked |

## Workflow

### 1. Confirm scope and success criteria

1. Bucket names, data classification, intended public object prefixes.
2. Success: non-public data not world-readable; public assets only under allowlisted prefixes; tokens least privilege.
3. Rollback: disable public access toggle; rotate API tokens.

### 2. Inventory

```bash
npx wrangler r2 bucket list
# Dashboard: R2 → bucket → Settings → Public access
# Audit tokens: R2 API tokens with Admin Read/Write
```

1. List objects with sensitive prefixes (`backups/`, `customer/`, `exports/`).
2. Note CORS rules and custom domains.

### 3. Baseline exposure test

```bash
# If public URL exists:
curl -sI "https://pub-xxxxx.r2.dev/some-object"
# Expect 404/403 for private; 200 only for intentional public objects
# Try listing if applicable — listing should not expose private catalogs
```

### 4. Configure safely

**Public assets pattern:**

1. Separate buckets: `assets-public` vs `data-private` (preferred over mixed).
2. Enable public access **only** on the public bucket.
3. Attach custom domain with TLS; set cache rules as needed.
4. Object naming: unguessable keys **not** a substitute for private when data is sensitive.

**Private data pattern:**

1. Public access **off**.
2. Serve via Worker that checks session/Access JWT then `env.BUCKET.get(key)`.
3. Or generate short-lived signed URLs from trusted backend.

**Token least privilege:**

| Token capability | When |
| --- | --- |
| Object Read | CDN warmer / backup reader |
| Object Read & Write | Deploy pipeline for public assets only |
| Admin | Break-glass only |

```toml
# wrangler — private binding example
[[r2_buckets]]
binding = "PRIVATE_BUCKET"
bucket_name = "data-private"
```

### 5. CORS (only if browsers upload/read cross-origin)

```json
[
  {
    "AllowedOrigins": ["https://app.example.com"],
    "AllowedMethods": ["GET", "HEAD"],
    "AllowedHeaders": ["*"],
    "MaxAgeSeconds": 3600
  }
]
```

1. Avoid `AllowedOrigins: *` with credentialed patterns.
2. Do not enable write CORS from untrusted origins.

### 6. Verify

1. Private object without auth → deny.
2. Public asset → 200 and correct `Content-Type`.
3. Random key enumeration does not yield sensitive exports.
4. Old tokens revoked after rotation work fail.
5. Worker path: unauthorized user cannot read private keys.

### 7. Operate

1. Alert/monitor on bucket public access changes (audit log).
2. Periodic scan: public buckets + unexpected object ACL-like configs.
3. Incident: disable public access, rotate tokens, review access logs, notify if PII exposed.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Layout | Separate public/private buckets | One public bucket with `/secrets` |
| Auth | Worker/Access/signed URL | “Secret URL path” only |
| Tokens | Scoped + rotated | Account-wide admin in CI forever |
| CORS | Explicit app origin | `*` + PUT from anywhere |
| Evidence | curl 403/200 matrix | Assumed private |

## Output Checklist

- [ ] Buckets classified public vs private
- [ ] Public access disabled on sensitive buckets
- [ ] Public assets limited and tested
- [ ] Tokens least-privilege and vaulted
- [ ] Worker/signed access path verified for private data
- [ ] CORS reviewed
- [ ] Audit monitoring for config changes
- [ ] Incident steps documented
- [ ] Residual risk (cache TTL of removed objects) noted

## Rules

- Owned R2 only; treat accidental public buckets as incidents.
- Prefer separate buckets over clever prefixes.
- Never commit R2 secrets.
- Focus on **R2 public access control**; Workers/D1/Access are siblings.
