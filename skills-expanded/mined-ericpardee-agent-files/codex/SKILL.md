---
name: codex
description: Use when the user asks to run Codex CLI (codex exec, codex resume) or references OpenAI Codex for code analysis, refactoring, or automated editing
---

# Codex CLI

Reference for driving `codex exec` correctly from an agent session. For a
full review gate with a fix-or-rebut loop, use the `codex-gate` skill instead.

## Invocation rules

- Do not pass `-m`. `~/.codex/config.toml` sets the default model; override it
  only when the user names a model. Pair reviews with
  `-c model_reasoning_effort="xhigh"` (options: `none`, `minimal`, `low`,
  `medium`, `high`, `xhigh`).
- Always redirect stdin from `/dev/null`. `codex exec` appends stdin to the
  prompt, so without the redirect it blocks on an open terminal and looks like
  a slow reasoning pass until killed. The tell is empty stdout with
  `Reading additional input from stdin...` on stderr.
- Append `2>/dev/null` to hide thinking tokens (stderr). Show stderr only when
  debugging.
- Sandbox: `--sandbox read-only` for reviews, `workspace-write` for edits,
  `danger-full-access` only for work that needs the network. `--full-auto`
  was removed (codex-cli 0.160 rejects it with `unexpected argument`); a
  `workspace-write` exec run edits without it. Ask before `danger-full-access`
  or `--skip-git-repo-check` unless the user already granted it.
- `-C <dir>` runs from another directory; `--skip-git-repo-check` is needed
  outside a repository.
- `-i <file>` attaches an image and takes a list of files, so it swallows a
  prompt placed after it (the run then fails with `No prompt provided via
  stdin`). Put the prompt before any `-i` flags, or repeat `-i` per file after
  the prompt.
- Pass `-o <file>` when the final message must survive scrollback.

## Reviews

`codex exec review` accepts a scope flag (`--base <branch>`, `--commit <sha>`,
`--uncommitted`) or a custom prompt, never both; combining them fails arg
parsing with `the argument '--base <BRANCH>' cannot be used with '[PROMPT]'`
(codex-cli 0.146 through 0.154). So:

- Codex's own review instructions on a scope:
  `codex exec review --base main </dev/null 2>/dev/null`
- Your own instructions: plain `codex exec` with the scope stated in the
  prompt, for example `codex exec --sandbox read-only "<instructions>. Review
  only the changes on this branch relative to main; see them with git diff
  main...HEAD." </dev/null 2>/dev/null`

## Resuming

`codex exec resume --last "<prompt>" </dev/null 2>/dev/null` continues the
previous session with its original model, reasoning effort, and sandbox; do not
pass configuration flags when resuming unless the user asks. After any run,
tell the user the session can be resumed this way.

## Quick reference

| Use case | Command |
| --- | --- |
| Review a branch | `codex exec review --base main </dev/null 2>/dev/null` |
| Review uncommitted work | `codex exec review --uncommitted </dev/null 2>/dev/null` |
| Review one commit | `codex exec review --commit abc123 </dev/null 2>/dev/null` |
| Review with your own instructions | `codex exec --sandbox read-only "<instructions> Review only <scope>." </dev/null 2>/dev/null` |
| Apply edits | `codex exec --sandbox workspace-write "Refactor ..." </dev/null 2>/dev/null` |
| Resume | `codex exec resume --last "continue with ..." </dev/null 2>/dev/null` |
| Another directory | `codex exec -C /path --sandbox read-only "..." </dev/null 2>/dev/null` |

## After a run

Summarize the outcome. When the output has actionable findings, offer to
resume the session to apply them; do not apply or commit changes on the
user's behalf without being asked. Stop and report when `codex` exits non-zero
or returns partial results, and ask how to proceed.
