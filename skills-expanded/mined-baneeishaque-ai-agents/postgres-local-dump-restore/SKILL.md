---
name: postgres-local-dump-restore
description: Industrial protocol for validating a project's `DATABASE_URL`, bootstrapping the missing role and database on the local PostgreSQL cluster, and restoring the latest dump from a `db_dumps/` directory.
category: Database-Operations
---

# Postgres Local Dump Restore Skill (v1)

This skill standardizes the recurring developer workflow of "the app's `.env` points at a Postgres URL — make
that URL valid on my machine and load the latest production dump into it". It covers `.env` parsing, role +
database bootstrap, dump-format detection, restore execution, and post-restore verification.

***

## 1. Environment & Dependencies

The agent MUST autonomously verify the following tools before proceeding. Each tool has a documented install
command for `brew` (macOS), `apt` (Debian/Ubuntu), and `yum` (RHEL/Fedora):

| Tool         | Verify                       | Install (brew)                | Install (apt)                          | Install (yum)                          |
|--------------|------------------------------|-------------------------------|----------------------------------------|----------------------------------------|
| `psql`       | `psql --version`             | `brew install libpq`          | `sudo apt install postgresql-client`   | `sudo yum install postgresql`          |
| `pg_restore` | `pg_restore --version`       | `brew install libpq`          | `sudo apt install postgresql-client`   | `sudo yum install postgresql`          |
| `file`       | `file --version`             | preinstalled                  | preinstalled                           | preinstalled                           |

If `psql` / `pg_restore` come from `libpq` on macOS, the agent MUST verify they are on `PATH`
(`brew link --force libpq` if not).

A reachable local PostgreSQL server is REQUIRED. The agent MUST probe with:

```bash
psql -h localhost -p 5432 -d postgres -c "SELECT 1;" 2>&1 | head -3
```

If this fails with a connection refused, the agent MUST stop and ask the user to start the local cluster
(e.g., `brew services start postgresql@16`) before proceeding. **Bootstrapping a server is OUT OF SCOPE**.

***

## 2. Operational Logic

### 2.1 Discover the `DATABASE_URL`

The agent MUST locate the project `.env` in this order and stop at the first hit:

1. Path explicitly provided by the user.
2. `<repo-root>/.env`.
3. `<repo-root>/<django-project>/.env` (cookiecutter-django layout — common when the Django package sits one
   level below the repo root).
4. `<repo-root>/.envs/.local/.postgres` (cookiecutter-django split-env layout — `POSTGRES_*` vars rather than a
   single `DATABASE_URL`; see §2.1.1).

Extract the URL with:

```bash
grep -E '^(DATABASE_URL|POSTGRES_(USER|PASSWORD|DB|HOST|PORT))=' <env-file>
```

- `grep` — text search.
- `-E` — extended regex (alternation).
- `^...=` — anchor at line start; ignores commented `#DATABASE_URL=...`.

The agent MUST ignore any line whose first non-whitespace character is `#`.

A valid URL MUST match `^(postgres|postgresql)://<user>:<password>@<host>:<port>/<db>$`. If the file uses
split `POSTGRES_*` vars, synthesize the URL using:

```text
postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
```

For a local restore, the agent MUST override `POSTGRES_HOST=localhost` if the file declares a docker-compose
service name (e.g., `POSTGRES_HOST=postgres`) — the docker hostname is unreachable from the host shell.

#### 2.1.1 Multi-Match Resolution

If multiple uncommented `DATABASE_URL=` lines exist, the **last** one wins (matches the shell semantics of
`source <env>`). The agent MUST report all matches and the resolved value before proceeding.

### 2.2 Validate the URL Against the Local Cluster

```bash
PGPASSWORD=<password> psql -h <host> -p <port> -U <user> -d <db> -c "SELECT current_user, current_database();" 2>&1
```

- `PGPASSWORD=...` — non-interactive password (avoids `~/.pgpass` dependency). MUST NOT be persisted in shell
  history or logs; prefer `read -s` if running interactively.
- `-h / -p / -U / -d` — host / port / user / database from the parsed URL.
- `-c "..."` — execute one statement and exit.
- `2>&1` — merge stderr so the agent captures connection diagnostics.

Classify the result into exactly one of these states:

| State                                                              | Action                                |
|--------------------------------------------------------------------|---------------------------------------|
| `current_user \| current_database` row returned                    | Proceed to §2.4 (already valid).      |
| `FATAL: role "<user>" does not exist`                              | §2.3.2 — create role.                 |
| `FATAL: database "<db>" does not exist`                            | §2.3.3 — create database.             |
| `FATAL: password authentication failed`                            | §2.3.4 — reset password.              |
| `connection to server at "<host>" ... failed`                      | STOP — server unreachable.            |

