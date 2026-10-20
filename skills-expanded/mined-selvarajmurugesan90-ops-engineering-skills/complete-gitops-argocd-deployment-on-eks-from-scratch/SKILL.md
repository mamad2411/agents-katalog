---
name: complete-gitops-argocd-deployment-on-eks-from-scratch
description: >
  Walks through a complete, end-to-end Argo CD GitOps deployment on an
  existing AWS EKS cluster — Helm install, IRSA-based AWS IAM integration
  for Argo CD's own components (cluster access via EKS access entries,
  private ECR pull auth), the first Application, an ApplicationSet for
  multi-environment rollout, and sync/health policy — sequenced as one
  coherent runbook rather than the individual mechanics each step depends
  on. Use when the user asks to "set up Argo CD on EKS from scratch,"
  "deploy GitOps end-to-end on AWS," "wire IRSA into Argo CD," "stand up
  GitOps for a new EKS cluster," or "go from a bare EKS cluster to a
  working multi-env GitOps pipeline."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: gitops-argo-ecosystem
  maturity: stable
---

# Complete GitOps/Argo CD Deployment on EKS, From Scratch

## Purpose

Every piece of this deployment — installing Argo CD, giving it AWS
permissions, writing an `Application`, templating that into an
`ApplicationSet`, and choosing a sync policy — already has its own deep
skill in this repo. What's missing is the **sequencing**: in what order do
you actually do these things on a fresh EKS cluster so that each step's
prerequisites are satisfied by the step before it, and where does this
specific cloud's IAM model (IRSA) plug in versus where the mechanics are
identical to any other Kubernetes cluster? This skill is that runbook. The
one genuinely AWS-specific decision point is **how Argo CD authenticates to
AWS**, both for its own EKS cluster access (via IAM, not a static bearer
token) and for pulling images from a private ECR registry — everything
downstream (the `Application` spec, the `ApplicationSet` generator, sync
policy) is identical to any other Kubernetes target and is covered in depth
by the linked skills, not repeated here.

## When to use

- Starting from a bare, already-provisioned EKS cluster with nothing
  GitOps-related installed, and needing a working Argo CD + first deployed
  app + multi-environment rollout by the end of the session.
- The user explicitly wants IRSA wired into Argo CD's own service accounts
  (not just application workloads) for cluster access or ECR pulls.
- Standing up a second/third environment (staging, prod) for a service
  already GitOps-managed in one EKS cluster.
- Migrating a team off manual `kubectl apply`/`helm upgrade` deploys to EKS
  onto a full GitOps flow, starting from zero.
- Diagnosing why a freshly installed Argo CD on EKS can't reach a private
  ECR image or can't register a second EKS cluster as a destination.

## Prerequisites & environment

- An EKS cluster already provisioned and reachable via `kubectl` — cluster
  creation, node groups, and networking are covered by
  [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md)
  and are **not** repeated here; this skill starts from "the cluster
  exists."
- An IAM OIDC identity provider already associated with the cluster
  (`eksctl utils associate-iam-oidc-provider`) — required before any IRSA
  role can be created; if this is missing, do it as the very first step,
  since every later IAM step silently fails without it.
- `helm` ≥ 3.12, `kubectl`, `eksctl` or Terraform's `aws` provider, and
  `aws` CLI v2 with IAM permissions to create roles/policies and EKS
  access entries.
- A Git repository already reachable from the cluster's network path to
  hold the GitOps config (Application manifests, Kustomize/Helm overlays).
- Least-privilege IAM design principles from
  [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md)
  should govern every role created in Phase 2 below.

## Step-by-step guidance

### Phase 0 — Confirm the cluster is IRSA-ready

```bash
eksctl utils associate-iam-oidc-provider --cluster payments-prod --approve
aws eks describe-cluster --name payments-prod --query "cluster.identity.oidc.issuer"
```
If the OIDC issuer isn't associated yet, every `iamserviceaccount`/IRSA
step in Phase 2 will silently produce a ServiceAccount with an annotation
pointing at a role AWS never trusts — confirm this first, not after Argo CD
is already installed.

### Phase 1 — Install Argo CD via Helm

```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
helm install argocd argo/argo-cd \
  --namespace argocd --create-namespace \
  --version 7.6.12 \
  --set server.service.type=ClusterIP
kubectl get pods -n argocd   # wait for all Deployments/StatefulSet Ready
```
Use `ClusterIP` (not a public `LoadBalancer`) for the server service by
default — Phase 3 puts a proper Ingress + TLS in front of it rather than
exposing the API server directly on a cloud load balancer.

