---
name: administration
description: n8n instance administration — data tables, folder management, community packages, Docker deployment, environment variables, backup/restore, upgrades, CLI commands, and troubleshooting. Operations the MCP does NOT cover. Auto-triggers on n8n data tables, n8n folders, move workflow, community packages, n8n setup, n8n upgrade, n8n backup, and n8n instance management tasks.
user-invokable: true
---

# n8n Administration

Operations the MCP and public API don't fully cover: data tables, folders, community packages, infrastructure, backup, CLI.

**Source: n8n-io/n8n GitHub repo, master branch.**

---

## When to Use What

| You want to... | Use | Why |
|----------------|-----|-----|
| Build/edit/validate workflows | **MCP** | Partial updates, validation, auto-fix |
| Search nodes, get node schema | **MCP** | Indexed node database with properties |
| Deploy templates | **MCP** | Auto-fix, version upgrades |
| Test/trigger workflows | **MCP** | Auto-detects trigger type |
| Manage executions | **MCP** | List, get, delete with filtering |
| Health check | **MCP** | `n8n_health_check` |
| CRUD credentials, test credentials | **See [credentials skill](../credentials/SKILL.md)** | Full credential management |
| CRUD data table rows | **Public REST API** | See section 1 below |
| CRUD data table columns, CSV import | **Internal API** | See section 1 below |
| Manage folders, move workflows | **Internal API** | Enterprise only — see section 2 |
| Install community packages | **Internal API** | See section 3 |
| Export decrypted credentials | **CLI** | `n8n export:credentials --decrypted` |
| Full database backup/restore | **CLI** | `n8n export:entities` / `import:entities` |
| Rollback database migration | **CLI** | `n8n db:revert` |
| Set encryption key, DB config | **Environment variables** | Not exposed via any API |
| Upgrade n8n version | **Docker** | Pull new image, redeploy |

**Priority: MCP → Public API → Internal API → CLI → Docker/Infra.**

---

## 1. Data Tables

n8n's built-in SQLite-backed structured storage. Each table belongs to a project.

Source: `data-table.controller.ts`, `data-table-aggregate.controller.ts`, `data-table-uploads.controller.ts`.

### Data Model

- **Table:** id (UUID), name (1-128 chars, unique per project), projectId, columns, createdAt, updatedAt
- **Column:** id, name (1-63 chars, regex `^[a-zA-Z][a-zA-Z0-9_]*$`, unique per table), type (`string` | `number` | `boolean` | `date`), index (position)
- **Row system columns** (auto-managed): id (auto-increment int), createdAt, updatedAt

### Filter Schema

Used by get rows, update rows, delete rows, upsert:

```json
{
  "type": "and",
  "filters": [
    { "columnName": "status", "condition": "eq", "value": "active" },
    { "columnName": "score", "condition": "gte", "value": 80 }
  ]
}
```

Conditions: `eq`, `neq`, `like`, `ilike`, `gt`, `gte`, `lt`, `lte`.
`like`/`ilike` auto-wraps with `%` if no wildcards in value.

### Public API (API key auth)

| Method | Path | What |
|--------|------|------|
| `GET` | `/api/v1/data-tables` | List tables. Query: `limit`, `cursor`, `filter` (JSON: `name`, `projectId`), `sortBy` |
| `POST` | `/api/v1/data-tables` | Create table. Body: `{ name, columns: [{ name, type }] }` |
| `GET` | `/api/v1/data-tables/:id` | Get table with columns |
| `PATCH` | `/api/v1/data-tables/:id` | Rename. Body: `{ name }` |
| `DELETE` | `/api/v1/data-tables/:id` | Delete table |
| `GET` | `/api/v1/data-tables/:id/rows` | Get rows. Query: `limit`, `cursor`, `filter`, `sortBy`, `search` |
| `POST` | `/api/v1/data-tables/:id/rows` | Insert rows. Body: `{ data: [...], returnType?: "count"\|"id"\|"all" }` |
| `PATCH` | `/api/v1/data-tables/:id/rows/update` | Update by filter. Body: `{ filter, data, returnData?, dryRun? }` |
| `POST` | `/api/v1/data-tables/:id/rows/upsert` | Upsert. Body: `{ filter, data, returnData?, dryRun? }` |
| `DELETE` | `/api/v1/data-tables/:id/rows/delete` | Delete by filter. Query: `filter` (**required**), `returnData`, `dryRun` |

