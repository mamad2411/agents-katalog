---
name: complete-kubernetes-deployment-on-oke-oci-from-scratch
description: >
  Sequences a complete, end-to-end OKE (Oracle Container Engine for
  Kubernetes) deployment from a bare OCI tenancy to a production-ready
  cluster serving a first workload — OCI landing zone prerequisites
  (Compartments, Dynamic Groups), OKE Enhanced cluster and node pool
  provisioning, VCN-Native pod networking (with the Calico NetworkPolicy
  add-on noted), ingress (Native Ingress Controller vs. ingress-nginx),
  cert-manager with OCI DNS via a community webhook solver, conformance
  validation, a Helm-deployed workload, and a node/cluster health
  baseline. This is an integration/orchestration skill sequencing several
  existing tool-specific skills in the correct order and flagging the
  handoff points between them — it does not restate their internals. Use
  when a user asks to "deploy a Kubernetes cluster on OKE from scratch,"
  "set up OKE on OCI end to end," "build a production OKE cluster from a
  fresh OCI tenancy," or "give me the full sequence to go from nothing to
  a working OKE cluster."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# Complete Kubernetes Deployment on OKE (OCI) From Scratch

## Purpose

OKE is the least "drop-in familiar" of the three major hyperscaler managed
Kubernetes offerings covered elsewhere in this repository — it has no
account/subscription/project isolation boundary (everything lives in one
tenancy's Compartment hierarchy), its workload-identity federation
mechanism is newer and only available on the Enhanced cluster tier, and
cert-manager has no built-in OCI DNS-01 provider the way it does for
Route 53/Azure DNS/Cloud DNS. Getting these OCI-specific mechanics wrong —
choosing a Basic cluster then discovering workload identity isn't
available, or expecting a native cert-manager OCI DNS solver that doesn't
exist — produces a cluster that looks provisioned right up until a later
phase depends on a capability that was never actually available. This
skill is the OCI-specific end-to-end runbook: it sequences Compartment/
Identity Domain prerequisites, OKE provisioning, VCN-Native pod
networking, ingress, cert-manager via a webhook solver, conformance
validation, a first workload, and a health baseline into one ordered
path, cross-referencing the tool-specific skill that covers each phase's
depth.

## When to use

- Deploying a brand-new OKE cluster into an OCI tenancy for the first
  time, where the Compartment hierarchy already exists but has no
  Kubernetes workload yet.
- Auditing an existing OKE rollout for a skipped or out-of-order phase
  (e.g. a Basic-tier cluster that can't support the workload identity
  binding a later phase assumed, or a cluster handed off with no
  conformance validation).
- Rebuilding a reference OKE environment (a second region, a DR cluster)
  that should follow the same sequence as a known-good first cluster.
- Onboarding a team unfamiliar with how OKE's compartment/Dynamic Group/
  workload-identity model differs from AWS/Azure/GCP's equivalent
  mechanisms, and how the individual skills in this repository fit
  together for an OCI deployment specifically.

## Prerequisites & environment

- An OCI tenancy already governed by a real Compartment hierarchy
  (Security, Network, Workloads/Production, Sandbox) with IAM policies,
  Cloud Guard, and Security Zones applied — this skill does **not** cover
  compartment design; see
  [oci-landing-zone-setup](../../../cloud/skills/oci-landing-zone-setup/SKILL.md).
- IAM policy-writing rights (plain-language OCI policy grammar) to create
  Dynamic Groups and scope policies to the target leaf compartment — see
  [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md)
  for the least-privilege discipline that applies equally to OCI's
  `manage`/`use`/`read`/`inspect` verb hierarchy.
- An OCI DNS public zone already delegated for the domain cert-manager
  will issue certificates for, and (since cert-manager has no built-in
  OCI DNS-01 provider) a deployed community webhook solver for OCI DNS
  before Phase 5 begins.
- OCI CLI ≥ 3.40, `kubectl`, and `helm` ≥ 3.14 authenticated against the
  target tenancy/compartment.
- A non-production compartment to rehearse this sequence in first — the
  Basic vs. Enhanced cluster tier decision in Phase 2 cannot be changed
  on a running cluster, so validating it before a production build is
  worthwhile.

## Step-by-step guidance

This is the phase sequence. Each phase links to the skill that covers its
full depth; the text here covers only OKE-specific sequencing and
integration decisions.

1. **Phase 1 — OCI landing zone & Dynamic Group prerequisites.** Confirm
   the target leaf compartment (e.g. `Workloads:Production:checkout-prod`)
   exists with the correct delegated-admin policy (see
   [oci-landing-zone-setup](../../../cloud/skills/oci-landing-zone-setup/SKILL.md)).
   OKE-specific sequencing point: OCI's workload-identity mechanism (Phase
   5/7) is bound via **Dynamic Groups matching a workload identity
   principal**, not a static compartment-wide role — plan the Dynamic
   Group's matching rule now, even though it references cluster/namespace
   details that only become concrete in Phase 2:
   ```hcl
   resource "oci_identity_dynamic_group" "cert_manager_wi" {
     compartment_id = var.tenancy_ocid
     name           = "cert-manager-workload-identity"
     matching_rule  = "ALL {request.principal.type='workload', request.principal.cluster_id='<OKE_CLUSTER_OCID_PLACEHOLDER>', request.principal.namespace='cert-manager', request.principal.service_account='cert-manager'}"
   }
   ```
   The `cluster_id` placeholder is finalized once Phase 2's cluster OCID
   is known — track this as an explicit follow-up, not a step silently
   skipped.

