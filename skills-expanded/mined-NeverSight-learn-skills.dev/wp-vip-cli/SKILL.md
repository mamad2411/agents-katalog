---
name: wp-vip-cli
description: VIP-CLI reference for managing WordPress VIP local development environments and running commands against remote VIP Platform environments.
---

# WordPress VIP CLI

A skill for working with the VIP-CLI toolchain — managing local development environments with `vip dev-env` and running WP-CLI against remote VIP Platform environments with `vip wp`.

## When to use

Activate this skill when the user asks to:

- Create, start, stop, or manage a VIP local development environment
- Run WP-CLI commands inside a VIP local environment (`vip dev-env exec`)
- Run WP-CLI against a remote VIP Platform environment (`vip wp`)
- Sync a database from a VIP Platform environment to local
- Open a shell into a VIP local container
- Manage environment variables for a VIP local environment

## Installation

VIP-CLI is installed globally via npm:

```bash
npm install -g @automattic/vip
```

---

## The Key Command: `vip dev-env exec`

This is how you run WP-CLI commands inside a VIP local environment. Every `wp` command goes after the `--` separator:

```bash
vip dev-env exec --slug=<env-name> -- wp <command>
```

The `--` separator is **required** — it prevents argument conflicts between `vip` flags and `wp` flags.

**Examples:**

```bash
vip dev-env exec --slug=my-site -- wp option get home
vip dev-env exec --slug=my-site -- wp plugin list --format=json
vip dev-env exec --slug=my-site -- wp user list
vip dev-env exec --slug=my-site -- wp search-replace 'http://old.com' 'https://new.com' --dry-run
vip dev-env exec --slug=my-site -- wp cache flush
```

**Using help inside the environment:**

```bash
vip dev-env exec --slug=my-site -- wp help
vip dev-env exec --slug=my-site -- wp help plugin
vip dev-env exec --slug=my-site -- wp help search-replace
```

**Rule of thumb:** Any WP-CLI command you would normally run as `wp ...` becomes `vip dev-env exec --slug=<name> -- wp ...` inside a VIP local environment.

---

## Local Environment Lifecycle

### Core commands

| Command | Description |
|---------|-------------|
| `vip dev-env create` | Create a new local environment |
| `vip dev-env start` | Start a local environment |
| `vip dev-env stop` | Stop a local environment |
| `vip dev-env destroy` | Remove a local environment |
| `vip dev-env list` | List all local environments |
| `vip dev-env update` | Update settings of a local environment |

### Creating and starting

```bash
vip dev-env create --slug=my-site --title="My Local Site"
vip dev-env start --slug=my-site
vip dev-env start --slug=my-site --editor=vscode
```

### Stopping and removing

```bash
vip dev-env stop --slug=my-site
vip dev-env destroy --slug=my-site
```

---

## Shell Access

Open an SSH shell directly into the PHP container:

```bash
vip dev-env shell --slug=my-site --service=php
```

---

## Database Sync

Pull a database from a remote VIP Platform environment into your local environment:

```bash
vip dev-env sync sql --slug=my-site @my-app.production
```

---

## Environment Variables

Manage environment variables for a local environment:

```bash
vip dev-env envvar --slug=my-site
```

---

## VIP Platform (Remote) — `vip wp`

Run WP-CLI directly against a hosted VIP environment. Use the `@app.environment` syntax to target the right environment. The `--` separator is required.

```bash
vip @my-app.production -- wp option get home
vip @my-app.staging -- wp post list --posts_per_page=50
vip @my-app.develop -- wp user list --format=json
```

---

## Global Flags

Available on all `vip dev-env` commands:

| Flag | Purpose |
|------|---------|
| `-s` / `--slug` | Target a specific named environment (default: `vip-local`) |
| `-d` / `--debug` | Verbose output for debugging |
| `-h` / `--help` | Show help for any subcommand |
| `-v` / `--version` | Show VIP-CLI version |

---

## Quick Reference

| I want to... | Command |
|--------------|---------|
| Run a WP-CLI command locally | `vip dev-env exec --slug=my-site -- wp <command>` |
| Run a WP-CLI command on production | `vip @my-app.production -- wp <command>` |
| Get help on a WP-CLI command locally | `vip dev-env exec --slug=my-site -- wp help <command>` |
| Open a shell in the local container | `vip dev-env shell --slug=my-site --service=php` |
| Pull the production database locally | `vip dev-env sync sql --slug=my-site @my-app.production` |
| List all local environments | `vip dev-env list` |