### Internal API additions (session cookie)

Base: `/rest/projects/:projectId/data-tables`

| Method | Path | What |
|--------|------|------|
| `POST` | `/:id/columns` | Add column. Body: `{ name, type, index? }` |
| `DELETE` | `/:id/columns/:colId` | Delete column |
| `PATCH` | `/:id/columns/:colId/move` | Reorder. Body: `{ targetIndex }` |
| `PATCH` | `/:id/columns/:colId/rename` | Rename. Body: `{ name }` |
| `GET` | `/:id/download-csv` | Download CSV. Query: `includeSystemColumns` |
| `POST` | `/:id/import-csv` | Import CSV. Body: `{ fileId }` |

CSV upload (multipart): `POST /rest/data-tables/uploads` — field `file` + `hasHeaders` ("true"/"false"). Returns `{ id, rowCount, columnCount, columns }`. Use returned `id` as `fileId` in import-csv or table creation.

Global listing: `GET /rest/data-tables-global/` — all tables across projects.
Storage limits: `GET /rest/data-tables-global/limits` — total bytes, quota status.

### Data Tables Gotchas

1. **Filter mandatory for delete** — prevents accidental full deletion
2. **`dryRun: true`** available on update, upsert, delete — previews changes without persisting
3. **Column names** must match `^[a-zA-Z][a-zA-Z0-9_]*$`, max 63 chars
4. **Table names unique per project** — 409 on conflict
5. **Column CRUD is internal API only** — not in public API
6. **CSV import is two-step:** upload file → use `fileId`
7. **Public API creates tables in API key owner's personal project**
8. **Source control protected instances block all writes** (403)
9. **Dates stored as UTC ISO 8601**

---

## 2. Folder Management

Organize workflows into nested folders within projects.

Source: `folder.controller.ts`, `workflows.controller.ts`, `folder.schema.ts`.

**Enterprise-only** — all endpoints require `@Licensed('feat:folders')`.
**Internal API only** — no public API endpoints for folders.

### Folder Endpoints

Base: `/rest/projects/:projectId/folders` (session cookie auth)

| Method | Path | What |
|--------|------|------|
| `POST` | `/` | Create. Body: `{ name, parentFolderId? }` |
| `GET` | `/` | List. Query: `skip`, `take`, `sortBy`, `filter` (JSON: `parentFolderId`, `name`, `tags`) |
| `GET` | `/:id/tree` | Ancestor chain from root to this folder |
| `GET` | `/:id/content` | Recursive counts: `{ totalSubFolders, totalWorkflows }` |
| `GET` | `/:id/credentials` | Credentials used by workflows in this folder |
| `PATCH` | `/:id` | Update. Body: `{ name?, tagIds?, parentFolderId? }` — setting `parentFolderId` **moves** the folder |
| `DELETE` | `/:id` | Delete. Query: `transferToFolderId` (optional) |
| `PUT` | `/:id/transfer` | Transfer to another project. Body: `{ destinationProjectId, destinationParentFolderId, shareCredentials }` |

### Folder Name Validation

- Cannot be empty
- Cannot contain: `[ ] ^ \ / : * ? " < > |`
- Cannot consist of only dots or start with a dot
- Max 128 characters

### Moving Folders

Set `parentFolderId` in PATCH body:
- Cannot set a folder as its own parent
- Cannot move into own descendants (circular reference check)
- New parent must be in same project
- Use `PROJECT_ROOT` to move to top level (sets parentFolder to null)

