---
name: team-memory-routing
description: Use when deciding whether a memory belongs in private or team scope, or when validating that team memory paths and keys stay inside the project team-memory directory
---

# Team Memory Routing

## Overview

This skill covers two linked problems:

- choosing private versus team memory scope
- keeping team-memory writes inside the allowed directory

It is grounded in `src/memdir/memoryTypes.ts`, `src/services/extractMemories/prompts.ts`, and `src/memdir/teamMemPaths.ts`.

## Scope Rules

### Always private

Use private memory for:

- user profile
- personal communication preferences
- user-specific overrides

### Usually team

Use team memory for:

- project-wide conventions
- shared testing policies
- external dashboards or systems every contributor should know
- ongoing project facts that affect multiple people

### Default to private when unsure

If the information sounds like a personal preference rather than a project rule, do not promote it to team scope.

## Routing Heuristic

Ask:

- would every contributor benefit from this?
- is this a stable project convention?
- would saving this publicly leak personal or sensitive data?

If the answer to the last question is yes, keep it private or do not save it at all.

## Sensitive Data Rule

Never store secrets, credentials, or private user data in shared team memory.

## Path Safety Rule

Team memory paths must stay inside the team-memory directory.

Reject:

- traversal via `..`
- encoded traversal
- backslashes as path separators
- absolute paths
- symlink escapes
- dangling symlink tricks

If containment cannot be proven, fail closed.

## Write Discipline

- Update existing team memory when possible.
- Keep index entries concise.
- Prefer semantic topic files over chronological dumps.

## Anti-Patterns

- saving personal style preferences as team rules
- storing secret material in team memory
- accepting server-provided path keys without validation
- trusting symbolic paths instead of resolved containment

## Done Condition

You have applied this skill correctly when shared knowledge is routed to team scope, personal knowledge stays private, and every team-memory write is validated against traversal and symlink escape risks.