### Phase 2 — AWS IAM integration for Argo CD's own components (IRSA)

This is the AWS-specific step with no equivalent on a plain Kubernetes
cluster. Two distinct needs, both solved with IRSA:

1. **Argo CD's `application-controller`/`server` need IAM, not just a
   static bearer token, to manage destination EKS clusters** beyond the
   one it's running on (a second EKS cluster in another account/region).
   Create an IRSA role for the controller's ServiceAccount, grant it
   `sts:AssumeRole` onto a role in the target account, and register the
   destination cluster using an **EKS access entry** (the modern
   replacement for hand-editing the `aws-auth` ConfigMap) instead of a
   long-lived kubeconfig token:
   ```bash
   eksctl create iamserviceaccount \
     --cluster payments-prod --namespace argocd \
     --name argocd-application-controller \
     --role-name argocd-eks-cross-cluster \
     --attach-policy-arn arn:aws:iam::<AWS_ACCOUNT_ID>:policy/ArgoCDAssumeSpokeRole \
     --override-existing-serviceaccounts --approve

   aws eks create-access-entry \
     --cluster-name payments-staging \
     --principal-arn arn:aws:iam::<AWS_ACCOUNT_ID>:role/argocd-eks-cross-cluster \
     --type STANDARD
   aws eks associate-access-policy \
     --cluster-name payments-staging \
     --principal-arn arn:aws:iam::<AWS_ACCOUNT_ID>:role/argocd-eks-cross-cluster \
     --policy-arn arn:aws:eks::aws:cluster-access-policy/AmazonEKSEditPolicy \
     --access-scope type=cluster
   ```
   The cluster `Secret` Argo CD uses to register `payments-staging` as a
   destination then uses an `exec`-based credential (`aws eks get-token`)
   instead of a bearer token/client cert:
   ```yaml
   config: |
     {
       "execProviderConfig": {
         "command": "aws",
         "args": ["eks", "get-token", "--cluster-name", "payments-staging", "--role-arn", "arn:aws:iam::<AWS_ACCOUNT_ID>:role/argocd-eks-cross-cluster"],
         "apiVersion": "client.authentication.k8s.io/v1beta1"
       },
       "tlsClientConfig": { "insecure": false, "caData": "${SPOKE_CA_DATA_BASE64}" }
     }
   ```
   This is the EKS-specific version of the cluster-registration pattern in
   [gitops-multi-cluster-management](../gitops-multi-cluster-management/SKILL.md)
   — same `Secret`-based registration mechanism, but the credential is a
   short-lived STS token brokered by IRSA instead of a static bearer token.

2. **`argocd-repo-server` (and any workload pulling private images) needs
   ECR pull access without a static Docker config secret.** IRSA-bind the
   repo-server's ServiceAccount to a role with `ecr:GetAuthorizationToken`/
   `ecr:BatchGetImage`, matching the workload-identity pattern in
   [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md):
   ```bash
   eksctl create iamserviceaccount \
     --cluster payments-prod --namespace argocd \
     --name argocd-repo-server --role-name argocd-repo-server-ecr-read \
     --attach-policy-arn arn:aws:iam::<AWS_ACCOUNT_ID>:policy/EcrReadOnly \
     --override-existing-serviceaccounts --approve
   kubectl patch deployment argocd-repo-server -n argocd --type=json \
     -p '[{"op":"add","path":"/spec/template/spec/serviceAccountName","value":"argocd-repo-server"}]'
   ```

### Phase 3 — Ingress and TLS for the Argo CD API/UI

Front the `argocd-server` Service with
[ingress-nginx-configuration](../../../kubernetes-platform/skills/ingress-nginx-configuration/SKILL.md)
and issue its certificate with
[cert-manager-tls-automation](../../../kubernetes-platform/skills/cert-manager-tls-automation/SKILL.md)
(DNS-01 via Route 53, backed by its own scoped IRSA role per that skill's
guidance) rather than a self-signed cert or a directly-exposed
`LoadBalancer` Service:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: argocd-server
  namespace: argocd
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-dns
    nginx.ingress.nginx.io/backend-protocol: "GRPC"
