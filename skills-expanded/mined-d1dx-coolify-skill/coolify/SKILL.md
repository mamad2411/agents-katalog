---
name: coolify
description: Coolify v4 — MCP operations, service management, deployment, environment variables, Docker Compose, Traefik routing, artisan tinker for MCP gaps, project/environment organization, health monitoring, and troubleshooting. Auto-triggers on Coolify, service management, deployment, server management, Traefik routing, and project organization tasks.
disable-model-invocation: false
user-invokable: true
argument-hint: "task description"
---

# Coolify Management Skill

Complete reference for managing services on Coolify v4.

Coolify v4 (self-hosted PaaS).

---

## 1. Method Decision Tree

```
I need to list, inspect, start, stop, restart, or deploy a resource
  → MCP (coolify MCP server) — always try first

I need to move a resource between projects/environments
  → artisan tinker via SSH — MCP rejects project_uuid on update

I need to rename a service
  → artisan tinker via SSH — service update via MCP is limited

I need service or database logs (not application logs)
  → SSH into container directly — MCP only has application_logs

I need to edit docker_compose_raw on a running service safely
  → artisan tinker or UI — MCP docker_compose_raw is create-only

I need to restart Coolify itself
  → SSH: docker restart coolify (approval required)

I need UI-only operations (moveTo, clone)
  → artisan tinker preferred — Livewire internal API is not practical
```

---

## 2. MCP Operations

### What the MCP can do

| Category | Operations |
|----------|-----------|
| **Projects** | list, get, create, update, delete |
| **Environments** | list, get, create, update, delete |
| **Servers** | list, get, validate, diagnose |
| **Applications** | create (public/github/key/dockerimage), update, delete |
| **Databases** | create (postgresql/mysql/mariadb/mongodb/redis/keydb/clickhouse/dragonfly), delete |
| **Services** | create (docker-compose YAML), update, delete |
| **Control** | start, stop, restart any app, database, or service |
| **Deployments** | list, get, deploy, redeploy |
| **Env vars** | get, create, update, delete per resource; bulk update |
| **Logs** | application logs (apps only) |
| **Diagnostics** | diagnose_app, diagnose_server, find_issues, infrastructure overview |
| **Other** | server_resources, server_domains, github_apps, private_keys, teams, cloud_tokens |

### Safe operations (no approval needed)

- List/get projects, services, applications, databases
- Read environment variables
- View deployment logs
- Check health status
- Diagnostics: diagnose_server, diagnose_app, find_issues, infrastructure overview
- server_resources, server_domains

### Approval required

- Start, stop, restart any resource
- Deploy, redeploy
- Create or delete any resource
- Create, update, or delete env vars
- Any change to docker_compose_raw

### MCP gaps (cannot do via MCP)

| Gap | Workaround |
|-----|-----------|
| Move resource between projects | artisan tinker — update `environment_id` directly |
| Rename a service | artisan tinker — update `name` directly |
| Read service/database logs | SSH into container: `docker logs <container>` |
| Edit docker_compose_raw on running service | artisan tinker or UI |
| Restart Coolify itself | SSH: `docker restart coolify` (approval required) |
| Access Docker directly | SSH to server |

---

## 3. Coolify API (Direct)

Auth: `Authorization: Bearer {COOLIFY_TOKEN}`

```bash
export COOLIFY_BASE="https://coolify.yourdomain.com"
export COOLIFY_TOKEN="your-token"

# List servers
curl -s "$COOLIFY_BASE/api/v1/servers" \
  -H "Authorization: Bearer $COOLIFY_TOKEN"

# List services
curl -s "$COOLIFY_BASE/api/v1/services" \
  -H "Authorization: Bearer $COOLIFY_TOKEN"

# Get specific service
curl -s "$COOLIFY_BASE/api/v1/services/{uuid}" \
  -H "Authorization: Bearer $COOLIFY_TOKEN"

# Restart a service
curl -s -X POST "$COOLIFY_BASE/api/v1/services/{uuid}/restart" \
  -H "Authorization: Bearer $COOLIFY_TOKEN"

# Deploy/redeploy
curl -s -X POST "$COOLIFY_BASE/api/v1/services/{uuid}/deploy" \
  -H "Authorization: Bearer $COOLIFY_TOKEN"
```

