---
name: cloudfront-origin-access-control
description: >
  Lock CloudFront origins with Origin Access Control (OAC) or legacy OAI: S3 bucket
  policies, HTTPS-only viewer policy, custom origin header allowlists, and blocking
  direct public bucket access. Use for owned AWS static sites and media distributions —
  not for probing third-party CloudFront tenants.
---

# CloudFront Origin Access Control

## Scope And Authorization

- **In scope:** CloudFront distributions, S3 buckets, and origins you own.
- **Out of scope:** abusing misconfigured third-party buckets found via scanning.
- Stage policy changes carefully — wrong bucket policy can cause global 403 outage.
- Redact account IDs and internal origin hostnames as needed.
- Pair with `code-quality-standards` for IaC.

## When To Use

- S3 website/static assets should be reachable **only via CloudFront**, not public S3 URL.
- Migrating from legacy **OAI** to **OAC**.
- Custom origins need shared-secret header or IP restrictions in addition to CF.
- Tokens: OAC, OAI, bucket policy, aws:SourceArn, CloudFront distribution, Origin Protocol Policy.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Cloudflare R2 public access | `cloudflare-r2-public-access` |
| WAF rules on distribution | WAF skill |
| General AWS IAM in CFN | `cloudformation-iam-guardrails` |
| SSRF to cloud metadata | `cloud-metadata-ssrf-defenses` |

## OAC vs OAI

| Feature | OAC (preferred) | OAI (legacy) |
| --- | --- | --- |
| Signing | SigV4 to S3 | Special canonical user |
| SSE-KMS | Better support patterns | More awkward |
| New work | Use OAC | Migrate away when possible |

## Workflow

### 1. Confirm scope and success criteria

1. Distribution IDs, origins (S3/custom), whether public read exists today.
2. Success: `https://dxxx.cloudfront.net/...` works; `https://bucket.s3.amazonaws.com/...` denied for public; HTTPS viewer enforced.
3. Rollback: previous bucket policy snapshot; dual-allow during cutover if needed.

### 2. Inventory

```bash
aws cloudfront list-distributions --query "DistributionList.Items[].{Id:Id,Domain:DomainName,Origins:Origins}"
aws s3api get-bucket-policy --bucket my-static-bucket
aws s3api get-public-access-block --bucket my-static-bucket
```

1. Note OAI IDs still attached.
2. List KMS keys if objects encrypted.

### 3. Create OAC and attach

```bash
aws cloudfront create-origin-access-control --origin-access-control-config file://oac.json
# Attach OAC to origin in distribution config; set S3 origin domain to bucket REST endpoint
# (not static website endpoint) when using OAC
```

**Bucket policy pattern (concept):**

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "AllowCloudFrontServicePrincipalRead",
    "Effect": "Allow",
    "Principal": { "Service": "cloudfront.amazonaws.com" },
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-static-bucket/*",
    "Condition": {
      "StringEquals": {
        "AWS:SourceArn": "arn:aws:cloudfront::ACCOUNT:distribution/DIST_ID"
      }
    }
  }]
}
```

1. Enable **S3 Block Public Access** after CloudFront path verified.
2. Remove public `Principal: "*"` GetObject statements.
3. Viewer protocol policy: **redirect-to-https** or https-only.
4. Origin protocol to S3 is HTTPS via CF signing (REST origin).

### 4. Custom origin extras (if not S3)

1. Prefer private ALB/origin in private subnets + restrict to CloudFront prefix lists or secret header.
2. CloudFront origin custom header `X-Origin-Verify: <secret>` checked at origin; rotate secret.
3. Do not rely on header alone without TLS and network controls.

### 5. Verify

```bash
# Via CloudFront — expect 200
curl -sI "https://dxxxx.cloudfront.net/index.html"
# Direct S3 — expect 403
curl -sI "https://my-static-bucket.s3.amazonaws.com/index.html"
# HTTP viewer — expect redirect/403 per policy
curl -sI "http://dxxxx.cloudfront.net/index.html"
```

1. Invalidate cache after policy tests if old public objects cached at CF edge as needed.
2. KMS: confirm CF can decrypt (key policy allows CloudFront/OAC pattern per AWS docs).

### 6. Operate

1. Monitor 403 spikes after policy change.
2. IaC: OAC + bucket policy + public access block as one module.
3. When adding distributions, update bucket policy SourceArn list.

### 7. Hand off

1. Document distribution ↔ bucket mapping.
2. Runbook: rotate origin verify header; add secondary distribution.
3. Decommission OAI after OAC stable.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Bucket | Private + OAC condition | Public ACL “because CDN” |
| Origin domain | S3 REST for OAC | Website endpoint with OAC confusion |
| Viewer | HTTPS redirect | HTTP only |
| Custom origin | Prefix list + secret header | Open 0.0.0.0/0 to world |
| Cutover | Dual-test then block public | Flip public block first |

## Output Checklist

- [ ] Distributions and origins inventoried
- [ ] OAC created and attached (or OAI migration plan)
- [ ] Bucket policy scoped to distribution ARN
- [ ] Public access blocked; direct S3 403 proven
- [ ] CloudFront 200 proven
- [ ] Viewer HTTPS policy set
- [ ] KMS key policy OK if used
- [ ] IaC/runbook updated
- [ ] Residual risks (legacy OAI, second buckets) noted

## Rules

- Owned AWS resources only.
- Prefer reversible cutover with dual verification.
- Evidence via curl 200/403 matrix.
- Focus on **CloudFront↔origin access**; WAF/CDN caching tuning is adjacent.
