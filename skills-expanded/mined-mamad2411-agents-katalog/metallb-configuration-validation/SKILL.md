---
name: metallb-configuration-validation
description: >
  Validates a MetalLB installation's actual IP pool allocation and BGP
  peering health before relying on it in production — confirming pool
  exhaustion isn't imminent, address assignment matches expectation,
  BGPPeer sessions reach `Established` (not just `Active`/`Connect`),
  and end-to-end external reachability of allocated Service IPs. Use
  when a user asks to "validate my MetalLB setup," "why is a
  LoadBalancer Service unreachable even though it has an IP," "check if
  MetalLB BGP peering is actually working," or "confirm MetalLB IP pool
  capacity before production."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# MetalLB Configuration Validation

## Purpose

MetalLB reporting a `LoadBalancer` Service's `EXTERNAL-IP` as assigned
only means the controller successfully allocated an address from a
pool — it says nothing about whether that address is actually reachable
from outside the cluster, which depends on a second, independent layer
(ARP/NDP announcement in Layer2 mode, or an `Established` BGP session in
BGP mode) that can fail silently relative to the allocation itself. This
gap — "Kubernetes says it's assigned" vs. "the network actually routes
to it" — is the most common source of confusing MetalLB incidents, and
is structurally the same class of problem as trusting a `CephCluster`
CRD's `Ready` status over `ceph status` in
[rook-ceph-configuration-validation](../rook-ceph-configuration-validation/SKILL.md).
This skill covers the validation checks — pool capacity, BGP peer state,
and true external reachability — that should run before depending on a
MetalLB configuration built per
[metallb-bare-metal-load-balancer-configuration](../metallb-bare-metal-load-balancer-configuration/SKILL.md)
in production.

## When to use

- Before cutting production traffic over to a newly configured MetalLB
  `LoadBalancer` Service.
- A `LoadBalancer` Service shows an `EXTERNAL-IP` but is unreachable
  from clients outside the cluster.
- Confirming an `IPAddressPool` has enough headroom before onboarding
  more Services, to avoid a future allocation failure.
- Validating BGP peering health (not just that a `BGPPeer` resource
  exists) after initial setup or after any network-side router
  reconfiguration.
- Periodic health verification of an existing MetalLB deployment as
  part of an operational runbook, not only during an active incident.
- Diagnosing intermittent reachability (works from some clients/paths,
  not others) that suggests a partial rather than total failure.

## Prerequisites & environment

- A MetalLB deployment already configured per
  [metallb-bare-metal-load-balancer-configuration](../metallb-bare-metal-load-balancer-configuration/SKILL.md),
  with `kubectl` access to the `metallb-system` namespace.
- For BGP-mode validation: read access to the upstream router's BGP
  neighbor status (via its own CLI/API, or coordination with whoever
  manages it) — MetalLB's own view of peer state should be
  cross-checked against the router's view, not trusted alone, the same
  way a `CephCluster` CRD's status shouldn't be trusted alone in
  [rook-ceph-configuration-validation](../rook-ceph-configuration-validation/SKILL.md).
- Network access to test actual external reachability from outside the
  cluster's own nodes — validating only from inside the cluster network
  can miss a failure that only manifests from a genuinely external
  vantage point.
- `metallb` CLI or direct `kubectl` access to MetalLB CRDs
  (`IPAddressPool`, `BGPPeer`, `BGPAdvertisement`,
  `L2Advertisement`) and the speaker pods' logs.

## Step-by-step guidance

1. **Check pool allocation state before it becomes a blocker** — don't
   wait for a Service to fail to get an IP to notice a pool is nearly
   exhausted:
   ```bash
   kubectl -n metallb-system get ipaddresspools -o yaml
   kubectl get svc -A -o jsonpath='{range .items[?(@.spec.type=="LoadBalancer")]}{.metadata.namespace}/{.metadata.name}: {.status.loadBalancer.ip}{"\n"}{end}'
   ```
   Compare the pool's configured range size against the count of
   currently-allocated Services; if headroom is within a handful of
   addresses of the pool's total capacity, treat that as an action item
   (expand the pool, or move some Services to another pool) before it
   blocks a future rollout.

2. **Confirm every `LoadBalancer` Service actually has a real, non-empty
   `EXTERNAL-IP`**, not just a status field that looks populated:
   ```bash
   kubectl get svc -A -o wide | grep LoadBalancer
   ```
   A Service stuck showing `<pending>` after a reasonable time (more
   than a few seconds past creation) means allocation itself failed —
   check the `metallb-controller` pod logs for the specific reason
   (pool exhausted, no pool matches the Service's
   `metallb.io/address-pool` annotation, `autoAssign: false` on every
   candidate pool with no explicit pool referenced):
   ```bash
   kubectl -n metallb-system logs -l app=metallb,component=controller --tail=100
   ```

