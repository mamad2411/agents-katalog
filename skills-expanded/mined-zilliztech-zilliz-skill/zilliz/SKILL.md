---
name: zilliz
description: >
  Manage Zilliz Cloud vector databases via zilliz-cli.
  Use when the user wants to: (1) set up zilliz-cli (install, login, configure),
  (2) manage clusters (create, list, describe, suspend, resume, delete, modify),
  (3) manage collections, indexes, partitions, databases, or aliases,
  (4) perform vector operations (search, query, insert, upsert, delete, hybrid search),
  (5) manage database users, roles, and RBAC privileges, or cloud-level access
      control (org/project roles, member and group grants),
  (6) handle backups, imports, volumes, storage integrations, billing,
      monitoring, projects, regions, or async jobs.
  Triggers on: zilliz, vector database, semantic search, RAG, embeddings,
  collection schema, vector index, similarity search, zilliz-cli.
---

# Zilliz Cloud CLI Skill

Operate Zilliz Cloud through `zilliz-cli`. All operations are executed via shell commands.

## Prerequisite Check (always run first)

Before any operation, verify in order:

```bash
# 1. Install or update the CLI
curl -fsSL https://raw.githubusercontent.com/zilliztech/zilliz-cli/master/install.sh | bash

# 2. Logged in? If not: guide user to login in their terminal
zilliz auth status

# 3. Context set? (only for data-plane ops)
zilliz context current
```

**CRITICAL:** `zilliz login`, `zilliz configure`, and `zilliz auth switch` require interactive input — NEVER run them in a non-interactive shell. Instruct the user to run in their own terminal. NEVER ask for API keys in chat.

## Command Pattern

```
zilliz <resource> <action> --flag <value> [--optional-flag <value>]
```

All commands support `--output json|table|text` (default: `text`). Use `--output json` for programmatic parsing.

## Cluster Type Capabilities

| Feature                      | Free | Serverless | Dedicated |
| ---------------------------- | ---- | ---------- | --------- |
| Collection CRUD & Vector ops | Yes  | Yes        | Yes       |
| Database create/drop         | No   | No         | Yes       |
| User/role management         | No   | Limited    | Yes       |
| Backup management            | No   | Yes        | Yes       |
| Cluster modify (CU/replica)  | No   | No         | Yes       |

Check cluster type first when a command fails with permission errors.

## Reference Files

Each reference covers one resource domain with full command syntax, options, and guidance. Read the relevant reference when handling that domain:

| Domain             | Reference                                                    | When to read                                                       |
| ------------------ | ------------------------------------------------------------ | ------------------------------------------------------------------ |
| Setup & auth       | [references/setup.md](references/setup.md)                   | Install, login, context, config, troubleshooting                   |
| Clusters           | [references/cluster.md](references/cluster.md)               | Create, list, describe, modify, suspend, resume, delete clusters; create Vector Lake |
| On-demand clusters | [references/on-demand-cluster.md](references/on-demand-cluster.md) | Create, list, describe, delete on-demand (Vector Lake) clusters with auto-suspend TTL |
| Collections        | [references/collection.md](references/collection.md)         | Create, list, describe, drop, rename, load, release, aliases, per-collection metrics |
| External collections | [references/external-collection.md](references/external-collection.md) | Trigger, describe, list refresh jobs for Vector Lake-backed collections |
| Vectors            | [references/vector.md](references/vector.md)                 | Search, query, insert, upsert, get, delete, hybrid search, filters |
| Indexes            | [references/index.md](references/index.md)                   | Create, list, describe, drop indexes                               |
| Databases          | [references/database.md](references/database.md)             | Create, list, describe, drop databases                             |
| Partitions         | [references/partition.md](references/partition.md)           | Create, list, load, release, drop partitions                       |
| Users & roles      | [references/user-role.md](references/user-role.md)           | RBAC: users, roles, privileges (Dedicated only)                    |
| Access control     | [references/acl.md](references/acl.md)                       | Cloud-level RBAC: custom org/project roles, policies, member and SCIM group grants |
| Backups            | [references/backup.md](references/backup.md)                 | Create, restore, export backups; manage backup policies            |
| Import             | [references/import.md](references/import.md)                 | Bulk data import from object storage or files uploaded to a volume |
| Billing            | [references/billing.md](references/billing.md)               | Usage queries, invoices, payment methods                           |
| Monitoring         | [references/monitoring.md](references/monitoring.md)         | Cluster status, collection stats, load states, cluster and per-collection time-series metrics |
| Projects & regions | [references/project-region.md](references/project-region.md) | Create, list, describe, delete, upgrade projects; bind regions     |
| Volumes            | [references/volume.md](references/volume.md)                 | Create, list, describe, delete volumes; upload local files for import |
| Storage integrations | [references/storage-integration.md](references/storage-integration.md) | Connect your own S3 / Azure Blob / GCS bucket: auth policy, validate, manage |
| PrivateLink        | [references/privatelink.md](references/privatelink.md)       | Endpoint services, project endpoints, whitelist management         |
| Jobs               | [references/job.md](references/job.md)                       | Track async job status, wait for completion                        |
| Diagnose           | [references/diagnose.md](references/diagnose.md)             | Read-only health diagnosis for clusters and collections (slow, stuck, errors, quota) |

## Quick-Start Workflow

For new users, guide through setup in order:

1. Install CLI: `curl -fsSL https://raw.githubusercontent.com/zilliztech/zilliz-cli/master/install.sh | bash`
2. Authenticate: user runs `zilliz login` in their terminal
3. Verify: `zilliz auth status`
4. List clusters: `zilliz cluster list`
5. Set context: `zilliz context set --cluster-id <id>`
6. Verify: `zilliz context current && zilliz collection list`

## Common Workflows

**Create collection and prepare for search:**

1. `zilliz collection create --name <name> --dimension <dim>` — create
2. `zilliz index create --collection <name>` — index (AUTOINDEX recommended)
3. `zilliz collection load --name <name>` — load into memory
4. `zilliz vector search --collection <name> --data '[[...]]'` — search

**Status overview** (read [references/monitoring.md](references/monitoring.md)):

1. `zilliz context current --output json`
2. `zilliz cluster describe --cluster-id <id> --output json`
3. `zilliz database list --output json`
4. For each DB: `collection list`, `get-stats`, `get-load-state`, `index list`
5. Present as formatted table

## Async Operations

These return immediately with a `jobId`; track with `job describe` (see [references/job.md](references/job.md)):

| Operation                        | Poll command                                       |
| -------------------------------- | -------------------------------------------------- |
| `cluster create`                 | `cluster describe --cluster-id <id>` until RUNNING |
| `backup create/export/restore-*` | `job describe --job-id <jid>` or `backup describe` |
| `import start`                   | `job describe --job-id <jid>`                      |
| Any async op with jobId          | `job describe --job-id <jid> --wait`               |

## Safety Rules

- **Confirm before destructive ops:** drop collection/database, delete cluster/backup/volume/storage integration, drop user/role
- **Sensitive commands in user's terminal:** `zilliz login`, `zilliz configure`, `zilliz billing bind-card`
- **Never expose credentials** in chat or command output
