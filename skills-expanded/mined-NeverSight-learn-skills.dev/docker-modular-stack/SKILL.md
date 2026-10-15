---
name: docker-modular-stack
description: >
  Define, scaffold, and lint Docker services for any project. Three modes: (1) Scaffold — copy
  curated templates (postgres, valkey, grafana, langfuse, litellm, 30+ more) into a new project
  with generated docker-compose.yaml, .env, and Taskfile; (2) Add — given any tool's
  documentation, derive a compliant service.yaml from scratch; (3) Lint — validate any service
  definition against the project's conventions. Use when setting up a docker stack, adding a new
  docker service from docs, or checking whether a service definition is correct.
compatibility: >
  Requires Docker and Docker Compose v2. Target project must have a writable root directory.
---

# docker-modular-stack

Three modes — read the user's intent and pick one:

| User says | Mode |
|-----------|------|
| "set up docker stack", "scaffold services", "add postgres/grafana/…" (named template) | **Scaffold** |
| "add [tool] to docker", "create a service for [tool]", provides docs/URL/README | **Add new tool** |
| "check this service", "does this follow the conventions", "lint this yaml" | **Lint** |

---

## MODE A — Scaffold from templates

### A1 — Collect inputs

Ask before doing anything else:

1. **Project slug** (kebab-case, e.g. `my-app`) — Compose project name, DNS zone prefix. Lowercase + hyphens only.
2. **Docker network prefix** (e.g. `10.9`) — first two octets of subnet. Remind user to check for conflicts: `docker network ls`.
3. **Networking mode** — `coredns` (default) or `traefik`.
   - **CoreDNS**: DNS-based `.internal` hostnames; systemd-resolved config generated in Taskfile.
   - **Traefik**: HTTP reverse proxy; ports 80/443 on host; label-based routing.

Derive: `DNS_ZONE = {slug}.internal`, `COMPOSE_NETWORK = {slug}_main`.

### A2 — Show service menu

Read `references/catalog.md` for the full list. Present grouped by layer:

```
NETWORK:        [ ] coredns  [ ] traefik  [ ] kong
DATA:           [ ] postgres [ ] clickhouse [ ] valkey [ ] redis
                [ ] minio    [ ] neo4j     [ ] falkor_db [ ] chroma
OBSERVABILITY:  [ ] grafana  [ ] tempo  [ ] otel-collector
                [ ] langfuse [ ] phoenix [ ] hyperdx
COMMUNICATIONS: [ ] mailpit  [ ] mailslurper
APP_DEPENDENCY: [ ] authentik [ ] oryd [ ] graphiti
APP:            [ ] litellm  [ ] hasura  [ ] kestra  [ ] hermes
                [ ] archon   [ ] paperclip [ ] tensorzero
                [ ] mission_control [ ] prefect
                [ ] ollama  [ ] webui  [ ] inspector
```

CoreDNS mode: auto-include `coredns`.

### A3 — Auto-resolve dependencies

```
otel-collector → clickhouse
graphiti       → falkor_db
grafana        → postgres, clickhouse
authentik      → postgres, valkey
oryd           → postgres
hasura         → postgres
kestra         → postgres
litellm        → postgres
langfuse       → postgres, clickhouse, minio, valkey
webui          → ollama (only auto-add if ollama also selected)
```

Deduplicate. Inform the user what was auto-added.

### A4 — Copy service files

Copy from `assets/services/{service}/` → `{project-root}/docker/{service}/`. Apply substitutions:

| Placeholder | Replace with |
|-------------|-------------|
| `PLACEHOLDER_DNS_ZONE` | `{slug}.internal` |
| `PLACEHOLDER_NET_PREFIX` | `{prefix}` |
| `PLACEHOLDER_COMPOSE_NETWORK` | `{slug}_main` |

Files containing `PLACEHOLDER_DNS_ZONE`: `coredns/Corefile`, `langfuse.yaml`, `litellm/service.yaml`.

Flat services (no folder — copy as `docker/{name}.yaml`):
`redis.yaml`, `valkey.yaml`, `minio.yaml`, `chroma.yaml`, `phoenix.yaml`, `hyperdx.yaml`, `mailpit.yaml`, `mailslurper.yaml`, `langfuse.yaml`, `ollama.yaml`, `webui.yaml`, `inspector.yaml`, `neo4j.yaml`.

### A5 — Generate docker-compose.yaml

```yaml
name: "{slug}"

include:
  - docker/{service}/service.yaml   # folder services
  - docker/{service}.yaml           # flat services

networks:
  main:
    driver: bridge
    ipam:
      config:
        - subnet: {prefix}.0.0/16
          gateway: "{prefix}.0.1"
```

### A6 — Generate .env

Open `assets/env.template`. Splice sections for selected services using the header map:

| Section header | Service(s) |
|---------------|-----------|
| `Postgres (db)` | postgres |
| `ClickHouse (analytics_db)` | clickhouse |
| `Valkey / Redis (cache)` | valkey, redis |
| `Neo4j (graph_db)` | neo4j |
| `FalkorDB (graph_db1)` | falkor_db |
| `MinIO / Object Store (os)` | minio |
| `Authentik (idp)` | authentik |
| `Ory Hydra (oauth2)` + `Ory Kratos (users)` | oryd |
| `Hasura` | hasura |
| `LiteLLM` | litellm |
| `Langfuse` | langfuse |
| `Grafana` | grafana |
| `Graphiti` | graphiti |
| `Archon` | archon |
| `Hermes` | hermes |
| `Paperclip` | paperclip |
| `HyperDX` | hyperdx |
| `AWS` | litellm, tensorzero, paperclip (include if any selected) |
| `OpenAI` | litellm, tensorzero (include if any selected) |
| `Open WebUI` | webui |
| `Chroma` | chroma |
| `Misc` | always include |

