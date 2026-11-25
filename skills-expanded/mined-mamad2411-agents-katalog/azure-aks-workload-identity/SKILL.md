---
name: azure-aks-workload-identity
description: >
  Azure Kubernetes Service (AKS) workload identity for owned clusters: migrating from
  pod-managed identity / AAD pod identity patterns, federated identity credentials,
  service account annotations, OIDC issuer, and least-privilege Azure RBAC for pods.
  Use when pods need Key Vault, Storage, or Azure API access without secrets in pods —
  not for cluster takeover of third-party AKS or generic Azure AD app registration alone.
---

# Azure AKS Workload Identity

## Scope And Authorization

- **In scope:** AKS clusters and Azure AD (Entra ID) applications/identities in subscriptions you own or are authorized to change.
- **Out of scope:** Attaching identities to clusters outside authorization; extracting cloud credentials from shared clusters without approval.
- Prefer nonprod cluster first; identity federation mistakes can grant broad Azure access.
- Pair with `azure-keyvault-basics` / `azure-managed-identity-federated` as helpers; `code-quality-standards` for manifests.

## When To Use

- Enabling Azure AD Workload Identity on AKS (OIDC issuer + mutating webhook).
- Replacing long-lived secrets or deprecated AAD Pod Identity.
- Granting a Kubernetes service account access to Key Vault, ACR, Storage, Event Hubs via federated credential.
- Debugging `DefaultAzureCredential` failures inside pods.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Key Vault secret operations / RBAC | `azure-keyvault-basics`, `azure-keyvault-rbac-migration` |
| Managed identity concepts outside AKS | `azure-managed-identity-basics`, `azure-managed-identity-federated` |
| NSG / network review | `azure-nsg-review` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Component | Role |
| --- | --- |
| AKS OIDC issuer | Issues tokens for service accounts |
| Entra app / user-assigned MI | Azure identity trusted via federated credential |
| Federated credential | Maps `system:serviceaccount:ns:sa` issuer/subject to identity |
| SA annotations | `azure.workload.identity/client-id` etc. |
| Pod label | `azure.workload.identity/use: "true"` |
| Tooling | `az aks`, `az identity`, `kubectl`, Azure RBAC, Key Vault |

## Workflow

### 1. Confirm scope and success criteria

1. Cluster name, resource group, namespaces, target Azure resources, least-privilege roles.
2. Success: pod obtains token and calls Azure API without secrets in env/K8s Secret; other SAs cannot.
3. Rollback: previous secret-based path documented until cutover complete.

### 2. Inventory cluster identity setup

```bash
az account show
az aks show -g "$RG" -n "$CLUSTER" --query "{oidc:oidcIssuerProfile,wi:securityProfile.workloadIdentity}"
kubectl get sa -A
kubectl get mut webhook -A 2>/dev/null || true
# List existing federated creds on identities
az identity list -g "$RG" -o table
```

1. Note if OIDC issuer already enabled.
2. Find pods still using secrets or IMDS pod identity.
3. List Azure role assignments on candidate identities.

### 3. Baseline

1. Capture app auth method (connection string vs MSI vs workload identity).
2. Record Key Vault access policies vs RBAC mode.
3. Confirm node pool outbound path can reach Entra ID and ARM.

### 4. Enable workload identity and wire federation

```bash
# Enable OIDC + workload identity (may restart/reconcile — use change window)
az aks update -g "$RG" -n "$CLUSTER" --enable-oidc-issuer --enable-workload-identity

ISSUER=$(az aks show -g "$RG" -n "$CLUSTER" --query "oidcIssuerProfile.issuerUrl" -o tsv)

az identity create -g "$RG" -n "id-app-api" -o json
CLIENT_ID=$(az identity show -g "$RG" -n "id-app-api" --query clientId -o tsv)
PRINCIPAL_ID=$(az identity show -g "$RG" -n "id-app-api" --query principalId -o tsv)

# Federate K8s SA to the user-assigned managed identity
az identity federated-credential create \
  --name "fc-app-api" \
  --identity-name "id-app-api" \
  --resource-group "$RG" \
  --issuer "$ISSUER" \
  --subject "system:serviceaccount:app:api-sa" \
  --audiences "api://AzureADTokenExchange"

# Example RBAC: Key Vault Secrets User on one vault
az role assignment create \
  --assignee-object-id "$PRINCIPAL_ID" \
  --assignee-principal-type ServicePrincipal \
  --role "Key Vault Secrets User" \
  --scope "/subscriptions/$SUB/resourceGroups/$RG/providers/Microsoft.KeyVault/vaults/$VAULT"
```

