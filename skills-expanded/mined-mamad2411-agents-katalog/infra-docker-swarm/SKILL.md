---
name: infra-docker-swarm
description: Use when running Docker Swarm — stacks, services, secrets, configs, overlay networks, placement, rolling updates.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [infra-docker-compose, infra-prometheus-grafana, observability-essentials]
---

# Infra Docker Swarm

**Iron Law: state belongs in stateful services with explicit volume placement, NEVER in "stateless" service containers. Use stacks + secrets + overlay networks. If you find yourself reaching for k8s features, you've outgrown Swarm — migrate, don't bend.**

**Base image default:** Debian (`*-slim`, `*-trixie-slim`, `distroless-debian`). Alpine only when image size dominates and you've verified musl-libc compat (cgo, glibc-only wheels, DNS resolver edge cases). Long-form rationale: `Skill(infra-docker-images)`.

## When Swarm (vs k8s / Nomad / Compose)

| Tool        | Fit                                                                                     |
| ----------- | --------------------------------------------------------------------------------------- |
| **Swarm**   | 1-20 nodes, 1-50 services, small team — **lighter than k8s, more capable than Compose** |
| **Compose** | 1 host; development + homelab only — not for multi-host production                      |
| **Nomad**   | mixed workloads (containers + raw binaries), HashiCorp shop                             |
| **k8s**     | 20+ nodes, complex routing/autoscaling/operators, dedicated platform team               |

Swarm is dead-simple to operate (one daemon, raft built-in) but lacks: HPA, complex Ingress, operators, CRDs, the entire CNCF ecosystem. If you need those, migrate.

## Bootstrap

```bash
# On manager
docker swarm init --advertise-addr 10.0.0.10

# On worker (run the join command swarm init printed)
docker swarm join --token SWMTKN-... 10.0.0.10:2377

# Promote workers to managers — keep an ODD number (1, 3, 5)
docker node promote worker1 worker2
```

**Manager count**: 1 (dev), 3 (prod small), 5 (prod resilient). Even counts cause raft split-brain. Don't run workloads on managers in prod.

## Stack file (compose v3.x with `deploy:`)

```yaml
# stack.yml — deploy with: docker stack deploy -c stack.yml myapp
services:
  api:
    image: registry.example.com/api:v1.4.2 # MUST be a registry the swarm can pull from
    networks: [appnet]
    secrets: [db_password]
    configs:
      - source: api_yaml
        target: /etc/api/config.yaml
        mode: 0444
    deploy:
      replicas: 4
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first # start new before stopping old (zero-downtime)
        failure_action: rollback
      rollback_config:
        parallelism: 1
        delay: 5s
      restart_policy:
        condition: any
        max_attempts: 3
      placement:
        constraints: ["node.role==worker", "node.labels.tier==app"]
        preferences: [{ spread: node.labels.zone }] # spread across AZs
      resources:
        limits: { cpus: "1.0", memory: 512M }
        reservations: { cpus: "0.25", memory: 128M }
    healthcheck:
      test: ["CMD", "curl", "-fsS", "http://localhost:8080/healthz"]
      interval: 10s
      timeout: 3s
      retries: 3

  db:
    image: postgres:17 # Debian variant; -alpine only after musl/cgo audit
    networks: [appnet]
    secrets: [db_password]
    volumes:
      - dbdata:/var/lib/postgresql/data
    deploy:
      replicas: 1
      placement:
        constraints: ["node.labels.has_db_volume==true"] # pin to the node with the disk
      restart_policy:
        condition: on-failure

volumes:
  dbdata: # local driver — pinned by constraint above

networks:
  appnet:
    driver: overlay # prod app network — NO attachable (would let any host container sniff inter-service traffic)
  debugnet:
    driver: overlay
    attachable: true # debug-only network for `docker run --network debugnet ...` triage

secrets:
  db_password:
    external: true # created out-of-band: docker secret create

configs:
  api_yaml:
    file: ./api.config.yaml
```

`docker stack deploy -c stack.yml myapp` — idempotent, applies diff.

## Secrets + configs

```bash
echo -n "$PASSWORD" | docker secret create db_password -
docker secret ls
```

Secrets are encrypted at rest in raft, mounted at `/run/secrets/<name>` (mode 0400) in containers. **Cannot be updated in place.** Rotate in this exact order to avoid an auth-failure window:

> **Prereq**: `update_config.order: start-first` on the service (Swarm default is `stop-first`, which creates a hard downtime window during rollout).
>
> 1. **Upstream dual-credentials**: configure DB/broker to accept BOTH old and new credentials simultaneously.
> 2. **Create v2 secret**: `docker secret create db_password_v2 - < /path/to/new`.
> 3. **Deploy**: update stack to reference `db_password_v2`; `docker stack deploy`. `start-first` brings new replicas up against either credential before old ones stop.
> 4. **Wait** for rollout to complete (`docker service ps <svc>` all Running).
> 5. **Revoke** the old credential upstream.
> 6. **Remove** old secret: `docker secret rm db_password`.

Skipping step 1 → new replicas fail auth → `rollback` triggers → you redeploy to a half-revoked state. Same model for `configs`.

## Overlay networks + service discovery

Each service is reachable as `<service>` (VIP) or `tasks.<service>` (per-replica DNS) on its overlay; Swarm L4-load-balances via the routing mesh. From a container: `curl http://api:8080/healthz` (round-robins replicas), `dig +short tasks.api` (individual IPs). `attachable: true` lets ad-hoc debug containers join — invaluable for triage but ANY host container can attach (no auth), so it's a sniffing primitive. Use a dedicated `debugnet` overlay, never `attachable: true` on the prod app network.

## Ingress routing mesh

```yaml
deploy:
  endpoint_mode: vip # default — VIP + iptables LB
  # or:  dnsrr                           # DNS-RR, exposes individual replicas
```

Publish a port and **any node** routes to a healthy replica:

```yaml
ports:
  - target: 8080
    published: 443
    protocol: tcp
    mode: ingress # routing mesh (default)
    # or: host                           # bind to that node only
```

Put a TLS-terminating proxy (Traefik, Caddy, nginx) on the swarm itself as a service for path-based routing and certs.

## Placement — non-negotiable for stateful

| Constraint                        | Use                             |
| --------------------------------- | ------------------------------- |
| `node.role==worker`               | keep load off managers          |
| `node.labels.zone==eu-west-1a`    | pin to zone for HA              |
| `node.labels.has_db_volume==true` | DB pinned to node with the disk |
| `node.hostname==db01`             | last resort, brittle            |

Label nodes: `docker node update --label-add zone=eu-west-1a node1`. Without constraints, the scheduler picks freely — and a DB with a local volume on the wrong node = data unreachable after restart.

## Rolling updates

```bash
docker service update --image registry.example.com/api:v1.4.3 myapp_api
# Honors update_config: parallelism, order, failure_action
```

Set `order: start-first` for HTTP services (zero-downtime). Set `failure_action: rollback` so a bad image auto-rolls back. Watch with `docker service ps myapp_api`.

## Anti-patterns

- Running stateful services without placement constraints — DB migrates, volume left behind
- Even number of managers (2, 4) — raft split-brain
- Workloads on managers in prod — manager loss = cluster loss + workload loss
- Local images (`build:` in stack file) — swarm pulls from registries only; pre-push
- Secrets via `environment:` — leak via `docker inspect`
- One stack for "everything" — keep stacks domain-scoped, ≤ 15 services each
- Building swarm-only features when you're 6 months from k8s — accept the migration
- Updating secrets in place by `docker secret rm` + recreate during traffic — service restart required; do the v2 swap pattern
- Ignoring `attachable: true` and SSHing into nodes to debug — debug container on the overlay net is cleaner
- `--force` recreating services in the middle of an incident — make a backup of the stack file state first

## Red flags

| Thought                                             | Reality                                                                   |
| --------------------------------------------------- | ------------------------------------------------------------------------- |
| "We just need autoscaling, swarm is fine otherwise" | Swarm has no HPA; you'll bolt on a script that breaks under load          |
| "All replicas died on one node"                     | Missing `placement.preferences: spread: zone` — fix it before next outage |
| "Just give it `node.role==manager`"                 | Now your control plane is also your hot path; one bad service kills both  |
| "We'll move to k8s next quarter"                    | Plan it now or accept Swarm; don't half-migrate for 18 months             |

## Hand-off

For single-host development with compose: `Skill(infra-docker-compose)`. For monitoring the swarm: `Skill(infra-prometheus-grafana)`. For logs/traces aggregation: `Skill(observability-essentials)`.
