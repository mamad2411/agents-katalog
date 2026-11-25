---
name: branch-and-title-conventions
description: "Derives branch names, commit scopes and PR or MR titles from the issue key: <prefix>/<KEY>-<summary> and <type>(<KEY>): <description>. Use when creating a branch or opening a PR or MR. Not for commit types (use dev-standards:commit-standards); not for issue state (use tracker-discipline)."
allowed-tools: Bash(git branch --show-current), Bash(printenv CLAUDE_TICKET_PATTERN)
license: MIT
---

# Branch and Title Conventions

This skill owns the branch-name and PR/MR-title shape for every forge. The forge skills
(`github-workflow:pr-lifecycle`, `gitlab-workflow:mr-lifecycle`) run the create commands and take
the title and branch from here. `dev-standards:commit-standards` owns the `<type>` vocabulary,
the scope charset and release impact.

The rule underneath: the issue key is recoverable from the branch name. The commit scope, the
title, the changelog line and the tracker link are then derived rather than remembered.

## The key

The key is whatever the ticket pattern matches. The pattern comes from the `Ticket pattern`
row of the project's `## Issue tracker` section, else `printenv CLAUDE_TICKET_PATTERN` in Claude
Code, else `[A-Z][A-Z0-9]+-[0-9]+`. The `tracker-discipline` skill's
`references/tracker-config.md` explains the order and how to set each.

## Branch names

```
<prefix>/<KEY>-<short-summary>
```

- `<prefix>` is the commit type of the main change, with `feat` spelled `feature`: `feature`,
  `fix`, `perf`, `refactor`, `docs`, `test`, `build`, `ci` or `chore`.
- `<short-summary>` is two to five lowercase kebab-case words: enough to recognise the branch in
  a list, not the issue title.
- With no tracker (the `Tracker` row is `none`), drop the key: `<prefix>/<short-summary>`.

```
feature/PROJ-123-add-auth-middleware
fix/PROJ-456-null-deref-on-empty-payload
refactor/PROJ-789-simplify-payment-flow
```

Claude Code's built-in worktrees choose their own directory and branch name. Before the first
push from one, rename its branch to this shape with `git branch -m <prefix>/<KEY>-<summary>`.

## PR and MR titles

```
<type>(<KEY>): <description>
```

`<type>` and the description rules (imperative, lowercase first word, no trailing period, header
under about 72 characters) come from `dev-standards:commit-standards`. This skill adds one rule:
when the work has a key, the scope is the key. A squash merge that takes the PR title as its
commit header then needs no editing.

```
feat(PROJ-123): add org hierarchy endpoint
fix(PROJ-456): route gateway traffic through the stable alias
chore(PROJ-789): bump runtime dependencies
```

A forge's closing reference goes in the body, not the title; for example GitHub closes an issue
from `Fixes #123` in the PR body. The adapter (`github-issues`, `jira-tracker`) says which form
its tracker needs.

## When the branch has no key

| Situation | Title | Branch |
| --- | --- | --- |
| Tracker configured, key known from the message or session | `<type>(<KEY>): …` | Rename if unpushed and nobody else has it; otherwise leave it and name the key in the PR body |
| Tracker configured, no key known | Ask for the key first (the `pre-work-gate` question) | As above, once the key is known |
| User chose to proceed without an item, or `Tracker` is `none` | `<type>(<component>): …` or `<type>: …`, per `dev-standards:commit-standards` | `<prefix>/<short-summary>` |

Use a key only when the tracker or the user supplied it; a made-up key points every later search
at the wrong item. Prefer the title fix over renaming a shared branch, because a rename breaks
everyone else's checkout.

## Examples

<example>
Branch `fix/PROJ-456-null-deref-on-empty-payload`; the change guards a null payload.
Title: `fix(PROJ-456): handle empty payload in intake parser`
</example>

<example>
Branch `dana-wip`, already pushed and shared; the user says the work is PROJ-212, a new export
option.
Title: `feat(PROJ-212): add csv export option`. Keep the branch name and write "Tracks PROJ-212"
in the PR body.
</example>

<example>
`Tracker` is `none`; the change bumps a linter.
Branch `chore/bump-linter`, title `chore(lint): bump eslint config`.
</example>

## Verify

Before creating the branch or opening the PR or MR:

- the branch matches `^(feature|fix|perf|refactor|docs|test|build|ci|chore)/` followed by the
  key (when there is one) and a kebab-case summary;
- the title's scope equals the key the pattern extracts from the branch, or the key the user
  supplied;
- the title passes the header check in `dev-standards:commit-standards`.

Without a checkout, check a pasted branch name and title the same way.
