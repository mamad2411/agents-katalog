---
name: managed-kubernetes-eks-aks-gke
description: >
  Guides provisioning and configuring managed Kubernetes clusters on
  AWS EKS, Azure AKS, and Google GKE — cluster creation, node
  group/pool design, and per-cloud workload identity (IRSA on EKS,
  Azure AD Workload Identity on AKS, Workload Identity Federation on
  GKE) so pods get least-privilege cloud API access without long-lived
  keys. Use when a user asks to "create an EKS/AKS/GKE cluster,"
  "set up node groups/node pools," "let a pod assume an IAM role
  without a static key," "configure IRSA," "compare managed Kubernetes
  across clouds," or "size and autoscale cluster nodes."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# Managed Kubernetes: EKS, AKS, GKE

## Purpose

Managed Kubernetes offloads control-plane operation (etcd, API server
HA, upgrades) to the cloud provider, but node groups, networking, and —
most consequentially — how pods authenticate to other cloud services
are still the operator's responsibility to design correctly. Getting
workload identity wrong is the most common and highest-impact mistake:
falling back to long-lived static cloud credentials mounted as
Kubernetes Secrets when a keyless federation mechanism (IRSA, Azure AD
Workload Identity, GKE Workload Identity Federation) was available
recreates exactly the long-lived-credential risk cloud IAM hardening
exists to eliminate. This skill covers cluster/node-group provisioning
and per-cloud workload identity; it assumes the surrounding cloud
account/org structure already exists.

## When to use

- Provisioning a new EKS, AKS, or GKE cluster and deciding control-plane
  version, networking mode, and node group/pool layout.
- Choosing between managed node groups/pools, self-managed nodes, and
  serverless node options (Fargate, AKS/GKE Autopilot) per workload.
- Giving a pod least-privilege access to a cloud API (S3, Blob Storage,
  Cloud Storage; a managed database; a secrets manager) without a
  long-lived static credential.
- Comparing EKS/AKS/GKE feature parity for a specific requirement before
  a cloud/cluster-topology decision.
- Setting up cluster autoscaling (Cluster Autoscaler or each cloud's
  Karpenter-equivalent/native autoscaler) and sizing node pools.
- Troubleshooting a pod that can't reach a cloud API despite the node's
  underlying instance profile/managed identity apparently being correct.

## Prerequisites & environment

- The surrounding cloud account/subscription/project structure and
  guardrails already in place — this skill does **not** cover account
  vending, OU/management-group hierarchy, or org-wide policy; see
  [aws-landing-zone-setup](../../../cloud/skills/aws-landing-zone-setup/SKILL.md),
  [azure-landing-zone-setup](../../../cloud/skills/azure-landing-zone-setup/SKILL.md),
  and [gcp-landing-zone-setup](../../../cloud/skills/gcp-landing-zone-setup/SKILL.md)
  for that layer, and provision the cluster into an account/subscription/
  project that already conforms to your org's landing zone.
- IAM/role permissions to create the control plane, node IAM
  roles/instance profiles or managed identities, and (for workload
  identity) to create/annotate service accounts and configure OIDC
  federation — see
  [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md)
  for the least-privilege design principles that should govern every
  role created here.
- CLI tooling matching the target cloud: `eksctl` ≥ 0.180 or Terraform's
  `aws` provider for EKS; `az aks` CLI ≥ 2.60 for AKS; `gcloud
  container` for GKE — plus `kubectl` and, ideally, the same IaC tool
  (Terraform/OpenTofu) used for the rest of the environment rather than
  mixing imperative CLI cluster creation with declarative everything
  else.
- Kubernetes version support windows differ per cloud and move fast —
  confirm the target version is inside each provider's currently
  supported range (all three providers deprecate old minor versions
  faster than upstream Kubernetes) before pinning a version in IaC.

## Step-by-step guidance

