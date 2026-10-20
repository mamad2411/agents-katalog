---
name: complete-kubernetes-deployment-on-prem-with-kubeadm-from-scratch
description: >
  Sequences a complete, end-to-end self-managed on-prem Kubernetes
  deployment from bare-metal hosts to a production-ready HA cluster
  serving a first workload — physical/network prerequisites, kubeadm
  init/join HA control plane with kube-vip, CNI (Calico/Flannel), MetalLB
  for LoadBalancer Services (bare metal has no cloud load balancer),
  ingress-nginx, cert-manager with a self-hosted internal CA or ACME,
  conformance validation, etcd backup setup, and a Helm-deployed first
  workload. This is an integration/orchestration skill that sequences
  several existing tool-specific skills in the correct order and flags
  the handoff points between them — it does not restate their internals.
  Use when a user asks to "deploy Kubernetes on-prem from scratch,"
  "build a bare-metal Kubernetes cluster end to end with kubeadm," "set
  up a self-managed HA cluster on our own hardware," "get LoadBalancer
  Services working on bare metal," or "give me the full sequence to go
  from bare servers to a working self-managed Kubernetes cluster."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# Complete Kubernetes Deployment On-Prem With kubeadm From Scratch

## Purpose

A self-managed on-prem cluster has no cloud provider underneath it doing
any of the work every cloud-managed skill in this family takes for
granted — no managed control plane, no automatic CNI, no cloud
LoadBalancer, and no publicly-trusted DNS-01 path unless one is
deliberately built. Every piece that a managed-Kubernetes deployment gets
"for free" (a healthy etcd, a working `Service` of `type: LoadBalancer`,
TLS certs from a well-known CA) has to be assembled explicitly here, in a
specific order, by the team operating the hardware. Getting the order
wrong most often looks like: bringing up a control plane with no CNI (so
every node sits `NotReady` and everything after that looks broken for the
wrong reason), or standing up MetalLB and ingress-nginx before the
control-plane VIP and etcd topology are actually settled, so a later
control-plane change disrupts already-configured networking. This skill
sequences the physical/network prerequisites, kubeadm HA bootstrap,
MetalLB, CNI, ingress, cert-manager, conformance validation, etcd backup,
and a first workload into one ordered path for bare-metal/on-prem
specifically.

## When to use

- Bootstrapping a brand-new self-managed Kubernetes cluster on physical
  or on-prem virtualized hardware, from racked-and-cabled servers to a
  production-ready cluster.
- Auditing an existing on-prem kubeadm deployment for a skipped or
  out-of-order phase (e.g. MetalLB configured before the control-plane
  VIP was stable, or a cluster running for months with no etcd backup
  ever taken).
- Rebuilding a reference on-prem cluster (a second site, a DR cluster)
  that should follow the same sequence as a known-good first cluster.
- Deciding, deliberately, the bare-metal-specific answers to problems a
  cloud-managed cluster would otherwise solve automatically: which CNI,
  how `LoadBalancer` Services get a real address, and where TLS trust
  comes from.

## Prerequisites & environment

- Racked, cabled, power/cooling-provisioned hosts with an isolated
  out-of-band management network reachable via Redfish/IPMI, and a
  reconciled DCIM/IPAM inventory — this skill does **not** cover physical
  facility or inventory setup; see
  [on-prem-infrastructure-patterns](../../../cloud/skills/on-prem-infrastructure-patterns/SKILL.md).
- A container runtime (containerd) already installed on every host — see
  [container-runtime-docker-containerd](../container-runtime-docker-containerd/SKILL.md).
- Matching `kubeadm`/`kubelet`/`kubectl` minor versions across every node,
  swap disabled, and the kernel/sysctl preflight requirements satisfied
  on every host.
- A stable control-plane endpoint address reachable **before**
  `kubeadm init` ever runs — either an existing hardware load balancer,
  or `kube-vip` run as a static pod (no external LB appliance required).
  This decision cannot be deferred: `--control-plane-endpoint` must point
  at it from the very first node.
- A dedicated, DHCP-excluded IP range for MetalLB, reserved with whoever
  manages the network segment, decided before Phase 4 (not discovered by
  trial and error once Services start conflicting with DHCP-assigned
  addresses).
- A plan for where TLS trust comes from: an existing internal CA's
  signing key/cert, or genuine internet reachability for public ACME —
  decide this before Phase 6, since it changes what credentials/network
  paths must exist.
