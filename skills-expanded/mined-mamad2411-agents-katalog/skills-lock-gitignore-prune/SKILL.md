---
name: skills-lock-gitignore-prune
description: Resync skills-lock.json with .gitignore by removing any skill entry whose files are git-ignored. Fixes lockfile "ghosting" — stale entries left behind after ignore rules are added — by delegating ignore resolution to `git check-ignore`, so globs like `agent-skill-kit-*`, the `.git/info/exclude` file, and the global excludesFile are all honored. Also catches the outlier case where a skill's `.agents/skills/<name>` source is tracked but its mirrored `.claude/skills/<name>` copy is ignored (or vice-versa). Zero-dependency Node script with a --dry-run preview. Use when skills-lock.json lists skills that are no longer tracked, after adding ignore rules for vendored skills, or to audit lockfile/ignore drift.
tier: project
---

# Skills Lock — Gitignore Prune

`skills-lock.json` pins each installed skill (`source`, `skillPath`, `computedHash`).
When an ignore rule is added *after* the lockfile was generated, the lockfile does not
auto-prune — the ignored skills "ghost" in the lockfile even though their files are no
longer tracked. This skill flushes those ghosts so the lockfile only lists skills git
actually tracks.

## What it does

For every entry under `skills` in the lockfile, it asks git whether the skill's files
are ignored. An entry is **PRUNED** if *any* of these candidate paths is ignored:

| Candidate | Example |
|-----------|---------|
| recorded `skillPath` | `.agents/skills/<name>/SKILL.md` |
| its parent directory | `.agents/skills/<name>` |
| the Claude mirror     | `.claude/skills/<name>` |
| the agents source     | `.agents/skills/<name>` |

The mirror/source pair is what resolves the **outlier**: a skill whose `.agents/skills`
source is tracked but whose `.claude/skills` symlink is ignored (e.g. an ignore rule
written against the `.claude/` root) is still pruned — no need to hand-edit `.gitignore`
to align roots first. (Pass `--strict` to test only the recorded `skillPath` if you'd
rather fix the ignore rule instead.)

Ignore matching is delegated to `git check-ignore`, so it honors the *full* git ignore
stack — every `.gitignore`, `.git/info/exclude`, and the global `core.excludesFile` —
with exact git glob/negation semantics. It never re-implements pattern matching.

The skill only ever **removes** entries; it never adds, reorders survivors, or rewrites
hashes. Surviving entries keep their original order and values.

## How to run

Zero dependencies (native Node + the `git` CLI). Resolves the repo root via
`git rev-parse --show-toplevel`, falling back to `$PWD`.

```bash
# 1. Preview — print KEEP/PRUNE verdicts, write nothing:
node .agents/skills/skills-lock-gitignore-prune/bin/prune-lock.mjs --dry-run

# 2. Apply — rewrite skills-lock.json with ghosts removed:
node .agents/skills/skills-lock-gitignore-prune/bin/prune-lock.mjs
```

### Flags

| Flag | Effect |
|------|--------|
| `--dry-run` | Report verdicts; do not modify the lockfile. |
| `--lock <path>` | Lockfile to operate on (default `<root>/skills-lock.json`). |
| `--strict` | Test only the recorded `skillPath` (+ its dir); skip the `.claude`/`.agents` mirror heuristic. |
| `[root]` | Repo root to run git in and resolve paths against (default: detected git root). |

### Exit codes

`0` on success (whether or not anything was pruned). `2` on a usage error, an unreadable
or invalid lockfile, or a `git check-ignore` failure (e.g. not a git work tree).

## Notes

- Idempotent: running again after a prune reports "already in sync" and writes nothing.
- The on-disk skill directories are not touched — only the lockfile is edited. Removing
  the directories themselves is a separate concern.
- To *also* stop a skill being ignored, edit `.gitignore` (or `--strict` + realign the
  rule), then re-run; an entry only survives when none of its candidate paths are ignored.
