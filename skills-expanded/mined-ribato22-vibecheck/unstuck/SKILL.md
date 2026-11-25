---
name: unstuck
description: Breaks the AI "fix loop", where the same bug keeps coming back, every fix breaks something else, or the agent keeps guessing. Stops editing, checkpoints the code, reproduces the bug, proves the root cause with evidence and one-change-at-a-time experiments, removes leftover failed fixes, and goes back to the last working version if that's faster. Use when the user says it's still broken, "same error again", "you keep going in circles", "nothing works", "it worked before", or after two or more failed attempts at the same problem.
argument-hint: "[what's broken]"
---

# unstuck: break the AI fix loop

Signs of a loop: the same error after two or more attempts; fixes that move the error somewhere else; edits to files unrelated to the symptom; "this should work now" without anyone seeing it work; a growing pile of try/catch, retries, `any`, `// @ts-ignore` and commented-out code.

**The rule that ends loops: no more edits until you can explain the bug with evidence.**

## 1. Freeze and take stock (no code changes)

- Write a short ledger: the symptom (exact error text and *where* it appears: browser console, terminal, server logs, hosting logs), each attempt so far, and what happened after it.
- Run `git status` and `git diff --stat`. How much has changed since the last commit?
- Offer a checkpoint: `git switch -c unstuck/<short-name>` plus a commit, so nothing is lost and you can compare. Ask first. No git? Say so: it's the #1 safety net for AI coding. Offer `git init`.

## 2. Reproduce it

- Get the exact steps and the exact error. Read the **full** stack trace and find the top frame in *their* code, not the library's.
- Make sure you're reading the right log. Server errors don't show in the browser console; browser errors don't show in the terminal; production errors live in the hosting dashboard (Vercel → Logs, Netlify → Functions, Supabase → Logs).
- Shrink it to the smallest repro: one command, one `curl`, one page, one test.

## 3. Was it ever working?

- Yes: `git log --oneline -20`, find the last good commit, `git diff <good>..HEAD --stat`. Often the culprit jumps out. For a long history, use `git bisect`.
- Works locally but not deployed: compare env vars, build-time vs runtime vars, URLs and ports, CORS, cookie domain, Node/Python version, and whether the database migration ran in production.

## 4. Clear the pile

Leftover changes from failed attempts hide the real bug and add new ones. List them and, with the user's OK, revert the ones that didn't help (`git restore -p`, or go back to the checkpoint). Work from the last known-good state plus the minimum change.

## 5. Hypotheses, then experiments

- Write down up to 3 hypotheses. For each: the evidence for it, the evidence against it, and **one cheap test that could prove it wrong** (log a value, `curl` the endpoint, check the response in the Network tab, print the installed version).
- Run one experiment at a time. Change one thing. Look at the result. Revert it if it didn't help.
- **Ground truth beats memory.** Check the installed version (`node_modules/<pkg>/package.json`, `pip show <pkg>`) and that version's docs or type definitions before assuming an API exists. AI-written code often targets another version, or calls functions that never existed.

## 6. Usual suspects in AI-built apps

| Symptom | Usual cause | Check |
|---|---|---|
| Works locally, broken in production | Env var missing or misnamed on the host; `NEXT_PUBLIC_`/`VITE_` values are baked in at build time (redeploy after changing); hardcoded `localhost` URL | The host's env settings; rebuild |
| Supabase returns `[]` or `null` with no error | RLS blocking: no policy matches this user, or the server client has no session | Run the query in the SQL Editor; read the policies; log `auth.getUser()` on the server |
| "Not authenticated" on the server but logged in in the browser | Cookies or session not passed to server code (SSR client not set up, different domain or port) | Look at the cookies on the actual request |
| CORS error | The *server's* response headers, often an error page without headers | Network tab: status code and response of the failing request |
| The change has no effect | Stale cache, dev server not restarted, wrong file or folder, service worker, CDN, Next.js cache | Add a deliberate `console.log("HERE")` to prove the code even runs |
| Hydration mismatch | `Date`, `Math.random`, `window` or `localStorage` used during render; invalid HTML nesting | Move to `useEffect`; fix the nesting |
| Module not found / wrong types | Package not installed, wrong import path, ESM/CJS mix, a hallucinated package or API | `npm ls <pkg>`; read the package's exports |
| Infinite re-render / request loop | `useEffect` dependencies; setting state during render; a new object in the deps every render | React DevTools; log each render |
| Webhook never arrives locally | It needs a tunnel (`stripe listen --forward-to …`); signature fails because the body was parsed first | Use the provider CLI; verify against the raw body |
| Migration "worked" but the app is broken | Applied to a different database or environment than the app uses | Compare the connection strings / project refs |
| 500 with no details | The real error is only in server logs | Read the server/hosting logs; log the caught error |
| AI API error | Wrong model ID, key from another project, quota or billing limit reached | The provider's dashboard and error body |
| Python import / version errors | Wrong virtualenv or interpreter | `which python`, `pip -V` |

## 7. Escalate instead of looping

After two failed experiments, zoom out: re-read the original symptom, question the assumption about *where* the bug is, search the exact error message together with the library version, read the library's source or types, or rebuild the feature smaller from the last good commit. Tell the user plainly when you need something only they have: hosting logs, dashboard settings, the exact click path.

## 8. Fix, prove and report

Once the root cause is proven: make the minimal fix, show the repro passing, remove debug logs and leftover attempt code.

```
🧭 unstuck
Root cause: … (evidence: …)
Fix: … (files)
Proof: the repro now … (command or steps)
Cleaned up: reverted N leftover changes from earlier attempts
Avoid next time: …
```

Offer to add a one-line lesson to `CLAUDE.md` / `AGENTS.md` (for example "Supabase returns [] when RLS blocks: check policies before changing queries") so future sessions don't repeat the loop. Ask first.