### Deleting Folders — Two Modes

1. **Without `transferToFolderId`:** Flatten + archive — all workflows moved to project root, **archived and deactivated**, then folder deleted
2. **With `transferToFolderId`:** Transfer — all children moved to target folder (or `PROJECT_ROOT`), preserves workflow state, then folder deleted

### Moving Workflows Between Folders

On the workflows controller, not the folder controller:

| Operation | How |
|-----------|-----|
| Create in folder | `POST /rest/workflows/` with `parentFolderId` in body |
| Move to folder | `PATCH /rest/workflows/:id` with `parentFolderId` in body |
| Move to root | Set `parentFolderId` to `PROJECT_ROOT` or null |
| List in folder | `GET /rest/workflows/?filter={"parentFolderId":"..."}&includeFolders=true` |
| Transfer + place | `PUT /rest/workflows/:id/transfer` with `destinationParentFolderId` in body |

---

## 3. Community Packages

Source: `community-packages.controller.ts`. Internal API only, session cookie auth.

| Method | Path | What |
|--------|------|------|
| `POST` | `/community-packages` | Install. Body: `{ "name": "n8n-nodes-package-name" }` |
| `GET` | `/community-packages` | List installed |
| `PATCH` | `/community-packages` | Update. Body: `{ "name": "n8n-nodes-package-name" }` |
| `DELETE` | `/community-packages` | Uninstall. Body: `{ "name": "n8n-nodes-package-name" }` |

Packages persist in the volume at `/home/node/.n8n/nodes/`. If volume is lost, reinstall.

---

## 4. CLI Commands

Run inside the container: `docker exec -it <container> n8n <command>`.

### Backup & Export

| Command | What |
|---------|------|
| `n8n export:workflow --all --output=file.json` | Export all workflows |
| `n8n export:workflow --id=ID --output=file.json` | Export one workflow |
| `n8n export:credentials --all --decrypted --output=file.json` | Export all credentials **in plaintext** |
| `n8n export:entities --outputDir=dir/` | Full database export |

### Restore & Import

| Command | What |
|---------|------|
| `n8n import:workflow --input=file.json` | Import workflows |
| `n8n import:credentials --input=file.json` | Import credentials |
| `n8n import:entities --inputDir=dir/ --truncateTables` | Full restore (**destructive**) |

### Instance Management

| Command | What |
|---------|------|
| `n8n execute --id=ID` | Run workflow without webhook |
| `n8n update:workflow --id=ID --active=true` | Activate |
| `n8n update:workflow --all --active=false` | Deactivate all |
| `n8n list:workflow` | List all |
| `n8n delete:workflow --id=ID` | Delete |
| `n8n audit` | Security audit |
| `n8n db:revert` | Rollback last DB migration |

### User & Auth

| Command | What |
|---------|------|
| `n8n user-management:reset` | Nuclear reset to initial setup |
| `n8n mfa:disable --email=user@example.com` | Disable MFA |
| `n8n ldap:reset` | Clear LDAP config |
| `n8n license:info` | License info |
| `n8n license:clear` | Remove license |

### Worker Mode

| Command | What |
|---------|------|
| `n8n start` | Main process (editor + triggers) |
| `n8n worker --concurrency=5` | Worker (queue mode) |
| `n8n webhook` | Dedicated webhook process |

---

## 5. Docker Deployment

### PostgreSQL (production)

```yaml
version: "3.8"
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=${N8N_HOST}
      - N8N_PROTOCOL=https
      - WEBHOOK_URL=https://${N8N_HOST}/
      - N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=${DB_PASSWORD}
      - EXECUTIONS_DATA_PRUNE=true
      - EXECUTIONS_DATA_MAX_AGE=168
      - GENERIC_TIMEZONE=${TIMEZONE}
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      - postgres

  postgres:
    image: postgres:16
    restart: unless-stopped
    environment:
      - POSTGRES_DB=n8n
      - POSTGRES_USER=n8n
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  n8n_data:
  postgres_data:
```

