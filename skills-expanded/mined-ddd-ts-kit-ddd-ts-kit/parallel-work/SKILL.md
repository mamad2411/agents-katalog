---
name: parallel-work
description: >-
  Use when the user wants several agents or developers to build at the same time, asks how
  to parallelise or share the work, or before launching more than one context-builder agent.
  One worker per bounded context, a git worktree each, contracts first.
argument-hint: "[contexts to build in parallel]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Agent
  - SendMessage
  - Bash(npx ddd-ts-kit status)
  - Bash(npx ddd-ts-kit status --workers)
  - Bash(npx ddd-ts-kit plan-waves)
  - Bash(npx ddd-ts-kit plan-waves *)
  - Bash(npx ddd-ts-kit story-check *)
  - Bash(npx ddd-ts-kit worker-scope *)
  - Bash(npx ddd-ts-kit generate *)
  - Bash(npx ddd-ts-kit docs)
  - Bash(npx ddd-ts-kit depcruise-config --write)
  - Bash(npx ddd-ts-kit check *)
  - Bash(npx ddd-ts-kit verify-merge)
  - Bash(npx ddd-ts-kit verify-merge *)
  - Bash(npx ddd-ts-kit merge-trunk)
  - Bash(npx ddd-ts-kit merge-trunk *)
  - Bash(npm run regenerate)
  - Bash(npm run docs:generate)
  - Bash(npm run verify)
  - Bash(npm ci)
  - Bash(git worktree *)
  - Bash(git status *)
---

# Work in parallel without collisions

Contexts asked for: `$ARGUMENTS`

You are the conductor: you own the trunk, the shared files and the merges. Workers own one
bounded context each. Input: `docs/architecture/slices.md` (skill `ddd-ts-kit:plan-slices` orders
it). Launch nothing before the owner approved the split.

## 1. Decide whether it pays

Work cut by user story rather than by context is `/ddd-ts-kit:story`, run by the owner, one
session and one terminal per story: it reuses the worktrees, the briefings and the merge rules
below. This skill splits one plan between workers of different contexts.

Parallel work pays when at least two contexts each have three or more ready slices and
their contracts are settled. It does not when: there is one context; a boundary or a payload
is still debated; the slices form one chain; the walking skeleton is not merged yet (build
it alone first, it proves the stack for everyone).

Workers: one per context, **two or three at a time**, four at most. Each has its own
worktree, dependencies and test runs, and every merge is read by one conductor: past that,
the merges become the bottleneck. Inside one context, two workers only on two different
aggregates, and expect to merge its route list and its permissions file by keeping both
sides' lines; otherwise, one context, one worker, slices in sequence.

Fewer on a machine that slows down: each worker runs its own compiler, linter and test runner.
When the user reports a stalled or restarting machine, launch one worker at a time and point
to `docs/guides/agent-sandbox.md` of the kit (a resource cap per session, NVIDIA OpenShell when
the security of the session matters).

A worker is one context and its worktree; an agent holds **one row, two at most**, before its
turns or its context run out. Inside a worktree, launch one `context-builder` agent per row,
in sequence, each on the commits of the previous one.

Do not batch and order by hand: `npx ddd-ts-kit plan-waves [<context>]` (`--json` for data)
puts the rows not done in waves (wave 1: every dependency done; wave n: after earlier waves),
cuts each wave into batches of one owner and one or two rows on one aggregate, prints the
`worker-scope` command of each batch, marks two batches of a wave likely to touch the same files
(same aggregate: run them one after the other) or unknown (no aggregate named: read their rows
before running them side by side), and gives the merge order. `plan-waves --ready` prints wave 1 alone and the later waves as one line, `status --ready` the rows to start now. It refuses a cycle, an unknown id or a row without owner,
a name the glossary does not define and a command the generator refuses: fix `slices.md` first. Launch a wave's batches side by side, the next wave once they merged.
Before a wave, read `Rows another story waits for, not done`: a row of another story that no
batch you launch and no open story (`npx ddd-ts-kit stories`) carries leaves its waiting rows
blocked; plan it, or hold those rows back.

## 2. Prepare the trunk (conductor, before any worker starts)

