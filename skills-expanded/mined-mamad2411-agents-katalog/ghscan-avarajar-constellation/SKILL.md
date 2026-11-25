---
description: Open the visual web UI to select your tech stack, then generate a fully functional project with AI
---

# Constellation — Interactive Project Generator

You are the Constellation project generator. Follow these steps in order.

## Step 1: Launch Web UI and Wait for Blueprint

Run Constellation in interactive mode. This opens the web UI and blocks until the user finishes configuring their stack.

```bash
npx @avarajar/constellation@latest web --wait 2>/dev/null | tail -1
```

Run this with a 600000ms timeout. The command:
1. Starts the web server at http://localhost:3210
2. Opens the browser automatically
3. Blocks until the user clicks "Send to Claude Code"
4. Outputs the blueprint file path as the last line of stdout
5. Shuts down the server

Capture the last line of output — that is the absolute path to the blueprint YAML file.

## Step 2: Read and Parse the Blueprint

Read the blueprint YAML file from the path captured in Step 1.

Parse and understand every section:
- `project.name`, `project.description`, `project.outputDir`
- `stack.frontend` (framework, CSS, build tool, state management, **package manager**)
- `stack.backend` (framework, language, runtime, **package manager**)
- `stack.database`, `stack.infrastructure`, `stack.testing`, `stack.monitoring`
- `generation.crudEntity`, `generation.crudFields`, `generation.features`
- `generation.docker`, `generation.ci`
- `github.mode`, `github.org`, `github.repoName`, `github.existingRepo`
- `versions` — the dynamically fetched latest versions for all selected technologies

If the blueprint doesn't specify a package manager, ask the user:
- **Frontend**: npm, yarn, pnpm, or bun?
- **Backend (Python)**: pip, uv, poetry, or pipenv?
- **Backend (Node.js)**: npm, yarn, pnpm, or bun?

Summarize the blueprint briefly, then proceed to Step 3.

## Step 3: Fetch Latest Package Versions

**THIS STEP IS MANDATORY. DO NOT SKIP IT.**

Your training data has outdated package versions. You MUST run commands to get the real current versions BEFORE generating any code.

Based on the selected technologies in the blueprint, run the appropriate commands:

**For Python packages** (if Django, Flask, FastAPI, etc. selected):
```bash
for pkg in django djangorestframework django-cors-headers gunicorn redis sentry-sdk flask fastapi uvicorn sqlalchemy; do
  ver=$(curl -s "https://pypi.org/pypi/$pkg/json" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin)['info']['version'])" 2>/dev/null)
  [ -n "$ver" ] && echo "$pkg==$ver"
done
```

**For Node.js packages** (if React, Vue, Next.js, Express, etc. selected):
```bash
for pkg in react react-dom vue svelte next nuxt astro @angular/core solid-js tailwindcss vite webpack esbuild express fastify hono @nestjs/core prisma typeorm sequelize jest vitest cypress @playwright/test @sentry/node zustand @reduxjs/toolkit pinia axios typescript; do
  ver=$(npm view "$pkg" version 2>/dev/null)
  [ -n "$ver" ] && echo "$pkg@$ver"
done
```

**For Go modules** (if Gin, Echo, Chi selected):
```bash
for mod in github.com/gin-gonic/gin github.com/labstack/echo/v4 github.com/go-chi/chi/v5; do
  ver=$(curl -s "https://proxy.golang.org/$mod/@latest" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('Version',''))" 2>/dev/null)
  [ -n "$ver" ] && echo "$mod@$ver"
done
```

**For Rust crates** (if Actix, Axum, Rocket selected):
```bash
for crate in actix-web axum rocket; do
  ver=$(curl -s "https://crates.io/api/v1/crates/$crate" -H "User-Agent: constellation" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin)['crate']['max_version'])" 2>/dev/null)
  [ -n "$ver" ] && echo "$crate=$ver"
done
```

Only run the commands relevant to the selected stack. Save ALL the version output — you will pass it to sub-agents.

## Step 4: Generate the Project

Create the project directory:
```bash
mkdir -p <outputDir>
```

For each non-null stack section, spawn a sub-agent. **Run all applicable agents in parallel.**

| Blueprint section | Condition |
|---|---|
| Frontend agent | `stack.frontend.framework` is not null |
| Backend agent | `stack.backend.framework` is not null |
| Database agent | `stack.database.primary` is not null |
| Infrastructure agent | containerization or cicd or cloud is not null |
| Testing agent | any testing tool is not null |
| Monitoring agent | any monitoring tool is not null |
| Security agent | always spawn (when backend exists) |
| Common agent | always spawn |

**IMPORTANT: In each sub-agent's prompt, include:**
1. The full blueprint YAML text
2. The EXACT version list from Step 3
3. This instruction: "Use ONLY the versions listed below. Do NOT use versions from your training data — they are outdated."

Each sub-agent should follow the instructions in its corresponding skill file (constellation:frontend, constellation:backend, etc.) but MUST use the versions you provide.

## Step 5: Verify

After all agents complete:
- Check that key files exist (package.json or equivalent entry points, main source files)
- **Spot-check dependency versions**: pick 3 packages from requirements.txt or package.json and verify they match the versions from Step 3. If they don't, fix them immediately.
- If TypeScript, attempt `npx tsc --noEmit` in relevant directories
- Verify `make dev` or `scripts/dev.sh` exists
- Fix any issues found
- Report a brief summary of what was generated

## Step 6: Git + GitHub

Read the `github` section from the blueprint.

If `github.mode` is **"new"**:
```bash
cd <outputDir>
git init
git add -A
git commit -m "Initial project scaffolding via Constellation"
```
Then ask the user if they want the repo **public or private**, and create it:
```bash
gh repo create <org-or-user>/<repoName> --source . --push --private
```

If `github.mode` is **"existing"**:
```bash
cd <outputDir>
git add -A
git commit -m "Add Constellation-generated project scaffolding"
git push
```

If `github.mode` is **"none"**: skip this step.

Report the repo URL if applicable.

## Step 7: Final Summary

Show the user:

> **Project generated successfully!**
>
> - **Name:** (project name)
> - **Path:** (output directory)
> - **Repo:** (repo URL or "local only")
> - **Stack:** (brief summary with versions)
>
> **Quick start:**
> ```bash
> cd <outputDir>
> make setup   # Install deps, create .env, run migrations, seed data
> make dev     # Start all services locally
> ```
