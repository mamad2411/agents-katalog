# Rule: Generating a Project Primer Skill

## Goal

Guide an AI assistant in creating a reusable `.agents/skills/project-primer/SKILL.md` file that helps future agent sessions bootstrap context quickly and consistently.

## Output

- **Format:** Markdown (`.md`)
- **Location:** `.agents/skills/project-primer/` in the parent repository root
- **Filename:** `SKILL.md`

If this prompt pack is stored in a folder such as `.agents/bootstrap/`, treat that as the prompt-pack location only.
Create this skill under the parent project's `.agents/skills/project-primer/` directory, not inside `.agents/bootstrap/` unless the parent project intentionally stores its live skills there.

## Purpose of the Skill

The project-primer skill should help a new agent session:
- understand what the project is
- understand why it exists
- find the planning documents
- find the task roadmap
- determine whether the repo is still in bootstrap or is in implementation mode
- identify the next actionable task

## Recommended Sections

1. Project overview
2. Why the project exists
3. Core product direction
4. Intended architecture or module layout
5. Source layout target
6. Build and tooling expectations
7. Planning documents and what each one means
8. Task tracking structure
9. Early-phase reality check
10. Workflow steps for new sessions
11. Decision logic for choosing the next area of focus
12. Completion criteria for the skill user
13. Handoff checklist for new agents
14. Important constraints
15. Reference files

## Process

1. Read the existing `README.md`, `plans/`, and `tasks/` if they exist.
2. Summarise the project in a way that future agent sessions can use immediately.
3. Keep the skill practical and navigational rather than aspirational.
4. Save the skill in `.agents/skills/project-primer/SKILL.md` in the parent repository root.

## Quality Rules

1. The skill should point agents to the current source-of-truth planning and task documents.
2. The skill should explain the repo maturity level.
3. The skill should help an agent identify the next actionable work without assuming implementation has already started.
4. Keep it general enough that it can be regenerated for other projects.
