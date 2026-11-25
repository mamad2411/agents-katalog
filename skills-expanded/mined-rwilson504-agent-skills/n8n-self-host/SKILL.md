---
name: n8n-self-host
description: Install, configure, and operate self-hosted n8n. Use when user says "self-host n8n", "install n8n with Docker", "n8n docker-compose", "n8n on Kubernetes", "n8n behind nginx/Traefik/Caddy", "configure n8n env vars", "n8n queue mode", "scale n8n workers", "n8n with Postgres", "encryption key rotation", "back up n8n", "upgrade n8n version", "n8n SSO", "n8n SSL", "WEBHOOK_URL", "EXECUTIONS_MODE", "N8N_ENCRYPTION_KEY", "n8n external secrets", "n8n binary storage to S3". Covers Docker Compose deployments (single + queue mode), env vars catalog, queue mode + workers (Redis + multiple worker processes), reverse proxy patterns, Postgres setup and migration from SQLite, encryption key handling, backup strategies, version upgrades. Do NOT use for building workflows (use n8n-build-workflow), debugging workflow logic (use n8n-debug-workflow), or community-node packaging (use n8n-create-nodes).
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["n8n", "self-hosted", "docker", "queue-mode", "postgres", "scaling", "hosting"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/n8n", "emoji": "🟧" } }
---

# n8n Self-Host

Install and operate self-hosted n8n responsibly. Most "n8n is broken in
production" tickets come from skipped Day-0 setup: wrong `WEBHOOK_URL`,
missing `N8N_ENCRYPTION_KEY`, default SQLite under load, no backup.

**References:** [DOCKER.md](references/DOCKER.md) | [ENV_VARS.md](references/ENV_VARS.md) | [QUEUE_MODE.md](references/QUEUE_MODE.md) | [REVERSE_PROXY.md](references/REVERSE_PROXY.md) | [SECURITY.md](references/SECURITY.md) | [BACKUP_UPGRADE.md](references/BACKUP_UPGRADE.md)

**Lessons:** [LESSONS_LEARNED.md](LESSONS_LEARNED.md) — read before non-trivial work.

**Authoritative docs:** <https://docs.n8n.io/hosting/>

---

## Day-0 checklist (DO NOT SKIP)

Before activating any production workflow, these are non-negotiable:

1. **Set `N8N_ENCRYPTION_KEY`** to a random 32+ character string. Without it,
   n8n generates one on first boot and writes it to disk — if that file is
   lost, ALL credentials become unrecoverable.

   ```bash
   openssl rand -hex 32
   ```

2. **Set `WEBHOOK_URL`** to the public URL where users reach the instance.
   n8n reports webhook URLs based on this env. If it doesn't match what
   callers hit, webhooks 404.

3. **Set `GENERIC_TIMEZONE`** to your team's timezone (e.g.
   `America/New_York`). Schedule Trigger uses this as the default.

4. **Use Postgres, not SQLite.** SQLite is the default but doesn't survive
   concurrent writes. Migrate before any real load.

5. **Set up a reverse proxy with HTTPS.** n8n serves plaintext by default.
   Put nginx/Traefik/Caddy in front and terminate TLS. See [REVERSE_PROXY.md](references/REVERSE_PROXY.md).

6. **Plan backups.** At minimum: the Postgres database (or SQLite file) +
   `/home/node/.n8n` config dir + binary data directory (if filesystem mode).
   See [BACKUP_UPGRADE.md](references/BACKUP_UPGRADE.md).

7. **Decide deployment mode early.** If you'll need to scale beyond ~50
   concurrent executions or have long-running workflows, plan for **queue
   mode** from the start. See [QUEUE_MODE.md](references/QUEUE_MODE.md).

---

## Minimum viable Docker setup (single instance)

