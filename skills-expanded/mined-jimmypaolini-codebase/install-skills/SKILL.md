---
name: install-skills
description: Explains how skills are synchronized, updated, and excluded from various tools in the repository. Use when adding a new skill, running skills update, investigating missing skills, or wondering why a skill is ignored by formatters and linters.
---
# Install Skills and Synchronization

This skill explains how agent skills are maintained in this repository, including how they are synchronized from external sources, checked in, and excluded from static analysis tools.

## When to Use This Skill

- When adding a new skill (vendored or native).
- When a skill goes missing and needs to be restored.
- When you need to understand the `skills update` process.
- When configuring exclusions for tools like Prettier, CSpell, Codometer, etc.

## The Rule of Committing

**Every skill is committed**, vendored ones included. They are checked in rather than restored on demand for one reason: **a skill only becomes a slash command if its file is on disk when the session starts.** Nothing runs between `git worktree add` and an agent session, so a gitignored skill leaves commands reporting `Unknown command` for the whole of that first session. Committing them makes a fresh clone or worktree work with no setup step at all.

## Skills Update and Lockfile

`skills-lock.json` maps each skill to its source, and `skills update` rewrites the lockfile and the skill folders together so upstream drift arrives as a reviewable pull request rather than silently. `upgrade-dependencies.yml` runs it weekly. Upstream licenses travel with the copies in `.agents/licenses/`, as MIT and Apache-2.0 both require.

```bash
pnpm exec skills update
```

## Restoring Missing Skills

`scripts/install-skills.sh` restores folders that are genuinely absent — after `skills update` adds a lockfile entry, or when one has been deleted. It is idempotent, never leaves tracked files dirty, and never fails an install, because a missing skill is a broken agent workflow rather than a broken build:

```bash
pnpm exec nx run codebase:install-skills
```

## Tool Exclusions

Five things reach `.agents/` and so must skip the **vendored** skills while still covering this repository's own: `prettier` scans `.`, `codometer` measures the process's working directory by default and reads `configuration/.codometerignore`, GitHub Linguist reads every committed file, and `cspell` and `markdownlint` both reach `.agents/` because this repository's own skills are documentation and are held to the same standards as the rest of its prose. Correcting a vendored skill's spelling or reflowing its tables would be a change this repository has no right to make.

The exclusions are generated, not hand-maintained. Each file marks its block with `installed-skills-start` and `installed-skills-end` comments in its own syntax — `#` in `configuration/.prettierignore`, `configuration/.codometerignore`, `configuration/cspell.config.yaml`, and `.gitattributes`; `//` in `configuration/.markdownlint-cli2.jsonc` — and the `skill-exclusions` synchronizer rewrites what sits between them from the lockfile. It joins `lint-code` in the same `nx affected` invocation, so a stale list fails there rather than silently:

```bash
pnpm exec nx run synchronization:skill-exclusions:write
```

Two details of that machinery matter before changing it:

- **A wholesale pattern defeats the whole arrangement**, and no check catches it. Re-adding `**/.agents/skills/**` outside a managed block leaves every per-skill entry in place while quietly taking this repository's own skills back out of scope, and the synchronizer reports nothing because its own block still matches the lockfile. **Exclude a vendored skill by name.**
- **The root `project.json` mirrors the exclusions as cache negations.** Its `vendored-skills` named input drops them from the `spell-check` and `markdown-lint` `inputs`, because a tool that ignores a file has no reason to rehash on it. That is a cache optimization rather than a correctness gate.

Every other tool scopes itself with explicit globs that never include `.agents/`.
