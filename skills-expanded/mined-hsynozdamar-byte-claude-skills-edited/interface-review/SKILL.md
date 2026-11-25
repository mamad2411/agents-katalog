---
name: interface-review
disable-model-invocation: true
description: Reviews your work across multiple categories like UI, typography, layout, color, writing and accessibility and gives you a detailed analysis of the findings.
---

# Change review

This skill reviews a change, not a screen: it resolves the scope, expands changed files to the surfaces they affect, reads both sides of the diff and gives every finding a status. It owns scope only. Domain rules belong to the `better-*` skills; severity, consolidation, coverage, the cap and the verdict belong to `better-interface`, which receives the review. Correctness, tests, security and performance belong to the project's code review: name such a concern once and move on.

The author asks "did I make this worse?". Report what the change caused; three pre-existing findings is a courtesy, thirty is a different review. Read the whole change and its stated intent before forming an opinion, so no finding targets code the next hunk already fixes.

## 1. Resolve the scope

The whole invocation is the target (`/interface-review pr 482` reviews pull request 482). Accepted targets and how each resolves: [scope-resolution.md](scope-resolution.md). With no target, stop at the first match:

1. `HEAD` is ahead of `git merge-base origin/<default-branch> HEAD`: that range plus uncommitted changes, with commit count and uncommitted file count stated separately.
2. The working tree is dirty: the uncommitted changes.
3. Neither: no change exists, go to step 2.

Check the merge base before the working tree, so one stray edit never shadows a twelve-commit branch. Exclude lockfiles, snapshots, generated output, vendored code and binaries, and name what was excluded.

## 2. No change: ask

A clean tree with nothing ahead of the merge base, or a scope emptied by exclusions, means there is nothing to review; the report says so and is never an `Approve` of nothing. Falling back to `HEAD~1..HEAD` on your own produces a report on whatever last landed. Instead state the repository facts ([Nothing to review](scope-resolution.md#nothing-to-review)) and offer, after checking for an open pull request on the current branch (offered first, since a branch whose commits landed still has its PR):

- the last commit, named by short SHA and subject;
- a target they name (`pr <n>`, branch, ref, range), resolved per step 1;
- a whole-repository interface audit, which is not a change review: hand it to `better-interface` as repository scope, without this skill's scope block, statuses or pre-existing section.

When exclusions emptied the scope, say which files were excluded.

## 3. Expand to surfaces

A changed file is evidence; the review subject is the set of surfaces it renders in. Expand one hop (direct importers and callers), two for design tokens, theme values and shared primitives. Review at most five consumers, ordered by [the rule in Scope resolution](scope-resolution.md#expanding-to-consumers), and state how many were not expanded.

## 4. Read the removed lines

Regressions hide on the `-` side. Check every hunk's removed lines against [removed-signals.md](removed-signals.md). A signal is a lead: it is a regression only when nothing in the change replaces it. Route each unmatched removal to its domain skill, report only what that skill confirms, status `Regression`.

## 5. Classify every finding

- `Introduced`: the change created it.
- `Regression`: the change weakened something previously correct.
- `Pre-existing`: present in touched code but not caused by this change.

Status by what the diff touched, not by file: an untouched line three lines from a hunk is `Pre-existing`. Confirm when it matters with `git blame -L <line>,<line> "$BASE" -- path/to/file`. Hand every finding up with its status to `better-interface`.

## 6. Hold the change to its stated intent

Read the PR title and body, the linked issue and the commit messages, then check the interface delivers what they claim. This catches the **incomplete** change that a review of present states cannot see:

- a new variant, size or theme covering some states but not all (hover, focus, active, disabled, loading, selected);
- a new user-facing string missing from the project's translation catalogue;
- a new component without empty, loading, error, disabled or narrow-width states;
- a control added to one surface but not the siblings that carry its peers.

Scope creep is a process question and stays out of the report.

## 7. Hand off to better-interface

Give `better-interface` the scope block, the affected surfaces and a status on every finding; it routes to the domain skills, applies severity, consolidates, enforces the cap and issues the verdict. If it is unavailable, report the resolved scope and file inventory, name it as the missing skill and stop; this skill defines no severity scale, cap or verdict of its own.

## 8. Read-only

Fetch PR refs and review them in place. `git fetch` is fine; `gh pr checkout`, `git checkout`, `git switch` and `git stash` rewrite the author's open files and are out. Visual and runtime claims are `Not verified` unless the project has a cheap preview or the user asks for a rendered review; then use an isolated worktree (`git worktree add /tmp/review-<n> refs/remotes/pr/<n>`) and remove it afterwards. Cite line numbers against the head ref named in the scope block.

## Output

Open with the scope block:

| Field | Value |
| --- | --- |
| Target | `branch`, `working`, `staged`, `pr 482`, or the range as entered |
| Base ref | `origin/main` at `a1b2c3d` |
| Head ref | `refs/remotes/pr/482` at `e4f5g6h` |
| Commits | 7 committed, 2 files uncommitted |
| Files in scope | 12 after exclusions |
| Excluded | `pnpm-lock.yaml`, `src/__snapshots__/`: lockfile and snapshots |
| Surfaces expanded | `CheckoutPage`, `SettingsPanel`; 3 further `Button` consumers not expanded |

The coverage table follows unchanged; a domain with no evidence in scope reads `Not reviewed: no evidence in the change scope`. Then the findings:

| Severity | Domain | Status | Location | Before | After | Why |
| --- | --- | --- | --- | --- | --- | --- |
| HIGH | Accessibility | Regression | `src/Dialog.tsx:42` | `aria-label="Close"` removed in this change | Restore `aria-label="Close"` on the icon-only control | The close control had an accessible name before this change and no longer does |

With no `Introduced` or `Regression` findings, omit the table and write "No actionable interface findings in this change."

Then at most three `Pre-existing` findings, highest severity first, stated as not this change's responsibility (omit the section when none):

| Severity | Domain | Location | Issue |
| --- | --- | --- | --- |
| MEDIUM | Typography | `src/Toolbar.tsx:7` | Numeric badges use proportional figures; predates this change |

The cap and verdict cover `Introduced` and `Regression` only; `Pre-existing` findings sit outside both, so a change with only pre-existing findings is an `Approve`. End with `Block` when any `HIGH` remains, otherwise `Approve`; severity scale and cap come from `better-interface`.
