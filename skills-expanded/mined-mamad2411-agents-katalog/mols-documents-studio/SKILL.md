---
name: mols-documents-studio
description: >
  USE WHEN: managing, creating, or modifying workspace design documents, decision records (ADRs), or structured project document templates.
  EXCLUDES: writing general application source code, performing manual file operations outside templates, or modifying agent instructions (AGENTS.md).
---

# mols Documents Studio

## Goal

Create, organize, and manage project-level documentation, templates, and decision records (ADRs) with high structure and consistency.

## When to Use

Use this skill when:

- Creating or editing Architecture Decision Records (ADRs) under the `decisions-lite` format.
- Modifying, generating, or validating project structure markdown documents.
- Resolving documentation workflows using designated templates under `templates/`.

## When NOT to Use

Do not use this skill when:

- Writing, refactoring, or debugging application source code.
- Editing agent configuration files (`AGENTS.md`, `.instructions.md`).
- Performing general non-templated text edits.

## Instructions

### Global Rules

- Follow defined template structures strictly. Fill in all placeholders.
- Always apply the **BLUF (Bottom Line Up Front)** principle for summary-heavy documents.
- Keep documentation updates minimal and focused; do not add redundant details or overcomplicate connections.

### Completion

Report changed documents, validation state, and links to generated files.

## Workflow: Documents Studio Router

### Context

#### Parameters

- **Target Path**: Target directory or document file path.
- **Workflow Route**: Sub-workflow route ID selected from `workflows/INDEX.csv`.

### Procedure

1. Read `workflows/INDEX.csv` once.
2. Match the requested action against the index definitions (trigger/description).
3. If no route matches, state that this skill does not cover the request.
4. Resolve the route ID, load the workflow markdown file from `workflows/<id>.md`, and strictly execute its procedure.
5. Perform validation of the created/edited document before completing.
