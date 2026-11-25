---
name: metallb-bare-metal-load-balancer-configuration
description: >
  Configures MetalLB to provide working `Service` type `LoadBalancer`
  support on bare-metal/on-prem Kubernetes clusters that have no cloud
  provider to allocate real load balancers — IP address pools,
  Layer2 (ARP/NDP failover) mode, and BGP mode with peer configuration.
  Use when a user asks to "set up MetalLB," "get LoadBalancer Services
  working on bare metal," "configure a MetalLB IP address pool,"
  "choose Layer2 vs BGP mode for MetalLB," or "configure BGP peering for
  MetalLB."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# MetalLB Bare-Metal Load Balancer Configuration

## Purpose

A `Service` of `type: LoadBalancer` is meaningless on a cluster with no
cloud provider integration — without something to satisfy that request,
the Service sits with `EXTERNAL-IP: <pending>` forever. MetalLB fills
exactly that gap for bare-metal and on-prem clusters by implementing the
load-balancer API itself: it watches for `LoadBalancer` Services,
allocates an IP from a configured pool, and announces reachability to
that IP using one of two fundamentally different mechanisms — Layer2
mode (ARP/NDP, one node at a time, simple but limited failover speed and
no real load spreading) or BGP mode (each node advertises routes to
upstream routers, enabling real ECMP load spreading but requiring actual
BGP peering with the physical/virtual network). Choosing the wrong mode
for the network you actually have, or misconfiguring the IP pool, is the
most common way MetalLB looks "installed" but doesn't actually make
Services reachable. This skill covers configuring both modes and the IP
pool; verifying that allocation and peering are actually healthy before
depending on it in production is
[metallb-configuration-validation](../metallb-configuration-validation/SKILL.md)'s
job.

## When to use

- Standing up `LoadBalancer` Service support on a new bare-metal/on-prem
  Kubernetes cluster (kubeadm, K3s, Cluster API on bare metal) with no
  cloud load-balancer integration.
- Deciding between Layer2 and BGP mode for a specific network
  environment.
- Configuring IP address pools and which Services/namespaces can draw
  from which pool.
- Setting up BGP peering between cluster nodes and upstream
  top-of-rack/router infrastructure.
- Debugging a `LoadBalancer` Service stuck `<pending>` on a bare-metal
  cluster.
- Migrating a cluster from Layer2 to BGP mode (or the reverse) for
  better failover/load-spreading characteristics.

## Prerequisites & environment

- A Kubernetes cluster ≥ 1.26 with no existing cloud-provider
  `LoadBalancer` implementation already claiming that role (MetalLB
  and a cloud controller manager's LB integration conflict if both are
  active).
- MetalLB ≥ v0.14 installed via its manifest or Helm chart, with
  `strictARP` enabled on kube-proxy if running in IPVS mode (required
  for Layer2 mode to work correctly — see step 2).
- A block of IP addresses on the same L2 segment as the cluster nodes
  (Layer2 mode) reserved and **not** handed out by DHCP to anything
  else, or a BGP-speaking upstream router/switch fabric with an
  available ASN and peering configuration (BGP mode) — this is a
  network-infrastructure prerequisite, not something MetalLB itself can
  provide.
