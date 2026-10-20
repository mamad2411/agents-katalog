---
name: github-pages-iteration
description: "Update a live GitHub Pages site (push conflicts, CDN lag)."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [github-pages, deployment, iteration, cdn-cache, git-rebase, website-landlord, <you>-solutions]
    triggers: [update-existing-github-pages-site, push-rejected-fetch-first, github-pages-stale-content, deploy-<you>, project-sites-deploy, cdn-cache-lag, redeploy-static-site]
    related_skills: [static-site-deployment, website-landlord-operations]
---

# GitHub Pages Iteration (updating a live site)

Workflow for pushing UPDATES to a site already deployed on GitHub Pages, especially the shared `pmb2/project-sites` repo that hosts many sites (the company, Website Landlord demos, motion sites). Initial setup lives in `static-site-deployment`; this covers the iterate loop.

## The one-command deploy script pattern

Keep a `deploy-<site>.sh` in the site's project dir. It copies files into a sibling clone of the deploy repo, commits, pushes, polls the Pages build, and verifies the live URL:

```bash
SITE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPLOY_REPO="${SITE_DIR}/../../project-sites-deploy"   # sibling of Projects/, NOT site dir
cp "${SITE_DIR}/index.html"  "${DEPLOY_REPO}/<you>-solutions/index.html"
mkdir -p "${DEPLOY_REPO}/<you>-solutions/scan"
cp "${SITE_DIR}/scan.html"   "${DEPLOY_REPO}/<you>-solutions/scan/index.html"
cd "${DEPLOY_REPO}" && git add <you>-solutions/
git -c user.name='<you>' -c user.email='<you>@users.noreply.github.com' commit -m "$1"
git push origin HEAD
sleep 20  # give Pages time to start the build
```

**Path gotcha:** if the site lives at `Projects/<site>/` and the deploy clone at `<home>/project-sites-deploy/`, the relative path is `../../project-sites-deploy` (up to Projects/, then up to home). A single `../` silently resolves to `Projects/project-sites-deploy` and the script fails the sanity check — verify with `readlink -f` before trusting the script.

Subdirectory deploys: any `<slug>.html` becomes `<repo>/<site>/<slug>/index.html`. Removing a page = `git rm -r <site>/<slug>` and push (old URL 404s after rebuild).

## Push rejected: fetch first (shared repo)

The `pmb2/project-sites` repo gets pushes from OTHER workstreams (motion-site demos, video fixes) between your commits. Expect `! [rejected] HEAD -> main (fetch first)` on roughly half of deploys — it is normal, not an error.

```bash
cd <deploy-repo> && git pull --rebase origin main && git push origin HEAD
```

Rebase (not merge) keeps history linear; conflicts are rare since each site lives in its own directory. After rebasing, confirm your file survived: `git log --oneline -4` and diff the site dir.

## CDN cache lag: the verification sequence

After a push, the Pages build and the CDN cache BOTH lag. The live URL can serve the OLD file even after the API reports "built". Three sources, three truths:

| Source | What it proves | Always current? |
|---|---|---|
| `raw.githubusercontent.com/<owner>/<repo>/main/<path>` | repo truth — did the push land | YES, instantly |
| `gh api repos/<owner>/<repo>/pages/builds --jq '.[0].status'` | build state: `building` → `built` | YES |
| `https://<user>.github.io/<repo>/<path>` | what users actually see | NO — CDN cache |

Correct order:
1. Verify raw URL has the new content (if not, the push failed — fix before anything else)
2. Poll builds until `built` (usually 1-4 checks at 10-12s)
3. Fetch the live URL with a cache-busting query param and compare bytes/title to the raw file: `curl -sL -H 'Cache-Control: no-cache' '.../<you>-solutions/?v=<timestamp>'`
4. If live still shows old bytes AFTER the build reports `built`, wait ~30-60s and re-curl — the CDN catches up; do not re-push to "fix" it

Verification without trusting the CDN: `curl -sL <raw-url> | grep -c '<new-marker>'` (e.g. a unique string from the new copy) vs the same grep on the live URL.

## Single-file HTML: DOM must precede the inline script

When adding modal/section markup to a single-file site, the new HTML must appear BEFORE the `<script>` block, or the IIFE runs before the elements exist and throws `Cannot read properties of null (reading 'addEventListener')`. Symptom: buttons do nothing, console shows null-element errors.

- Verify order programmatically: `data.index('<!-- Booking modal') < data.index('<script>')`
- Careful with `data.index('<script>')`: `<script type="application/ld+json">` does NOT match the exact string `<script>` (needs the closing `>` immediately), so JSON-LD in the head is safe — but confirm placement with context output anyway.
- When relocating a large block, do it in Python (extract slice → remove → reinsert) rather than hand-reproducing the HTML in a patch string.
- After any JS/markup change, drive the interaction in the browser (click, phase switches, Escape close) — a clean console is the pass criterion. Note: Chrome DevTools MCP in a throttled background tab can time out on screenshots and miss scroll-driven reveals; DOM assertions via evaluate_script are the reliable verification.

## Graceful fallbacks for config-gated features

When a feature needs user-owned credentials (Stripe payment link, Calendly/cal.diy URL), build it to render fallbacks when the config value is empty (e.g. mailto link + "being finalized" note), and centralize the URLs in a single `TBA_CONFIG` object at the top of the inline script. Test BOTH states: empty config (fallbacks visible) and simulated configured state (widget loads, button href correct) via evaluate_script.
