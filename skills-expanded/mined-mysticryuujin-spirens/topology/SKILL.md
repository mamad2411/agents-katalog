---
name: topology
description: Single-host Docker Compose vs Docker Swarm vs multi-zone — overlay networks, routing mesh, stateful service constraints (IPFS repo locality, Redis as shared cache). Use when deciding how to deploy, scaling out, or debugging cross-host networking.
---

# Deployment topology

## What You Probably Got Wrong

**You think Swarm = "more servers = more throughput."** Some services
scale horizontally (stateless HTTP proxies, RPC caches). Some don't
(IPFS nodes have per-repo state, Redis is typically a singleton cache).
Adding nodes to a Swarm doesn't magically make a stateful service
faster — it just gives you more places for the scheduler to land it.

**You assume overlay networks are transparent.** They aren't. Overlay
networks add VXLAN encapsulation: MTU shrinks (~1450 by default),
latency adds a hop, and some UDP-heavy protocols (notably QUIC/HTTP3)
misbehave. Know the cost before designing around multi-host.

**You publish a port in Swarm mode and assume Swarm's routing mesh
"just works" from outside.** The mesh routes any external request
hitting any node to a healthy replica — which is great, unless your
client sees a SYN-ACK from a different IP than it SYN'd to (some
firewalls drop this) or you care about source IPs (mesh rewrites them
unless you use host-mode publishing).

**You forget Compose's `include:` is not the same as Swarm stacks.**
Compose `include:` composes multiple files into one compose project.
Swarm stacks are independent deployments. SPIRENS handles both but they
aren't the same mechanism — don't copy compose patterns into Swarm
YAML blindly.

## The three topologies

### Single-host Compose

One box. `docker compose up`. Everything on one bridge network.

- **Pros:** simplest, most debuggable, no overlay overhead.
- **Cons:** one machine's failure = full outage; single machine's CPU
  / RAM / disk caps your scale.
- **When:** home lab, small production, any first deployment.

### Docker Swarm (single-host or multi-host)

Swarm adds the services/stacks abstraction with overlay networking and
optional multi-host scheduling.

- **Pros:** multi-host scheduling, rolling updates, built-in service
  discovery, secrets, routing mesh, health-based replica placement.
- **Cons:** overlay adds MTU + latency overhead; stateful services
  need volume strategy (`local` volumes tie a container to a node, or
  use a shared filesystem); troubleshooting is two levels deep.
- **When:** 2-10 hosts, you want HA without the kubernetes learning
  curve, your app decomposes cleanly into horizontally-scalable pieces.

### Multi-zone / cloud-managed

Kubernetes, Nomad, ECS, Fly.io — one step up in complexity and
capability.

- **Pros:** operational maturity, ecosystem, true HA across zones,
  autoscaling.
- **Cons:** every decision takes longer; most home-lab users regret
  reaching for this too early.
- **When:** you have multi-zone HA requirements, hundreds of services,
  a platform team, or compliance demands this flavor.

## Stateful service constraints

Every service in the SPIRENS stack has a specific statefulness story:

| Service       | Stateful?                     | Scaling story                                               |
| :------------ | :---------------------------- | :---------------------------------------------------------- |
| Traefik       | No (certs via volume)         | Scale horizontally if cert storage is shared                |
| Redis         | Yes                           | Single-node cache; cluster mode if you really need HA       |
| eRPC          | No (unless cache DB is local) | Stateless; stateful when pointed at persistent cache        |
| Kubo (IPFS)   | **Yes**                       | Repo is per-node; multi-node needs peering + per-node repos |
| dweb-proxy    | No                            | Stateless; scale horizontally                               |
| Ethereum node | Yes                           | Single node per client; run clients you need across boxes   |

### IPFS repo locality

Each Kubo node has its own blockstore on local disk. You cannot share
one `.ipfs/` repo between multiple Kubo processes — it would corrupt.

Options for multi-node IPFS:

1. **Independent nodes peered together.** Each has its own repo; when
   one is asked for a CID it doesn't have, it bitswaps from the other.
   Standard pattern. See `ipfs/SKILL.md`.
2. **One node, many gateway proxies.** Run one Kubo; put N stateless
   reverse proxies in front. Limits throughput to one Kubo's disk.
3. **Pinning service pattern.** Dedicated pinners (where content
   lives) + dedicated gateways (stateless, fetch from pinners).

SPIRENS ships pattern 1 by default; pattern 2 is what most single-host
deployments effectively are.