1. **Provision the cluster** with an explicit, pinned Kubernetes
   version and private (or restricted-public) API endpoint access:
   ```bash
   # EKS (eksctl)
   eksctl create cluster --name payments-prod --version 1.30 \
     --region us-east-1 --without-nodegroup \
     --vpc-private-subnets <subnet-ids>
   ```
   ```bash
   # AKS
   az aks create --name payments-prod --resource-group payments-rg \
     --kubernetes-version 1.30 --enable-managed-identity \
     --network-plugin azure --enable-private-cluster
   ```
   ```bash
   # GKE
   gcloud container clusters create payments-prod \
     --release-channel regular --enable-private-nodes \
     --workload-pool=<project-id>.svc.id.goog
   ```
   Prefer a private/restricted API endpoint over fully public in every
   case; each cloud's console/CLI defaults vary, so set this
   explicitly rather than trusting the default.

2. **Design node groups/pools per workload shape**, not one generic
   pool for everything:
   ```bash
   # EKS managed node group, on-demand, general purpose
   eksctl create nodegroup --cluster payments-prod --name general \
     --node-type m6i.large --nodes-min 3 --nodes-max 10 --managed
   ```
   Use Fargate (EKS), Autopilot (GKE), or AKS's virtual-node/serverless
   options for bursty, low-ops-overhead workloads; use dedicated
   spot/preemptible node pools with taints for interruption-tolerant
   batch workloads, keeping stateful/critical workloads off spot capacity.

3. **Set up cluster autoscaling** appropriate to the node group model —
   Cluster Autoscaler (works across all three, watches for unschedulable
   pods) or a cloud-native alternative (Karpenter on EKS gives faster,
   more bin-packing-aware scale-out than the classic Cluster Autoscaler):
   ```yaml
   # Karpenter NodePool (EKS) — minimal example
   apiVersion: karpenter.sh/v1
   kind: NodePool
   metadata: { name: general }
   spec:
     template:
       spec:
         requirements:
           - key: karpenter.sh/capacity-type
             operator: In
             values: ["on-demand"]
     limits: { cpu: "1000" }
   ```

4. **Configure workload identity — EKS (IRSA or Pod Identity)**. IRSA
   maps a Kubernetes ServiceAccount to an IAM role via OIDC federation;
   EKS Pod Identity (newer, simpler setup, no per-role OIDC trust policy
   templating) is the current recommended approach for new clusters on
   supported EKS versions:
   ```bash
   eksctl utils associate-iam-oidc-provider --cluster payments-prod --approve
   eksctl create iamserviceaccount \
     --cluster payments-prod --namespace payments \
     --name payments-api --role-name payments-api-s3-read \
     --attach-policy-arn arn:aws:iam::<ACCOUNT_ID>:policy/PaymentsS3ReadOnly \
     --approve
   ```
   ```yaml
   apiVersion: v1
   kind: ServiceAccount
   metadata:
     name: payments-api
     namespace: payments
     annotations:
       eks.amazonaws.com/role-arn: arn:aws:iam::<ACCOUNT_ID>:role/payments-api-s3-read
   ```
   Pods using this ServiceAccount get temporary, auto-rotated
   credentials via the injected AWS SDK environment/webhook — no static
   access key ever touches the cluster.

5. **Configure workload identity — AKS (Azure AD Workload Identity)**:
   ```bash
   az identity create --name payments-api-identity --resource-group payments-rg
   az identity federated-credential create \
     --name payments-api-fic --identity-name payments-api-identity \
     --resource-group payments-rg \
     --issuer <AKS_OIDC_ISSUER_URL> \
     --subject system:serviceaccount:payments:payments-api
   ```
   ```yaml
   apiVersion: v1
   kind: ServiceAccount
   metadata:
     name: payments-api
     namespace: payments
     annotations:
       azure.workload.identity/client-id: <MANAGED_IDENTITY_CLIENT_ID>
     labels:
       azure.workload.identity/use: "true"
   ```

