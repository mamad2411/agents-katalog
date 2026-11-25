---
name: magento2-warden
description: >
  Warden environment operations for Magento 2: database queries, Magento CLI
  commands, DB import/export, environment management, and shell access.
  Use when user asks to "run warden", "check database", "warden db connect",
  "run magento command", "import db", "export db", "warden shell", or any
  task involving the Warden local development environment.
  Do NOT use for code generation, frontend, or non-Warden environments.
metadata:
  author: tuanhaviet22
  version: 1.0.0
  tags: [magento2, warden, database, cli, devops]
  compatibility: Magento 2.4+, Warden 0.13+
---

# magento2-warden

Warden environment toolkit for Magento 2 — database access, CLI execution, DB import/export, and environment management.

---

## Critical Rules

- NEVER run `bin/magento` directly — always via `warden env exec php-fpm bin/magento`
- NEVER delete cache folders manually (`rm -rf var/cache`) — use `bin/magento cache:flush` via warden
- NEVER run raw SQL mutations (`UPDATE`, `DELETE`, `DROP`) without explicit user confirmation
- Always quote SQL in `warden db connect` with `-e "..."` flag
- Always use `-A` flag with `warden db connect` to disable auto-rehash (faster for large schemas)

---

## Feature 1: Database Queries

Use `warden db connect` to run SQL queries non-interactively.

```bash
# Show all databases
warden db connect -A -e "SHOW DATABASES;"

# Show all tables in the current database
warden db connect -A -e "SHOW TABLES;"

# Describe a table structure
warden db connect -A -e "DESCRIBE catalog_product_entity;"

# Select with filter
warden db connect -A -e "SELECT * FROM core_config_data WHERE path LIKE '%base_url%';"

# Count rows
warden db connect -A -e "SELECT COUNT(*) FROM catalog_product_entity;"
```

**Notes:**
- `-A` disables auto-rehash (faster startup for large schemas)
- Always use `-e "..."` for non-interactive queries
- For multi-line queries, use a `.sql` file: `warden db connect -A < query.sql`

---

## Feature 2: Magento CLI via Warden

Always use `warden env exec php-fpm` to run `bin/magento` commands inside the container.

```bash
# Cache operations
warden env exec php-fpm bin/magento cache:flush
warden env exec php-fpm bin/magento cache:clean

# Indexer operations
warden env exec php-fpm bin/magento indexer:reindex
warden env exec php-fpm bin/magento indexer:status

# Setup / upgrade
warden env exec php-fpm bin/magento setup:upgrade
warden env exec php-fpm bin/magento setup:di:compile
warden env exec php-fpm bin/magento setup:static-content:deploy -f

# Module management
warden env exec php-fpm bin/magento module:enable {Vendor}_{Module}
warden env exec php-fpm bin/magento module:disable {Vendor}_{Module}
warden env exec php-fpm bin/magento module:status

# Deploy mode
warden env exec php-fpm bin/magento deploy:mode:set developer
warden env exec php-fpm bin/magento deploy:mode:show

# Cron
warden env exec php-fpm bin/magento cron:run
```

---

## Feature 3: DB Import / Export

```bash
# Import a SQL dump into the Warden database
warden db import < dump.sql

# Export full database to a SQL file
warden db export > dump.sql

# Export a single table
warden db dump tablename > tablename.sql

# Export with gzip compression
warden db export | gzip > dump.sql.gz

# Import from gzip
gunzip -c dump.sql.gz | warden db import
```

**Notes:**
- `warden db import` / `warden db export` use the database defined in `.env` (`DB_DATABASE`)
- For large dumps, pipe through `pv` to monitor progress: `pv dump.sql | warden db import`

---

## Feature 4: Environment Management

```bash
# Start the Warden environment
warden env up

# Stop the Warden environment
warden env down

# Restart all containers
warden env restart

# Show running services and their ports
warden env ps

# Open an interactive shell in the php-fpm container
warden shell

# Open a shell as root
warden shell --user root

# View container logs
warden env logs php-fpm
warden env logs -f php-fpm   # follow/tail logs

# Rebuild containers (after docker-compose changes)
warden env up --build
```

---

## Feature 5: Common Magento Diagnostics (via warden db connect)

Ready-to-use queries for common diagnostic tasks.

### Check Base URLs
```bash
warden db connect -A -e "SELECT scope, scope_id, path, value FROM core_config_data WHERE path LIKE '%base_url%' ORDER BY scope, scope_id;"
```

### Find Config Values by Path
```bash
warden db connect -A -e "SELECT scope, scope_id, path, value FROM core_config_data WHERE path LIKE '%{search_term}%';"
```

### Check Cron Job Status
```bash
warden db connect -A -e "SELECT job_code, status, scheduled_at, executed_at, finished_at, messages FROM cron_schedule ORDER BY scheduled_at DESC LIMIT 20;"

# Show only failed cron jobs
warden db connect -A -e "SELECT job_code, status, messages, scheduled_at FROM cron_schedule WHERE status = 'error' ORDER BY scheduled_at DESC LIMIT 20;"
```

### Check Admin Users
```bash
warden db connect -A -e "SELECT user_id, username, email, is_active, created FROM admin_user ORDER BY created DESC;"
```

### Inspect Module Status
```bash
warden db connect -A -e "SELECT module, schema_version FROM setup_module ORDER BY module;"

# Check a specific module
warden db connect -A -e "SELECT * FROM setup_module WHERE module LIKE '%{Vendor}%';"
```

### Check Store Configuration
```bash
warden db connect -A -e "SELECT store_id, code, name, is_active FROM store ORDER BY store_id;"
warden db connect -A -e "SELECT website_id, code, name, is_default FROM store_website ORDER BY website_id;"
```

### Find Products by SKU
```bash
warden db connect -A -e "SELECT entity_id, sku, type_id, created_at FROM catalog_product_entity WHERE sku LIKE '%{sku}%' LIMIT 20;"
```

### Check Recent Orders
```bash
warden db connect -A -e "SELECT entity_id, increment_id, status, grand_total, created_at FROM sales_order ORDER BY created_at DESC LIMIT 10;"
```

### Check Customer Count
```bash
warden db connect -A -e "SELECT COUNT(*) AS total_customers FROM customer_entity;"
```

---

## Workflow

When the user asks a Warden-related question:

1. **Identify the task type**: DB query, CLI command, import/export, environment, or diagnostics
2. **Select the appropriate command pattern** from the features above
3. **Replace placeholders** (`{Vendor}`, `{Module}`, `{search_term}`, etc.) with user-provided values
4. **Confirm before running mutations**: For any `UPDATE`, `DELETE`, `DROP`, or `INSERT`, show the command and ask for confirmation first
5. **Show output interpretation**: For diagnostic queries, explain what the results mean

---

## Common Pitfalls

| Wrong | Correct |
|-------|---------|
| `bin/magento cache:flush` | `warden env exec php-fpm bin/magento cache:flush` |
| `mysql -u root -p` | `warden db connect -A` |
| `warden db connect -e SELECT ...` | `warden db connect -A -e "SELECT ...;"` |
| `rm -rf var/cache` | `warden env exec php-fpm bin/magento cache:flush` |
| `docker exec -it ...` | `warden shell` or `warden env exec php-fpm ...` |
