---
name: envshed
description: "Guide for using the envshed CLI — a secrets management tool for managing environment variables across projects, workspaces, and environments. Use when the user asks about env vars, secrets, .env files, envshed commands, or needs help with environment configuration."
progressive_disclosure:
  entry_point:
    summary: "Secrets management CLI for syncing environment variables across teams, projects, and environments"
    when_to_use: "When working with envshed, environment variables, secrets management, .env files, or related configuration."
    quick_start: "1. Review core concepts below. 2. Apply the right command for your use case. 3. Consult references for advanced features."
  references:
    - workspaces-monorepo.md
    - secret-management.md
    - environments.md
    - ci-cd-service-tokens.md
    - api-reference.md
---

# Envshed CLI — Secrets Management

Envshed is a secrets management CLI for syncing environment variables across teams, projects, and environments. It supports monorepo workspaces, secret linking between projects, version history with rollback, snapshots, and service tokens for CI/CD.

## Quick Start

```bash
# 1. Login (opens browser for device-code auth)
envshed login

# 2. Initialize project (creates .envshed.json)
envshed init

# 3. Pull secrets to .env
envshed pull

# 4. Push local .env changes
envshed push

# 5. Run a command with secrets injected
envshed run -- npm start
```

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Organization** | Top-level container for projects; manages billing and team members |
| **Project** | Collection of environments and secrets within an org |
| **Environment** | Named set of secrets (e.g., development, staging, production) |
| **Secret** | Key-value pair encrypted at rest (AES-256-GCM) |
| **Workspace** | Monorepo sub-project with its own project/env mapping |
| **Secret Link** | Cross-project secret sharing with auto-propagation |
| **Snapshot** | Point-in-time backup of an entire environment |
| **Service Token** | Scoped machine-to-machine credential for CI/CD |

## Configuration Files

### Project Config: `.envshed.json`

Created by `envshed init`. Place at project root. Walks up the directory tree to find it.

**Single project:**
```json
{
  "org": "my-org",
  "project": "my-project",
  "defaultEnv": "development",
  "apiUrl": "https://app.envshed.com"
}
```

**Monorepo with workspaces:**
```json
{
  "org": "my-org",
  "apiUrl": "https://app.envshed.com",
  "workspaces": {
    "apps/api": {
      "project": "api-backend",
      "defaultEnv": "development",
      "file": ".env"
    },
    "apps/web": {
      "project": "web-frontend",
      "defaultEnv": "development",
      "file": ".env.local"
    }
  }
}
```

Each workspace can override `org`, `project`, `defaultEnv`, and `file`.

### Global Config: `~/.envshed/config.json`

Stores authentication token and API URL. Managed by `envshed login` and `envshed token`.

```json
{
  "token": "envshed_...",
  "apiUrl": "https://app.envshed.com",
  "locale": "en"
}
```

### Version Cache: `~/.envshed/version-cache.json`

Tracks environment versions locally to detect when remote secrets have been updated since your last pull.

## Resolution Order

When resolving org, project, and environment:

1. CLI flags (`-o`, `-p`, `-e`)
2. Workspace config (when `-w` or auto-detected)
3. Root `.envshed.json` values
4. Environment variables (`ENVSHED_API_URL`, `ENVSHED_TOKEN`, `ENVSHED_ENV`)
5. Global `~/.envshed/config.json`

## All Commands

### Authentication

| Command | Description |
|---------|-------------|
| `envshed login` | Authenticate via browser device-code flow |
| `envshed login --token <token>` | Set token directly (e.g., service token) |
| `envshed login --api-url <url>` | Override API URL |
| `envshed whoami` | Display authenticated user's email |
| `envshed token show` | Display masked current token |
| `envshed token set <token>` | Set API token directly |
| `envshed token clear` | Clear saved token |

### Project Setup

| Command | Description |
|---------|-------------|
| `envshed init` | Interactive setup creating `.envshed.json` |
| `envshed init -o <org> -p <project> -e <env>` | Non-interactive setup |
| `envshed init -w <path>` | Configure a single workspace |
| `envshed branch` | Show current context (org, project, environment) |

### Secret Operations

