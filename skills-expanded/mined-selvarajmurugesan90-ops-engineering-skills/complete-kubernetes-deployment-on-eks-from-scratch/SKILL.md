---
name: complete-kubernetes-deployment-on-eks-from-scratch
description: >
  Sequences a complete, end-to-end EKS deployment from a bare AWS account to
  a production-ready cluster serving a first workload — landing zone/IAM
  prerequisites, EKS cluster and node group provisioning, VPC CNI (with the
  Calico/Cilium alternative noted), ingress (ALB vs. ingress-nginx), cert-
  manager with Route 53 DNS-01, conformance validation, a Helm-deployed
  workload, and a node/cluster health baseline. This is an integration/
  orchestration skill that sequences several existing tool-specific skills
  in the correct order and flags the handoff points between them — it does
  not restate their internals. Use when a user asks to "deploy a Kubernetes
  cluster on EKS from scratch," "stand up a new EKS environment end to
  end," "build a production EKS cluster from a fresh AWS account," or
  "give me the full sequence to go from nothing to a working EKS cluster."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# Complete Kubernetes Deployment on EKS From Scratch

## Purpose

Standing up a production-ready EKS cluster is not one task — it is roughly
eight tasks that must happen in a specific order, each with its own
existing skill in this repository covering the depth. Get the order wrong
(most commonly: standing up cert-manager's DNS-01 solver before the IAM/
OIDC federation it needs exists, or declaring a cluster "done" the moment
`kubectl get nodes` shows `Ready`) and the result is a cluster that looks
finished but fails the first time someone actually depends on it — a stuck
`Certificate`, an Ingress that never gets a usable address, or a CNI
NetworkPolicy that silently no-ops. This skill is the AWS-specific
end-to-end runbook: it sequences AWS landing zone/IAM prerequisites, EKS
provisioning, VPC CNI, ingress, cert-manager, conformance validation, a
first workload, and a health baseline into one ordered path, cross-
referencing the tool-specific skill that covers each phase's actual detail
rather than repeating it here.

## When to use

- Deploying a brand-new EKS cluster into an AWS account for the first
  time, from a landing zone that already exists but has no Kubernetes
  workload on it yet.
- Auditing an existing EKS rollout for a skipped or out-of-order phase
  (e.g. cert-manager installed before its IAM role existed, or a cluster
  handed to application teams with no conformance/smoke validation ever
  run).
