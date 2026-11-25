---
name: consul-service-mesh-and-discovery-configuration
description: >
  Configures HashiCorp Consul as a combined service mesh and service
  discovery layer, especially across multi-cloud or hybrid (VM +
  Kubernetes, multi-datacenter) environments where a Kubernetes-only
  mesh doesn't reach. Covers Consul Connect sidecar injection,
  intentions, config entries (service-splitter, service-resolver,
  service-router), and cluster peering / WAN federation for
  cross-datacenter service discovery. Use when a user asks to "set up
  Consul service mesh," "federate Consul across datacenters," "register
  a VM service with Consul alongside Kubernetes services," "configure
  Consul Connect sidecars," or "do service discovery across cloud
  providers."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: service-mesh-and-api-gateway
  maturity: stable
---

# Consul Service Mesh and Discovery Configuration

## Purpose

Consul solves a problem Kubernetes-native meshes (Istio, Linkerd) don't:
service discovery and mesh connectivity across environments that aren't
a single Kubernetes cluster — VMs, bare metal, multiple Kubernetes
clusters, and multiple cloud providers, all registered in one catalog
and reachable through one mesh. Its service discovery (DNS and HTTP API
over a distributed, Raft-backed catalog) predates and works
independently of its service-mesh (Connect) capability, which is why
Consul is often chosen specifically for hybrid/multi-cloud estates where
"just use the Kubernetes-native mesh" isn't an option because not
everything is in Kubernetes. This skill covers configuring Consul
Connect sidecars, intentions, traffic-management config entries, and
cross-datacenter connectivity. Validating service definitions and
intentions before they reach production is a separate, deeper topic —
see
[consul-configuration-validation](../consul-configuration-validation/SKILL.md).

## When to use

- Standing up Consul as the mesh and/or discovery layer for an estate
  that spans VMs and Kubernetes, or multiple Kubernetes clusters across
  cloud providers.
- Registering non-Kubernetes services (VM-hosted, bare-metal) into the
  same catalog and mesh as Kubernetes-hosted services.
- Writing or reviewing **intentions** that authorize (or deny)
  service-to-service mesh traffic.
- Configuring traffic splitting/routing across service versions with
  Consul's `service-splitter`/`service-router`/`service-resolver`
  config entries.
- Federating multiple Consul datacenters (WAN federation) or connecting
  independently-administered Consul clusters (cluster peering) for
  cross-datacenter or cross-cloud service discovery and mesh traffic.
- A user is choosing between Consul, Linkerd, Cilium, or Istio for a new
  mesh and the deciding factor is non-Kubernetes workloads or
  multi-datacenter reach.

## Prerequisites & environment

- A running Consul server cluster (odd number of servers, typically 3
  or 5, using the Raft consensus protocol) reachable by every agent that
  needs to register services or resolve the catalog.
- For Kubernetes workloads: the `consul-k8s` Helm chart installed with
  `connectInject.enabled=true`, which runs the sidecar-injection webhook
  and (per pod) an Envoy sidecar proxy — Consul Connect's data plane is
  Envoy, not a custom proxy, so Envoy version compatibility with your
  Consul server version matters when upgrading either.
- For VM/bare-metal workloads: the `consul` agent running locally on
  each host in client mode, registering local services via service
  definition files or the HTTP API.
- ACLs enabled (`acl.enabled = true`) with a bootstrap token rotated out
  of the initial bootstrap state — running a production Consul cluster
  with ACLs disabled means intentions have no enforcement teeth, since
  anything can register or call anything.
- For multi-datacenter: either WAN federation (requires routable network
  connectivity between all federated datacenters' server clusters, plus
  matching Gossip encryption keys) or cluster peering (Consul's newer
  mechanism that doesn't require federated servers to share a flat
  network, better suited to genuinely separate cloud environments).

## Step-by-step guidance

1. **Register services with health checks, not bare registration** — a
   service registered without a check is assumed healthy forever, which
   defeats the purpose of service discovery under real failure:
   ```json
   {
     "service": {
       "name": "payments-api",
       "port": 8080,
       "connect": { "sidecar_service": {} },
       "checks": [
         {
           "http": "http://localhost:8080/healthz",
           "interval": "10s",
           "timeout": "2s"
         }
       ]
     }
   }
   ```
   `"connect": {"sidecar_service": {}}` is what enrolls this service into
   the mesh with an auto-configured Envoy sidecar on a VM/bare-metal
   host; on Kubernetes this is handled instead by the `consul-k8s`
   inject webhook via a pod annotation
   (`consul.hashicorp.com/connect-inject: "true"`).

