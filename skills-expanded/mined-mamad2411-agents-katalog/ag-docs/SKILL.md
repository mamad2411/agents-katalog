---
name: ag-docs
description: Analyze codebase and manage project documentation. Use for doc initialization,
  updates, summaries, codebase analysis.
---


# Documentation Management

Analyze codebase and manage project documentation through scouting, analysis, and structured doc generation.

**IMPORTANT:** Invoke "/ag-project-organization" skill to organize the outputs.

## Default (No Arguments)

If invoked without arguments, use `ask_question` to present available documentation operations:

| Operation | Description |
|-----------|-------------|
| `init` | Analyze codebase & create initial docs |
| `update` | Analyze changes & update docs |
| `summarize` | Quick codebase summary |

Present as options via `ask_question` with header "Documentation Operation", question "What would you like to do?".

## Subcommands

| Subcommand | Reference | Purpose |
|------------|-----------|---------|
| `/ag-docs init` | `references/init-workflow.md` | Analyze codebase and create initial documentation |
| `/ag-docs update` | `references/update-workflow.md` | Analyze codebase and update existing documentation |
| `/ag-docs summarize` | `references/summarize-workflow.md` | Quick analysis and update of codebase summary |

When another workflow needs to decide whether docs should change, load
`references/documentation-management.md` before invoking a docs update.

## Routing

Parse `$ARGUMENTS` first word:
- `init` → Load `references/init-workflow.md`
- `update` → Load `references/update-workflow.md`
- `summarize` → Load `references/summarize-workflow.md`
- empty/unclear → ask_question (do not auto-run `init`)

## Shared Context

Documentation lives in `./docs` directory:
```
./docs
├── project-overview-pdr.md
├── code-standards.md
├── codebase-summary.md
├── design-guidelines.md
├── deployment-guide.md
├── system-architecture.md
└── project-roadmap.md
```

Use `docs/` directory as the source of truth for documentation.

When authoring or refreshing diagrams in `system-architecture.md`, apply the universal SVG layout rules from `/ag-tech-graph` at `claude/skills/tech-graph/references/svg-layout-best-practices.md` (component spacing, arrow routing, label placement, z-index ordering). Pair with `/ag-preview --diagram` for visual self-review, or use `/ag-tech-graph` directly for publish-grade output.

**IMPORTANT**: **Do not** start implementing code.
