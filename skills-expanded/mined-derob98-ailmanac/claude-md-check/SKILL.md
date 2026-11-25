---
name: claude-md-check
description: Use when the user asks to review, audit, improve, shorten or write a CLAUDE.md, CLAUDE.local.md, AGENTS.md or .claude/rules file, or says Claude Code keeps ignoring their instructions or forgetting project conventions. Checks the file against the repository it describes and against how memory files actually load, then reports concrete fixes.
---

# CLAUDE.md check

A memory file is read at the start of every session, so each line either helps
every future task or quietly costs context and trust. This check finds the
lines that are wrong, vague or misplaced.

Report first. Do not edit any file until the user asks.

## 1. Find what is loaded

Look for, and read, every one that exists:

- `./CLAUDE.md` or `./.claude/CLAUDE.md` — project instructions, committed
- `./CLAUDE.local.md` — personal notes for this project, should be gitignored
- `./.claude/rules/*.md` — topic files, discovered recursively
- `./AGENTS.md` — shared with other coding agents
- `~/.claude/CLAUDE.md` — the user's preferences across all projects

If the working directory is inside a larger repository, check the parent
directories too: files above the working directory load at launch, files in
subdirectories load only when Claude works there.

## 2. Refresh the specifics

Loading rules change between releases. Before judging, fetch
`https://derob98.github.io/ailmanac/docs/claude-code/claude-md.md` and note
the verified date on its `> Source:` line and the official source named in its
`VerifyNote`.
If the fetch fails, continue with the checks below and say that the specifics
could not be refreshed.

## 3. Check each file

Verify claims against the repository instead of reading them on trust.

| Check | How to verify | Typical fix |
| --- | --- | --- |
| **True today** | Every command, script, path and tool it names exists: compare with `package.json` scripts, `Makefile`, `pyproject.toml`, the directory tree. | Correct or delete the line. A stale instruction is worse than none. |
| **Run, test, lint** | The file says how to install, run, test and lint. | Add the exact commands. |
| **Checkable, not wishful** | Flag lines nobody could verify, such as "write clean code" or "follow best practices". | Replace with the concrete rule, or delete. |
| **Only what cannot be inferred** | Flag lines that restate what the code already shows. | Delete. Keep naming, structure and commit conventions that are not obvious. |
| **No pasted documents** | Long copied sections of a README, style guide or API reference. | Import instead: `@path/to/file`. |
| **Imports resolve** | Each `@path` exists. Relative paths resolve against the file that contains the import, not the working directory. A path with spaces needs backslashes; quoting it does not work. An `@path` inside backticks is literal text, not an import. Imports nest to a limited depth. | Fix the path or the escaping. |
| **Right file for the scope** | Personal preferences in a committed file; machine-specific values such as local URLs in a shared file. | Move to `~/.claude/CLAUDE.md` or `CLAUDE.local.md`. |
| **`CLAUDE.local.md` is ignored** | `git check-ignore CLAUDE.local.md` | Add it to `.gitignore`. |
| **No secrets** | Tokens, passwords, private keys, internal credentials. | Remove and rotate. Say so plainly. |
| **No contradictions** | The same topic stated differently in two files. | Keep one statement in the narrowest file that needs it. |
| **Size** | A file that has grown past what someone would read in a minute. | Split into `.claude/rules/*.md`, one topic per file; add `paths` frontmatter so a rule loads only for matching files. |
| **Hard rules are enforced elsewhere** | "Never" and "always" lines that must not be broken. | Memory files are context Claude weighs, not enforcement. Suggest a permission `deny` rule or a `PreToolUse` hook for anything that must be blocked. |

## 4. Report

Lead with a one-line verdict. Then list findings, most damaging first, each as:
the line or section, why it is a problem, and the exact replacement text. Group
trivial findings on one line. End with what is already good, in a sentence, so
the user knows what to keep.

Cite the page you refreshed from and its verified date:

`Reference: CLAUDE.md & Memory Files — https://derob98.github.io/ailmanac/docs/claude-code/claude-md (verified YYYY-MM-DD)`

Then offer to apply the fixes.

## If there is no file yet

Say so, and offer two routes: run `/init` and trim the draft to what is true,
or start from a template at
https://derob98.github.io/ailmanac/docs/templates/claude-md. Either way the
result should state what the project is, how to run, test and lint it, the
conventions that are not obvious from the code, and the guardrails.
