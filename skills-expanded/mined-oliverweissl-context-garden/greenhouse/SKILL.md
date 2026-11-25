---
name: greenhouse
description: Shared memory across the repositories of one platform (what each repo provides, depends on, and its key facts) kept in a base folder next to the repos. Use when a task touches an API, package, schema or convention shared with other repos, instead of opening those repos; publish this repo's card at task end.
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/bin/greenhouse *), Bash("${CLAUDE_SKILL_DIR}/bin/greenhouse" *)
---

# greenhouse

!`"${CLAUDE_SKILL_DIR}/bin/greenhouse" mode --banner`

Agents that do not expand the line above (e.g. Codex): run
`<this-skill-dir>/bin/greenhouse mode --banner` first and follow it.

A *base* is a folder (usually `<workspace>/.greenhouse/`, beside the repos)
with one card per repo and platform-wide notes. Cards are harvested
deterministically: README summary, packages provided, dependencies,
entrypoints, layout, the repo's seedbank hot facts and mycelium notes.
Repos link automatically when one depends on a package another provides.

`greenhouse` is not on PATH: always run `<this-skill-dir>/bin/greenhouse`.

**No base found** (`mode on`, the session-start hook or any command says
so): never create one unasked. Ask the user with AskUserQuestion: create a
new base beside the repo (`bin/greenhouse init`), use an existing one or a
specific path (`bin/greenhouse link <path>` / `init --at <path>`), or this
repo is standalone (`bin/greenhouse mode off`). Then run their choice.

1. **Start** (only if the task may cross a repo boundary):
   `bin/greenhouse brief "<task>"`. It lists this repo's upstream and
   downstream repos, matching platform notes and the relevant facts of
   other repos. `bin/greenhouse show <slug>` gives one full card. A card
   marked STALE must be verified before you rely on it. If a card does not
   settle the question, delegate one bounded question to the `envoy` agent
   (read-only; give it the card and the checkout path) instead of reading
   the other repo yourself; record its platform note if it returns one.
2. **End**, after a change that others depend on, or when the brief said
   this repo's card is missing or old:
   ```
   bin/greenhouse sync [--summary "<what this repo is for>"] [--provides "<interface>"] [--consumes "<repo>: <what>"]
   ```
   `--summary/--provides/--consumes` are kept across syncs; give them once.
3. **Platform facts** that hold across repos (shared conventions, a
   contract between two services, a migration in progress):
   `bin/greenhouse note "<topic>" "<fact>" [--repo <slug>]`.
   Repo-local facts belong in the repo (seedbank), not here.

Handing cards/notes to another base: `bin/greenhouse export [--repo <slug>] --out f.json`,
then `bin/greenhouse import f.json` there (never clobbers newer cards).

Discovery, layout, hook setup, sharing the base: `references/guide.md`.
