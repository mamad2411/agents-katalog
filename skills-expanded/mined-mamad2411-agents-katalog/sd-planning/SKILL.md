---
name: sd-planning
description: Generate a feature plan through iterative problem breakdown, codebase research, and clarifying questions before handing off to tlc-spec-driven and requirements-table generation. Use when user says 'plan this feature step by step', 'help me plan this properly', 'generate a plan for this problem', or 'walk through planning this feature'.
model: claude-opus-5-5[1m]
---

# Steps

See [diagram](references/diagram.md) for a visual flow overview.

Add the following steps as tasks using the `TaskCreate`, `TaskUpdate`, `TaskGet`, and `TaskList` tools. Update the status as you progress through each step to keep the user informed.

1. Execute the `/tlc-spec-driven` skill to generate a plan/spec based on the described problem.
2. Execute the `/spec-to-requirements-table` skill to generate a `requirements.md` file.
3. **Verifier pass (always-on, author ≠ verifier):** dispatch a fresh sub-agent — no inherited context from steps 1-2 — to run `/sd-review-spec` in report-only mode against the generated `spec.md`, `design.md`, `tasks.md`, `requirements.md`, and any cited ADRs. Give it only: the original feature request (verbatim, as the user stated it), and the feature's spec dir path. It audits every doc claim against the real code and checks the full set covers everything the original request needs — scope, constraints, edge cases, dependencies, and every requirement in `requirements.md` traced to a task. It does not edit anything; it returns the severity-classified gap report (same table as `/sd-review-spec` step 8). If gaps exist: show them to the user and apply fixes per `/sd-review-spec` steps 4-7 before continuing. Do not skip this step and do not ask the user whether to run it — only ask what to do with findings.
4. Once planning is complete, ask the user if they wish to register the feature in _taskmaster_. If the answer is "yes," use the `/sd-insert-taskmaster` skill.
5. Check the definitions in [docs-adr](./references/docs-adr.md) and consider offering to create an ADR when the criteria are met.
6. At the end of the session, evaluate whether there is anything worth saving as permanent memory. Save as permanent memory only what the next session will need and cannot rediscover by reading the code, Git, or CLAUDE.md—such as the _reason_ behind a decision, a non-obvious invariant, or a user preference; if it is already in the repo or only matters for this specific conversation, do not save it. Use the `ai-memory-durable-pages` skill to persist it.
