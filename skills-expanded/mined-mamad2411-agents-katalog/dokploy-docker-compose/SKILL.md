---
name: dokploy-docker-compose
description: >
  Comprehensive guide for deploying Docker Compose stacks on Dokploy (self-hosted VPS deployment platform).
  Use this skill whenever the user mentions Dokploy, deploying Docker Compose to a VPS, deploying applications
  with docker-compose.yml on a self-hosted server, or when troubleshooting Docker Compose stacks running on
  Dokploy. Covers both Compose (stack) and Application (Git) deployment types, volume strategies,
  networking, environment variables, init containers, healthchecks, domains with Traefik, and troubleshooting
  common errors like EAI_AGAIN, permission denied, unhealthy containers, and JWT/config issues. Also applies
  when deploying any multi-service Docker Compose stack to Dokploy.
---

# Dokploy Docker Compose Deployment Skill

## Overview

Dokploy is a self-hosted deployment platform that manages Docker containers on a VPS. It supports two
compose modes (Docker Compose and Docker Stack) and requires specific patterns to work reliably.

**Quick decision tree:**
- Single-repo app with `Dockerfile`? → **Application (Git)** deployment
- Pre-built images or multi-service stack? → **Compose** deployment
- Need a public HTTPS domain? → **Domains tab** (Dokploy auto-injects Traefik labels)
- Need isolated networking per-app? → Enable **Isolated Deployments** in UI
- Config files needed without SSH? → **File Mounts** in Advanced → Mounts
- Complex stack needing generated configs + binary downloads? → **Init Containers** pattern

---

## Part 1: Service Types

### Compose (Docker Compose mode)
Best for: multi-service stacks using pre-built images. Standard `docker compose up` behavior.

Key constraints vs running locally:
- Each deploy via AutoDeploy does a **`git clone`** which clears the repository directory — any relative path like `./config.yaml` will be **empty or missing** after the first push
- Never use `container_name:` on services — it breaks Dokploy's logs, metrics, and monitoring features
- Relative bind mounts (`./data`) work only on first deploy; use `../files/` or named volumes instead

### Stack (Docker Swarm mode)
Docker Stack mode for orchestrated deployments. Key differences from Compose mode:
- **No `build:` directive** — must use pre-built images from a registry
- Traefik labels must go under **`deploy.labels`**, not directly under `labels`
- Add `--with-registry-auth` flag in Advanced → Command if using private registries with replicas

### Application (Git) Deployment
Best for: source code you build from a Dockerfile.

Steps: Create Service → Application → Source: Git → Build Type: Dockerfile → configure Volumes and Ports in Advanced.

---

## Part 2: Volume Strategy

⚠️ **Critical Dokploy rule:** Absolute host paths (e.g., `/opt/myapp/`) are **cleaned up during deployments**. Never use them. Use the `../files/` folder or named volumes instead.

### Named Volumes (Best for databases and large data)
```yaml
services:
  db:
    image: postgres:16
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```
Docker manages these. Supports **automated backups** via Dokploy's Volume Backups feature. Best for databases, large datasets.

### `../files/` Bind Mounts (Best for config files and small data)
Dokploy provides a persistent `../files/` folder that survives deployments:
```yaml
volumes:
  - ../files/my-config:/etc/myapp/config    ✅ persists across deploys
  - ../files/my-database:/var/lib/mysql     ✅ persists across deploys
  - ./config.yaml:/app/config.yaml          ❌ wiped on each AutoDeploy (git clone)
  - /opt/myapp/data:/app/data               ❌ absolute paths are cleaned up by Dokploy
```
No direct host file access needed. Best for config files, small datasets. No backup support.

**Host path on the VPS:** `../files/` maps to a `files/` folder inside Dokploy's project directory on the host. To find the exact path after first deploy, SSH in and run:
```bash
# Step 1: find your container name (Dokploy names them <stack>-<service>-1)
docker ps --format "table {{.Names}}\t{{.Image}}" | grep <service-keyword>

# Step 2: inspect that container to see where ../files/ maps on the host
docker inspect <container-name> | grep -A2 '"Source"'
```
Or check the **Docker tab** in the Dokploy UI — the container name is listed there directly.

### File Mounts (Dokploy UI — for pasting config content directly)
In **Advanced → Mounts → Add Mount → File Mount**:
- **Content**: paste the file text
- **File Path**: just the filename (e.g., `config.yaml`)
- **Mount Path**: full container path (e.g., `/app/config/config.yaml`)

✅ Best for: config files you want to manage entirely in Dokploy UI
❌ Not for: binary files, files needing runtime generation, files > a few KB

