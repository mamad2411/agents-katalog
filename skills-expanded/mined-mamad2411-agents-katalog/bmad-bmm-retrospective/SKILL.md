---
name: bmad-bmm-retrospective
description: >-
  Use this skill to facilitate a structured post-epic retrospective that
  extracts lessons learned, assesses success, creates action items, and
  prepares the team for the next epic. Invoke when the user says "run a
  retrospective" or "let's retro the epic [number]", or when an epic has been
  completed and the team needs a formal review before starting the next one.
  The skill loads all story files from the completed epic, analyzes dev notes
  and review feedback, loads the previous retrospective for continuity, previews
  the next epic, then facilitates a two-part interactive retrospective covering
  what went well, what did not, and next epic preparation — using all installed
  BMAD agents in character for realistic team dynamics. Output is a retrospective
  document with SMART action items and updated sprint status. Unlike a simple
  summary request, this skill runs a full facilitated multi-agent session.
  Requires a completed epic and associated story files to proceed.
argument-hint: "Optionally provide the epic number to review."
metadata:
  bmad:
    module: bmm
    type: workflow
---

# Retrospective

Post-epic review to extract lessons and assess success.

## Outcome

A comprehensive retrospective document covering epic review, lessons learned, action items with owners, next epic preparation tasks, and updated sprint status — saved to `{implementation_artifacts}/epic-{epic_number}-retro-{date}.md`.

## Your Role

Scrum Master facilitating retrospective. Continue to operate with your given name, identity, and communication_style, merged with this role.

## Core Rules

- No time estimates — NEVER mention hours, days, weeks, months, or ANY time-based predictions. AI has fundamentally changed development speed.
- Always communicate in `{communication_language}`, tailored to `{user_skill_level}`.
- Generate all documents in `{document_output_language}`.
- User skill level affects conversation style ONLY, not retrospective content.
- Psychological safety is paramount — NO BLAME.
- Focus on systems, processes, and learning — not individuals.
- Everyone contributes; specific examples preferred.
- Action items must be achievable with clear ownership.
- Two-part format: (1) Epic Review + (2) Next Epic Preparation.

## Party Mode Protocol

- ALL agent dialogue MUST use format: `Name (Role): dialogue`
- Example: `Bob (Scrum Master): "Let's begin..."`
- Example: `{user_name} (Project Lead): [User responds]`
- Create natural back-and-forth with user actively participating.
- Show disagreements, diverse perspectives, authentic team dynamics.

## Initialization

Before starting Step 1, load and resolve configuration:

1. `Invoke skill: bmad-core-config` — loads core config and auto-delegates to `bmad-bmm-config` for module-specific values (`project_name`, `user_name`, `communication_language`, `document_output_language`, `user_skill_level`, `planning_artifacts`, `implementation_artifacts`, etc.).
2. Set `date` as system-generated current datetime.
3. Set `sprint_status` = `{implementation_artifacts}/sprint-status.yaml`.
4. Set `epic_number` from user argument if provided (auto-discovered if empty).

### Input Files

| Input | Description | Path Pattern(s) | Load Strategy |
|-------|-------------|------------------|---------------|
| epics | The completed epic for retrospective | whole: `{planning_artifacts}/*epic*.md`, sharded_index: `{planning_artifacts}/*epic*/index.md`, sharded_single: `{planning_artifacts}/*epic*/epic-{epic_num}.md` | SELECTIVE_LOAD |
| previous_retrospective | Previous epic's retrospective (optional) | `{implementation_artifacts}/**/epic-{prev_epic_num}-retro-*.md` | SELECTIVE_LOAD |
| architecture | System architecture for context | whole: `{planning_artifacts}/*architecture*.md`, sharded: `{planning_artifacts}/*architecture*/*.md` | FULL_LOAD |
| prd | Product requirements for context | whole: `{planning_artifacts}/*prd*.md`, sharded: `{planning_artifacts}/*prd*/*.md` | FULL_LOAD |
| document_project | Brownfield project documentation (optional) | sharded: `{planning_artifacts}/*.md` | INDEX_GUIDED |

## Execution Order

Follow these steps in order. Each step file contains the full procedure.

1. [Discover Epic](./steps/discover-epic.md) — Find the completed epic via sprint status, user input, or fallback; verify completion; load project documents
2. [Analyze Stories](./steps/analyze-stories.md) — Deep-read all story files to extract dev notes, review feedback, lessons, debt, and cross-story patterns
3. [Load Previous Retro](./steps/load-previous-retro.md) — Find and analyze previous epic's retrospective for continuity and follow-through tracking
4. [Preview Next Epic](./steps/preview-next-epic.md) — Load next epic definition, identify dependencies, gaps, and preparation needs
5. [Initialize Retro](./steps/initialize-retro.md) — Load agent roster, present epic summary with metrics, set ground rules, open the session
6. [Epic Review Discussion](./steps/epic-review-discussion.md) — Facilitate what went well / what didn't, surface patterns from story analysis, resolve conflicts, review previous retro follow-through
7. [Next Epic Discussion](./steps/next-epic-discussion.md) — Explore readiness for next epic, surface technical and knowledge concerns, negotiate preparation strategy
8. [Synthesize Actions](./steps/synthesize-actions.md) — Create SMART action items, preparation tasks, critical path items; detect significant changes requiring epic updates
9. [Readiness Exploration](./steps/readiness-exploration.md) — Interactive deep dive on testing, deployment, stakeholder acceptance, technical health, and unresolved blockers
10. [Closure](./steps/closure.md) — Summarize takeaways, acknowledge team, capture final reflections
11. [Save Document](./steps/save-document.md) — Write retrospective document and update sprint status
12. [Final Summary](./steps/final-summary.md) — Present completion summary, commitments, and next steps

## Halt Conditions

- HALT if no epic files can be found in `{planning_artifacts}` and the user cannot identify which epic to retrospect
- HALT if the identified epic has no associated story files in `{implementation_artifacts}` — there are no stories to analyze for lessons learned
- HALT if `{implementation_artifacts}/sprint-status.yaml` is missing and the user cannot confirm the epic is complete
- HALT if the agent roster cannot be loaded via `bmad-agents` — the multi-agent retrospective format requires at least one agent persona

## External Skill Dependencies

- `bmad-bmm-sprint-planning` — Referenced when incomplete epic needs story tracking refresh
- `bmad-bmm-create-story` — Referenced as next step after retrospective for new epic

## When to Use

Use this skill when:
- The user says "run a retrospective" or "lets retro the epic [epic]"
- An epic has been completed and the team needs a post-epic review to extract lessons and assess success
- The user wants to generate a retrospective document covering lessons learned, action items, and next epic preparation

## Boundaries

This skill should NOT:
- Mention time estimates of any kind — NEVER mention hours, days, weeks, months, or ANY time-based predictions
- Assign blame or focus on individuals — psychological safety is paramount; retrospective discussion must focus on systems, processes, and learning, not people
- Skip the two-part format: the session must cover both (1) Epic Review and (2) Next Epic Preparation — neither part is optional
- Be run on an epic that has no associated story files — there must be story data (dev notes, review feedback) to analyze for lessons learned
- Directly edit or update planning artifacts (PRD, architecture, epics) — if significant discoveries are flagged, the skill alerts the user and stops; actual artifact changes must be handled by `bmad-bmm-correct-course` or the relevant editing skill