---

## 4. artisan tinker via SSH (for MCP gaps)

Coolify is a Laravel app. When the MCP or API can't do something, use artisan tinker to access Eloquent models directly.

```bash
ssh <server> "docker exec coolify php artisan tinker --execute=\"...\""
```

### Key Laravel models

| Model | Key fields |
|-------|-----------|
| `App\Models\Application` | `id`, `name`, `fqdn`, `environment_id`, `status` |
| `App\Models\StandalonePostgresql` | `id`, `name`, `environment_id` |
| `App\Models\StandaloneMysql` | `id`, `name`, `environment_id` |
| `App\Models\StandaloneMariadb` | `id`, `name`, `environment_id` |
| `App\Models\StandaloneMongodb` | `id`, `name`, `environment_id` |
| `App\Models\StandaloneRedis` | `id`, `name`, `environment_id` |
| `App\Models\StandaloneKeydb` | `id`, `name`, `environment_id` |
| `App\Models\Service` | `id`, `name`, `environment_id`, `status` |
| `App\Models\Project` | `id`, `uuid`, `name` |
| `App\Models\Environment` | `id`, `name`, `project_id` |

### Common tinker operations

```bash
# Move an application to a different project
# First find the target environment_id (each project has a default "production" environment)
ssh <server> "docker exec coolify php artisan tinker --execute=\"
App\Models\Application::find(\$id)->update(['environment_id' => \$targetEnvId]);
\""

# Move a service to a different project
ssh <server> "docker exec coolify php artisan tinker --execute=\"
App\Models\Service::find(\$id)->update(['environment_id' => \$targetEnvId]);
\""

# Move a database to a different project
ssh <server> "docker exec coolify php artisan tinker --execute=\"
App\Models\StandalonePostgresql::find(\$id)->update(['environment_id' => \$targetEnvId]);
\""

# List all projects with their environment IDs
ssh <server> "docker exec coolify php artisan tinker --execute=\"
\\\$projects = App\Models\Project::all();
foreach(\\\$projects as \\\$p) {
    \\\$env = \\\$p->environments()->first();
    echo \\\$p->id . ' | ' . \\\$p->name . ' | env_id=' . \\\$env->id . PHP_EOL;
}
\""

# List all resources in an environment
ssh <server> "docker exec coolify php artisan tinker --execute=\"
App\Models\Application::where('environment_id', \$envId)->get(['id','name','fqdn','status']);
\""

# Rename a service
ssh <server> "docker exec coolify php artisan tinker --execute=\"
App\Models\Service::find(\$id)->update(['name' => 'new-name']);
\""
```

### How resource organization works

Resources belong to **Environments**, which belong to **Projects**. By default each project has one "production" environment. To move a resource between projects, update its `environment_id` to the target project's environment ID.

```
Project (id, uuid, name)
  └── Environment (id, name, project_id)
       └── Application / Service / Database (environment_id)
```

---

## 5. Livewire Internal API (browser-level)

Coolify's UI uses Laravel Livewire for real-time updates. Some operations (like `moveTo`) are only available through Livewire.

- URL: `POST https://<coolify-domain>/livewire/update`
- Requires active session cookies (XSRF-TOKEN + coolify_session)
- Each request needs a valid snapshot+checksum from the rendered page
- Session cookies expire; checksums are per-component instance
- **Not practical for automation — prefer artisan tinker for all programmatic access**

---

## 6. Service Configuration

### Docker Compose in Coolify