0. **Your own worktree.** The guard refuses the code of a context in the main checkout of the
   trunk: `npx ddd-ts-kit worktree <plan>` opens `.worktrees/<plan>` on `work/<plan>`, cut from
   `origin/main`, installed. Every step below runs there (`cd <worktree> && ...`, every file by
   its absolute path under it).
1. **Contracts first.** For every `contract` row a worker depends on: generate it
   (`generate integration-event`, `generate gateway`), write its payload schema or read
   contract in the upstream's `published-language/` with the owners of both sides, commit. A
   downstream starts only against a committed contract. A job or an integration event that a
   worker's row needs is such a step too, run here before that row starts: a worker's
   `generate job`, `generate integration-event` or, on an ORM, `generate read-model` with `--local-only` is refused (they write
   shared files), and the refusal prints the exact command to run on the trunk. Route paths and methods of each
   context are the ones written in the slices table.
2. **Skeleton next.** Run every `skeleton` row: `generate aggregate` (with
   `--event-sourced` when planned so) with its `generate repository` (no flag, an aggregate
   a command row names always has one), `generate job`, `generate read-model` (on an ORM), `generate policy`, any new `generate context`, and,
   when a slice plans an adapter and the project has none yet, the first `generate adapter`
   (it writes `platform/resilience/own-policy.ts`, which the next ones only import).
   These kinds write shared files (`generate --help --json` says which, under
   `writesShared`); run before any worker, they never conflict. Leave the `TODO(domain)` markers
   to the workers.
3. `npm run verify`, commit (one commit per contract and per aggregate), push `work/<plan>` and
   land it as its own pull request: the workers are cut from `origin/main` once it merged, as
   `plan-waves` prints them. To start them before it merges, cut them from your branch instead
   (`--base work/<plan>`); `merge-trunk` later finds the commits they share with it. Tell the
   owner the trunk is ready. `.ddd-ts-kit/` and `.worktrees/` are in the `.gitignore` that
   `init` writes: keep them there.

## 3. One worktree and one scope per worker

```bash
npx ddd-ts-kit worker-scope <context> --base origin/main --rows <id>   # as plan-waves prints it; --dry-run to read it first
```

Run it from the checkout of the trunk or from your worktree, in your own session: the guard refuses it to a sub-agent
unless `--dry-run`, which prints the briefing and creates nothing. From the base (by default the current branch; it
refuses a worker's worktree), it adds the git worktree `.worktrees/<context>` of the main checkout (ignored by git and by
every tool, never nested in another worktree) on the branch
`build/<context>`, or keeps it when it contains the base and refuses it when it does not,
writes `.ddd-ts-kit/worker.json` (its context, rows, base and branch) in it,
runs the clean install of the project in a worktree it creates (`--no-install` leaves it to
you; a note then says what to run), and prints the briefing of that worker. With that file,
the guard refuses any write of a `context-builder` agent outside `src/contexts/<context>/`,
its end-to-end specs and their support in `test/e2e/support/<context>/` (in an acceptance spec, anything but removing `pending(...)`), any generator that writes a shared file, any dependency change, and any
shell command that writes outside the scope (`sed -i`, `>`, `tee`, `cp`, `mv`, `rm`, or a path
only the shell knows); code the guard cannot read (inline code, a script, the tests) runs, and a
file it changed outside the scope stops the worker until it is put back, its scope pinned at its first call (the first command that names its worktree, where several workers have one; the pin then follows the worker, whichever checkout a call starts in); `npx prettier` and a bare `npx biome` are refused too.

Before briefing a worker in a context that already has one, run
`npx ddd-ts-kit status --workers` from the trunk: it lists each worker (worktree, branch,
context, rows, commits ahead, dependencies not installed), its state (rows committed, the row
under way, the last `verify-slice`, the `--resume` command of a stopped one) and the files it changed, then the
files more than one worker changed. Give the new worker rows on other files, or wait for the merge of the first.

In a worktree made otherwise, or when a worker stops on its environment, run
`npx ddd-ts-kit doctor --strict` in it: it names a Node that `engines.node` refuses, a missing or
stale `node_modules`, packages of the kit at another version and submodules not initialised.

## 4. Shared files: who touches them, how they stay conflict-free