### 2.3 Bootstrap the Missing Role / Database

#### 2.3.1 Determine a Superuser Fallback

The agent MUST discover a superuser-capable login on the local cluster. Try in order:

1. The OS user (Postgres ident-auth default on macOS / many Linux installs):

   ```bash
   psql -h localhost -p 5432 -d postgres -c "SELECT current_user;"
   ```

2. The classic `postgres` superuser:

   ```bash
   psql -h localhost -p 5432 -U postgres -d postgres -c "SELECT 1;"
   ```

The first one that returns a row is the bootstrap login. If neither works, the agent MUST stop and ask the
user for a superuser password.

#### 2.3.2 Create the Missing Role

```bash
psql -h localhost -p 5432 -d postgres <<SQL
CREATE ROLE <user> WITH LOGIN PASSWORD '<password>' CREATEDB;
SQL
```

- `CREATE ROLE ... WITH LOGIN` — make it a login role (equivalent to `CREATE USER`).
- `PASSWORD '<password>'` — exactly the password from the parsed `DATABASE_URL`.
- `CREATEDB` — required so the same role can later run `manage.py reset_db` / Django test-DB creation.

The agent MUST NOT grant `SUPERUSER` for a developer-app role.

#### 2.3.3 Create the Missing Database

```bash
psql -h localhost -p 5432 -d postgres -c "CREATE DATABASE <db> OWNER <user>;"
```

- `OWNER <user>` — keeps the dump's `--no-owner` restore consistent with the role that owns the database.

#### 2.3.4 Reset a Stale Password

```bash
psql -h localhost -p 5432 -d postgres -c "ALTER ROLE <user> WITH PASSWORD '<password>';"
```

The agent MUST re-run §2.2 after any of §2.3.x to confirm the URL now connects.

### 2.4 Discover the Latest Dump

Search recursively under each `db_dumps/` directory the user mentions, defaulting to:

1. `<repo-root>/db_dumps/`
2. `<repo-root>/../db_dumps/` (sibling of the repo, common for shared dumps)

```bash
find <db-dumps-root> -type f \( -name '*.dump' -o -name '*.sql' -o -name '*.tar' \) -print0 \
  | xargs -0 stat -f '%m %N' \
  | sort -rn \
  | head -20
```

- `-type f` — only files.
- `\( -name ... -o -name ... \)` — accept `.dump` (custom or directory format), `.sql` (plain), `.tar` (tar
  format).
- `-print0` / `xargs -0` — null-delimited to survive spaces in paths.
- `stat -f '%m %N'` — macOS BSD `stat`; on Linux use `stat -c '%Y %n'`.
- `sort -rn | head -20` — newest first; show top 20 so the agent can pick visually.

**Latest = highest mtime**, unless the user names a specific dump. The agent MUST report the chosen file
(absolute path + mtime + size) and ask the user to confirm if more than one candidate is within 24 hours of
the newest.

### 2.5 Detect the Dump Format

```bash
file <dump-path>
```

| `file` output                                                   | Format        | Restore tool   |
|-----------------------------------------------------------------|---------------|----------------|
| `PostgreSQL custom database dump`                               | custom (`-Fc`)| `pg_restore`   |
| `POSIX tar archive`                                             | tar (`-Ft`)   | `pg_restore`   |
| `ASCII text` containing `-- PostgreSQL database dump`           | plain (`-Fp`) | `psql`         |

For **directory format** (`-Fd`) the path is a directory containing `toc.dat`. The agent MUST detect with
`test -d <path> && test -f <path>/toc.dat` and treat it as a `pg_restore` input.

### 2.6 Restore

#### 2.6.1 Custom / Tar / Directory Format

```bash
PGPASSWORD=<password> pg_restore \
  -h <host> -p <port> -U <user> -d <db> \
  --no-owner --no-privileges \
  --clean --if-exists \
  -j 4 \
  <dump-path>
```

- `--no-owner` — re-assign every object to the connecting role; required because the production dump's
  owner (e.g., `acersuser`) does not exist locally.
- `--no-privileges` — strip GRANT statements that reference non-existent roles.
- `--clean --if-exists` — drop existing objects before recreating; idempotent across re-runs.
- `-j 4` — parallel restore with 4 worker jobs (custom & directory only; **invalid for plain SQL**). Tune
  to match the local CPU count; do NOT exceed the cluster's `max_connections / 2`.
- The dump path is the LAST positional argument.