### Init Container Pattern (for complex stacks needing generated configs)
When a stack needs multiple config files written at runtime, or binary downloads, use an alpine init
container that writes files into a shared named volume before the main service starts:

```yaml
services:
  my-conf:
    image: alpine:3.20
    command:
      - /bin/sh
      - -lc
      - |
        cat > /config/app.yaml <<'YAML'
        key: value
        YAML
        apk add --no-cache wget && wget -O /scripts/tool "https://..."
    volumes:
      - app-config:/config
      - app-scripts:/scripts
    restart: "no"   # MUST exit after running

  app:
    depends_on:
      my-conf:
        condition: service_completed_successfully
    volumes:
      - app-config:/etc/app/
      - app-scripts:/usr/local/scripts/
```

**Shell escaping:** Use `$$` inside compose heredocs — `$$(uname -s)` not `$(uname -s)`.

See `references/init-container-patterns.md` for complete examples.

### Choosing the Right Volume Method

| Need | Method |
|------|--------|
| Database data | Named volume |
| Automated backups to S3 | Named volume (only option) |
| Config file — manage in UI | File Mount |
| Config file — large or complex | `../files/` bind mount |
| Generated configs + binaries | Init container → named volume |
| ❌ Do NOT use | Absolute host paths, `./` relative paths |

---

## Part 3: Environment Variables

### How Dokploy handles env vars
Variables set in the **Environment tab** are written to a `.env` file in the same directory as
`docker-compose.yml`. They are **NOT automatically injected** into containers. You must explicitly
load them in your compose YAML using one of two approaches:

**Option A — Load all variables (simpler for many vars):**
```yaml
services:
  app:
    env_file:
      - .env        # loads every variable from Dokploy's Environment tab
```

**Option B — Select specific variables:**
```yaml
services:
  app:
    environment:
      - JWT_SECRET=${JWT_SECRET}
      - DATABASE_URL=${DATABASE_URL}
      - PORT=3000                   # hardcoded values also work
```

⚠️ If you use `environment:` with explicit variables, only those listed variables are passed.
Any variable set in the UI but not listed here will be silently ignored.

**Recommendation:** For stacks with many secrets (LibreChat, etc.) use `env_file: - .env` on each
service that needs them. For stacks where services need different subsets, use explicit `${VAR}` refs.

### Generate secure values
```bash
openssl rand -hex 32    # 64-char hex string (for keys like CREDS_KEY)
openssl rand -hex 16    # 32-char hex string (for IVs like CREDS_IV)
```

---

## Part 4: Domains & Traefik Routing

Dokploy uses Traefik as a reverse proxy. There are two ways to expose services via a domain.

### Method 1: Dokploy Domains UI (Recommended — since v0.7.0)
Go to your service → **Domains tab** → **Add Domain**. Dokploy **automatically injects** the
correct Traefik labels into your compose file at deploy time. You never touch the labels manually.

- Use `expose:` (not `ports:`) in your compose YAML when routing via domain
- Use **Preview Compose** button to see the final compose file with auto-injected labels

```yaml
services:
  app:
    image: myapp:latest
    expose:
      - 3000    # container-only; Traefik routes via domain, no host port needed
```

### Method 2: Manual Traefik Labels (Advanced)
For fine-grained control, add labels directly in your compose file. Requires connecting to
`dokploy-network` (the shared Traefik network):

```yaml
services:
  frontend:
    image: myapp:latest
    expose:
      - 3000
    networks:
      - dokploy-network
    labels:
      - traefik.enable=true
      - traefik.http.routers.my-unique-name.rule=Host(`app.yourdomain.com`)
      - traefik.http.routers.my-unique-name.entrypoints=websecure
      - traefik.http.routers.my-unique-name.tls.certResolver=letsencrypt
      - traefik.http.services.my-unique-name.loadbalancer.server.port=3000

networks:
  dokploy-network:
    external: true
```

**For Docker Stack** — labels go under `deploy.labels`:
```yaml
services:
  frontend:
    image: myapp:latest
    deploy:
      labels:
        - traefik.enable=true
        - traefik.http.routers.my-app.rule=Host(`app.yourdomain.com`)
        - traefik.http.services.my-app.loadbalancer.server.port=3000
    networks:
      - dokploy-network
```

### Isolated Deployments
Enable this in the Dokploy UI (toggle on the Compose service page) to give your stack its own
private network instead of sharing `dokploy-network`. This is:
- Required when running **multiple instances** of the same app (e.g., two WordPress sites)
- Safer — services aren't visible across other stacks
- Automatic — Dokploy handles all network creation and Traefik wiring

When Isolated Deployments is enabled, you don't need to add `dokploy-network` manually.
All open-source templates shipped with Dokploy have this enabled by default.

