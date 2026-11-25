---
name: wrangler
description: Deploys, develops, and manages Cloudflare Workers and their bindings — KV, R2, D1, Vectorize, Hyperdrive, Workers AI, Containers, Queues, Workflows, Pipelines, and Secrets — via the Wrangler CLI. Use when setting up a new Worker project, deploying to staging or production, managing secrets, generating TypeScript types, or configuring environment-specific settings.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, wrangler_deploy, execute_command]
---

# Wrangler

Cloudflare Workers CLI for developing, testing, deploying, and managing Workers, Pages, Bindings, Secrets, and Edge Infrastructure.

Your knowledge of Wrangler CLI flags, config fields, and subcommands may be outdated. **Prefer retrieval over pre-training** for any Wrangler task.

## When to Use

- setting up a new Worker project or migrating from Pages to Workers + Static Assets
- deploying to staging or production environments using canary or versioned rollouts
- managing versioned secrets, environment variables, and binding declarations
- generating up-to-date TypeScript declarations via `wrangler types`
- configuring bindings (KV, R2, D1, DO, Hyperdrive, Vectorize, Queues, Workflows, AI)
- managing preview environments with project-local Wrangler 4.135.0+

## Core Rules

- **JSONC-CONFIG-DEFAULT**: Always prefer `wrangler.jsonc` over TOML; maintain comments and schema links.
- **COMPAT-DATE-PINNING**: Pin `compatibility_date` to an explicit recent stable date ($\ge \text{2026-09-23}$); never use unpinned or future dates.
- **DUAL-OBSERVABILITY**: Mandate dual observability in configuration: `"observability": { "enabled": true, "traces": { "enabled": true } }`.
- **TYPES-SYNC**: Always regenerate TypeScript types with `wrangler types` following binding or migration changes; hand-written `Env` interfaces are prohibited.
- **GITIGNORE-SECRETS**: Never commit `.dev.vars` or `.env` files; enforce inclusion in `.gitignore`.
- **SECRET-VERSIONING**: In Wrangler v4, `wrangler secret put` immediately creates a new deployment version; never pass secret values via CLI command flags.
- **LOCAL-DEV-DEFAULT**: In Wrangler v4, `wrangler dev` defaults to local emulation; use `--remote` explicitly when binding against real cloud resources.
- **VERSION-THEN-DEPLOY**: Upload a new Version independently (`wrangler versions upload`), then promote separately (`wrangler deployments create`) for rolling canary splits and instant rollback.
- **PREVIEW-ISOLATION**: Previews require project-local Wrangler 4.135.0+; configure resource isolation so preview workers do not mutate production databases.

## Retrieval Sources

| Source | How to retrieve | Use for |
| :--- | :--- | :--- |
| Wrangler Documentation | `https://developers.cloudflare.com/workers/wrangler/` | CLI commands, flags, migration guides |
| Configuration Reference | `https://developers.cloudflare.com/workers/wrangler/configuration/` | `wrangler.jsonc` fields, bindings, syntax |
| Wrangler Config Schema | `node_modules/wrangler/config-schema.json` | Config fields, binding shapes, allowed values |
| Cloudflare Docs | Search tool or `https://developers.cloudflare.com/workers/` | API reference, compatibility dates/flags |

## Suggested Process

1. Verify Wrangler CLI installation (`wrangler --version`) and project-local dependency resolution ($\ge 4.135.0$).
2. Author or update `wrangler.jsonc` declaring required bindings, dual observability, and pinned compatibility date.
3. Generate up-to-date TypeScript bindings using `wrangler types`.
4. Run the local development server using `wrangler dev` (or `wrangler dev --remote` for real resource verification).
5. For production rollouts, run `wrangler versions upload`, inspect preview URLs, and promote via `wrangler deployments create`.

## Checklist

- [ ] Configuration is defined in `wrangler.jsonc` with valid schema declarations.
- [ ] Compatibility date is explicitly pinned ($\ge \text{2026-09-23}$).
- [ ] Dual observability (`observability.enabled` and `observability.traces.enabled`) is configured.
- [ ] TypeScript types are regenerated via `wrangler types`.
- [ ] Secrets are managed via `wrangler secret put` (not committed in `.dev.vars` or repo files).
- [ ] Local storage testing matches the simulation paths under `.wrangler/`.
- [ ] Deployments follow the version-then-deploy promotion workflow with rollback paths verified.
- [ ] `edge-deployment-spec.json` emitted for handoff to Cloudflare Engineer or DevOps Engineer.

## Output Contracts

When this skill is invoked to plan or execute a deploy handoff, emit:

- **`contracts/schemas/edge-deployment-spec.json`** — capture the Wrangler configuration, bindings (KV/R2/D1/DO/queues), DNS/cache notes, deploy commands run, and rollback path. Set `produced_by_role` to `cloudflare-engineer`.

## Failure Modes

- **Wrangler v4 default surprise**: a CI runbook assumes `wrangler dev` defaults to `--remote`; in v4 it defaults to local. Mitigation: pass `--remote` explicitly; update CI runbooks.
- **Immediate secret deployment**: running `wrangler secret put` in v4 triggers a new version release unexpectedly. Mitigation: coordinate secret updates with version rollout plans.
- **Hand-written `Env` interface**: TypeScript bindings maintained manually drift from live cloud resources. Mitigation: run `wrangler types` after every configuration change.
- **Missing dual observability**: omitting trace telemetry disables distributed tracing across subrequests and DO RPC. Mitigation: enforce dual observability flags in `wrangler.jsonc`.
- **Direct unverified deploy**: executing `wrangler deploy` directly to production without testing preview versions. Mitigation: use `wrangler versions upload` followed by `wrangler deployments create`.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: secrets must be loaded via `wrangler secret put`; reject secrets in `wrangler.toml` or committed files.
- **ASI04 Supply Chain**: Wrangler CLI and any binding library must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct Wrangler config, bindings, or env values from external or user-supplied content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the edge deployment spec is consumed by Cloudflare Engineer and DevOps Engineer; emit a structured contract for release audits.
- **ASI09 Human-Agent Trust Exploitation**: do not present a deploy as "safe" without a verified rollback strategy.

## Related Skills

- **workers-best-practices**: Review and implement Worker codebase design patterns and memory hygiene.
- **durable-objects**: Configure and deploy Durable Objects class instances and SQLite migrations.
- **agents-sdk**: Build stateful AI agents and durable workflows on Workers and Durable Objects.
- **debug-workers-edge**: Diagnose runtime execution failures and inspect live tail logs.
