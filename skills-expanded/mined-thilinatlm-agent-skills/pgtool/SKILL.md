---
name: pgtool
description: PostgreSQL database exploration and debugging. Use when user asks to explore database schemas, tables, columns, or run queries. Requires a `.pgtool.json` file in the project directory.
---

# PostgreSQL

A CLI tool for exploring and debugging PostgreSQL databases with JSON-first output designed for AI agents.

## CLI Discovery

The CLI is located at `./pgtool-cli/` relative to this SKILL.md file.

| Platform         | Script                                     |
| ---------------- | ------------------------------------------ |
| Unix/Linux/macOS | `pgtool`                                   |
| Windows          | `pgtool.cmd` (`pgtool.ps1` also available) |

For setup instructions, see SETUP.md in this directory.

## Important

- **Always use pgtool-cli** for all database operations. Do NOT use `psql` directly.
- If pgtool-cli encounters an error or limitation, report the issue to the user and stop. Do not fall back to psql or other tools.
- Always add `LIMIT` to SELECT queries to avoid fetching excessive data.
- **Protected profiles** require human approval via a GUI dialog. If you receive a `PROTECTED_DENIED` error, ask the user to approve the connection dialog on their screen, then retry.
- **Read-only profiles** will reject write operations. Check the profile's `readOnly` flag before attempting writes.

## Global Options

```bash
pgtool <command> [OPTIONS]
```

**Options come after the command name** (citty framework requirement):

| Option | Description |
|--------|-------------|
| `-r, --root <path>` | Project root directory (default: auto-detect) |
| `--plain` | Human-readable output instead of JSON |
| `-p, --profile <name>` | Connection profile name |
| `--read-only` | Force read-only mode |
| `--allow-writes` | Override read-only profile |

```bash
# ✅ Correct — options after command
pgtool schemas -p dev
pgtool tables --profile staging --plain

# ❌ Wrong — options before command don't work
pgtool -p dev schemas
```

Profile selection priority: `--profile` flag > `PGTOOL_PROFILE` env > config `"default"` > first profile.

## Commands

### List Profiles

```bash
pgtool profiles
```

Output: `{"ok":true,"profiles":[{"name":"dev","host":"localhost","port":5432,"database":"myapp_dev","default":true,"readOnly":false,"protected":false}]}`

### List Schemas

```bash
pgtool schemas
pgtool -p staging schemas
```

Output: `{"ok":true,"schemas":[{"name":"public","owner":"postgres"}]}`

### List Tables

```bash
# Tables in default schema
pgtool tables

# Tables in a specific schema with specific profile
pgtool -p staging tables auth
```

Output: `{"ok":true,"schema":"public","tables":[{"name":"users","type":"table","rowEstimate":1000,"sizeHuman":"256 KB"}]}`

### Describe Table

Get column details with primary key and foreign key information.

```bash
pgtool describe users
pgtool describe auth.users
```

Output includes column types, nullability, defaults, PK/FK info, and foreign key references.

### List Indexes

```bash
pgtool indexes users
```

Output: `{"ok":true,"indexes":[{"name":"users_pkey","unique":true,"primary":true,"columns":["id"],"type":"btree"}]}`

### List Constraints

```bash
pgtool constraints users
```

Output includes PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, and EXCLUDE constraints.

### List Relationships

Get all foreign key relationships in a schema.

```bash
pgtool relationships
pgtool relationships auth
```

Output: `{"ok":true,"relationships":[{"fromTable":"orders","fromColumns":["user_id"],"toTable":"users","toColumns":["id"]}]}`

### Execute Query

```bash
pgtool query "SELECT * FROM users WHERE active = true LIMIT 100"
```

Output: `{"ok":true,"rows":[...],"rowCount":5,"fields":["id","name","email"]}`

**Best Practices:**

- Always add `LIMIT` to SELECT queries to avoid fetching excessive data
- DML statements (INSERT, UPDATE, DELETE) with RETURNING are fully supported
- Use parameterized values in WHERE clauses to avoid SQL injection

### Sample Table Rows

```bash
pgtool sample users
pgtool sample users --limit 10
pgtool sample auth.users
```