⚠️ If NOT using Isolated Deployments, only the domain-targeted service gets `dokploy-network`
added automatically. Other services in the stack won't be on that network unless you add it manually.

---

## Part 5: Networking & DNS (EAI_AGAIN Fix)

The most common multi-service error:
```
getaddrinfo EAI_AGAIN mongodb
```
Container can't resolve another service's hostname. Causes: race condition or DNS confusion.

**Fix 1 — Healthchecks + proper `depends_on`** (prevents race conditions):
```yaml
services:
  api:
    depends_on:
      mongodb:
        condition: service_healthy    # waits until healthy, not just started
  mongodb:
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      retries: 5
      start_period: 10s
```

**Fix 2 — Explicit custom network** (guarantees DNS between services):
```yaml
networks:
  app-net:
    driver: bridge

services:
  api:
    networks: [app-net]
  mongodb:
    networks: [app-net]
```

⚠️ Avoid using `container_name:` as a DNS workaround — it breaks Dokploy monitoring features.
Use service names for inter-container communication instead.

---

## Part 6: Healthchecks

Add a `healthcheck` to every dependency service (databases, caches, queues). Pair it with `depends_on: condition: service_healthy` on services that need them — this prevents race conditions where a service starts before its dependency is ready.

**Example:**
```yaml
services:
  postgres:
    image: postgres:16
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
  app:
    depends_on:
      postgres:
        condition: service_healthy
```

---

## Part 7: Updating Deployed Services

### Manual update (public repos you don't own)
1. Go to Deployments tab → Click **Deploy**
2. If Docker cache is stale: look for "Redeploy without Cache" or clear Build Cache in System Settings

### Automatic updates via Webhook
1. Copy Webhook URL from **Deployments tab**
2. Add it to your GitHub/GitLab/Gitea repo Settings → Webhooks
3. Every push to the branch triggers an automatic deploy

---

## Part 8: Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `getaddrinfo EAI_AGAIN <hostname>` | Race condition / DNS | Add healthcheck + `condition: service_healthy`; use custom network |
| Config file empty after redeploy | `./` relative path wiped by git clone | Use `../files/` bind mount or File Mount in UI |
| `JwtStrategy requires a secret or key` | JWT env var not injected | Add `env_file: - .env` or explicit `- JWT_SECRET=${JWT_SECRET}`; **Redeploy** (not Restart) |
| `ENOENT: no such file or directory` | Config file not mounted | Use File Mount in Advanced → Mounts, or `../files/` bind mount |
| `permission denied` on volume | Old volume from different user | Rename volume (e.g., `data-v2`) to force fresh creation |
| Container `is unhealthy` | Wrong healthcheck for image | Match healthcheck command to image type; see Part 6 |
| Logs/metrics missing in Dokploy | `container_name:` set on service | Remove `container_name:` — it breaks Dokploy's monitoring |
| Services can't see each other after adding domain | Not on same network | Use Isolated Deployments, or manually add `dokploy-network` to all services |

---

## Part 9: Reference Files

- `references/sop-compose-deployment.md` — step-by-step SOP for any multi-service Compose stack
- `references/sop-git-deployment.md` — deploying from Git with Dockerfile
- `references/librechat-example.md` — LibreChat: JWT secrets, MongoDB DNS, librechat.yaml mounting
- `references/signoz-example.md` — SigNoz: init containers, ClickHouse, Zookeeper migration
- `references/init-container-patterns.md` — init container patterns with heredocs and binary downloads
- `references/healthchecks.md` — healthcheck snippets for common services

---

## Quick Checklist: Adapting any docker-compose.yml for Dokploy

- [ ] **Remove all `container_name:`** — breaks Dokploy logs and metrics
- [ ] **Replace `./` relative bind mounts** with `../files/` or named volumes
- [ ] **No absolute host paths** (`/opt/...`) — they get cleaned up on deploy
- [ ] **Remove `user: "${UID}:${GID}"`** — causes permission errors in Dokploy
- [ ] **Remove `env_file: - ./.env`** — file won't exist; use `env_file: - .env` (no `./`) or `${VAR}` syntax
- [ ] **Add `env_file: - .env`** OR explicit `${VAR}` refs for every secret — env vars aren't auto-injected
- [ ] **Add healthchecks** to all database/dependency services
- [ ] **Update `depends_on`** to use `condition: service_healthy` instead of just service name
- [ ] **For domains**: use Dokploy's Domains tab (Method 1) unless you need custom Traefik config
- [ ] **Use `expose:`** (not `ports:`) for services routed via Traefik domain
- [ ] **Declare all named volumes** at the bottom of the file
