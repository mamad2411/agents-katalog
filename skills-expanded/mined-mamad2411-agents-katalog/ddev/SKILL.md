---
name: ddev
description: >
  General DDEV environment management for any project type: start, stop, configure, import
  databases, isolate worktrees, troubleshoot containers. For Drupal tooling inside DDEV
  (drush, phpcs, phpstan, phpunit) use drupal-lab:ddev.
allowed-tools: Bash, Read, Glob, Grep
---

# lib:ddev

## When to use

Full routing detail, kept out of the always-loaded skill listing:

> General-purpose DDEV development environment management across all project types (WordPress, Drupal, Laravel, generic PHP). Use when starting, stopping, diagnosing, or configuring DDEV environments, importing databases, managing worktree isolation, or troubleshooting container issues. Trigger phrases: "ddev start", "ddev import", "ddev status", "start ddev", "import database", "ddev troubleshoot", "ddev config", "set up ddev", "ddev worktree", "ddev pull", "configure ddev". Do NOT use for Drupal-specific DDEV commands (phpcs, phpstan, phpunit, drush) -- use drupal-lab:ddev for those.

General DDEV knowledge for any project type. CMS-specific skills (drupal-lab:ddev) extend this with framework-specific commands.

## Resources in this skill

- `references/providers.md` -- provider YAML patterns (direct mysqldump, SSH tunnel, Rackspace Cloud DB); read when creating or debugging a `ddev pull` provider
- `references/troubleshooting.md` -- container log patterns, Mutagen issues, port conflicts, error table; read when diagnosing a DDEV problem

## Pre-flight

```bash
ddev version 2>/dev/null || echo "NOT INSTALLED"
```

Install: https://ddev.readthedocs.io/en/stable/users/install/

## Project naming and URLs

DDEV generates URLs as `<name>.<project_tld>`.

- `name` defaults to the folder name if omitted from `config.yaml`
- `project_tld` defaults to `ddev.site`

### Multi-project worktree convention

When working across multiple projects with worktrees, folder names like `main` collide across projects. Use `project_tld` to namespace by project:

```yaml
# .ddev/config.yaml (checked in, shared by all worktrees)
project_tld: kellogg.ddev.site
```

DDEV uses the folder name as the subdomain automatically:

| Worktree folder | URL |
|---|---|
| `main` | `main.kellogg.ddev.site` |
| `sprint-2026.4.1` | `sprint-2026-4-1.kellogg.ddev.site` |
| `KDRRCPS-44` | `kdrrcps-44.kellogg.ddev.site` |

This works because `*.ddev.site` has wildcard DNS at any subdomain depth. Any `<x>.<y>.ddev.site` resolves to 127.0.0.1.

**Only use suffixes ending in `.ddev.site`.** Custom TLDs require local DNS configuration and break zero-config resolution.

### When you still need `name` in config.local.yaml

Override the name only when the folder name produces collisions or is unsuitable:

```yaml
# .ddev/config.local.yaml (gitignored, per-worktree)
name: kellogg-sprint
```

Prefer letting the folder name drive the project name.

## Lifecycle

```bash
ddev start              # start this project
ddev stop               # stop this project
ddev stop --all         # stop all projects (frees Docker resources)
ddev restart            # restart and re-trigger hooks
ddev list               # all projects on this machine
ddev status             # human-readable status
ddev describe --json    # machine-readable (pipe to jq)
```

Use `ddev restart` when:
- `.ddev/config.yaml` or `config.local.yaml` changed
- Post-start hooks need to re-run
- Container state seems stale

## Database operations

### Import

```bash
ddev import-db --file=path/to/db.sql.gz
```

Auto-detects `.sql`, `.sql.gz`, `.tar.gz`. For WordPress, DDEV rewrites `siteurl`/`home` to the DDEV URL automatically.

### Export

```bash
ddev export-db --file=/tmp/db-export.sql.gz --gzip
```

### Direct query

```bash
ddev mysql -e "SHOW TABLES;"
ddev mysql -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'db';"
```

### Snapshot (fast local backup/restore)

```bash
ddev snapshot --name=before-migration
ddev snapshot restore before-migration
ddev snapshot --list
```

Snapshots are filesystem-level copies -- instant. Use before risky imports or migrations.

## Executing commands

```bash
ddev exec <command>         # web container
ddev exec -s db <command>   # db container
ddev ssh                    # interactive shell (web)
ddev ssh -s db              # interactive shell (db)
```

### CMS CLIs

```bash
ddev wp <command>           # WordPress (wp-cli)
ddev drush <command>        # Drupal
ddev artisan <command>      # Laravel
ddev composer <command>     # all project types
```

## Worktree isolation

Each worktree gets its own DDEV instance. Key files:

| File | In git? | Purpose |
|---|---|---|
| `.ddev/config.yaml` | Yes | Shared config (type, PHP, project_tld) |
| `.ddev/config.local.yaml` | No | Per-worktree overrides (name, credentials) |
| `.ddev/config.*.yaml` | Varies | Feature config fragments (merged alphabetically) |

### Concurrent instance limits

Rule of thumb: **max 3 concurrent DDEV projects** on a standard dev machine. Stop idle projects.

```bash
ddev list          # what's running?
ddev stop --all    # stop everything
```

## Providers (ddev pull)

Providers define how `ddev pull <name>` fetches databases and files. Files live in `.ddev/providers/<name>.yaml`.

Read `references/providers.md` before creating or debugging a provider.

Quick usage:

```bash
ddev auth ssh          # forward SSH keys into container (once per session)
ddev pull <provider>   # pull DB and files
```

## WordPress table prefix

DDEV generates `wp-config-ddev.php` with `wp_` as default prefix. Override via a post-start hook:

```yaml
# .ddev/config.wordpress-table-prefix.yaml
hooks:
  post-start:
    - exec: >
        sed -i.bak "s/\$table_prefix = 'wp_';/\$table_prefix = getenv('WORDPRESS_TABLE_PREFIX') ?: 'wp_';/"
        /var/www/html/web/wp-config-ddev.php
```

Set the prefix in `web_environment`:

```yaml
web_environment:
  - WORDPRESS_TABLE_PREFIX=emasy_
```

After importing a DB with a non-standard prefix, `ddev restart` to re-trigger the hook.

## Quick diagnostics

When something isn't working, run these in order:

1. **Is it running?** `ddev status`
2. **What do logs say?** `ddev logs` (web) or `ddev logs -s db` (database)
3. **Sync issues?** `ddev utility mutagen-diagnose`
4. **Port conflict?** `ddev debug router-ports`
5. **Nuclear reset:** `ddev poweroff && ddev start`

Read `references/troubleshooting.md` for the full error table and log patterns.
