---
name: stackfork
description: Use when preparing, starting, testing, or cleaning up a local development environment in a Git worktree or branch with the stackfork CLI, especially when Docker Compose ports, databases, volumes, or app configuration could collide with another checkout.
---

# stackfork

Use the project's actual runtime, package manager and startup flow through `stackfork`, a framework-independent Compose isolation helper (optional Nuxt/Bun template included). Adapt existing stacks first; do not force a non-Nuxt or dependency-only project into the Nuxt template.

## Reuse before rediscovering

Run `stackfork where` (lists prepared instances and configured profiles) and `stackfork status` first. If `.stackfork/knowledge.md` is `verified`, apply its recorded adapter and startup plan directly — no scan, no questions (`references/learning.md`); `stackfork plan` shows the plan's steps and whether this machine trusts them. Otherwise run `stackfork learn` (`prepare` and `up` refuse a repository that was never learned), read `.stackfork/knowledge.md`, and run the learn session in `references/learning.md`. `learn` proposes the startup plan; record each step with `learn record step`. Record the dependency install (`yarn install --frozen-lockfile`, `npm ci`, `pnpm install --frozen-lockfile`, `bun install`) as an exec step with `--once deps`, before build and migrate steps. If it proposes a seed step, confirm the command with the user and record it (`--seed-once CMD`, or `none` to disable); with no decision a new database is seeded with the detected script automatically, but not while the knowledge is a draft. Do not repeat a full discovery, or rewrite a launcher, for a routine restart of an unchanged adapter. Before preparing a brand-new instance, run `stackfork list` — an instance for this project may already exist elsewhere (another branch, another worktree) with data worth starting from via `clone-db --from <instance>` instead of an empty database, or `clone-db --from-dump FILE` to seed from a local `.sql`/`.sql.gz`/Postgres dump (or `stackfork dashboard` for the same cross-checkout view in a local, read-mostly web page — never used for the destructive commands below).

## Follow profile context

For each profile `stackfork where` lists with `"context": true`, follow that profile's `context.md` first, before anything below — it may point at a private reference and template for this project instead of the generic one. Profiles are private and never part of this repository.

## Prepare, start, verify, stop

1. **Discover:** resolve the checkout with Git, read AGENTS.md/README, and adapt the project's real Compose stack (`references/adapting-compose.md`, or a template for a bare app with no app-building Compose at all: `references/nuxt-template.md` for Nuxt, `references/go-template.md` for a Go web app). Use a separate worktree per concurrent agent, created with `stackfork worktree add REPO BRANCH` (`references/worktrees.md`); a branch already checked out (for example `main` in the main checkout) is started in that checkout, never a second worktree.
2. **Prepare:** `stackfork --root "$CHECKOUT" prepare -f <compose files> --env-file <runtime env>`
3. **Start:** `stackfork --root "$CHECKOUT" up`. Hybrid mode (`stackfork config set mode hybrid`) runs the app on the host as a plan `host` step; only a person can trust it (`stackfork plan --trust`), never an agent. A host-run app starts with `stackfork --root "$CHECKOUT" host start app -- <your command>`: detached and supervised, so it survives your shell, and `host ls|logs|stop|restart|rm` and `up` manage it later (stable port, this instance's env, a portless route; `references/adapting-compose.md`); in a host `cmd` use `{{port}}`, `{{url}}`, `{{APP.url}}` and `{{service.NAME.url}}` instead of fixed ports or hostnames (`references/learning.md`). `host start` is for servers only; run a one-shot command (tests, a script) with `stackfork run`/`exec` or in your shell, and `host rm NAME` clears a finished one. During learn, record each host app's `depends_on` (`--depends-on postgres`) and, if the person wants a lost database to stop its apps, `learn record stop-cascade on` (`references/learning.md`). A foreground `host app -- cmd` dies with your shell. Never start the app directly on the host (`bun run dev`, `npm run dev`, etc.) for a stackfork-managed checkout — that bypasses isolation, and the guard hook blocks it. After a failed start, read `stackfork --root "$CHECKOUT" runs show` (and `--step STEP` for its log) before retrying.
4. **URLs:** `stackfork --root "$CHECKOUT" urls` — report the named `<instance>.localhost` URL it prints, never a bare `localhost`/`127.0.0.1` (`references/hostnames.md`). During learn, record the app's entry and named links (`learn record entry|link`; `references/learning.md`).
5. **Verify:** database identity and app readiness at minimum; login, HMR and a representative flow on first adoption. Stay inside the checked-out instance for this. If verifying something would need new infrastructure beyond it (a different environment mode, a second stack, anything you'd have to build rather than just check) — ask first; report the gap instead of silently building it.
6. **Stop:** `stackfork --root "$CHECKOUT" down` (keeps data).

## One-off builds, tests and troubleshooting

A one-off build or test that could fight the running dev process (a different install step, a migration, a full test run) uses `stackfork --root "$CHECKOUT" run <service> <cmd>` (a fresh, separate container), never `exec` into the running one. When it's done, `stackfork --root "$CHECKOUT" down` (data kept) unless the user asked to keep the instance running. An unhealthy or exited service: `stackfork restart <service>` (affects only this instance; never restart Docker).

## Refusals and deletion

Trust `stackfork prepare`'s refusals (fixed container names, external networks, Docker sockets, writable binds outside the checkout, fixed subnets) — never work around one. `down --volumes`, `reset`, `gc --apply` and `prune --yes`/`--all` delete data and need the user's own authorization for that specific deletion (the guard blocks them); agents may run only the dry run `stackfork prune`, and never prune for the user without an explicit request. Never turn live mode or automatic cleanup on (`live on`, `live cleanup auto`, `live clean --yes` are for people); read `stackfork live status`. To test a feature flag or another variable of one service without editing the project, use `stackfork --root "$CHECKOUT" env set SERVICE NAME=VALUE` (and `env unset`, `env overrides`): it is per instance, outside the repository, and recreates only that service. It refuses secret-like names; `--allow-secret` and `env overrides --clear` are for people. Secrets: list them with `stackfork secret ls`/`check`; setting and mapping them is for a person, so ask the user. Never open or copy another project's real env files, registry credentials, certificates or private keys.

## Report

Report checkout, branch, Compose project, app/DB/auxiliary endpoints, and the checks actually run, without any credential values. Distinguish a validated Compose model and running dependencies from a working application — do not describe a dependency-only check as full application validation.

From any directory, address an instance with `--instance NAME` (names: `stackfork list`) instead of `--root`. Full command reference: `references/commands.md`; or run `stackfork help` / `stackfork <command> --help`.
