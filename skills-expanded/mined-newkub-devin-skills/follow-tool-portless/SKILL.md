---
name: follow-tool-portless
description: Use portless instead of port numbers — named .localhost URLs for dev servers
argument-hint: "[app-name-or-command]"
related:
  - check-my-global-cli
---

## Goal

Use `portless` to run dev servers through an HTTPS proxy with stable named URLs (`https://<name>.localhost`) instead of `localhost:<port>` — for humans and agents

## Scope

Use when a task needs to run a dev server, preview, or wire services together on the local machine — covers run, routes, aliases, subdomains, worktrees, custom TLD, LAN mode, troubleshooting — not production deploy

## Execute

### 1. Verify Install

> Goal: `portless` ready to use

1. `portless --version` to check installation — if missing → `mise use -g portless` or `npm install -g portless` (requires Node.js 24+)
2. On first run, `portless trust` — adds the local CA to the system trust store (required for HTTPS)
3. `portless doctor` checks health: Node version, state dir, proxy, CA trust, hostname resolution

### 2. Run App

> Goal: run a dev server through a named URL

```bash
portless                          # run "dev" script from package.json → https://<project>.localhost
portless --script start           # run a different script instead of "dev"
portless run --name myapp vite    # override the inferred name
portless myapp vite dev           # explicit name + command
portless api.myapp pnpm start     # subdomain → https://api.myapp.localhost
```

- The name is inferred from `portless.json`, `package.json`, the git root, or the directory name
- A monorepo root (workspaces/pnpm-workspace) → `portless` opens every package that has that script
- A random port in 4000-4999 is passed via the `PORT` env; Vite/Astro/RR/Angular get auto-injected `--port`/`--host`

### 3. Routes And Aliases

> Goal: manage routes and service URLs

```bash
portless list                          # active routes + ports
portless get <name>                    # print URL — e.g. BACKEND_URL=$(portless get backend)
portless alias <name> <port>           # route to a service not run through portless (Docker etc.)
portless alias --remove <name>
portless <name> --force <cmd>          # override a conflicting route
```

### 4. Advanced Modes

> Goal: worktrees, custom TLD, LAN, sharing

- Git worktrees: `portless run` in a linked worktree → automatic branch prefix `https://<branch>.<app>.localhost` — the main worktree uses the bare name
- Custom TLD: `portless proxy start --tld test` → `https://myapp.test` (auto-syncs `/etc/hosts`); `--tld` can be repeated for several; use `.test` (IANA-reserved), avoid `.local` (mDNS conflict) and `.dev` (HSTS)
- LAN mode: `portless proxy start --lan` → reachable from a phone on the same WiFi via `.local` mDNS (macOS/Linux only); Next.js needs `allowedDevOrigins` added manually
- Share: `--tailscale`, `--funnel`, `--ngrok` flags on the run command

### 5. Proxy Control And Cleanup

> Goal: manage the proxy lifecycle

```bash
portless proxy start [-p 443] [--no-tls] [--foreground]
portless proxy stop
portless service install|status|uninstall   # OS startup service
portless prune [--force]                     # kill orphaned dev servers after a crash
portless clean                               # stop + remove CA + hosts entries + state
portless hosts sync|clean                    # manual /etc/hosts sync
PORTLESS=0 pnpm dev                          # bypass the proxy
```

## Rules

### 1. Prefer Named URLs

- Use `portless` instead of remembering ports when running dev servers that must open in a browser or be wired between services
- Use `portless get <name>` in scripts/env vars instead of hard-coding `localhost:<port>`

### 2. Framework Port Injection

- When a framework ignores `PORT` (Vite, Astro, RR, Angular), portless injects `--port` itself — but compound commands (`&&`, `|`), env prefixes, or script delegation (`npm run dev:vite`) are skipped → set the port in the script yourself
- Never repeat `--port`/`--host` in the command when portless already injects them

### 3. State And Elevation

- First time requires `portless trust` — binding port 443 may ask for sudo/admin
- If the hostname doesn't resolve → `portless hosts sync`; if a route lingers after a crash → `portless prune`

### 4. Windows Notes

- LAN mode is not supported on Windows; `.localhost` resolves in modern browsers without editing hosts
- `service install` uses Task Scheduler (SYSTEM) on Windows
- Use /deep-test load if needed
- Use /check-my-global-cli if needed


## Expected Outcome

- Dev servers reachable at `https://<name>.localhost` instead of port numbers
- Multi-service wiring via `portless get` without hard-coded ports
- Worktrees/aliases/subdomains work without colliding
- Trust/resolution/orphan issues fixed with `doctor`/`trust`/`hosts sync`/`prune`
