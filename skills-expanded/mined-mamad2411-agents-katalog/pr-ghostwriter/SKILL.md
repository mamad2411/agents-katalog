---
name: pr-ghostwriter
description: Use when writing a PR description, commit message, or changelog from a diff — reads changes, infers intent, matches repo style.
metadata:
  added: 2026-06-27
  last_reviewed: 2026-06-27
  type: meta
  status: draft
  related: [commit-writer, pr-description]
  owns: pr-writing
---

# PR Ghostwriter

This skill turns code changes into clear, review-ready documentation. Use it when you need
a PR description, a commit message, or a changelog generated from a diff. It reads diffs
and writes descriptions that help reviewers understand WHAT changed, WHY it changed, and
WHAT to watch for — first person, confident, specific.

Use read-only git only (`git log/blame/show/diff/rev-parse/ls-files/cat-file`). You read
history; you do not change it. The user runs `git commit` / `git push` after reviewing the
draft.

You produce three types of output: PR descriptions, commit messages, and changelogs.

## Process

### Step 1: Read the changes

```bash
git diff --stat HEAD~1          # What files changed
git diff HEAD~1                 # Actual changes
git log -5 | cat                # Recent commit messages — FULL, including bodies, for style matching
git log --oneline -20           # Subject patterns at a glance
```

For PR descriptions, also read the branch name (often contains ticket/feature context) and
any related issue/ticket mentioned in commits.

**Iron rule for commits**: match the existing style exactly. Do not invent a prefix scheme
(`feat:`/`fix:`) for a repo that uses imperative subjects, and do not strip prefixes from a
repo that uses conventional commits. The style is a repo-wide editorial decision; you copy,
you do not legislate. One exception: a lone placeholder commit (`init`, `wip`, or any bare
generic placeholder that names nothing specific) is not a style to match — if that is all
the history holds, fall back to an imperative-with-s subject + prose body rather than echoing
the one-word subject. Look past housekeeping (version bumps, merges) when judging this.

### Step 2: Classify the change

| Type            | Signal                                    | Description Approach                |
| --------------- | ----------------------------------------- | ----------------------------------- |
| **Feature**     | New files, new exports, new routes        | Lead with what users can now do     |
| **Bug fix**     | Changed conditionals, error handling      | Lead with what was broken and how   |
| **Refactor**    | Same tests pass, different implementation | Lead with WHY the change was needed |
| **Performance** | Caching, query changes, algorithm swap    | Lead with measurable improvement    |
| **Config**      | .env, tsconfig, package.json changes      | Lead with what this enables         |
| **Docs**        | README, comments, type annotations        | Lead with what's now clearer        |

### Step 3: Write the description

#### PR description format

```markdown
## What

[1-2 sentences: what this PR does]

## Why

[1-2 sentences: why this change was needed]

## Changes

- [Specific change 1 — what file, what was done]
- [Specific change 2]

## Testing

- [ ] [How to verify change 1]
- [ ] [How to verify change 2]

## Notes for Reviewers

[Anything non-obvious: tradeoffs made, areas of uncertainty, things that look wrong but aren't]
```

#### Commit message format

There is no fixed format — **match the repo's style** as captured in Step 1's
`git log -5 | cat`. Common shapes:

- **Imperative-with-s + prose body** (e.g., toolkit, devkit):

  ```
  Adds plan mode support to review commands

  Detects plan mode at command start and switches behavior: validation is
  read-only, findings append to the active plan file instead of triggering
  edits. Preserves the existing flow when plan mode is inactive.
  ```

- **Conventional commits** (only if the repo already uses them):

  ```
  feat(orders): add bulk-cancel endpoint
  ```

- **One-line minimalist** (small repos, no body for trivial changes):

  ```
  Fix off-by-one in pagination cursor
  ```

Whichever the repo uses, emit something indistinguishable from the existing log. Do not
introduce a new convention; if you think the repo should switch styles, surface that as a
question, not a unilateral change. The minimalist shape applies only when existing subjects
are short **and specific** — a bare generic placeholder (`init`, `wip`) is not a style to
match; use imperative-with-s + prose body instead.

#### Changelog format

```markdown
### [version] — YYYY-MM-DD

#### Added

- [user-facing feature description]

#### Fixed

- [what was broken — user-facing impact]

#### Changed

- [what's different — migration notes if needed]
```

## Rules

- **Read the diff first.** Never write a description from memory or assumption.
- **Be specific.** "Updated user authentication" = bad. "Added JWT refresh token rotation
  with 7-day expiry" = good.
- **Match the project's style.** Read recent commit messages and match their convention.
- **Flag risks.** If a change could break something, call it out in "Notes for Reviewers."
- **No filler.** Every sentence should contain information. Remove "This PR..." and "I've
  made some changes to..."
- **Changelogs are for users.** No internal jargon, implementation details, or file paths.
