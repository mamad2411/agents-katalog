---
name: buildkite
description: Interact with Buildkite using the bk CLI. Use when the user wants to trigger builds, check build status, list pipelines, view build logs, or perform any Buildkite operations from the command line.
allowed-tools: "Bash(bk:*), Bash(jq:*), Read"
argument-hint: [pipeline-slug or build-number]
---

# Buildkite CLI (`bk`)

## Prerequisites

- **bk CLI**: https://github.com/buildkite/cli

```bash
which bk || echo "bk not installed: https://github.com/buildkite/cli"
```

One-time auth setup: `bk configure`

## Triggering Builds

```bash
bk build create --pipeline <org>/<pipeline> --branch <branch>
bk build create --pipeline <org>/<pipeline> --branch <branch> --commit <sha> --message "..." \
  --env KEY1=value1 --env KEY2=value2
bk build create --pipeline <org>/<pipeline> --branch main --web   # trigger and open in browser
```

**Prompts for confirmation in non-interactive shells** — pipe `Y` explicitly:
```bash
printf 'Y\n' | bk build create --pipeline <org>/<pipeline> --branch <branch> --message "..."
```

## Querying Build Status

```bash
bk build view                                              # most recent (auto-detects from git)
bk build view <build-number> --pipeline <org>/<pipeline>
bk build list --pipeline <org>/<pipeline>
bk build list --pipeline <org>/<pipeline> --branch <branch> --state failed --since 24h
```

### Build frequency analysis

**Always pass `--no-limit`** — the default cap is 50 results, which covers less than one day for high-frequency pipelines.

**Exclude today** (partial day distorts averages): filter `date < today` when aggregating.

**Low-activity pipelines**: if 0 builds in 3 days, extend to 7 then 10 days before concluding inactive.

**Pipeline 404**: mark explicitly — slugs in docs can be stale/renamed. Don't silently treat as 0 activity.

## Pipeline Operations

```bash
bk pipeline list
bk pipeline view <org>/<pipeline>
```

## Job and Log Operations

There is no `--build` flag for `bk job list` — use `bk build view` and parse the JSON instead.

```bash
bk job log <job-id> -p <org>/<pipeline> -b <build-number>
bk job log <job-id> -p <org>/<pipeline> -b <build-number> --no-timestamps
```

**`bk job log` does NOT support `-o json`.**

**Large logs**: use `head -N` instead of `tail -N` or `grep` — `head` exits early via SIGPIPE and is significantly faster. For pipeline YAML, download the artifact instead:
```bash
bk artifacts list <build-number> --pipeline <org>/<pipeline>
bk artifacts download <artifact-id>
```

**`bk build view -o json` warning prefix**: output starts with a deprecation warning before the JSON. Strip it:
```python
data = json.loads(next(l for l in raw.splitlines() if l.strip().startswith('{')))
```

**Empty log output**: either a trigger step (check the downstream build) or expired logs. Fall back to reading the build script from the local repo or via `gh api`.

## Common Workflows

```bash
bk build rebuild <build-number> --pipeline <org>/<pipeline>
bk build cancel <build-number> --pipeline <org>/<pipeline>
bk build view <build-number> --pipeline <org>/<pipeline> --web
```

## Tips

- Use `-o json` for machine-readable output (`build`, `pipeline` commands; NOT `job log`)
- **Prefer `jq` over Python** for simple parsing: `bk build list -p org/pipeline -o json | jq -r '.[].state'`
- Short flags: `-p` (pipeline), `-b` (branch), `-m` (message), `-c` (commit), `-e` (env), `-w` (web)

## Sandbox / Permissions

**Always use `required_permissions: ["all"]`** — `["network"]` is NOT sufficient: `bk` fails with a TLS certificate error inside the sandbox even with network access enabled.
