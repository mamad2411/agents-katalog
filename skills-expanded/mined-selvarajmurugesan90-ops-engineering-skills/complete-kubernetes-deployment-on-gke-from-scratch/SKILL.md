---
name: complete-kubernetes-deployment-on-gke-from-scratch
description: >
  Sequences a complete, end-to-end GKE deployment from a bare GCP project to
  a production-ready cluster serving a first workload — GCP landing zone
  prerequisites, GKE cluster and node pool provisioning, VPC-native/
  Dataplane V2 CNI (with the Calico alternative noted), ingress (GKE
  Ingress/Gateway API vs. ingress-nginx), cert-manager with Cloud DNS,
  conformance validation, a Helm-deployed workload, and a node/cluster
  health baseline. This is an integration/orchestration skill that
  sequences several existing tool-specific skills in the correct order and
  flags the handoff points between them — it does not restate their
  internals. Use when a user asks to "deploy a Kubernetes cluster on GKE
  from scratch," "set up a new GKE environment end to end," "build a
  production GKE cluster from a fresh GCP project," or "give me the full
  sequence to go from nothing to a working GKE cluster."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# Complete Kubernetes Deployment on GKE From Scratch

## Purpose

A GKE cluster showing every node `Ready` is not the same claim as "this
environment is ready for a production workload" — the Workload Identity
Federation pool binding, the Shared VPC attachment it depends on, the
Dataplane V2 (Cilium-based) networking mode chosen at creation, and cert-
manager's Cloud DNS credentials each have their own setup order. Skip or
misorder any of them and the cluster looks finished right up until
something depends on the piece that was never wired up. This skill is the
GCP-specific end-to-end runbook: it sequences GCP landing zone
prerequisites, GKE provisioning, CNI/Dataplane V2, ingress, cert-manager
with Cloud DNS, conformance validation, a first workload, and a health
baseline into one ordered path, cross-referencing the tool-specific skill
that covers each phase's actual detail.

## When to use

- Deploying a brand-new GKE cluster into a GCP project for the first
  time, where the project already exists inside the org's folder
  hierarchy and Shared VPC but has no Kubernetes workload yet.
- Auditing an existing GKE rollout for a skipped or out-of-order phase
  (e.g. cert-manager configured before its Workload Identity binding
  existed, or a cluster handed off with no conformance validation).
- Rebuilding a reference GKE environment (a second region, a DR cluster)
  that should follow the same sequence as a known-good first cluster.
- Onboarding a team unfamiliar with how the individual GKE/CNI/ingress/
  cert-manager skills in this repository fit together into one coherent
  deployment.

## Prerequisites & environment

- A GCP project already vended through the org's project factory and
  attached to the correct folder and Shared VPC — this skill does **not**
  cover folder/Organization Policy design or project vending; see
  [gcp-landing-zone-setup](../../../cloud/skills/gcp-landing-zone-setup/SKILL.md).
- IAM rights to create the GKE cluster, GCP service accounts, and
  Workload Identity Federation bindings — see
  [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md)
  for the least-privilege design that should govern every service account
  binding created in Phase 1.
- A Cloud DNS public managed zone already delegated for the domain
  cert-manager will issue certificates for (Phase 4 depends on this
  existing before DNS-01 can succeed).
- `gcloud` ≥ 470.0.0, `kubectl`, and `helm` ≥ 3.14 authenticated against
  the target project.
- A non-production project to rehearse this sequence in first — the
  Shared VPC attachment and Workload Identity pool decisions in Phases
  2–3 are not free to redo once real workloads depend on them.

## Step-by-step guidance

This is the phase sequence. Each phase links to the skill that covers its
full depth; the text here covers only GKE-specific sequencing and
integration decisions.

