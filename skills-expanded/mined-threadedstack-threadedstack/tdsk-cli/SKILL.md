---
name: "tdsk-cli"
description: "Knowledge base for the developer CLI repo - DevOps orchestration for Docker, Kubernetes, and DevSpace"
tags: ["cli", "nodejs", "devops", "kubernetes", "docker", "devspace"]
---
# CLI Repo Skill

## Overview

The CLI repo (`@tdsk/cli`) is a developer CLI for managing the Threaded Stack monorepo.

- **Docker**: Build, pull, push, run, exec containerized applications (supports sandbox image type variants)
- **Kubernetes**: Secrets (7 presets: tdsk, docker, database, payments, email, egress + list), namespaces, logs, pod inspection
- **DevSpace**: Development environment start, clean, log, enter, render, attach, use
- **Web UI**: Start admin UI in dev mode
- **NPM**: Package management (pack, publish) with alias `pkg`
- **Hierarchical tasks**: Built on `@keg-hub/args-parse` with nested commands (3 levels deep), aliases, and options across 7 task groups

## Directory Structure

```
repos/cli/
├── configs/              # cli.config.ts (six contexts), aliases.ts (@TSCL/*), tsup, vitest
├── scripts/              # loadEnvs.ts, addToProcess.ts
├── src/
│   ├── index.ts          # Entry point (exports cli.ts)
│   ├── cli.ts            # Main CLI runner — argsParse integration
│   ├── constants/        # EnvFilter for child process env vars
│   ├── types/            # TTask, TTaskAction, TCliCfg, ECtxMap
│   ├── tasks/            # Command definitions
│   │   ├── index.ts      # Task registry
│   │   ├── db/           # certs, check, cleanup, db, dbExport, dk, drop, dup, generate, introspect, migrate, purge, push, reset, rmf, seed, studio
│   │   ├── deploy/       # apply, deploy, status
│   │   ├── docker/       # build, run, exec, pull, push, login
│   │   ├── kube/         # set, pod, secret, remove, logs, namespace
│   │   ├── npm/          # pack, publish (alias: pkg)
│   │   │   └── secret/   # Presets: tdsk, docker, database, payments, email, egress
│   │   ├── devspace/     # start, clean, log, enter, render, attach, use
│   │   ├── fleet/        # on, off, status — toggle the autonomous agent fleet
│   │   └── web/          # start
│   └── utils/
│       ├── config/       # getCtx — context resolution with alias + sandbox type support
│       ├── devspace/     # DevSpace CLI helpers
│       ├── docker/       # Docker CLI helpers
│       ├── kube/         # kubectl wrapper (create, delete, apply, describe, getPod, getPods, ensureContext)
│       ├── pnpm/         # PNPM command execution
│       ├── proc/         # Process management (spawn with lifecycle hooks)
│       ├── tasks/        # Task utilities (find, error, options)
│       └── helpers/      # General helpers
```

## Architecture

**Execution flow**: `process.argv` → `find(tasks, args)` (resolve by name/alias, traverse nested tasks) → `argsParse()` → `loadCfg(env)` → `task.action({ task, tasks, params, config, options })`

**Config loading**: `--env` option (default: `local`) → `cli.config.ts` imports `@tdsk/domain/loadEnvs` → provides `config.contexts` with repo metadata (paths, images, tags, ports).

**Task structure**: `{ name, alias?, action?, tasks? (nested), options? }` — supports up to 3 levels of nesting.

**Key files**:

| File | Purpose |
|------|---------|
| `src/cli.ts` | Main CLI entry — parses args, loads config, executes tasks |
| `src/tasks/index.ts` | Task registry exporting all command groups |
| `configs/cli.config.ts` | Config with paths, six contexts, and env vars |
| `src/types/tasks.types.ts` | Core types: TTask, TTasks, TTaskAction, TTaskOptions |
| `src/types/config.types.ts` | Config types and ECtxMap enum |
| `src/utils/config/getCtx.ts` | Context resolver with alias and sandbox type variant support |
| `src/utils/kube/kubectl.ts` | Kubectl wrapper: create, delete, apply, describe, getPod, getPods, ensureContext |
| `src/tasks/kube/secret/egress.ts` | Egress CA secret — self-signed cert generation + K8s secret creation |

