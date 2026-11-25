---
name: init-adrs
description: Scaffold the adrs/ and architecture/ directory structure in the current project. Use when setting up ADRs for the first time.
disable-model-invocation: true
allowed-tools: Skill
---

# Initialize ADRs

Scaffolds the `adrs/` and `architecture/` directory structure in a project that hasn't used ADRs before.

## Workflow

### 1. Check for Existing Structure

Look for an `adrs/` directory at the repository root.

- **If it does not exist:** proceed to step 2.
- **If it exists and matches the expected structure** (`1-pending/`, `2-implemented/`, and `README.md` all present): report that the ADR directory is already initialized and stop.
- **If it exists but does not match:** describe the current structure to the user and ask whether they want to migrate existing content to the expected format or leave it as-is. If they choose to migrate, rename/move directories to match the expected structure. If they choose to leave it, stop.

Also check for an `architecture/` directory at the repository root.

- **If it does not exist:** proceed to scaffold it in step 2.
- **If it exists and contains a `README.md`:** report that the architecture directory is already initialized.
- **If it exists but has no `README.md`:** proceed to scaffold the README in step 2.

### 2. Scaffold

Create the following files:

- `adrs/README.md` (content from the README Content section below)
- `adrs/1-pending/.gitkeep`
- `adrs/2-implemented/.gitkeep`
- `architecture/README.md` -- invoke the `/writing-architecture-readme` skill for the template and guidance, then adapt it to fit the project

### 3. Confirm

Report the files that were created across both directories. Suggest the user run `/draft-adr` to create their first ADR. If the `architecture/` directory was created, also suggest the user run `/init-architecture` to populate it with comprehensive documentation of their project's existing architecture.

## README Content

Write the following content to `adrs/README.md` (adapt to the project if needed, though this should rarely be necessary):

~~~~~markdown
# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs). These documents capture significant technical decisions along with their context and consequences.

## Folder Structure

```
adrs/
  1-pending/        ADRs pending implementation
  2-implemented/    ADRs that have been implemented
```

Each ADR lives in its own subdirectory named `YYYY-MM-DD-short-name/`. The main document is always `ADR.md`. Supporting materials (diagrams, data, references) go alongside it in the same directory.

## Lifecycle

1. Create a new ADR with `/draft-adr` and place it in `1-pending/`
2. The user opens a pull request (or explicitly asks an agent to). Agents should never create PRs autonomously. The PR is the review forum: the team comments, asks questions, and requests changes there
3. When the PR merges, the ADR is approved
4. The subsequent PR that implements the decision moves the ADR from `1-pending/` to `2-implemented/`

## Creating a New ADR

Run `/draft-adr [short-name] [description]` to start.
~~~~~