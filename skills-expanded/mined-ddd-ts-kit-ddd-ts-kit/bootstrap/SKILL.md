---
name: bootstrap
description: >-
  Chooses the stack and creates the project with the ddd-ts-kit CLI: config, platform,
  database, pipeline, contexts, in an empty directory or an existing backend. Run by the
  user with /ddd-ts-kit:bootstrap.
argument-hint: "[stack hints, for example: fastify prisma keycloak]"
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(ls *)
  - Bash(git remote *)
  - Bash(npx ddd-ts-kit init *)
  - Bash(npx ddd-ts-kit@* init *)
  - Bash(npx ddd-ts-kit generate context *)
  - Bash(npx ddd-ts-kit docs)
  - Bash(npx ddd-ts-kit list *)
  - Bash(pnpm exec ddd-ts-kit generate context *)
  - Bash(pnpm exec ddd-ts-kit docs)
  - Bash(pnpm exec ddd-ts-kit list *)
  - Bash(npm install --global pnpm)
  - Bash(pnpm install)
  - Bash(pnpm run verify)
  - Bash(pnpm run docs:generate)
  - Bash(pnpm run hooks:install)
  - Bash(npm install)
  - Bash(npm run verify)
  - Bash(npm run docs:generate)
  - Bash(npm run hooks:install)
---

# Choose the stack and bootstrap

Stack hints given: `$ARGUMENTS`

## 1. Look before asking

Read `docs/architecture/plan.md`, `contexts.md`, `glossary.md` and `context-map.md` there when
they exist, and `package.json` when there is one. An existing project is adopted, never
overwritten: the CLI skips existing files unless `--force`.

The bootstrap is step 5 of the supported path. Without the strategic artefacts, say it plainly:
steps 1 to 4 (discovery, contexts, glossaries, context map) are being skipped, the contexts
would be drawn without an argued boundary and named before their language exists, and
`/ddd-ts-kit:start` produces them first. Recommend running it; go on without only on the
owner's explicit yes, and then record steps 1 to 4 as `skipped` with the reason in
`docs/architecture/plan.md`.

## 2. Choose the stack by criteria

Follow [stack-criteria.md](stack-criteria.md): infer each choice from the artefacts, the
hints and `package.json`, and ask only what it marks as not inferable, in one batch. Show the
resulting table (choice, value, why) and the full `init` command; the owner confirms. Record
the command under `## Decisions` of the plan.

## 3. Create the project

`init` creates no repository: in a fresh directory `git init` comes first, by the owner (this skill
runs no `git init`), or `hooks:install` of step 5 fails.

```bash
npx ddd-ts-kit@latest init <flags> --dry-run --json   # read `created`, `skipped`, `unwritable` and `notes`
npx ddd-ts-kit@latest init <flags> --json             # its `notes` end with the two commands to run next
pnpm install                                          # `npm install` with --package-manager npm
pnpm run verify                                       # the bare project is green before its first context
```

In a sandboxed session (the sandbox of Claude Code, which the regulated profile turns on), or
whenever the dry run exits 3 with files under `unwritable`, the real `init` is the owner's: the
sandbox keeps the agent from writing `.claude/settings.json` and `.claude/hooks/`. Exit code 3
with `unwritable` means "hand `init` to the owner", not a failure to retry or to work around. Run
the dry run, show the owner the same command without `--dry-run` and `--json`, to run from a
terminal outside the sandbox, and wait for their word that it ran; resume at `pnpm install`. An
`init` run in the sandbox anyway exits 3 too, after writing every other file, and ends with a
note that gives the command to finish: hand it to the owner the same way. Exit 3 with
`src/platform/database/schema.ts` under `left` is another case: `init --force` left the schema
index as it stood because its rewrite would lose a table, move a name, or drop a line it cannot read; no sandbox is involved,
and the note says what to move by hand. Hand that note to a person too, never retry around it.

Under `--agent-profile regulated`, the first `pnpm install` is the owner's too, from the same
terminal outside the agent, right after `init`; resume at `pnpm run verify`. The sandbox makes no
directory writable that is missing when the session starts, so this first install creates the
caches the agent may write afterwards (the pnpm store or `~/.npm`, `~/.cache/prisma`), and it runs
the install scripts of the stack (the engines of Prisma, the prebuilt binary of the Kafka client)
under the owner's eyes: `init` allows them by name (`allowBuilds` of `pnpm-workspace.yaml`,
`allowScripts` of `package.json` on npm), and the owner then pins them to the versions read, as
the notes say. Later installs, `pnpm install --frozen-lockfile` in a worktree included, run in the
sandbox. `init` says the same in its `notes`. A `doctor` line `install-script <package>` after a
bump is the owner's to approve, never the agent's.

