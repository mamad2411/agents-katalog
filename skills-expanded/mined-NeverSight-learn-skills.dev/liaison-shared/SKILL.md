---
name: liaison-shared
version: 0.1.0
description: "Liaison Cloud CLI shared foundation: installation, authentication with Personal Access Tokens, token precedence (flag > env > config file), error handling, and output format. Auto-loaded by every other liaison-* skill — always consult first when you are helping a user operate liaison-cli."
metadata:
  requires:
    bins: ["liaison"]
  cliHelp: "liaison --help"
---

# liaison-shared

Core knowledge every liaison-cli task depends on. Read this first.

## What this CLI is for

`liaison` is the official command-line client for [liaison.cloud](https://liaison.cloud) — a zero-trust reverse tunnel / connector platform. A **connector** is an agent running on a user's machine that registers back to the cloud; **applications** are the services (IP + port) behind a connector; **entries** (aka proxies) expose those applications to the public internet.

Typical user intents you will be asked to automate:

- Install a connector on a new machine
- Expose an HTTP/SSH/DB service through a public URL or port
- Kick a misbehaving connector offline or re-enable it
- List/audit what's currently running

## Installation (for the user)

If `liaison` is not on the user's PATH, offer **one** of these install paths:

```bash
# 1) curl one-liner (Linux/macOS) — no Node required
curl -fsSL https://github.com/liaisonio/cli/releases/latest/download/install.sh | sh

# 2) npx (any Node environment)
npx -y @liaisonio/cli@latest version

# 3) go install (developers with a Go toolchain)
go install github.com/liaisonio/cli/cmd/liaison@latest
```

The agent skill files themselves are installed via:

```bash
npx skills add liaisonio/cli -y -g
```

Both `npm i -g @liaisonio/cli` and the curl installer also pre-populate
`~/.claude/skills` as a safety net, so on a fresh CLI install the skill
files are usually already there. If `npx skills add` can't reach GitHub,
`liaison skills install -g` reads the embedded copy out of the CLI binary —
fully offline fallback.

## Authentication — Personal Access Tokens

The CLI authenticates with a **Personal Access Token (PAT)** — a long-lived bearer token the user creates in the Liaison dashboard. Tokens look like `liaison_pat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`.

### Token precedence (highest wins)

1. `--token <pat>` flag on the command
2. `LIAISON_TOKEN` environment variable
3. `~/.liaison/config.yaml` (written by `liaison login`)
4. Built-in default: none — command fails with a clear error

### For agents

**Best path**: the user stores a PAT in your secrets store as `LIAISON_TOKEN`. Then every command works without any login flow:

```bash
LIAISON_TOKEN=liaison_pat_... liaison whoami
```

### For human users

```bash
# Option A: browser flow — opens the dashboard, click approve, auto-saves token
liaison login

# Option B: SSH/headless — prints URL instead of opening a browser
liaison login --no-browser

# Option C: skip browser, paste a token directly
liaison login --token liaison_pat_xxxxx
```

`liaison login` verifies the token against `/api/v1/iam/profile_json` before saving — if the server returns an error the token is NOT persisted.

Other auth commands:

```bash
liaison whoami        # prints the current user (JSON)
liaison logout        # clears the token from config
```

## Output contract

**Default output is JSON.** Parse stdout directly — all resource fields are preserved, ids are numeric, nulls stay null. Examples:

```bash
liaison edge list                     # JSON (default, agent-friendly)
liaison edge list -o yaml             # YAML (human-readable)
liaison edge list -o table            # aligned text table (lossy — only key columns)
liaison edge get 100017 | jq .name    # piping into jq works
```

- **stdout** carries only data (or a CLI-printed success line for `delete`)
- **stderr** carries errors and interactive progress (like `liaison login`'s "Waiting for authorization...")
- **exit code** `0` = success, `1` = any error

## Error handling rules (CRITICAL for agents)

When a command fails, **read the stderr message before retrying**. The CLI does not retry on network errors — that's your job if appropriate.

Common errors and the correct response:

| Error | Meaning | Correct action |
|-------|---------|----------------|
| `unauthorized (HTTP 401): token missing or invalid — run \`liaison login\`` | No token or expired token | Ask the user to set `LIAISON_TOKEN` or run `liaison login` |
| `refusing to delete without --yes (non-interactive safety)` | Destructive action without confirmation | Add `--yes` to the command |
| `api error 403: ... WAF_BLOCKED` | The request body triggered the server WAF | Inspect the body — this is usually a real attack pattern, not a retry case |
| `--application-id is required` / `--app-name is required` | Missing required flag | Supply the flag |

## Global flags

| Flag | Env | Default |
|------|-----|---------|
| `--server` | `LIAISON_SERVER` | `https://liaison.cloud` |
| `--token` | `LIAISON_TOKEN` | (none) |
| `--config` | — | `~/.liaison/config.yaml` |
| `--output`, `-o` | — | `json` |
| `--insecure` | — | false — **never** enable for production |
| `--verbose`, `-v` | — | false — prints HTTP method+URL to stderr (never the token) |

## Destructive-action safety

**Every `delete` subcommand requires `--yes`.** The CLI refuses to proceed without it:

```bash
liaison edge delete 100017 --yes           # required
liaison proxy delete 10 --yes              # required
liaison application delete 5 --yes         # required
```

This is non-negotiable — do not try to work around it. If a user wants to delete, either ask them to confirm (human case) or have explicit authorization in your task (agent case).

## What you should NOT do

- **Do not retry on exit code 1** without reading the error message first
- **Do not use `--insecure`** unless the user is explicitly testing against a self-signed server
- **Do not include the token in log output** — it's sensitive; redact it before echoing
- **Do not call `go install` / `curl | sh`** without confirming with the user; those modify their system

## Discovering more commands

Every subcommand supports `--help`:

```bash
liaison --help                           # top-level commands
liaison <resource> --help                # list of actions under a resource
liaison <resource> <action> --help       # flags + examples for one action
```

When uncertain, run the relevant `--help` **before** guessing at flag names. The help text is hand-written, has examples, and is authoritative.