```yaml
# docker-compose.yml
services:
  n8n:
    image: n8nio/n8n:latest
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      # Identity / encryption — DO NOT change after first boot
      N8N_ENCRYPTION_KEY: "${N8N_ENCRYPTION_KEY}"

      # Public URL
      N8N_HOST: n8n.example.com
      N8N_PROTOCOL: https
      WEBHOOK_URL: https://n8n.example.com/

      # Timezone
      GENERIC_TIMEZONE: America/New_York
      TZ: America/New_York

      # DB — Postgres
      DB_TYPE: postgresdb
      DB_POSTGRESDB_HOST: postgres
      DB_POSTGRESDB_PORT: 5432
      DB_POSTGRESDB_DATABASE: n8n
      DB_POSTGRESDB_USER: n8n
      DB_POSTGRESDB_PASSWORD: "${POSTGRES_PASSWORD}"

      # Reasonable defaults
      EXECUTIONS_DATA_PRUNE: "true"
      EXECUTIONS_DATA_MAX_AGE: "336"    # 14 days in hours
      N8N_METRICS: "true"
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      - postgres

  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: n8n
      POSTGRES_PASSWORD: "${POSTGRES_PASSWORD}"
      POSTGRES_DB: n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  n8n_data:
  postgres_data:
```

```bash
# .env
N8N_ENCRYPTION_KEY=<openssl rand -hex 32 output>
POSTGRES_PASSWORD=<a long random password>
```

```bash
docker compose up -d
```

Then put nginx/Traefik/Caddy in front to terminate TLS for
`n8n.example.com`. See [REVERSE_PROXY.md](references/REVERSE_PROXY.md).

---

## Queue mode — when and how

Switch to queue mode when ANY of these are true:

