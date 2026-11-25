---

name: vercel-site-deploy
description: Create and deploy websites to Vercel — static HTML workflow that avoids build errors
category: web

---
When asked to create and deploy a website, follow this exact process.

## What This Skill Does

This skill Create and deploy websites to Vercel — static HTML workflow that avoids build errors.

## Next.js Deployment (alternative to static HTML)

When the user specifically wants a Next.js deployment (not a static site), use the `vercel-deploy` skill's guidance with these specifics:

### Vercel Token & Team Info
The Vercel API token is stored at `/root/.openclaw/workspace/.secrets/vercel.env`:
```
VERCEL_TOKEN=...
```
Read it programmatically — the shell `cat` may truncate long lines:
```python
with open('/root/.openclaw/workspace/.secrets/vercel.env') as f:
    for line in f:
        if 'VERCEL_TOKEN' in line and not line.startswith('#'):
            token = line.split('=', 1)[1].strip()
```
**Team ID:** `team_RI521BtIL6MYYsZZaNfI1oQo`

### Deploy Next.js App
```bash
cd /path/to/project && npx vercel deploy --prod --yes --token="<TOKEN>"
```

**Flags:**
- `--prod` — production deployment
- `--yes` — non-interactive (required on headless servers)
- `--token` — API token (required on headless servers)
- No need for `--name` (deprecated) or `--org` — CLI picks project from `.vercel/project.json` after initial link

### Known Issue: Vercel Build Failures
Vercel's build servers occasionally return "Unexpected error. Please try again later." on every Next.js deployment attempt. This is a Vercel-side infrastructure issue — not a code problem. If it survives 3+ attempts, fall back to the static HTML approach (single `index.html` in a clean directory, no build step).

### Project structure expected (Next.js)
- `package.json` with `next`, `react`, `react-dom` dependencies
- Build scripts: `dev`, `build`, `start`
- `.vercel/` directory created by `vercel deploy --yes` on first run
- `node_modules/` and `.next/` in `.gitignore`

---

## Static HTML Site Deployment (DEFAULT)

## Workflow

### 1. Create the Project
```bash
mkdir -p /root/projects/<project-name>
```

### 2. Write the Site
Create a single `index.html` file with everything inline:
- CSS in `<style>` tags
- JavaScript in `<script>` tags
- Google Fonts loaded directly in `<head>`
- Use modern design patterns: gradients, glass-morphism, CSS animations, scroll-reveal via IntersectionObserver

### 3. Deploy to Vercel

```bash
cd /root/projects/<project-name>
npx vercel deploy --prod --yes --token="<TOKEN>"
```

Where `<TOKEN>` is read from `~/.openclaw/workspace/.secrets/vercel.env` (look for `VERCEL_TOKEN=` line).

**Team:** `team_RI521BtIL6MYYsZZaNfI1oQo`

The CLI will auto-link to the team's Vercel org and deploy. No `vercel.json` needed — Vercel auto-detects static HTML.

### 4. Provide the URL
The deploy output will show two URLs. Give the user the **aliased/production URL** (the clean one, e.g., `https://projectname.vercel.app`), NOT the preview URL with random suffixes.

### 5. Verify It's Live
```python
import urllib.request
resp = urllib.request.urlopen("https://<domain>", timeout=10)
print(resp.status)
```
Confirm 200 and content length matches the index.html file size.

## Troubleshooting

- **"Invalid vercel.json" error**: Remove `vercel.json` entirely. Static HTML doesn't need it.
- **"Unexpected error" during build**: This is a Vercel server-side issue with Next.js/Framework builds. Switch to static HTML single-file deploy.
- **"Requires confirmation"**: Add `--yes` flag.
- **If deploy succeeds but site shows 404**: The output directory may be wrong. Vercel defaults to `.` for static sites — make sure `index.html` is at the project root.
- Never use `--name` flag (deprecated).
- If token in `.secrets/vercel.env` contains literal `...` (truncated display), read it programmatically to get the real value.

## Design Standards
- Modern UI: gradients, smooth transitions, scroll animations, glass-morphism cards
- Mobile-responsive via CSS media queries
- Google Fonts (Inter, or similar)
- Professional typography with proper hierarchy
- Clear CTAs with pulse/shimmer effects
- Testimonials, benefits, how-it-works sections for business sites