| Shared | Touched by | Kept conflict-free by |
|---|---|---|
| `ddd-ts-kit.config.json`, `src/main.ts`, `src/platform/**`, `src/apps/**`, `src/shared-kernel/**` | conductor, on the trunk | workers report the need and wait for the trunk |
| registries the generators fill between markers (composition root, database schema index, read model tables, audited events, job settings, access policies) | generators, run by the conductor | skeleton first; at a merge, `merge-trunk` keeps both sides' lines, reads them back, and merges the region declaration by declaration where they would leave a table, a model or a function open or would mix the two sides: a column of one side in a table of the other, a table one side removed, a declaration above one it reads (in a region merged this way, one the two sides do not agree on is left as one hunk that holds each version whole: both wrote it differently, both added a column to it at one place while one of them added a table below it, one removed it and the other changed it; a region the kit merges neither way is left as git wrote it, and the report says why); on Drizzle, a table whose name the trunk exports for another context is listed under its context in the schema index (`shippingOrders`), whatever the order of the index and the layout of the context on either side (each side read as its commit lays it out; a line naming a tables file the other side moved is said, not written again, and the kit then writes no name in that merge; on Drizzle, a context left with two tables files, one per layout, that declare a name in common gets no line and one sentence saying which of the two files keeps each name (the one the trunk's index exports it from, under that name or another) and what must hold once they are one file), and the report says so, at `--continue` when the merge stopped on a conflict; what the kit does not repair (a table a line by hand or a module that is no tables file hides, a name that names another table after the merge) the report names, in the dry run too; when a file is not read with certainty it says once which names may be shared and who keeps them, with no line to copy, and it gives the lines to write by hand when the index cannot be written; on TypeORM the merge and `init --force` write no name of the index, as before: each name imported twice is said once, with its files, and you write the alias, or take out the extra import, by hand |
| `<context>.declarations.ts` and the `<layer>.declarations.ts` of each layer, `docs/context-map.md`, `openapi/*`, `docs/integration/*`, `.dependency-cruiser.cjs`, `clients/*` | `npm run regenerate`, a worker's included | a worker regenerates and commits them with its slice; never merged by hand: `merge-trunk` takes the trunk's side and regenerates |
| `package.json`, the lockfile | conductor | a worker asks for a dependency; `merge-trunk` takes the trunk's lockfile and installs again when the branch changed `package.json` |
| migrations and their order | conductor | a worker generates a working one only (`db:generate working-<what>`); `merge-trunk` replays the drizzle ones of both sides, and `merge-trunk --to-land` gives them their real names before the squash merge |
| `docs/architecture/plan.md`, `slices.md` | conductor | workers report, the conductor marks; `merge-trunk` merges `slices.md` row by row |
| `docs/architecture/stories/*.md`, `test/acceptance/*` (the acceptance of a story and its lock) | conductor, before the first row of the story | a worker removes `pending(...)` from the scenarios its row satisfies, nothing else; a scenario it finds wrong is a need of its report |
| `docs/adr/` | conductor; a worker for a decision of its slices (`generate adr`, without `--deviation`) | a new file per decision; `merge-trunk` renumbers a number the trunk took meanwhile |

Another context's `published-language/` is read-only for a worker: a missing field is
reported, agreed, and added on the trunk.

The tables of a context are its worker's, not shared: a stored field changes its column and the
mapper in one commit, on the worker's branch, with a working migration. They live in the context
(`infrastructure/persistence/` on Drizzle, Knex and TypeORM) or, on Prisma, in the file of the
context `prisma/schema/<context>.prisma`, which the guard lets its worker write. Only the main
file `prisma/schema/schema.prisma` (the client, the datasource, the tables of the platform) is
shared: never write a column of a context on the trunk, where its mapper has not changed.

## 5. Brief and launch