1. **Phase 1 — GCP landing zone & IAM prerequisites.** Confirm the
   project sits in the correct folder, is attached to the Shared VPC host
   project, and inherits the org's Organization Policy constraints (see
   [gcp-landing-zone-setup](../../../cloud/skills/gcp-landing-zone-setup/SKILL.md)).
   GKE-specific sequencing point: **create the GCP service accounts this
   cluster will need now**, even though their Workload Identity bindings
   (which need the cluster's Workload Identity pool from Phase 2) can't
   be finished until after the cluster exists:
   ```bash
   gcloud iam service-accounts create payments-api-gsa --project=<PROJECT_ID>
   gcloud iam service-accounts create cert-manager-dns01-gsa --project=<PROJECT_ID>
   gcloud projects add-iam-policy-binding <PROJECT_ID> \
     --member="serviceAccount:cert-manager-dns01-gsa@<PROJECT_ID>.iam.gserviceaccount.com" \
     --role="roles/dns.admin" --condition=None
   ```
   Scope `roles/dns.admin` down to a custom role restricted to the
   specific managed zone rather than project-wide DNS admin — see
   [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md).

2. **Phase 2 — Provision the GKE cluster and node pools.** Use
   [managed-kubernetes-eks-aks-gke](../managed-kubernetes-eks-aks-gke/SKILL.md)
   for the full `gcloud container clusters create`/node pool/Workload
   Identity setup detail. GKE-specific sequencing point: Workload Identity
   Federation is enabled via `--workload-pool` at cluster creation, and
   the cluster must attach to the Shared VPC host project's subnet
   explicitly if it isn't a standalone-VPC project:
   ```bash
   gcloud container clusters create payments-prod \
     --release-channel regular --enable-private-nodes \
     --workload-pool=<PROJECT_ID>.svc.id.goog \
     --network=projects/<HOST_PROJECT_ID>/global/networks/shared-vpc \
     --subnetwork=projects/<HOST_PROJECT_ID>/regions/us-central1/subnetworks/gke-prod
   ```

3. **Phase 3 — CNI: VPC-native with Dataplane V2 by default.** GKE
   clusters created with `--enable-dataplane-v2` (the current default for
   new clusters in most release channels) use a Cilium-based CNI with
   built-in `NetworkPolicy` enforcement out of the box — unlike EKS's VPC
   CNI (limited native policy support) or AKS's default CNI modes
   (policy requires a separate add-on), **GKE's default CNI already
   enforces `NetworkPolicy` with no additional installation**:
   ```bash
   kubectl get pods -n kube-system -l k8s-app=cilium
   ```
   Confirm this explicitly rather than assuming policy enforcement is
   missing and reaching for Calico unnecessarily — the most common
   GKE-specific mistake in this phase is installing Calico "to get
   NetworkPolicy support" on a cluster that already enforces it via
   Dataplane V2, creating two competing dataplanes.
   **Alternative:** legacy GKE clusters or those still on the older
   route-based (non-VPC-native) networking mode may need an explicit CNI
   decision — see
   [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md)
   for the underlying Calico tradeoffs if Dataplane V2 is deliberately
   disabled for a specific compatibility reason.

4. **Phase 4 — Ingress: GKE Ingress/Gateway API vs. ingress-nginx, and
   DNS wiring.** Decide deliberately:
   - **GKE Ingress (or the newer Gateway API implementation)** — native
     integration provisioning a Google Cloud external HTTP(S) Load
     Balancer directly from Ingress/Gateway resources, with Google-
     managed certificates as an alternative to cert-manager for the
     simplest cases.
   - **ingress-nginx** behind a `Service` of `type: LoadBalancer`
     (provisions a Google Cloud Network Load Balancer) — see
     [ingress-nginx-configuration](../ingress-nginx-configuration/SKILL.md)
     for full install/annotation detail; preferred for parity with
     non-GCP clusters running the same ingress-nginx configuration and
     for keeping cert-manager (rather than Google-managed certs) as the
     single certificate-issuance mechanism across all clouds.
   Once the controller has an external address, create the Cloud DNS
   record pointing at it **before** Phase 5's DNS-01 challenge needs to
   resolve.

5. **Phase 5 — cert-manager with Cloud DNS.** Install cert-manager and
   configure a `ClusterIssuer` per
   [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md),
   substituting Cloud DNS for the Route 53 example shown there. The
   GKE-specific integration point: bind the `cert-manager-dns01-gsa`
   planned in Phase 1 to the cluster's Kubernetes ServiceAccount via
   Workload Identity Federation, using the pool enabled in Phase 2:
   ```bash
   gcloud iam service-accounts add-iam-policy-binding \
     cert-manager-dns01-gsa@<PROJECT_ID>.iam.gserviceaccount.com \
     --role roles/iam.workloadIdentityUser \
     --member "serviceAccount:<PROJECT_ID>.svc.id.goog[cert-manager/cert-manager]"
   ```
   ```yaml
   apiVersion: v1
   kind: ServiceAccount
   metadata:
     name: cert-manager
     namespace: cert-manager
     annotations:
       iam.gke.io/gcp-service-account: cert-manager-dns01-gsa@<PROJECT_ID>.iam.gserviceaccount.com
   ---
   apiVersion: cert-manager.io/v1
   kind: ClusterIssuer
   metadata: { name: letsencrypt-dns }
   spec:
     acme:
       server: https://acme-v02.api.letsencrypt.org/directory
       email: platform-team@example.com
       privateKeySecretRef: { name: letsencrypt-dns-account-key }
       solvers:
         - dns01:
             cloudDNS:
               project: <PROJECT_ID>
               hostedZoneName: example-com
           selector: { dnsZones: ["example.com"] }
   ```
   Validate against Let's Encrypt staging first, exactly as
   [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md)
   describes.

6. **Phase 6 — Conformance and smoke validation.** Run Sonobuoy quick
   mode, then full `certified-conformance`, then targeted smoke tests —
   see
   [kubernetes-cluster-post-provision-conformance-validation](../kubernetes-cluster-post-provision-conformance-validation/SKILL.md).
   For GKE specifically, also run a positive/negative `NetworkPolicy`
   smoke test given Dataplane V2's built-in enforcement from Phase 3 —
   confirming the policy is actually enforced (not merely accepted by the
   API server) closes a gap generic conformance doesn't cover, and
   confirm the default `standard-rwo` `StorageClass` (Persistent Disk CSI
   driver) provisions a PVC.

7. **Phase 7 — Deploy the first workload via Helm.** Package and install
   per
   [helm-chart-authoring](../helm-chart-authoring/SKILL.md), completing
   the `payments-api-gsa` Workload Identity binding from Phase 1 the same
   way Phase 5 completed cert-manager's:
   ```bash
   gcloud iam service-accounts add-iam-policy-binding \
     payments-api-gsa@<PROJECT_ID>.iam.gserviceaccount.com \
     --role roles/iam.workloadIdentityUser \
     --member "serviceAccount:<PROJECT_ID>.svc.id.goog[payments/payments-api]"
   helm upgrade --install payments-api oci://ghcr.io/example/charts/payments-api \
     --version 2.3.0 --namespace payments --create-namespace --atomic --timeout 5m
   ```

8. **Phase 8 — Node/cluster health baseline.** Establish the ongoing
   operational baseline: node drain/cordon discipline and `NotReady`
   diagnosis via
   [kubernetes-node-maintenance-and-troubleshooting](../kubernetes-node-maintenance-and-troubleshooting/SKILL.md).
   **Note what does *not* apply here:** GKE's control plane and etcd are
   fully Google-managed — the procedures in
   [etcd-backup-restore-and-cluster-health](../etcd-backup-restore-and-cluster-health/SKILL.md)
   do not apply; rely on GKE audit logs routed to the landing zone's
   aggregated log sink instead.

## Best practices

- Enable Workload Identity Federation and Dataplane V2 at cluster
  creation (Phase 2/3) rather than retrofitting either onto a running
  cluster — both are far cheaper to get right the first time.
- Confirm Dataplane V2's built-in `NetworkPolicy` enforcement before
  installing any additional CNI/policy engine "just in case" — running
  Calico alongside an already-enforcing Dataplane V2 creates two
  competing dataplanes, not additional protection.
- Treat Phase 6 as a hard gate before Phase 7 — an unvalidated Shared VPC
  attachment or ingress path surfaces as a confusing application bug
  instead of a clean pre-handoff finding if skipped.
- Rehearse this sequence in a non-production project first, specifically
  to validate the Shared VPC subnet attachment and Workload Identity pool
  binding before committing a production cluster to either.
- Keep the whole sequence as versioned IaC (Terraform, Helm values,
  cert-manager manifests) in one repository per cluster.

## Common pitfalls

- **Symptom:** cert-manager's `Certificate` in Phase 5 never leaves
  `Pending`, with the `Challenge` object reporting a permission-denied
  error against Cloud DNS.
  **Fix:** This traces back to Phase 1/2: either the `roles/dns.admin`
  (or scoped custom role) binding on `cert-manager-dns01-gsa` is missing
  or too narrow for the specific managed zone, or the Workload Identity
  binding in Phase 5 references the wrong `<PROJECT_ID>.svc.id.goog`
  member string — the bracketed `[namespace/serviceaccount]` portion must
  match the ServiceAccount's actual namespace and name exactly.

- **Symptom:** A team installs Calico on a GKE cluster "to enable
  NetworkPolicy support" and pod networking becomes unstable or
  inconsistent shortly after.
  **Fix:** Recent GKE clusters already run Dataplane V2 (Cilium-based)
  with `NetworkPolicy` enforcement built in — installing a second CNI on
  top produces two competing dataplanes rather than added capability.
  Confirm via `kubectl get pods -n kube-system -l k8s-app=cilium` before
  Phase 3 concludes that a second CNI is even necessary; it almost always
  isn't on a current GKE cluster.

- **Symptom:** A workload's Workload Identity binding in Phase 7 works
  for one namespace's ServiceAccount but an identically-named
  ServiceAccount in a second namespace doesn't get the same access.
  **Fix:** The `--member` string in
  `gcloud iam service-accounts add-iam-policy-binding` is scoped to an
  exact `[namespace/serviceaccount]` pair — copying a Deployment to a new
  namespace without creating and binding a matching GCP service account
  member for that namespace leaves it with no federated identity at all.

- **Symptom:** The cluster is declared "production ready" and handed off
  the same day Phase 2 completes, skipping Phase 6 — and a Shared VPC
  routing or `NetworkPolicy` gap surfaces days later under real traffic.
  **Fix:** Treat Phase 6 as a required gate, not optional — see
  [kubernetes-cluster-post-provision-conformance-validation](../kubernetes-cluster-post-provision-conformance-validation/SKILL.md)
  for exactly the checklist this catches before handoff.

## Worked example

**Scenario:** Deploy `payments-api` end-to-end on a new GKE cluster in a
freshly vended GCP project attached to an existing Shared VPC, with
ingress-nginx (for parity with an existing EKS cluster), Cloud DNS-01,
and a full validation gate before handoff.

```bash
# Phase 1 — service accounts planned up front
gcloud iam service-accounts create payments-api-gsa --project=prj-checkout-prod
gcloud iam service-accounts create cert-manager-dns01-gsa --project=prj-checkout-prod
gcloud projects add-iam-policy-binding prj-checkout-prod \
  --member="serviceAccount:cert-manager-dns01-gsa@prj-checkout-prod.iam.gserviceaccount.com" \
  --role="roles/dns.admin" --condition=None

# Phase 2 — cluster attached to Shared VPC, Workload Identity enabled at creation
gcloud container clusters create payments-prod \
  --release-channel regular --enable-private-nodes \
  --workload-pool=prj-checkout-prod.svc.id.goog \
  --network=projects/prj-net-host-prod/global/networks/shared-vpc \
  --subnetwork=projects/prj-net-host-prod/regions/us-central1/subnetworks/gke-prod
gcloud container clusters get-credentials payments-prod --region us-central1

# Phase 3 — Dataplane V2 already active; confirm, don't install Calico
kubectl get pods -n kube-system -l k8s-app=cilium

# Phase 4 — ingress-nginx via Helm
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx --create-namespace \
  --set controller.service.type=LoadBalancer
kubectl get svc -n ingress-nginx ingress-nginx-controller   # note EXTERNAL-IP
gcloud dns record-sets create payments.example.com. --type=A --ttl=300 \
  --zone=example-com --rrdatas=<EXTERNAL_IP>

# Phase 5 — cert-manager Workload Identity binding + Cloud DNS-01
gcloud iam service-accounts add-iam-policy-binding \
  cert-manager-dns01-gsa@prj-checkout-prod.iam.gserviceaccount.com \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:prj-checkout-prod.svc.id.goog[cert-manager/cert-manager]"
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace --version v1.15.1 --set crds.enabled=true
kubectl apply -f cloud-dns-staging-issuer.yaml   # validate, then swap to prod

# Phase 6 — validation gate
sonobuoy run --mode quick --wait && sonobuoy results "$(sonobuoy retrieve)"
sonobuoy run --mode certified-conformance --wait && sonobuoy results "$(sonobuoy retrieve)" --mode=report

# Phase 7 — Workload Identity binding + first workload
gcloud iam service-accounts add-iam-policy-binding \
  payments-api-gsa@prj-checkout-prod.iam.gserviceaccount.com \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:prj-checkout-prod.svc.id.goog[payments/payments-api]"
helm upgrade --install payments-api oci://ghcr.io/example/charts/payments-api \
  --version 2.3.0 --namespace payments --create-namespace --atomic --timeout 5m

# Phase 8 — health baseline
kubectl get nodes
kubectl get pdb -A
```

`curl -I https://payments.example.com` returns `HTTP/2 200` with a
Let's Encrypt production certificate, confirming the full sequence wired
together correctly across the Shared VPC boundary, and the node
maintenance runbook (Phase 8) is documented before the first planned
node pool upgrade.

## Cross-references

- [gcp-landing-zone-setup](../../../cloud/skills/gcp-landing-zone-setup/SKILL.md) — the folder/project/Shared VPC/guardrail layer this sequence assumes already exists.
- [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md) — least-privilege design for every service account binding created across Phases 1, 5, and 7.
- [managed-kubernetes-eks-aks-gke](../managed-kubernetes-eks-aks-gke/SKILL.md) — full detail for Phase 2's cluster/node pool/Workload Identity provisioning.
- [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md) — the Calico alternative referenced in Phase 3 for legacy/non-Dataplane-V2 clusters.
- [ingress-nginx-configuration](../ingress-nginx-configuration/SKILL.md) — full detail for the ingress-nginx path in Phase 4.
- [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md) — full detail for Phase 5's Issuer/Certificate setup.
- [kubernetes-cluster-post-provision-conformance-validation](../kubernetes-cluster-post-provision-conformance-validation/SKILL.md) — full detail for Phase 6's validation gate.
- [helm-chart-authoring](../helm-chart-authoring/SKILL.md) — full detail for Phase 7's chart packaging and release discipline.
- [kubernetes-node-maintenance-and-troubleshooting](../kubernetes-node-maintenance-and-troubleshooting/SKILL.md) — the ongoing operational baseline established in Phase 8.
- [etcd-backup-restore-and-cluster-health](../etcd-backup-restore-and-cluster-health/SKILL.md) — explains why its procedures do not apply to this managed control plane.
