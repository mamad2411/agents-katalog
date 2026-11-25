---
name: cloud-metadata-ssrf-defenses
description: >
  Defend applications and workloads against SSRF that reaches cloud instance metadata
  (IMDS): block link-local targets, enforce IMDSv2/hop limits, harden URL fetchers,
  and reduce role blast radius. Use when hardening against 169.254.169.254,
  metadata.google.internal, Azure IMDS, webhook/preview SSRF, or credential theft via
  SSRF — authorized/org-owned systems only. Complements ssrf-server-side-request-forgery.
---

# Cloud Metadata SSRF Defenses

## Scope And Authorization

- **In scope:** owned cloud accounts, apps, labs, authorized assessments.
- **Out of scope:** stealing credentials from third-party cloud tenants; probing IMDS on systems you do not own.
- Prefer staging for IMDSv2 enforcement (may break legacy agents).
- Redact any temporary credentials that appear in test output — rotate if exposed.
- Pair with `ssrf-server-side-request-forgery` for general SSRF and `code-quality-standards`.

## When To Use

- App can fetch attacker-controlled URLs (webhooks, previews, importers, PDF renderers).
- Hardening EC2/ECS/EKS/GCE/Azure IMDS against SSRF credential theft.
- Tokens: IMDS, IMDSv2, 169.254.169.254, metadata.google.internal, hop limit, SSRF.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General SSRF classes / open redirect chains | `ssrf-server-side-request-forgery` |
| Full injection unknown class | `injection-checking` |
| IAM least privilege program-wide | cloud IAM skills |
| Secrets hygiene beyond instance roles | `secrets-management-hygiene` |

## Metadata Endpoints (defense awareness)

| Cloud | Common targets | Notes |
| --- | --- | --- |
| AWS | `http://169.254.169.254/latest/...` | Prefer **IMDSv2** (PUT token) + hop limit 1 |
| GCP | `http://metadata.google.internal/computeMetadata/v1/` | Requires `Metadata-Flavor: Google` |
| Azure | `http://169.254.169.254/metadata/...` | Requires `Metadata: true` |
| Containers | Same link-local from task/pod if routed | Restrict network + task role |

## Defense Layers

| Layer | Controls |
| --- | --- |
| Workload identity | Least-privilege instance/task/pod role; no admin on web tiers |
| IMDS config | AWS IMDSv2 required; HTTP put response hop limit = 1 |
| Network | Block app egress to link-local / metadata from app namespaces where possible |
| Application | URL allowlists; block private/link-local IPs after DNS resolve; no redirects to private |
| Parser safety | Reject weird IPv6/decimal IP forms; pin protocols https/http only as needed |
| Runtime | IMDSv2 in containers; not host network unless required |

## Workflow

### 1. Confirm scope and success criteria

1. Cloud provider(s), compute types, apps with outbound fetch, role ARNs/names.
2. Success: SSRF to metadata fails; legitimate cloud SDK on instance still works if needed; roles minimized.
3. Rollback: dual-stack IMDS optional mode during migration.

### 2. Inventory SSRF sinks and roles

```bash
# Code
rg -n "requests\.(get|post)|urllib|http\.Get|fetch\(|Webhook|preview" 
# AWS example (authorized)
aws ec2 describe-instances --query "Reservations[].Instances[].MetadataOptions"
```

1. List instance profiles / task roles attached to internet-facing apps.
2. Note who still needs IMDS (agents) vs pure app servers.

### 3. Baseline

1. From a **jump/debug** path with authorization, document whether IMDSv1 works.
2. Map sensitive role permissions (s3:*, sts, secretsmanager).
3. Capture existing egress policies.

### 4. Apply cloud hardening

**AWS EC2 (conceptual):**

```bash
aws ec2 modify-instance-metadata-options \
  --instance-id i-... \
  --http-tokens required \
  --http-put-response-hop-limit 1 \
  --http-endpoint enabled
```

1. Set hop limit **1** so containers/SSRF one hop away cannot easily reach IMDS (validate your network model).
2. GCP: ensure only Google headers work (default); restrict SA scopes/permissions.
3. Azure: require Metadata header; restrict managed identity roles.

**Kubernetes:** prefer IRSA/Workload Identity over node IMDS for pods; block `169.254.169.254` via network policy where apps should not need it.

### 5. Harden application fetchers

```text
On each outbound URL:
1) parse scheme (allow http/https only)
2) resolve DNS
3) reject if any IP in: link-local, loopback, private, CGNAT, metadata DNS names
4) connect to resolved IP (not re-resolve open to TOCTOU) or use safe library
5) disable or carefully limit redirects; re-check each hop
6) prefer allowlist of hostnames for webhooks
```

```python
# Pseudocode guard
FORBIDDEN_NETS = ["169.254.0.0/16", "127.0.0.0/8", "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]
# also block metadata.google.internal, ::1, fc00::/7, fe80::/10, etc.
```

1. Unit test: `http://169.254.169.254/`, decimal IPs, DNS rebinding hosts (lab).
2. Do not log full IMDS responses.

### 6. Verify with evidence

```bash
# From app container (authorized): expect fail without token / blocked route
curl -sS -m 2 http://169.254.169.254/latest/meta-data/ || echo blocked
# IMDSv2 token flow should work only where intended (node agent), not via SSRF sink
# App integration tests: webhook URL to metadata denied
```

1. Prove role cannot read unrelated secrets/buckets even if IMDS were reached.
2. Regression: cloud SDKs on hardened instances still function.

### 7. Hand off

1. Document IMDS policy org-wide (SCP/policy-as-code if available).
2. Incident runbook: suspected SSRF credential theft → revoke role sessions, rotate.
3. Continuous tests in CI for URL validator.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| IMDS | v2 required + hop 1 | IMDSv1 forever |
| Roles | Minimal task role | Admin on web ASG |
| SSRF filter | Post-DNS IP checks | Hostname blacklist only |
| Redirects | Revalidate each hop | Follow blindly |
| Evidence | Blocked fetch tests | “WAF maybe blocks” |

## Output Checklist

- [ ] SSRF sinks inventoried
- [ ] Compute metadata options hardened
- [ ] Network/policy blocks where appropriate
- [ ] URL fetcher guards + tests
- [ ] Roles least-privilege reviewed
- [ ] Verification evidence captured (no live secrets stored)
- [ ] Incident revoke path documented
- [ ] Residual risk (legacy agents) ticketed

## Rules

- Authorized systems only; treat any leaked temp creds as incident.
- Prefer defense in depth: identity + IMDS + app + network.
- Focus on **metadata SSRF**; general SSRF methodology is the companion skill.
- Never paste live cloud credentials into notes.