spec:
  ingressClassName: nginx
  tls:
    - hosts: ["argocd.example.com"]
      secretName: argocd-server-tls
  rules:
    - host: argocd.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend: { service: { name: argocd-server, port: { number: 443 } } }
```

### Phase 4 — First `Application`

Write the first real `Application` following
[argocd-application-configuration](../argocd-application-configuration/SKILL.md)
in full — sync policy fields, sync waves/hooks, and custom health checks
are all covered there in depth:
```bash
kubectl apply -f payments-api-staging-application.yaml
argocd login argocd.example.com --sso
argocd app sync payments-api-staging --dry-run
argocd app sync payments-api-staging
argocd app wait payments-api-staging --health --timeout 300
```

### Phase 5 — `ApplicationSet` for multi-environment rollout

Once the first `Application` works, replace hand-authored per-environment
manifests with an `ApplicationSet` per
[argocd-applicationset-patterns](../argocd-applicationset-patterns/SKILL.md)
— a List generator for a small fixed set of environments, or a Cluster
generator (labeled `tier: staging`/`tier: prod`) if staging and prod are
separate EKS clusters rather than separate namespaces on one cluster, in
which case each cluster's registration reuses the IRSA/access-entry
pattern from Phase 2.

### Phase 6 — Sync policy and health checks, deliberately

Per [argocd-application-configuration](../argocd-application-configuration/SKILL.md):
manual sync for the initial rollout, `automated` (with `prune`/`selfHeal`)
only after the team trusts the pipeline; add custom Lua health checks for
any internal CRDs the workloads depend on before relying on Argo CD's
health status for alerting.

### Phase 7 — Verify end-to-end

```bash
argocd cluster list
argocd app list
kubectl exec -n argocd deploy/argocd-repo-server -- aws sts get-caller-identity
```
The `sts get-caller-identity` from inside `argocd-repo-server` should show
the IRSA role's ARN, not an EC2 instance profile — confirming the pod is
actually using the federated identity, not silently falling back to node
credentials.

## Best practices

- Do Phase 0 (OIDC provider) and Phase 2 (IRSA) **before** registering any
  additional destination cluster or private-registry `Application` — an
  `Application` created against a cluster secret with no working IAM
  credential fails in a way that looks like a networking problem, not an
  IAM one.
- Prefer EKS access entries over editing the legacy `aws-auth` ConfigMap
  for any cluster created on a current EKS version — access entries are
  auditable via the EKS API and don't risk a ConfigMap edit locking out
  cluster-admin.
- Keep the IRSA role for `argocd-repo-server` scoped to `ecr:GetAuthorizationToken`
  plus `GetDownloadUrlForLayer`/`BatchGetImage` on the specific repositories
  it needs — not registry-wide `ecr:*`, mirroring the least-privilege
  guidance in [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md).
- Never expose `argocd-server` directly via a public `LoadBalancer` Service
  — always terminate through Ingress + cert-manager so TLS and access
  logging are consistent with every other service on the cluster.
- Default to manual sync until the config repo's own CI (SAST/SCA gates
  per [secure-cicd-gates](../../../devsecops/skills/secure-cicd-gates/SKILL.md))
  is trusted, then promote to `automated` per environment.

## Common pitfalls

- **Symptom:** An `iamserviceaccount` is created and the ServiceAccount
  shows the correct `eks.amazonaws.com/role-arn` annotation, but pods
  using it still get `AccessDenied` from AWS.
  **Fix:** This is almost always Phase 0 skipped or run after the
  `iamserviceaccount` command — the IAM OIDC provider must be associated
  with the cluster *before* `eksctl create iamserviceaccount` runs, or the
  role's trust policy references an OIDC provider ARN that doesn't
  actually exist yet. Re-run `associate-iam-oidc-provider` and recreate the
  service account.

- **Symptom:** A second EKS cluster is registered as an Argo CD destination
  using the exec-based `aws eks get-token` credential, and `argocd cluster
  list` shows it as `Unknown`/unreachable even though the access entry was
  created.
  **Fix:** `aws eks associate-access-policy` was likely run with the wrong
  `--access-scope` (namespace-scoped instead of cluster-scoped, or vice
  versa relative to what the `Application`s targeting it need) — verify
  with `aws eks list-access-entries --cluster-name <spoke>` and
  `describe-access-policy` before assuming the exec plugin itself is
  broken.

- **Symptom:** The first `Application` was created with
  `automated: {prune: true, selfHeal: true}` straight out of the gate
  (skipping the manual-sync validation step in Phase 4), and a bad initial
  manifest deleted an unrelated pre-existing resource in the target
  namespace.
  **Fix:** This is the ordering pitfall specific to end-to-end setup —
  always run the *first* sync of a brand-new `Application` manually with
  `--dry-run` first (Phase 4), and only add `automated` sync in a later,
  deliberate step (Phase 6) once the manifest set is verified.

- **Symptom:** `argocd-repo-server` can clone the Git repo fine but pulling
  the application's own container image from ECR fails with
  `ImagePullBackOff` even though the repo-server itself authenticates to
  AWS correctly.
  **Fix:** ECR pull auth for the *workload's* pods is a separate IRSA
  binding from the repo-server's — the repo-server's IRSA role only
  affects what Argo CD itself can read (Git, and optionally a Helm OCI
  registry), not what the deployed workload's own ServiceAccount can pull
  as its container image; bind IRSA to the workload's ServiceAccount
  separately, per
  [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md).

## Worked example

**Scenario:** Stand up Argo CD from scratch on an existing `payments-prod`
EKS cluster, register a second `payments-staging` EKS cluster as a
destination via IRSA/access entries, and roll `payments-api` out to both
environments via an `ApplicationSet`.

```bash
# Phase 0
eksctl utils associate-iam-oidc-provider --cluster payments-prod --approve