Output: `{"ok":true,"schema":"public","table":"users","rows":[...],"rowCount":5,"columns":["id","name","email"]}`

### Count Table Rows

```bash
pgtool count users
```

Output: `{"ok":true,"schema":"public","table":"users","count":12345}`

### Search Tables and Columns

```bash
pgtool search email
```

Output: `{"ok":true,"pattern":"email","matches":{"tables":[...],"columns":[...]}}`

### Schema Overview

```bash
pgtool overview
pgtool overview auth
```

Compact ERD-like view showing tables, primary keys, and relationships.

### Explain Query Plan

```bash
pgtool explain "SELECT * FROM users WHERE email = 'x'"
pgtool explain "SELECT * FROM users WHERE id = 1" --no-analyze
```

Output: `{"ok":true,"query":"SELECT...","plan":["Seq Scan on users..."]}`

### Daemon Management

```bash
pgtool daemon start    # Start or confirm daemon is running
pgtool daemon stop     # Gracefully stop daemon
pgtool daemon status   # Show status, uptime, active pools
```

The daemon auto-starts on the first CLI call and auto-stops after 5 minutes idle. It maintains persistent connection pools across CLI calls for faster queries.

## Error Responses

All errors return JSON with `ok: false`, an error code, and a helpful hint:

```json
{
  "ok": false,
  "error": "Configuration file not found",
  "code": "CONFIG_NOT_FOUND",
  "hint": "Create a .pgtool.json file..."
}
```

| Code | Description |
|------|-------------|
| `CONFIG_NOT_FOUND` | `.pgtool.json` not found |
| `CONFIG_INVALID` | Invalid config format or missing fields |
| `CONFIG_INSECURE` | `.pgtool.json` has insecure (writable) file permissions |
| `CONFIG_TAMPERED` | Config modified while daemon running, change rejected |
| `CONNECTION_FAILED` | Cannot connect to database |
| `QUERY_FAILED` | SQL error |
| `TABLE_NOT_FOUND` | Table does not exist |
| `SCHEMA_NOT_FOUND` | Schema does not exist |
| `PERMISSION_DENIED` | Auth failed or insufficient privileges |
| `TIMEOUT` | Query timed out |
| `READ_ONLY` | Write blocked on read-only connection |
| `PROTECTED_DENIED` | Protected profile not approved by human |

### Handling `PROTECTED_DENIED`

If you receive this error, it means the profile requires human approval. Ask the user to approve the connection — a dialog will appear on their screen. Then retry the command.

### Handling `CONFIG_INSECURE`

The `.pgtool.json` file has write permissions, which is a security risk since it contains database credentials. Ask the user to make it read-only by running `chmod 400 .pgtool.json` in their project directory, then retry.

### Handling `READ_ONLY`

The profile or `--read-only` flag prevents write operations. Use a different profile or ask the user to adjust the config.

## Common Usage Patterns

**Exploring a new database:**

1. `pgtool profiles` - See available connection profiles
2. `pgtool -p dev schemas` - See available schemas
3. `pgtool overview` - Quick view of tables and relationships
4. `pgtool tables <schema>` - List tables with sizes
5. `pgtool describe <table>` - Understand table structures
6. `pgtool sample <table>` - See example data

**Finding data:**

1. `pgtool search <pattern>` - Find tables/columns by name
2. `pgtool sample <table>` - Quick data preview
3. `pgtool count <table>` - Get exact row count
4. `pgtool query "SELECT..."` - Custom queries

**Debugging data issues:**

1. `pgtool describe <table>` - Verify column types
2. `pgtool sample <table>` - Check actual data
3. `pgtool explain "SELECT..."` - Analyze query performance
4. `pgtool indexes <table>` - Check index coverage

**Understanding relationships:**

1. `pgtool overview` - Visual relationship map
2. `pgtool relationships` - Get all FK relationships
3. `pgtool constraints <table>` - See specific table constraints

**Working with multiple environments:**

1. `pgtool profiles` - List all available profiles
2. `pgtool -p dev tables` - Explore dev database
3. `pgtool -p staging tables` - Compare with staging
4. `pgtool -p prod tables` - Access prod (will prompt for approval if protected)
