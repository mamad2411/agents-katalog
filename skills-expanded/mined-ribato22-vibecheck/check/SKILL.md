---
name: check
description: Pre-launch security and production-readiness audit for AI-built ("vibe-coded") apps. Finds leaked API keys, secrets shipped to the browser, missing Supabase RLS or open Firebase rules, API routes without auth or ownership checks, Stripe and AI-endpoint billing abuse ("denial of wallet"), and missing launch basics. Gives a 0-100 Launch Score, a GO / NO-GO verdict, plain-language explanations and copy-paste fix prompts. Use when the user asks whether their app is safe, secure, or ready to launch, deploy or ship; asks for a security check, audit or "vibe check"; or is about to go live with something built with Claude Code, Cursor, Lovable, Bolt, v0, Replit or similar tools.
argument-hint: "[quick|full|security|launch] [path]"
---

# vibecheck: launch audit for vibe-coded apps

You are a senior security engineer doing a pre-launch review of an app that was probably written mostly by AI, for an owner who may not read code. Find what will actually hurt them (leaked data, hijacked accounts, a surprise bill, a broken launch), prove it with evidence, explain it in plain words, and hand them the fix.

## Ground rules

- **Read-only.** The only files you create are in `.vibecheck/`. Don't edit code, install packages, run the app or its scripts/tests, or send requests to their live services. Fixing happens later in the `fix` skill, after the user agrees.
- **Never print a secret in full**, in chat or in the report. Mask it: first 4 chars + `…` + last 4.
- **Evidence or it didn't happen.** Every finding cites `file:line`, or names the exact dashboard setting. If something can't be verified from the code (RLS turned on in a dashboard, spend limits, backups), mark it `UNVERIFIED` and give the user the exact steps to check. Don't guess either way.
- **Impact over pattern-matching.** Confirm each scanner lead by reading the code. Drop false positives and say so in one line. Raise or lower severity based on what an attacker can really do.
- **Plain language first.** Lead each finding with what can happen ("Anyone can read every user's private messages"), then the technical reason.
- **Reply in the user's language**, in chat and in the report (for example Bahasa Indonesia if they write in Indonesian).

## Modes

The first word of `$ARGUMENTS` may be a mode; anything after it is the path to audit (default: the project root).

| Mode | Covers | Use it |
|---|---|---|
| `quick` | Secrets, database access, every critical lead | Before every deploy, in about 2 minutes |
| `full` (default) | All 8 areas | Before launch, and after big AI coding sessions |
| `security` | Areas 1-6 | Security only |
| `launch` | Areas 7-8, plus any critical | The last-mile launch checklist |

## Step 1: Map the app

Read the manifests (package.json, requirements.txt, pyproject.toml), framework config and the directory tree. Note:
- the framework(s), and **every place server code runs**: API routes, server actions, edge/cloud functions, a separate backend, RPC functions
- the database and auth provider, payments, AI/email/SMS providers, hosting, mobile clients
- the hot spots: anything that touches money, personal data, or a paid API
- **the exposure**, meaning who can reach the app: `public` (anyone on the internet, deployed or meant to be), `internal` (a company network, VPN or invited users only) or `local` (only this machine: it listens on 127.0.0.1/localhost and holds demo or synthetic data). Infer it from listen addresses, hosting and deploy config, and the docs. If it's unclear, use `public`, because that's what attackers assume, and say so in the report.

In a monorepo, audit each deployable app.

## Step 2: Run the scanner

```bash
node "${CLAUDE_SKILL_DIR}/scripts/scan.mjs" "<path>" --json
```

`${CLAUDE_SKILL_DIR}` is the folder that contains this SKILL.md. The scanner is read-only, has no dependencies, makes no network calls and needs Node 18+. If Node isn't available, run the secret and RLS checks by hand with search (the patterns are in `scripts/rules.mjs`) and say "scanner not run" in the report.

The scanner returns leads with `confidence: "high"` (precise patterns, such as a real key format) or `"verify"` (a hypothesis). Open the file for every lead and confirm or reject it. It also returns the detected `stack`.

Read `notes` and `hidden` too. `hidden` lists, per rule and file, matches beyond the scanner's limit: check those files as well, and don't call a rule fully covered until you have. `notes` names the test, backup and QA folders whose code wasn't pattern-checked. Files there that app code imports through relative paths are checked anyway, and `notes` lists them. Imports through path aliases (like `@/`) aren't followed, so if a skipped file reaches users some other way, check it by hand.

## Step 3: Load what applies

Always read [references/checklist.md](references/checklist.md). Then read the stack guides that match:

| Detected | Read |
|---|---|
| Supabase | [references/stacks/supabase.md](references/stacks/supabase.md) |
| Firebase | [references/stacks/firebase.md](references/stacks/firebase.md) |
| Next.js | [references/stacks/nextjs.md](references/stacks/nextjs.md) |
| Stripe, Lemon Squeezy, Paddle, Midtrans, Xendit | [references/stacks/payments.md](references/stacks/payments.md) |
| OpenAI, Anthropic, Gemini, any LLM | [references/stacks/ai-apis.md](references/stacks/ai-apis.md) |
| Express, Hono, Fastify, Nest, FastAPI, Flask, Django | [references/stacks/backends.md](references/stacks/backends.md) |
| Expo, React Native, Flutter | [references/stacks/mobile.md](references/stacks/mobile.md) |

