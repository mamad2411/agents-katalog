---
name: loop-setup
description: Session 0. Sets up the loop in this project - detects the stack, checks which connections actually work (git, database, browser, payments sandbox), asks the few decisions only the owner can make, and writes the .loop/ files. Run this once per project, before any planning or building.
---

# Session 0 — set up the loop

You are setting up a working method in **someone else's project**. Touch nothing
until they have seen what you propose to write. Never invent a fact about their
stack: check it.

## 1 · Read the project

Detect, don't ask, what you can find yourself: `ls`, `git remote -v`,
`git branch --show-current`, `cat .gitignore`, and whichever of these exist —
`package.json` scripts, `Makefile`, `pyproject.toml`, `Cargo.toml`, `go.mod`,
`docker-compose.yml`, CI config, test config, migrations directory.
Report in three lines what this project is and how it is built.

## 2 · Check the connections — live, not by asking

The method depends on being able to *observe* things. Find out what is actually
available in this session, right now, and print a table of PASS / FAIL / ABSENT:

| Need | How to check |
|---|---|
| Version control | `git status` works, and whether a remote exists |
| Build / tests | run the project's build or test command once |
| Browser | is a browser-driving tool available (in-app browser, Chrome extension, Playwright/Puppeteer in devDependencies)? If yes, open one page and confirm it renders |
| Database | is there a DB MCP server, a CLI (`psql`, `mysql`, `sqlite3`), or an ORM with a dev database? If yes, run one harmless read query |
| Payments sandbox | if the project charges money: is a test-mode key present in the environment (never print its value) |
| Deploy | how does this project publish, and is that command something the owner runs, not the agent |

For anything ABSENT, say in one line what will not be verifiable without it and
what the cheapest substitute is. **Do not silently accept a gap** — an absent
connection becomes a declared GAP in `.loop/VERIFY.md`, not a shrug.

## 3 · Decide which models run which role

Ask, do not guess: **which is the strongest model you have access to, and do you have
one you would rather keep for the expensive steps?** Plans differ, and a managed
install can restrict models outright.

Explain the shape in one breath, then write the answer into `.loop/roles/*.json`:

- **plan** and **close** want the strongest reasoning at the highest effort. These are
  the two steps where being wrong is most expensive: a bad plan wastes every session
  after it, and a soft audit lets a broken slice through.
- **build** and **verify** can be a mid-tier model. The hard calls are already made.
- Use **aliases** (`opus`, `sonnet`, `haiku`, or whatever the strongest tier is called
  on their plan), never full model ids — aliases survive model releases.

If they only have one model, say so plainly and write that one everywhere: the method
still works, it just loses the quality gradient. **Never leave a profile pointing at a
model they do not have** — an unavailable model can fall back silently, and a silent
fallback is the exact failure this method exists to prevent. Then tell them that no
session can report which model it is on, so the profile is the only record.

Ask **how they work**, because it changes what the profiles are worth:

- **In a terminal** — the `loop` wrapper launches each role with its model already set.
  The profiles do the work; they never choose a model by hand again.
- **In the desktop app or an IDE** — sessions are launched by the app, so the wrapper is
  not the path. They invoke the skills directly and pick the model in the app's model
  selector. Say this plainly instead of letting them think the profile applied. It costs
  little: the plan, the council and the audit dispatch subagents whose model is fixed in
  their own definitions, so the expensive thinking is strong either way.

## 4 · Ask only what you cannot find out (these are the owner's calls)

1. **Are the loop files versioned or local-only?** `.loop/` holds the plan, the
   decisions and the hard-won techniques. Committing them means the method survives
   a dead laptop and travels to teammates; keeping them local means nothing new
   enters the history. Recommend committing, and either way write
   `.loop/ACCESS.local.md` for anything sensitive and always gitignore that file.
2. **Which branch is protected** (never pushed to by an agent) and **who authorizes
   publishing**.
3. **Which commands are forbidden** to the agent in this project — the destructive
   or expensive ones (a deploy, a production migration, a data wipe).
4. **Is there a shared resource** two parallel sessions could collide on (one
   database, a schema version counter, a staging environment), and the exact command
   that reads its current true state.
5. **Solo or team?** Solo: an item closes with a commit on a branch. Team: it closes
   with a pull request, green CI, and a reviewer.

## 5 · Write the files

Copy from this skill's `templates/` directory into the project, filling in what you
learned. **Show the list first and get a yes.**

- `.loop/STATE.md` — the single source of truth for the plan
- `.loop/VERIFY.md` — the verification contract, filled in with *their* real commands
- `.loop/DECISIONS.md` — append-only ledger
- `.loop/GOTCHAS.md` — techniques learned the hard way, starts empty
- `.loop/ACCESS.local.md` — how to reach test accounts and environments. **Copy it
  from `templates/ACCESS.md`** (the template is not named `.local` so that a
  `*.local.md` ignore rule cannot swallow it) and always gitignore the installed copy
- `.loop/roles/{plan,build,verify,close}.json` — one launch profile per session role
- `loop` at the repo root — the wrapper, `chmod +x`
- `.claude/agents/loop-{planner,builder,verifier,auditor}.md` — copy the role agents
  here so the project controls them (agents shipped inside a plugin cannot carry
  permission rules)
- Append `.gitignore` entries according to their answer in step 4.1 — always
  `.loop/ACCESS.local.md`.

Then append **six lines** to their `CLAUDE.md` (create it if absent), so that any
future session lands in the loop without anyone saying the word "loop":

```
## How we work
Before building anything, read `.loop/STATE.md` and follow the `loop` skill.
`.loop/STATE.md` is the only source of truth for what is done and what is left —
nothing lives only in someone's head. Nothing is "done" until it has been observed
working, per `.loop/VERIFY.md`. Never push to the protected branch.
```

## 6 · Close session 0

Print: the connection table, the files written, the decisions recorded, and the exact
next command **for the way they actually work** — `./loop plan "<the first goal>"` in a
terminal, or "switch to your strongest model, then run the `loop-plan` skill with your
goal" in the app. Then stop. Session 0 does not build anything.
