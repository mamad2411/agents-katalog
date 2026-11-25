---
name: dox-agent-framework
version: 1.0.0
author: Hermes Agent
license: MIT
description: DOX AGENTS.md framework — golden standard for project context docs. Initialize, maintain, and audit DOX across all repos.
metadata:
  hermes:
    tags: [dox, agents-md, framework, documentation, project-context, golden-standard]
    triggers: [dox-framework, agents-md, initialize-dox, add-dox, dox-tree, golden-standard, project-documentation, context-files]
    related_skills: [the planning repo-architecture, project-documentation-standards]
---

# DOX Framework — Standard Operating Procedure

DOX (https://github.com/agent0ai/dox) is a hierarchical AGENTS.md framework that turns flat instructions into a connected tree of contracts that AI agents follow.

## Golden Standard

**DOX is mandatory for every project.** Every AGENTS.md must have the DOX framework. Child docs follow the DOX child doc shape. New projects get a DOX-rooted AGENTS.md immediately.

## DOX Framework Block

Copy the following into every root AGENTS.md (at the top, before all existing content):

```
# DOX framework

- DOX is a highly performant AGENTS.md hierarchy installed here
- Agent must follow DOX instructions across any edits

## Core Contract

- AGENTS.md files are binding work contracts for their subtrees
- Work products, source materials, instructions, records, assets, and durable docs must stay understandable from the nearest applicable AGENTS.md plus every parent AGENTS.md above it

## Read Before Editing

1. Read the root AGENTS.md
2. Identify every file or folder you expect to touch
3. Walk from the repository root to each target path
4. Read every AGENTS.md found along each route
5. If a parent AGENTS.md lists a child AGENTS.md whose scope contains the path, read that child and continue from there
6. Use the nearest AGENTS.md as the local contract and parent docs for repo-wide rules
7. If docs conflict, the closer doc controls local work details, but no child doc may weaken DOX

Do not rely on memory. Re-read the applicable DOX chain in the current session before editing.

## Update After Editing

Every meaningful change requires a DOX pass before the task is done.

Update the closest owning AGENTS.md when a change affects:
- purpose, scope, ownership, or responsibilities
- durable structure, contracts, workflows, or operating rules
- required inputs, outputs, permissions, constraints, side effects, or artifacts
- user preferences about behavior, communication, process, organization, or quality
- AGENTS.md creation, deletion, move, rename, or index contents

Update parent docs when parent-level structure, ownership, workflow, or child index changes. Update child docs when parent changes alter local rules. Remove stale or contradictory text immediately.

## Hierarchy

- Root AGENTS.md is the DOX rail: project-wide instructions, global preferences, durable workflow rules, and the top-level Child DOX Index
- Child AGENTS.md files own domain-specific instructions and their own Child DOX Index
- Each parent explains what its direct children cover and what stays owned by the parent

## Child Doc Shape

Default section order: Purpose, Ownership, Local Contracts, Work Guidance, Verification, Child DOX Index

## Style

- Keep docs concise, current, and operational
- Document stable contracts, not diary entries
- Delete stale notes instead of explaining history

## Closeout

1. Re-check changed paths against the DOX chain
2. Update nearest owning docs and any affected parents or children
3. Refresh every affected Child DOX Index
4. Remove stale or contradictory text
5. Run existing verification when relevant

## User Preferences

When the user requests a durable behavior change, record it here or in the relevant child AGENTS.md

## Child DOX Index

| Path | Scope |
|------|-------|
| (populate with actual child index) |
```

## Child Doc Shape Template

For child AGENTS.md files under a subtree:

```
## Purpose

Why this directory exists.

## Ownership

- Key files and directories owned

## Local Contracts

- Binding rules specific to this subtree

## Work Guidance

- How to work in this subtree

## Verification

- How to verify changes work

## Child DOX Index

No child AGENTS.md files in this subtree.
```

## Initializing DOX Tree for a New Project

1. Create root AGENTS.md with DOX framework block (above)
2. Scan the project structure for durable boundaries (subdirectories with their own purpose/rules)
3. For each durable boundary, create a child AGENTS.md following child doc shape
4. Populate the root's Child DOX Index with the full table of paths and scope descriptions
5. Run verification: confirm every AGENTS.md has the DOX framework (roots) or child doc shape (children)

## Adding DOX to Existing AGENTS.md Files

Files with YAML frontmatter (`---`): insert DOX block after the closing `---`, before agent/persona content.
Files without frontmatter: prepend DOX block at the top of the file, then a `---` separator, then existing content.
Children already in DOX shape: leave as-is (they don't need the full DOX framework block — just Purpose/Ownership/Local Contracts/Work Guidance/Verification/Child DOX Index).

## DOX Tree Index Format

```
| Path | Scope |
|------|-------|
| `subsystem-a/` | 🎯 One-line scope description |
| `subsystem-b/` | 🛠️ One-line scope description |
| `subsystem-b/subdir/` | 🔧 Deeper child scope |
```

Sorted by path. One emoji prefix per row for quick scanning.

## Audit Checklist

- [ ] Every root AGENTS.md has DOX framework block
- [ ] Every child AGENTS.md follows DOX child doc shape (Purpose/Ownership/Local Contracts/Work Guidance/Verification/Child DOX Index)
- [ ] Root Child DOX Index lists every child with scope descriptions
- [ ] No stale placeholder text ("This project is not yet indexed")
- [ ] New projects get DOX AGENTS.md immediately on init
