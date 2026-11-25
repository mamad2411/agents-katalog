---
name: external-dns-ownership
description: >
  kubernetes-dns ownership for owned Kubernetes DNS: domain filters, TXT registry
  ownership records, txt-owner-id, policy upsert-only vs sync, provider IAM
  least privilege, and preventing cross-cluster record clobber. Use when
  external-dns, dnsEndpoints, or multi-cluster DNS ownership.
---

# external-dns Ownership

## Scope And Authorization

- **In scope:** DNS zones and clusters you own; provider credentials under your control.
- **Out of scope:** Pointing external-dns at zones you do not own; hijacking third-party domains.
- Misconfig can delete or overwrite production DNS—use upsert-only and filters first.
- Redact provider secrets and zone IDs in tickets.
- Pair with DMARC/email DNS ops only when those records are in-scope separately.

## When To Use

- Installing or hardening kubernetes-dns for Services/Ingress/Gateway.
- Multiple clusters writing to the same zone.
- Migrating ownership (`txt-owner-id`) between clusters.
- Restricting which domains external-dns may manage.
- Incident: unexpected DNS changes from automation.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Email DMARC records content | `email-dmarc-reporting-ops` |
| Generic DNS takeover recon | recon skills (authorized) |
| External Secrets for tokens | `external-secrets-operator` |
| cert-manager DNS01 depth | cert-manager skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Domain filter | Explicit allowlist of domains/zones |
| Registry | TXT ownership records (`heritage=external-dns,...`) |
| owner id | Unique per cluster/controller |
| Policy | `upsert-only` safer; `sync` can delete |
| Sources | ingress/service annotations only as intended |
| IAM | Least privilege per zone |

## Workflow

### 1. Confirm scope and success criteria

1. Zones, clusters, who may create DNS.
2. Success: each record has clear owner id; no cross-cluster clobber; IAM scoped; dry-run evidence.

### 2. Inventory controllers

```bash
kubectl -n external-dns get deploy,args -o yaml 2>/dev/null | head
kubectl get deploy -A -o yaml | rg -n "external-dns" -n
# Provider side: list recent record changes if available
```

1. List `--domain-filter`, `--txt-owner-id`, `--policy`, `--registry`.
2. Note annotation filters (`--annotation-filter`).

### 3. Baseline risk

| Config | Risk |
| --- | --- |
| No domain-filter | Manages unintended zones if creds allow |
| Shared owner-id across clusters | Fight over records |
| policy=sync | Deletes records not seen in cluster |
| Broad IAM `* on *` | Blast radius |

### 4. Apply ownership controls

```yaml
# Helm values sketch
domainFilters:
  - "apps.example.com"
txtOwnerId: "cluster-prod-a"
policy: upsert-only   # start here
registry: txt
txtPrefix: "edd-"     # optional clarity
sources:
  - ingress
  - service
```

1. **Unique** `txtOwnerId` per controller instance.
2. Prefer separate subzones per cluster/environment (`prod.apps.`, `staging.apps.`).
3. IAM: only `ChangeResourceRecordSets` on intended hosted zone IDs (AWS example).
4. Use annotation filters so only opted-in Ingresses are published.

### 5. Multi-cluster patterns

1. Split zones or prefixes—avoid two sync controllers on same FQDNs.
2. If shared zone required: different owner ids and non-overlapping hostnames.
3. Migration: change owner carefully; understand registry TXT rewrite behavior; prefer blue/green hostnames.

### 6. Verify with evidence

```bash
# Dry run if supported by your chart/version
# kubectl logs deploy/external-dns -n external-dns | tail
dig +short service.apps.example.com
dig TXT e-service.apps.example.com   # ownership txt shape varies by config
```

1. Create test Ingress → record appears with expected owner metadata.
2. Delete Ingress under upsert-only → confirm **no** unexpected mass deletes of unrelated names.
3. Confirm second cluster cannot alter first cluster’s names.

### 7. Hand off

1. Runbook: break-glass DNS change when controller down.
2. Alert on external-dns errors and unexpected IAM denials.
3. Document zone → cluster ownership map.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Filter | Explicit domainFilters | All zones in account |
| Owner | Unique txtOwnerId | Default same everywhere |
| Policy | upsert-only until trusted | sync day one on shared zone |
| IAM | Zone-scoped | `Route53:*` on `*` |
| Hostnames | Non-overlapping | Two clusters same hostname |

## Output Checklist

- [ ] Zones and clusters mapped
- [ ] domainFilters set
- [ ] Unique txtOwnerId per controller
- [ ] Policy chosen and documented
- [ ] IAM least privilege
- [ ] Test record + dig evidence
- [ ] Multi-cluster collision reviewed
- [ ] Residual risk noted

## Rules

- Only zones you own.
- Prefer upsert-only and narrow filters before sync deletes.
- Unique ownership IDs are mandatory multi-cluster.
- Treat provider credentials as high-value secrets.
- Secrets injection → `external-secrets-operator`.
