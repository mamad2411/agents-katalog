---
name: databases
description: Work with databases — schema design, queries, indexing, migrations, and selecting the right store.
category: development
aliases:
- sql
- nosql
- schema
- migrations
triggers:
- design a database schema
- write a migration
- optimize this query
- pick a database
keywords:
- database
- sql
- postgres
- mysql
- mongodb
- schema
- migration
- index
- query
dependencies: []
risk: medium
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- database
- databases
- development
- mysql
- postgres
- sql
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

# Databases

## Purpose

Help the user with databases: design schemas, write queries, plan migrations, optimize
performance, and choose the right store for the workload.

## When to Use

- User is designing a schema
- User is writing or optimizing queries
- User needs to migrate data
- User is picking between SQL / NoSQL / graph

## Safety

- Always backup before destructive migrations
- Test migrations on a copy first
- Don't dump credentials into query logs

## Source

Custom skill, written for this library.

## Notes

Pairs with `backend`, `architecture`, `data-analysis`.

## When NOT to Use

Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.

## Capabilities

- Apply the databases workflow consistently.
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

Requests that should activate this skill include: "design a database schema"; "write a migration"; "optimize this query".
