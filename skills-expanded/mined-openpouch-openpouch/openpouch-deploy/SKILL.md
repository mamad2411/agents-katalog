---
name: openpouch-deploy
description: Deploy an app or static site to a live URL with openpouch (agent-native hosting — no account, no CAPTCHA, one command). Use when the user asks to deploy, publish, ship, host, or wants a live/preview/shareable URL for what you built.
---

# Deploy with openpouch

openpouch is hosting built for agents: you can complete the whole deploy autonomously. Anonymous works (free, ephemeral preview); an `OPENPOUCH_API_KEY` (env or `~/.openpouch/openpouch-run.key`) lifts deploys into the human's account tier. Never a CAPTCHA or human-verification wall.

## Deploy

Pick the command by project shape — this choice is the one thing worth getting right up front:

| Project shape | Command |
|---|---|
| Built static output (`dist/`, `build/`, plain HTML) | `npx openpouch deploy <dir> --json` |
| Raw source (unbuilt SPA, needs `npm install`/build) | `npx openpouch deploy . --json` (server builds it) |
| Full-stack (server entry, e.g. Express + SPA) | `npx openpouch deploy . --health-path /api/health --json` — set `--health-path` to a real API route **on the first deploy**, so health checks probe the backend, not just the static root |

Env vars: `--var KEY=value` (repeatable) or `--env-file .env`. Values are used at runtime only and never appear in any output. Never echo secret values yourself either.

## After the deploy

Parse the JSON result:

- `url` — the live URL. This is the primary result.
- `summary` — plain-language text written for a possibly non-technical human. Relay it verbatim.
- `nextCommands` — ready-to-run `verify` / `logs` / `inspect` commands; prefer them over constructing your own.
- The claim link is **for the human only** (it lets them keep the preview past expiry). The CLI stores it privately in `.openpouch/claim.json`; don't post claim tokens/links into shared contexts.

Verify before reporting success: run the `nextCommands.verify` command (it includes the right `--health-path` automatically) and only then tell the human the app is live.

## If the app is unhealthy (self-repair loop)

1. `npx openpouch logs <slug-or-url> --json` — build/runtime output with phase markers (`[install]`, `[build]`, `[app]`).
2. Fix the code locally.
3. Re-run **the same deploy command you used first** — on the instant lane a redeploy produces a **new URL**; tell the human the link changed.
4. Verify again. Repeat until healthy.

## Resuming in a later session

Deployment truth survives in the repo: read `DEPLOYMENT.md` (human-readable, includes a resume checklist and this self-repair runbook) and `deploy.evidence.json` (machine-readable: URL, commit, time, smoke results). Re-reading them is always sufficient — no session memory required.

## Hard rules

- `approve` (governed production lane) is **human-only** in every interface. If a command answers `human-required`, relay the included instructions to the human — never try to work around it.
- Secret values never go into output, files, or chat — names and presence only.
- If `npx` itself fails with `EACCES` before openpouch runs, the sandbox's npm cache is read-only — retry with `npx --cache .openpouch-cache openpouch …`.

Full reference: `npx openpouch --help`, per-command `--help`, and https://openpouch.dev/llms.txt