- Rebuilding a reference EKS environment (a second region, a DR cluster,
  a new business unit's cluster) that should follow the exact same
  sequence as a known-good first cluster.
- Onboarding a team unfamiliar with how the individual EKS/CNI/ingress/
  cert-manager skills in this repository fit together into one coherent
  deployment.

## Prerequisites & environment

- An AWS account that already conforms to the organization's landing
  zone — account vended through Account Factory, baseline guardrails
  (SCPs, CloudTrail, Config) already applied. This skill does **not**
  cover vending the account itself; see
  [aws-landing-zone-setup](../../../cloud/skills/aws-landing-zone-setup/SKILL.md).
  Provisioning an EKS cluster directly into an ungoverned flat account
  works mechanically but inherits none of the landing zone's guardrails
  retroactively.
- IAM permissions to create the EKS cluster/node IAM roles, an OIDC
  identity provider, and IRSA-scoped roles — see
  [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md)
  for the least-privilege design that should govern every role created in
  Phase 1.
- A Route 53 public hosted zone already delegated for the domain
  cert-manager will issue certificates for (Phase 4 depends on this
  existing before DNS-01 can succeed).
- `eksctl` ≥ 0.180, `kubectl`, `helm` ≥ 3.14, and `awscli` v2 authenticated
  against the target account.
- A non-production AWS account/VPC to rehearse this exact sequence in at
  least once before running it against a production account — several of
  the phases below (OIDC association, DNS-01 issuance against Let's
  Encrypt production) have real, hard-to-reverse side effects the first
  time through.

## Step-by-step guidance

This is the phase sequence. Each phase links to the skill that covers its
full depth; the text here covers only EKS-specific sequencing and
integration decisions.

1. **Phase 1 — AWS landing zone & IAM prerequisites.** Confirm the target
   account sits in the correct OU with guardrails applied (see
   [aws-landing-zone-setup](../../../cloud/skills/aws-landing-zone-setup/SKILL.md)).
   Critically, **decide and pre-plan every IAM role this cluster will need
   via IRSA/Pod Identity now** — not just the cluster/node roles, but the
   cert-manager Route 53 DNS-01 role and the workload's own application
   role from Phase 7. Planning these together avoids re-running IAM
   Terraform/eksctl commands per phase later:
   ```bash
   aws iam create-policy --policy-name Route53DNS01Payments \
     --policy-document file://route53-dns01-policy.json
   ```
   See [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md)
   for scoping this policy to the specific hosted zone ID only.

2. **Phase 2 — Provision the EKS cluster and node group.** Use
   [managed-kubernetes-eks-aks-gke](../managed-kubernetes-eks-aks-gke/SKILL.md)
   for the full `eksctl create cluster`/node group/IRSA setup detail.
   EKS-specific sequencing point: associate the OIDC provider **in this
   phase**, even though the first IRSA role that consumes it (cert-manager,
   Phase 5) doesn't exist yet — associating it later requires no
   destructive action, but planning it here means Phase 5 is a five-minute
   `eksctl create iamserviceaccount` instead of a cluster-level change:
   ```bash
   eksctl create cluster --name payments-prod --version 1.30 \
     --region us-east-1 --vpc-private-subnets <subnet-ids> --without-nodegroup
   eksctl create nodegroup --cluster payments-prod --name general \
     --node-type m6i.large --nodes-min 3 --nodes-max 10 --managed
   eksctl utils associate-iam-oidc-provider --cluster payments-prod --approve
   ```

3. **Phase 3 — CNI: VPC CNI by default.** EKS ships the AWS VPC CNI
   (`aws-node` DaemonSet) pre-installed — unlike self-managed kubeadm/K3s
   clusters, **there is no "install a CNI" step for the default path**; a
   fresh EKS cluster's nodes reach `Ready` immediately because VPC CNI is
   already running. Confirm it's healthy and sized correctly for the node
   type's max-pods-per-node limit (VPC CNI allocates pod IPs directly from
   VPC ENIs, so pod density per node is capped by instance ENI/IP limits,
   not an arbitrary Kubernetes default):
   ```bash
   kubectl get daemonset aws-node -n kube-system
   kubectl describe configmap amazon-vpc-cni -n kube-system
   ```
   **Alternative:** if `NetworkPolicy` enforcement beyond VPC CNI's native
   (limited, opt-in) policy support is required, or a non-AWS-specific CNI
   is preferred for portability, replace VPC CNI with Calico or Cilium —
   see
   [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md)
   for the tradeoffs; this is a deliberate, planned swap done before any
   workload is scheduled, not a default recommendation for most EKS
   clusters.

