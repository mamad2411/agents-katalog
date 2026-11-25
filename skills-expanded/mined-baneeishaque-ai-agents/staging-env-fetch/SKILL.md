---
name: staging-env-fetch
description: >
  Fetch the .env file from a staging server via the ssh-staging MCP tool and place it in the correct local path. Use
    when a local dev server fails to start with a missing env var error, or when onboarding a developer who needs a
    baseline local .env.
category: Database-Operations
---

# Staging Env Fetch Skill (v1)

Fetches the `.env` file from a staging server via the `ssh-staging-exec` MCP tool and
writes it to the correct local path so the development server can start.

## When to Use

- `python manage.py runserver` (Django) or equivalent dev server fails with
  `ImproperlyConfigured` / missing environment variable errors
- Local `.env` file is missing
- Developer needs a baseline local environment file from staging
- Onboarding a new dev who does not yet have a `.env`

## Prerequisites

- The `ssh-staging-exec` MCP server must be configured and connected to the staging host.
  This MCP tool comes from the public [`ssh-mcp`](https://www.npmjs.com/package/ssh-mcp) npm
  package (`npx -y ssh-mcp`). The MCP server key is `ssh-staging`; the tool name exposed to
  agents is `ssh-staging-exec`.
- Git repository must be cloned locally.

## Procedure

### Step 1 — Discover the Deployment Path via CI/CD Workflows

Read the local workflow files first to confirm the exact remote project directory.

```bash
find . -path "*/.github/workflows/*.yml" -exec cat {} \;
```

Look for the `cd` command in the deploy script. It reveals the server-side project root
and the application subdirectory. The `.env` lives in the application subdirectory.

### Step 2 — Locate the `.env` on the Staging Server

```text
ssh-staging-exec: find / -name ".env" -not -path "*/proc/*" -not -path "*/sys/*" 2>/dev/null | head -20
```

Cross-reference results with the path from Step 1. Ignore dated-backup directories
such as `<repo>-<DD-MM-YY>/` — they are stale snapshots.

### Step 3 — Read the Remote `.env`

```text
ssh-staging-exec: cat <deploy-root>/<app-dir>/.env
```

### Step 4 — Write the Local `.env`

The local target path mirrors the remote path inside the cloned repo
(e.g., `<repo-root>/<app>/.env`). Copy the content verbatim.

If the file already exists locally, ask the user before overwriting.

### Step 5 — Verify `.gitignore` Coverage

```bash
grep -E "(^|/)\.env$" .gitignore */.gitignore 2>/dev/null
```

If `.env` is not listed, add it to prevent accidental credential commits.

### Step 6 — Adapt DATABASE_URL for Local Use (Advisory Only)

The staging `.env` typically points `DATABASE_URL` at the server's local PostgreSQL
instance. Inform the user:

> The `DATABASE_URL` in the fetched `.env` targets the staging database. For local
> development, change it to `sqlite:///db.sqlite3` or point it at your local Postgres
> instance.

Do NOT silently rewrite the `DATABASE_URL` — preserve the staging value and leave the
choice to the developer.

## Related Skills

- [`env-example-creation`](../../env-example-creation/SKILL.md) — After fetching the
  `.env`, use this complementary skill to sanitize it into a `.env.example`
  with placeholders, so the template can be safely committed
- [`pg-cluster-backup-compare`](../pg-cluster-backup-compare/SKILL.md) — companion for
  PostgreSQL cluster backup and comparison workflows
- [`pg-cluster-mirror`](../pg-cluster-mirror/SKILL.md) — companion for restoring cluster
  dumps onto target environments

## Security Reminders

- Never log or echo SSH credentials (passwords, private keys) in chat output.
- Never commit `.env` to version control.
- If the SSH password was shared in chat, remind the user to rotate it immediately.
- The fetched file may contain database credentials, secret keys, and API tokens.

## Anti-Patterns

- Guessing the remote path without consulting `.github/workflows/` first.
- Copying a stale `.env` from a dated-backup directory instead of the active deployment dir.
- Rewriting `DATABASE_URL` or other values during the fetch.
- Asking the user to SSH manually when the `ssh-staging-exec` MCP tool is available.
