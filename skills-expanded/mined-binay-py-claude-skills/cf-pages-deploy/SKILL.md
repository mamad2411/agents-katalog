---
name: cf-pages-deploy
description: Deploy a static site or single HTML file to Cloudflare Pages safely and verify it is live. Stages a clean copy (no .env, node_modules, README, keys), scans for secrets, creates the project if asked, deploys to production or a preview branch, then checks the live file matches byte for byte. Use for any "deploy/redeploy this to Cloudflare Pages / pages.dev" request.
---

# cf-pages-deploy

`scripts/deploy.mjs` is zero-dependency Node 22+ and calls `npx wrangler`. Run `npx wrangler whoami` first; if it says you're not logged in, ask the user to run `npx wrangler login`.

```
node deploy.mjs --project my-site --dir ./public --dry-run     # ALWAYS first: shows exactly what goes live
node deploy.mjs --project my-site --dir ./public               # production (branch main), verified
node deploy.mjs --project my-site --dir . --include "index.html,*.css,*.js,assets/**"
node deploy.mjs --project my-site --dir dist --build "npm run build"
node deploy.mjs --project new-site --dir dist --create         # make the project if missing
node deploy.mjs --project my-site --dir dist --branch preview  # preview URL; production untouched
```

## Rules
- Run `--dry-run` and read the file list before the first deploy of any folder. Everything uploaded is public.
- Prefer `--include` for project folders that mix site and source files. A single-file site is `--include index.html`.
- Excluded by default: `.git`, `node_modules`, `.wrangler`, `.env*`, `.dev.vars`, keys/certs, `*.md`, `package*.json`, lockfiles, `wrangler.*`, OS junk, logs and databases. They stay out under `--include` too (`*.js` doesn't reach into `node_modules`) unless `--include` names the exact path, and `--exclude` still applies.
- The secret scan reads every non-binary file that would go live, whatever its extension.
- A secret found in a file that would go public stops the deploy. Never pass `--allow-secrets` unless the user confirms the value is meant to be public (e.g. a browser-restricted Maps key).
- `--create` only when the user wants a NEW project. Look up existing names first with `npx wrangler pages project list`.
- Production deploys replace the live site. Confirm with the user unless they asked for a deploy/redeploy.

## Gotchas this script handles
- **Real URL ≠ project name.** Pages may add a suffix (`my-game-28c.pages.dev`). The script reads the domain from `wrangler pages project list --json`; report that URL, not a guessed one.
- **wrangler 4.15x+ `pages project create`** delegates to "Pages in Workers" and can fail ("Could not detect a directory containing static files") or create a Worker instead. The script passes the hidden `--force` flag to create a classic Pages project. Only creation needs it.
- `--branch main` = production. Any other branch = preview deployment at `https://<hash>.<project>.pages.dev`.
- Unknown paths return HTTP 200 with `index.html` (SPA fallback), so a 200 on `/.env` doesn't mean it leaked. Check the body.
- Limits: 25 MiB per file, 20,000 files per deployment.
- Redirects/headers: put `_redirects` / `_headers` files in the site root. They're deployed as-is.
- Verification retries for ~60 s. If it still fails, the edge may be slow. Report the deployment URL and re-check; don't redeploy blindly.
