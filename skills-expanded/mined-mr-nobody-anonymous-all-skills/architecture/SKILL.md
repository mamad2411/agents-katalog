---
name: architecture
description: Design and review software architecture — modules, boundaries, data flow, dependencies, and trade-offs.
category: development
aliases:
- system-design
- design
- architect
- modular
triggers:
- how should I structure this
- design the architecture
- system design
- architect this
- pick a tech stack
- module boundaries
keywords:
- architecture
- design
- module
- boundary
- layer
- dependency
- stack
- trade-off
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- architecture
- boundary
- design
- development
- module
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

# Architecture

## Purpose

Help the user make structural decisions about software: module boundaries, data flow,
dependency choices, and trade-offs. Produce diagrams-in-prose and concrete recommendations.

## When to Use

- Designing a new system or major feature
- Refactoring a system that has outgrown its structure
- Picking a tech stack
- Reviewing an existing design

## When NOT to Use

- A small, well-scoped change (route to `coding`)
- Performance / scaling issues (route to `performance-optimization`)

## Capabilities

- Identify bounded contexts / modules
- Map data flow
- Choose between monolith / modular monolith / services
- Reason about dependency direction
- Pick data storage for the workload
- Document trade-offs explicitly

## Inputs

- The system requirements
- Scale / load expectations
- Team size and skills
- Constraints (existing systems, vendor, regulation)

## Workflow

1. **Requirements.** What must the system do? What are the non-functional requirements?
2. **Bounded contexts.** Identify the major domains. Each becomes a module or service.
3. **Data flow.** How does information move between contexts? Where is the source of truth?
4. **Storage.** Match data shape to store (relational, document, graph, time-series).
5. **Dependencies.** What's third-party vs. first-party? What can fail?
6. **Trade-offs.** Name 2–3 alternatives and pick one with explicit reasoning.
7. **Diagram-in-prose.** Describe the structure so the next person can build it.

## Tools

- Whiteboard / paper
- Diagram tool (draw.io, Mermaid)
- ADRs (Architecture Decision Records)

## Safety

- Don't over-engineer for hypothetical scale
- Don't pick exotic tech for novelty

## Source

Custom skill, written for this library.

## Notes

Pairs with:
- `coding` (implementation)
- `refactoring` (moving toward the target architecture)

## Examples

Requests that should activate this skill include: "how should I structure this"; "design the architecture"; "system design".