3. **For Layer2 mode, confirm which node is currently announcing each
   service IP**, and that it's a genuinely healthy node:
   ```bash
   kubectl -n metallb-system logs -l app=metallb,component=speaker --tail=200 | grep <service-ip>
   ```
   MetalLB's speaker logs identify which node currently holds the
   "leader" role for each address; cross-check that node is `Ready` and
   not under memory/CPU pressure — an address being announced from an
   unhealthy node is a leading indicator of an impending, harder-to-
   diagnose outage when that node eventually fails completely.

4. **For BGP mode, check MetalLB's own view of peer state first, but
   don't stop there**:
   ```bash
   kubectl -n metallb-system logs -l app=metallb,component=speaker --tail=200 | grep -i bgp
   ```
   Recent MetalLB versions expose peer session state directly; a peer
   stuck anywhere other than `Established` (`Active`, `Connect`,
   `OpenSent`, `OpenConfirm`) means the session never actually formed,
   and every IP MetalLB "assigned" for that peer is unreachable from
   the network side despite Kubernetes reporting the Service as having
   an `EXTERNAL-IP`.

5. **Cross-check against the router's own BGP neighbor table** — this
   is the step most teams skip, and the one that actually confirms
   reachability rather than just MetalLB's self-reported state:
   ```
   # On the router (syntax varies by vendor)
   show bgp neighbors 10.0.0.1
   ```
   Confirm the neighbor state is `Established` on the router's side
   too, and that routes for the MetalLB-advertised prefixes
   (`aggregationLength: 32` means individual `/32` routes per Service
   IP) are actually present in the router's routing table
   (`show ip route 10.0.100.20`) — a session that's `Established` on
   MetalLB's side but where the router hasn't installed the
   corresponding route is still a broken path.

6. **Validate true end-to-end external reachability**, from a vantage
   point genuinely outside the cluster's own node network, not just
   from another pod or another cluster node:
   ```bash
   curl -sS -o /dev/null -w '%{http_code}\n' --max-time 5 https://<external-ip>:<port>/healthz
   ```
   Run this from a client machine on a different subnet/VLAN than the
   cluster nodes when possible — a reachability test run from inside
   the same L2 segment as the cluster can succeed even when a routing
   or BGP misconfiguration would prevent access from anywhere else.

7. **Simulate a node failure in a non-production validation exercise**
   to confirm failover actually works before trusting it in an
   incident:
   ```bash
   kubectl cordon <node-currently-announcing-ip>
   # for a real test: power off or kubectl drain --delete-emptydir-data --force the node in a staging cluster
   ```
   For Layer2 mode, confirm a different node picks up the
   announcement within an acceptable time window (watch the speaker
   logs); for BGP mode, confirm the router's ECMP/failover reroutes
   traffic to a surviving node's advertised path. Never perform this
   test by powering off a node in a live production cluster without an
   explicit, planned maintenance window.

8. **Re-run pool/peering checks after any change to the underlying
   network** (a router firmware upgrade, a VLAN change, a new switch
   in the path) — MetalLB's configuration itself may be unchanged while
   the network beneath it silently stops cooperating, and only a
   validation pass (not just "no one changed the MetalLB YAML")
   catches that.

## Best practices

- Validate reachability from a genuinely external vantage point, not
  just from inside the cluster's own network — the two can disagree
  in exactly the failure modes (BGP route not installed, VLAN
  misconfiguration) that matter most.
- Cross-check BGP peer state on both sides (MetalLB and the router),
  not MetalLB's self-reported state alone — a session state
  disagreement between the two sides is itself a diagnostic signal.
- Track pool utilization as a capacity metric over time, the same way
  you'd track any other finite resource pool, rather than discovering
  exhaustion only when the next Service creation fails.
- Practice a node-failure/failover drill in a non-production
  environment on a recurring basis, mirroring the etcd/Ceph
  restore-drill discipline in
  [etcd-backup-restore-and-cluster-health](../etcd-backup-restore-and-cluster-health/SKILL.md)
  and
  [rook-ceph-configuration-validation](../rook-ceph-configuration-validation/SKILL.md).
- Wire pool-utilization and BGP-peer-state checks into
  [prometheus-and-grafana-monitoring-stack](../../../observability-and-platform-extras/skills/prometheus-and-grafana-monitoring-stack/SKILL.md)
  (MetalLB exposes Prometheus metrics for both) so degradation is
  caught by alerting, not by a customer reporting an outage.
- Coordinate any BGP peering validation or test with whoever owns the
  physical network — checking neighbor state on a router you don't own
  without informing its owner can look like unexpected/unauthorized
  probing.

## Common pitfalls

- **Symptom:** `kubectl get svc` shows a real `EXTERNAL-IP`, but the
  Service is unreachable from outside the cluster.
  **Fix:** An allocated IP is not the same as a reachable one — check
  Layer2 speaker logs for which node (if any) is actually announcing
  that address, or BGP peer state for `Established` vs. stuck in an
  earlier negotiation phase. Kubernetes-level Service status reflects
  successful allocation from the pool, not network-level reachability.