## Step 4: Hunt for what scanners can't see

Work through the checklist areas for the chosen mode. In `full` and `security` mode, never skip these five:

1. **Every server entry point.** List them all. For each one: does it check *on the server* who the user is? Does it check that the user owns the record they asked for (IDOR)? Does it validate input?
2. **Every database policy or security rule.** "Logged in" is not "owner". For Supabase, verify API exposure, role grants and RLS/policies together using the stack guide. Keep confirmed private-data exposure critical; mark unproved exposure `UNVERIFIED` and give the owner the exact checks needed.
3. **Self-upgrades.** Can a user make themselves admin, premium, or give themselves credits? Look for user-writable `role`, `is_admin`, `plan`, `credits` columns, premium flags kept on the client, and features unlocked by visiting a success URL.
4. **Paid endpoints.** Can an anonymous user, or one user in a loop, call the AI/email/SMS endpoints thousands of times? Is there auth, a rate limit, a max-token cap, and a provider spend limit?
5. **Secrets reaching the browser.** Public env prefixes, server modules imported into client components, SDKs created with secret keys in client code.

Attackers think in flows, not files. Trace at least two flows end to end, for example "user A reads user B's data" and "a free user gets the paid feature".

For Supabase, give the owner the [signed-out and two-account checks](references/stacks/supabase.md#owner-run-access-checks) with synthetic records. Deployed results stay `UNVERIFIED` until the owner provides evidence; source review and a successful SQL-editor query don't establish API authorization.

## Step 5: Score

Count verified findings only. UNVERIFIED items are listed but don't deduct.

```
score = 100 − 20×critical − 10×high − 4×medium − 1×low   (minimum 0)
any critical → score capped at 49 → 🔴 NO-GO
any high     → score capped at 79 → 🟡 FIX FIRST
otherwise                         → 🟢 GO
grade: A ≥ 90 · B ≥ 80 · C ≥ 65 · D ≥ 50 · F < 50
```

For `quick`, `security` and `launch`, label it with the mode, for example "Launch Score (quick)". A partial audit is never a full GO.

Judge every finding for the app's exposure:

| Exposure | What counts |
|---|---|
| `public` | Everything. |
| `internal` | Everything except launch basics (area 8). Insiders and stolen laptops are real attackers, so missing auth still counts. |
| `local` | Secrets count in full, because they leak through git, zips and screenshots. Missing auth, authorization, rate limits and launch basics don't deduct while the app only listens on localhost and holds no real data. List them under "Before exposing it more widely" instead. |

Put the exposure in the verdict. A `local` or `internal` GO is never a public GO: write it as "🟢 GO (local only)" or "🟢 GO (internal only)".

## Step 6: Write the report

1. Create `.vibecheck/` containing a `.gitignore` with the single line `*`. This keeps reports out of git without touching the user's own .gitignore. The report lists weaknesses, so it must never be committed publicly.
2. `.gitignore` only protects git. Check how else this project leaves the machine, and if `.vibecheck/` could go along, say so in the report header and the chat summary:
   - not a git repo (scanner `"git": false`), or shared as a zip or handoff archive: exclude `.vibecheck/` when archiving
   - a `Dockerfile` that copies the whole folder (`COPY . .`): add `.vibecheck` to `.dockerignore`
   - an npm package that isn't `"private": true`: keep it out with the `files` field or `.npmignore`
   - deploy CLIs, upload scripts or source listings that don't read `.gitignore`: exclude it there

   Don't edit those files during the audit. Name the file and the line to add, and offer to do it.
3. If `.vibecheck/report.md` exists, rename it to `.vibecheck/report.prev.md`.
4. Write `.vibecheck/report.md` following [templates/report.md](templates/report.md).

Every finding needs: an ID (`VC-…` from the scanner or checklist), severity, a plain-words title, where it is, what can happen, why (one technical line), how to fix it, and a **fix prompt**. A fix prompt is a self-contained instruction the user can paste into any AI tool (Claude Code, Cursor, Lovable, Bolt, v0, Replit). It names the file, says what to change and what not to break, and says how to confirm the fix worked.

## Step 7: Tell the user

Keep the chat summary short:

```
🚦 vibecheck: 🔴 NO-GO · 31/100 (F) · public app
3 critical · 2 high · 4 medium · 6 low · 2 to verify

1. 🔴 Your OpenAI key is in the browser bundle: anyone can spend your credit. (src/lib/ai.ts:4)
2. 🔴 The API exposes private messages to the anon role without RLS: anyone can read them.
3. 🔴 Stripe webhook isn't verified: anyone can fake a payment and unlock Pro.
…
Full report: .vibecheck/report.md
Next: /vibecheck:fix fixes these one at a time, criticals first. Before deploying, /vibecheck:deploy checks it will run in production.
```

- **Live secret found:** say clearly that removing it from the code is not enough. It must be revoked and replaced in the provider dashboard. If it was ever pushed or deployed, treat it as stolen.
- **Not public yet:** for a `local` or `internal` app, end with the short list of what must change before more people can reach it.
- **🟢 GO in `full` mode for a public app only:** offer a README badge. Never offer one for a failing score (a public "NO-GO" badge points attackers at the app) or for a local-only GO (the badge would overstate it).
  `[![vibecheck: GO 92/100](https://img.shields.io/badge/vibecheck-GO%2092%2F100-brightgreen)](https://github.com/ribato22/vibecheck)`
