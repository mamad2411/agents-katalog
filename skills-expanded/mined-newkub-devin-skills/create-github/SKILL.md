---
name: create-github
description: Create GitHub resources — issue, PR, repo via create-github-* skills
argument-hint: "[domain]"
related:
  - list-github
  - git-push
  - ask-me

---

## Goal

Dispatch to the right skill based on the GitHub resource to create — the parent only does routing

## Scope

- (pr is a submodule `create-github-pr`)
- the argument is the domain; if not specified → `/ask-me` picks the domain

## Execute

### Create GitHub Skills

| Domain | Skill |
|---|---|
| `issue` | `/create-github-issue` — create an issue with template/labels |
| `pr` | `/create-github-pr` — create a pull request (submodule: create-github-pr) |
| `repo` | `/create-github-repo` — create a new repo with init settings |

1. Determine the domain from the argument (e.g. `/create-github pr`)
2. If the domain is supported → call the skill from the table and follow that skill's flow
3. If the domain is missing or unrecognized → `/ask-me` picks the domain

## Rules

- the parent only dispatches — never duplicate the target skill's workflow
- use the `gh` CLI or GitHub MCP tools as available in that skill

- Use /list-github if needed
- Use /open-github if needed
- Use /git-push if needed

## Expected Outcome

- the caller is dispatched to the skill matching the domain and creates the resource via that flow
