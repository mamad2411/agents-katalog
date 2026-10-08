---
name: buddy
description: >-
  Deploy apps to Buddy sandboxes, publish artifacts, create tunnels, manage domains,
  configure distributions, and run CI/CD pipelines using `bdy` CLI. Triggers on: deploy,
  sandbox, tunnel, expose, artifact, static site, publish, domain, distribution, pipeline, CI/CD.
---

# Buddy Platform

On-demand cloud infrastructure via `bdy` CLI. Run `bdy <command> --help` for flag details.

## Authentication

If any command returns `Token not provided` or `Not logged in`: ask the user to run `bdy login` in a **separate terminal** (AI cannot do interactive OAuth). To check if user is logged in run `bdy whoami`

## Sandbox (`bdy sandbox|sb`)

Cloud environments for dynamic apps (servers, databases, background processes).

### Critical Rules

- Sandboxes must live in a project. Before `sandbox create`, check `bdy whoami` for a project context and the `BUDDY_PROJECT` env var. If neither is set, ask the user (AskUserQuestion) whether to create a new project, then run `bdy proj link -p <project>` to attach it.
- Apps MUST bind to `0.0.0.0` (not `127.0.0.1`) for endpoints to work
- ALWAYS use `--ignore "node_modules/**" ".git/**"` when copying projects — install deps on sandbox instead.
- Preinstalled on Ubuntu 24.04: Node.js 24, Python 3.12, Go 1.25, Git, curl, jq, ripgrep

### Workflow

1. Create: `bdy sandbox create -i <name> --resources 2x4 --wait-for-running`
2. Copy files: `bdy sandbox cp ./src <name>:/app --ignore "node_modules/**" ".git/**" > /dev/null`
3. Install deps: `bdy sandbox exec command <name> "cd /app && npm install" --wait`
5. Start app via `app add` (NOT exec — gives you status/logs/restart):
   `bdy sandbox app add <name> "cd /app && npm start -- -H 0.0.0.0"`
6. Check app: `bdy sandbox app status <name> <app-id>` and `bdy sandbox app logs <name> <app-id>`
7. Add endpoint: `bdy sandbox endpoint add <name> -n web -e <port>`
8. Show the user the public endpoint URL, then ask via AskUserQuestion if they want to attach a custom domain. Options: claim one of the free domains available in Buddy, buy a new domain, or reuse one already in their workspace. Keep the option labels short — don't put CLI commands in them. After the user picks, run the relevant `bdy domain` command and wire it up with `bdy distro route create`.

### Tips

- Use `app add` to start services — NOT `exec command`. Apps are managed as systemd services with status, logs, stop, start, restart
- `bdy sandbox app list <name>` shows running apps with IDs
- Write config files locally, then `sandbox cp` — avoids heredoc escaping issues in exec
- Use `sandbox snapshot` to save/restore sandbox state
- Use `bdy distro route create` for custom domain routing + cdn

## Artifact (`bdy artifact|art`)

Two types of artifacts:

- **BUCKET** (default) — versioned file hosting with public URLs. Use for static sites, build outputs, downloadable files
- **CONTAINER** — Docker registry. Use for Docker images. Ask the user to run `bdy artifact docker login` in a **separate terminal** (AI cannot handle interactive credentials), then push/pull with standard `docker` commands

### BUCKET Workflow

1. Build if needed: `npm run build`
2. Create artifact: `bdy artifact create <name>` (default type is BUCKET)
   - Auth is set on creation, not per-version — ask about auth first (HTTP Basic `-a` / Buddy `-b` / None)
3. Publish with version: `bdy artifact publish <name>@1.0.0 ./dist`
   - Without version: `bdy artifact publish <name> ./dist` → creates `latest` version
4. Get URL: `bdy artifact version get <name> <version>`
5. Show the user the published URL, then ask via AskUserQuestion if they want to attach a custom domain. Options: claim one of the free domains available in Buddy, buy a new domain, or reuse one already in their workspace. Keep the option labels short — don't put CLI commands in them. After the user picks, run the relevant `bdy domain` command and wire it up with `bdy distro route create`.

### Critical Rules

- Main HTML file MUST be named `index.html` (otherwise serves directory listing)
- Use `@` or `:` as version separator: `my-site@1.0.0` or `my-site:1.0.0`
- Use `--force` to overwrite an existing version
- Use `--create` to create artifact and publish in one step: `bdy artifact publish -c <name>@1.0.0 ./dist`

### TIPS
- Use `bdy distro route create` for custom domain routing + cdn

## Tunnel (`bdy tunnel`)

Expose local services to the internet via secure tunnels.

### Critical Rules (MANDATORY)

- **ALWAYS** use `run_in_background: true` when running tunnel commands — they block execution
- **ALWAYS** ask about authentication via AskUserQuestion before creating HTTP tunnels:
  - HTTP Basic Auth → `-a`
  - Buddy Auth → `--buddy`
  - No auth → no flag
- For Docker: verify the app binds to `0.0.0.0`


### Tips

- Save tunnel configs: `bdy tunnel config add http <name> localhost:<port>`
- Start saved tunnel: `bdy tunnel start <name>`

## Domain (`bdy domain`)

Search, purchase, and manage custom domains.

```bash
bdy domain search <query>     # Search available domains
bdy domain buy <name>         # Purchase a domain
bdy domain list               # List owned domains
```

Run `bdy domain --help` for full options (TLD filters, sorting, etc.).

## Distribution (`bdy distro`)

Route traffic across services with custom rules and domains.

### Route Types

- **PROXY** / **PROXY_NO_CACHE** — reverse-proxy traffic to a backend. URL shows the distro domain, real paths (`/foo/bar`) are visible and forwarded. Use this for CDN/edge in front of a real app.
- **REDIRECT** — HTTP 3xx redirect to another URL. Browser navigates away; final URL shows the target domain.
- **CLOAKING** — the distro domain serves a single page that embeds the target as a full-page iframe. URL bar stays on the distro domain regardless of navigation inside the iframe, so the real paths/subpages are never visible

```bash
bdy distro create -i <name>                          # Create distribution
bdy distro route create <name> -t PROXY -d <domain>  # Add route
bdy distro route list <name>                          # List routes
```

Run `bdy distro --help` for full options.

## Pipeline (`bdy pipeline|pip`)

CI/CD pipelines for build, test, and deploy automation.

```bash
bdy pipeline list                          # List pipelines
bdy pipeline run start <identifier>        # Run a pipeline
bdy pipeline run status <identifier> <id>  # Check run status
bdy pipeline run logs <identifier> <id> <action-id>  # View logs
```

Run `bdy pipeline --help` for full options (variables, scheduling, YAML config, etc.).