- For BGP mode specifically: coordination with whoever manages the
  physical network, since MetalLB's BGP speaker needs a peer
  relationship configured on both sides (MetalLB's `BGPPeer` CRD and
  the router's own BGP neighbor configuration).
- Familiarity with [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md)
  if also running Calico in BGP mode on the same cluster — Calico's pod
  networking BGP and MetalLB's service-IP BGP are separate BGP sessions
  serving different purposes, and can coexist but should be configured
  and reasoned about independently.

## Step-by-step guidance

1. **Install MetalLB**:
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.8/config/manifests/metallb-native.yaml
   kubectl -n metallb-system get pods   # controller + speaker DaemonSet, wait for Running
   ```

2. **If kube-proxy runs in IPVS mode, enable `strictARP`** before
   configuring Layer2 mode — without it, kube-proxy's own ARP handling
   conflicts with MetalLB's, and Services intermittently become
   unreachable:
   ```bash
   kubectl get configmap kube-proxy -n kube-system -o yaml | \
     sed -e 's/strictARP: false/strictARP: true/' | \
     kubectl apply -f - -n kube-system
   ```
   Not required for iptables-mode kube-proxy (the more common default),
   but always confirm which mode is actually running before skipping
   this step.

3. **Choose Layer2 or BGP mode based on the actual network**, not
   familiarity:
   - **Layer2** when nodes share a flat L2 segment and there's no BGP
     fabric available (the common case for smaller on-prem/homelab/
     simpler datacenter setups) — one node at a time answers ARP/NDP
     for each service IP; failover on node loss takes a few seconds
     (ARP cache expiry-dependent) and there's no real load spreading
     across nodes for a single Service IP.
   - **BGP** when upstream routers support BGP peering and either
     faster failover or genuine multi-node ECMP load spreading for a
     single Service IP is required — this is a real network design
     decision requiring the network team's involvement, not a
     Kubernetes-only configuration change.

4. **Configure an `IPAddressPool`** (works for both modes — this is
   what actually gets allocated to Services):
   ```yaml
   apiVersion: metallb.io/v1beta1
   kind: IPAddressPool
   metadata:
     name: production-pool
     namespace: metallb-system
   spec:
     addresses:
       - 10.0.100.10-10.0.100.50
     autoAssign: true
   ```
   Reserve a separate, non-overlapping pool per environment/purpose
   (e.g. a smaller `autoAssign: false` pool for Services that need a
   specific, manually-chosen IP) rather than one pool for everything —
   see step 7 for scoping pools to specific namespaces.

5. **Configure Layer2 advertisement**:
   ```yaml
   apiVersion: metallb.io/v1beta1
   kind: L2Advertisement
   metadata:
     name: production-l2
     namespace: metallb-system
   spec:
     ipAddressPools:
       - production-pool
   ```

6. **Configure BGP mode instead**, with explicit peer(s) matching the
   upstream router's actual configuration:
   ```yaml
   apiVersion: metallb.io/v1beta2
   kind: BGPPeer
   metadata:
     name: rack1-router
     namespace: metallb-system
   spec:
     myASN: 64512
     peerASN: 64500
     peerAddress: 10.0.0.1
     holdTime: "90s"
   ---
   apiVersion: metallb.io/v1beta1
   kind: BGPAdvertisement
   metadata:
     name: production-bgp
     namespace: metallb-system
   spec:
     ipAddressPools:
       - production-pool
     aggregationLength: 32
   ```
   `myASN`/`peerASN`/`peerAddress` must exactly match what's configured
   on the router's side — mismatches here are the most common cause of
   a `BGPPeer` never reaching `Established` (see
   [metallb-configuration-validation](../metallb-configuration-validation/SKILL.md)).

7. **Scope pools to specific namespaces/Services** when different
   teams or environments must not draw from each other's IP ranges:
   ```yaml
   apiVersion: metallb.io/v1beta1
   kind: IPAddressPool
   metadata:
     name: dev-pool
     namespace: metallb-system
   spec:
     addresses:
       - 10.0.100.60-10.0.100.70
     autoAssign: false
   ```
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: dev-app
     annotations:
       metallb.io/address-pool: dev-pool
   spec:
     type: LoadBalancer
   ```
   `autoAssign: false` on a pool means Services must explicitly opt in
   via the annotation, preventing accidental allocation from a
   restricted pool.

8. **Request a specific IP for a Service** when a stable, pre-registered
   address (e.g. already in DNS) is required, rather than accepting
   whatever the pool auto-assigns:
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: payments-api
     annotations:
       metallb.io/loadBalancerIPs: "10.0.100.20"
   spec:
     type: LoadBalancer
   ```

## Best practices

- Reserve the IP range given to MetalLB explicitly with whoever manages
  DHCP/IPAM for that network segment — an overlapping range handed out
  by both DHCP and MetalLB produces intermittent, very confusing IP
  conflicts that look like a Kubernetes bug.
- Default to Layer2 mode unless BGP's load-spreading or faster-failover
  benefits are actually needed and the network team can commit to
  maintaining the peering — BGP mode adds a real, ongoing
  cross-team dependency that Layer2 mode doesn't.
- Keep `aggregationLength: 32` (advertise each service IP individually)
  unless there's a specific reason to aggregate into larger CIDR
  blocks — aggregation trades route-table size for less precise
  per-service traffic engineering.
- Split pools by purpose/environment (`autoAssign: false` for anything
  needing a deliberately chosen IP) rather than one large pool where
  any Service could land on any address.
- Document the chosen mode and IP ranges alongside the cluster's
  broader network documentation (VLAN/subnet plan), not only in the
  MetalLB CRDs themselves — someone doing network planning six months
  later needs to know this range is claimed.
- Treat BGP peer configuration changes as a coordinated, two-sided
  change (MetalLB `BGPPeer` and the router's neighbor config) — one
  side changing without the other produces a session that silently
  never re-establishes.

## Common pitfalls

- **Symptom:** A `LoadBalancer` Service stays `EXTERNAL-IP: <pending>`
  indefinitely.
  **Fix:** Check that an `IPAddressPool` actually exists with
  `autoAssign: true` (or the Service references one explicitly via
  annotation) and that the pool isn't already exhausted
  (`kubectl -n metallb-system get ipaddresspools -o yaml` and compare
  addresses used vs. available) — a common cause is every address in
  the pool already allocated to existing Services, leaving nothing for
  a new one.

- **Symptom:** A Service gets an `EXTERNAL-IP` assigned, but it's
  unreachable from outside the cluster.
  **Fix:** In Layer2 mode, confirm `strictARP` is enabled if kube-proxy
  runs in IPVS mode (step 2) — without it, ARP responses for the
  service IP can be inconsistent. In BGP mode, confirm the `BGPPeer`
  session is actually `Established` (see
  [metallb-configuration-validation](../metallb-configuration-validation/SKILL.md))
  — an assigned IP with no working BGP session announces nothing to
  the upstream network, leaving the address unreachable despite
  Kubernetes reporting it as allocated.

- **Symptom:** Two Services end up with the same external IP, or a
  Service gets an IP that's also in use by something else on the
  network.
  **Fix:** The MetalLB pool overlaps with a range still handed out by
  DHCP or statically assigned elsewhere — reserve the pool's range
  explicitly and remove it from DHCP scope before assigning it to
  MetalLB, and audit existing static assignments on that subnet before
  the pool is put into production use.

- **Symptom:** Failover after a node failure in Layer2 mode takes much
  longer than expected (tens of seconds to minutes), causing visible
  client-side disruption.
  **Fix:** This is an inherent Layer2-mode limitation, not a
  misconfiguration — failover depends on ARP cache expiry on
  upstream switches/clients, which MetalLB can influence somewhat via
  gratuitous ARP but not eliminate. If faster failover is a hard
  requirement, this is a reason to move to BGP mode (ECMP reroutes
  faster) rather than tuning Layer2 mode further.

- **Symptom:** Someone deletes an `IPAddressPool` that still has
  Services actively using addresses from it, "to reconfigure the range."
  **Fix:** Deleting a pool still in use by live Services leaves those
  Services with an orphaned/unmanaged external IP and can disrupt
  traffic — check `kubectl get svc -A -o jsonpath='{range .items[?(@.spec.type=="LoadBalancer")]}{.metadata.namespace}/{.metadata.name}: {.status.loadBalancer.ip}{"\n"}{end}'`
  for current allocations from a pool before deleting or resizing it,
  and migrate/re-provision affected Services deliberately rather than
  deleting the pool out from under them.

## Worked example

**Scenario:** A 4-node on-prem cluster on a flat `10.0.0.0/24` L2
segment needs `LoadBalancer` Services to work, with no BGP-capable
router available, and a stable IP reserved in advance for a public-
facing `payments-api` Service that's already registered in DNS.

```bash
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.8/config/manifests/metallb-native.yaml
kubectl -n metallb-system get pods
```

Confirm kube-proxy mode and enable `strictARP` if IPVS:
```bash
kubectl get configmap kube-proxy -n kube-system -o jsonpath='{.data.config\.conf}' | grep mode
# mode: "ipvs"
kubectl get configmap kube-proxy -n kube-system -o yaml | \
  sed -e 's/strictARP: false/strictARP: true/' | kubectl apply -f - -n kube-system
```

```yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata: { name: production-pool, namespace: metallb-system }
spec:
  addresses: ["10.0.0.200-10.0.0.220"]
  autoAssign: true
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata: { name: production-l2, namespace: metallb-system }
spec:
  ipAddressPools: ["production-pool"]
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: payments-api
  namespace: payments
  annotations:
    metallb.io/loadBalancerIPs: "10.0.0.210"
spec:
  type: LoadBalancer
  selector: { app: payments-api }
  ports: [{ port: 443, targetPort: 8443 }]
```

`10.0.0.210` was chosen deliberately (already registered as
`payments-api.example.com` in DNS) and sits outside the `.200-.220`
`autoAssign` pool's typical auto-pick order but still within it, so it's
both explicitly pinned and validly drawn from the reserved range —
`kubectl get svc payments-api -n payments` confirms
`EXTERNAL-IP: 10.0.0.210` and the Service is reachable from outside the
cluster once ARP for that address resolves to the node currently
holding it.

## Cross-references

- [metallb-configuration-validation](../metallb-configuration-validation/SKILL.md) — validating IP pool allocation and BGP peering health before relying on this configuration in production.
- [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md) — Calico's separate BGP usage for pod networking, distinct from but potentially coexisting with MetalLB's BGP mode on the same cluster.
- [ingress-nginx-configuration](../ingress-nginx-configuration/SKILL.md) — commonly layered on top of a MetalLB-provided `LoadBalancer` IP to route HTTP(S) traffic to multiple Services.
- [on-prem-infrastructure-patterns](../../../cloud/skills/on-prem-infrastructure-patterns/SKILL.md) — broader on-prem network/infrastructure design this skill's IP pool and BGP peering decisions fit into.
