---
name: claude-to-agy
description: Offloads heavy, token-intensive reasoning and search tasks to Antigravity CLI (agy) via MCP. MANDATORY delegation for grep, git diff, git log, large files, multi-file analysis.
---

# Skill: claude-to-agy

This workspace is equipped with a custom MCP bridge that connects Claude to the local `agy` CLI. It enables Claude to safely delegate massive reasoning tasks, huge file reads, and web searches without exhausting its own context window.

## The routing gate - consume vs. operate

Before any read, search, or analysis, pick the mode:

- **Operate-on** - code you're about to edit. Read the file and edit it yourself - even if it's over 200 lines; don't delegate it. Never edit from a summary.
- **Consume-and-discard** - you want a verdict, not the bytes (audits, searches, reviews, git history, external research). Delegate to agy.
- **Unsure which mode?** If you don't yet know whether you'll edit, treat it as consume and delegate. Only keep it local once you've committed to editing it.

If a review leads straight into editing the same file, read it locally once - don't delegate then re-read it.

## Terminal Command Delegation

**BEFORE** running ANY of these commands in a terminal, you MUST use `delegate_to_agy` instead:

- `grep` - always delegate. Flag combinations (`-r`, `-A`, `-B`, `-C`) make output size unpredictable regardless of `-m`.
- `git diff` / `git log` - delegate by default. **Exception:** when you can bound it small and need it inline - `git log -n 5`, `git diff --stat`, a `git diff` of the single file you just touched - run it directly.

**NEVER** run grep directly. **NEVER** run unbounded `git diff` / `git log` directly. This applies during ALL phases: planning, exploration, implementation, review.

## Delegation Thresholds

Consume-and-discard work goes to agy per the gate above. On top of that, delegate when ANY of these conditions are met:

1. **File length >200 lines**: Any analysis, review, or reading of files exceeding 200 lines.
2. **Multi-file analysis (>3 files)**: Bug hunting, architecture review, or debugging spanning more than 3 files.
3. **Web/external knowledge**: Documentation lookups, current-info queries, research digs - always delegate. A fetched page lands in context whole, however small the answer.
4. **Adversarial review / plan critique**: Always delegate.

If you are unsure whether a file exceeds 200 lines, delegate it anyway - Antigravity CLI handles the cost, not you.

## STOP & VERIFY

**You are violating these rules if**:

- You edited from agy's summary instead of reading the file yourself. Editing is local - never edit from a summary.
- You ran `grep` directly, or an **unbounded** `git diff` / `git log` in-terminal instead of delegating. (Bounded git commands like `-n 5` or `--stat` are fine).
- You read a whole file over 200 lines locally to audit or review it, instead of delegating.
- You answered a consume trigger from memory instead of verifying - code changes.

## Rationalization Table

| Excuse                                                            | Reality                                                                                               |
| ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| "I already know this / can answer from memory."                   | Code changes and memory goes stale. If you're verifying or consuming, delegate.                       |
| "The file is probably small."                                     | If you're consuming and unsure, delegate - don't guess.                                               |
| "It's faster if I just read it."                                  | For consume work, context-budget conservation outranks speed.                                         |
| "I only need a small part of the file."                           | _Consuming_ → delegate the whole file, let agy extract. _Editing_ → just read the file and edit it.   |
| "I'll just delegate this file I'm about to edit."                 | It's operate-on: read the file and edit it yourself. Never edit from a summary.                       |
| "I just ran a bounded git command, so this next one is fine too." | _Independent bounds_ → a prior bounded command doesn't make an unbounded one safe. Re-check per call. |

## How to Delegate

- Formulate a clear, detailed `prompt` explaining exactly what needs to be found, analyzed, or searched. **CRITICAL: You must explicitly instruct agy in your prompt to act in READ-ONLY mode and forbid it from modifying any files or running mutating commands.**
- **Always pass `cwd`** with your current working directory (absolute path) so agy knows where the project is.
- Call `delegate_to_agy` with your `prompt`, `cwd`, and any relevant file paths in the `files` array.
- Await the text response and use the summary/data provided by agy to fulfill the user's request.
