---
name: complete-gitops-argocd-deployment-on-aks-from-scratch
description: >
  Walks through a complete, end-to-end Argo CD GitOps deployment on an
  existing Azure AKS cluster — Helm install, Azure AD Workload Identity
  integration for Argo CD's own components (federated-credential-based
  cluster access, private ACR pull auth), the first Application, an
  ApplicationSet for multi-environment rollout, and sync/health policy —
  sequenced as one coherent runbook. Use when the user asks to "set up
  Argo CD on AKS from scratch," "deploy GitOps end-to-end on Azure," "wire
  Azure AD Workload Identity into Argo CD," "stand up GitOps for a new AKS
  cluster," or "go from a bare AKS cluster to a working multi-env GitOps
  pipeline."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: gitops-argo-ecosystem
  maturity: stable
---

# Complete GitOps/Argo CD Deployment on AKS, From Scratch

## Purpose

This is the AKS sequencing counterpart to the EKS and GKE variants of this
skill: Argo CD install, `Application`, `ApplicationSet`, and sync policy
mechanics are identical across every cloud and are covered once, in depth,
in the linked skills. What's genuinely different on Azure is **how Argo
CD's own components authenticate** — Azure AD Workload Identity (the
successor to the deprecated AAD Pod Identity) federates a Kubernetes
ServiceAccount to an Azure AD application via OIDC, using `kubelogin` as
the exec credential plugin rather than AWS's `aws eks get-token` or GKE's
`gke-gcloud-auth-plugin`. This skill sequences that federation correctly
relative to everything else, so Argo CD can both manage additional AKS
clusters via Azure AD and pull private images from Azure Container
Registry (ACR) without a static registry secret.

## When to use

- Starting from a bare, already-provisioned AKS cluster with nothing
  GitOps-related installed, needing a working Argo CD + first deployed app
  + multi-environment rollout by the end of the session.
- The user explicitly wants Azure AD Workload Identity wired into Argo
  CD's own service accounts (not just application workloads) for cluster
  access or ACR pulls.
- Standing up a second/third AKS-hosted environment for a service already
  GitOps-managed in one cluster.
- Migrating a team off manual `kubectl apply`/`helm upgrade` deploys to AKS
  onto a full GitOps flow, starting from zero.
- Diagnosing why a freshly installed Argo CD on AKS can't pull a private
  ACR image or can't register a second AKS cluster as a destination.

## Prerequisites & environment

- An AKS cluster already provisioned with the OIDC issuer and Workload
  Identity features enabled (`az aks create --enable-oidc-issuer
  --enable-workload-identity`, or `az aks update` on an existing cluster)
  — cluster/node-pool provisioning itself is covered by
  [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md)
  and is not repeated here.
- `helm` ≥ 3.12, `kubectl`, `az` CLI ≥ 2.60, and the **Azure Workload
  Identity webhook** already installed on the cluster (bundled by
  `--enable-workload-identity`, but confirm with
  `kubectl get pods -n kube-system -l azure-workload-identity.io/system=true`).
- The `kubelogin` binary available wherever Argo CD's exec credential runs
  (baked into the `argocd-application-controller`/`argocd-server` image or
  mounted as an init step) — Azure AD-based `kubeconfig`s reference
  `kubelogin` as their exec plugin, unlike a plain bearer token.
- A Git repository already reachable from the cluster's network path.
- Least-privilege principles from
  [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md)
  should govern every Azure AD application/federated credential created in
  Phase 2.

## Step-by-step guidance

### Phase 0 — Confirm OIDC issuer and Workload Identity are enabled

```bash
az aks show --name payments-prod --resource-group payments-rg \
  --query "oidcIssuerProfile.issuerUrl" -o tsv
az aks show --name payments-prod --resource-group payments-rg \
  --query "securityProfile.workloadIdentity.enabled"
```
If either is missing, enable them before anything in Phase 2 — a federated
credential created against a cluster with no OIDC issuer has nothing to
federate against, and fails the same silent way as EKS's missing OIDC
provider.

### Phase 1 — Install Argo CD via Helm

```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
helm install argocd argo/argo-cd \
  --namespace argocd --create-namespace \
  --version 7.6.12 \
  --set server.service.type=ClusterIP
kubectl get pods -n argocd
```

### Phase 2 — Azure AD Workload Identity integration for Argo CD's own components

Two distinct needs, both solved with Workload Identity:

