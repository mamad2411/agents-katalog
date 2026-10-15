---
name: npx-skills
description: >-
  Documents the `npx skills` CLI for installing and updating agent
  skills, plus the project-level `skills-lock.json` lockfile.
  On start, detects a `skills-lock.json` without installed skills
  under `.claude/skills/` and proposes restoring them via
  `npx skills add … --copy -y` per the source recorded in the
  lockfile.
when_to_use: >-
  Two modes.
  (1) Startup —
  on the first interaction in a project that has `skills-lock.json`
  at the repo root but no installed skills under `.claude/skills/`,
  surface the gap and propose `npx skills add … --copy -y` per the
  source(s) recorded in the lockfile.
  (2) On request —
  when the user asks how to install, add, update, or restore agent
  skills via the `npx skills` CLI.
  Triggers: «поставь скиллы», «установи скиллы», «обнови скиллы»,
  «верни скиллы из lockfile», «как добавить скилл», «npx skills»,
  «skills-lock», «install skills», «add a skill», «update skills»,
  «restore skills from lockfile».
---

# npx-skills

The `npx skills` CLI
(https://github.com/vercel-labs/skills)
installs agent skills from a GitHub source
into the host project's `.claude/skills/` directory,
and writes a project-level `skills-lock.json` recording what was
installed.

## Lock files

| File                           | Scope   | Checked in | Per-skill fields                                    |
|--------------------------------|---------|------------|-----------------------------------------------------|
| `skills-lock.json` (repo root) | project | yes        | `source`, `sourceType`, `skillPath`, `computedHash` |
| `~/.agents/.skill-lock.json`   | global  | no         | written when `-g` is used                           |

The project lockfile is the source of truth for which skills the
repo expects to be present.

## Startup detection

On the first interaction in a project that has `skills-lock.json`
at the repo root but no `.claude/skills/` directory
(or the directory exists yet skills listed in the lockfile are
missing):

1. Read `skills-lock.json`,
   list the skill names under `skills.*`
   that are not present in `.claude/skills/`.
2. Collect the unique `source` values from those entries.
3. Report the missing skills to the user,
   and propose one install command per unique source:

   ```sh
   npx skills add <source> --skill '*' --copy -a claude-code -y
   ```

4. Wait for the user's confirmation before running anything.

Use `-g` instead of the project-local default
only when the user explicitly wants the install under
`~/.claude/skills/`.

## Install — all skills from a source

```sh
npx skills add <owner/repo> --skill '*' --copy -a claude-code -y
```

- `--skill '*'` —
  every skill in the source.
  Replace with `--skill <name>` for a single skill.
- `--copy` —
  write plain file copies,
  not symlinks.
  Symlinks couple the host repo to the source checkout
  and clutter the consumer's `git status`.
- `-a claude-code` —
  target Claude Code's `.claude/skills/` layout.
- `-y` —
  non-interactive
  (skip the per-skill confirmation prompt).

## Install — a single skill

```sh
npx skills add <owner/repo> --skill <skill-name> -a claude-code
```

Drop `-y` when adding a single skill —
the interactive prompt is quick
and confirms the resolved source.

## Update — re-run `add --copy -y`

Re-running the install with `--copy -y` overwrites existing files in
`.claude/skills/` in place,
so install and update share one command:

```sh
npx skills add <owner/repo> --skill '*' --copy -a claude-code -y
```

## Avoid `npx skills update`

`update` stages the package under `.agents/` in the host repo,
which clutters `git status` in the consumer project.
The `--copy` flag does not change this —
`update` accepts it but silently ignores it.
Use `add --copy -y` instead.

## Scope: project vs global

| Mode    | Flag      | Install path        |
|---------|-----------|---------------------|
| Project | (default) | `.claude/skills/`   |
| Global  | `-g`      | `~/.claude/skills/` |

Project is the default and the recommended scope.

## Verifying against upstream

The `npx skills` doc site is shallow.
When the exact behavior of a flag or command is unclear,
read the source at
https://github.com/vercel-labs/skills
(`src/add.ts`, `src/update.ts`, `src/skill-lock.ts`)
rather than guessing.
