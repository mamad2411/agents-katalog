---
name: onboarding-doc
description: Write or audit onboarding documentation so a new engineer can get productive without ambient knowledge - setup, architecture, conventions, who to ask. Use when the user asks to write onboarding docs, improve dev setup instructions, create a getting-started guide, or audit new-hire experience.
license: MIT
compatibility: elyra >=0.1, claude-code
allowed-tools: read, bash, grep, edit
metadata:
  author: elyra-skills
  version: 1.0.0
  tags: [onboarding, documentation, dx]
---

# Onboarding Doc

The goal: a new engineer with no prior context can **clone, run, change, and ship** a small fix on their first day or two. Without DMing anyone.

A README that says "install dependencies and run the app" doesn't pass that bar.

## When to use

- "Write onboarding docs for X"
- "Improve our README / setup guide"
- "What does a new dev need to get started?"
- "Audit the new-hire experience"
- "Make it easier to contribute"

## Procedure

1. **Find a recent new hire / outside contributor** and ask what tripped them up — that's your spec
2. **Read the current README cold**, pretending you've never seen the code. Note every "wait, what?"
3. **Try to bootstrap from scratch** on a clean machine (or container) — every command you have to figure out is a gap
4. **Structure as a journey**, not a reference (see structure below)
5. **Cut ruthlessly** — every paragraph the reader skips is a paragraph that doesn't exist

## The 30-minute rule

A reader should be running the app locally within **30 minutes** of opening the README. If they're not, you're losing them.

If the actual setup takes longer (DB seeding, build), the *first 30 minutes* should include the "press enter and wait" command.

## Structure

The order matters. People read top-down and stop when frustrated.

```markdown
# <Project name>

<One sentence: what this is and who it's for.>

<One paragraph: a bit more context if the one-liner is mysterious.>

## Quick start

\`\`\`bash
git clone <repo>
cd <repo>
<one command to set up>
<one command to run>
\`\`\`

You should see <expected output / page>. If you don't, jump to [Troubleshooting](#troubleshooting).

## Requirements

- <runtime + version, with how to install>
- <language toolchain + version>
- <external service or "none — we mock it locally">

## Repository tour

Where things live. Don't list every file — describe the logical zones.

\`\`\`
src/
  domain/      ← business logic, no framework imports
  api/         ← HTTP layer
  jobs/        ← background workers
tests/         ← mirrors src/
docs/          ← architecture docs and ADRs
\`\`\`

## How things fit together

A diagram or short walkthrough of the request lifecycle.

## Conventions

The things tools can't enforce. Keep this short — link out for details.

- We use Conventional Commits → see `docs/contributing.md`
- Tests live next to code, named `*.test.ts`
- Migrations are expand/contract → see `docs/migrations.md`

## Common tasks

How to do the things you'll actually do daily:

- Run tests: `<command>`
- Run only one test: `<command>`
- Create a migration: `<command>`
- Reset the database: `<command>`
- Run against staging API: `<command or env var>`

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| <error> | <why> | <do this> |
| <error> | <why> | <do this> |

## Where to ask

- General questions: #channel
- This codebase: @<team-handle>
- Security: security@example.com
```

## What to put in vs link out

### In the main onboarding doc

- Quick start
- Requirements
- Repo tour (paragraph + tree)
- Common tasks they'll actually do
- Troubleshooting top issues
- Where to get help

### Linked from it (separate docs)

- Architecture deep dive
- Coding conventions in detail
- Deployment / release process
- Security policy
- ADRs

The main doc is the **table of contents to the team's knowledge**, not all of it.

## Make every command runnable

```markdown
❌ "Set up your environment variables"
✅ "Copy the example env file and fill in the values:
     `cp .env.example .env`
     The placeholders work for local dev. For staging values, ask in #channel."
```

```markdown
❌ "Install dependencies"
✅ "`npm install` (uses the version in `.nvmrc`; install [nvm](https://...) first if missing)"
```

Every step should be **copy-pasteable** and produce visible output.

## `.env.example` matters more than you think

The single most common onboarding failure: an env var that's required but undocumented.

- [ ] `.env.example` lives in the repo, committed
- [ ] Every key has a one-line comment explaining what it does and where to get the value
- [ ] Defaults that work for local dev are filled in
- [ ] Secrets clearly marked: "ask in #channel for the staging value"

```bash
# .env.example
# App
APP_URL=http://localhost:3000
APP_ENV=local

# Database (local Docker default — see docker-compose.yml)
DATABASE_URL=postgresql://app:app@localhost:5432/app_dev

# Mailer (Mailtrap for local; production uses Postmark)
MAIL_FROM=hello@example.test
MAIL_API_KEY=  # ask in #infra for the staging key

# Feature flags (optional)
FLAGS_SDK_KEY=  # leave empty for local; flags default to off
```

## "First contribution" path

Bonus: identify a small task a new hire can do on day 1–2 to actually ship something.

- Tag good-first-issue / starter tickets
- Document the "first PR" path: fork (if external) → branch → push → PR template → who reviews
- Pair them with a buddy for the first one

## Output format

When auditing existing docs:

```markdown
## Onboarding audit: <project>

**Test scenario:** Cold clone on a fresh machine, no team context.

**Time to first run:** <actual minutes>
**Number of times I had to ask / search:** <n>

### What works
- ✅ <thing>

### Gaps
- 🔴 <missing critical info — blocks setup entirely>
- 🟠 <ambient knowledge assumed — slows but doesn't block>
- 🟡 <polish>

### Top 5 fixes (ordered by impact)
1. <fix> — <impact>
2. …

### Trial: ask <recent new hire> to follow the updated doc
- <observed friction points>
```

When writing a new onboarding doc, follow the structure template above.

## Anti-patterns

- ❌ Outdated commands ("we don't use that script anymore")
- ❌ "Just ask <person>" — the doc is supposed to replace the asking
- ❌ Walls of prose where a code block would do
- ❌ Setup that requires access you have to request through five channels with no instructions on which
- ❌ "Run `make setup`" where `make setup` does undocumented magic
- ❌ Docs that describe what the team *will* do, not what it currently does
- ❌ Burying critical info under "Advanced topics"
- ❌ Treating onboarding as a one-time event rather than an artifact you can run
- ❌ No troubleshooting section — every team has a known list of "if you see X, do Y"
- ❌ Different commands in README, Makefile, and CI — pick one source of truth

## Tips

- **Audit annually**, ideally by sitting next to a new hire. Most onboarding bugs are invisible to those with context.
- **Track time-to-first-PR** as a metric — it should trend down.
- **Make setup scriptable**: `bin/setup` that does the right thing on a fresh machine is the gold standard. README then becomes "run `bin/setup`, then …"
- **Devcontainers / Nix / `bin/setup` scripts** save more onboarding pain than any prose.
- **The team's tribal knowledge is the bug** — every "you have to know that…" goes in the doc.
- **Read the doc out loud** to find dropped antecedents and assumptions.
- **Don't fear redundancy** — repeat critical things; readers don't read linearly.

## References

- [GitLab Handbook](https://handbook.gitlab.com/) — extreme example of writing everything down
- [Stripe README guide](https://stripe.com/blog/canon) — internal-docs philosophy
- [The Documentation System (Diátaxis)](https://diataxis.fr/) — tutorial vs how-to vs reference vs explanation
- [Write the Docs guides](https://www.writethedocs.org/guide/)
