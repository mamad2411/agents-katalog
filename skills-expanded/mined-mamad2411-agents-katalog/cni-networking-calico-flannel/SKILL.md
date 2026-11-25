---
name: cni-networking-calico-flannel
description: >
  Guides choosing and installing a Kubernetes CNI plugin — Calico vs.
  Flannel — including NetworkPolicy enforcement capability differences,
  BGP vs. VXLAN/overlay data paths, and IP address management (IPAM)
  tradeoffs. Use when a user asks to "choose a CNI plugin for
  Kubernetes," "enable NetworkPolicy enforcement," "set up Calico with
  BGP peering," "install Flannel," "debug pod-to-pod connectivity
  across nodes," or "migrate from Flannel to Calico."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# CNI Networking: Calico vs. Flannel

## Purpose

The CNI plugin is what actually gives every pod an IP and moves packets
between nodes — everything above it (Services, Ingress, NetworkPolicy,
a service mesh's sidecar interception) depends on it working correctly.
Flannel and Calico are the two most common choices for self-managed
clusters, and they solve different problems: Flannel is a simple overlay
network with no built-in policy enforcement, while Calico adds
`NetworkPolicy` enforcement and, optionally, a non-overlay BGP data
path. Picking the wrong one for the requirement (e.g. Flannel when
`NetworkPolicy` isolation is actually needed) produces a cluster where
security policy is silently a no-op. This skill covers choosing between
them and installing/troubleshooting each.

## When to use

- Choosing a CNI for a new self-managed cluster (kubeadm, K3s without
  its default, on-prem bare metal).
- A `NetworkPolicy` resource is applied but pods can still reach each
  other across the denied path — diagnosing whether the CNI even
  enforces `NetworkPolicy`.
- Deciding between an overlay (VXLAN/IPIP) and a native-routed (BGP)
  data path for performance or firewall/ACL-visibility reasons.
- Planning IP address management (pod CIDR sizing, per-node block size)
  before cluster bring-up, since it's disruptive to change after pods
  are scheduled.
- Migrating an existing cluster from Flannel to Calico (or vice versa)
  to gain policy enforcement or simplify the network model.
- Debugging cross-node pod-to-pod connectivity failures that look like
  an application bug but are actually a CNI/routing issue.

## Prerequisites & environment

- Root/administrative access to install a DaemonSet cluster-wide and,
  for BGP mode, access to configure routing on the underlying network
  (or confirm full-mesh BGP works without physical network changes,
  which is the common case for a flat L2/L3 cluster network).
- Flannel ≥ 0.24 or Calico ≥ 3.27 (Calico's Helm chart / Tigera
  Operator is now the recommended install path over raw manifests for
  new installs; both projects move quickly enough that the exact
  manifest URLs and default backend are worth re-checking against the
  target Kubernetes version's compatibility matrix before install).
- Know your target Kubernetes CNI plugin conformance requirement — most
  managed Kubernetes distributions (EKS, AKS, GKE) ship their own
  default CNI (see
  [managed-kubernetes-eks-aks-gke](../managed-kubernetes-eks-aks-gke/SKILL.md))
  and this skill applies primarily to self-managed clusters, or to
  managed clusters that explicitly support swapping the CNI (e.g. EKS
  with the AWS VPC CNI replaced by Calico for policy enforcement).
- A cluster with no CNI plugin installed yet (a fresh `kubeadm init`
  leaves nodes `NotReady` until a CNI is applied) or an explicit,
  planned migration window if replacing an existing CNI on a live
  cluster.

## Step-by-step guidance

1. **Decide based on actual requirements, not familiarity**:
   - Choose **Flannel** for the simplest possible overlay network when
     `NetworkPolicy` enforcement is not required (or is handled by a
     separate policy engine) and operational simplicity is the priority
     — it has fewer moving parts and a smaller learning curve.
   - Choose **Calico** when `NetworkPolicy` enforcement is required
     (namespace isolation, default-deny postures, egress control), when
     a non-overlay BGP data path is wanted for performance or
     network-visibility reasons, or when advanced policy (Calico's own
     `GlobalNetworkPolicy`, tiered policy, host endpoint protection)
     is needed beyond what native Kubernetes `NetworkPolicy` supports.
   - Flannel has an experimental/limited policy story; **do not rely on
     Flannel alone if `NetworkPolicy` enforcement is a stated security
     requirement** — it typically requires pairing with a separate
     policy engine (e.g. Calico running in policy-only mode alongside
     Flannel's dataplane, a supported combination via Canal) rather than
     assuming plain Flannel enforces anything.

2. **Install Flannel** (VXLAN backend, the common default):
   ```bash
   kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml
   ```
   Confirm the pod CIDR passed to `kubeadm init --pod-network-cidr=...`
   matches Flannel's expected default (`10.244.0.0/16`) or override
   Flannel's `net-conf.json` ConfigMap to match your chosen CIDR —
   mismatches here leave nodes stuck `NotReady`.

3. **Install Calico** via the Tigera Operator (recommended over raw
   manifests for lifecycle management):
   ```bash
   kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.28.0/manifests/tigera-operator.yaml
   ```
   ```yaml
   # custom-resources.yaml
   apiVersion: operator.tigera.io/v1
   kind: Installation
   metadata:
     name: default
   spec:
     calicoNetwork:
       ipPools:
         - cidr: 192.168.0.0/16
           encapsulation: VXLANCrossSubnet   # overlay only across subnets, native routing within
   ```
   ```bash
   kubectl create -f custom-resources.yaml
   watch kubectl get tigerastatus
   ```

4. **Choose Calico's data path deliberately**:
   - `VXLAN`/`IPIP` (overlay): works across any L3 network without
     requiring BGP peering with physical routers; simplest to deploy on
     cloud VPCs or networks you don't control the routing on.
   - Native BGP (no encapsulation): lower per-packet overhead and pod
     IPs visible to the underlying network's routing/firewalling, but
     requires either full-mesh BGP between nodes (works out of the box
     on a flat L2 network) or peering with physical top-of-rack
     routers/route reflectors for larger/segmented networks — this is
     an infrastructure decision, not just a Kubernetes config change.
   - `VXLANCrossSubnet`/`IPIPCrossSubnet` hybrid: encapsulates only when
     crossing an L3 subnet boundary, giving native routing performance
     within a subnet and overlay compatibility across subnets — a
     reasonable default when unsure.

5. **Enforce NetworkPolicy** once Calico (or Canal) is installed:
   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: deny-all-ingress
     namespace: payments
   spec:
     podSelector: {}
     policyTypes: ["Ingress"]
   ```
   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: allow-from-frontend
     namespace: payments
   spec:
     podSelector: { matchLabels: { app: payments-api } }
     policyTypes: ["Ingress"]
     ingress:
       - from:
           - podSelector: { matchLabels: { app: frontend } }
         ports:
           - { protocol: TCP, port: 8080 }
   ```
   Apply default-deny before allow-rules in a namespace being locked
   down, and verify with a connectivity test from both an allowed and a
   denied source before considering the policy complete.

6. **For BGP mode, verify peering status**:
   ```bash
   calicoctl node status
   calicoctl get bgppeer
   ```
   A node showing peers in a non-`Established` state has broken pod
   routing to/from that node even though the node itself is `Ready`.

7. **Validate cross-node pod connectivity directly** when debugging,
   independent of any application-level assumption:
   ```bash
   kubectl run net-test --image=busybox:1.36 --rm -it --restart=Never -- \
     wget -qO- --timeout=2 <target-pod-ip>:<port>
   ```
   Combine with `kubectl get pods -o wide` to confirm which nodes the
   source/destination land on — same-node connectivity working while
   cross-node fails points squarely at the CNI's inter-node data path
   (VXLAN interface, BGP route, or a firewall blocking the
   encapsulation protocol/port between nodes).

## Best practices

- Decide the CNI, its data path mode, and the pod CIDR sizing *before*
  cluster bring-up — changing pod CIDR or switching CNIs on a live
  cluster with running workloads is disruptive and typically requires
  draining and re-joining nodes.
- Size the pod CIDR for real scale, not the pilot: a `/24` per node
  block only fits 254 pods; undershoot this and nodes silently stop
  being able to schedule new pods once the block is exhausted, well
  before hitting the node's actual pod-count limit.
- If a security requirement mandates `NetworkPolicy` enforcement,
  confirm the CNI actually implements the full `NetworkPolicy` API
  (Calico does; plain Flannel does not) rather than assuming any CNI
  plugin enforces policy resources it accepts without erroring.
- When choosing native BGP, confirm the underlying network (cloud VPC,
  on-prem switches) actually permits or is configured for the BGP
  sessions Calico needs — most public cloud VPCs do not support this
  without additional configuration (VPC route tables, cloud-specific
  peering), which is why overlay/cross-subnet modes are the common
  default in cloud environments.
- Keep the CNI's own components (`calico-node`, `flanneld`) monitored
  like any other critical system DaemonSet — a crash-looping CNI pod on
  one node silently breaks networking for every pod scheduled there
  afterward, often without an obvious top-level cluster alert.
- Test `NetworkPolicy` changes with both a positive (should connect) and
  negative (should be blocked) case — a policy that "does nothing" due
  to a selector typo looks identical to a correctly-applied allow-all
  policy until you test the deny path explicitly.

## Common pitfalls

- **Symptom:** `NetworkPolicy` resources apply without error, but
  traffic that should be denied still gets through.
  **Fix:** Confirm the CNI actually enforces `NetworkPolicy` — plain
  Flannel accepts the resource via the Kubernetes API (any CNI can, since
  the API server doesn't require a specific CNI to store the object) but
  does not enforce it without a paired policy engine. Check
  `kubectl get pods -n kube-system` for a policy-enforcing component
  (`calico-node`, `kube-router`) actually running; if absent, the
  `NetworkPolicy` is a no-op regardless of how correct it looks.

- **Symptom:** New nodes join the cluster and stay `NotReady`
  indefinitely with a CNI-related error in `kubectl describe node`.
  **Fix:** Usually a pod CIDR mismatch between what `kubeadm`/the
  cluster bootstrap configured and what the CNI's ConfigMap/IPPool
  expects, or the CNI DaemonSet pod failing to schedule on that node
  (check taints/tolerations). Confirm `--pod-network-cidr` (kubeadm) or
  the cluster provisioner's pod CIDR setting matches the CNI's
  configured pool exactly.

- **Symptom:** Pods on the same node can reach each other, but
  cross-node pod-to-pod traffic times out.
  **Fix:** The overlay's encapsulation traffic (VXLAN UDP/4789 for
  Flannel/Calico VXLAN mode, IP protocol 4 for IPIP) is being blocked
  by a host firewall, security group, or NACL between nodes — this is
  an infrastructure-firewall problem, not a Kubernetes-level
  misconfiguration, and is invisible to `kubectl` since the API server
  reports the node `Ready` regardless.

- **Symptom:** After switching Calico from overlay to native BGP mode
  (or vice versa) on an existing cluster, some pods lose connectivity
  intermittently for an extended period.
  **Fix:** Changing the data-path mode requires every node to converge
  on the new mode; a rolling, mixed-mode state where some nodes still
  expect encapsulated traffic and others expect native routing produces
  intermittent failures until all nodes finish converging. Treat this as
  a planned, monitored migration with a rollback plan, not a
  live config flip on a single-digit-minute change window.

- **Symptom:** BGP-mode Calico shows nodes `Ready` in Kubernetes but
  `calicoctl node status` shows peers stuck in `Active`/`Connect`
  (never `Established`).
  **Fix:** BGP session isn't forming — check that nothing between nodes
  blocks TCP/179, and that any router-reflector or peering
  configuration (for non-full-mesh topologies) matches on both sides.
  Kubernetes-level node readiness does not reflect BGP peering health at
  all.

## Worked example

**Scenario:** Bring up a new self-managed 3-node kubeadm cluster with
Calico in `VXLANCrossSubnet` mode, then lock down a namespace to
default-deny with an explicit allow rule.

```bash
kubeadm init --pod-network-cidr=192.168.0.0/16
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.28.0/manifests/tigera-operator.yaml
```

```yaml
# custom-resources.yaml
apiVersion: operator.tigera.io/v1
kind: Installation
metadata: { name: default }
spec:
  calicoNetwork:
    ipPools:
      - cidr: 192.168.0.0/16
        encapsulation: VXLANCrossSubnet
        natOutgoing: Enabled
```

```bash
kubectl create -f custom-resources.yaml
watch kubectl get tigerastatus
kubectl get nodes    # confirm all nodes reach Ready
```

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: default-deny, namespace: payments }
spec: { podSelector: {}, policyTypes: ["Ingress"] }
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: allow-frontend, namespace: payments }
spec:
  podSelector: { matchLabels: { app: payments-api } }
  policyTypes: ["Ingress"]
  ingress:
    - from: [{ podSelector: { matchLabels: { app: frontend } } }]
      ports: [{ protocol: TCP, port: 8080 }]
```

```bash
kubectl apply -f netpol.yaml
# negative test: should time out
kubectl run probe --image=busybox:1.36 --rm -it --restart=Never -n payments -- \
  wget -qO- --timeout=2 payments-api:8080
# positive test from an allowed pod: should succeed
kubectl exec -n payments deploy/frontend -- wget -qO- --timeout=2 payments-api:8080
```

The first probe (unlabeled pod) times out, confirming default-deny is
active; the second (from a `frontend`-labeled pod) succeeds, confirming
the allow rule and Calico's policy enforcement are both working as
intended.

## Cross-references

- [managed-kubernetes-eks-aks-gke](../managed-kubernetes-eks-aks-gke/SKILL.md) — CNI choices and constraints on managed clusters, where the default CNI is often fixed or cloud-specific.
- [service-mesh-istio](../service-mesh-istio/SKILL.md) — how mesh sidecar traffic interception layers on top of (and depends on) a working CNI data path.
