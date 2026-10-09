---
name: n8nctl
description: Operate an n8n instance via the `n8nctl` CLI (package `@trngthnh369/n8nctl`, installed globally). Use when user asks to list, create, update, trigger, debug, backup, restore, watch, validate, or manage n8n workflows / executions / credentials / tags. Requires N8N_HOST + N8N_API_KEY env vars OR a configured n8nctl profile. Curl fallback documented for edge cases the CLI does not cover.
allowed-tools: "Bash Read Write Edit"
---

# n8n API Operations

> **🎯 Preferred tool: `n8nctl` CLI** (package `@trngthnh369/n8nctl`, installed globally).
> Fall back to curl only when: (a) the CLI doesn't cover the operation, or (b) you need raw HTTP for debugging.

The CLI wraps the n8n REST API with retry, auth layering, --dry-run, --json/--jq/--template output, and typed exit codes (0 OK, 1 API, 2 auth, 3 validation, 4 network, 5 internal).

---

## Quick reference — n8nctl commands

### Workflow
```bash
n8nctl workflow list [--active] [--tag <t>] [--search <text>] [--all] [--redact]
n8nctl workflow get <id> [-o <file>] [--redact]           # v0.2: --redact scrubs pinData/webhookId/credName
n8nctl workflow status <id> [--exit]                       # v0.2.5: pretty state + webhooks + last exec; --exit maps active→0/1
n8nctl workflow create <file.json> [--activate]            # v0.2.4: --activate registers webhook in same step. or "-" for stdin
n8nctl workflow update <id> <file.json> [--activate]       # v0.2.4: --activate. or "-" for stdin
n8nctl workflow activate <id>
n8nctl workflow deactivate <id>
n8nctl workflow refresh <id> [--delay <ms>]                # v0.2.5: deactivate→wait→activate to refresh n8n webhook router cache
n8nctl workflow trigger-webhook <id> [--data <json>] [--wait --timeout <ms>] \
  [--auth-bearer <token>] [--auth-basic <user:pass>] [--auth-header "Name: Value"]    # v0.2; pre-checks active, --test for /webhook-test/
n8nctl workflow run <id> [--trigger <node name>] [--wait] [--timeout <ms>]   # v0.5: execute headless via /rest session (Public API has no execute). For manual/scheduled/sub-workflow; bypasses webhook router (#21614). Needs `auth login --session`
n8nctl workflow backup <id> [-o <dir>]
n8nctl workflow watch [--workflow <id>] [--status <s>] [--interval <ms>]   # v0.2: realtime tail
n8nctl workflow delete <id> [--yes]
n8nctl workflow validate <file.json> [--strict]            # v0.5: +E070 settings-no-logs, E071 node-id-not-uuid, E072 typeVersion-outdated
n8nctl workflow normalize <file.json> [-o <out>] [-w]      # v0.5: fix node-id→UUID + inject save-log settings (deterministic). create/update auto-normalize (--no-normalize to skip)
n8nctl workflow diff <id> <file.json>                      # preview changes
n8nctl workflow restore <backup.json> [--activate]
n8nctl workflow tag <id> <tag-names...> [--replace --create]
n8nctl workflow export-all -o <dir> [--active --tag <t>]
n8nctl workflow import <dir> [--force --activate]
```

### Execution
```bash
n8nctl execution list [--workflow <id>] [--status <s>] [--limit <n>]
n8nctl execution get <id> [--logs]
n8nctl execution retry <id>
n8nctl execution wait <id> [--timeout <ms>]     # poll until terminal
n8nctl execution last-error --workflow <id> [--summary]
```

### Credential / Tag / Auth / Config / Profile / Doctor / Completion
```bash
n8nctl credential list [--type <t>]                     # derived from workflow nodes
n8nctl credential schema <type>
n8nctl credential create <file>                          # POST /credentials from JSON ({name,type,data})
n8nctl credential create <file> --no-validate            # skip schema pre-flight
n8nctl tag list
n8nctl tag create <name>                                 # max 24 chars (n8n limit)
n8nctl auth login [--host <url>] [--profile <name>] [--insecure]
n8nctl auth login --session [--email <addr>] [--cookie-only]   # v0.5: email/password for `workflow run` (/rest). Cookie+password in keyring. Use automation member user
n8nctl auth status
n8nctl auth logout [--profile <name>]                          # v0.5: purges api-key + session password + cookie
n8nctl profile {list|add|switch|remove}
n8nctl config {get|set|list}
n8nctl doctor                                            # 10 checks incl. write permission (v0.2)
n8nctl completion {bash|zsh|fish|powershell}             # v0.2: shell completion script
```

### Global flags (on every command)
- `--json` / `--jq <expr>` / `--template <handlebars>` — output format
- `--profile <name>` — one-shot profile override
- `--api-key <token>` + `--host <url>` — ephemeral auth override
- `--insecure` — disable TLS verify (self-signed dev instances only)
- `--dry-run` — preview for destructive commands (delete, update, tag, import, restore, trigger-webhook)
- `--timeout <ms>` — per-command HTTP timeout