- **Symptom:** A new Service fails to get any `EXTERNAL-IP` at all,
  staying `<pending>` indefinitely, even though existing Services
  using the same pool work fine.
  **Fix:** Check pool utilization (step 1) — the pool is very likely
  exhausted, and MetalLB has no fallback behavior beyond leaving the
  Service unassigned. Expand the pool's address range or free up
  addresses from decommissioned Services rather than assuming a
  MetalLB bug.

- **Symptom:** A `BGPPeer` resource exists and MetalLB's logs show no
  errors, but the router's neighbor table never shows the session
  established.
  **Fix:** Check for an ASN or peer-address mismatch between the
  `BGPPeer` CRD's `myASN`/`peerASN`/`peerAddress` and what's actually
  configured on the router — this is the single most common BGP
  peering failure, and it's invisible from the Kubernetes side alone
  since MetalLB may just show the session stuck in an early state
  without a descriptive error pointing at "your ASN doesn't match."

- **Symptom:** Reachability works fine from a test machine on the same
  subnet as the cluster nodes, but fails from a genuinely external
  client (a different VLAN, or over the internet through an edge
  router).
  **Fix:** The earlier test wasn't actually exercising the network path
  that matters — a same-subnet test can succeed via ARP/local routing
  even when the BGP-advertised route (or a firewall rule along the real
  external path) is broken. Always include at least one test from a
  vantage point outside the cluster's local L2 segment before declaring
  a Service production-ready.

- **Symptom:** Someone runs a node-failure test by hard-powering-off a
  production node "just to check failover," causing a real, unplanned
  outage for Services whose only healthy replica/announcement was on
  that node.
  **Fix:** This is a destructive validation action performed against
  the wrong environment — failover/failure-injection tests belong in a
  staging/non-production cluster with a planned maintenance window and
  stakeholder notice, following the same discipline as chaos-engineering
  practice in
  [chaos-engineering-and-resilience-testing](../../../site-reliability-engineering/skills/chaos-engineering-and-resilience-testing/SKILL.md),
  not as an ad hoc test against production.

## Worked example

**Scenario:** `payments-api`'s `LoadBalancer` Service (configured per
[metallb-bare-metal-load-balancer-configuration](../metallb-bare-metal-load-balancer-configuration/SKILL.md)'s
worked example) shows `EXTERNAL-IP: 10.0.0.210`, but a customer reports
intermittent timeouts reaching it.

1. Confirm the Service's own status looks fine (allocation succeeded):
   ```bash
   kubectl get svc payments-api -n payments
   # EXTERNAL-IP: 10.0.0.210   PORT(S): 443:31820/TCP
   ```

2. Check which node is currently announcing that IP in Layer2 mode:
   ```bash
   kubectl -n metallb-system logs -l app=metallb,component=speaker --tail=500 | grep 10.0.0.210
   ```
   Shows `worker-2` announcing the address. Check `worker-2`'s health:
   ```bash
   kubectl describe node worker-2 | grep -A5 Conditions
   ```
   `MemoryPressure: True` — the node is under memory pressure, which
   can cause the speaker pod itself to be slow to respond to ARP
   requests or occasionally get OOM-adjacent scheduling delays,
   producing exactly the intermittent (not total) timeout pattern
   reported.

3. Validate from a genuinely external vantage point to confirm the
   scope of impact:
   ```bash
   curl -sS -o /dev/null -w '%{http_code} %{time_total}\n' --max-time 5 https://10.0.0.210/healthz
   ```
   Run repeatedly over a few minutes — intermittent failures/timeouts
   correlate with the memory-pressure windows on `worker-2`.

4. Remediate the underlying node pressure (reschedule workloads,
   investigate the memory-hungry pod) rather than treating this as a
   MetalLB configuration problem — MetalLB itself is configured
   correctly; the node it happened to be announcing from was
   unhealthy. Confirm resolution by re-running the external curl test
   and checking `worker-2`'s conditions return to normal.

## Cross-references

- [metallb-bare-metal-load-balancer-configuration](../metallb-bare-metal-load-balancer-configuration/SKILL.md) — the configuration (IP pools, Layer2/BGP mode, peering) this skill validates.
- [rook-ceph-configuration-validation](../rook-ceph-configuration-validation/SKILL.md) — the same "CRD status vs. actual system health" validation pattern applied to storage instead of networking.
- [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md) — a structurally similar BGP-session validation workflow (`calicoctl node status`), for pod-network BGP rather than MetalLB's service-IP BGP.
- [prometheus-and-grafana-monitoring-stack](../../../observability-and-platform-extras/skills/prometheus-and-grafana-monitoring-stack/SKILL.md) — continuous alerting on MetalLB's pool-utilization and peer-state metrics.
- [chaos-engineering-and-resilience-testing](../../../site-reliability-engineering/skills/chaos-engineering-and-resilience-testing/SKILL.md) — the disciplined approach to failure-injection testing referenced in the node-failure drill above.