1. **Cross-cluster access.** For Argo CD to manage a second AKS cluster
   (`payments-staging`) as a destination, create a managed identity, a
   federated credential trusting `payments-prod`'s OIDC issuer for the
   `argocd-application-controller` ServiceAccount, and grant that identity
   `Azure Kubernetes Service Cluster User Role` plus an AKS **Azure RBAC**
   binding (`Azure Kubernetes Service RBAC Writer`) scoped to
   `payments-staging`:
   ```bash
   az identity create --name argocd-cross-cluster --resource-group payments-rg
   az identity federated-credential create \
     --name argocd-cross-cluster-fic --identity-name argocd-cross-cluster \
     --resource-group payments-rg \
     --issuer "$(az aks show -n payments-prod -g payments-rg --query oidcIssuerProfile.issuerUrl -o tsv)" \
     --subject system:serviceaccount:argocd:argocd-application-controller \
     --audience api://AzureADTokenExchange

   az role assignment create \
     --assignee "$(az identity show -n argocd-cross-cluster -g payments-rg --query principalId -o tsv)" \
     --role "Azure Kubernetes Service RBAC Writer" \
     --scope "$(az aks show -n payments-staging -g payments-rg --query id -o tsv)"
   ```
   ```yaml
   apiVersion: v1
   kind: ServiceAccount
   metadata:
     name: argocd-application-controller
     namespace: argocd
     annotations:
       azure.workload.identity/client-id: <ARGOCD_CROSS_CLUSTER_CLIENT_ID>
     labels:
       azure.workload.identity/use: "true"
   ```
   The destination cluster `Secret` Argo CD uses to register
   `payments-staging` then points its `exec` credential at `kubelogin`
   instead of a static bearer token:
   ```yaml
   config: |
     {
       "execProviderConfig": {
         "command": "kubelogin",
         "args": ["get-token", "--login", "workloadidentity",
                   "--server-id", "6dae42f8-4368-4678-94ff-3960e28e3630"],
         "apiVersion": "client.authentication.k8s.io/v1beta1"
       },
       "tlsClientConfig": { "insecure": false, "caData": "${SPOKE_CA_DATA_BASE64}" }
     }
   ```
   This is the Azure counterpart of the cluster-registration pattern in
   [gitops-multi-cluster-management](../gitops-multi-cluster-management/SKILL.md)
   — same `Secret`-based registration, but the credential is an Azure AD
   token exchanged via `kubelogin` instead of a static bearer token or
   AWS's `aws eks get-token`.

2. **Private ACR image pulls for `argocd-repo-server`** (Helm OCI charts)
   and application workloads, using the same federation mechanics shown in
   [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md):
   ```bash
   az identity create --name argocd-repo-server-acr --resource-group payments-rg
   az role assignment create \
     --assignee "$(az identity show -n argocd-repo-server-acr -g payments-rg --query principalId -o tsv)" \
     --role AcrPull \
     --scope "$(az acr show -n paymentsregistry --query id -o tsv)"
   az identity federated-credential create \
     --name argocd-repo-server-fic --identity-name argocd-repo-server-acr \
     --resource-group payments-rg \
     --issuer "$(az aks show -n payments-prod -g payments-rg --query oidcIssuerProfile.issuerUrl -o tsv)" \
     --subject system:serviceaccount:argocd:argocd-repo-server
   ```
   ```yaml
   apiVersion: v1
   kind: ServiceAccount
   metadata:
     name: argocd-repo-server
     namespace: argocd
     annotations:
       azure.workload.identity/client-id: <ARGOCD_REPO_SERVER_ACR_CLIENT_ID>
     labels:
       azure.workload.identity/use: "true"
   ```

### Phase 3 — Ingress and TLS for the Argo CD API/UI