### A7 — Generate Taskfile.yaml

**CoreDNS:**
```yaml
version: "3"
dotenv: ['.env']
tasks:
  dns:setup:
    desc: Forward {DNS_ZONE} queries to CoreDNS. Requires sudo.
    cmds:
      - sudo mkdir -p /etc/systemd/resolved.conf.d
      - |
        sudo tee /etc/systemd/resolved.conf.d/{slug}.conf > /dev/null <<'EOF'
        [Resolve]
        DNS={prefix}.255.254
        Domains=~{DNS_ZONE}
        EOF
      - sudo systemctl restart systemd-resolved
  dns:teardown:
    cmds:
      - sudo rm -f /etc/systemd/resolved.conf.d/{slug}.conf
      - sudo systemctl restart systemd-resolved
```

**Traefik:**
```yaml
version: "3"
dotenv: ['.env']
tasks:
  hosts:setup:
    desc: Add /etc/hosts entries for Traefik services. Requires sudo.
    cmds:
      - sudo tee -a /etc/hosts <<'EOF'
        127.0.0.1  traefik.{slug}.local
        EOF
  hosts:teardown:
    cmds:
      - sudo sed -i '/{slug}\.local/d' /etc/hosts
```

---

## MODE B — Add new tool from documentation

Use when the user provides a tool name, Docker Hub URL, README, or any documentation for a service not in the template library.

### B1 — Extract from docs

Read the provided documentation and extract:

- **Image**: exact name on Docker Hub / GHCR. Check available tags.
- **Required env vars**: what must be set for the container to start.
- **Optional env vars**: configuration knobs.
- **Ports**: which ports the container listens on and what they serve (UI vs. API vs. internal).
- **Volumes**: what data directories need persistence.
- **Healthcheck**: any `/health`, `/ping`, or `/_status` endpoint; or a CLI command the image ships.
- **Dependencies**: does it need a database, cache, or other service?

### B2 — Make conventions decisions

Apply the conventions checklist (see below) to every decision:

1. **Layer** — classify by role: network / data / observability / communications / app_dependency / app.
2. **Container name** — generic purpose noun, not the tool name (e.g. `metrics_db` not `prometheus`).
3. **Image tag** — pick the most recent stable, non-RC tag. Prefer `:{version}-alpine`, then `:{version}-slim`, then `:{version}`.
4. **Custom packages** — if the base image needs additions, write a `Dockerfile FROM {image}:{tag}` and comment out `image:` in `service.yaml`.
5. **IP** (CoreDNS mode) — assign from the correct layer range (see catalog.md).
6. **File layout** — flat `.yaml` if no config files; folder with `service.yaml` + `config/` if config is needed.

### B3 — Write the service file

Produce a `service.yaml` (or flat `{tool}.yaml`) that passes every item in the conventions checklist. Then:

- Add it to `docker/` in the project.
- Add its `include:` line to `docker-compose.yaml`.
- Add its env vars to `.env`.
- If CoreDNS: add its hostname to `coredns/Corefile` (new stanza or entry).

---

## MODE C — Lint / review

Run this checklist against any service definition the user provides. Report each failure with the rule that was violated.

### Conventions checklist

**File structure**
- [ ] Flat `.yaml` if no config files; folder with `service.yaml` + `config/` if config needed
- [ ] Folder/file name matches the tool name exactly (kebab-case)

**Naming**
- [ ] Container service name is a generic purpose noun, not the tool name
- [ ] No `container_name:` field anywhere

**Labels**
- [ ] Every service and helper container has a `layer=` label
- [ ] Helper containers inherit the same layer as their parent

**Images**
- [ ] Tag is pinned to a specific version — not `latest`, `main`, or any floating tag
- [ ] Alpine variant used if available (`:{version}-alpine`); slim second; full debian/ubuntu only if no alternative
- [ ] Tag is a stable release — no `-rc`, `-m0x`, `-beta`, `-alpha`, `-milestone` suffixes
- [ ] If custom packages needed: `Dockerfile` extends upstream image; original `image:` line is commented out in `service.yaml`

**Networking**
- [ ] No ports exposed to host unless the port serves a UI for external access
- [ ] Inter-service comms use Docker network service names, not `localhost`
- [ ] CoreDNS mode: static IP assigned from correct layer range (see catalog.md)

**CoreDNS networking** (check only when networking mode is CoreDNS)
- [ ] Service names contain no underscores — underscores are not valid DNS hostname characters; use hyphens (e.g. `mission-control` not `mission_control`)
- [ ] Authentik service (`idp-server`) includes `AUTHENTIK_LISTEN__HTTP: "0.0.0.0:80"` — without this, Authentik binds at port 9000 and all cross-service SSO URLs must include `:9000`

**Volumes**
- [ ] Named (managed) volumes used for data
- [ ] Bind mounts used only for config files

**Service definition**
- [ ] Healthcheck present if the image supports one
- [ ] `condition: service_healthy` used in `depends_on` when dependency has a healthcheck
- [ ] Helper containers (worker, beat, mcp) defined in the same file as their parent service
- [ ] No init-containers
- [ ] Env vars use inline `KEY: "value"` syntax — not `- KEY=VALUE` array form
