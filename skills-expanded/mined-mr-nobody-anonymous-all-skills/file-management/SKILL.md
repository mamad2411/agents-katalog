---
name: file-management
description: Safely and predictably manage files and directories — read, write, copy, move, rename, organize.
category: utilities
aliases:
- fs
- filesystem
- file-ops
triggers:
- organize my files
- rename these files
- move files
- clean up the folder
keywords:
- file
- folder
- directory
- organize
- rename
- move
- copy
- fs
dependencies: []
risk: medium
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- directory
- file
- folder
- management
- organize
- utilities
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: write
credential_access: false
destructive_operations: false
---

# File Management

## Purpose

Help the user manage files and folders: organize, rename, copy, move, and clean up — with
safety against accidental data loss.

## When to Use

- User wants to organize / rename / move files
- User wants to clean up a messy folder

## Safety

- Always confirm destructive ops (delete, overwrite, bulk rename)
- Prefer dry-run previews
- Never invoke a recursive-force-delete against the root filesystem

## Source

Custom skill, written for this library.

## Notes

Foundation for many other skills. Pairs with `text-processing`.

## When NOT to Use

Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.

## Capabilities

- Apply the file-management workflow consistently.
- Produce a clear, reviewable result.
- Surface assumptions, constraints, and unresolved risks.

## Inputs

- The user's goal and desired output.
- Relevant source material, constraints, and environment details.
- Acceptance criteria when available.

## Workflow

1. Confirm the goal, scope, and constraints.
2. Inspect the available context before acting.
3. Apply the skill-specific guidance in this document.
4. Verify the result and report limitations or next steps.

## Tools

- No mandatory tool unless declared in frontmatter.
- Use only project-approved tools and documented optional dependencies.

## Examples

Requests that should activate this skill include: "organize my files"; "rename these files"; "move files".
