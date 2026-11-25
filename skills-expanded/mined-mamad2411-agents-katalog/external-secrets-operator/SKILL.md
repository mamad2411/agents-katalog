---
name: external-secrets-operator
description: >
  External Secrets Operator (ESO) for Kubernetes: SecretStore and
  ClusterSecretStore design, ExternalSecret sync, and provider IAM for AWS
  Secrets Manager, HashiCorp Vault, and GCP Secret Manager. Use when wiring or
  reviewing ESO CRDs, dataFrom/extract mappings, IRSA/Workload Identity, or Vault
  Kubernetes auth—not Vault Agent Injector alone.
---

# External Secrets Operator

## Scope And Authorization

- **In scope:** Clusters and secret backends you operate.
- **Out of scope:** Using stolen cloud creds to pull third-party secrets.
- ESO creates Kubernetes Secrets—still RBAC-protect namespaces and etcd encryption.
- Never commit provider static keys in git; prefer IRSA/Workload Identity/K8s auth.
- Pair with `external-secrets-refresh` for refresh/rotation timing and `secrets-management-hygiene`.

## When To Use

- Syncing cloud/Vault secrets into K8s Secrets for apps.
- Designing namespaced SecretStore vs cluster-wide ClusterSecretStore.
- Mapping remote keys to Secret data keys with templates.
- Least-privilege provider access for controllers.
- Replacing hand-managed opaque Secrets in GitOps (without putting values in git).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Refresh interval / rotation UX detail | `external-secrets-refresh` |
| Org secrets program | `secrets-management-hygiene` |
| Vault Agent sidecars | vault-agent-injection if catalogued |
| env 12-factor app loading | `env-config-12factor` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Stores | Prefer namespaced SecretStore; ClusterSecretStore tightly controlled |
| Identity | IRSA / GCP WI / Vault K8s auth over static tokens |
| Mapping | Explicit `data` keys; careful `dataFrom` extract |
| RBAC | Limit who can create ExternalSecret |
| GitOps | Commit CRs only—not secret values |
| Status | Watch Ready conditions and events |

## Workflow

### 1. Confirm scope and success criteria

1. Provider, clusters, namespaces, secret inventory.
2. Success: app pods mount synced secrets; controller least privilege; no static long-lived keys in CRs.

### 2. Inventory ESO install

```bash
kubectl get crd | rg externalsecret
kubectl -n external-secrets get deploy,sa
kubectl get clustersecretstore,secretstore -A
kubectl get externalsecret -A
```

### 3. Design stores and IAM

```yaml
# ClusterSecretStore sketch (AWS SM + IRSA)
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: aws-sm
spec:
  provider:
    aws:
      service: SecretsManager
      region: eu-west-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets
            namespace: external-secrets
```

1. Scope IAM to specific secret ARNs/prefixes per env.
2. For multi-tenant clusters, prefer per-team SecretStore + SA.

### 4. Define ExternalSecret

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: api-creds
  namespace: payments
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-sm
    kind: ClusterSecretStore
  target:
    name: api-creds
    creationPolicy: Owner
  data:
    - secretKey: DATABASE_URL
      remoteRef:
        key: prod/payments/db
        property: url
```

1. Avoid syncing entire secret blobs into broadly readable Secrets.
2. Use templating only when necessary; keep templates reviewed.
3. Set `creationPolicy` / deletion policy intentionally.

### 5. RBAC and GitOps

1. Developers create ExternalSecret in their namespace only.
2. ClusterSecretStore create restricted to platform team.
3. CI validates manifests; never echoes secret values in logs.

### 6. Verify with evidence

```bash
kubectl -n payments get externalsecret api-creds -o yaml | head
kubectl -n payments get secret api-creds -o jsonpath='{.metadata.annotations}' ; echo
# Confirm keys exist without printing values:
kubectl -n payments get secret api-creds -o jsonpath='{.data}' | jq 'keys'
```

1. Rotate value in provider → after refresh, app sees new value (see refresh skill).
2. Deny IAM → ExternalSecret shows error condition (fail closed).

### 7. Hand off

1. Runbook: SecretStore auth failures, provider outages.
2. Dashboards: reconcile errors, age of last sync.
3. Link refresh/rotation procedures.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Auth | IRSA/WI | Static AKIA in SecretStore |
| Scope | Prefix-limited IAM | `secretsmanager:*` on `*` |
| Git | ExternalSecret YAML | Base64 values in git |
| Access | Tight K8s RBAC on Secrets | All SA can read all secrets |
| Stores | Controlled ClusterSecretStore | Every dev creates cluster stores |

## Output Checklist

- [ ] ESO installed and CRDs present
- [ ] Store auth uses workload identity where possible
- [ ] IAM/Vault policy least privilege
- [ ] ExternalSecrets map only needed keys
- [ ] RBAC on stores and secrets reviewed
- [ ] Sync Ready evidence without leaking values
- [ ] Alerts on reconcile failures
- [ ] Residual risk noted

## Rules

- Owned clusters/backends only.
- Never commit secret values.
- Kubernetes Secret is not a vault—control etcd and RBAC.
- Refresh/rotation specifics → `external-secrets-refresh`.
- Redact provider responses in tickets.
