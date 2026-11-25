---
name: speckit.map
description: Codebase Mapper - Build a bounded, evidence-backed architecture and dependency map for existing projects.
---

## Mission
Create a navigable map of structure, ownership, dependencies, conventions, integrations, and runtime boundaries without loading the whole repository into context.

## Inputs and Outputs
- Read project config, manifests, entrypoints, exports, Docker files, and representative source slices.
- Write `.agents/codebase/ARCHITECTURE.md`, `STRUCTURE.md`, `INTEGRATIONS.md`, and `CONVENTIONS.md` with scan scope and timestamp.

## Protocol
1. Identify repository type, languages, frameworks, package managers, services, build/test commands, and generated/vendor paths.
2. Enumerate directories and entrypoints; sample headers/exports before reading implementation details. Use CodeGraph when `.codegraph/` exists; otherwise use `rg`.
3. Trace imports, routes, jobs, data stores, external services, configuration, and critical request/event paths. Distinguish confirmed links from inferred ones.
4. Record ownership boundaries, shared utilities, duplication, cycles, risk hotspots, and unknowns with file:line evidence.
5. Update maps after major refactors and compare the previous map to surface structural drift.

## Completion Gate
Every output states scope, date, evidence, unknowns, and confidence; major runtime and integration boundaries are traceable to source locations.

## Guard Rails
Read-only. Do not scan secrets into reports, read every file indiscriminately, or invent dependencies from naming alone.