- `helm` ≥ 3.14 and `kubectl` on an administrative workstation with
  access to the control-plane endpoint once it exists.

## Step-by-step guidance

This is the phase sequence. Each phase links to the skill that covers its
full depth; the text here covers only on-prem/bare-metal-specific
sequencing and integration decisions.

1. **Phase 1 — Physical/network prerequisites and IP planning.** Confirm
   inventory-as-code, out-of-band management isolation, and the
   virtualization/bare-metal provisioning pipeline are in place per
   [on-prem-infrastructure-patterns](../../../cloud/skills/on-prem-infrastructure-patterns/SKILL.md).
   Reserve, in one place, every IP range this deployment will need:
   the pod CIDR (Phase 3), the control-plane VIP (Phase 2), and the
   MetalLB pool (Phase 4) — deciding these together now avoids a CIDR
   collision discovered mid-bootstrap.

2. **Phase 2 — kubeadm HA control plane with kube-vip.** Follow
   [kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api](../kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api/SKILL.md)
   for the full `kubeadm init`/`join`/`kube-vip` bootstrap detail. The
   on-prem-specific sequencing point: `kube-vip` (or an equivalent
   hardware LB) must be reachable at the address passed to
   `--control-plane-endpoint` **before** the first `kubeadm init` runs —
   this is the one on-prem decision with no cheap way to change later,
   since every node's certificates are issued against that endpoint from
   the start:
   ```yaml
   # kubeadm-config.yaml
   apiVersion: kubeadm.k8s.io/v1beta4
   kind: ClusterConfiguration
   kubernetesVersion: v1.30.4
   controlPlaneEndpoint: "10.0.0.100:6443"
   networking: { podSubnet: "192.168.0.0/16" }
   ```
   ```bash
   kubeadm init --config kubeadm-config.yaml --upload-certs
   ```

3. **Phase 3 — CNI: Calico or Flannel, no cloud default to fall back
   on.** Unlike every managed-Kubernetes skill in this family (which
   ship a CNI already running) and unlike K3s (which bundles Flannel),
   a fresh kubeadm cluster leaves every node `NotReady` until a CNI is
   explicitly applied — there is no default here at all:
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.28.0/manifests/tigera-operator.yaml
   kubectl apply -f custom-resources.yaml   # ipPools.cidr must match podSubnet from Phase 2 exactly
   ```
   Choose Calico when `NetworkPolicy` enforcement is required (the common
   case for on-prem clusters subject to the same security expectations as
   any cloud cluster) or Flannel for the simplest possible overlay when
   it isn't — see
   [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md)
   for the full tradeoff, including the BGP-vs-overlay data-path decision
   this on-prem network (unlike most cloud VPCs) may actually be able to
   support natively.

4. **Phase 4 — MetalLB for `LoadBalancer` Services.** This is the phase
   with no equivalent at all in the cloud-managed skills in this family:
   bare metal has no cloud API to allocate a real load balancer, so
   every `Service` of `type: LoadBalancer` sits `EXTERNAL-IP: <pending>`
   forever without something to satisfy that request. See
   [metallb-bare-metal-load-balancer-configuration](../metallb-bare-metal-load-balancer-configuration/SKILL.md)
   for the full Layer2-vs-BGP decision and IP pool setup:
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.8/config/manifests/metallb-native.yaml
   kubectl apply -f metallb-ipaddresspool-and-l2advertisement.yaml
   ```
   Use the IP range reserved in Phase 1 — a range still handed out by
   DHCP elsewhere on the same segment produces intermittent, confusing
   address conflicts that look like a Kubernetes bug rather than an IPAM
   coordination gap.

5. **Phase 5 — ingress-nginx, exposed via the MetalLB-provisioned
   address.** Install per
   [ingress-nginx-configuration](../ingress-nginx-configuration/SKILL.md),
   with `controller.service.type=LoadBalancer` now meaningful because
   Phase 4 gave MetalLB something to allocate from:
   ```bash
   helm install ingress-nginx ingress-nginx/ingress-nginx \
     --namespace ingress-nginx --create-namespace \
     --set controller.service.type=LoadBalancer
   kubectl get svc -n ingress-nginx ingress-nginx-controller   # confirm a real EXTERNAL-IP from the MetalLB pool
   ```
   Point internal DNS (or a hosts-file entry for a small lab deployment)
   at this address before Phase 6 needs it resolvable.