## Context System

Six contexts map to repos/services. `getCtx()` resolves a context name (with alias support) to its config object containing image, tag, dockerfile, location, ports, and mounts.

| Alias | Context | Dockerfile | Notes |
|-------|---------|------------|-------|
| — | `app` | `Dockerfile.app` | Root monorepo image |
| `px` | `proxy` | `Dockerfile.proxy` | Auth gateway |
| `be` | `backend` | `Dockerfile.backend` | Core API |
| `ad` | `admin` | `Dockerfile.admin` | SPA dashboard |
| `cd` | `caddy` | `Dockerfile.caddy` | TLS/LB |
| `sb` | `sandbox` | `Dockerfile.sandbox` | Dynamic pods (no K8s deployment) |

**ECtxMap aliases**: `be` → backend, `px` → proxy, `ad` → admin, `cd` → caddy, `sb` → sandbox.

**Sandbox image variants**: When `--context sandbox` and `--type` is specified (not "base"), `getCtx()` replaces the `-base` suffix in the image name with `-<type>` (e.g., `--type claude` produces `image-claude`).

**Context config fields**: image, tag, from (base image), dtag (dev tag), deployment (K8s deployment name, empty for sandbox), dockerfile, location (repo path), tags, mounts, ports.

## Command Summary

| Task Group | Commands | Aliases | Key Options |
|---|---|---|---|
| **db** | certs, check, cleanup, db, dbExport, dk, drop, dup, generate, introspect, migrate, purge, push, reset, rmf, seed, studio | — | --context, --env |
| **deploy** | apply, deploy, status | — | --context, --env, --namespace |
| **web** | start | ui | --context (default: admin) |
| **docker** | build, run, exec, pull, push, login | doc, dc | --context, --tag, --image, --port, --type, --push, --cache, --arm, --platforms, --login |
| **kube** | set, pod, secret, remove, logs, namespace | kubectl, kb, kcl | --context, --output, --name, --namespace |
| **npm** | pack, publish | pkg | --context, --tag |
| **kube secret** | tdsk, docker, database, payments, email, egress | egress-ca, eca | --cert, --key, --log, --name, --file, --keyvalue, --secrets |
| **devspace** | start, clean, log, enter, render, attach, use | dev, ds | --build, --debug, --follow, --selector, --purge, --deploy |
| **fleet** | on, off, status | on: up/enable · off: down/disable · status: state/st | — |

### Fleet Toggle (`tasks/fleet/`)

`tdsk fleet on | off | status` toggles the autonomous AI agent fleet (6 always-on residents + steward/CTO-board schedules + the `system-monitor`/`update-behind-prs` GitHub workflows) down or up in one command. The platform (backend/proxy/caddy/egress/admin/threads) is untouched. The task is a thin wrapper that delegates to the single implementation in the database repo (`repos/database/scripts/toggleFleet.ts`, via `pnpm --filter @tdsk/database run fleet:<mode>`), which reads the prod DB URL from the `tdsk-db-cfg` k8s secret itself (no credential export). Always targets prod. **Caveat**: "off" is live DB/workflow state, so a full `tdsk release` re-reconciles the fleet back on — re-run `tdsk fleet off` after any deploy while it should stay down.

### Key Commands

```bash
# Docker
pnpm tdsk docker build --context proxy --tag v1.2.3
pnpm tdsk docker build --context sandbox --type claude    # Sandbox variant
pnpm tdsk docker build --context sandbox --type codex     # Sandbox variant
pnpm tdsk docker exec --context proxy --cmd "/bin/sh"
pnpm tdsk docker pull --context proxy
pnpm tdsk docker push --context proxy --tag v1.0.0

# Kubernetes secrets
pnpm tdsk kube secret database
pnpm tdsk kube secret tdsk
pnpm tdsk kube secret payments
pnpm tdsk kube secret email
pnpm tdsk kube secret docker --env prod --namespace production
pnpm tdsk kube secret egress                              # Generate self-signed CA + K8s secret
pnpm tdsk kube secret egress --cert ./ca.crt --key ./ca.key  # Use existing cert
pnpm tdsk kube secret --name my-secret --keyvalue key1:value1

# Kubernetes pod inspection
pnpm tdsk kube pod --context proxy
pnpm tdsk kube pod --name my-pod-abc123 --output json

# DevSpace
pnpm tdsk dev start --clean
pnpm tdsk dev start --build --debug
pnpm tdsk dev log --follow --context backend
pnpm tdsk dev enter --context backend --cmd "/bin/sh"
pnpm tdsk dev render                                      # Dry-run Helm templates
pnpm tdsk dev clean --images --cache
pnpm tdsk dev use --namespace dev --context minikube

# Web UI
pnpm tdsk web start                                       # Start admin UI dev server

# Database management
pnpm tdsk db migrate                                      # Run migrations
pnpm tdsk db seed                                         # Seed database
pnpm tdsk db studio                                       # Open Drizzle Studio
pnpm tdsk db generate                                     # Generate migration files
pnpm tdsk db push                                         # Push schema changes

# Deployment
pnpm tdsk deploy apply                                    # Apply deployment
pnpm tdsk deploy status                                   # Check deployment status
```

