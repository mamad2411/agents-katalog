---
name: claude-md-doctor
description: Check the instruction files Claude Code loads into every session — CLAUDE.md (project, parent folders, ~/.claude), .claude/CLAUDE.md, CLAUDE.local.md, .claude/rules, AGENTS.md, @imports and the auto-memory MEMORY.md — for broken or too-deep imports, files over the recommended 200 lines, MEMORY.md past the 200-line/25 KB load limit, references to files and npm scripts that no longer exist, secrets, a committed CLAUDE.local.md, and an AGENTS.md that is silently ignored. Shows what loads at launch and its token cost. Use when Claude ignores instructions, when setting up or cleaning a project's CLAUDE.md, or alongside claude-token-audit.
---

# claude-md-doctor

`scripts/md-doctor.mjs` is zero-dependency Node 22+ and read-only.

```
node md-doctor.mjs                 # what loads when Claude Code starts in the current folder
node md-doctor.mjs path/to/project
```

Output: every file loaded at launch with its token cost (and the import chain that pulled it in), the files that load on demand, then findings.

## Checks (rules from the Claude Code memory docs)
| Severity | Finding |
|---|---|
| high | `@import` of a file that doesn't exist; something that looks like a key, token or credentialed URL |
| medium | CLAUDE.md or a rule file over 200 lines (the docs' target); an import more than **4 hops** deep (it won't load); an import cycle; MEMORY.md past the **first 200 lines / 25 KB**, so the rest is invisible; instructions to run `npm run x` / `pnpm x` scripts missing from package.json; CLAUDE.local.md committed to git |
| low | backticked paths that no longer exist (stale instructions), CLAUDE.local.md not gitignored, memory files not linked from MEMORY.md, or links to missing ones |
| info | AGENTS.md ignored because a CLAUDE.md exists (add `@AGENTS.md` to read both) |

It understands the loading rules: parent-folder files load at launch, subfolder CLAUDE.md files and `paths:`-scoped rules load on demand, imports inside code spans/blocks are skipped (`` `@README` `` is literal), and block-level HTML comments are stripped (and not counted).

## Fixing
- Over 200 lines: move area-specific instructions into `.claude/rules/<topic>.md` with a `paths:` frontmatter so they only load when Claude touches matching files. Imports don't save context; the imported file loads in full.
- Contradictions and vague rules are a judgment call this script doesn't make. Run Claude Code's built-in `/doctor prompt-audit` for that.
- Stale paths and scripts: update them, or Claude will waste turns looking for files that moved.
