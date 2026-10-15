---
name: relay-operator
description: Use when an agent needs to operate the Relay CLI end-to-end on a real repository.
---

# Relay Operator

This skill is only the agent adapter layer.

Treat `relay-operator` as the current best-practice path, not as a frozen or exclusive workflow.
If you find a path that is clearer, safer, or more effective than the current one, prefer improving Relay itself and sending a GitHub PR to refine this skill and the CLI guidance.

Before doing Relay work on first use:

```bash
command -v relay >/dev/null 2>&1 || npm install -g @eddiearc/relay || go install github.com/eddiearc/relay/cmd/relay@latest
relay upgrade --check
relay help
```

For concrete operations, use the Relay CLI as the source of truth:

- `relay help`
- `relay help watch`
- `relay help pipeline`
- `relay help issue`
- `relay pipeline list`
- `relay pipeline show <name>`
- `relay pipeline template`
- `relay issue template`
- `relay issue add --pipeline <name> --goal "..." --description "..."`
- `relay watch -issue <id>`
- `relay help upgrade`

Rules:

- do not restate Relay workflows from memory when CLI help already covers them
- inspect the current repository before choosing a pipeline
- use `relay pipeline list` and `relay pipeline show` to inspect candidates
- if one pipeline is clearly the right fit for the current repo and task, select it directly
- if multiple pipelines are plausible or the fit is unclear, present the candidates and ask the user to choose
- if no saved pipeline is clearly suitable, start from `relay pipeline template`, write a repository-specific pipeline, and import it
- when selecting or creating a pipeline, do not silently proceed; first give the user a short directional summary and ask whether it sounds right
- summarize the pipeline at the intent level instead of dumping full prompt text by default; cover:
  - what planning should focus on for this repo and task
  - what coding should focus on, including important repo constraints and reusable project assets
  - how the work should be verified
  - whether reusable E2E or unit-test coverage already exists
  - if the task is a good E2E candidate and reusable E2E coverage is missing, suggest adding a reusable `relay-e2e` scenario or another suitable verification skill
  - if unit tests are missing, call that out more strongly and recommend adding them
- before creating or editing an issue, say plainly where the user's task definition is weak or risky; if the goal, scope, non-goals, or verification path are underspecified, fix that with the user instead of silently guessing
- once the pipeline and issue direction looks good, explain the key directional decisions in terms of the chosen pipeline config and prompt intent, then ask the user to confirm that the direction sounds right before proceeding
- treat project-level verification as harness-critical, not optional
- use the strongest realistic verification path as the default for meaningful behavior changes, but allow narrower verification when the task genuinely does not justify the heavier path; when making that exception, say so explicitly and explain why
- use `relay help pipeline` and `relay help issue` for the concrete verification defaults by project shape
- if the repo lacks the right verification layer, call that out explicitly and recommend the missing script, test suite, or skill
- rewrite the task into a Relay-ready issue before creating it
- if the issue is still too vague, ask the user several focused questions in one turn before creating it; those questions should cover:
  - the target end result
  - scope limits and explicit non-goals
  - how completion should be verified
- use `relay watch` for user-facing monitoring; keep `relay serve` as the executor
- do not duplicate templates or deep operational guidance in this skill
- if CLI help is insufficient, improve the CLI help instead of expanding this file
- if the bundled skill itself should be refreshed, use:
  `npx skills add https://github.com/eddiearc/relay --skill relay-operator -g -y`