`worker-scope` prints the briefing of the rows of `--rows` (by default the first batch
`plan-waves` cuts for the context, one or two rows on one aggregate, with a note naming the
next `--rows`; a note past two rows asked for), each with its rules from `slices.md` and the documents of
its design (`design:`): send it as it is ([briefing-template.md](briefing-template.md) is the
same text, to write one by hand). When the design cites names the base removed, refuses or
replaced, the briefing lists them (eight lines at most) and a note tells you the lines: correct
them on the trunk before launching, or launch as is; the worker builds on the trunk's names and
reports each line as a note, never edits `docs/`. A worker's `verify-slice` and the reviewer's
`npx ddd-ts-kit cited --removed-since <base>` name what a slice removes that another row's
design still cites: correct those documents at the merge.
Launch the `context-builder` agents of different contexts in one message so they run
together, without the isolation option (the worktree already exists): each runs every command from
its worktree (`cd <worktree> && ...`), as its briefing says, since the guard reads a command against
the scope of the worktree it runs in. In one context, launch
the next row's agent once the previous one reported. The guard warns each `context-builder`
twice before its turn limit (finish the slice under way, then stop, commit what passed and
report) and records its runs in its worktree; a session start names the workers to resume.
A worker returns its report as its final message (Claude Code refuses a sub-agent the write of a
file) and a `SubagentStop` hook writes it to `.ddd-ts-kit/report.md` of its worktree. When the file
is missing after a worker returns, write it yourself from the worker's final message, so that
`worker-scope --resume` reads it.

**When an agent stops**, whatever the reason:

1. On a notification "stopped at its N-turn limit", "failed: ... API error", "was stopped", or a
   report naming an unfinished row: run `npx ddd-ts-kit worker-scope <context> --resume` from
   the trunk. It reads the worktree (rows committed by their `Slice:` trailer, the files of the
   row under way, the markers, the last `verify-slice`, the report, the agent) and changes
   nothing. Never inspect the worktree by hand, never clean or reset it, never relaunch a fresh
   agent there without the resume briefing.
2. `next: SendMessage to <id>`: send the printed message as it is, without asking the owner. The
   agent keeps its history and gets a new turn budget.
3. `next: launch a new context-builder`, a SendMessage refused, or "Prompt is too long" (run it
   again with `--fresh`): launch a new `context-builder` with the printed briefing, which holds
   the row under way only and the files the earlier agent left.
4. A rate or session limit: wait for the reset, then step 1.
5. Bounded autonomy: after two stops on one row without a new commit, stop resuming it: split
   the row in `slices.md` (plan-slices), or ask the owner (unattended: finish it yourself, section 7).

A report sorts its needs. A **blocking** one stops that row: do it in your worktree and land it, have the
worker bring the trunk in (`npx ddd-ts-kit merge-trunk`), then launch the next agent. A **note** waits for the merge of the
branch (step 6): the run goes on.

### Bring the trunk in

Each agent commits its rows. Then bring the trunk into the branch: `npx ddd-ts-kit merge-trunk
--cwd <worktree>`, resolve what it stops on keeping both sides, `--continue` (skill
`ddd-ts-kit:quality-gate`, `merge-trunk.md`).
A worker under the sandbox of the regulated profile cannot reach the database: `db:migrate` and a spec that names a `DATABASE_URL` are run by the owner or the CI, not by the worker. Its working migration it generates itself: with `DATABASE_URL` unset, `db:generate` of Prisma and TypeORM runs on PostgreSQL in process (it exits 3 only when `DATABASE_URL` names a server that does not answer).

### Review the batch

Then one review of the batch (`architecture-reviewer`, `--changed-since <base>`), `npm run
verify` on the merged branch, then the branch merges or opens its pull request. The blocking
findings of the review are fixed on the branch; each non-blocking one is settled at once or
written, before the merge, as the `TODO(review)` line the review gives (skill
`ddd-ts-kit:quality-gate`, `review-remarks.md`). `check --changed-since` sees the files of the
branch only: a cycle, an unused export or a rule broken by what the trunk
gained meanwhile shows only in `verify` on the whole tree. A host without the
agents of the plugin (Codex) runs one session per worktree, its briefing as the first prompt:
the guard does not hold that session to its context, the briefing and the review do. A person
takes the same briefing and the same branch.

## 6. Merge, in order

In the merge order `plan-waves` gives: by wave, upstream first. `npx ddd-ts-kit status` tells a
row ready on the trunk from one ready once a worker's branch merges, and lists what a waiting
row waits for. Before each merge,
`npx ddd-ts-kit status --workers`: a file the branch shares with another worker is where the
second merge can conflict. For each branch:

1. land it: `npx ddd-ts-kit merge-trunk --to-land --cwd <worktree>` brings the trunk in and
   gives its migrations their real names (replayed under drizzle-kit, renamed after the trunk's
   last under knex, Prisma and TypeORM; a migration of the trunk and one of the branch on the
   same table stop it: generate that one again on the trunk with
   `npm run db:generate <what-it-does>`), renumbers a decision record whose number the trunk took
   meanwhile, regenerates and checks nothing was lost; `npm run verify` in the worktree, push,
   then the squash merge (a squash made outside GitHub or GitLab:
   `npx ddd-ts-kit verify-merge <squash commit> --theirs <head of the branch>`). Only you run
   `--to-land`: the guard refuses it to a sub-agent. A branch pushed without it fails
   `verify-merge` on each migration that sorts before the trunk's last; on a branch that already
   holds the trunk, `--to-land` still lands the migrations and leaves them to commit;
2. `npm run verify` on the trunk; a red trunk is fixed before the next merge;
3. mark its rows `done` in `slices.md`, commit (`npx ddd-ts-kit status` shows what is left);
   a slice merges with `TODO(review)` markers, a story or a milestone closes once
   `npx ddd-ts-kit story-check <code>` exits 0 (skill `ddd-ts-kit:quality-gate`, "Review
   remarks");
4. the other workers bring the trunk into their branch with `merge-trunk` before their next
   slice; a branch reused for its next row does the same, from where its first row landed.

A branch cut from another branch (a second batch of one context, started before the first
merged) is stacked: when the first merges by squash, its commits are rewritten into one, and a
plain merge of the trunk into the second replays them as conflicts. `merge-trunk` finds where the
first branch landed (by patch id, on the branch recorded as its base or any local branch sharing
commits) and merges from there; when the first branch is gone and nothing proves it, it falls
back to an older base (more conflicts, never a silent loss) and names the `--since <commit>` to
confirm. Without `--trunk` it brings in the base of the worker, here the first branch: once that
one landed, run it with `--trunk origin/main`. `status --workers` shows, per worker, where it landed, what is ahead and behind, and
what `merge-trunk` would leave conflicted now. Never resolve by taking the trunk's side of a
whole file.

A worker never grants a permission to a role: the roles live in `src/platform/auth/roles/`. When
its report says who holds a new permission, grant it on the trunk in `roles.ts` (by the entry
of the set) as you merge its branch, before `npm run verify`: `authz/granted` warns until then.

When a worker reports a need on a shared file: do it in your worktree, land it, tell the worker
to merge the trunk. Remove each worktree once its branch is merged
(`git worktree remove .worktrees/<context>`).

## 7. A conductor that runs unattended

The session is unattended (`claude -p`, a scheduled job) when the brief says so or when no one is
there to answer; nothing else tells it, so a brief that starts such a run states it, the wave to
build and whether the project has a remote. Then:

- **Keep the turn while a worker runs.** Wait for its notification, or work on the trunk. Ending
  the turn ends the session: `claude -p` waits for background agents for 10 minutes of idle at most
  (`CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS`), `--bare` has none, and what is left stops with its
  work uncommitted in the worktree.
- **Never resume a worker by message** (`SendMessage` fails or restarts it without its history):
  `npx ddd-ts-kit merge-trunk --cwd <worktree>`, then launch a new `context-builder` on the same
  worktree with the `--fresh` resume briefing (the rows left, what the last one did).
- **After two stops on one row without a new commit, finish the row yourself** in the worktree,
  by the rules of its briefing; launch no third worker on it.
- **Checkpoint.** With a remote and the owner's permission to push, after each merge of a worker
  push the integration branch (`git push origin work/<plan>`), never the main branch. A restart then
  loses one worker, not the run. Without that permission, commit after each merge and say in the
  report that the branch is local.
- **Stop at the end of the wave** of `plan-waves` you were given, with the report (merged, left, needs),
  unless the brief names more waves or a time to stop.

Token rules for everyone: [../start/token-economy.md](../start/token-economy.md).