2. **Write intentions to explicitly allow required traffic** — Consul's
   mesh defaults to deny-by-default once intentions are in use, so every
   legitimate caller needs an explicit allow:
   ```hcl
   Kind = "service-intentions"
   Name = "payments-api"
   Sources = [
     {
       Name   = "checkout-service"
       Action = "allow"
     },
     {
       Name   = "*"
       Action = "deny"
     }
   ]
   ```
   Apply via `consul config write payments-api-intentions.hcl`, or as a
   Kubernetes CRD (`ServiceIntentions`) if using `consul-k8s`. The
   trailing wildcard `deny` makes the default-deny posture explicit in
   the same file rather than relying on a separate global default.

3. **Use `service-resolver` to define subsets** (Consul's equivalent of
   Istio's `DestinationRule` subsets), then `service-splitter` to weight
   traffic across them for a canary rollout:
   ```hcl
   Kind = "service-resolver"
   Name = "payments-api"
   Subsets = {
     "v1" = { Filter = "Service.Meta.version == v1" }
     "v2" = { Filter = "Service.Meta.version == v2" }
   }
   ```
   ```hcl
   Kind = "service-splitter"
   Name = "payments-api"
   Splits = [
     { Weight = 90, ServiceSubset = "v1" },
     { Weight = 10, ServiceSubset = "v2" },
   ]
   ```

4. **Use `service-router` for L7 routing decisions** (path/header-based
   routing to different subsets or even different services), analogous
   to Istio `VirtualService` HTTP match rules:
   ```hcl
   Kind = "service-router"
   Name = "payments-api"
   Routes = [
     {
       Match { HTTP { PathPrefix = "/v2/" } }
       Destination { Service = "payments-api", ServiceSubset = "v2" }
     }
   ]
   ```

5. **Federate across datacenters with WAN federation** when server
   clusters can reach each other over a routable network:
   ```hcl
   # datacenter "dc2" server config
   datacenter = "dc2"
   primary_datacenter = "dc1"
   retry_join_wan = ["<dc1-server-1-address>", "<dc1-server-2-address>"]
   ```
   Or, for environments where server clusters are genuinely isolated
   (separate cloud accounts/VPCs with no flat network), use **cluster
   peering** instead, which establishes a mesh gateway-routed connection
   between independently-administered clusters without requiring shared
   Gossip/Raft membership:
   ```bash
   consul peering generate-token -name dc2-peer > dc2-peering-token.txt
   consul peering establish -name dc1-peer -peering-token "$(cat dc2-peering-token.txt)"
   ```
   Exported services between peers are then explicitly declared via an
   `exported-services` config entry — peering does not expose the whole
   catalog by default.

6. **Enable mesh gateways for cross-datacenter mesh traffic** so
   service-to-service calls across datacenters don't require every
   agent to have direct L3 connectivity to every remote service, only to
   the remote datacenter's mesh gateway:
   ```hcl
   Kind = "mesh"
   TransparentProxy { MeshDestinationsOnly = false }
   ```
   Mesh gateways terminate/originate the encrypted mesh connection at
   the datacenter boundary, which is also what makes WAN federation or
   peering practical across networks that aren't fully flat/routable.

7. **Confirm ACLs and intentions are actually enforcing**, not just
   present, before relying on them:
   ```bash
   consul intention check checkout-service payments-api
   ```
   This returns the actual allow/deny decision Consul's mesh would make
   for that source/destination pair — more reliable than reading the
   intention file and assuming it's correctly scoped.

## Best practices

- Enable ACLs and ship every production Consul cluster with a
  default-deny intention posture — a mesh where anything can call
  anything by default provides discovery but no real authorization.
- Prefer cluster peering over WAN federation for genuinely separate
  cloud environments or organizations — federation assumes a level of
  network and Gossip-key trust between datacenters that often doesn't
  match a real multi-cloud/multi-tenant boundary.
- Keep `service-resolver`/`service-splitter`/`service-router` config
  entries paired and reviewed together per service — a `service-splitter`
  referencing a subset the `service-resolver` doesn't define fails
  silently rather than erroring loudly.
- Register health checks on every service — a service with no check is
  reported healthy indefinitely even after it stops responding, which
  defeats both discovery and mesh routing decisions.
- Explicitly declare `exported-services` per peering relationship rather
  than assuming peered clusters see each other's whole catalog — peering
  is opt-in per service by design.
- If most of the estate is Kubernetes-only with no VM/bare-metal or
  multi-datacenter requirement, weigh whether Consul's operational
  overhead (running and federating server clusters, agent placement on
  every VM) is worth it versus a Kubernetes-native mesh — see
  [linkerd-service-mesh-configuration](../linkerd-service-mesh-configuration/SKILL.md)
  or
  [service-mesh-istio](../../../kubernetes-platform/skills/service-mesh-istio/SKILL.md)
  for that comparison when hybrid/multi-cloud reach isn't actually
  needed.

## Common pitfalls

- **Symptom:** A service is registered and shows healthy in the catalog,
  but calls to it over the mesh are rejected.
  **Fix:** Registration and mesh authorization are separate layers — an
  intention explicitly allowing the caller must exist. Run `consul
  intention check <source> <destination>` to see the actual decision
  Consul's mesh makes, rather than assuming registration implies
  reachability.

- **Symptom:** A `service-splitter` is applied with the intended
  weights, but all traffic still lands on one subset.
  **Fix:** The referenced `service-resolver` subset filter (e.g.
  `Service.Meta.version == v2`) doesn't match any actually-registered
  service instance's metadata — check that instances are registered
  with the `version` meta tag the resolver's `Filter` expects, since a
  splitter referencing a resolver subset with zero matching instances
  fails without an explicit error.

- **Symptom:** WAN federation between two datacenters intermittently
  drops or never establishes.
  **Fix:** Usually a network reachability or Gossip-encryption-key
  mismatch between the datacenters' server clusters — WAN federation
  requires routable connectivity on the serf WAN port between all
  federated servers and identical Gossip keys. If the datacenters are in
  genuinely separate networks/cloud accounts without a routable path,
  use cluster peering instead of trying to force WAN federation to work
  across a boundary it wasn't designed for.

- **Symptom:** After enabling ACLs, agents across the fleet start
  failing to register services or resolve the catalog.
  **Fix:** Every agent and service registration needs a valid ACL token
  with sufficient policy scope once `acl.enabled = true` — this is a
  deliberate, disruptive migration, not a flip-a-flag change. Roll out
  ACLs with `acl.default_policy = allow` initially paired with explicit
  deny rules for what you actually want to restrict, then migrate to
  `default_policy = deny` once every legitimate agent/service has a
  correctly-scoped token, rather than flipping straight to deny-by-default
  cluster-wide.

- **Symptom:** To debug a mesh connectivity failure, someone disables
  ACLs or sets a wildcard `allow` intention cluster-wide "temporarily,"
  and it's still in place weeks later.
  **Fix:** This is a significant security regression — a
  default-allow-everything mesh has no authorization boundary at all.
  Debug via `consul intention check` and agent/proxy logs instead of
  disabling enforcement; if enforcement genuinely must be relaxed to
  isolate a problem, scope the relaxation narrowly (one specific
  source/destination pair, on a non-production datacenter) and track an
  explicit revert.

## Worked example

**Scenario:** A hybrid estate has `checkout-service` running on
Kubernetes and `payments-api` running on a fleet of VMs in a different
cloud account, connected via cluster peering, with a canary rollout of
`payments-api` v2 at 10% traffic.

VM-side service registration (`payments-api.hcl`, loaded by the local
Consul agent):
```hcl
service {
  name = "payments-api"
  port = 8080
  meta = { version = "v1" }
  connect { sidecar_service {} }
  checks = [
    { http = "http://localhost:8080/healthz", interval = "10s", timeout = "2s" }
  ]
}
```

Intention allowing only `checkout-service`:
```hcl
Kind = "service-intentions"
Name = "payments-api"
Sources = [
  { Name = "checkout-service", Action = "allow" },
  { Name = "*", Action = "deny" }
]
```

Canary split:
```hcl
Kind = "service-resolver"
Name = "payments-api"
Subsets = {
  "v1" = { Filter = "Service.Meta.version == v1" }
  "v2" = { Filter = "Service.Meta.version == v2" }
}
```
```hcl
Kind = "service-splitter"
Name = "payments-api"
Splits = [
  { Weight = 90, ServiceSubset = "v1" },
  { Weight = 10, ServiceSubset = "v2" },
]
```

Apply and verify:
```bash
consul config write payments-api-intentions.hcl
consul config write payments-api-resolver.hcl
consul config write payments-api-splitter.hcl
consul intention check checkout-service payments-api
```

`checkout-service`, running on Kubernetes in a peered cluster, resolves
and calls `payments-api` through the mesh gateway connecting the two
peered environments, with 10% of calls landing on the v2 subset — all
without either side needing direct L3 reachability to individual
instances in the other cloud account. Before promoting the split
further, run the intention and config-entry checks in
[consul-configuration-validation](../consul-configuration-validation/SKILL.md).

## Cross-references

- [consul-configuration-validation](../consul-configuration-validation/SKILL.md) — validating service definitions and intentions before applying them, including catching the subset/resolver mismatches described above.
- [linkerd-service-mesh-configuration](../linkerd-service-mesh-configuration/SKILL.md) — a simpler Kubernetes-native mesh alternative when the multi-cloud/VM reach Consul provides isn't actually needed.
- [cilium-ebpf-cni-and-mesh-configuration](../cilium-ebpf-cni-and-mesh-configuration/SKILL.md) — a CNI-layer alternative for Kubernetes-only mesh/networking needs, worth comparing when Consul's VM support is the only reason it's on the table.
- [service-mesh-istio](../../../kubernetes-platform/skills/service-mesh-istio/SKILL.md) — the equivalent Kubernetes-native mesh concepts (`VirtualService`/`DestinationRule` map roughly to `service-router`/`service-resolver` here) for teams comparing the two.