### Egress CA Secret Details

Generates a self-signed CA certificate (~10 years valid) via OpenSSL. Cert/key resolution fallback chain:
1. CLI args (`--cert`/`--key`)
2. Env vars (`TDSK_EGRESS_CA_CERT`/`TDSK_EGRESS_CA_KEY`)
3. `~/.config/tdsk/domain/egress.cert` and `egress.key` (generates new if absent)

Creates a K8s secret named per `TDSK_KUBE_SCRT_EGRESS_CA` env var (default: `tdsk-egress-ca`) with `tls.crt` and `tls.key` keys.

### Pod Inspection

`kube pod --context <name>` resolves pod from context label via `kubectl.getPod()`, then calls `kubectl.describePod()`. Aliases: `pods`, `po`, `describe`. Supports `--output json/yaml/wide`.

## Key Utilities

| Utility | Location | Purpose |
|---------|----------|---------|
| `getCtx()` | `utils/config/getCtx.ts` | Context resolution with alias + sandbox type variants; validates context exists and directory is on disk |
| `kubectl` | `utils/kube/kubectl.ts` | Kubectl wrapper: create, delete, apply, describe, getPod, getPods, ensureContext |
| `spawn()` | `utils/proc/spawn.ts` | Child process spawning with lifecycle hooks (close, exit, error, stdout, stderr) |
| `find()` | `utils/tasks/find.ts` | Task resolution for nested commands and aliases |
| `pnpm.run()` | `utils/pnpm/` | Execute workspace commands via PNPM |

## Environment Management

- **EnvFilter**: Controls which env vars pass to child processes. Filters by prefix (npm_, HOME, KEG_, FIREBASE, GOOGLE, AZURE, AWS), suffix (_PATH, _PORT), and exclusion lists.
- **NODE_ENV**: Set via `--env` option (default: `local`)
- **Image tags**: Environment-specific via env vars (TDSK_PX_IMAGE_TAG, TDSK_BE_IMAGE_TAG, TDSK_AD_IMAGE_TAG, TDSK_CADDY_IMAGE_TAG, TDSK_SB_IMAGE_TAG)

## Integration Points

- **`@tdsk/domain`**: `loadEnvs()` for environment config from `deploy/values.*.yml`
- **`@tdsk/logger`**: `Logger.info()`, `Logger.pair()`, `Logger.stdout()`, `Logger.stderr()`, `Logger.colors`
- **External tools**: Docker CLI, kubectl, DevSpace CLI, PNPM, OpenSSL (egress CA generation)

## Using the CLI

```bash
pnpm tdsk <command> <subcommand> <options>   # Via PNPM workspace (monorepo root)
pnpm cli <command>                            # Dev mode (from repos/cli/)
node dist/index.js <command>                  # Direct execution (from repos/cli/)
```

## Error Handling

- **Task not found**: `taskError()` throws when command doesn't exist
- **Missing options**: Validation for required options
- **Process failures**: spawn() captures exit codes and stderr
- **Config errors**: Try-catch around config loading
- **Cleanup**: K8s secret temp files removed even on error
- **Context validation**: `getCtx()` verifies context exists in config and directory exists on disk

## Test Coverage

Minimal: 1 test file (`src/utils/config/getCtx.test.ts`) with a placeholder test. CLI relies on manual integration testing.