The `allow` rules `init` writes apply only in a workspace trusted on the machine: a headless `claude -p` in a
clone nobody opened ignores them (stderr: `Ignoring N permissions.allow entries`) and keeps `deny` and `ask`.
Tell the owner to open the project once in Claude Code, or to set `hasTrustDialogAccepted` for its root in
`~/.claude.json`, before handing headless runs to the project; never edit that file yourself.

On an existing project, a note of the dry run that starts with `package.json depends on` is a
dependency the flags contradict: put it to the owner, and run the dry run again with the flag it
names, or with the owner's reason to change the stack under `## Decisions`.

A project is on pnpm unless `--package-manager npm` was chosen, or it is a package of an npm
workspace (`init` then takes npm and says so in a note): every command below is said for
pnpm, and reads `npm run <script>` and `npx ddd-ts-kit <command>` on npm. pnpm is pinned in
`package.json` and installed by npm (`npm install --global pnpm`, once per machine; pnpm then runs the release it pins). A red `verify`
on a project nothing was generated in is a bug of the kit: report it, do not patch the project.

No `--context` here: contexts come next, with their language.

## 4. Create the contexts, upstreams first

One command per row of `contexts.md`, in the order of the context map (a context after its
upstreams), with the purpose, the sentence of why it is of its classification, every row of its
section of `glossary.md` with its three cells, and its relationships:

```bash
pnpm exec ddd-ts-kit generate context <name> --classification <core|supporting|generic> \
  --reason "<one sentence: why it is core, supporting or generic>" --purpose "<two sentences>" \
  --term "<Term>=<meaning>|<not to be confused with>" --term "<Term>=<meaning>" ... \
  --upstream <upstream>:<pattern> --json
```

The `|` opens the third cell, "Not to be confused with"; leave it out of a row whose cell is
empty. A cell never holds a `|`, so a meaning cannot clash with it. Read `CONTEXT.md` after each
command: every row of the draft is there, three cells each.

A context whose row of `contexts.md` names modules gets, right after its `generate context`, one
command per module, on the trunk too (the module name is a glossary term, hence the `--term`):

```bash
pnpm exec ddd-ts-kit generate module <context> <module> --purpose "<one sentence>" --term "<Module>=<meaning>"
```

A `generic` context whose language is the one of a preset of the kit is written whole instead:
`generate context <name> --preset identity --json` for accounts provisioned from the identity
provider, organisations, members with roles, invitations and delegations. Propose it only when
the row of `contexts.md` says so in those words, never for a context that only looks generic
(delegations on a desk, practices in a time zone are a model of their own); the preset refuses
a stack it is not written for, with the flag to change, and a second context of the same preset. It is green as written once
`pnpm run docs:generate` has added its routes and events to the contracts, which are written from
the running application: run it before `verify`, then read its
`## Design` with the owner. Why and when:
`docs/guides/bootstrap-with-well-designed-contexts.md` of the kit.

Then, by hand, only what a flag cannot carry: in `docs/context-map.md`, outside the markers,
the reasons from the draft map and from `contexts.md`. Delete
`docs/architecture/glossary.md` and `docs/architecture/context-map.md`: their content now
lives in the `CONTEXT.md` files, the config and `docs/context-map.md`, and a second copy
would drift.

## 5. Prove it and commit

```bash
pnpm run verify          # types, lint, format, tests, end to end, architecture, import graph, dead code, docs drift
pnpm run hooks:install   # pre-commit checks and conventional commit messages
```

In a sandboxed session `.git/hooks` is read-only to the agent: `hooks:install` is the owner's too,
from a terminal outside the sandbox, once `pnpm install` has run (lefthook comes with the
dependencies). Commit after their word that it ran, so that the first commit goes through the
hooks.

Report the real output. Propose the commits (skill `ddd-ts-kit:commit-discipline`): one for
the bare project (`chore: bootstrap the project`), then one per context
(`feat(<context>): declare the context and its language`). Then `pnpm run infra:up` and
`pnpm run dev` when the owner wants to see it run; the API documentation is on `/docs`.

## 6. Hand over

Update the plan: step 5 `done`, `Next: 6 plan-slices - ...`. Say what exists now, and that the
next step is to plan the slices (`/ddd-ts-kit:plan-slices`), then to build them one at a time:
the order of `docs/guides/methodology.md` is the supported path.

Never hand-write a file the CLI generates. A generated file that is wrong is a bug of the
template: report it, do not patch it locally.

## Done when

Put this to the owner: **is the empty project green on `pnpm run verify`, with one
`CONTEXT.md` per context, and committed?** On a yes, the next step is
`ddd-ts-kit:plan-slices`.
