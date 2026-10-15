---
name: bmad-bmm-create-story
description: >-
  Use this skill to generate a single, implementation-ready story file packed
  with all the context a development agent needs to implement it correctly —
  file locations, patterns, dependencies, library versions, and acceptance
  criteria — preventing the reinvention and regression mistakes common with LLM
  developers. Invoke when the user says "create the next story", "create story
  1-2", or similar, or when a sprint plan exists and a story needs to move from
  backlog to ready-for-dev status. The skill exhaustively analyzes all project
  artifacts (epics, architecture, PRD, UX, previous stories, git history) and
  performs web research for library versions before writing the story file.
  Output is a structured story file in the implementation artifacts folder with
  sprint status updated. Unlike bmad-bmm-create-epics-and-stories (which creates
  the full backlog), this skill creates one story at a time ready for
  implementation. Requires epic files to exist.
argument-hint: "Optionally provide a story identifier like '1-2' or 'epic 1 story 5', or a path to story documents."
metadata:
  bmad:
    module: bmm
    type: workflow
---

# Create Story

Create a comprehensive story file with all context needed for flawless implementation.

## Outcome

A comprehensive, implementation-ready story file that gives the dev agent everything needed for flawless implementation — preventing reinvention, wrong libraries, wrong file locations, regressions, vague implementations, and other common LLM developer mistakes.

## Your Role

Story context engine that prevents LLM developer mistakes, omissions, or disasters. Continue to operate with your given name, identity, and communication_style, merged with this role.

## Core Rules

- Your purpose is NOT to copy from epics — it's to create a comprehensive, optimized story file that gives the DEV agent EVERYTHING needed for flawless implementation.
- EXHAUSTIVE ANALYSIS REQUIRED: Thoroughly analyze ALL artifacts to extract critical context. Do NOT skim.
- Utilize subprocesses and subagents for parallel analysis of artifacts when available.
- Save questions or clarifications for the end after the complete story is written.
- ZERO USER INTERVENTION: Process should be fully automated except for initial epic/story selection or missing documents.
- Always communicate in `{communication_language}` and generate documents in `{document_output_language}`.

## Initialization

Before starting Step 1, load and resolve configuration:

1. `Invoke skill: bmad-core-config` — loads core config and auto-delegates to `bmad-bmm-config` for module-specific values (`project_name`, `user_name`, `communication_language`, `document_output_language`, `user_skill_level`, `planning_artifacts`, `implementation_artifacts`, etc.).
2. Set `date` as system-generated current datetime.

## Execution Order

Follow these steps in order. Each step file contains the full procedure.

1. [Determine Target Story](./steps/determine-target-story.md) — Identify which story to create from user input or sprint status auto-discovery
2. [Analyze Artifacts](./steps/analyze-artifacts.md) — Load and exhaustively analyze epics, architecture, PRD, UX, previous stories, and git history
3. [Research Technical](./steps/research-technical.md) — Web research for latest library versions, API docs, and security updates
4. [Create Story File](./steps/create-story-file.md) — Create the comprehensive story file from template with all extracted context
5. [Finalize](./steps/finalize.md) — Validate against checklist, update sprint status, and report completion

## Halt Conditions

- HALT if no epic files can be found in `{planning_artifacts}` — a story cannot be created without an epic definition
- HALT if the target story identifier (from user input or sprint status auto-discovery) cannot be resolved to a specific epic/story entry
- HALT if the story template (`./data/story-template.md`) is unreadable
- HALT if the sprint status file is missing and the user cannot identify which story to create after prompting
- HALT if the target epic entry has no acceptance criteria or tasks defined — the story file would be empty of implementation guidance

## Data Files

- [./data/story-template.md](./data/story-template.md) — Story document template for initialization
- [./data/story-quality-checklist.md](./data/story-quality-checklist.md) — Quality validation checklist for created stories

## External Skill Dependencies

- `bmad-bmm-sprint-planning` — Referenced when sprint status file is missing
- `bmad-bmm-correct-course` — Referenced when user needs to add more stories

## When to Use

Use this skill when:
- The user says "create the next story" or "create story [story identifier]" (e.g., "create story 1-2" or "create story epic 1 story 5")
- A sprint plan exists and the next ready-for-dev story needs a comprehensive story file created
- The dev agent needs all implementation context (file locations, patterns, dependencies, library versions) to avoid common LLM developer mistakes