4. **Phase 4 — Ingress: ALB vs. ingress-nginx, and DNS wiring.** Decide
   deliberately, since this determines the load-balancer story for the
   rest of the deployment:
   - **AWS Load Balancer Controller (ALB Ingress)** — native integration,
     provisions a real AWS Application Load Balancer per Ingress/
     IngressGroup, target-type `ip` routes directly to pod IPs (works
     cleanly with VPC CNI's pod-ENI addressing). Preferred when ALB-
     specific features (WAF association, Cognito auth at the LB) are
     needed.
   - **ingress-nginx** behind a `Service` of `type: LoadBalancer`
     (provisions a Network Load Balancer) — see
     [ingress-nginx-configuration](../ingress-nginx-configuration/SKILL.md)
     for the full install/annotation detail. Preferred for parity with
     non-AWS clusters (AKS/GKE/on-prem) running the same ingress-nginx
     configuration everywhere.
   Either way, once the controller has an external address, create the
   Route 53 record pointing at it **before** Phase 5's DNS-01 challenge
   needs to resolve — DNS-01 validates against the zone's actual `TXT`
   records, not the Ingress's `A`/`CNAME` record, but a missing
   application DNS record here means Phase 7's workload is unreachable
   even after TLS succeeds.

5. **Phase 5 — cert-manager with Route 53 DNS-01.** Install cert-manager
   and configure a `ClusterIssuer` per
   [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md).
   The EKS-specific integration point: cert-manager's Route 53 API calls
   must authenticate via the IRSA role planned in Phase 1 and the OIDC
   provider associated in Phase 2 — **not** a static AWS access key:
   ```bash
   eksctl create iamserviceaccount \
     --cluster payments-prod --namespace cert-manager \
     --name cert-manager --role-name cert-manager-route53-dns01 \
     --attach-policy-arn arn:aws:iam::<ACCOUNT_ID>:policy/Route53DNS01Payments \
     --approve
   helm install cert-manager jetstack/cert-manager \
     --namespace cert-manager --create-namespace --version v1.15.1 \
     --set crds.enabled=true --set serviceAccount.create=false \
     --set serviceAccount.name=cert-manager
   ```
   Validate against Let's Encrypt staging first, exactly as
   [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md)
   describes, before cutting over to production.

6. **Phase 6 — Conformance and smoke validation.** Run Sonobuoy quick
   mode, then full `certified-conformance`, then the targeted DNS/storage/
   ingress smoke tests — see
   [kubernetes-cluster-post-provision-conformance-validation](../kubernetes-cluster-post-provision-conformance-validation/SKILL.md).
   For EKS specifically, also confirm the `gp3`/`ebs-csi` default
   `StorageClass` (via the EBS CSI driver add-on) actually provisions a
   PVC — a common EKS-specific gap is the EBS CSI driver add-on not being
   enabled at cluster creation, which the generic conformance suite
   surfaces as a storage-test failure that traces back to a missing
   EKS add-on, not a Kubernetes defect.

7. **Phase 7 — Deploy the first workload via Helm.** Package and install
   per
   [helm-chart-authoring](../helm-chart-authoring/SKILL.md), using the
   IRSA ServiceAccount pattern from
   [managed-kubernetes-eks-aks-gke](../managed-kubernetes-eks-aks-gke/SKILL.md)
   for any of the workload's own AWS API access (its own IAM role,
   planned back in Phase 1, is distinct from cert-manager's):
   ```bash
   helm upgrade --install payments-api oci://ghcr.io/example/charts/payments-api \
     --version 2.3.0 --namespace payments --create-namespace --atomic --timeout 5m
   ```

8. **Phase 8 — Node/cluster health baseline.** Establish the ongoing
   operational baseline before declaring the cluster handed off: node
   drain/cordon discipline and `NotReady` diagnosis via
   [kubernetes-node-maintenance-and-troubleshooting](../kubernetes-node-maintenance-and-troubleshooting/SKILL.md).
   **Note what does *not* apply here:** EKS's control plane and etcd are
   fully AWS-managed — the procedures in
   [etcd-backup-restore-and-cluster-health](../etcd-backup-restore-and-cluster-health/SKILL.md)
   do not apply to this cluster at all (there is no customer-accessible
   `etcdctl` endpoint); rely on EKS control-plane logging (enabled to the
   landing zone's central log destination) instead of etcd-level
   snapshotting for control-plane observability.

## Best practices

- Plan every IRSA role the cluster will ever need (cert-manager, the
  workload, any future add-on) during Phase 1, even though most of them
  aren't created until later phases — retrofitting IAM design after the
  cluster exists means re-deriving least-privilege scopes under time
  pressure instead of deliberately up front.
- Treat Phase 6 (conformance validation) as a hard gate before Phase 7 —
  deploying a real workload onto an unvalidated cluster means any Phase
  3/4 misconfiguration (CNI, storage, ingress) surfaces as a confusing
  application-level bug instead of a clean pre-handoff finding.
- Rehearse this entire sequence in a non-production account at least once
  — several phases (OIDC association, Let's Encrypt production issuance)
  have effects that are awkward, not impossible, to undo, and doing so is
  much cheaper before production DNS records point at anything.
- Keep the whole sequence as versioned IaC (Terraform/eksctl config
  files, Helm values, cert-manager manifests) in one repository per
  cluster, not a mix of remembered CLI invocations — this is what makes
  Phase reproduction for a second cluster (DR, new region) fast and
  correct.
- Route every phase's audit-relevant logs (EKS control-plane logs,
  cert-manager events, Ingress access logs) to the landing zone's central
  logging destination from day one, not as an afterthought once the
  cluster is already handling production traffic.

## Common pitfalls

- **Symptom:** cert-manager's `Certificate` resource in Phase 5 never
  progresses past `Pending`, with the DNS-01 `Challenge` object showing
  an authentication or authorization error calling Route 53.
  **Fix:** This almost always traces back to Phase 1: the IRSA policy was
  either never scoped to the specific hosted zone ID, or the OIDC
  provider from Phase 2 wasn't associated before the `iamserviceaccount`
  was created in Phase 5, leaving the ServiceAccount with no valid trust
  relationship. Confirm the trust policy's `subject` matches
  `system:serviceaccount:cert-manager:cert-manager` exactly and that the
  policy document references the exact hosted zone ARN, not a wildcard.

- **Symptom:** The ALB or NLB provisioned in Phase 4 comes up healthy, but
  Phase 5's DNS-01 challenge still fails validation.
  **Fix:** DNS-01 validates against the hosted zone's `TXT` records via
  the Route 53 API directly — it does not depend on the Ingress/Service
  having a working `A`/`CNAME` record at all. A failure here means the
  IAM role can't write to the zone (see the pitfall above), not an
  ingress misconfiguration; don't waste time debugging the load balancer
  when the actual failure is in cert-manager's Route 53 API calls.

- **Symptom:** The cluster is declared "production ready" and handed to
  an application team the same day Phase 2 (cluster/node group creation)
  completes, skipping Phases 6 entirely — and a NetworkPolicy the
  application team relies on turns out to be a silent no-op once real
  traffic patterns exercise it weeks later.
  **Fix:** This is exactly the gap
  [kubernetes-cluster-post-provision-conformance-validation](../kubernetes-cluster-post-provision-conformance-validation/SKILL.md)
  exists to catch before handoff, not after. Treat Phase 6 as a required
  gate in the sequence, not an optional step skipped under deadline
  pressure — if VPC CNI was swapped for Calico in Phase 3 specifically
  for `NetworkPolicy` enforcement, the smoke test must include an actual
  positive/negative connectivity test of that policy, not just a
  conformance pass.

- **Symptom:** A storage smoke test in Phase 6 fails with PVCs stuck
  `Pending`, even though the cluster otherwise looks healthy.
  **Fix:** EKS does not enable the EBS CSI driver by default — it's an
  optional add-on. Confirm it was enabled during Phase 2
  (`eksctl create addon --name aws-ebs-csi-driver`) rather than assuming
  every EKS cluster ships a working default `StorageClass` out of the
  box the way a fresh kubeadm-with-Longhorn or a GKE cluster might.

## Worked example

**Scenario:** Deploy `payments-api` end-to-end on a new EKS cluster in a
freshly vended AWS account, with ingress-nginx (for parity with an
existing AKS cluster running the same application), Route 53 DNS-01, and
a full validation gate before handoff.

```bash
# Phase 1 — IAM prerequisite for cert-manager, planned now
aws iam create-policy --policy-name Route53DNS01Payments \
  --policy-document file://route53-dns01-policy.json

# Phase 2 — cluster + nodes + OIDC
eksctl create cluster --name payments-prod --version 1.30 \
  --region us-east-1 --vpc-private-subnets subnet-aaa,subnet-bbb --without-nodegroup
eksctl create nodegroup --cluster payments-prod --name general \
  --node-type m6i.large --nodes-min 3 --nodes-max 10 --managed
eksctl create addon --cluster payments-prod --name aws-ebs-csi-driver
eksctl utils associate-iam-oidc-provider --cluster payments-prod --approve

# Phase 3 — VPC CNI is already running; confirm health
kubectl get daemonset aws-node -n kube-system

# Phase 4 — ingress-nginx via Helm, NLB-backed
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx --create-namespace \
  --set controller.service.type=LoadBalancer
kubectl get svc -n ingress-nginx ingress-nginx-controller   # note EXTERNAL-IP
# create Route 53 A/ALIAS record for payments.example.com -> that NLB

# Phase 5 — cert-manager with IRSA-backed Route 53 DNS-01
eksctl create iamserviceaccount \
  --cluster payments-prod --namespace cert-manager \
  --name cert-manager --role-name cert-manager-route53-dns01 \
  --attach-policy-arn arn:aws:iam::<ACCOUNT_ID>:policy/Route53DNS01Payments --approve
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace --version v1.15.1 \
  --set crds.enabled=true --set serviceAccount.create=false --set serviceAccount.name=cert-manager
kubectl apply -f route53-staging-issuer.yaml   # validate, then swap to prod issuer

# Phase 6 — validation gate
sonobuoy run --mode quick --wait && sonobuoy results "$(sonobuoy retrieve)"
sonobuoy run --mode certified-conformance --wait && sonobuoy results "$(sonobuoy retrieve)" --mode=report

# Phase 7 — first workload
helm upgrade --install payments-api oci://ghcr.io/example/charts/payments-api \
  --version 2.3.0 --namespace payments --create-namespace --atomic --timeout 5m

# Phase 8 — health baseline
kubectl get nodes
kubectl get pdb -A
```

`curl -I https://payments.example.com` returns `HTTP/2 200` with a
Let's Encrypt production certificate, confirming Phases 1–7 wired
together correctly end to end, and the cluster's node maintenance
runbook (Phase 8) is in place before the first planned patch window.

## Cross-references

- [aws-landing-zone-setup](../../../cloud/skills/aws-landing-zone-setup/SKILL.md) — the account/OU/guardrail layer this sequence assumes already exists.
- [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md) — least-privilege design for every IAM role created across Phases 1, 5, and 7.
- [managed-kubernetes-eks-aks-gke](../managed-kubernetes-eks-aks-gke/SKILL.md) — full detail for Phase 2's cluster/node group/IRSA provisioning.
- [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md) — the Calico/Cilium alternative to VPC CNI referenced in Phase 3.
- [ingress-nginx-configuration](../ingress-nginx-configuration/SKILL.md) — full detail for the ingress-nginx path in Phase 4.
- [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md) — full detail for Phase 5's Issuer/Certificate setup.
- [kubernetes-cluster-post-provision-conformance-validation](../kubernetes-cluster-post-provision-conformance-validation/SKILL.md) — full detail for Phase 6's validation gate.
- [helm-chart-authoring](../helm-chart-authoring/SKILL.md) — full detail for Phase 7's chart packaging and release discipline.
- [kubernetes-node-maintenance-and-troubleshooting](../kubernetes-node-maintenance-and-troubleshooting/SKILL.md) — the ongoing operational baseline established in Phase 8.
- [etcd-backup-restore-and-cluster-health](../etcd-backup-restore-and-cluster-health/SKILL.md) — explains why its procedures do not apply to this managed control plane.