2. **Phase 2 — Provision an Enhanced-tier OKE cluster and node pools.**
   OKE offers two cluster tiers, and this decision **cannot be changed
   after creation**: **Basic** (no extra control-plane cost, but no
   workload identity, no cluster autoscaler flexibility beyond simple
   pool sizing) vs. **Enhanced** (adds workload identity federation, more
   autoscaling options, and OKE virtual nodes) — Enhanced is required if
   Phase 5/7's workload identity is in scope at all:
   ```bash
   oci ce cluster create \
     --name payments-prod --compartment-id <CHECKOUT_PROD_COMPARTMENT_OCID> \
     --kubernetes-version v1.30.1 --type ENHANCED_CLUSTER \
     --vcn-id <VCN_OCID> --service-lb-subnet-ids '["<LB_SUBNET_OCID>"]'
   oci ce node-pool create \
     --cluster-id <CLUSTER_OCID> --compartment-id <CHECKOUT_PROD_COMPARTMENT_OCID> \
     --name general --node-shape VM.Standard.E5.Flex \
     --size 3 --node-subnet-ids '["<NODE_SUBNET_OCID>"]'
   ```
   Enhanced clusters expose an OIDC-style workload identity discovery
   endpoint automatically as part of cluster creation — unlike AKS/GKE,
   there is no separate `--enable-workload-identity` flag to remember;
   the tier choice itself is the gate.

3. **Phase 3 — CNI: VCN-Native pod networking, with Calico for policy
   enforcement.** OKE's modern default, **VCN-Native pod networking**,
   assigns pods real IPs from a dedicated pod subnet in the VCN (similar
   in spirit to EKS's VPC CNI or GKE's VPC-native mode) and is markedly
   simpler to operate than the legacy **Flannel overlay** mode (still
   available for compatibility, but with no direct VCN routing/firewall
   visibility into pod traffic). Critically, **neither VCN-Native nor
   Flannel-overlay mode enforces Kubernetes `NetworkPolicy` on its own** —
   unlike GKE's Dataplane V2, OKE requires installing Calico explicitly
   if `NetworkPolicy` enforcement is a stated requirement:
   ```bash
   kubectl get pods -n kube-system -l name=oci-vcn-ip-native-cni
   kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.28.0/manifests/tigera-operator.yaml
   ```
   See
   [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md)
   for the Calico installation and policy-enforcement detail; on OKE this
   is a common **addition on top of** VCN-Native networking, not a
   replacement for it, unlike the full CNI swap sometimes done on EKS.

4. **Phase 4 — Ingress: OCI Native Ingress Controller vs. ingress-nginx,
   and DNS wiring.** Decide deliberately:
   - **OCI Native Ingress Controller (NIC)** — provisions/manages an OCI
     Flexible Load Balancer directly from Ingress resources, OCI's
     closest analog to ALB/AGIC/GKE Ingress.
   - **ingress-nginx** behind a `Service` of `type: LoadBalancer`
     (provisions an OCI Flexible Load Balancer via the OCI Cloud
     Controller Manager) — see
     [ingress-nginx-configuration](../ingress-nginx-configuration/SKILL.md)
     for full install/annotation detail; preferred for parity with
     non-OCI clusters running the same ingress-nginx configuration.
   Once the controller has an external address, create the OCI DNS
   record pointing at it **before** Phase 5's DNS-01 challenge needs to
   resolve.