---

## Workflow patterns

### Deploy a workflow file from git
```bash
n8nctl workflow validate ./my-workflow.json --strict
n8nctl workflow diff 42 ./my-workflow.json          # see what changes
n8nctl workflow update 42 ./my-workflow.json --dry-run  # preview (optional)
n8nctl workflow update 42 ./my-workflow.json
n8nctl workflow activate 42
```

### Backup before risky change
```bash
n8nctl workflow backup 42 -o ./_backups/
# ... make changes ...
n8nctl workflow restore ./_backups/xxx.json --activate   # rollback
```

### Test gate (webhook-triggered workflows)
```bash
# Fire the webhook and wait for completion in one command
n8nctl workflow trigger-webhook 42 --data '{"input":"x"}' --wait --timeout 60000
# Exit code: 0 = success, 1 = execution failed, 4 = timeout

# Webhook with custom auth (v0.2)
n8nctl workflow trigger-webhook 42 --auth-bearer $TOKEN --data '{...}' --wait
n8nctl workflow trigger-webhook 42 --auth-header "X-Signature: $SIG" --data '{...}'
```

### Watch executions realtime (v0.2)
```bash
# Tail all new executions
n8nctl workflow watch

# Only failed ones for a specific workflow
n8nctl workflow watch --workflow 42 --status error --interval 2000
```

### Pipe workflow JSON via stdin (v0.2, kubectl-style)
```bash
cat my-workflow.json | n8nctl workflow create -
curl -s .../template | n8nctl workflow update 42 -
```

### Safely inspect workflow without leaking secrets (v0.2)
```bash
# Scrub pinData, credentials.*.name, webhookId — useful for bug reports / PRs
n8nctl workflow get 42 --redact --json > safe-to-share.json
```

### Self-heal loop
```bash
n8nctl execution last-error --workflow 42 --summary
# → shows failing node + error message
# ... fix workflow JSON ...
n8nctl workflow update 42 ./fixed.json
n8nctl execution retry <last-execution-id>
```

### Bulk git-sync (export-all + import)
```bash
# Export entire instance to git-tracked directory
n8nctl workflow export-all -o ./workflows/

# Later, deploy to another instance
n8nctl --profile staging workflow import ./workflows/ --force
```

---

## Debugging: output + jq

Claude can pipe CLI output directly to jq or Handlebars templates:

```bash
# Find all active workflows using a specific credential
n8nctl credential list --type googleSheetsOAuth2Api \
  --jq '.[] | {name, count: (.usedInWorkflows | length)}'

# List execution IDs of failures in last hour
n8nctl execution list --status error --limit 20 \
  --jq '[.[] | select(.startedAt > (now - 3600) | todate)] | map(.id)'
```

---

## Auth resolution (CLI)

1. `--api-key` + `--host` flags (ephemeral)
2. `N8N_API_KEY` + `N8N_HOST` env vars (legacy, still works for one-liners)
3. OS keyring (from `n8nctl auth login`)
4. `~/.config/n8nctl/config.yml` / `%APPDATA%\n8nctl\config.yml`

**Multi-instance** (dev/staging/prod):
```bash
n8nctl profile add prod --host https://n8n-prod.example.com
n8nctl auth login --profile prod
n8nctl profile switch prod
n8nctl --profile dev workflow list    # one-shot override
```

---

## Raw curl fallback (avoid unless necessary)

Use curl ONLY when the CLI doesn't cover something (rare — mostly never):

```bash
# base
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_HOST/api/v1/<endpoint>"
```

### Important API quirks (not obvious)
- **NO `/workflows/:id/execute` in the PUBLIC API** — but `n8nctl workflow run` (v0.5) executes headless via the internal `/rest/.../run` (session cookie auth), the same endpoint the UI "Execute Workflow" button uses. Use `workflow run` for manual/scheduled/sub-workflows; `trigger-webhook` for webhook-path tests.
- **NO `GET /credentials` list endpoint** — CLI derives from workflow nodes. To get credential metadata, use `credential schema <type>` instead.
- `activate/deactivate` is `POST /workflows/{id}/activate`, NOT `PATCH` on the workflow.
- Workflow `PUT /workflows/{id}` replaces the full body; DO NOT include `id`, `createdAt`, `updatedAt`, `versionId`, `active`, or `tags` fields in the body — the API rejects them. Use `n8nctl workflow update` which handles stripping.

---

## Tips

- Always call `n8nctl doctor` at the start of a new pipeline run — verifies auth + connectivity + permissions in one shot
- Add `--dry-run` liberally for destructive ops until you're sure
- For automation in shell scripts, parse with `--json --jq '...'` instead of brittle text scraping
- Binary lives at `~/.npm-global/bin/n8nctl` or `%APPDATA%\npm\n8nctl.cmd` depending on platform — always on PATH after `npm i -g @trngthnh369/n8nctl`