# Phase 1
helm install argocd argo/argo-cd -n argocd --create-namespace --version 7.6.12

# Phase 2 — cross-cluster IRSA + access entry
eksctl create iamserviceaccount --cluster payments-prod --namespace argocd \
  --name argocd-application-controller --role-name argocd-eks-cross-cluster \
  --attach-policy-arn arn:aws:iam::<AWS_ACCOUNT_ID>:policy/ArgoCDAssumeSpokeRole --approve
aws eks create-access-entry --cluster-name payments-staging \
  --principal-arn arn:aws:iam::<AWS_ACCOUNT_ID>:role/argocd-eks-cross-cluster --type STANDARD
aws eks associate-access-policy --cluster-name payments-staging \
  --principal-arn arn:aws:iam::<AWS_ACCOUNT_ID>:role/argocd-eks-cross-cluster \
  --policy-arn arn:aws:eks::aws:cluster-access-policy/AmazonEKSEditPolicy --access-scope type=cluster

# Phase 3 — Ingress/TLS (see linked skills for full manifests)
kubectl apply -f argocd-server-ingress.yaml

# Phase 4 — first Application, manual sync
kubectl apply -f payments-api-staging-application.yaml
argocd app sync payments-api-staging --dry-run
argocd app sync payments-api-staging
```
Phase 5 then replaces the single `Application` with a Cluster-generator
`ApplicationSet` selecting `tier: staging`/`tier: prod` labeled clusters
(full YAML in
[argocd-applicationset-patterns](../argocd-applicationset-patterns/SKILL.md)),
and Phase 6 promotes `staging`'s sync policy to `automated` once the
manual rollout in Phase 4 is confirmed healthy, while `prod` stays manual
per the environment-specific policy guidance in
[argocd-application-configuration](../argocd-application-configuration/SKILL.md).

## Cross-references

- [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md) — EKS cluster/node-group provisioning and IRSA mechanics this skill assumes and builds on.
- [argocd-application-configuration](../argocd-application-configuration/SKILL.md) — full depth on the `Application` spec used in Phase 4/6.
- [argocd-applicationset-patterns](../argocd-applicationset-patterns/SKILL.md) — generator mechanics used in Phase 5.
- [gitops-multi-cluster-management](../gitops-multi-cluster-management/SKILL.md) — hub-and-spoke RBAC/registration pattern this skill's Phase 2 adapts with IRSA.
- [ingress-nginx-configuration](../../../kubernetes-platform/skills/ingress-nginx-configuration/SKILL.md) and [cert-manager-tls-automation](../../../kubernetes-platform/skills/cert-manager-tls-automation/SKILL.md) — Phase 3's Ingress/TLS mechanics.
- [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md) — least-privilege principles governing every IAM role/policy created here.
- [gitops-workflow](../../../devops/skills/gitops-workflow/SKILL.md) — the vendor-neutral GitOps concepts this EKS-specific runbook implements.
