---
name: deploy
description: Deploy an app or static site to a live URL with openpouch (agent-native hosting — no account, no CAPTCHA, one command). Use when the user asks to deploy, publish, ship, host, or wants a live/preview/shareable URL for what you built.
---

# Deploy with openpouch

openpouch is hosting built for agents: you can complete the whole deploy autonomously. Anonymous works (free, ephemeral preview); an `OPENPOUCH_API_KEY` (env or `~/.openpouch/openpouch-run.key`) lifts deploys into the human's account tier. Never a CAPTCHA or human-verification wall.

This plugin also ships the openpouch MCP tools (`openpouch_deploy`, `openpouch_verify`, `openpouch_logs`, …) — prefer them when available; the CLI commands below are the equivalent fallback and work in any shell. Both return the same truth.

## Deploy

Pick the command by project shape — this choice is the one thing worth getting right up front:

| Project shape | Command |
|---|---|
| Built static output (`dist/`, `build/`, plain HTML) | `npx openpouch deploy <dir> --json` |
| Raw source (unbuilt SPA, needs `npm install`/build) | `npx openpouch deploy . --json` (server builds it) |
| Full-stack (server entry, e.g. Express + SPA) | `npx openpouch deploy . --health-path /api/health --json` — set `--health-path` to a real API route **on the first deploy**, so health checks probe the backend, not just the static root |

Env vars: `--var KEY=value` (repeatable) or `--env-file .env`. Values are used at runtime only and never appear in any output. Never echo secret values yourself either.

**Stable URL across redeploys (0.4.0+):** add `--app <name>` (account key required) — the first deploy mints ONE URL, every later `deploy --app <name>` updates the app behind it (health-gated; a failed update never breaks the live version; result carries `urlStability: "stable"`). Without `--app`, every deploy mints a fresh URL. Apps that store data on disk: add `--volume` (paid tiers) for a persistent `/data`; `npx openpouch data push|pull|ls <name>` moves/backs up that data (push replaces `/data` with a health-gated restart).

## After the deploy

Parse the JSON result:

- `url` — the live URL. This is the primary result.
- `summary` — plain-language text written for a possibly non-technical human. Relay it verbatim.
- `tellYourUser` — when present, a ready-to-relay hand-off block (live URL, exact expiry date, the ways to keep the app). Pass it on to your human — don't summarize it away.
- `nextCommands` — ready-to-run `verify` / `logs` / `inspect` commands; prefer them over constructing your own.
- The claim link is **for the human only** (it lets them keep the preview past expiry). The CLI stores it privately in `.openpouch/claim.json`; don't post claim tokens/links into shared contexts.

Verify before reporting success: run the `nextCommands.verify` command (it includes the right `--health-path` automatically) and only then tell the human the app is live.

## If the app is unhealthy (self-repair loop)

1. `npx openpouch logs <slug-or-url> --json` — build/runtime output with phase markers (`[install]`, `[build]`, `[app]`).
2. Fix the code locally.
3. Re-run **the same deploy command you used first** — on the instant lane a redeploy produces a **new URL** (tell the human the link changed) unless it's a named app (`--app <name>`), which keeps the same URL across updates.
4. Verify again. Repeat until healthy.

## Resuming in a later session

Deployment truth survives in the repo: read `DEPLOYMENT.md` (human-readable, includes a resume checklist and this self-repair runbook) and `deploy.evidence.json` (machine-readable: URL, commit, time, smoke results). Re-reading them is always sufficient — no session memory required.

## Two lanes — know which one you're on

`openpouch deploy` puts the app on openpouch's own hosting (a migration). `openpouch init` on a project with an existing provider key may map the EXISTING service as a governance layer — the app keeps running on the old host. Since 0.4.0 the CLI forks this intent itself: on a project whose manifest maps another provider, `deploy` refuses without `--app` and names the migration move; with `--app` it deploys (that IS the migration), the old host keeps running untouched as the rollback anchor, and `data push` brings stored data along. Never tell your human a migration happened when you set up governance; the full recipe is `docs/WORKFLOWS.md` §10 on openpouch.dev.

## Hard rules

- `approve` (governed production lane) is **human-only** in every interface. If a command answers `human-required`, relay the included instructions to the human — never try to work around it.
- Secret values never go into output, files, or chat — names and presence only.
- If `npx` itself fails with `EACCES` before openpouch runs, the sandbox's npm cache is read-only — retry with `npx --cache .openpouch-cache openpouch …`.

Full reference: `npx openpouch --help`, per-command `--help`, and https://openpouch.dev/llms.txt