**Kubernetes manifests:**

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: api-sa
  namespace: app
  annotations:
    azure.workload.identity/client-id: "<CLIENT_ID>"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  namespace: app
spec:
  template:
    metadata:
      labels:
        azure.workload.identity/use: "true"
    spec:
      serviceAccountName: api-sa
      containers:
        - name: api
          image: example.azurecr.io/api:stable
          # Use Azure SDK DefaultAzureCredential / WorkloadIdentityCredential
```

1. One identity per app (or per blast-radius boundary), not one cluster-wide super identity.
2. Subjects must match exactly: namespace + SA name.
3. Avoid putting client secrets in pod env as “backup.”

### 5. Verify with evidence

```bash
kubectl -n app exec deploy/api -- env | rg "AZURE|IDENTITY"  # projected token path vars present; no secrets
# App-level: successful Key Vault get; failed access with wrong SA
kubectl auth can-i --list --as=system:serviceaccount:app:api-sa -n app
az role assignment list --assignee "$PRINCIPAL_ID" -o table
```

1. Negative test: SA without federation cannot read vault.
2. Token files projected; restart pods after annotation changes.
3. Audit logs: Azure activity log shows app identity, not developer creds.

### 6. Observe and harden

1. Alert on auth failures to Key Vault/ARM from the app.
2. Periodic review of federated credentials and role assignments.
3. Disable/remove legacy pod identity components when migration completes.

### 7. Hand off

1. Document identity → namespace/SA → Azure roles matrix.
2. GitOps manifests for SA annotations; IaC for federated credentials.
3. Onboarding template for new microservices.

## Common Failure Modes

| Symptom | Cause | Direction |
| --- | --- | --- |
| Credential unavailable | Missing pod label / webhook | `azure.workload.identity/use: "true"` |
| Federated token rejected | Subject/issuer mismatch | Fix subject; confirm issuer URL |
| 403 on vault | Wrong RBAC / still access policy mode | Align KV permission model |
| Works on one pool only | Old nodes / webhook issues | Node image / addon health |
| Secret still required | SDK not using WI credential chain | Update Azure Identity library |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Identity scope | Per-app user-assigned MI | Cluster MI with Owner on subscription |
| Federation | Exact SA subject | Wildcard-style overbroad subjects |
| Secrets | None in pod for Azure auth | Connection string “just in case” |
| RBAC | Data-plane least privilege | Contributor on resource group |
| Migration | Dual-run then remove secrets | Big-bang delete secrets pre-verify |

## Output Checklist

- [ ] OIDC issuer + workload identity enabled on AKS
- [ ] User-assigned identity + federated credential created
- [ ] SA annotations + pod labels applied
- [ ] Azure RBAC least privilege on target resources
- [ ] Positive and negative access tests passed
- [ ] Legacy secret/pod-identity paths removed or ticketed
- [ ] Matrix of SA↔identity↔roles documented
- [ ] Monitoring for auth failures considered
- [ ] `code-quality-standards` applied to manifests/code

## Rules

- Authorized subscriptions/clusters only.
- Prefer workload identity over long-lived secrets for Azure APIs.
- Least privilege per app identity; no shared Owner identities for pods.
- Exact subject matching; review federated creds on SA rename.
- Redact client IDs in public docs only if policy requires; never ship client secrets.