Same mechanics as any other cluster:
[ingress-nginx-configuration](../../../kubernetes-platform/skills/ingress-nginx-configuration/SKILL.md)
in front of `argocd-server`, certificate issued by
[cert-manager-tls-automation](../../../kubernetes-platform/skills/cert-manager-tls-automation/SKILL.md)
via DNS-01 against Azure DNS (its own Workload-Identity-federated
credential, per that skill's guidance) rather than a self-signed cert.

### Phase 4 — First `Application`

Follow [argocd-application-configuration](../argocd-application-configuration/SKILL.md)
in full for the `Application` spec, sync-wave ordering, and health checks;
apply and sync manually first:
```bash
kubectl apply -f payments-api-staging-application.yaml
argocd login argocd.example.com --sso
argocd app sync payments-api-staging --dry-run
argocd app sync payments-api-staging
```

### Phase 5 — `ApplicationSet` for multi-environment rollout

Replace the single hand-authored `Application` with an `ApplicationSet`
per [argocd-applicationset-patterns](../argocd-applicationset-patterns/SKILL.md).
If staging and prod are separate AKS clusters, use the Cluster generator
filtered by label, with each cluster's registration reusing the Workload
Identity federation from Phase 2.

### Phase 6 — Sync policy and health checks, deliberately

Manual sync until the pipeline feeding the config repo is trusted, then
`automated` per environment, plus custom Lua health checks for any
internal CRDs — both per
[argocd-application-configuration](../argocd-application-configuration/SKILL.md).

### Phase 7 — Verify end-to-end

```bash
argocd cluster list
argocd app list
kubectl exec -n argocd deploy/argocd-repo-server -- az account show
```
`az account show` from inside `argocd-repo-server` should show the
federated managed identity, not an error — confirming the workload
identity webhook actually injected the federated token rather than the
pod silently having no Azure identity at all.

## Best practices

- Enable `--enable-oidc-issuer` and `--enable-workload-identity` at
  cluster creation time where possible; enabling them later on an existing
  cluster works but requires a rollout of every pod that needs the
  webhook's mutation to take effect.
- Scope each federated credential's `--subject` to an exact
  `system:serviceaccount:<namespace>:<name>` pair — a federated credential
  is not automatically valid for a same-named ServiceAccount in a
  different namespace, mirroring the equivalent pitfall in
  [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md).
- Grant `AcrPull` only on the specific ACR registry (or repository, if
  using ACR's repository-scoped tokens) Argo CD needs — not
  subscription-wide `Contributor`.
- Never expose `argocd-server` via a public `LoadBalancer` Service —
  terminate through Ingress + cert-manager as in Phase 3.
- Default to manual sync until the config repo's CI gates are trusted,
  matching the EKS/GKE variants of this runbook.

## Common pitfalls

- **Symptom:** A ServiceAccount has the correct
  `azure.workload.identity/client-id` annotation and the
  `azure.workload.identity/use: "true"` label, but a pod using it still
  gets an authentication error from Azure.
  **Fix:** Check that the pod was actually recreated after the annotation
  was added — the Workload Identity webhook only mutates pods at creation
  time; patching an existing running pod's ServiceAccount reference does
  not retroactively inject the federated token volume. Delete and let the
  Deployment recreate the pod.

- **Symptom:** The federated credential's `--subject` was copy-pasted from
  a working example and cluster access silently fails for a differently-
  named ServiceAccount in a new namespace.
  **Fix:** Federated credentials are exact-match on
  `namespace:serviceaccount` — create a new federated credential (or add
  a namespace) per actual `subject`, don't assume one credential covers
  every namespace a workload might run in.

- **Symptom:** The first `Application` was created with `automated:
  {prune: true, selfHeal: true}` immediately, and a bad initial manifest
  deleted an unrelated pre-existing resource in the target namespace.
  **Fix:** Same end-to-end sequencing pitfall as on any cloud — always run
  the first sync manually with `--dry-run` (Phase 4) before enabling
  `automated` in a later, deliberate step (Phase 6).

- **Symptom:** `argocd-repo-server` can reach the Git repo but pulling a
  Helm OCI chart or the workload's own image from ACR fails with
  `unauthorized`.
  **Fix:** ACR pull auth for the workload's own pods is a separate
  Workload Identity binding from the repo-server's — bind the workload's
  own ServiceAccount to a federated identity with `AcrPull` on the
  relevant registry, don't assume the repo-server's binding covers it.

## Worked example

**Scenario:** Stand up Argo CD from scratch on `payments-prod` AKS,
register `payments-staging` AKS as a second destination via Workload
Identity, and roll `payments-api` out to both via an `ApplicationSet`.

```bash
# Phase 0
az aks update -n payments-prod -g payments-rg \
  --enable-oidc-issuer --enable-workload-identity

# Phase 1
helm install argocd argo/argo-cd -n argocd --create-namespace --version 7.6.12

# Phase 2 — cross-cluster federated credential
az identity create --name argocd-cross-cluster --resource-group payments-rg
az identity federated-credential create --name argocd-cross-cluster-fic \
  --identity-name argocd-cross-cluster --resource-group payments-rg \
  --issuer "$(az aks show -n payments-prod -g payments-rg --query oidcIssuerProfile.issuerUrl -o tsv)" \
  --subject system:serviceaccount:argocd:argocd-application-controller
az role assignment create \
  --assignee "$(az identity show -n argocd-cross-cluster -g payments-rg --query principalId -o tsv)" \
  --role "Azure Kubernetes Service RBAC Writer" \
  --scope "$(az aks show -n payments-staging -g payments-rg --query id -o tsv)"

# Phase 4 — first Application, manual sync
kubectl apply -f payments-api-staging-application.yaml
argocd app sync payments-api-staging --dry-run
argocd app sync payments-api-staging
```
Phase 5 then replaces the single `Application` with a Cluster-generator
`ApplicationSet` selecting `tier: staging`/`tier: prod` labeled clusters
(full YAML in
[argocd-applicationset-patterns](../argocd-applicationset-patterns/SKILL.md)),
and Phase 6 promotes staging's sync policy to `automated` once verified.

## Cross-references

- [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md) — AKS cluster/node-pool provisioning and Workload Identity mechanics this skill assumes and builds on.
- [argocd-application-configuration](../argocd-application-configuration/SKILL.md) — full depth on the `Application` spec used in Phase 4/6.
- [argocd-applicationset-patterns](../argocd-applicationset-patterns/SKILL.md) — generator mechanics used in Phase 5.
- [gitops-multi-cluster-management](../gitops-multi-cluster-management/SKILL.md) — hub-and-spoke registration pattern this skill's Phase 2 adapts with Workload Identity.
- [ingress-nginx-configuration](../../../kubernetes-platform/skills/ingress-nginx-configuration/SKILL.md) and [cert-manager-tls-automation](../../../kubernetes-platform/skills/cert-manager-tls-automation/SKILL.md) — Phase 3's Ingress/TLS mechanics.
- [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md) — least-privilege principles governing every Azure AD role assignment created here.
- [gitops-workflow](../../../devops/skills/gitops-workflow/SKILL.md) — the vendor-neutral GitOps concepts this AKS-specific runbook implements.
