---
name: project-knowledge-maintainer
description: Maintain a project-level knowledge base for coding agents using AGENTS.md, knowledge files, bug memory, decisions, and changelog records.
---

# Project Knowledge Maintainer

## Purpose

Use this Skill to initialize, maintain, and evolve a project-level knowledge base for AI coding agents. The knowledge base helps future agent sessions understand project purpose, architecture, interfaces, decisions, bugs, and recent changes without rediscovering everything from scratch.

Keep the workflow tool-neutral. It should be usable by Codex, Claude Code, Cursor, Gemini CLI, and other coding agents that can read project files and follow repository-local instructions.

## When To Use

Use this Skill when the user asks to:

- initialize a project knowledge base
- summarize or document a project
- fix a bug and preserve the repair experience
- add or change a feature
- add or change an API, schema, command, or data format
- record a technical decision or tradeoff
- organize raw project materials into structured knowledge
- review or retrospect a completed development session
- update `AGENTS.md` or files under `knowledge/`

## Inputs

Common inputs include:

- The current repository or target project path.
- Existing project files, source code, docs, issues, logs, or raw materials.
- The user's current task and any implementation changes made during the session.
- Existing `AGENTS.md`, `knowledge/`, `raw/`, or `skills/` content if present.

## Outputs

Expected outputs include:

- `AGENTS.md` project rules.
- `knowledge/overview.md` project overview.
- `knowledge/business.md` business logic and usage scenarios.
- `knowledge/architecture.md` system architecture and data flow.
- `knowledge/api.md` interfaces, schemas, commands, and data structures.
- `knowledge/decisions.md` technical decisions and tradeoffs.
- `knowledge/bugs.md` bug history, root causes, fixes, and prevention rules.
- `knowledge/changelog.md` session-level change records.
- Optional `raw/` and project-local `skills/` folders.
- A short final report listing what was updated and what still needs verification.

## Workflow

1. Read project rules first:
   - `AGENTS.md` if present.
   - `knowledge/overview.md`
   - `knowledge/architecture.md`
   - `knowledge/decisions.md`
   - `knowledge/bugs.md`
2. If initializing a repository, use the templates in `references/templates/` or run the initializer script from this package.
3. Understand the current task and identify what changed:
   - project goal or business logic
   - architecture or module boundaries
   - API, command, data file, schema, or return structure
   - bug symptom, root cause, fix, or prevention rule
   - technical decision or tradeoff
   - user-facing behavior or UI convention
4. Update only the relevant knowledge files.
5. Remove or reconcile duplicate, stale, or contradictory content.
6. Always update `knowledge/changelog.md` after important work.
7. Report the updated files and any missing validation.

For more detailed maintenance guidance, read `references/playbook.md`.

## Updating `knowledge/`

Use the smallest file that matches the change:

- Update `overview.md` for durable project purpose, scope, major modules, and major outputs.
- Update `business.md` for user scenarios, workflows, domain rules, and safety boundaries.
- Update `architecture.md` for module relationships, data flow, runtime modes, and integration boundaries.
- Update `api.md` for endpoints, functions, commands, events, data files, schemas, and return structures.
- Update `decisions.md` for meaningful technical choices and tradeoffs.
- Update `bugs.md` for confirmed bugs and lessons learned.
- Update `changelog.md` for every important task summary.

Do not dump transient reasoning into the knowledge base. Prefer stable facts, validated decisions, and reusable lessons.

## Bug Retrospectives

When a bug is fixed, update `knowledge/bugs.md` with:

- Problem symptom.
- Root cause.
- Fix.
- Affected scope.
- Validation performed.
- Rule to prevent recurrence.

If the root cause is uncertain, mark it as pending verification instead of guessing.

## Interface Changes

When an API, command, function, schema, CSV, event, or file format changes, update `knowledge/api.md` with:

- Interface name.
- Request method or invocation style.
- Path, command, function name, or file path.
- Inputs and parameters.
- Response or output format.
- Notes, constraints, and examples.

Use exact names and field spellings.

## Technical Decisions

When a meaningful technical choice is made, update `knowledge/decisions.md` with:

- Decision background.
- Options considered.
- Final choice.
- Reason for the choice.
- Consequences and follow-up work.

Record decisions that will help future agents avoid reopening settled questions.

## Avoiding Knowledge Rot

- Prefer editing an existing entry over adding a near-duplicate entry.
- Mark outdated content as superseded or replace it with the current fact.
- Keep project facts separate from speculation.
- Use dates for decisions, bugs, and changelog entries.
- Keep wording agent-neutral unless a specific tool integration requires a tool-specific note.
- Do not overwrite user-authored project rules without an explicit request.

## Final Response

Keep the final response concise. Include:

- Files updated.
- Validation performed.
- Any remaining manual checks.
