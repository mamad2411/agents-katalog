---
name: bmad-bmm-document-project
description: >-
  Use this skill to generate comprehensive AI-context documentation for an
  existing (brownfield) project so that AI agents can understand and work
  within it effectively. Invoke when the user says "document this project",
  "generate project docs", or wants to create architecture docs, source tree
  analysis, API contracts, data models, and dev guides for an existing codebase.
  The skill scans the project structure, classifies tech stack and architecture
  patterns, generates a suite of documentation files, and creates a master
  index.md — all written immediately to disk to avoid context overload. Supports
  full scans, rescans, and targeted deep-dives into specific subsystems. Input
  is the project root; output is a populated project_knowledge directory. Unlike
  bmad-bmm-generate-project-context (which captures AI implementation rules),
  this skill documents what the project already does. Do not use on a greenfield
  project with no existing code.
argument-hint: "Optionally provide the project root path or specify 'deep-dive' for targeted area documentation."
metadata:
  bmad:
    module: bmm
    type: workflow
---

# Document Project

Document brownfield projects for AI context.

## Outcome

Comprehensive project documentation generated for AI-assisted brownfield development, including architecture, tech stack, source tree, API contracts, data models, and development guides — written to the configured `{project_knowledge}` directory with an `index.md` master entry point.

## Your Role

Project documentation specialist. Communicate all responses in `{communication_language}`.

## Core Rules

- Write each document to disk IMMEDIATELY after generation — do not accumulate content in memory.
- After writing a document, purge detailed findings from context and keep only a 1–2 sentence summary.
- Update the state file (`project-scan-report.json`) after every step completion with step id, summary, timestamp, and outputs.
- When batching file reads (deep/exhaustive scans), process one subfolder at a time: read → extract → write → validate → purge → next.
- Always speak in `{communication_language}`.

## Initialization

Before starting execution, load and resolve configuration:

1. `Invoke skill: bmad-core-config` — loads core config and auto-delegates to `bmad-bmm-config` for module-specific values. Resolve: `project_knowledge`, `user_name`, `communication_language`, `document_output_language`, `user_skill_level`, `date` (system-generated current datetime).
2. Set `installed_path` — the absolute path to this skill's `data/` directory for template and CSV access.

## Execution Order

The workflow has two execution paths selected during routing. Follow steps in order within each path.

### Common Steps (all modes)

1. [Initialize](./steps/initialize.md) — Load config, resolve paths, set runtime variables
2. [Route Workflow](./steps/route-workflow.md) — Detect resume state, determine mode (initial_scan / full_rescan / deep_dive / cancel)

### Full Scan Path (initial_scan / full_rescan)

3. [Load Requirements](./steps/load-requirements.md) — Load documentation-requirements.csv, select scan level
4. [Detect Project](./steps/detect-project.md) — Classify project structure and type
5. [Discover Docs](./steps/discover-docs.md) — Inventory existing documentation
6. [Analyze Tech Stack](./steps/analyze-tech-stack.md) — Extract frameworks, languages, versions, architecture patterns
7. [Scan Project](./steps/scan-project.md) — Conditional analysis: APIs, data models, state, UI, assets (batched)
8. [Generate Source Tree](./steps/generate-source-tree.md) — Annotated directory structure
9. [Extract Dev Info](./steps/extract-dev-info.md) — Prerequisites, setup, build, test, deploy info
10. [Detect Integration](./steps/detect-integration.md) — Multi-part integration architecture (skip if single-part)
11. [Generate Architecture](./steps/generate-architecture.md) — Architecture documents per part
12. [Generate Supporting Docs](./steps/generate-supporting-docs.md) — Overview, components, dev guide, deployment, API, data models
13. [Generate Index](./steps/generate-index.md) — Master index.md with navigation and completeness markers
14. [Validate and Review](./steps/validate-review.md) — Run checklist, detect incomplete docs, offer regeneration loop
15. [Finalize](./steps/finalize.md) — Completion summary, next steps, close state file

### Deep Dive Path (deep_dive)

16. [Deep Dive Select](./steps/deep-dive-select.md) — Identify and confirm target area
17. [Deep Dive Scan](./steps/deep-dive-scan.md) — Exhaustive file-by-file analysis
18. [Deep Dive Analyze](./steps/deep-dive-analyze.md) — Dependency graph, data flow, related patterns
19. [Deep Dive Generate](./steps/deep-dive-generate.md) — Generate deep-dive document, update index
20. [Deep Dive Complete](./steps/deep-dive-complete.md) — Summary, offer another area or finish

## Halt Conditions

- HALT if the project root cannot be determined and the user cannot provide a valid path
- HALT if `{project_knowledge}` output directory cannot be created due to permission errors
- HALT if `./data/documentation-requirements.csv` is unreadable — scan level and document type selection depend on it
- HALT if deep-dive mode is requested but the user cannot specify a target area after repeated prompting

## Data Files

- [./data/documentation-requirements.csv](./data/documentation-requirements.csv) — 24-column CSV: project type detection + documentation requirements
- [./data/checklist.md](./data/checklist.md) — Validation checklist for all workflow modes
- [./data/project-scan-report-schema.json](./data/project-scan-report-schema.json) — JSON schema for the resumable state file
- [./data/templates/deep-dive-template.md](./data/templates/deep-dive-template.md) — Output template for deep-dive documents
- [./data/templates/index-template.md](./data/templates/index-template.md) — Output template for index.md
- [./data/templates/project-overview-template.md](./data/templates/project-overview-template.md) — Output template for project-overview.md
- [./data/templates/source-tree-template.md](./data/templates/source-tree-template.md) — Output template for source-tree-analysis.md

## External Skill Dependencies

- `bmad-core-config` — Configuration loading and resolution

## When to Use

Use this skill when:
- The user says "document this project", "generate project docs", or wants to create comprehensive project documentation for AI-assisted development
- A brownfield project needs documentation generated for AI context (architecture, tech stack, source tree, API contracts, data models)
- The user wants to create or update the `{project_knowledge}` directory with an `index.md` master entry point
- The user specifies "deep-dive" for targeted area documentation of a specific subsystem

## Boundaries

This skill should NOT:
- Be used on a greenfield project with no existing code — it documents what already exists, not what is planned
- Accumulate generated content in memory before writing — each document must be written to disk immediately after generation, then purged from context
- Process an entire codebase in one pass — file reads must be batched one subfolder at a time to avoid context overload
- Modify or refactor any source code — it reads and analyzes code only to produce documentation artifacts
- Generate implementation rules or prescriptive coding guidelines — use `bmad-bmm-generate-project-context` for that; this skill produces descriptive documentation about what the project does

