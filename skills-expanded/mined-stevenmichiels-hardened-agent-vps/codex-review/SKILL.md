---
name: codex-review
description: Run Codex CLI as a read-only reviewer from Claude and save a Markdown review report. Use when the user asks Codex to review a diff, create codex-review.md, get a second opinion from Codex, compare Claude/Codex work, or use one agent to develop while the other reviews. Supports uncommitted, commit, and base-branch reviews through Codex's native review command.
trigger: /codex-review
---

# Codex Review

## Core Rule
Use Codex as a reviewer, not a co-editor. One agent develops in the worktree; the other produces a Markdown review. The reviewer must not stage, commit, or edit source files.

## Workflow
1. Make sure the implementation agent has produced a normal git diff, or identify a commit/base to review.
2. Locate this skill's bundled helper at `scripts/claude-codex-review` relative to this `SKILL.md`.
3. Run the helper from the target repository root:
   ```bash
   /path/to/codex-review/scripts/claude-codex-review "Review the current diff as a strict senior engineer."
   ```
4. Read the generated Markdown report under `.claude/reviews/`.
5. Decide which findings to apply. Apply changes as the primary agent.
6. If the review report should be versioned, inspect it first and commit only the Markdown report in a separate commit.

## Review Modes
Default mode reviews staged, unstaged, and untracked changes:

```bash
/path/to/codex-review/scripts/claude-codex-review
```

Review one committed change:

```bash
/path/to/codex-review/scripts/claude-codex-review --commit HEAD
```

Review the current branch against a base:

```bash
/path/to/codex-review/scripts/claude-codex-review --base main
```

## Output Path
Default output is timestamped:

```bash
.claude/reviews/codex-review-YYYYMMDDTHHMMSSZ.md
```

Use `-o` for a stable path:

```bash
/path/to/codex-review/scripts/claude-codex-review \
  -o codex-review.md \
  "Check whether this implementation is overengineered."
```

## Context Included
The helper calls Codex's native `codex review` command and adds:
- the reviewer task
- up to three recently modified `.codex/plan/*.md` files as prompt context
- mode metadata in the Markdown report

The plan does not need a fixed name. To omit plan context:

```bash
CODEX_REVIEW_INCLUDE_PLAN=0 \
  /path/to/codex-review/scripts/claude-codex-review
```

## Safety Controls
- Codex runs through `codex review`, not `codex exec`.
- The helper refuses likely secret-bearing paths by default, such as `.env`, `secrets/`, `config/credentials.json`, and private key filenames.
- The helper refuses diffs larger than `CODEX_REVIEW_MAX_DIFF_BYTES` (default `200000`) unless explicitly overridden.
- The helper never stages, commits, or edits source files.

Useful overrides:

```bash
CODEX_REVIEW_MAX_DIFF_BYTES=400000 \
  /path/to/codex-review/scripts/claude-codex-review

CODEX_REVIEW_ALLOW_LARGE_DIFF=1 \
  /path/to/codex-review/scripts/claude-codex-review
```

Use `CODEX_REVIEW_ALLOW_SENSITIVE_DIFF=1` only after manually confirming the diff contains no secrets.
