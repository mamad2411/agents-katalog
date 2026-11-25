---
name: branch-name-standard
description: 'Use when: creating, naming, renaming, reviewing, or auditing a Git branch in this repository. Applies to feature branches, fix branches, hotfixes, release branches, chore work, refactors, docs, CI, build, or any branch that will be pushed or reviewed.'
---

# Branch Name Standard

Use this skill **before** running `git checkout -b` or `git switch -c`. The repository follows a Conventional-Commits–aligned branch naming scheme so branch names map 1:1 to commit type categories and to issue tracker entries.

## Format

```
<type>/<short-kebab-description>
<type>/<issue-id>-<short-kebab-description>   # when an issue / ticket exists
```

- All lowercase.
- Words inside the description are joined with `-` (kebab-case). No spaces, no `_`, no `CamelCase`.
- Total length ≤ 50 characters; description ≤ ~40 chars after the prefix.
- Description is a short, actionable noun phrase, not a sentence (`add-ink-panel`, **not** `i-am-adding-the-new-ink-panel`).
- One slash only — `<type>/<desc>`. Do not nest (`feat/sub/foo` is wrong).
- Use ASCII; no Unicode, no emoji.

## Allowed `<type>` Values

The type set is the same as Conventional Commits used by `commitlint.config.mjs`:

| type       | when to use                                                              |
| ---------- | ------------------------------------------------------------------------ |
| `feat`     | New user-visible feature or new public API surface.                      |
| `fix`      | Bug fix that resolves incorrect behavior.                                |
| `hotfix`   | Urgent fix branched off a release tag, intended for immediate deploy.    |
| `chore`    | Maintenance work that is not feat/fix (deps bumps, repo housekeeping).   |
| `docs`     | Documentation-only changes.                                              |
| `refactor` | Code change that neither fixes a bug nor adds a feature.                 |
| `test`     | Adds or fixes tests only.                                                |
| `perf`     | Performance improvement.                                                 |
| `build`    | Build system, bundler, packaging, tsup/vite/turbo config changes.        |
| `ci`       | CI configuration only (workflows, hooks).                                |
| `revert`   | Reverts a previous commit / branch.                                      |
| `release`  | Release preparation branch (version bump, changelog).                    |
| `wip`      | Personal work-in-progress only — must not be opened as PR until renamed. |

## Examples

Good:

- `feat/quality-gate-ink-panel`
- `feat/123-quality-gate-ink-panel`
- `fix/mcp-resource-notifier-race`
- `chore/bump-pnpm-10.15`
- `docs/agentils-readme-walkthrough`
- `refactor/cli-template-loader`
- `ci/precommit-gate-runner`

Bad:

- `Feature_Add_New_Panel` — uppercase, snake_case, no type prefix.
- `feat/add the new ink panel for the pre commit gate` — spaces, too long.
- `agentils/feat/panel` — wrong order, extra slash.
- `panel` — missing type prefix.
- `feat/✨-shiny` — emoji / non-ASCII.

## Procedure

1. Pick the single `<type>` that matches the dominant change. If the change spans types, choose the user-visible one (`feat` over `refactor`, `fix` over `chore`).
2. If an issue tracker ID exists, prepend it to the description: `feat/123-quality-gate-ink-panel`.
3. Write the description as 2–5 kebab-case tokens summarizing the **outcome**, not the steps.
4. Run `git checkout -b <name>`. Never push directly to `main`.
5. When opening a PR, the PR title should mirror the branch using a Conventional Commit header: `feat(quality-gate): ink ECAM panel`.

## Rename Recovery

If a branch is already created with a non-conforming name:

```sh
git branch -m old-bad-name <type>/<good-desc>
git push origin :old-bad-name <type>/<good-desc>
git push origin -u <type>/<good-desc>
```

(Only rebase the upstream rename if no one else has based work on the old name.)

## Cross-References

- `commitlint.config.mjs` — defines the same `<type>` taxonomy for commit messages.
- `instructions-sync-discipline` skill — for the related rule that this SKILL file is a generated **target**; edit only `docs/skills/branch-name-standard/SKILL.md`.
