---
name: git-workflow
description: Handle guarded Git and source-control workflows. MUST be used before any commit, branch creation, push, merge, rebase, or pull request. Use when inspecting repository status/history/diffs, matching repository commit and branch conventions, or when cleanup/reporting needs source-control evidence. Never performs mutating Git actions unless explicitly requested.
---
# Git Workflow

## Inspect Before Acting
Before a requested commit or source-control change:
- Inspect `git status`.
- Inspect relevant `git diff` (staged and unstaged as applicable).
- Inspect recent history to match repository conventions.
- Understand what belongs to the logical change.

## Repository Conventions
Detect and follow the repository's own branch naming format rather than inventing one. If it has none, use the default from the global `## GitHub Pushes` rules and continue its sequence. Stage only the files belonging to the logical change.

## QA Artifact Check

Before staging for commit, scan the pending file list for artifacts that exist only to support automatic verification of the change rather than to ship. Seeds, throwaway fixtures, scratch test routes, mock or stub data added only for local QA, ad-hoc verification scripts, and generated test output must be removed or converted into real tests before they are staged. Nothing meant only for automatic QA may be pushed. Legitimate test infrastructure and deliberate seed systems are fine to stage; when unsure, ask.

## Branch Description

The branch / PR description follows the Change Description contract below. Derive the items from the active WIP, the durable change audit, and the actual final diff.

## Jira Backlog Title
When the branch name matches `^[A-Z]+-\d+-(.+)$`, derive the Jira title from the description: split on `-`, uppercase any word of two characters or fewer, capitalize the rest, and join with spaces.

```text
GX-33-be-fix-sales-journey-medicare-admission-count
  → BE Fix Sales Journey Medicare Admission Count
```

Do not derive a title from a branch that does not match, or from a protected branch. Always show the derived title and let the user confirm or correct it before it is used.

The `/git-push` command implements this workflow end to end.

## Release Notes After a Push

After a successful user-requested push, offer paste-ready release notes for the changes accumulated since the previous release, and run `/release-notes` when the user accepts. The offer is one short question. Skip it when there are no eligible changes, and skip asking again when the user declines for that push. Preparing notes never creates a release, a tag, or a pull request, and never changes the completed push.

## Change Description
One contract governs three outputs: the body of a commit, a proposed or authorized PR description, and the ready-to-paste text for a PR the user will open by hand. Do not invent a separate style for any of them.

```text
<One short sentence summarizing the change, if useful.>

1. <Concrete change and observable outcome.>
2. <Another distinct change.>
```

- Use a numbered list, 3–10 items for a substantial change; fewer when only one or two meaningful changes exist. Never pad to reach a count.
- One outcome per item, roughly 15–30 words. Plain language, naming the affected feature or skill when useful.
- Exclude file paths, symbol names, loader mechanics, stack traces, investigation narratives, and test inventories by default.
- Avoid Root Cause, Implementation, Testing, Notes, and Documentation sections in the default body.
- Include a short material limitation when omitting it would mislead. Never hide unresolved risk for brevity, and never claim tests or live behavior passed without observed evidence.
- A detailed body remains available when the user asks for one or repository policy requires it.
- The detailed technical record lives in the change audit and the vault, not in the commit or PR body.

## Commits
Create one focused commit per logical unit. Match existing repository commit style, and apply the Change Description contract to the body.

Prepare and check the subject and body before committing, not after. Write a multiline message through a file outside the repository and commit with `git commit -F`, never an inline shell string, so real newlines survive and nothing is interpolated.

Confirm what was recorded with `git show -s --format=%B HEAD` before a requested push. If it is verbose, say so and offer a corrected commit or a concise PR body. Never silently amend or rewrite an existing shared commit, and never squash history to influence what GitHub prefills.

## Pull Requests
A push does not create or update a pull request. Push authorization is not PR authorization.

After pushing, print the ready-to-paste PR title and body in their own block, visually separate from the console report. Keep the branch name, commit reference, test results, cleanup detail, and required Notes outside that block so they are never copied in by accident.

GitHub suggests a PR title and body from the commit subject and body when the comparison has a single commit. With multiple commits or a template, do not promise the prepared text will appear automatically; give the user the exact text to paste.

When the user separately authorizes PR creation or an update, pass the description explicitly. With `gh`, use a body file with `--body-file`. Never substitute the console report or a vault audit as the PR body.

## Knowledge Sync
After meaningful work, ensure relevant WIP/vault knowledge reflects what is being committed. Do not claim source-control state without checking it.
