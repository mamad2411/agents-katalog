---
name: docs-readme-writer
description: Generate a README/quickstart for any project — what it is, a 5-minute start that actually works, configuration table, and troubleshooting — grounded in the real repo, not guesses. Use when the user says "write a README", "document this project", "quickstart guide", "how do people run this", or is handing a repo to teammates/users. Don't use for user-facing release notes on a new version — use changelog-release-notes.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Builder Dev, Documentation, README, Onboarding]
    related_skills: [changelog-release-notes, lovable-brief-writer, env-secrets-hygiene, vercel-deploy-check]
---

# Docs & README Writer

Writes the README a stranger can clone-and-run from in five minutes. The standard: every command in the doc was actually derived from the repo (package.json, env usage, real file paths) — never from what projects like this "usually" do. A README with a command that doesn't work is worse than no README.

## When to Use

- A project has no README, or the README lies about how to run it.
- Handing the repo to a collaborator, a client, a hackathon judge, or future-you.
- User wants setup/config/troubleshooting documented after shipping.
- **Not for:** announcing what changed in a release — use `changelog-release-notes`. Not for spec'ing a feature to build — use `lovable-brief-writer`.

## Quick Reference

| Action | Command / Call |
|---|---|
| What is this project? | `cat package.json \| python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('name'), '—', d.get('description','(no description)'))"` |
| Real run commands | `python3 -c "import json; print(json.load(open('package.json'))['scripts'])"` |
| Env vars the code needs | `grep -rhoE "process\.env\.[A-Z0-9_]+" src/ app/ lib/ 2>/dev/null \| sort -u` |
| Repo shape | `find . -maxdepth 2 -type d -not -path "*/node_modules*" -not -path "*/.git*" -not -path "*/.next*"` |
| Node version expected | `cat .nvmrc 2>/dev/null; python3 -c "import json; print(json.load(open('package.json')).get('engines','no engines field'))"` |
| Prove the quickstart | run it top-to-bottom in a fresh clone/temp dir |

## Procedure

1. **Precheck** — confirm the repo path, the audience (teammate dev? non-dev client? end user?), and where it's deployed (README should link the live thing). Audience changes depth: non-devs get more "install Node from nodejs.org", fewer flags.
2. **Mine the repo** — run the Quick Reference commands. Collect: name + real one-line purpose, install/dev/build commands from `scripts`, the full env var list, prerequisites (Node version, Supabase project, Stripe account…), and the 2–4 directories a newcomer should know about.
3. **Draft the 5-minute start** — the exact sequence: clone → install → configure env → run → what you should see. Every env var appears in an `.env.example` snippet with a placeholder and a one-line "where to get this" (dashboard URL). Placeholders only — real values never go in a README (see `env-secrets-hygiene`).
4. **Config + troubleshooting** — config as a table (Variable / Required? / What it does / Where to get it). Troubleshooting from real failure modes: what happens if each required var is missing, wrong Node version, port already in use, database not migrated. Format: symptom the user sees → cause → fix command.
5. **Test the quickstart** — this step is the skill. In a temp dir: fresh clone (or copy), follow your own doc exactly, keyboard only. Every command that fails or assumes unstated setup gets fixed in the doc, not worked around. Success: app running from doc alone.
6. **Deliver** — write `README.md` at the repo root (confirm before overwriting an existing README — offer a diff or merge of any sections worth keeping). Keep it under ~150 lines; deep dives go to `docs/` and get linked.

## Output Template

```markdown
# <Project Name>
<One sentence: what it does and for whom.>  Live: <url>

## Quickstart (5 minutes)
Prereqs: Node <version>, <other>
1. git clone <url> && cd <dir>
2. npm install
3. cp .env.example .env   # then fill in the values below
4. npm run dev
5. Open http://localhost:3000 — you should see <specific thing>.

## Configuration
| Variable | Required | What it does | Where to get it |
|---|---|---|---|
| SUPABASE_URL | yes | database connection | supabase.com → project settings |

## Project layout
- `app/` — pages and routes
- `lib/` — shared logic

## Troubleshooting
**"Invalid API key" on load** → SUPABASE_URL/key missing or wrong → recheck step 3.
**Port 3000 in use** → `npm run dev -- -p 3001`

## Deploying
<one paragraph + link, e.g. Vercel — see vercel-deploy-check>
```

## Pitfalls

- **Documented from memory, not the repo** — README says `npm start`, package.json says `npm run dev`. Recovery: scripts and env lists come only from the mining commands; if you didn't read it, don't write it.
- **Quickstart assumes invisible setup** — works for the author because their global config fills the gaps. Recovery: the fresh-clone test in step 5 exposes this; add every discovered prerequisite to the Prereqs line.
- **Real secrets in the README or .env.example** — docs get committed and shared. Recovery: placeholders only (`sk_test_your_key_here`); if a real key already shipped in a doc, rotate it now via `env-secrets-hygiene`.
- **Everything-README** — 600 lines covering architecture philosophy; nobody finds the run command. Recovery: quickstart stays in the first screenful; move essays to `docs/` and link.
- **Doc rot after the next feature** — README describes last month's app. Recovery: end the README with a "docs updated: <date> @ <commit>" line, and re-run step 5 whenever setup-affecting changes ship.

## Verification

- [ ] Quickstart executed top-to-bottom in a clean environment; app ran
- [ ] Every command in the doc copied from a real run, not typed from memory
- [ ] Env table matches the grep of actual `process.env` usage — no extras, no gaps
- [ ] Zero real secret values anywhere in README or .env.example
- [ ] Step 5 of the quickstart names the specific thing the user should see
- [ ] Existing README (if any) overwritten only with user confirmation