Coolify supports raw Docker Compose definitions. Services can be:
- **Docker Image** — pull and run a public/private image
- **Docker Compose** — full compose file with multiple containers
- **Git Repository** — build from Dockerfile in a repo

### Environment Variables

Set via Coolify UI, MCP, or API. Variables are injected into containers at runtime.

```bash
# Via API
curl -s "$COOLIFY_BASE/api/v1/services/{uuid}/envs" \
  -H "Authorization: Bearer $COOLIFY_TOKEN"

# Add/update env var
curl -s -X POST "$COOLIFY_BASE/api/v1/services/{uuid}/envs" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"key": "API_KEY", "value": "new-value", "is_build_time": false}'
```

### Domain Routing (Traefik)

1. Set domain in Coolify UI → Service → Settings → Domains
2. DNS must point to server IP — A record, proxied if using Cloudflare
3. Coolify auto-provisions SSL via Let's Encrypt (Cloudflare proxy handles edge SSL)
4. For domains behind Zero Trust: add bypass application in Terraform if webhooks need external access

---

## 7. Monitoring & Troubleshooting

### Start with diagnostics

Use MCP diagnostics tools first — they're read-only and safe:

```
infrastructure_overview   → full resource summary
find_issues               → scan for problems across all resources
diagnose_server           → server-level diagnostics
diagnose_app              → application-level diagnostics
```

### Container logs (when MCP insufficient)

```bash
# Application logs
ssh <server> "docker logs <container-name> --tail 100"

# Traefik proxy logs
ssh <server> "docker logs coolify-proxy --tail 100"

# Coolify app logs
ssh <server> "docker logs coolify --tail 100"

# All running containers
ssh <server> "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"
```

### Common issues

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| 502 Bad Gateway | Service crashed or restarting | Check application_logs, restart via MCP |
| 504 Gateway Timeout | Coolify backend overloaded (e.g., stuck health checks) | Restart Coolify: `docker restart coolify` |
| OOM Killed | Service exceeded memory limit | Increase limit or reduce load; check server_resources |
| Connection refused | Service not running | Restart via MCP |
| SSL error | Certificate expired/missing | Coolify auto-renews; check Traefik container logs |
| Slow response | Memory pressure on server | Run server_resources, identify memory hog |
| Service not reachable | Traefik label mismatch | Check service domains in Coolify, redeploy |
| `starting:unhealthy` stuck | Container runs but health check fails or isn't configured | Check health check config, or fix the app's health endpoint |

---

## 8. Deployment Patterns

### Rolling Update (default)

Coolify deploys new container, waits for health check, then stops old container. Zero-downtime if health check is configured.

### Manual Deploy

```bash
# Via API
curl -s -X POST "$COOLIFY_BASE/api/v1/services/{uuid}/deploy" \
  -H "Authorization: Bearer $COOLIFY_TOKEN"
```

### Git-Based Deploy

For services linked to a git repo:
1. Push to main branch
2. Coolify webhook triggers build
3. Dockerfile builds image
4. Deploy new container

---

## 9. Critical Gotchas

1. **Set memory limits** — always set memory limits on services to prevent OOM kills on single-server setups.
2. **Coolify UI is the source of truth** — env vars and compose config live in Coolify, not in git.
3. **Traefik labels auto-generated** — never manually set Traefik labels in compose files managed by Coolify.
4. **Let's Encrypt rate limits** — more than 5 cert requests/week for the same domain gets rate-limited.
5. **Docker volume persistence** — data persists in named volumes across deploys but NOT across server rebuilds.
6. **Back up databases** — PostgreSQL and other stateful services need scheduled `pg_dump` or equivalent.
7. **MCP can't move resources** — use artisan tinker to update `environment_id` directly.
8. **Never restart Coolify without approval** — `docker restart coolify` drops all in-flight requests.
9. **Livewire API not practical** — session cookies and per-component checksums make it unusable for automation. Use artisan tinker instead.
10. **Coolify updates** — update carefully, test in off-hours, have rollback plan.
