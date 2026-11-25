---
name: fix
description: Fixes the problems found by a vibecheck audit, one at a time and safest-first. Moves leaked keys server-side and walks the user through rotating them, adds Supabase RLS policies, locks down Firebase rules, adds server-side auth and ownership checks, rate limits and payment-webhook verification, then re-checks and shows the before → after Launch Score. Use after /vibecheck:check, or when the user asks to fix vibecheck findings, fix the security issues in the report, or "make it safe to launch".
argument-hint: "[finding-id | critical | high | all]"
---

# vibecheck fix

Turn the audit into a safe app without breaking it. Small, verified, reversible steps.

## 0. Load the findings

- Read `.vibecheck/report.md`, and `.vibecheck/deploy.md` for `VC-DEPLOY-*` findings. If neither exists, run the `check` skill in `quick` mode first (or `deploy`, if the user is fixing a deploy). Code changes since the report? Re-check each finding before touching it.
- Scope from `$ARGUMENTS`: a finding ID (`VC-DB-NO-RLS`), a severity (`critical`, `high`), or `all`. Default: every critical, then every high.
- Show the user the plan in plain words: which findings, what will change, what they'll need to do themselves (rotate keys, apply a migration, change a dashboard setting). Get a yes before editing.

## 1. Safety net first

- In a git repo with uncommitted changes: suggest committing or stashing first, so every fix is its own clean diff. Ask; don't commit for them unasked.
- No git: offer `git init` plus an initial commit. It's the undo button if a fix goes wrong. If they'd rather not, copy each file you'll change into `.vibecheck/backup-<finding-id>/` before editing it, and tell them where the copies are.

## 2. Fix one finding at a time

For each finding, in severity order:

1. **Re-read the code** around the finding. Understand the data flow before changing it.
2. **Say what you'll do** in one or two plain sentences.
3. **Make the smallest change that removes the root cause.** Follow the project's existing patterns, libraries and style. No drive-by refactors, renames or upgrades.
4. **Verify it**:
   - re-run the scanner (`node "${CLAUDE_SKILL_DIR}/../check/scripts/scan.mjs" --json`, or the copy wherever the `check` skill lives) and confirm the lead is gone;
   - run the project's type-check, lint and tests if they exist. Ask first if they're slow or call external services;
   - trace the original attack again by reading the new code. Does it fail now?
5. **Record it** in `.vibecheck/report.md`: `✅ FIXED: <what changed, files>` or `👤 NEEDS YOU: <exact steps>`.

New dependency needed (a rate limiter, zod, DOMPurify)? Name it and why, and ask before installing.

## 3. Never do this

- **Never "fix" by weakening**: no `using (true)`, no disabling RLS or rules, no removing a check that blocks the app, no catch-and-ignore, no deleting the feature, no moving a secret into a `NEXT_PUBLIC_`/`VITE_` var to "make it work".
- **Never rotate keys, change dashboard settings or run SQL against production yourself.** Write the migration and the steps; the user applies them.
- **Never rewrite git history or force-push** without an explicit yes, and only *after* the leaked key is rotated (rotation is what actually protects them).
- Never paste a secret into chat, the report or a commit message.
- **Stay inside the finding.** Don't edit files the fix doesn't need (other features, docs, build, QA or packaging scripts) without asking first. If something else should change, say what and why, and wait for a yes.
- **Don't restart, stop or redeploy** processes you didn't start. Running dev servers, workers and deployed apps keep the old code until they restart: tell the user what to restart, and that unsaved demo state may be lost.

## 4. Recipes

Details per stack are in the `check` skill's `references/stacks/*.md`. Read the matching file before fixing.

| Finding | Fix |
|---|---|
| Leaked secret (VC-KEY-*, VC-ENV-PUBLIC-SECRET, VC-ENV-TRACKED, VC-ENV-HISTORY) | 1) User revokes and recreates the key at the provider (give the dashboard location). 2) Store it in `.env` without a public prefix plus the host's env settings. 3) Move the code that uses it to the server. 4) Make sure `.gitignore` has `.env*` / `!.env.example`; `git rm --cached` tracked env files. 5) Optional, with consent: purge history with `git filter-repo --invert-paths --path <file>`, then force-push. |
| No RLS / open policy (VC-DB-*) | New migration in `supabase/migrations/<timestamp>_vibecheck_rls.sql`: enable RLS **and** add owner policies in the same file (RLS without policies makes the app look broken). Protect privileged columns. User applies it with `supabase db push` or the SQL Editor, then tests as a normal user. |
| Open Firebase rules | Owner-scoped rules (see `firebase.md`). User deploys with `firebase deploy --only firestore:rules,storage` and tests in the Rules Playground. |
| Missing auth / IDOR | Verify the session on the server at the top of the handler; scope queries with the user ID (`where: { id, userId }`); return 401 / 403 / 404. |
| No rate limit (VC-MONEY-NO-RATE-LIMIT) | Serverless: `@upstash/ratelimit`. Long-running Node: `express-rate-limit`. Python: `slowapi` / `flask-limiter`. Key by user ID, falling back to IP. Plus max tokens and an input cap. Remind the user to set provider spend limits. |
| AI called from the browser (VC-AI-BROWSER) | Server route with auth + rate limit + max tokens. The client calls the route. Remove `dangerouslyAllowBrowser`. |
| Unverified webhook / client price / success-URL grants (VC-PAY-*) | `constructEvent` on the raw body (or the provider's equivalent); fulfil from the webhook; look prices up by ID on the server; make the handler idempotent. |
| SQL injection / mass assignment | Parameterized queries; explicit field picking with zod. |
| XSS | Sanitize with DOMPurify, or render as text. |
| Deploy breakers (VC-DEPLOY-*) | Match the import to the file's exact letter case (and `git mv` a case-only rename); `npm install` undeclared packages and commit the lockfile; replace hardcoded localhost with an env var; listen on `process.env.PORT` and bind 0.0.0.0 in production; add `prisma generate` to the build; move SQLite or disk writes to a hosted database or object storage; one lockfile; one Node version. Env vars missing on the host are a "needs you" item: give the names, never the values. |
| Launch basics (VC-LAUNCH-*) | Generate a privacy policy and terms draft (mark them "review with a lawyer"), OG metadata, robots, sitemap, 404, favicon placeholder. Batch these in one step after the security fixes. |

## 5. Finish

Re-run the `check` skill in `quick` mode (or `full` if the user wants) and show the change:

```
🛠️ vibecheck fix: 31 → 86/100 · 🔴 NO-GO → 🟢 GO
✅ Fixed (7): VC-KEY-OPENAI, VC-DB-NO-RLS (messages), VC-PAY-WEBHOOK-UNVERIFIED, …
👤 Needs you (3):
  1. Rotate the OpenAI key: platform.openai.com → API keys
  2. Apply supabase/migrations/20261028_vibecheck_rls.sql (supabase db push)
  3. Set a monthly spend limit at OpenAI and Vercel
Then restart your dev server and redeploy, so the fixed code and new env vars are what actually runs.
```

Remind them a GO is only GO after the "needs you" items are done and the app is redeployed.
