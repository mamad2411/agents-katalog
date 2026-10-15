---
name: pr-hygiene
description: Make PRs merge-ready — tight scope, clear description, no leftover debug, honest test notes. Use when opening a PR, writing a PR description, cleaning a branch before review, or when the user mentions pull request, merge-ready, or PR hygiene.
---

# PR Hygiene

Turn the current work into a PR a human can review in one pass.

## Before opening

- [ ] Branch contains **one** logical change (or clearly labeled stacked commits)
- [ ] No leftover `console.log`, `debugger`, `TODO: temp`, commented-out blocks you added
- [ ] No unrelated formatting-only churn
- [ ] Secrets, `.env`, and local-only files are not staged
- [ ] Diff matches the stated goal — nothing "extra helpful"

## Description template

Use this structure (adapt section names to the host: GitHub/GitLab):

```markdown
## Summary
<1–3 bullets: what and why>

## Test plan
- [ ] <how you verified>
- [ ] <edge case worth checking>

## Notes
<risks, follow-ups, screenshots if UI>
```

## Commit / PR title

- Imperative, specific: `fix checkout: reject expired discount codes`
- Not: `update stuff`, `fix`, `WIP`, `address comments`

## Reviewer empathy

Call out:

- Files that look scary but are mechanical (renames, generated)
- Behavior that changed for callers/API consumers
- Anything you are unsure about

## Anti-patterns

- NEVER mix refactor + feature + dependency bump in one PR unless required
- NEVER force-push shared branches without warning
- NEVER open a PR with "tests TBD" and no plan
- NEVER bury breaking changes in the middle of the description

## If asked to open the PR

1. Summarize the diff in your own words first
2. Draft title + body with the template
3. List residual risks in one short section