6. **Phase 6 — cert-manager with an internal CA or ACME, decided by
   actual reachability.** Install cert-manager per
   [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md).
   On-prem-specific decision, made explicitly rather than defaulted:
   - **Internal/private CA** — the common on-prem choice when services
     are internal-only and there's no reason to seek public trust; use
     cert-manager's `CA` Issuer type against an existing internal CA's
     signing key/cert, or bootstrap cert-manager's own self-signed root.
     Plan trust-bundle distribution to every client that must validate
     these certs (browsers, internal service callers) as part of this
     phase, not as a follow-up.
   - **Public ACME (Let's Encrypt)** — viable only if this on-prem site
     genuinely has inbound port 80 (HTTP-01) or an automatable public DNS
     provider (DNS-01) reachable from cert-manager; many on-prem
     deployments have neither, in which case forcing ACME here is not a
     configuration problem to keep debugging but a network reality to
     accept and switch away from.

7. **Phase 7 — Conformance validation and etcd backup setup together.**
   Run Sonobuoy quick mode, then full `certified-conformance`, then
   targeted smoke tests per
   [kubernetes-cluster-post-provision-conformance-validation](../kubernetes-cluster-post-provision-conformance-validation/SKILL.md),
   explicitly including a `NetworkPolicy` positive/negative test if
   Calico was chosen in Phase 3. **In parallel, and before this cluster
   is declared production-ready, stand up scheduled etcd snapshots** —
   unlike every managed-Kubernetes skill in this family, this cluster's
   etcd is entirely self-operated and has no provider-side safety net at
   all:
   ```bash
   ETCDCTL_API=3 etcdctl snapshot save /backup/etcd-snapshot-$(date +%Y%m%d%H%M%S).db \
     --endpoints=https://127.0.0.1:2379 \
     --cacert=/etc/kubernetes/pki/etcd/ca.crt \
     --cert=/etc/kubernetes/pki/etcd/healthcheck-client.crt \
     --key=/etc/kubernetes/pki/etcd/healthcheck-client.key
   ETCDCTL_API=3 etcdctl snapshot status /backup/etcd-snapshot-$(date +%Y%m%d%H%M%S).db -w table
   ```
   See
   [etcd-backup-restore-and-cluster-health](../etcd-backup-restore-and-cluster-health/SKILL.md)
   for automating this as a CronJob, shipping snapshots off-node, and the
   quorum-health monitoring that should run continuously from this point
   forward — treat a cluster with no verified etcd backup as not yet
   production-ready, regardless of how clean its conformance results are.

8. **Phase 8 — Deploy the first workload via Helm.** Package and install
   per
   [helm-chart-authoring](../helm-chart-authoring/SKILL.md):
   ```bash
   helm upgrade --install payments-api oci://ghcr.io/example/charts/payments-api \
     --version 2.3.0 --namespace payments --create-namespace --atomic --timeout 5m
   ```
   If this workload needs to call a public cloud provider's API (a
   hybrid architecture), design that credential path via the hybrid
   connectivity and federation guidance in
   [on-prem-infrastructure-patterns](../../../cloud/skills/on-prem-infrastructure-patterns/SKILL.md)
   rather than assuming any of the cloud-managed workload-identity
   mechanisms (IRSA, Azure AD Workload Identity, Workload Identity
   Federation) are automatically available — none of them apply to a
   self-managed on-prem cluster.

9. **Phase 9 — Node/cluster health baseline.** Establish node drain/
   cordon discipline and `NotReady` diagnosis, including the
   kubeadm-specific one-node-at-a-time upgrade sequence, via
   [kubernetes-node-maintenance-and-troubleshooting](../kubernetes-node-maintenance-and-troubleshooting/SKILL.md)
   and
   [kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api](../kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api/SKILL.md).
   Confirm the etcd quorum-monitoring from Phase 7 is genuinely running
   (not just configured once) as part of this ongoing baseline.

## Best practices

- Reserve every IP range (pod CIDR, control-plane VIP, MetalLB pool) in
  one pass during Phase 1 — discovering a collision mid-bootstrap is far
  more disruptive here than in a cloud VPC with its own IPAM tooling.
- Decide the control-plane endpoint/VIP mechanism before Phase 2's first
  `kubeadm init` — this is the one decision in this entire sequence with
  no cheap way to change afterward.
- Treat MetalLB (Phase 4) as a mandatory phase, not an optional add-on —
  every `LoadBalancer` Service depends on it, and skipping it silently
  leaves ingress-nginx (Phase 5) with no real external address.
