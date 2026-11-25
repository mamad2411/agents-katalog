---
name: pr-writer
description: Writes clear pull request titles and descriptions from the actual commits and diff. Use whenever the user is about to open a pull request, asks for a PR description, changelog entry, merge request text or release note for a branch, or says "summarize my changes", even if they only paste a diff or commit list. Collects facts with a script, then writes why, what, how it was tested and risk, and flags breaking changes and missing tests.
---

# pr-writer

A good PR description lets a reviewer decide in a minute what to read first, what could break and how it was verified. The script gathers facts; the writing explains intent.

```
pr-writer/
├── SKILL.md
├── scripts/
│   └── pr_summary.sh         commits, suggested title, changed areas, test and risk signals
└── templates/
    └── pull-request.md       description template with prompts for each section
```

## When to use

- Opening a pull request or merge request
- Turning a branch into a changelog or release note entry
- Summarizing someone else's diff
- Rewriting a vague description such as "fixes stuff"

## Workflow

1. **Collect facts**: `bash scripts/pr_summary.sh origin/main` inside the branch. It lists commits, a suggested title, changed areas, whether tests changed, migrations, dependency and CI changes, breaking change markers and referenced issues.
2. **Read the diff** for the parts that matter (`git diff origin/main...HEAD`). The script cannot know intent; do not invent it. Ask the user for the reason if it is not visible in commits or issues.
3. **Write the title**: imperative, specific, under about 70 characters, in the repository's style (for example `fix(cart): round totals half up`). Check the suggested title; it is only a starting point.
4. **Fill the template** (`templates/pull-request.md`). Delete sections that do not apply instead of writing "N/A".
5. **State testing honestly**: exact commands and results, and what was not tested. If tests did not change, say how the change was verified.
6. **Flag risk**: migrations, auth, dependency, CI or breaking changes get their own note with a rollback path.
7. **Check before sending**: every claim traces to the diff, issue links are right, no secrets or private data.

## Writing rules

- Lead with the effect on users or developers, then the mechanism
- Explain why, not a list of files; reviewers can see the files
- Group by area, not by commit order
- One logical change per PR; if the summary needs "and also", suggest splitting
- Never claim tests passed unless they were run
- Use plain words; avoid "various improvements" and "minor fixes"
- Link the issue: `Closes #123` closes it on merge

## Title quality

| Weak | Better |
|------|--------|
| `Fixes` | `fix(auth): reject expired refresh tokens` |
| `Update code` | `refactor(cart): extract price calculation` |
| `WIP` | `feat(search): add fuzzy matching behind a flag` |

## Changelog entry

When asked for a changelog line, give one sentence from the user's point of view:

```
- Discount codes now apply before tax, so totals match invoices. (#12)
```

## What to report back

| Field | Content |
|-------|---------|
| Title | one line |
| Description | filled template |
| Open questions | anything you could not determine from the diff |
| Suggested follow ups | split, missing tests, docs |

## Related skills

- `commitsmith`: clean commit messages that feed a good PR
- `code-review`: the review the PR will receive; self-review first
- `secrets-hygiene`: scan the diff before pushing
