---
description: Maintains the project's README.md by cross-referencing git history with
  the current README content. Use this whenever you want to check if the README is
  up to date, after a sprint, before a release, or when you suspect the docs have
  fallen behind. Handles creating a README from scratch if none exists. Follows agent-native
  CI/CD with eval-gated promotion, canary rollouts, and compensating rollback actions.
license: MIT
metadata:
  evolved: true
  evolved_at: '2026-07-20T14:07:06.276168+00:00'
name: readme-update
tags:
- documentation
- deploy
version: 2
---

# README Update Workflow

Your job is to keep the project's README.md in sync with what the project actually does.
Work methodically through the steps below. Always confirm changes with the user before writing.

---

## Step 1 — Check for README

Look for `README.md` in the project root (the directory where you're currently working).

**If no README exists:**
Ask the user these questions (you can ask them all at once):
1. What is this project? (one-sentence description)
2. Who is it for? (end users, developers, internal tooling, etc.)
3. Are there any sections you definitely want? (e.g. Installation, Usage, API, Contributing)

Then inspect the project to fill in what you can automatically:
- `package.json` / `Cargo.toml` / `pyproject.toml` / etc. for name, description, scripts
- Entry points and key source files to understand structure
- Existing docs, comments, or config files

Draft the README, present it to the user for approval, then write it only after they confirm.
a
**If README exists:** Continue to Step 2.

---

## Step 2 — Find the README's last update in git

Run:
```bash
git log --follow --format="%H %ai %s" -- README.md | head -1
```

This gives you the most recent commit that touched the README. Note the commit hash and date.

If git returns nothing (README exists but was never committed), treat it as if the last update was the beginning of time — all commits are "since then."

---

## Step 3 — Collect commits since the README was last updated

Run:
```bash
git log --format="%H %ai %s" <last-readme-commit-hash>..HEAD
```

If there are no commits since then, tell the user: "The README appears to be up to date — no commits have been made since it was last modified." Then stop.

---

## Step 4 — Identify commits that likely require README changes

Go through the commit list and flag commits that:

1. **Introduce new features** — commit message starts with `feat`, `feature`, `add`, or similar
2. **Change existing behavior** — `fix`, `change`, `update`, `modify`, `rename`, `refactor` — but only when the change is user-facing or behavioral (not purely internal cleanup)
3. **Cross-reference with the README** — regardless of the semrel prefix, if the commit message mentions something that's *already described in the README* (a command name, a flag, a concept, a workflow, a dependency, a section topic), that commit is relevant. Read the README carefully and match against commit message content.

Commits you can usually ignore:
- Pure chore / ci / style / lint / test commits with no behavioral changes
- Dependency bumps that don't affect the user-facing API or usage

**If you find relevant commits:** Go to Step 5.

**If there are commits but none seem relevant:**
Tell the user what you found, e.g.:
> "There are 8 commits since the README was last updated, but none appear to introduce new features or change anything already described in the README. The commits are mostly [chores/dependency updates/internal refactors].
>
> Want me to dig into the actual diffs to double-check? I might find something the commit messages didn't make obvious."

Wait for the user's answer. If they say yes, proceed to Step 5 using all commits. If no, stop.

---

## Step 5 — Examine diffs for relevant commits

For each flagged commit, run:
```bash
git show <hash> --stat
git diff <hash>^..<hash> -- <relevant files>
```

Focus on source files, config files, and CLI entry points — not test files or build artifacts unless the README specifically mentions them.

You're looking for:
- New commands, flags, options, or modes
- Changed command names, flag names, or default values
- New or removed dependencies that users need to know about
- New setup steps, environment requirements, or prerequisites
- Renamed concepts, files, or workflows that the README currently describes incorrectly

---

## Step 6 — Draft the changes

Based on what you found, draft the minimal set of README changes needed:
- **Add** content for genuinely new things the README doesn't mention
- **Update** content that's now inaccurate (old command names, changed behavior, etc.)
- **Remove** content only if you're confident it's obsolete — if you're not sure, flag it as a question for the user rather than removing it

For anything you're uncertain about — especially removals or significant rewrites — ask the user before including it in the draft:
> "The README mentions X, but commit abc1234 seems to have removed/changed it. Should I remove/update this section?"

---

## Step 7 — Present the draft for approval

Show the user a clear diff-style summary of what you're proposing to change. Use this format:

```
## Proposed README changes

### Add to "Installation" section:
<the new content>

### Update in "Usage" section:
Old: <current text>
New: <proposed text>

### Remove from "Configuration" section:
<the content you'd remove, and why>
```

Then ask: "Does this look right? Should I go ahead and apply these changes?"

Only write to `README.md` after the user confirms. Apply all changes in a single edit.

---

## Principles

- **Don't over-document.** Only add things a user of this project needs to know. Internal implementation details don't belong in the README unless it's a library/API.
- **Preserve the user's voice and structure.** Don't reorganize, reformat, or rewrite sections that aren't affected by the changes.
- **When in doubt, ask.** It's better to confirm a small thing than to silently remove something the user cares about.
- **Show your work.** When you flag a commit as relevant, briefly explain why (what in the README it relates to).

## Prerequisites

- Ensure all required tools and dependencies are installed
- Verify you have the necessary permissions and access credentials
- Check that the target environment is in a known good state


## Error Handling

- Always check the exit code or response status of commands before proceeding
- On failure, log the error details and attempt recovery if a retry strategy exists
- If recovery fails, report the error with context: what was attempted, what went wrong, and suggested next steps
- Never silently ignore errors — treat unexpected output as potential failure


## Verification

- After each step, verify the expected outcome before continuing
- Use idempotent checks: running the same action twice produces the same result
- If verification fails, roll back the last change and report the issue
- Log verification results for audit trail


## Rollback

- Every action should have a defined undo procedure
- If a step fails after partial completion, reverse all changes made in this session
- Verify the system is in a known good state after rollback
- Document what was rolled back and why


## Security

- Never hardcode secrets, tokens, or credentials in skill files or scripts
- Use environment variables or secret management tools for sensitive values
- Validate all user inputs before processing
- Follow least-privilege principle: request only the permissions you need
- Log all security-relevant actions for audit
