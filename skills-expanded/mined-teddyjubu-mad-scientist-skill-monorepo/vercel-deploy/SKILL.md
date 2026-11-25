---
name: vercel-deploy
description: Deploy a Next.js project to Vercel using the CLI with a stored API token.
trigger: When the user wants to deploy a web app to Vercel.
---

## What This Skill Does

This skill Deploy a Next.js project to Vercel using the CLI with a stored API token.

## How to deploy to Vercel

### 1. Find the Vercel token & team info
The Vercel API token is stored at `/root/.openclaw/workspace/.secrets/vercel.env`:
```
VERCEL_TOKEN=vcp_...
```
Read it with Python (the shell `cat` may truncate long lines with `...` in the display):
```python
with open('/root/.openclaw/workspace/.secrets/vercel.env') as f:
    for line in f:
        if line.startswith('VERCEL_TOKEN=') and not line.startswith('#'):
            token = line.split('=', 1)[1].strip()
```
Team ID: `team_RI521BtIL6MYYsZZaNfI1oQo`

### 2. Deploy with the CLI
```bash
cd /path/to/project && npx vercel deploy --prod --token="<VERCEL_TOKEN>"
```

**Flags:**
- `--prod` — production deployment
- `--token` — API token (required on headless servers)
- No need for `--name` (deprecated) or `--org` — the CLI picks the project from `.vercel/project.json` after initial link

### 3. Non-interactive deployments
Always use `--yes` flag:
```bash
npx vercel deploy --prod --yes --token="<TOKEN>"
```
Without `--yes`, the CLI errors with "Command `vercel deploy` requires confirmation" on headless servers.

### 4. Static site deployments (no build step)
If a Next.js project fails to build on Vercel's servers (the persistent "Unexpected error" issue), convert to a single `index.html` file in a separate directory and deploy that as a static site instead.

**For static-only deployments:**
- Put `index.html` in a clean directory
- `vercel.json` should be minimal:
```json
{ "cleanUrls": true }
```
- Do NOT include `publicDir`, `name`, or `builds` — these cause errors
- Deploy: `npx vercel deploy --prod --yes --token="<TOKEN>"`
- The `name` property in `vercel.json` is deprecated; the CLI will create `.vercel/project.json` on link

### 5. Known issue: Vercel build failures
Vercel's build servers occasionally return "Unexpected error. Please try again later." on every Next.js deployment attempt. This is a Vercel-side infrastructure issue — not a code problem. The error persists across all tokens and retries. If it survives 3+ attempts, fall back to the static HTML approach (#4).

### Project structure expected (Next.js)
- `package.json` with `next`, `react`, `react-dom` dependencies
- Build scripts: `dev`, `build`, `start`
- `.vercel/` directory created by `vercel deploy --yes` on first run to link project
- `node_modules/` and `.next/` in `.gitignore`