6. **Configure workload identity — GKE (Workload Identity Federation)**:
   ```bash
   gcloud iam service-accounts add-iam-policy-binding \
     payments-api-gsa@<project-id>.iam.gserviceaccount.com \
     --role roles/iam.workloadIdentityUser \
     --member "serviceAccount:<project-id>.svc.id.goog[payments/payments-api]"
   ```
   ```yaml
   apiVersion: v1
   kind: ServiceAccount
   metadata:
     name: payments-api
     namespace: payments
     annotations:
       iam.gke.io/gcp-service-account: payments-api-gsa@<project-id>.iam.gserviceaccount.com
   ```

7. **Attach the ServiceAccount to the workload** (identical pattern
   across all three clouds — only annotations/webhooks differ):
   ```yaml
   spec:
     template:
       spec:
         serviceAccountName: payments-api
         containers:
           - name: payments-api
             image: ghcr.io/example/payments-api:1.4.2
   ```

8. **Verify least privilege end-to-end**: confirm the pod can perform
   only the intended cloud API calls and nothing more by testing from
   inside the pod (`aws sts get-caller-identity`, `az account show`,
   `gcloud auth list`) and cross-checking the bound role/policy's
   actual permissions against
   [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md)'s
   least-privilege review guidance — a workload-identity binding is only
   as safe as the policy it's bound to.

## Best practices

- Never fall back to mounting a long-lived cloud access key/service
  account JSON as a Kubernetes Secret "to get unblocked quickly" — every
  major managed Kubernetes offering now has a mature, federation-based
  workload identity mechanism; a static key defeats the credential
  rotation and blast-radius benefits the platform otherwise provides.
- Scope one IAM role/managed identity/GCP service account per workload
  (or tightly-related workload group), not one shared identity for an
  entire namespace or cluster — a shared identity means every workload
  in that scope inherits every other workload's permissions.
- Separate node pools by workload sensitivity and interruption
  tolerance: keep stateful/critical workloads off spot/preemptible
  capacity, and use taints+tolerations (not just node selectors) so
  scheduling mistakes fail closed rather than silently landing sensitive
  pods on the wrong pool.
- Pin and stagger control-plane and node version upgrades — test the
  new version's compatibility with installed CRDs/webhooks (Istio,
  cert-manager, ingress-nginx, any Operators) in a non-prod cluster
  before rolling to prod, since managed control planes can auto-upgrade
  on a schedule if not pinned.
- Keep the cluster's node IAM role/managed identity itself scoped to
  what nodes need structurally (pulling images, CNI/CSI operations,
  logging) — don't let broad workload-level permissions get attached at
  the node level "for convenience," since that grants it to every pod on
  the node regardless of that pod's own service account.
- Enable and route control-plane audit logs (EKS control plane logging,
  AKS diagnostic settings, GKE audit logs) to the same central log
  destination your landing zone already established, rather than
  leaving them cluster-local and unreviewed.

## Common pitfalls

- **Symptom:** A pod's cloud SDK calls fail with an access-denied error
  even though the IAM role/managed identity clearly has the needed
  permission attached.
  **Fix:** Check that the ServiceAccount annotation, the trust
  policy/federated credential's `subject` (must exactly match
  `system:serviceaccount:<namespace>:<name>`), and the pod's actual
  `serviceAccountName` all agree — a namespace or ServiceAccount name
  typo in any one of the three breaks the federation silently, and the
  pod instead falls back to (or fails entirely without) the node's own
  identity, not the intended workload identity.