5. **Phase 5 — cert-manager with OCI DNS via a community webhook
   solver.** Install cert-manager per
   [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md),
   but note the OCI-specific gap that skill's built-in examples don't
   cover: **cert-manager ships no native OCI DNS-01 provider** (unlike
   Route 53, Azure DNS, and Cloud DNS, which are first-class solver
   types). DNS-01 against OCI DNS requires deploying a community
   `cert-manager-webhook-oci`-style webhook solver alongside cert-manager
   and referencing it as a `webhook` solver type:
   ```bash
   helm install cert-manager-webhook-oci oci-webhook/cert-manager-webhook-oci \
     --namespace cert-manager
   ```
   ```yaml
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
             webhook:
               groupName: acme.oci.example.com
               solverName: oci
               config:
                 ociZoneName: example.com
                 ociProfile: cert-manager-workload-identity
           selector: { dnsZones: ["example.com"] }
   ```
   Finalize the `cert-manager-workload-identity` Dynamic Group's
   `cluster_id` from Phase 1 now that the real OCID exists, and attach
   the policy scoping it to DNS management on the target zone only:
   ```
   Allow dynamic-group cert-manager-workload-identity to manage dns-zones in compartment Network where target.dns-zone.name = 'example.com'
   ```
   Validate against Let's Encrypt staging first, exactly as
   [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md)
   describes.

6. **Phase 6 — Conformance and smoke validation.** Run Sonobuoy quick
   mode, then full `certified-conformance`, then targeted smoke tests —
   see
   [kubernetes-cluster-post-provision-conformance-validation](../kubernetes-cluster-post-provision-conformance-validation/SKILL.md).
   For OKE specifically, if Calico was added in Phase 3 for `NetworkPolicy`
   enforcement, run an explicit positive/negative connectivity smoke test
   — this is not covered by generic conformance and is the single most
   likely OKE-specific gap to go unnoticed, given neither of OKE's two
   native CNI modes enforces policy without it. Also confirm the default
   OCI Block Volume CSI `StorageClass` provisions a PVC.

7. **Phase 7 — Deploy the first workload via Helm.** Package and install
   per
   [helm-chart-authoring](../helm-chart-authoring/SKILL.md), finalizing a
   second Dynamic Group for the workload's own OCI API access the same
   way Phase 5 finalized cert-manager's:
   ```
   Allow dynamic-group payments-api-workload-identity to read secret-bundles in compartment Security
   ```
   ```bash
   helm upgrade --install payments-api oci://ghcr.io/example/charts/payments-api \
     --version 2.3.0 --namespace payments --create-namespace --atomic --timeout 5m
   ```

8. **Phase 8 — Node/cluster health baseline.** Establish the ongoing
   operational baseline: node drain/cordon discipline and `NotReady`
   diagnosis via
   [kubernetes-node-maintenance-and-troubleshooting](../kubernetes-node-maintenance-and-troubleshooting/SKILL.md).
   **Note what does *not* apply here:** OKE's control plane and etcd are
   fully Oracle-managed for both Basic and Enhanced tiers — the
   procedures in
   [etcd-backup-restore-and-cluster-health](../etcd-backup-restore-and-cluster-health/SKILL.md)
   do not apply; rely on OCI Audit logs routed through the Service
   Connector Hub to the landing zone's central `Security` compartment
   bucket instead.

## Best practices

- Decide Basic vs. Enhanced cluster tier before Phase 2 runs, based on
  whether workload identity (Phases 5/7) is in scope at all — this is
  not a setting a running cluster can change, unlike AKS's/GKE's
  workload-identity flags which are more forgiving to enable after the
  fact in some configurations.
- Plan every Dynamic Group's matching rule in Phase 1, even with a
  placeholder `cluster_id`, so Phase 5/7 is "fill in the real OCID and
  attach the policy" rather than designing the Dynamic Group's structure
  under time pressure later.
