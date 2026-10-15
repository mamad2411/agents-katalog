---
name: aio-ffcpe-cli
description: >-
  Use when working with the Adobe I/O CLI plugin @adobe/aio-cli-plugin-ffcpe (FFCPE — Firefly Creative Production for Enterprise).
  Covers installation, authentication, env overrides, and all `aio ffcpe catalog` commands. Use for terminal workflows, scripting catalog changes, or explaining how developers should invoke this plugin. Some users still say **Workflow Builder**; that name referred to the same product area — the CLI topic is **`ffcpe`** (`aio ffcpe`).
---

# aio-cli-plugin-ffcpe (FFCPE CLI)

This repository is an **oclif plugin** for Adobe I/O CLI. **Topic: `ffcpe`** — **Firefly Creative Production for Enterprise (FFCPE)** — focused on the **run-workflow Catalog API** for custom actions.

**Legacy language:** internal and older docs sometimes say **Workflow Builder** or used older topic naming in screenshots. That is the same capability; current branding and the **`aio`** topic are **`ffcpe`**.

## When to use this skill

- Installing or troubleshooting the plugin
- Choosing the right `aio ffcpe catalog …` command
- Explaining flags (`--base-url`, `--org-id`, `--api-key`, `--json`, etc.)
- How auth and org context are resolved

## Setup

### 1. Install Adobe I/O CLI (`aio`)

Requires **Node.js 18+**.

```sh-session
npm install -g @adobe/aio-cli
aio --version
```

### 2. Install this plugin (`@adobe/aio-cli-plugin-ffcpe`)

```sh-session
aio plugins:install @adobe/aio-cli-plugin-ffcpe
```

Or from Git (fork or internal repo):

```sh-session
aio plugins:install https://github.com/adobe/aio-cli-plugin-ffcpe
```

### 3. Verify and authenticate

```sh-session
aio ffcpe catalog --help
aio login
aio console org select
```

If **`aio ffcpe`** is missing, run **`aio plugins`** and confirm this package is installed.

## Base URL

- **Default:** `https://run-workflow.adobe.io`
- **Override:** environment variable **`AIO_FFCPE_CATALOG_BASE_URL`** or flag **`--base-url`** (`-u`) on catalog commands.

## Commands (catalog)

| Command | Purpose |
|--------|---------|
| **`aio ffcpe catalog validate`** | Local validation of catalog entry JSON (typically **`<action-name>.entry.json`**). Use `--file` / `-f`. |
| **`aio ffcpe catalog register`** | POST a new catalog entry from a JSON file. Validates first; optional **`--strict`** to fail on validation warnings. |
| **`aio ffcpe catalog inspect ACTIONTYPE`** | GET one action; optional **`--version`** for a specific semver. |
| **`aio ffcpe catalog list`** | GET catalog actions (supports filters per command help). |
| **`aio ffcpe catalog update ACTIONTYPE`** | PUT a full replacement definition. |
| **`aio ffcpe catalog disable ACTIONTYPE`** | Disable (and typically hide from the FFCPE workflow UI). |
| **`aio ffcpe catalog enable ACTIONTYPE`** | Re-enable a disabled action. |
| **`aio ffcpe catalog delete ACTIONTYPE`** | DELETE; use **`--version`** to delete one semver only. |

Run **`aio ffcpe catalog --help`** or **`aio ffcpe catalog <command> --help`** for exact flags and examples.

## Common flags

- **`--org-id`** — override `x-gw-ims-org-id` (default from `aio console org select`).
- **`--api-key`** — override `x-api-key` when needed.
- **`--json`** — print raw API JSON where supported.

## Authoring catalog entries

The CLI does not scaffold entries interactively. Use the **`ffcpe-catalog-entry-json`** skill (or **`/aio-ffcpe-skills:ffcpe-catalog-entry-json`** when the plugin is installed).

**Recommended layout in App Builder repos:** store each action’s catalog JSON as **`<action-name>.entry.json`** next to **`<action-name>.web.*`** and **`<action-name>.worker.*`** (e.g. **`actions/resize-image/resize-image.entry.json`**). That groups implementation and registration for one custom action. See **`ffcpe-app-builder-actions`** in [ffcpe-custom-node-sdk](https://github.com/adobe/ffcpe-custom-node-sdk).

Then validate and register:

```sh-session
aio ffcpe catalog validate -f ./actions/resize-image/resize-image.entry.json
aio ffcpe catalog register -f ./actions/resize-image/resize-image.entry.json
```

## Pre-registration: wiring the App Builder project

Before registering, the App Builder app must be deployed and the local project wired to a Console workspace.

### Console project naming

| Rule | Detail |
|------|--------|
| Alphanumeric only | Hyphens rejected: `demo-qr-app` fails with `Project name … is invalid` |
| Max 20 characters | Longer names fail at create time |
| Name ≠ package | Console project (e.g. `demoQrFfcpe`) can differ from OpenWhisk **`runtimeManifest` package** (e.g. `demo-qr-custom-ffcpe-nodes`) |

Stage and Production workspaces are created automatically with a new project.

### Console CLI flag gotchas

The `aio console workspace` commands have **inconsistent flag shapes** — using the wrong flag throws `NonExistentFlagsError`:

| Command | Correct flags |
|---------|---------------|
| `aio console workspace create` | `--projectName <name>` (required), `--name <name>` (required) |
| `aio console workspace select` | positional `[NAME_OR_ID]` + optional `--projectId <id>` |
| `aio console workspace list`   | `--projectId <id>` — **no `--projectName` flag** |
| `aio console workspace download` | optional positional destination path |

### Wire, build, deploy

```sh-session
aio console project create -n myproject -t "My FFCPE App" --json
aio console project select myproject
aio console workspace select Stage --projectId <PROJECT_ID>
aio console workspace download myproject-Stage.json
echo 'myproject-Stage.json' >> .gitignore
aio app use myproject-Stage.json --overwrite --no-input
aio app build
aio app deploy
```

Use **`--overwrite --no-input`** on **`aio app use`** when `.env` already exists from `aio app init` — otherwise the CLI prompts interactively and can hang in agent/CI sessions.

The downloaded JSON file contains client credentials and API keys. The generated `.gitignore` does **not** cover this file automatically (it only covers `console.json` and `.env*`). Add the exact filename — or the pattern `[0-9]*-*-*.json` — immediately after download.

### Post-deploy: endpoints → catalog → register

1. Copy each **web action base URL** from deploy output.
2. Set **`submitEndpoint`** = `{base}/submit`, **`statusEndpoint`** = `{base}/status` in **`<action-name>.entry.json`**.
3. Set **`authentication`** to **`ims_service_token`** when using default SDK route auth (see **`ffcpe-catalog-entry-json`**).
4. Register:

```sh-session
aio console org select
aio ffcpe catalog validate -f ./actions/my-action/my-action.entry.json
aio ffcpe catalog register -f ./actions/my-action/my-action.entry.json
# or, if actionType already exists:
aio ffcpe catalog update my-action -f ./actions/my-action/my-action.entry.json
```

See **`ffcpe-app-builder-actions`** skill for the full init-bare → deploy → register flow.

## Deeper docs

- **`skills/README.md`** — agent skills (Claude **`/`** commands, Cursor paths, **`npx skills`** install).
- **`.cursor/ffcpe-catalog/SKILL.md`** — catalog operations via **`aio ffcpe catalog`** (same HTTP API under the hood; do not hand-craft curl).
