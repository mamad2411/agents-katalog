---
name: connect-your-data
description: Use when the user wants to get their customer data INTO Boom — connect a PostgreSQL/MySQL database, Shopify, or Skio; set up a read-only sync user; reach a database behind a VPC/bastion via SSH tunnel; write the sync SQL mapping; or decide between DB sync, CSV upload, and the API. Triggers on "connect our database", "sync customers", "conectar la base de datos", "SSH tunnel", "bastion", "Shopify integration", "keep segments fresh".
---

# Connect Your Data

Boom's CDP (persons, custom objects, events) is what segments filter over — fresh data means accurate audiences. There are three routes in; pick by cadence:

| Route | When | Where |
|---|---|---|
| **Database / Shopify / Skio sync** | Data lives in your systems and changes continuously | Boom app → sidebar **Integrations** → **Directory** tab (UI-only; **not on the MCP**) |
| **API / MCP writes** | You push from your own backend or an agent | `cdp_people_*`, `cdp_custom_objects_*`, `cdp_events_*` tools |
| **CSV upload** | One-shot list for a single initiative | Boom app, or `initiatives_participants_add` with per-person `context` |

## Tools used

| Tool | Purpose | Scope |
|---|---|---|
| `cdp_people_upsert` / `cdp_people_batch_upsert` | Push persons from an agent/backend | write |
| `cdp_custom_object_types_list` / `cdp_custom_object_types_create` | Inspect/register object types before syncing | read / write |
| `cdp_events_record` / `cdp_events_batch_record` | Push events (single = real-time, can trigger journey enrollment; batch = bulk backfill, does **not** trigger) | write |
| `cdp_relationship_types_register` / `cdp_relationships_batch` | Register + link person↔object relationships | write |
| `segments_catalog` | Verify synced attributes are filterable | read |

Database connections themselves are configured in the Boom app — this skill prepares everything the user pastes into that UI.

## Step 1 — least-privilege read-only user

Boom only ever `SELECT`s. Have the customer's DBA run:

```sql
-- PostgreSQL
CREATE USER boom_readonly WITH PASSWORD 'your-strong-password';
GRANT CONNECT ON DATABASE your_db_name TO boom_readonly;
GRANT USAGE ON SCHEMA public TO boom_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO boom_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO boom_readonly;
```

```sql
-- MySQL
CREATE USER 'boom_readonly'@'%' IDENTIFIED BY 'your-strong-password';
GRANT SELECT ON your_db_name.* TO 'boom_readonly'@'%';
```

Tighter is better: grant per-table if the DB holds data Boom doesn't need.

## Step 2 — direct or SSH tunnel?

- **DIRECT** — the DB has a public endpoint (managed Postgres/MySQL with SSL). Form needs host, port, database, user, password; SSL is required. Private/loopback IPs are blocked by design (SSRF protection) — a "host not allowed" error on a private IP means you need the tunnel.
- **SSH_TUNNEL** — the DB lives in a VPC and is only reachable through a bastion. Extra fields: bastion host/port/username + a **dedicated SSH private key** (generate fresh: `ssh-keygen -t ed25519 -f boom-bastion -C boom-sync`; give Boom the private key, put the `.pub` on the bastion; least-privilege: a user that can only port-forward). On first connect Boom shows the bastion's host-key fingerprint — **pin it** so a swapped bastion is refused later.

Click **Save** — it tests the connection as it saves (reachability, TLS, credentials) and lands on the connection page with **Active** or **Error** plus a normalized message (auth vs network vs TLS). Fix with **Edit**, retest with **Test connection** there. There is no SSL setting: every connection uses TLS `Require`.

## Step 3 — the sync mapping (the technical part)

Saving a connection does not create its sync: Boom switches syncing on for it (ask Boom if nothing shows under **Integrations → Syncs**). Then open the sync, **+ Add data**, and walk the four steps: **What it becomes** (People / Objects / Link) → **Choose a table** → **Query & mapping** (**Run preview**, **Create sync**) → **Preview & go live** (**Go live**; **Pause** stops it).

Each synced resource is a SQL query over the customer's schema honoring this contract:

| Column | Required | Meaning |
|---|---|---|
| `external_id` | yes | Stable unique id in *their* system (cast to text) — identity is `(org, external_id)` |
| `source_updated_at` | yes | Cursor column — sync is incremental (`WHERE updated_at > $cursor`); must move on every change |
| `source_deleted` | recommended | Boolean soft-delete flag (`deleted_at IS NOT NULL`) so removals propagate |
| everything else | — | Mapped to person fields (`personFieldMap`: email, phone, name…) or object attributes |

Example — persons from a `users` table:

```sql
SELECT
  u.id::text            AS external_id,
  u.email               AS email,
  u.phone_e164          AS phone,
  u.full_name           AS name,
  u.plan                AS plan,           -- becomes a filterable attribute
  (u.deleted_at IS NOT NULL) AS source_deleted,
  u.updated_at          AS source_updated_at
FROM users u
```

Relationships (e.g. order↔product) add `left_external_id` / `right_external_id` for the two sides. Model non-person entities (orders, subscriptions, policies) as **custom object types** and relate them to persons — that's what powers segments like "personas con una orden > $500 en 30 días".

**Authoring tips:** phone must land as E.164 (`+521…`) — transform in SQL if stored bare; keep attribute names snake_case and stable (renaming creates a new attribute); exclude columns Boom doesn't need (PII minimization); ensure an index on the cursor column so incremental pulls stay cheap.

## Shopify / Skio

**Skio**: **Integrations → Directory → Skio** (Shopify domain + Skio API key → **Connect Skio**). **Shopify** is not in the Directory: Boom sends the store an install link. Neither needs a SQL contract; customers, orders, and subscriptions map automatically. Use these over a DB connection when the store *is* the system of record.

## Verify the sync

1. Status shows **ACTIVE** with a recent last-synced time (PENDING_AUTH/ERROR/REAUTH_REQUIRED all name the problem).
2. `segments_catalog` lists the new attributes; spot-check one person with `cdp_people_get`.
3. Build a test segment (`segments_preview`) and compare its count against a known number from the source DB.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| "Host not allowed" on test | Private/loopback IP with DIRECT mode | Use SSH_TUNNEL through a public bastion |
| `HOST_KEY_MISMATCH` | Bastion host key changed since pinning | Confirm with the infra owner it was intentional, then re-pin |
| Sync ACTIVE but people missing | Cursor column doesn't move on update, or rows soft-deleted upstream without `source_deleted` | Fix the query contract |
| Duplicated people | `external_id` not stable (e.g. email used as id) | Use the immutable PK, cast to text |
| Segment counts drift from source | Replica/sync lag or timezone mismatch in cursor | Compare with lag tolerance; store cursors in UTC |

See [`CONTEXT.md`](../../CONTEXT.md) for the domain model. Building audiences on top: `cdp-and-segments`.
