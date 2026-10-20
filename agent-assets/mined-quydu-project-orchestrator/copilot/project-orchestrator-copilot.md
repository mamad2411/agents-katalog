# Repository Instructions

## Engagement protocol (mandatory, highest precedence)

Apply this to every new user prompt, without exception, before any analysis, tool use, file change, or answer.

1. Run `clarify-the-ask`.
2. Ask one question round only: ask three questions for an ordinary request, and up to five only when the request is complex, confusing, high-impact, or potentially damaging to the current project.
3. Wait for the user's answers. Do not begin work while a question is unanswered.
4. After the answers arrive, do not ask any more clarification questions for this prompt. State the objective, concrete steps, files or systems touched, and risks, then continue.

- This runs once for every new prompt, including follow-ups later in the same session. Answers close clarification for that prompt; the next prompt starts a new round.
- Ground the three questions in repository evidence; ask about intent, scope, constraints, and acceptance criteria rather than facts the repository already answers.
- Never treat your own plan description as approval.
- Do not ask filler questions. Three is the normal round size; use four or five only when additional decisions are genuinely material. Unresolved material ambiguity still blocks.
- The only exception is an explicit instruction in the current prompt to skip clarification,
  including the exact `--proceed` or `--Proceed` token. Treat the token case-insensitively.

## Orchestration

Use `.github/skills/project-skills-orchestrator/SKILL.md` for project orchestration. Audit existing project state, inventory available skills, plan before execution, preserve repository-owned skills, and stop at approval gates.

- Inspect `reports/current-work-state.json` and `reports/project-handoff.json` when present.
- Treat machine-readable artifacts in `reports/` as authoritative.
- Never rewrite accepted records in `reports/execution-log.jsonl`.

## Launch Pad boundary

This repository is the Project Orchestrator launch pad and source framework. Do not create application code, generated project files, demo implementation files, deployment outputs, or target-project artifacts inside this repository. After a target project is created or adopted, all project-specific implementation, validation, documentation, and deployment work must occur inside that target project. Modify this repository only when the requested work explicitly updates Project Orchestrator itself: runtime, skills, templates, schemas, prompts, docs, tests, reports, release assets, or orchestration behavior.

## Azure environment automation

- Read `.azure/environment.json` before Awith a client ID.

## Repository standards

- For every request, automatically use an existing skill when its trigger and ownership match the work; continue with normal engineering work only when no available skill fits. Prefer reuse over duplicating an existing skill, script, workflow, report, or capability.
- Before creating a new skill, invoke `/skill-create`. It must inventory and compare current skills for reuse or duplication. If no existing skill fits, notify the user and obtain explicit approval before authoring the new skill.
- Before changing an existing skill, invoke `/skill-update`. Resolve an inexact name by offering ranked candidate skill IDs, identify one exact target, present every proposed file and behavior change, and wait for `-Proceed` or `--proceed` before editing.
- The skill catalog, `config/profiles.yaml`, `schemas/`, and `templates/project/` are contract surfaces. Changing any of them requires updating `tests/skill-contracts.test.mjs`.
- Every skill contract carries all twelve required sections and a distinct trigger description.
- Skill dependencies must stay acyclic and every conformance profile must remain dependency-closed.
- Templates under `templates/project/` are shipped to generated and adopted projects. Keep them free of secrets, tenant identifiers, and unpinned GitHub Actions.
- Run `npm run check` before declaring implementation work complete.

## Approval gates

Require explicit approval before destructive changes, external publication, deployment, remote mutation, commits, and pushes.
