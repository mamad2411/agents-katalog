---
name: github-secrets-bulk-set
description: Industrial protocol for setting GitHub repository (or environment) secrets in bulk from a local
  .env-style secrets file using the `gh` CLI.
category: GitHub-Automation
---

# GitHub Secrets Bulk Set Skill (v1)

This skill provides the exact operational steps for populating GitHub Actions repository (or environment) secrets
from a local `.env`-style file using the `gh` CLI. It covers environment verification, naming constraints,
bulk import, and known failure modes.

***

## 1. Environment & Dependencies

The agent MUST verify the `gh` CLI is installed and authenticated before executing any secrets operation.

### 1.1 Verify Installation

```bash
which gh          # Must return a path, e.g. /usr/local/bin/gh
gh --version      # Must return gh version 2.x.x or higher
```

If `gh` is absent, defer to the **System-Wide Tool Management** skill for installation:

- macOS: `brew install gh`
- Linux: `sudo apt install gh` or `sudo dnf install gh`
- Windows: `winget install GitHub.cli`

### 1.2 Verify Authentication

```bash
gh auth status
```

Expected output includes `Logged in to github.com as <username>`. If not authenticated, run:

```bash
gh auth login
```

If authentication fails with `HTTP 401 Bad credentials` or `HTTP 403`, defer to
[Git / GitHub Auth Fallback](../git-github-auth-fallback/SKILL.md) §3.4 (`gh auth login` flow) or §3.5
(PAT validation via `GET /user`) before retrying any secret operation.

### 1.3 No-`gh` Fallback (REST API)

When `gh` is unavailable and installation via
[System-Wide Tool Management](../system-wide-tool-management/SKILL.md) is not desired, every operation in this
skill MUST be performed through the REST API per
[GitHub REST API Fallback](../github-rest-api-fallback/SKILL.md) §3 (endpoint cookbook). The two-step
`public-key` + sealed-value workflow for `PUT /repos/{owner}/{repo}/actions/secrets/{name}` is the REST
equivalent of `gh secret set`.

***

## 2. Secrets File Format

The secrets file MUST be a plain `.env`-style file: one `KEY=VALUE` pair per line.

```dotenv
DB_HOST=64.62.151.106
DB_USER=example_user
DB_PASSWORD=S3cr3t!
DB_NAME=example_db

SERVER_NAME=My_Server
```

**Rules:**

- Blank lines are silently ignored by `gh secret set --env-file`.
- Comment lines (starting with `#`) are also ignored.
- Values do NOT need quoting — the entire string after the first `=` is treated as the value.

***

## 3. GitHub API Naming Constraints (MUST READ)

GitHub enforces strict naming rules on secrets. The agent MUST check before bulk import:

- **Reserved prefix `GITHUB_`** — Secret names MUST NOT start with `GITHUB_`. API returns HTTP 422.
- **Case sensitivity** — Secret names are case-insensitive on GitHub but stored as upper-case.
- **Allowed characters** — Alphanumeric + underscore only (`[A-Z0-9_]`).
- **Max length** — 256 characters.

> [!CAUTION]
> If the secrets file contains a key starting with `GITHUB_` (e.g. `GITHUB_TOKEN`), **remove or rename it**.
> Rename to e.g. `MY_GITHUB_TOKEN` or `PAT_TOKEN` in both the secrets file and the workflow YAML before
> running the bulk import command. The built-in `${{ secrets.GITHUB_TOKEN }}` is auto-provided per workflow
> run and MUST NOT be overridden via a custom secret.

***

## 4. Operational Logic

### 4.1 Bulk Set — Repository Secrets (Standard)

```bash
gh secret set \
  --repo <OWNER>/<REPO> \
  --env-file <PATH_TO_SECRETS_FILE>
```

**Flag-by-flag breakdown:**

- **`secret set`** — Sub-command to create or update a secret (idempotent — safe to re-run).
- **`--repo`** — Target repository in `OWNER/REPO` format. Overrides the current-directory remote.
- **`--env-file`** — Path to the `.env`-style secrets file. All valid `KEY=VALUE` pairs are imported.

**Example (concrete):**

```bash
gh secret set \
  --repo sample_owner/sample_repo \
  --env-file "$HOME/sample-repo/file.secrets"
```

> [!NOTE]
> The `$HOME` expansion ensures portability across user accounts. Never hardcode an absolute path with
> a username (e.g., `/Users/X/`) in committed configs or scripts.

### 4.2 Bulk Set — Environment Secrets

If secrets are scoped to a GitHub environment (e.g. `production`):

```bash
gh secret set \
  --repo <OWNER>/<REPO> \
  --env <ENVIRONMENT_NAME> \
  --env-file <PATH_TO_SECRETS_FILE>
```

**Additional flag:**

| Flag    | Purpose                                                                               |
| ------- | ------------------------------------------------------------------------------------- |
| `--env` | Scopes secrets to a named GitHub Actions environment instead of the repository level. |

### 4.3 Single Secret (One-off)

```bash
gh secret set SECRET_NAME \
  --repo <OWNER>/<REPO> \
  --body "secret_value"
```

***

## 5. Verification

After bulk import, list the secrets to confirm all keys were written:

```bash
gh secret list --repo <OWNER>/<REPO>
```

Expected: all imported key names appear (values are never displayed by the API for security).

***

## 6. Known Failure Modes

| Error                                      | Cause                                      | Resolution                                            |
| ------------------------------------------ | ------------------------------------------ | ----------------------------------------------------- |
| `HTTP 422: Secret names must not start...` | Key starts with `GITHUB_`                  | Rename key in the secrets file and workflow YAML.     |
| `HTTP 403: Resource not accessible`        | Token lacks `secrets:write` permission     | Re-authenticate: `gh auth refresh -s write:secrets`. For deeper diagnosis (wrong identity cache, expired PAT, etc.) defer to [Git / GitHub Auth Fallback](../git-github-auth-fallback/SKILL.md) §2. |
| `gh: command not found`                    | `gh` not installed or not in `PATH`        | Install via [System-Wide Tool Management](../system-wide-tool-management/SKILL.md), OR perform the operation via [GitHub REST API Fallback](../github-rest-api-fallback/SKILL.md) §3. |
| `Could not resolve to a Repository`        | Wrong `--repo` value or typo               | Verify with `gh repo view <OWNER>/<REPO>` (or REST `GET /repos/{owner}/{repo}` per [GitHub REST API Fallback](../github-rest-api-fallback/SKILL.md) §3). |

***

## 7. Traceability

This skill was established from the following conversation session:

- **Session log**: [2026-03-23-github-secrets-bulk-set.md](../../../docs/conversations/2026-03-23-github-secrets-bulk-set.md)
- **Originating task**: Bulk-setting GitHub Actions secrets from a local `.env`-style secrets file
  using `gh secret set --env-file`.
- **Date**: 2026-03-23
