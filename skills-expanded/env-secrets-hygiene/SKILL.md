---
name: env-secrets-hygiene
description: Audit a project for leaked secrets (grep patterns across working tree AND git history), set up .env/.gitignore correctly, and run rotation when a key has leaked. Use when the user says "did I leak a key", "secret scan", "set up my .env", "I committed my API key", or before making a repo public. Don't use for checking what ships in the deployed client bundle — use vercel-deploy-check.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Builder Dev, Security, Secrets, Environment]
    related_skills: [vercel-deploy-check, supabase-migration-writer, git-ship-flow, api-endpoint-tester]
---

# Env & Secrets Hygiene

Finds leaked keys, fixes the setup that leaked them, and runs the only response that actually works. The iron rule: **leaked = rotate immediately — deleting the file or the commit is not enough.** The key lives on in git history, forks, clones, CI logs, and scrapers' databases; bots harvest keys from public pushes in under a minute. Rotation is the fix; cleanup is just tidying.

## When to Use

- "I think I committed my API key" / a provider emailed about an exposed key.
- New project needs `.env` / `.env.example` / `.gitignore` set up right.
- Pre-flight before making a repo public or sharing it.
- **Not for:** secrets baked into the deployed client bundle — use `vercel-deploy-check` (but the rotation rule here still applies to whatever it finds).

## Quick Reference

| Action | Command / Call |
|---|---|
| Scan working tree | `grep -rniE "(sk_live_\|sk_test_\|sk-proj-\|sk-ant-\|ghp_\|gho_\|AKIA[0-9A-Z]{16}\|service_role\|-----BEGIN( RSA)? PRIVATE KEY)" . --exclude-dir={.git,node_modules,.next,dist}` |
| Generic assignments | `grep -rniE "(api[_-]?key\|secret\|password\|token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}" . --exclude-dir={.git,node_modules,.next,dist}` |
| Scan ALL git history | `git log -p --all \| grep -nE "(sk_live_\|sk-proj-\|sk-ant-\|ghp_\|AKIA\|service_role\|BEGIN.*PRIVATE KEY)" \| head -40` |
| Is .env tracked? | `git ls-files \| grep -E "^\.env" ` (any output = it's in the repo) |
| Is .env ignored? | `git check-ignore -v .env` (no output = NOT ignored) |
| Stop tracking, keep file | `git rm --cached .env` |
| History rewrite (last resort) | `git filter-repo --invert-paths --path .env` (needs `pip install git-filter-repo`; destructive — gate behind confirm) |

## Procedure

1. **Precheck** — `command -v git grep`; confirm the repo path and whether it's public, private, or about to be shared (raises the stakes, changes nothing about the method).
2. **Scan** — run all three scans from Quick Reference: working tree (high-signal prefixes), generic assignments, and full git history. The history scan is the one people skip and the one that matters — a key deleted three commits ago is still fully visible.
3. **If anything real is found → rotation protocol, immediately, before any cleanup:**
   1. **Rotate now** — new key at the provider, old key revoked: Stripe dashboard → API keys → roll; OpenAI/Anthropic → delete key, create new; GitHub → Settings → Developer settings → revoke token; Supabase `service_role` → project settings → API → rotate; AWS → IAM → deactivate access key. Minutes matter on public repos.
   2. **Update every consumer** — local `.env`, Vercel (`vercel env rm NAME production && vercel env add NAME production`), CI secrets, teammates. Verify the app still works with the new key.
   3. **Check for abuse** — provider usage dashboard / billing for the exposure window; unexpected activity → provider support + note in the incident line of the report.
   4. **Then clean up** — only after rotation: fix tracking (step 4), and optionally rewrite history (step 5). Say it plainly to the user: the old key is dead, so history cleanup is hygiene, not security.
4. **Set up the plumbing** — make leaks structurally hard:
   - `.gitignore` contains `.env` and `.env*.local` (append if missing); verify with `git check-ignore -v .env`.
   - If `.env` is tracked: `git rm --cached .env && git commit -m "chore: stop tracking .env"` — file stays locally, leaves the index.
   - Create `.env.example` mirroring every var with placeholders (`STRIPE_SECRET_KEY=sk_test_your_key_here`) — this is what gets committed and documented (`docs-readme-writer`).
   - Code reads keys only via `process.env` / `os.environ` — grep for hardcoded literals and replace.
5. **History rewrite (optional, destructive, confirm required)** — only worth it for private repos going public or org policy. `git filter-repo` rewrites every sha: coordinate with anyone who has a clone, take a backup clone first, and require explicit user confirmation before running and before the forced push that follows. Never present this as an alternative to rotation.
6. **Deliver** — report via the template; re-run all scans to show clean.

## Output Template

```
## Secrets Audit — <repo> — <date>
Scans: working tree ✅ | generic patterns ✅ | full git history ✅

Findings:
| # | Secret type | Location | In history? | Status |
|---|---|---|---|---|
| 1 | Stripe sk_live | .env @ commit a1b2c3d | yes | ROTATED ✅ old key revoked <time> |

Abuse check: <provider dashboard reviewed — none found / details>
Plumbing: .gitignore ✅  .env untracked ✅  .env.example ✅  no hardcoded keys ✅
History rewrite: not needed / done with user confirm (backup at <path>)
Rule applied: leaked = rotate immediately — deleting the commit is not enough.
```

## Pitfalls

- **"I deleted the commit, we're safe"** — the single most dangerous belief in this domain. The key persists in reflog, remotes, forks, clones, and scraper caches. Recovery: rotate anyway, every time, no exceptions; then clean up if desired.
- **Rotating but missing a consumer** — prod goes down because Vercel still holds the dead key. Recovery: before revoking, list every place the old key lives (grep + `vercel env ls` + CI settings); update all, verify the app, then revoke — or revoke first only when actively being abused.
- **False positives flood the report** — `PASSWORD_MIN_LENGTH = 8` matches the generic pattern. Recovery: eyeball every generic-pattern hit; only real credential values go in the findings table. High-signal prefixes (sk_live, AKIA, ghp_) are near-zero false positive — treat those as real.
- **`.env` in `.gitignore` but already tracked** — gitignore doesn't untrack existing files; every edit keeps committing. Recovery: `git rm --cached .env`, commit, and scan history for what already leaked.
- **filter-repo run without coordination** — every collaborator's clone breaks against rewritten history. Recovery: backup clone first, explicit confirm, teammates re-clone after; if it went wrong, the backup clone restores the old history.

## Verification

- [ ] All three scans ran (tree, generic, full history) and final re-run is clean of real secrets
- [ ] Every found key ROTATED at the provider — not merely deleted from files
- [ ] All consumers updated with new keys; app verified working
- [ ] Provider usage reviewed for the exposure window
- [ ] `.env` untracked + ignored; `.env.example` uses placeholders only
- [ ] Any history rewrite had explicit confirm + backup clone
- [ ] No secret values echoed into this transcript or the report (types + locations only)