- Never let Phase 7's conformance validation substitute for Phase 7's
  etcd backup setup, or vice versa — a cluster that passes conformance
  cleanly but has no verified etcd snapshot is not production-ready, and
  neither is one with backups but unvalidated networking/storage.
- Practice a full etcd restore in a non-production environment on a real
  schedule once Phase 7 is complete — a backup that's never been test-
  restored is unverified, exactly as
  [etcd-backup-restore-and-cluster-health](../etcd-backup-restore-and-cluster-health/SKILL.md)
  describes.
- Keep the whole sequence (kubeadm config, MetalLB pools, ingress-nginx
  values, cert-manager Issuers) as versioned IaC in one repository per
  cluster, mirroring the discipline
  [on-prem-infrastructure-patterns](../../../cloud/skills/on-prem-infrastructure-patterns/SKILL.md)
  recommends for the hardware layer beneath it.

## Common pitfalls

- **Symptom:** Every node sits `NotReady` right after Phase 2 completes,
  and Phase 4/5's MetalLB/ingress-nginx installs appear to silently do
  nothing.
  **Fix:** This is Phase 3 being skipped or misordered — a fresh kubeadm
  cluster has no CNI at all until one is explicitly applied, unlike every
  managed-Kubernetes skill in this family. Confirm Calico or Flannel is
  actually applied and its `ipPools`/CIDR matches `podSubnet` from Phase
  2 exactly before troubleshooting any later phase.

- **Symptom:** A `LoadBalancer` Service in Phase 5 stays
  `EXTERNAL-IP: <pending>` indefinitely even though the cluster and CNI
  both look healthy.
  **Fix:** Phase 4 (MetalLB) was skipped or its `IPAddressPool` is
  exhausted/misconfigured — bare metal has no cloud API to satisfy a
  `LoadBalancer` request on its own. Confirm MetalLB is installed with a
  valid, non-exhausted pool before assuming the ingress controller itself
  is broken.

- **Symptom:** cert-manager's `Certificate` in Phase 6 never issues, and
  debugging the ACME solver configuration goes nowhere for hours.
  **Fix:** Confirm the honest reachability assessment from Phase 6 was
  actually done — many on-prem sites have no inbound port 80 and no
  automatable public DNS provider, making ACME structurally unable to
  succeed regardless of configuration correctness. Switch to an internal
  CA `Issuer` instead of continuing to debug a network path that cannot
  work as designed.

- **Symptom:** A production incident requires an etcd restore, and there
  is no snapshot to restore from — or the only snapshot that exists was
  never verified and turns out to be corrupt.
  **Fix:** Phase 7's etcd backup setup was treated as optional or
  deferred past the initial deployment. This is exactly the gap
  [etcd-backup-restore-and-cluster-health](../etcd-backup-restore-and-cluster-health/SKILL.md)
  exists to close — schedule snapshots, verify each one with
  `etcdctl snapshot status`, and ship them off-node as part of Phase 7,
  not as a task revisited only after an incident makes it urgent.

- **Symptom:** The control-plane VIP needs to move to a new address
  months after go-live (a network redesign, a rack migration), and doing
  so turns into a multi-day certificate-reissuance project.
  **Fix:** This traces back to Phase 2 — `controlPlaneEndpoint` was
  decided without enough foresight into future network changes.
  Re-issuing control-plane certificates for a new endpoint is
  substantially more disruptive than the up-front planning Phase 1/2
  are meant to force; treat this as confirmation that Phase 2's decision
  deserves real deliberation, not a placeholder value fixed later.

## Worked example

**Scenario:** Bootstrap a 3-node HA on-prem cluster on a flat L2 network
segment, with Calico for `NetworkPolicy` enforcement, MetalLB in Layer2
mode, ingress-nginx, an internal CA for TLS (no public internet
reachability at this site), full conformance validation, and etcd
snapshotting, before deploying `payments-api`.