- Install Calico deliberately alongside VCN-Native pod networking when
  `NetworkPolicy` enforcement is required — don't assume either OKE CNI
  mode enforces it natively the way GKE's Dataplane V2 does.
- Deploy and validate the OCI DNS webhook solver against Let's Encrypt
  staging well before Phase 5's production cutover — a community webhook
  solver has a different failure surface (the webhook pod itself, its own
  RBAC) than a first-class built-in cert-manager provider.
- Treat Phase 6 as a hard gate before Phase 7, with particular attention
  to the `NetworkPolicy` smoke test if Calico was added in Phase 3.

## Common pitfalls

- **Symptom:** Workload identity federation for cert-manager or the
  application in Phase 5/7 simply isn't available — no OIDC-style
  discovery endpoint, no Dynamic Group matching rule ever succeeds.
  **Fix:** The cluster was created as **Basic** tier in Phase 2, which
  does not support workload identity at all. This requires provisioning
  a new Enhanced-tier cluster; there is no live-cluster upgrade path from
  Basic to Enhanced. Confirm the tier decision in Phase 2 explicitly
  before any later phase assumes workload identity is available.

- **Symptom:** `NetworkPolicy` resources apply cleanly via `kubectl` but
  traffic that should be denied still gets through on an OKE cluster.
  **Fix:** Neither VCN-Native pod networking nor Flannel-overlay mode
  enforces `NetworkPolicy` by default on OKE — this is a common
  assumption carried over from GKE (where Dataplane V2 does enforce it
  out of the box). Confirm Calico (or another policy-enforcing CNI
  add-on) is actually installed per
  [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md)
  before treating a `NetworkPolicy` as active.

