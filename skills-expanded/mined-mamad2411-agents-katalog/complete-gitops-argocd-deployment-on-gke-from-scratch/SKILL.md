---
name: complete-gitops-argocd-deployment-on-gke-from-scratch
description: >
  Walks through a complete, end-to-end Argo CD GitOps deployment on an
  existing Google GKE cluster — Helm install, Workload Identity Federation
  integration for Argo CD's own components (federated cluster access,
  private Artifact Registry pull auth), the first Application, an
  ApplicationSet for multi-environment rollout, and sync/health policy —
  sequenced as one coherent runbook. Use when the user asks to "set up
  Argo CD on GKE from scratch," "deploy GitOps end-to-end on GCP," "wire
  Workload Identity Federation into Argo CD," "stand up GitOps for a new
  GKE cluster," or "go from a bare GKE cluster to a working multi-env
  GitOps pipeline."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: gitops-argo-ecosystem
  maturity: stable
---

# Complete GitOps/Argo CD Deployment on GKE, From Scratch

## Purpose

This is the GKE sequencing counterpart to the EKS and AKS variants of this
skill: Argo CD install, `Application`, `ApplicationSet`, and sync policy
mechanics are identical across clouds and are covered once, in depth, by
the linked skills. What's genuinely different on GCP is **how Argo CD's
own components authenticate** — GKE's Workload Identity Federation binds a
Kubernetes ServiceAccount to a Google service account (GSA) via the
`<project>.svc.id.goog` identity pool, and the `gke-gcloud-auth-plugin`
exec credential (mandatory as of client-go's removal of built-in GCP auth)
replaces AWS's `aws eks get-token` or Azure's `kubelogin`. This skill
sequences that federation correctly relative to everything else, so Argo
CD can manage additional GKE clusters via IAM and pull private images from
Artifact Registry without a static registry key.

## When to use

- Starting from a bare, already-provisioned GKE cluster with nothing
  GitOps-related installed, needing a working Argo CD + first deployed app
  + multi-environment rollout by the end of the session.
- The user explicitly wants Workload Identity Federation wired into Argo
  CD's own service accounts (not just application workloads) for cluster
  access or Artifact Registry pulls.
- Standing up a second/third GKE-hosted environment for a service already
  GitOps-managed in one cluster.
- Migrating a team off manual `kubectl apply`/`helm upgrade` deploys to GKE
  onto a full GitOps flow, starting from zero.
- Diagnosing why a freshly installed Argo CD on GKE can't pull a private
  Artifact Registry image or can't register a second GKE cluster as a
  destination.

## Prerequisites & environment

- A GKE cluster already provisioned with Workload Identity Federation
  enabled (`--workload-pool=<project-id>.svc.id.goog` at cluster creation,
  or enabled after the fact via `gcloud container clusters update`) —
  cluster/node-pool provisioning itself is covered by
  [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md)
  and is not repeated here.
- `helm` ≥ 3.12, `kubectl`, `gcloud` CLI, and the
  `gke-gcloud-auth-plugin` component installed
  (`gcloud components install gke-gcloud-auth-plugin`) wherever Argo CD's
  exec credential runs — required for any exec-based GKE cluster
  authentication since GCP auth was removed from client-go directly.
- A Git repository already reachable from the cluster's network path.
- Least-privilege principles from
  [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md)
  should govern every IAM binding created in Phase 2.

## Step-by-step guidance

### Phase 0 — Confirm Workload Identity Federation is enabled

```bash
gcloud container clusters describe payments-prod --zone us-central1-a \
  --format="value(workloadIdentityConfig.workloadPool)"
```
Expect `<project-id>.svc.id.goog`. If empty, enable it before Phase 2 — a
`iam.workloadIdentityUser` binding created against a cluster with no
workload pool configured has nothing to federate against, and fails the
same silent way as EKS's missing OIDC provider or AKS's missing OIDC
issuer.

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

### Phase 2 — Workload Identity Federation for Argo CD's own components

Two distinct needs, both solved with Workload Identity Federation:

1. **Cross-cluster access.** For Argo CD to manage a second GKE cluster
   (`payments-staging`) as a destination, create a GSA, bind it to the
   `argocd-application-controller` KSA via `workloadIdentityUser`, and
   grant the GSA `roles/container.developer` scoped to the
   `payments-staging` project/cluster:
   ```bash
   gcloud iam service-accounts create argocd-cross-cluster \
     --project <project-id>
   gcloud iam service-accounts add-iam-policy-binding \
     argocd-cross-cluster@<project-id>.iam.gserviceaccount.com \
     --role roles/iam.workloadIdentityUser \
     --member "serviceAccount:<project-id>.svc.id.goog[argocd/argocd-application-controller]"
   gcloud projects add-iam-policy-binding <project-id> \
     --member "serviceAccount:argocd-cross-cluster@<project-id>.iam.gserviceaccount.com" \
     --role roles/container.developer \
     --condition "expression=resource.name.startsWith('projects/<project-id>/locations/us-central1-a/clusters/payments-staging'),title=staging-only"
   ```
   ```yaml
   apiVersion: v1
   kind: ServiceAccount
   metadata:
     name: argocd-application-controller
     namespace: argocd
     annotations:
       iam.gke.io/gcp-service-account: argocd-cross-cluster@<project-id>.iam.gserviceaccount.com
   ```
   The destination cluster `Secret` Argo CD uses to register
   `payments-staging` then points its `exec` credential at
   `gke-gcloud-auth-plugin` instead of a static bearer token:
   ```yaml
   config: |
     {
       "execProviderConfig": {
         "command": "gke-gcloud-auth-plugin",
         "installHint": "Install gke-gcloud-auth-plugin for use with kubectl by following https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke",
         "provideClusterInfo": true,
         "apiVersion": "client.authentication.k8s.io/v1beta1"
       },
       "tlsClientConfig": { "insecure": false, "caData": "${SPOKE_CA_DATA_BASE64}" }
     }
   ```
   This is the GCP counterpart of the cluster-registration pattern in
   [gitops-multi-cluster-management](../gitops-multi-cluster-management/SKILL.md)
   — same `Secret`-based registration, but the credential is a Google
   IAM-federated token exchanged via `gke-gcloud-auth-plugin` instead of a
   static bearer token, AWS's `aws eks get-token`, or Azure's `kubelogin`.

2. **Private Artifact Registry image pulls for `argocd-repo-server`**
   (Helm OCI charts) and application workloads, using the same federation
   mechanics shown in
   [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md):
   ```bash
   gcloud iam service-accounts create argocd-repo-server-ar --project <project-id>
   gcloud artifacts repositories add-iam-policy-binding payments-images \
     --location us-central1 \
     --member "serviceAccount:argocd-repo-server-ar@<project-id>.iam.gserviceaccount.com" \
     --role roles/artifactregistry.reader
   gcloud iam service-accounts add-iam-policy-binding \
     argocd-repo-server-ar@<project-id>.iam.gserviceaccount.com \
     --role roles/iam.workloadIdentityUser \
     --member "serviceAccount:<project-id>.svc.id.goog[argocd/argocd-repo-server]"
   ```
   ```yaml
   apiVersion: v1
   kind: ServiceAccount
   metadata:
     name: argocd-repo-server
     namespace: argocd
     annotations:
       iam.gke.io/gcp-service-account: argocd-repo-server-ar@<project-id>.iam.gserviceaccount.com
   ```

### Phase 3 — Ingress and TLS for the Argo CD API/UI

Same mechanics as any other cluster:
[ingress-nginx-configuration](../../../kubernetes-platform/skills/ingress-nginx-configuration/SKILL.md)
in front of `argocd-server`, certificate issued by
[cert-manager-tls-automation](../../../kubernetes-platform/skills/cert-manager-tls-automation/SKILL.md)
via DNS-01 against Cloud DNS (its own Workload-Identity-federated
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
If staging and prod are separate GKE clusters, use the Cluster generator
filtered by label, with each cluster's registration reusing the Workload
Identity Federation from Phase 2.

### Phase 6 — Sync policy and health checks, deliberately

Manual sync until the pipeline feeding the config repo is trusted, then
`automated` per environment, plus custom Lua health checks for any
internal CRDs — both per
[argocd-application-configuration](../argocd-application-configuration/SKILL.md).

### Phase 7 — Verify end-to-end

```bash
argocd cluster list
argocd app list
kubectl exec -n argocd deploy/argocd-repo-server -- gcloud auth list
```
`gcloud auth list` from inside `argocd-repo-server` should show the
federated GSA as the active account, not the node's own default compute
service account — confirming the pod is actually using Workload Identity
Federation rather than silently falling back to the node's identity.

## Best practices

- Enable Workload Identity Federation at cluster creation
  (`--workload-pool`) where possible; enabling it on an existing node pool
  requires a node pool recreation (`--workload-metadata=GKE_METADATA`) for
  the metadata server proxy to actually intercept credential requests.
- Bind each GSA to an exact `<project>.svc.id.goog[<namespace>/<ksa>]`
  member — a binding is not automatically valid for a same-named KSA in a
  different namespace, mirroring the equivalent pitfall in
  [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md).
- Grant `roles/artifactregistry.reader` scoped to the specific repository
  Argo CD needs, not project-wide `roles/artifactregistry.admin`.
- Never expose `argocd-server` via a public `LoadBalancer` Service —
  terminate through Ingress + cert-manager as in Phase 3.
- Default to manual sync until the config repo's CI gates are trusted,
  matching the EKS/AKS variants of this runbook.

## Common pitfalls

- **Symptom:** A ServiceAccount has the correct
  `iam.gke.io/gcp-service-account` annotation and the IAM binding exists,
  but a pod using it still gets a `403`/metadata-server error from Google
  APIs.
  **Fix:** Check the node pool's `--workload-metadata` setting — if the
  node pool was created before Workload Identity was enabled cluster-wide,
  its nodes may not have `GKE_METADATA` mode active, so the metadata
  server never intercepts and rewrites the credential request; recreate
  or update the specific node pool, not just the cluster-level setting.

- **Symptom:** The `iam.workloadIdentityUser` binding's member string was
  copy-pasted from a working example and cluster access silently fails
  for a differently-named KSA in a new namespace.
  **Fix:** Workload Identity bindings are exact-match on
  `<project>.svc.id.goog[namespace/ksa-name]` — add a new binding per
  actual namespace/ServiceAccount pair, don't assume one binding covers
  every namespace a workload might run in.

- **Symptom:** The first `Application` was created with `automated:
  {prune: true, selfHeal: true}` immediately, and a bad initial manifest
  deleted an unrelated pre-existing resource in the target namespace.
  **Fix:** Same end-to-end sequencing pitfall as on any cloud — always run
  the first sync manually with `--dry-run` (Phase 4) before enabling
  `automated` in a later, deliberate step (Phase 6).

- **Symptom:** `argocd-repo-server` can reach the Git repo but pulling a
  Helm OCI chart or the workload's own image from Artifact Registry fails
  with `PERMISSION_DENIED`.
  **Fix:** Artifact Registry pull auth for the workload's own pods is a
  separate Workload Identity binding from the repo-server's — bind the
  workload's own ServiceAccount to a GSA with `artifactregistry.reader` on
  the relevant repository, don't assume the repo-server's binding covers
  it.

## Worked example

**Scenario:** Stand up Argo CD from scratch on `payments-prod` GKE,
register `payments-staging` GKE as a second destination via Workload
Identity Federation, and roll `payments-api` out to both via an
`ApplicationSet`.

```bash
# Phase 0
gcloud container clusters update payments-prod --zone us-central1-a \
  --workload-pool=<project-id>.svc.id.goog

# Phase 1
helm install argocd argo/argo-cd -n argocd --create-namespace --version 7.6.12

# Phase 2 — cross-cluster federated GSA
gcloud iam service-accounts create argocd-cross-cluster --project <project-id>
gcloud iam service-accounts add-iam-policy-binding \
  argocd-cross-cluster@<project-id>.iam.gserviceaccount.com \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:<project-id>.svc.id.goog[argocd/argocd-application-controller]"

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

- [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md) — GKE cluster/node-pool provisioning and Workload Identity Federation mechanics this skill assumes and builds on.
- [argocd-application-configuration](../argocd-application-configuration/SKILL.md) — full depth on the `Application` spec used in Phase 4/6.
- [argocd-applicationset-patterns](../argocd-applicationset-patterns/SKILL.md) — generator mechanics used in Phase 5.
- [gitops-multi-cluster-management](../gitops-multi-cluster-management/SKILL.md) — hub-and-spoke registration pattern this skill's Phase 2 adapts with Workload Identity Federation.
- [ingress-nginx-configuration](../../../kubernetes-platform/skills/ingress-nginx-configuration/SKILL.md) and [cert-manager-tls-automation](../../../kubernetes-platform/skills/cert-manager-tls-automation/SKILL.md) — Phase 3's Ingress/TLS mechanics.
- [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md) — least-privilege principles governing every IAM binding created here.
- [gitops-workflow](../../../devops/skills/gitops-workflow/SKILL.md) — the vendor-neutral GitOps concepts this GKE-specific runbook implements.
