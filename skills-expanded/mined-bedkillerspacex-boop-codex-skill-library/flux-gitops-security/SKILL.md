---
name: flux-gitops-security
description: >
  Flux GitOps security for owned/authorized clusters: source trust (Git/OCI), multi-tenant
  path and namespace isolation, controller and impersonation RBAC, secrets decryption
  (SOPS/age/ESO), image automation and admission pins, and notification webhook hygiene.
  Use when hardening or reviewing Flux v2 bootstrap, GitRepository/OCIRepository,
  Kustomization/HelmRelease, flux-system ServiceAccounts, decrypt keys, or GitOps repo
  branch protection before or after continuous reconcile.
---

# Flux GitOps Security

## Scope And Authorization

- **In scope:** Kubernetes clusters and Git/OCI sources you own or are authorized to secure.
- **Out of scope:** compromising other orgs’ GitOps pipelines or planting malicious manifests in repos without authorization.
- Git write access ≈ cluster admin—protect accordingly.
- Redact decrypt keys, tokens, and webhook secrets.
- Pair manifests with `code-quality-standards`.

## When To Use

- Bootstrapping or reviewing **Flux v2** (`flux-system`).
- Threat modeling continuous reconcile from Git/OCI to cluster state.
- Multi-tenant path restrictions, Kustomization `.spec.path`, service account impersonation.
- SOPS/age decryption keys and notification providers.
- Before enabling image automation (pair with `flux-image-automation`).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Image repo tag automation detail | `flux-image-automation` |
| Binary auth / admission image pins (GCP) | `gcp-binary-authorization` |
| Secrets program broadly | `secrets-management-hygiene` |
| General K8s priv-esc | container/K8s skills in catalog |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Resource | Trust impact |
| --- | --- |
| GitRepository / OCIRepository / Bucket | What code can enter cluster |
| Kustomization / HelmRelease | What applies where; decryption; SA |
| ImageRepository / ImagePolicy / ImageUpdateAutomation | Who can move tags in Git |
| Provider / Alert | Webhook authenticity |
| RBAC for controllers | Blast radius if controller compromised |

## Threats

| Threat | Control |
| --- | --- |
| Malicious PR merged to main | Branch protection, reviews, signed commits optional |
| Deploy from wrong path | `path` + `targetNamespace` + deny cluster-admin apps in tenant repos |
| Secret plaintext in Git | SOPS/ESO; sealed secrets patterns |
| Overpowered reconcile SA | Impersonate least-privilege SA per Kustomization |
| Spoofed git host | Known hosts, pinned deploy keys, OCI sig verify when used |
| Notification SSRF/spam | Scoped tokens; no secret echo |

## Workflow

### 1. Confirm scope and success criteria

1. Clusters, Flux version, tenancy model, Git orgs, secret strategy.
2. Success: only protected refs reconcile; tenant cannot apply beyond namespace; decrypt keys restricted; notifications authenticated.
3. Break-glass cluster-admin path documented offline.

### 2. Inventory Flux install

```bash
flux check
flux get sources all -A
flux get ks -A
flux get hr -A
kubectl -n flux-system get deploy,sa,secret
```

1. Map each Kustomization → source → path → namespace → serviceAccountName.
2. List who can merge to reconcile branches.

### 3. Harden source trust

1. Deploy keys **read-only** where possible; fine-scoped GitHub apps.
2. Reconcile only from protected branches/tags; avoid wild `*`.
3. For OCI: enable verification (cosign/notation) if in use.
4. `interval` sensible; no anonymous HTTP sources for prod.

### 4. Harden apply path and RBAC

```yaml
# Conceptual Kustomization fields to review
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: app
  namespace: flux-system
spec:
  path: ./apps/prod/myapp
  targetNamespace: myapp
  serviceAccountName: myapp-reconciler  # not cluster-admin
  decryption:
    provider: sops
    secretRef:
      name: sops-keys
  # prune, healthChecks, etc.
```

1. Prefer per-team SAs with Role bindings only in target namespaces.
2. Disable or tightly control multi-tenancy features that allow remote bases without review.
3. Gate CRDs/cluster-scoped resources to platform Git paths only.

### 5. Secrets decryption

1. SOPS age/pgp keys in sealed K8s secrets; restrict RBAC get.
2. Prefer external secret operators for cloud KMS when scale demands.
3. Never commit private decrypt keys to the same app repo without encryption—and still limit who can decrypt in-cluster.

### 6. Notifications and webhooks

1. Alert provider tokens least privilege.
2. Validate events; do not post secrets into Slack.
3. Protect receivers that accept Git webhooks if used for automation.

### 7. Verify with evidence

| Test | Expect |
| --- | --- |
| PR without review cannot merge to prod ref | Protected |
| Tenant path apply ClusterRole | Denied by SA RBAC |
| Wrong SOPS key | Kustomization fails, no plaintext leak in logs |
| Delete deploy key | Reconcile fails closed |

```bash
flux logs --level=error --all-namespaces --tail=50
```

### 8. Hand off

1. Architecture diagram sources→ks→namespaces.
2. Access review cadence for Git and decrypt keys.
3. Image automation linked to `flux-image-automation`.
4. Apply `code-quality-standards` for policy-as-code.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Git | Protected main + reviews | Direct push with cluster keys |
| SA | Namespace-scoped impersonation | Controller SA * on * |
| Secrets | SOPS+KMS / ESO | Plain Secret YAML in Git |
| Sources | HTTPS/SSH known | Random HTTP tarball |
| Tenancy | Path+NS isolation | Monorepo root apply all |
| Alerts | Redacted | Dump kubeconfig on fail |

## Output Checklist

- [ ] Flux version and sources inventoried
- [ ] Branch protection / source auth reviewed
- [ ] Kustomization path/NS/SA matrix complete
- [ ] Decrypt key RBAC reviewed
- [ ] Notification secrets scoped
- [ ] Failure modes fail closed
- [ ] Break-glass documented
- [ ] Image automation posture linked
- [ ] `code-quality-standards` applied

## Rules

- Owned clusters/repos only.
- Treat Git write as production access.
- Prefer least-privilege reconcile identities.
- Continuous reconcile amplifies mistakes—default deny on scope.
