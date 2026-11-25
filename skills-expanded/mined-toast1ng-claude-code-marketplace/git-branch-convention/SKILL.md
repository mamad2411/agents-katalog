---
name: git-branch-convention
description: Suggest a git branch name following team conventions. Use this skill whenever the user wants a branch name or asks what to name their branch — in English or Korean. Trigger on phrases like "suggest a branch name", "branch name for this", "branch convention", "what branch should I use", "브랜치 이름 추천해줘", "브랜치 이름 만들어줘", "브랜치 뭐로 할까", "브랜치 컨벤션", "이 작업 브랜치 이름".
---

Suggest a branch name for the given task following the branch naming convention below.

## Format

```
<type>/<short-description>
```

- All lowercase, kebab-case (words separated by hyphens)
- Output only the branch name, nothing else

## Slug length rules (non-negotiable)

The slug (the part after `type/`) must satisfy **both** of these:

1. **3–4 words maximum** — if you have more, cut the least important word
2. **30 characters maximum** — if you're over, shorten or abbreviate words

When in conflict, prioritize the character limit. These are hard limits, not guidelines — if the first draft is too long, revise before outputting.

## Branch types

| Type | When to use |
|------|-------------|
| `feature/` | New functionality or enhancement |
| `fix/` | Bug fix |
| `hotfix/` | Urgent fix that needs to go to production immediately |
| `chore/` | Maintenance, configuration, dependency updates |
| `refactor/` | Code restructuring with no behavior change |
| `docs/` | Documentation only |
| `test/` | Adding or fixing tests without changing production code |

## Steps

1. Understand what the user is working on from their message or the current conversation context.
2. Pick the most fitting type from the table above.
3. Derive a short, descriptive slug from the task — drop articles and filler words, keep the core noun + verb.
4. Output the branch name.

## Examples

| Task | Branch name |
|------|-------------|
| Add login page with JWT auth | `feature/add-login-page` |
| Fix off-by-one error in pagination | `fix/pagination-off-by-one` |
| Critical production crash on checkout | `hotfix/checkout-crash` |
| Upgrade dependencies | `chore/upgrade-dependencies` |
| Extract payment logic into service | `refactor/extract-payment-service` |
| Update API documentation | `docs/update-api-docs` |

## Rules

- Output only the branch name. No explanation, no alternatives, no extra text.
- Do not use uppercase, underscores, or spaces.
- Do not include a ticket number.