Common harmless warnings the agent MUST tolerate:

- `WARNING: errors ignored on restore` when `--clean` drops objects that did not exist (ALWAYS expected on a
  fresh database).
- `role "<original-owner>" does not exist` is silenced by `--no-owner`; if it still appears, the dump used
  `SET SESSION AUTHORIZATION` instead of `ALTER ... OWNER` and MUST be restored with
  `--use-set-session-authorization` removed.

#### 2.6.2 Plain SQL Format

```bash
PGPASSWORD=<password> psql \
  -h <host> -p <port> -U <user> -d <db> \
  -v ON_ERROR_STOP=1 \
  -f <dump-path>
```

- `-v ON_ERROR_STOP=1` — abort at the first SQL error rather than silently continuing with a half-restored
  schema.
- `-f <path>` — read SQL from the file.

For plain SQL, ownership stripping is NOT automatic. If the dump contains `ALTER ... OWNER TO <prod-role>`,
the agent MUST either pre-create that role as a no-op (`CREATE ROLE <prod-role> NOLOGIN;`) or `sed`-strip the
ALTER OWNER lines. The first option is preferred — it preserves the dump unchanged.

### 2.7 Post-Restore Verification

```bash
PGPASSWORD=<password> psql -h <host> -p <port> -U <user> -d <db> -c \
  "SELECT count(*) AS tables FROM information_schema.tables WHERE table_schema='public';"
```

The agent MUST report:

1. Total table count in the `public` schema.
2. Top-5 tables by row count (sanity check the restore is non-empty):

   ```sql
   SELECT relname, n_live_tup
   FROM pg_stat_user_tables
   ORDER BY n_live_tup DESC
   LIMIT 5;
   ```

3. The Django `django_migrations` row count if the project is a Django app — confirms the dump includes
   migration state.

***

## 3. Prohibited Behaviors

- The agent MUST NOT log the `PGPASSWORD` or any value parsed from `.env` to a chat-visible artifact (commit
  messages, summaries, plan files). Show only the URL with the password masked as `***`.
- The agent MUST NOT grant `SUPERUSER` to the application role.
- The agent MUST NOT skip `--no-owner` / `--no-privileges` when restoring a production dump into a local
  developer cluster — doing so re-introduces production role names that don't exist locally.
- The agent MUST NOT delete or overwrite dumps. The skill is restore-only.
- The agent MUST NOT push or commit `.env` files, even if the user has them tracked.

***

## 4. Selection & Trade-offs

| Concern                          | Option A (Recommended)                           | Option B                                          |
|----------------------------------|--------------------------------------------------|---------------------------------------------------|
| Restore engine for `.dump`       | `pg_restore -j 4 --no-owner --no-privileges`     | `pg_restore` single-threaded — slower, no upside  |
| Drop-and-recreate                | `--clean --if-exists`                            | Drop the database manually then `CREATE DATABASE` |
| Password delivery to CLI         | `PGPASSWORD=...` env var inline                  | `~/.pgpass` (persistent — leaks across projects)  |
| Bootstrapping the missing role   | `CREATEDB` privilege (no SUPERUSER)              | `SUPERUSER` (over-privileged, security risk)      |

Option A is the documented default. Deviations require an explicit user override.

***

## 5. Real Usage Sample

Reference run (Acers backend, May 2026):

- `.env` location: `<repo-root>/acers/.env`
- Parsed URL: `postgresql://myprojectuser:***@localhost:5432/acers_20_01_2026`
- State: `FATAL: role "myprojectuser" does not exist`
- Bootstrap login: OS user (`<user>`) via ident-auth on `postgres` DB
- Created role with `CREATEDB` and matching password
- Created database `acers_20_01_2026 OWNER myprojectuser`
- Latest dump: `<repo-parent>/db_dumps/acers-production-cluster-12-05-2026-19-19-UTC/acers.dump`
  (PostgreSQL custom format)
- Restored via `pg_restore --no-owner --no-privileges --clean --if-exists -j 4`
- Verified: 80 tables in `public` schema

See [docs/conversation-log.md](docs/conversation-log.md) for the full transcript.

***

## 6. Traceability

Reference Implementation:

- [Conversation Log](docs/conversation-log.md)

This skill follows all standards defined in:

- [AI Rule Standardization Rules](../../../ai-agent-rules/ai-rule-standardization-rules.md)
- [Markdown Generation Rules](../../../ai-agent-rules/markdown-generation-rules.md)

Related skills:

- [MCP Management](../mcp-management/SKILL.md) — analogous "verify-then-bootstrap" pattern for MCP servers.