| Command | Description |
|---------|-------------|
| `envshed pull` | Download secrets to local `.env` file |
| `envshed pull --stdout` | Print secrets to stdout |
| `envshed pull --format json` | Output as JSON |
| `envshed pull --force` | Skip breaking change detection |
| `envshed pull -e <env>` | Pull from specific environment |
| `envshed pull --all` | Pull all workspaces (monorepo) |
| `envshed pull -w <path>` | Pull specific workspace |
| `envshed push` | Upload local `.env` to remote |
| `envshed push -f <file>` | Push from specific file |
| `envshed push --force` | Skip breaking change detection |
| `envshed push --all` | Push all workspaces |
| `envshed run -- <cmd>` | Execute command with secrets injected |
| `envshed run --watch -- <cmd>` | Auto-restart on remote changes |
| `envshed run --interval <s> -- <cmd>` | Custom poll interval for watch |

### Individual Secret Management

| Command | Description |
|---------|-------------|
| `envshed secret get <KEY>` | Get a single secret value |
| `envshed secret set <KEY>` | Set a secret (prompts for value via hidden input or stdin) |
| `envshed secret set <KEY> --placeholder` | Create a placeholder secret (no value) |
| `envshed secret delete <KEY> [-y]` | Delete a secret (`-y` skips confirmation) |
| `envshed secret override set <KEY>` | Set personal override (prompts for value) |
| `envshed secret override remove <KEY> [-y]` | Remove personal override |

### Environment Management

| Command | Description |
|---------|-------------|
| `envshed env checkout <slug>` | Switch active environment (alias: `switch`) |
| `envshed env list` | List all environments for current project |
| `envshed env create -n <name>` | Create a new environment |
| `envshed env update <slug> -n <name>` | Update environment name/description |
| `envshed env delete <slug> [-y]` | Delete an environment |
| `envshed env duplicate <source> -n <name>` | Clone an environment with all secrets |
| `envshed envs` | Shorthand for `env list` |
| `envshed env-version` | Get environment version and last update time |
| `envshed rename-env <slug> -n <name> -s <new-slug>` | Rename an environment |
| `envshed diff <env1> <env2>` | Compare two environments |
| `envshed diff <env1> <env2> --show-values` | Compare with actual values |

### Version History & Rollback

| Command | Description |
|---------|-------------|
| `envshed versions <KEY>` | View version history for a secret |
| `envshed versions <KEY> --limit <n>` | Limit results |
| `envshed rollback <KEY> --version <n>` | Restore secret to a previous version |

### Snapshots

| Command | Description |
|---------|-------------|
| `envshed snapshot create` | Create environment snapshot |
| `envshed snapshot create -n <name>` | Create named snapshot |
| `envshed snapshot list` | List snapshots |
| `envshed snapshot restore <id>` | Restore from snapshot |

### Secret Linking (Cross-Project)

| Command | Description |
|---------|-------------|
| `envshed link <KEY> --to-project <p> --to-env <e>` | Link secret to another project |
| `envshed unlink <KEY>` | Remove secret link |

### Import

| Command | Description |
|---------|-------------|
| `envshed import <file> --format env` | Import from .env file |
| `envshed import <file> --format json` | Import from JSON |
| `envshed import <file> --format yaml` | Import from YAML |
| `envshed import <file> --format csv` | Import from CSV |

### Organization & Project Management

| Command | Description |
|---------|-------------|
| `envshed orgs` | List all organizations |
| `envshed projects` | List projects in current org |
| `envshed projects -o <org>` | List projects in specific org |
| `envshed project create -o <org> -n <name>` | Create project |
| `envshed project delete -o <org> -p <project>` | Delete project |

### Team Management

| Command | Description |
|---------|-------------|
| `envshed member list -o <org>` | List org members |
| `envshed member invite <email> -r <role> -o <org>` | Invite member by email |
| `envshed member role <email> -r <role> -o <org>` | Update member role |
| `envshed member remove <email> -o <org> [-y]` | Remove member |

### Workspace Management

