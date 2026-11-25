---
name: automation
description: Automate repetitive workflows — scripts, scheduled jobs, glue code, and "do this every time" tasks.
category: utilities
aliases:
- script
- workflow-automation
- glue
triggers:
- automate this
- run this every day
- write a script for
- glue this together
keywords:
- automation
- script
- schedule
- cron
- glue
- workflow
dependencies: []
risk: medium
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- automation
- cron
- schedule
- script
- utilities
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Automation

## Purpose

Help the user automate repetitive tasks. Identify the trigger, write the script, and wire up
scheduling where appropriate.

## Safety

- Confirm before running anything that modifies external systems
- Idempotent scripts preferred
- Don't automate destructive ops without a guard

## Source

Custom skill, written for this library.

## When to Use

Use when the request matches the documented automation capability or its declared triggers.

## When NOT to Use

Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.

## Capabilities

- Apply the automation workflow consistently.
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

Requests that should activate this skill include: "automate this"; "run this every day"; "write a script for".

## Notes

This section was normalized to satisfy the library contract; retain more specific guidance elsewhere in this file.
