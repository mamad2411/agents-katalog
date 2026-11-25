---
name: standards-first
description: "Use when starting an implementation, refactor or review, or when unsure which convention governs a change. Finds and reads the project's written and machine-enforced standards, and reports gaps and contradictions between them."
license: MIT
---

# Standards first

Work that starts from habit instead of the project's written standards gets rewritten in review.
Locate the governing source for each area the task touches before changing or judging code.

## Where standards live

`CLAUDE.md` and `.claude/rules/` above the working directory are usually already in context; ones in
a subdirectory load when you read a file there. `AGENTS.md` loads on its own only when the repo has
no `CLAUDE.md` or `CLAUDE.local.md`, so when both exist, read `AGENTS.md` yourself. A subagent may
start without any of them, so read the repo-root `CLAUDE.md` when it is not in your context. Then
check, stopping when the question is answered:

| Source | Where |
| --- | --- |
| Contribution rules | `CONTRIBUTING.md`, PR templates |
| Decisions already made | `docs/adr/`, `docs/decisions/`, `rfcs/` |
| Domain guides | `docs/`, the `README.md` beside the code you are changing |
| Machine-enforced rules | linter and formatter config, `.editorconfig`, pre-commit config, CI pipeline, branch protection |
| Existing code | the two or three files nearest the change, when nothing is written down |

## Config versus prose

A config file is what actually runs; prose explains intent. Treat the config as authoritative for
*what is enforced* and the prose for *why*.

| Question | Read |
| --- | --- |
| Allowed commit types | the commit-msg hook's configured list |
| Lint rules | the linter config |
| What must pass before merge | the CI definition and branch protection |
| Coverage floor | the coverage tool's configured threshold |

When the two disagree, report the gap instead of silently picking one.

## Steps

1. Name the areas the task touches (testing, security, CI, data model, a specific service).
2. Read the governing source for each, in full rather than by heading.
3. Apply it over your own defaults and patterns from other projects.
4. Where no standard exists, apply general practice and state the gap in your summary: an unwritten
   convention is a decision someone still has to make.
5. Where a standard looks wrong or blocks the task, say so and propose changing it as separate work,
   rather than deviating quietly.
6. Cite the file (and section) each convention came from, so a reviewer can check it.

## Verify

Before acting, list each area from step 1 with the file (and section) that governs it, or "no
standard found". An area with neither is not done; go back to step 2 for it.

Without a checkout, ask for or work from pasted standards and config, and say which areas you could
not check.