- **Symptom:** Cluster autoscaler or Karpenter doesn't scale out despite
  clearly unschedulable pods.
  **Fix:** Check for a node group/pool at its configured max size, an
  IAM/managed-identity permission the autoscaler component itself needs
  (to call the cloud's scale-set/instance-group API) that's missing, or
  a pod requesting a resource combination (e.g. a specific GPU type) no
  configured node pool can satisfy — `kubectl describe pod` and the
  autoscaler component's own logs (not just cluster events) usually
  pinpoint which.

- **Symptom:** A control-plane version auto-upgraded and an installed
  Operator/webhook (Istio, cert-manager, an admission webhook) started
  failing immediately after.
  **Fix:** Managed control planes can enforce upgrades on a schedule
  once a version reaches end-of-support, regardless of whether the
  cluster owner is ready. Pin and proactively schedule upgrades ahead of
  the provider's forced timeline, and validate every installed
  CRD/webhook's compatibility with the target minor version in a
  non-prod cluster first.

- **Symptom:** A workload identity binding works for one namespace's
  ServiceAccount but a second, differently-named ServiceAccount
  intended for the same workload in another namespace doesn't get the
  same access.
  **Fix:** Workload identity trust bindings (IRSA trust policy, Azure AD
  federated credential subject, GKE `workloadIdentityUser` binding) are
  scoped to an exact `namespace:serviceaccount` pair — copying a
  Deployment to a new namespace without also creating and binding a
  matching ServiceAccount in that namespace leaves it with no (or the
  node's default, broader) identity.

- **Symptom:** Node pool costs are far higher than expected for the
  actual workload.
  **Fix:** Check for over-provisioned `requests` driving the autoscaler
  to add nodes well beyond actual usage, a lack of spot/preemptible
  usage for interruption-tolerant workloads, or idle node pools left at
  a nonzero minimum size — reconcile node pool minimums against actual
  baseline load, not against a "just in case" buffer chosen at initial
  setup and never revisited.

## Worked example

**Scenario:** Provision an EKS cluster with a general-purpose managed
node group and give `payments-api` least-privilege, read-only access to
a specific S3 bucket via IRSA — no static AWS keys anywhere.

```bash
eksctl create cluster --name payments-prod --version 1.30 \
  --region us-east-1 --vpc-private-subnets <subnet-ids> --without-nodegroup

eksctl create nodegroup --cluster payments-prod --name general \
  --node-type m6i.large --nodes-min 3 --nodes-max 10 --managed

eksctl utils associate-iam-oidc-provider --cluster payments-prod --approve
```

```json
// payments-s3-read-policy.json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:GetObject", "s3:ListBucket"],
    "Resource": [
      "arn:aws:s3:::payments-statements-prod",
      "arn:aws:s3:::payments-statements-prod/*"
    ]
  }]
}
```

```bash
aws iam create-policy --policy-name PaymentsS3ReadOnly \
  --policy-document file://payments-s3-read-policy.json

eksctl create iamserviceaccount \
  --cluster payments-prod --namespace payments \
  --name payments-api --role-name payments-api-s3-read \
  --attach-policy-arn arn:aws:iam::<ACCOUNT_ID>:policy/PaymentsS3ReadOnly \
  --approve
```

```bash
kubectl set serviceaccount deployment/payments-api payments-api -n payments
kubectl exec -n payments deploy/payments-api -- aws sts get-caller-identity
```

The `sts get-caller-identity` output shows the assumed
`payments-api-s3-read` role's ARN (not the node's own instance-profile
identity), and `aws s3 ls s3://payments-statements-prod` succeeds from
inside the pod while any write or delete call to that bucket, or any
call to an unrelated bucket, fails with `AccessDenied` — confirming both
the federation and the least-privilege scope are working as intended.

## Cross-references

- [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md) — CNI options and constraints specific to self-managed-CNI configurations on these managed clusters.
- [ingress-nginx-configuration](../ingress-nginx-configuration/SKILL.md) — installing an Ingress controller on top of a freshly provisioned cluster.
- [helm-chart-authoring](../helm-chart-authoring/SKILL.md) — packaging and deploying workloads onto the cluster once provisioned.
- [aws-landing-zone-setup](../../../cloud/skills/aws-landing-zone-setup/SKILL.md), [azure-landing-zone-setup](../../../cloud/skills/azure-landing-zone-setup/SKILL.md), [gcp-landing-zone-setup](../../../cloud/skills/gcp-landing-zone-setup/SKILL.md) — the account/subscription/project and org-policy layer this skill assumes already exists.
- [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md) — least-privilege policy design principles that should govern every IAM role/managed identity created for workload identity here.