- More than ~50 concurrent active executions expected.
- Workflows that take >5 minutes (so the main process isn't tied up).
- Need to scale horizontally across machines.
- Need rolling restarts of workers without downtime.

Queue mode separates the main process (UI, webhooks, scheduler) from worker
processes (actual workflow execution), using Redis as a queue.

```
                 ┌──────────────┐
   Browser ─────▶│   n8n main   │──┐
   Webhook ─────▶│  (UI/API)    │  │ enqueue
                 └──────────────┘  │
                                   ▼
                              ┌────────┐
                              │ Redis  │
                              └────────┘
                                   ▲
                                   │ dequeue
                 ┌─────────────────┴────────────────┐
                 │                                  │
         ┌──────────────┐                  ┌──────────────┐
         │  n8n worker  │   ...            │  n8n worker  │
         └──────────────┘                  └──────────────┘
```

See [QUEUE_MODE.md](references/QUEUE_MODE.md) for the full Compose file
and tuning.

---

## Critical env vars (always set in production)

| Env var | Why |
|---|---|
| `N8N_ENCRYPTION_KEY` | Encrypts credentials. NEVER change after first boot |
| `WEBHOOK_URL` | Public URL n8n reports for webhooks |
| `N8N_HOST` / `N8N_PROTOCOL` / `N8N_PORT` | Internal URL components |
| `GENERIC_TIMEZONE` / `TZ` | Scheduler reference |
| `DB_TYPE=postgresdb` + `DB_POSTGRESDB_*` | Use Postgres |
| `EXECUTIONS_DATA_PRUNE=true` | Auto-clean old execution data |
| `EXECUTIONS_DATA_MAX_AGE=336` | 14 days (hours) of execution retention |
| `N8N_METRICS=true` | Prometheus metrics on `/metrics` |
| `EXECUTIONS_MODE=queue` (queue mode) | + worker process + Redis |
| `QUEUE_BULL_REDIS_*` (queue mode) | Redis connection |
| `N8N_BLOCK_ENV_ACCESS_IN_NODE=true` | Stop expressions from reading host env (security) |
| `N8N_DIAGNOSTICS_ENABLED=false` | Disable telemetry to n8n.io (if you want) |

See [ENV_VARS.md](references/ENV_VARS.md) for the full catalog.

---

## What breaks in production (most common)

| Symptom | Cause | Reference |
|---|---|---|
| All credentials disappear after restart | `N8N_ENCRYPTION_KEY` regenerated | [SECURITY.md](references/SECURITY.md#encryption-key) |
| Webhooks 404 | `WEBHOOK_URL` doesn't match what callers hit | [REVERSE_PROXY.md](references/REVERSE_PROXY.md) |
| Schedule fires at wrong wall-clock time | `GENERIC_TIMEZONE` wrong | [ENV_VARS.md](references/ENV_VARS.md) |
| "Database is locked" errors | Still on SQLite | [BACKUP_UPGRADE.md](references/BACKUP_UPGRADE.md#migrate-sqlite-to-postgres) |
| Workers don't pick up jobs | Queue mode env vars mismatched between main and workers | [QUEUE_MODE.md](references/QUEUE_MODE.md) |
| Disk fills | No execution data pruning | [ENV_VARS.md](references/ENV_VARS.md#execution-data-retention) |
| OOM on large file processing | Binary data not in filesystem/S3 mode | [SECURITY.md](references/SECURITY.md#binary-data-storage) |
| Cannot enable SSO | SSO is Enterprise-only | <https://docs.n8n.io/hosting/sso/> |

---

## Procedure (any self-host request)

1. **Identify what the user actually needs.** "Install n8n" can mean
   anything from `docker run` to a multi-node HA cluster. Ask:
   - Cloud provider / on-prem?
   - Expected concurrent executions and workflow duration?
   - HTTPS termination already handled?
   - Existing Postgres / Redis available?
   - SSO required? (Enterprise)

2. **Walk through Day-0 checklist** before any specific setup. If the user
   says "just give me Docker Compose", give them the [Minimum viable Docker
   setup](#minimum-viable-docker-setup-single-instance) above and DO call
   out the checklist items they should set.

3. **Use real values, not placeholders.** When generating env vars, run
   `openssl rand -hex 32` and put the actual output in the user's
   `.env`. Don't leave `<YOUR_KEY_HERE>` for them to forget about.

4. **Generate a single `docker-compose.yml` + `.env` + reverse-proxy snippet**
   as a copy-paste-ready bundle. Don't make the user assemble pieces.

5. **For upgrades, ALWAYS back up first.** See [BACKUP_UPGRADE.md](references/BACKUP_UPGRADE.md).
   Do not run `docker compose pull && docker compose up -d` without confirmation
   if the user is on a major version boundary.

6. **Update [LESSONS_LEARNED.md](LESSONS_LEARNED.md)** if you discovered a
   new hosting gotcha.

---

## Best practices

**Do:**
- Pin the n8n image version (`n8nio/n8n:1.78.0`) in production, not `latest`.
- Run as the non-root `node` user (the official image already does).
- Mount `/home/node/.n8n` as a named Docker volume or persistent disk —
  this contains the SQLite DB (if using SQLite), the auto-generated
  encryption key fallback, and some local config.
- Keep `N8N_ENCRYPTION_KEY` in a secrets manager. Treat losing it as
  equivalent to losing all credentials.
- Monitor `/healthz/readiness` and `/healthz` for health checks.
- Scrape `/metrics` with Prometheus for execution counts, durations,
  queue depth.
- Run periodic `EXECUTIONS_DATA_PRUNE` audits — if disk grows despite
  pruning enabled, check `EXECUTIONS_DATA_MAX_AGE` setting.
- For Kubernetes, use the official Helm chart:
  <https://github.com/n8n-io/n8n-hosting/tree/main/kubernetes>.

**Don't:**
- Don't run multiple n8n main processes against the same Postgres without
  queue mode. Schedules will fire multiple times, webhooks may double-process.
- Don't use SQLite in production. Period.
- Don't expose port 5678 directly to the internet — always behind a proxy
  with TLS.
- Don't rotate `N8N_ENCRYPTION_KEY` casually — it requires re-encrypting
  all stored credentials (n8n provides a CLI for this; do it deliberately).
- Don't skip backups because "Postgres has its own backup". You also need
  `/home/node/.n8n` (config, license file, custom nodes if installed there)
  and the binary data directory.

---

## Continuous learning

Self-hosting touches a lot of moving parts (Docker, Postgres, Redis,
reverse proxy, your environment's specifics). Every non-trivial deployment
discovers something worth capturing. After any setup, debugging session,
or upgrade, append a dated entry to [LESSONS_LEARNED.md](LESSONS_LEARNED.md).