| Command | Description |
|---------|-------------|
| `envshed workspace add <path>` | Add workspace to config |
| `envshed workspace remove <path>` | Remove workspace |
| `envshed workspace list` | List configured workspaces |

### Secret Definitions (Schema)

| Command | Description |
|---------|-------------|
| `envshed definition list` | List secret definitions |
| `envshed definition create <KEY> -d <desc> [--required]` | Create definition |
| `envshed definition update <KEY> -d <desc> [--required/--no-required]` | Update definition |
| `envshed definition delete <KEY> [-y]` | Delete definition |

### Service Tokens (CI/CD)

| Command | Description |
|---------|-------------|
| `envshed token create-service -o <org> -n <name> -s <scope> -p <perm>` | Create service token |
| `envshed token list-service -o <org>` | List service tokens |
| `envshed token update-service <id> -o <org>` | Update service token (name, description, active status) |
| `envshed token revoke-service -o <org> --id <id>` | Revoke service token |

### Webhooks

| Command | Description |
|---------|-------------|
| `envshed webhook list -o <org>` | List webhooks |
| `envshed webhook create --name <n> --url <url> --events <e> -o <org>` | Create webhook |
| `envshed webhook update <id> -o <org>` | Update webhook (name, url, events, active) |
| `envshed webhook delete <id> -o <org> [-y]` | Delete webhook |
| `envshed webhook test <id> -o <org>` | Send test event to webhook |

### Organization & Project Management (extended)

| Command | Description |
|---------|-------------|
| `envshed project list -o <org>` | List projects (full form) |
| `envshed project update <slug> -o <org> -n <name>` | Update project |
| `envshed project delete <slug> -o <org> [-y]` | Delete project |

### Other

| Command | Description |
|---------|-------------|
| `envshed completions <shell>` | Generate shell completions (bash, zsh) |
| `envshed --locale <code>` | Set language (en, es, pt-BR) |
| `envshed --version` | Show CLI version |

## Global Flags

| Flag | Description |
|------|-------------|
| `--locale <code>` | Language: en, es, pt-BR (default: auto-detect) |
| `-w, --workspace <path>` | Target specific workspace |
| `-a, --all` | Run for all workspaces (bulk mode) |
| `-o, --org <slug>` | Override organization |
| `-p, --project <slug>` | Override project |
| `-e, --env <slug>` | Override environment |
| `--help` | Show help for command |
| `--version` | Show CLI version |

## Common Workflows

### Initial Setup for a Monorepo

```bash
envshed login
envshed init                   # Auto-detects workspaces from pnpm-workspace.yaml
envshed pull --all             # Pull secrets for all workspaces
```

### Daily Development

```bash
envshed pull                   # Sync latest secrets
envshed run -- pnpm dev        # Start dev server with secrets
```

### Switching Environments

```bash
envshed env staging            # Switch to staging (handles local changes)
envshed pull                   # Pull staging secrets
envshed run -- pnpm dev        # Dev against staging
envshed env development        # Switch back
```

### Before a Deploy

```bash
envshed snapshot create -n "pre-deploy-$(date +%Y%m%d)" -e production
envshed push -e production     # Push production secrets
```

### CI/CD Pipeline

```bash
# Create a service token (once, from your machine)
envshed token create-service -o my-org -n "GitHub Actions" -s project --project-id <id> -p read

# In CI (use ENVSHED_TOKEN env var)
export ENVSHED_TOKEN=envshed_svc_...
envshed pull -e production -f .env.production
```

### Rollback After Bad Secret Change

```bash
envshed versions API_KEY                      # Find the good version
envshed rollback API_KEY --version 5          # Restore it
# Or restore the entire environment:
envshed snapshot list
envshed snapshot restore <snapshot-id>
```

### Compare Environments Before Promotion

```bash
envshed diff staging production --show-values
```

### Import Existing Secrets

```bash
envshed import .env.local --format env
envshed import config/secrets.json --format json
envshed import secrets.yaml --format yaml
```

## Localization

The CLI supports three languages, auto-detected from system locale:
- **English** (en) — default
- **Spanish** (es)
- **Portuguese** (pt-BR)

Override with `--locale pt-BR` or set `locale` in `~/.envshed/config.json`.