```bash
# Phase 1 — IP ranges reserved together: pod CIDR 192.168.0.0/16, VIP 10.0.0.100, MetalLB 10.0.0.200-220

# Phase 2 — kube-vip-fronted HA control plane
cat > kubeadm-config.yaml <<'EOF'
apiVersion: kubeadm.k8s.io/v1beta4
kind: ClusterConfiguration
kubernetesVersion: v1.30.4
controlPlaneEndpoint: "10.0.0.100:6443"
networking: { podSubnet: "192.168.0.0/16" }
EOF
kubeadm init --config kubeadm-config.yaml --upload-certs   # node-1
# kube-vip static pod deployed on all 3 control-plane nodes
kubeadm join 10.0.0.100:6443 --token <TOKEN> --discovery-token-ca-cert-hash sha256:<HASH> \
  --control-plane --certificate-key <CERT_KEY>              # node-2, node-3

# Phase 3 — Calico, matching podSubnet
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.28.0/manifests/tigera-operator.yaml
kubectl create -f calico-custom-resources.yaml   # ipPools.cidr: 192.168.0.0/16
kubectl get nodes   # all Ready once Calico is up

# Phase 4 — MetalLB, Layer2 mode, using the reserved range
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.8/config/manifests/metallb-native.yaml
kubectl apply -f metallb-pool-10.0.0.200-220-l2.yaml

# Phase 5 — ingress-nginx exposed via MetalLB
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx --create-namespace \
  --set controller.service.type=LoadBalancer
kubectl get svc -n ingress-nginx ingress-nginx-controller   # EXTERNAL-IP from 10.0.0.200-220

# Phase 6 — internal CA (no public internet path at this site)
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace --version v1.15.1 --set crds.enabled=true
kubectl apply -f internal-ca-issuer.yaml

# Phase 7 — conformance + etcd backup together
sonobuoy run --mode quick --wait && sonobuoy results "$(sonobuoy retrieve)"
sonobuoy run --mode certified-conformance --wait && sonobuoy results "$(sonobuoy retrieve)" --mode=report
kubectl apply -f netpol-default-deny.yaml -n payments   # positive/negative Calico smoke test
ETCDCTL_API=3 etcdctl snapshot save /backup/etcd-baseline-$(date +%F).db \
  --endpoints=https://127.0.0.1:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/healthcheck-client.crt --key=/etc/kubernetes/pki/etcd/healthcheck-client.key
ETCDCTL_API=3 etcdctl snapshot status /backup/etcd-baseline-$(date +%F).db -w table

# Phase 8 — first workload
helm upgrade --install payments-api oci://ghcr.io/example/charts/payments-api \
  --version 2.3.0 --namespace payments --create-namespace --atomic --timeout 5m

# Phase 9 — health baseline
kubectl get pdb -A
```

`curl -I https://payments.internal.example.com` (validated against the
internal CA's trust bundle, distributed to internal clients as part of
Phase 6) returns `HTTP/2 200`, the etcd snapshot's `snapshot status`
reports a non-zero key count confirming a real, verified backup exists,
and the cluster is handed off with a documented node-maintenance and
etcd-restore runbook rather than an assumed-but-unverified one.

## Cross-references

- [on-prem-infrastructure-patterns](../../../cloud/skills/on-prem-infrastructure-patterns/SKILL.md) — the physical/network/inventory layer this sequence assumes already exists, and the hybrid-connectivity pattern for any workload needing cloud API access.
- [container-runtime-docker-containerd](../container-runtime-docker-containerd/SKILL.md) — installing/configuring the container runtime kubeadm requires on every node before Phase 2.
- [kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api](../kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api/SKILL.md) — full detail for Phase 2's kubeadm HA bootstrap and Phase 9's upgrade sequence.
- [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md) — full detail for Phase 3's CNI choice and installation.
- [metallb-bare-metal-load-balancer-configuration](../metallb-bare-metal-load-balancer-configuration/SKILL.md) — full detail for Phase 4's Layer2/BGP mode and IP pool setup.
- [ingress-nginx-configuration](../ingress-nginx-configuration/SKILL.md) — full detail for Phase 5's controller install and Ingress configuration.
- [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md) — full detail for Phase 6's internal-CA and ACME Issuer setup.
- [kubernetes-cluster-post-provision-conformance-validation](../kubernetes-cluster-post-provision-conformance-validation/SKILL.md) — full detail for Phase 7's validation gate.
- [etcd-backup-restore-and-cluster-health](../etcd-backup-restore-and-cluster-health/SKILL.md) — full detail for Phase 7's backup automation and the ongoing quorum-health monitoring in Phase 9.
- [helm-chart-authoring](../helm-chart-authoring/SKILL.md) — full detail for Phase 8's chart packaging and release discipline.
- [kubernetes-node-maintenance-and-troubleshooting](../kubernetes-node-maintenance-and-troubleshooting/SKILL.md) — the ongoing operational baseline established in Phase 9.
