---
name: acr-content-trust
description: >
  Enable, operate, and enforce Azure Container Registry (ACR) content trust and image
  integrity: legacy Docker Content Trust / Notary, modern Notation (ORAS) or Cosign
  signatures on ACR, digest-only promote, and pull/deploy gates for signed digests.
  Use when ACR content trust, Docker Content Trust with ACR, Notary keys for Azure
  registry, notation sign/verify against ACR, Azure Policy or AKS admission requiring
  signed images, or hardening org-owned ACR so unsigned tags cannot reach production —
  not Dockerfile authorship alone, generic Cosign outside ACR, or third-party registry hunting.
---

# ACR Content Trust

## Scope And Authorization

- **In scope:** Azure Container Registries and AKS/containers in subscriptions you own or are authorized to harden.
- **Out of scope:** Pushing to or re-tagging registries you do not own; bypassing signature gates on production without change control.
- Prefer non-prod registry for pilot signing; use break-glass process for emergency unsigned deploys with expiry.
- Protect signing keys (HSM/Key Vault) as high-value secrets; redact connection strings from tickets.
- Pair pipeline code with `code-quality-standards` and secrets hygiene skills.

## When To Use

- Enforcing that only **signed** container images deploy to production from ACR.
- Migrating from legacy Docker Content Trust (Notary v1) to **Notation** or **Cosign**.
- Wiring CI to `notation sign` / `cosign sign` after `docker push` / `az acr build`.
- Azure Policy / Gatekeeper / Ratify / admission controllers verifying signatures.
- Promoting by **digest** rather than mutable tags.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Dockerfile / image build hardening | Docker/image hardening skills in catalog |
| Generic SBOM generation | SBOM skills (cluster primary per catalog) |
| Kubernetes PSS / RBAC broadly | kubernetes security skills |
| Secrets rotation program | `secrets-management-hygiene` / Key Vault skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Approach | Status / notes |
| --- | --- |
| Docker Content Trust + ACR | Legacy Notary v1 model; `DOCKER_CONTENT_TRUST=1`; key ceremony complexity |
| Notation (CNCF) + ORAS | Preferred modern path; sign/verify artifacts in ACR; Key Vault support |
| Cosign (Sigstore) | Cosign signatures/attestations stored alongside image; policy verify in admit |
| Digest pin | `repo@sha256:…` immutable reference regardless of signing tool |
| Admission | AKS policy, OPA/Gatekeeper, Ratify, Kyverno + verify image |

## Workflow

### 1. Confirm scope and success criteria

1. Record subscription, ACR name, repos, prod clusters, key custody owners.
2. Success: CI signs every release; cluster rejects unsigned/mutated digests; break-glass documented.
3. Choose **one** primary signing stack (Notation **or** Cosign) to avoid dual policy confusion; document any dual-run period.

### 2. Inventory ACR and current trust state

```bash
az account show
az acr show -n "$ACR" -g "$RG" --query "{loginServer:loginServer,adminUser:adminUserEnabled}"
az acr repository list -n "$ACR" -o table
az acr repository show-tags -n "$ACR" --repository "$REPO" -o table
```

1. Disable admin user if still on; prefer RBAC + managed identity / OIDC for push.
2. Note geo-replication and retention policies (signatures are artifacts too).
3. List who can `push` vs `pull` vs `AcrDelete`.

### 3. Baseline promote-by-digest (always)

```bash
# After build/push
DIGEST=$(az acr repository show -n "$ACR" --image "$REPO:$TAG" --query digest -o tsv)
echo "$ACR.azurecr.io/$REPO@$DIGEST"
# Deploy manifests must use @sha256: not floating :latest
```

1. CD pipelines resolve tag → digest once at promote time; never re-resolve `latest` in prod.

### 4. Sign with Notation (recommended modern path)

```bash
# Login (example)
az acr login -n "$ACR"
# Install notation CLI per current docs; configure key (Key Vault / file for lab)
notation key ls
notation policy ls

# Sign
IMAGE="$ACR.azurecr.io/$REPO@$DIGEST"
notation sign "$IMAGE"

# Verify locally
notation verify "$IMAGE"
```

1. Store signing keys in **Azure Key Vault** with restricted RBAC; CI uses federated identity.
2. Document identity trust policy (who may sign prod vs dev).
3. Retain signature artifacts; ensure GC/retention does not drop signatures prematurely.

### 5. Sign with Cosign (alternative)

```bash
az acr login -n "$ACR"
cosign sign --key cosign.key "$ACR.azurecr.io/$REPO@$DIGEST"
cosign verify --key cosign.pub "$ACR.azurecr.io/$REPO@$DIGEST"
# Prefer KMS-backed keys over file keys in production
```

1. Decide keyful vs keyless (Fulcio) per org threat model and air-gap needs.
2. Store public keys / trust roots in admission config as configmaps with change control.

### 6. Enforce at deploy time

| Gate | Action |
| --- | --- |
| CI | Fail pipeline if `notation verify` / `cosign verify` fails post-sign |
| CD | Deploy only digest refs |
| Cluster | Admission policy denies unsigned or wrong identity |
| Azure Policy | Restrict registries and optionally require signed images where supported |

```bash
# Example: dry-run check in pipeline
notation verify "$IMAGE" || exit 1
kubectl apply --dry-run=server -f deploy.yaml
```

1. Pilot on non-prod namespace; watch deny logs.
2. Break-glass: time-limited exception annotation + pager + automatic expiry.

### 7. Legacy Docker Content Trust notes

```bash
export DOCKER_CONTENT_TRUST=1
# Requires Notary setup compatible with target ACR features — verify current Azure docs
docker push "$ACR.azurecr.io/$REPO:$TAG"
```

1. Treat DCT as legacy; plan migration if still enabled.
2. Root/targets key backup and rotation are operationally heavy — document owners.

### 8. Observe and hand off

1. Metrics: signed push rate, admission denials, key age.
2. Alerts: verify failures in prod pipeline; unexpected unsigned deploys.
3. Runbook: rotate keys, revoke trust for compromised identity, rebuild+resign.
4. Train developers: tags are mutable; digests + signatures are the contract.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Reference | Deploy `@sha256:…` | Prod `:latest` pull on every pod restart |
| Keys | Key Vault + MI, split sign/verify roles | Shared `cosign.key` in git |
| Policy | Admit only trusted signers | Verify optional “warning only” forever |
| Registry auth | RBAC, no admin user | Admin password in plain CI var |
| Migration | Dual-run with deadline | DCT + Cosign + Notation all required indefinitely |

## Output Checklist

- [ ] ACR, repos, clusters, owners recorded
- [ ] Admin user / RBAC reviewed
- [ ] Digest-based promotion path implemented
- [ ] Signing tool chosen; keys in HSM/Key Vault (or documented lab exception)
- [ ] CI signs and verifies every release image
- [ ] Cluster/policy admission enforces signatures in prod
- [ ] Break-glass procedure with expiry
- [ ] Retention/GC safe for signature artifacts
- [ ] Monitoring and key rotation runbook
- [ ] `code-quality-standards` on pipeline code

## Rules

- Authorized Azure resources only.
- Prefer modern Notation/Cosign over expanding legacy DCT.
- Never commit private signing keys; rotate on personnel change.
- Unsigned emergency deploys require ticket + time limit.
- Focus on ACR integrity gates; general K8s hardening is out of primary scope.
