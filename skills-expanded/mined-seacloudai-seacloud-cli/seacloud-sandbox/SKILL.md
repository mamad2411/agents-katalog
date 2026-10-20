---
name: seacloud-sandbox
description: >-
  Use this skill when the user wants to create, run commands in, connect to, inspect, observe, or clean up SeaCloud sandboxes or sandbox templates with the SeaCloud CLI.
  It covers E2B-compatible sandbox workflows, safe automation defaults, dry-run previews for writes and deletes, network policy, volumes, lifecycle events, webhooks, metrics, logs, teams, observability, and template build commands.
---

# SeaCloud Sandbox

Use `seacloud sandbox` for cloud sandbox runtime work and `seacloud template` for sandbox template projects and builds.

## Start Here

Verify the CLI and auth state before real operations:

```bash
seacloud --version || npm install -g @seacloudai/seacloud-cli
seacloud auth status
```

If auth is missing or expired, run:

```bash
seacloud auth login
```

`seacloud auth set-key <api-key>` is not enough for sandbox or template
operations; those commands need the login session.

When a login command opens a browser, prints a URL, or shows a device code, tell the user the exact action required.

## Automation Defaults

For non-interactive agent work, create sandboxes with:

```bash
seacloud sandbox create base --no-connect --wait --output json --metadata app=agent
```

Rules:

1. Use `--output json` or `--format json` when another tool needs structured data.
2. Use `--no-connect` for automation so create does not open an interactive shell.
3. Keep the returned sandbox ID and pass it explicitly to `exec`, `logs`, `metrics`, `info`, and `kill`.
4. Run write, delete, replay, and bulk cleanup commands once with global `--dry-run` before the real command.
5. Prefer explicit sandbox IDs over bulk operations. When bulk cleanup is needed, use narrow `--state` and `--metadata` filters.
6. Use `--limit`, `--next-token`, `--cursor`, or `--offset` on list, log, event, and delivery commands.

## Core Workflow

```bash
seacloud sandbox create base --no-connect --wait --output json --metadata app=agent
seacloud sandbox list --state running,paused --metadata app=agent --limit 10 --output json
seacloud sandbox exec <sandbox_id> "python --version"
seacloud sandbox logs <sandbox_id> --limit 100 --direction backward --output json
seacloud sandbox metrics <sandbox_id> --output json
seacloud --dry-run sandbox kill <sandbox_id>
seacloud sandbox kill <sandbox_id>
```

Use `connect` only when the user wants an interactive terminal:

```bash
seacloud sandbox connect <sandbox_id> --shell bash
```

## Command Map

Common sandbox commands:

```bash
seacloud sandbox create [template]
seacloud sandbox list --state running,paused --metadata app=agent --limit 10 --next-token <token>
seacloud sandbox info <sandbox_id>
seacloud sandbox exec <sandbox_id> "ls -la"
seacloud sandbox exec --cwd /workspace --user root --env NODE_ENV=production <sandbox_id> "node app.js"
seacloud sandbox exec --background <sandbox_id> "sleep 60 && echo done"
seacloud sandbox connect <sandbox_id> --shell bash
seacloud sandbox kill <sandbox_id>
seacloud sandbox metrics <sandbox_id>
seacloud sandbox logs <sandbox_id> --limit 100 --direction backward
```

Lifecycle and policy commands:

```bash
seacloud sandbox pause <sandbox_id>
seacloud sandbox timeout <sandbox_id> --seconds 3600
seacloud sandbox refresh <sandbox_id> --duration 300
seacloud sandbox network update <sandbox_id> --allow-public-traffic=false --allow-internet-access=false
seacloud sandbox network update <sandbox_id> --allow-out 1.1.1.1 --deny-out 10.0.0.0/8
```

Volumes:

```bash
seacloud sandbox volume create cache
seacloud sandbox create base --volume-mount cache:/cache --no-connect --wait --output json
seacloud sandbox volume list --output json
seacloud sandbox volume get <volume_id>
seacloud sandbox volume delete <volume_id>
```

Events, webhooks, and observability:

```bash
seacloud sandbox events --type sandbox.lifecycle.created --limit 20
seacloud sandbox webhook create --name lifecycle --url https://example.com/webhook --secret <secret> --event sandbox.lifecycle.created
seacloud sandbox webhook list --limit 20
seacloud sandbox webhook get <webhook_id>
seacloud sandbox webhook update <webhook_id> --enabled=false
seacloud sandbox webhook delete <webhook_id>
seacloud sandbox webhook deliveries --status failed --limit 20
seacloud sandbox webhook replay <delivery_id>
seacloud sandbox team list
seacloud sandbox team metrics <team_id> --start 1710000000 --end 1710003600
seacloud sandbox team metrics-max <team_id> --metric concurrent_sandboxes
seacloud sandbox observability
```

Templates:

```bash
seacloud template init --language typescript --name my-template
seacloud template migrate --language python --name my-template
seacloud template build my-template --dockerfile Dockerfile
seacloud template build my-template --image python:3.13 --cpu-count 2 --memory-mb 2048 --tag v1
seacloud template build my-template --from-template base --no-wait
seacloud template list --format json
seacloud template get my-template
seacloud template builds my-template
seacloud template status <template_id> <build_id>
seacloud template logs <template_id> <build_id> --limit 100
seacloud template tags assign my-template:v1 production stable
seacloud template tags list my-template
seacloud template tags remove my-template staging
seacloud template delete my-template
```

## Environment

Sandbox and template commands use the SeaCloud login session.

Useful overrides:

- `--base-url`: command-line sandbox API base URL override.
- `SEACLOUD_BASE_URL`: alternate SeaCloud API origin; sandbox commands normalize it to `/api/sandbox/v1`.
- `SEACLOUD_SANDBOX_URL`: sandbox API base URL override.
- `SEACLOUD_NAMESPACE_ID`: namespace scope for scoped sandbox APIs.
- `SEACLOUD_USER_ID`: user scope header.
- `SEACLOUD_PROJECT_ID`: project or team scope header.

Endpoint priority is `--base-url`, `SEACLOUD_SANDBOX_URL`,
`SEACLOUD_BASE_URL`, then `https://cloud.seaart.ai/api/sandbox/v1`.

## Recovery

If `seacloud sandbox create` opens a shell unexpectedly, rerun with `--no-connect` or `--output json`.
If a write/delete command is risky, run the same command with global `--dry-run` first.
If an API returns too much data, add `--limit` and pagination flags.
If a command reports missing auth, run `seacloud auth status` and then `seacloud auth login`.
If parameter shape is unclear, inspect the live help:

```bash
seacloud sandbox --help
seacloud sandbox <command> --help
seacloud template --help
```