### SQLite (simple)

```yaml
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=${N8N_HOST}
      - WEBHOOK_URL=https://${N8N_HOST}/
      - N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
      - DB_TYPE=sqlite
    volumes:
      - n8n_data:/home/node/.n8n
```

---

## 6. Key Environment Variables

### Critical

| Variable | Purpose |
|----------|---------|
| `N8N_ENCRYPTION_KEY` | Encrypts credentials. **Irreplaceable.** |
| `WEBHOOK_URL` | Full public URL. Must end with `/`. |
| `DB_TYPE` | `sqlite` or `postgresdb` |
| `GENERIC_TIMEZONE` | Default for cron triggers |

### Execution

| Variable | Default |
|----------|---------|
| `EXECUTIONS_DATA_PRUNE` | `false` |
| `EXECUTIONS_DATA_MAX_AGE` | `336` (hours) |
| `N8N_CONCURRENCY_PRODUCTION_LIMIT` | `-1` (unlimited) |
| `N8N_EXECUTIONS_MODE` | `regular` (or `queue` for Redis workers) |

### Misc

| Variable | Default |
|----------|---------|
| `N8N_LOG_LEVEL` | `info` |
| `N8N_COMMUNITY_PACKAGES_ENABLED` | `true` |
| `N8N_RUNNERS_ENABLED` | `false` |

---

## 7. Backup & Restore

### Quick Backup

```bash
docker exec n8n n8n export:workflow --all --output=/home/node/.n8n/backups/workflows.json
docker exec n8n n8n export:credentials --all --decrypted --output=/home/node/.n8n/backups/credentials.json
docker cp n8n:/home/node/.n8n/backups/ ./n8n-backup-$(date +%Y%m%d)/
```

### Database Backup

```bash
# PostgreSQL
docker exec postgres pg_dump -U n8n n8n > n8n-db-$(date +%Y%m%d).sql

# SQLite
docker cp n8n:/home/node/.n8n/database.sqlite ./n8n-db-$(date +%Y%m%d).sqlite
```

### Restore

```bash
docker exec n8n n8n import:workflow --input=/home/node/.n8n/backups/workflows.json
docker exec n8n n8n import:credentials --input=/home/node/.n8n/backups/credentials.json
# Full restore (DESTRUCTIVE):
docker exec n8n n8n import:entities --inputDir=/dir/ --truncateTables
```

---

## 8. Upgrades

```bash
docker pull docker.n8n.io/n8nio/n8n:latest
docker compose down && docker compose up -d
```

Pin version: `image: docker.n8n.io/n8nio/n8n:1.70.3`

Rollback: `docker exec n8n n8n db:revert`

---

## 9. Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Webhooks not receiving | Wrong `WEBHOOK_URL` | Set to full URL with trailing `/` |
| Credentials invalid after move | Different encryption key | Use original `N8N_ENCRYPTION_KEY` |
| Schedules not triggering | Wrong timezone | Set `GENERIC_TIMEZONE` |
| Community nodes missing | Volume not persisted | Check volume mount |
| "Workflow could not be activated" | Missing credentials | Re-link credentials |

Health: `curl -s "$N8N_URL/healthz"` or MCP `n8n_health_check`.
Debug: `N8N_LOG_LEVEL=debug` then `docker logs n8n -f --tail 100`.

---

## 10. Gotchas

1. **Encryption key is irreplaceable**
2. **`WEBHOOK_URL` must end with `/`**
3. **Test vs production webhooks** — external systems use `/webhook/`, not `/webhook-test/`
4. **Credential IDs are instance-specific** — relink after import
5. **Webhook paths must be unique** across ALL workflows
6. **Internal API requires session cookie** — not API key
7. **Folders are enterprise-only** — requires `feat:folders` license
8. **Data table column CRUD is internal API only**
