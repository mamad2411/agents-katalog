---
name: onboarding-guide
description: "Builds a developer onboarding doc from the repo's actual setup, scripts, conventions and CI, so day-one questions get answered in writing."
---

# Onboarding guide

Describe how this team really works, as proven by the repository.

## Steps

1. Survey the repo: top-level layout, manifests, scripts, Docker and compose files, CI workflows, linters and formatters, test setup, pre-commit hooks, CODEOWNERS and any existing docs.
2. Mine conventions from evidence. Use recent history (`git log --oneline -50`) for commit message style, branch naming and PR size. Read lint and format config for code style. Read CI for what must pass before merge.
3. Write the guide with these sections: What this system does and who uses it; Architecture in one page (main modules and how a request or job flows through them); Local setup (verified commands); Daily workflow (branch, test, lint, open PR, review, deploy); Conventions (naming, errors, logging, tests); Where things live (a table of folder to purpose); Who to ask (from CODEOWNERS only).
4. Add a "first task" walkthrough: a tiny real change such as editing a message string, taken from setup to merged.
5. Finish with Open questions, listing facts you could not find.

## Rules

- State only what you found. Cite the file for each convention.
- No org charts, no wishes, no marketing text.
- Keep it under 800 lines and link to deeper docs.

## Report

The guide path, what you verified by running it, and the open questions for the team to answer.