### Redis as shared cache

dweb-proxy uses Redis for caching and rate limiting. If you scale
dweb-proxy horizontally, they must all talk to the same Redis (or share
a Redis Cluster).

- **Single Redis:** the default in SPIRENS. Fine up to tens of
  thousands of ops/sec.
- **Redis Cluster:** real HA requires 6+ nodes (3 primaries + 3
  replicas minimum). Overkill for anything in the SPIRENS problem
  space.

## Swarm routing mesh — what it does and doesn't

When a service publishes port 443 in Swarm mode, any node in the swarm
accepts traffic on :443 and routes it to a healthy replica, even if the
replica is on a different node. This is the routing mesh.

**Gotchas:**

- **Source IP is lost** unless you use `mode: host` publishing. For a
  gateway that cares about `X-Real-IP` — every web3 gateway does —
  always use host-mode publishing on the edge proxy (Traefik), and
  make sure Traefik runs on every edge node via a global service.
- **Routing mesh latency** adds a hop when the request lands on a node
  that doesn't have a replica.
- **Asymmetric routing** can confuse stateful firewalls — if they see
  a SYN from Node A and a SYN-ACK from Node B, some drop the flow.

### The SPIRENS Swarm pattern

Traefik runs as a global service (one replica per node) in host-mode.
Backend services run as replicated services on the overlay network
without port publishing. Traefik forwards overlay-internally to
backends.

Details: [`docs/04-deployment-profiles.md`](../docs/04-deployment-profiles.md).

## Volume strategies for stateful services in Swarm

Options, ordered by complexity:

1. **Constraint to a specific node.** Tie the service to one node via
   `deploy.placement.constraints` so its local volume persists across
   restarts. Simple; service can't move.
2. **NFS / S3-backed volume driver.** `docker volume` with an NFS or
   S3 backend. Service can move; network filesystem adds latency and
   operational surface.
3. **Per-node data + application-level sync.** Each replica has its
   own local data; the application replicates at the application layer
   (Redis replication, IPFS peering, Ethereum client P2P). This is the
   right pattern for IPFS.

Don't use pattern 2 for IPFS repo (Kubo performs badly on network
filesystems). Don't use pattern 1 for something that needs HA.

## Picking the right topology for SPIRENS

- **Home lab, one box, up to a few users:** single-host Compose.
- **2-3 boxes, you want restart survival:** single-host Compose with
  off-site backups, or trivial Swarm (one manager) to get rolling
  updates.
- **Multi-box, real availability needs:** proper Swarm with separate
  manager and worker nodes, global Traefik, per-node Kubo peered
  across nodes, shared Redis.
- **Multi-zone HA, multiple admins, long-term maintenance:** reach for
  Kubernetes. Out of scope for SPIRENS.

## Troubleshooting topology issues

### Overlay networking

```bash
# Confirm overlay exists and is attached to services.
docker network ls | grep overlay
docker network inspect <overlay-name>

# From inside a container, test reach to another service by name.
docker exec -it <container> sh
ping -c1 other-service
nslookup other-service
```

### Routing mesh misbehavior

```bash
# Show which node each replica is on.
docker service ps <service>

# Which node is this request hitting right now?
curl -s https://rpc.example.com/diag   # if you implement a diag endpoint

# Is publishing host-mode or ingress?
docker service inspect --format '{{json .Endpoint}}' <service>
```

### IPFS across nodes

```bash
# Are the two Kubo nodes actually peered?
docker exec spirens-ipfs-node1 ipfs swarm peers | grep <node2-peer-id>

# If not, check Peering config on each.
```

## Worked example: SPIRENS both topologies

Two parallel trees that share `config/`:

- `compose/single-host/*.yml` — `docker compose` entrypoint.
- `compose/swarm/stack.*.yml` — one stack per service for `docker stack
deploy`.

Module parity: every service is in both. The Compose `include:` file
bundles them into one project; Swarm deploys each as a separate stack
on a shared overlay network.

Full details: [`docs/04-deployment-profiles.md`](../docs/04-deployment-profiles.md).

## Upstream references

- [Docker Compose specification](https://compose-spec.io/)
- [Docker Swarm mode](https://docs.docker.com/engine/swarm/)
- [Swarm routing mesh](https://docs.docker.com/engine/swarm/ingress/)
- [Swarm services publishing](https://docs.docker.com/engine/swarm/services/#publish-ports)
- [Docker volume drivers](https://docs.docker.com/engine/extend/plugins_volume/)
