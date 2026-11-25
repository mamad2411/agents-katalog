---
name: matilha-den
description: Use when user is wrapping a project or milestone — captures learnings, patterns, and re-usable insights into the project's knowledge base.
category: matilha
version: "1.0.0"
optional_companions: []
---

## When this fires

Project or milestone completion. User wants to distill what was learned, what patterns emerged, what to reuse. Writes `docs/matilha/den/<date>-<topic>.md`.

## Preconditions

- `project-status.md` exists.
- At least one wave completed.

## Execution Workflow

1. Read completed waves from project-status.md via Read tool.
2. Prompt user for topic (e.g., "auth system patterns").
3. Read relevant wave outputs (commits via Bash, spec/plan/review_report via Read) for the topic.
4. Synthesize via Write into `docs/matilha/den/<date>-<topic>.md` with sections: context, patterns observed, decisions + why, would-do-differently.
5. Update project-status.md `recent_decisions` with pointer to the den file.

## Rules: Do

- Cite specific commits + files in findings.
- Include "would-do-differently" section (honest retrospective).
- Timestamp the filename.

## Rules: Don't

- Delete existing den files (keep history).
- Write generic advice (be specific to THIS project).

## Expected Behavior

Knowledge captured in navigable markdown that informs future `/matilha-pack` packaging.

## Quality Gates

- Den file exists at `docs/matilha/den/<date>-<topic>.md`.
- Cited commits are real (verifiable via git log).

## Companion Integration

No companion integrations in Wave 4a.

## Output Artifacts

- `docs/matilha/den/<date>-<topic>.md`.

## Example Constraint Language

- Use "must" for: cite wave(s) being distilled.
- Use "should" for: include would-do-differently.
- Use "may" for: split across multiple files for a large project.

## Troubleshooting

- **"no waves completed"**: Run `/matilha-gather` first.
- **"topic too broad"**: Split into multiple den files per sub-topic.

## CLI shortcut (optional)

> `matilha den <topic>` (future CLI command; not shipped yet).
