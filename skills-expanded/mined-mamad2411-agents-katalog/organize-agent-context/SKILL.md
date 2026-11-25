---
name: organize-agent-context
description: Reorganize a repo's AI-agent instruction files into a canonical layout — a thin CLAUDE.md pointer, one AGENTS.md per directory as the single source of truth, deep topic docs split under docs/, and project skills consolidated in .claude/skills/. Use when a CLAUDE.md or AGENTS.md is bloated, duplicated, or drifted out of sync, when setting up agent instructions for a repo or monorepo, or when the user mentions organizing, splitting, or cleaning up AI context, CLAUDE.md, or AGENTS.md.
---

# Organize agent context

One source of truth per directory, thin pointers for Claude Code, deep detail split out and loaded
on demand. Works for a single repo or a monorepo.

## Target layout

| File | Role |
|---|---|
| `AGENTS.md` (per directory) | **Canonical.** Read natively by Codex/Gemini/Cursor, by Claude Code via the pointer. Only what applies to *every* task: stack, structure, invariant rules, pointers. Aim under ~200 lines. |
| `CLAUDE.md` (per directory) | Thin pointer: `@AGENTS.md` + one line "don't add rules here, edit AGENTS.md". Claude Code reads `CLAUDE.md`, **not** `AGENTS.md`. |
| `<pkg>/docs/*.md` | One file per topic — the *why* and *how*. Reference, loaded on demand, linked from `AGENTS.md`. Split here only when `AGENTS.md` outgrows ~200 lines. |
| `.claude/skills/<name>/` | Project skills, one real dir each, versioned. |

Monorepo: root `AGENTS.md` (overview + team + repo map + cross-cutting rules) plus one `AGENTS.md`
per package. Nested `CLAUDE.md` files load on demand when the agent touches that directory.

## Workflow

1. **Recon.** Run the audit block below. List every instruction file with its line count, and any
   `CLAUDE.md`/`AGENTS.md` pair that has drifted.
2. **Pick canonical.** `AGENTS.md` per directory. If both a `CLAUDE.md` and `AGENTS.md` hold real
   content, the fuller / more current one wins → it *becomes* `AGENTS.md`; the stale one is discarded.
3. **Split by altitude.** Walk the canonical file top to bottom. For each section:
   - a rule that applies every task (short "always / never X") → **stays** in `AGENTS.md`
   - narrative, a lookup table, a runbook, a per-feature deep-dive → **moves** to
     `<pkg>/docs/<topic>.md` with a one-line pointer left behind. Rule stays, explanation moves.
   - verify facts against the code as you go — stale canonical files lie; recover anything real
     that no file documents.
4. **Write the pointers.** Every `CLAUDE.md` → `@AGENTS.md` + the "don't duplicate" line. Use the
   `@import`, not a symlink, if any contributor is on native Windows.
5. **Consolidate skills.** One skill root: `.claude/skills/`. See [REFERENCE.md](REFERENCE.md) § Skills.
6. **Verify.** New Claude Code session → `/context` lists the files under **Memory files**. Re-run
   the audit block: no dangling pointers, no stray `@token` imports in `AGENTS.md`.

## Audit block

```bash
# every agent instruction file + size, smallest first
# -r on xargs (skip the command on empty input): with none found, plain `xargs wc -l`
# runs `wc -l` with no file arg and hangs reading stdin — exactly the fresh-repo case this skill targets.
find . \( -name CLAUDE.md -o -name AGENTS.md -o -name .cursorrules -o -name copilot-instructions.md \) \
  -not -path '*/node_modules/*' -print0 | xargs -0 -r wc -l | sort -n
# drift: diff each CLAUDE.md against its sibling AGENTS.md
# stray @imports in AGENTS.md that Claude Code would try to load (bare @word, not in backticks)
# same empty-input guard: grep with zero file args reads stdin and hangs.
files=$(find . -name AGENTS.md -not -path '*/node_modules/*')
[ -n "$files" ] && grep -nE '(^|[[:space:]])@[A-Za-z]' $files | grep -vE '`@' || true
```

## Don't

- Add `SECURITY.md` unless the repo is public with outside vulnerability reporters.
- Add `CHANGELOG.md` unless the project cuts versioned releases.
- Split `docs/` preemptively — only split a file already over ~200 lines.
- Copy a PR/issue template verbatim — adapt it to the repo's real verification commands, drop
  sections that don't apply (semver, changelog-gate).
- Bundle a copy of a script inside a skill — the script lives in `scripts/`, the `SKILL.md` points
  at it.

Claude Code loading mechanics, skill consolidation detail, and a worked before/after: [REFERENCE.md](REFERENCE.md).