- **Symptom:** A `Certificate` resource in Phase 5 stays stuck `Pending`
  with no `Challenge` resource ever created, unlike the Route 53/Azure
  DNS/Cloud DNS pattern shown in
  [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md).
  **Fix:** cert-manager has no built-in OCI DNS-01 solver type — a
  `ClusterIssuer` referencing a `dns01.ociDNS`-style built-in field (which
  doesn't exist) silently fails to match any solver. Confirm the
  community webhook solver is deployed and the `ClusterIssuer` uses the
  `webhook` solver type with the webhook's own `groupName`/`solverName`,
  not a built-in provider key.

- **Symptom:** The cluster is declared "production ready" and handed off
  the same day Phase 2 completes, skipping Phase 6 — and a missing Calico
  install (Phase 3) surfaces as a security incident once a `NetworkPolicy`
  that was assumed to be enforced turns out never to have been.
  **Fix:** Treat Phase 6 as a required gate, not optional, with the OKE-
  specific `NetworkPolicy` smoke test explicitly included — see
  [kubernetes-cluster-post-provision-conformance-validation](../kubernetes-cluster-post-provision-conformance-validation/SKILL.md).

## Worked example

**Scenario:** Deploy `payments-api` end-to-end on a new Enhanced-tier OKE
cluster in the `Workloads:Production:checkout-prod` compartment, with
Calico for `NetworkPolicy` enforcement, ingress-nginx (for parity with an
existing EKS cluster), OCI DNS-01 via a webhook solver, and a full
validation gate before handoff.

```bash
# Phase 1 — Dynamic Group planned with a placeholder cluster_id
oci iam dynamic-group create --name cert-manager-workload-identity \
  --description "cert-manager OKE workload identity" \
  --matching-rule "ALL {request.principal.type='workload', request.principal.cluster_id='PLACEHOLDER', request.principal.namespace='cert-manager', request.principal.service_account='cert-manager'}" \
  --compartment-id <TENANCY_OCID>

# Phase 2 — Enhanced cluster + node pool
oci ce cluster create --name payments-prod \
  --compartment-id <CHECKOUT_PROD_COMPARTMENT_OCID> \
  --kubernetes-version v1.30.1 --type ENHANCED_CLUSTER \
  --vcn-id <VCN_OCID> --service-lb-subnet-ids '["<LB_SUBNET_OCID>"]'
oci ce node-pool create --cluster-id <CLUSTER_OCID> \
  --compartment-id <CHECKOUT_PROD_COMPARTMENT_OCID> --name general \
  --node-shape VM.Standard.E5.Flex --size 3 --node-subnet-ids '["<NODE_SUBNET_OCID>"]'

# Phase 3 — VCN-Native pod networking confirmed, Calico added for policy enforcement
kubectl get pods -n kube-system -l name=oci-vcn-ip-native-cni
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.28.0/manifests/tigera-operator.yaml

# Phase 4 — ingress-nginx via Helm
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx --create-namespace \
  --set controller.service.type=LoadBalancer
kubectl get svc -n ingress-nginx ingress-nginx-controller   # note EXTERNAL-IP, create OCI DNS A record

# Phase 5 — finalize Dynamic Group with real cluster OCID, deploy webhook solver
oci iam dynamic-group update --dynamic-group-id <DG_OCID> \
  --matching-rule "ALL {request.principal.type='workload', request.principal.cluster_id='<CLUSTER_OCID>', request.principal.namespace='cert-manager', request.principal.service_account='cert-manager'}"
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace --version v1.15.1 --set crds.enabled=true
helm install cert-manager-webhook-oci oci-webhook/cert-manager-webhook-oci --namespace cert-manager
kubectl apply -f oci-dns-staging-issuer.yaml   # validate, then swap to prod

# Phase 6 — validation gate, with an explicit NetworkPolicy smoke test
sonobuoy run --mode quick --wait && sonobuoy results "$(sonobuoy retrieve)"
sonobuoy run --mode certified-conformance --wait && sonobuoy results "$(sonobuoy retrieve)" --mode=report
kubectl apply -f netpol-default-deny.yaml -n payments
kubectl run probe --image=busybox:1.36 --rm -it --restart=Never -n payments -- \
  wget -qO- --timeout=2 payments-api:8080   # expect this to time out

# Phase 7 — Dynamic Group for the workload + first deployment
oci iam dynamic-group create --name payments-api-workload-identity \
  --matching-rule "ALL {request.principal.type='workload', request.principal.cluster_id='<CLUSTER_OCID>', request.principal.namespace='payments', request.principal.service_account='payments-api'}" \
  --compartment-id <TENANCY_OCID>
helm upgrade --install payments-api oci://ghcr.io/example/charts/payments-api \
  --version 2.3.0 --namespace payments --create-namespace --atomic --timeout 5m

# Phase 8 — health baseline
kubectl get nodes
kubectl get pdb -A
```

`curl -I https://payments.example.com` returns `HTTP/2 200` with a
Let's Encrypt production certificate, and the negative `NetworkPolicy`
probe in Phase 6 confirms Calico is genuinely enforcing default-deny —
closing the specific gap OKE's native CNI modes leave open on their own.

## Cross-references

- [oci-landing-zone-setup](../../../cloud/skills/oci-landing-zone-setup/SKILL.md) — the tenancy/Compartment/Identity Domain/guardrail layer this sequence assumes already exists.
- [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md) — least-privilege design for every Dynamic Group and policy statement created across Phases 1, 5, and 7.
- [managed-kubernetes-eks-aks-gke](../managed-kubernetes-eks-aks-gke/SKILL.md) — the analogous managed-Kubernetes workload-identity pattern (IRSA/Azure AD Workload Identity/Workload Identity Federation) this skill's OKE Dynamic Group binding parallels conceptually.
- [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md) — full detail for installing Calico alongside VCN-Native pod networking in Phase 3.
- [ingress-nginx-configuration](../ingress-nginx-configuration/SKILL.md) — full detail for the ingress-nginx path in Phase 4.
- [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md) — full detail for the general Issuer/Certificate mechanics extended here with the OCI webhook solver in Phase 5.
- [kubernetes-cluster-post-provision-conformance-validation](../kubernetes-cluster-post-provision-conformance-validation/SKILL.md) — full detail for Phase 6's validation gate.
- [helm-chart-authoring](../helm-chart-authoring/SKILL.md) — full detail for Phase 7's chart packaging and release discipline.
- [kubernetes-node-maintenance-and-troubleshooting](../kubernetes-node-maintenance-and-troubleshooting/SKILL.md) — the ongoing operational baseline established in Phase 8.
- [etcd-backup-restore-and-cluster-health](../etcd-backup-restore-and-cluster-health/SKILL.md) — explains why its procedures do not apply to this managed control plane.
