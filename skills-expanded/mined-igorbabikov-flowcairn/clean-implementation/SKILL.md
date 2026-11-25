---
name: clean-implementation
description: Propose minimal maintainable structured edits for linked requirements within ai-implement scope.
---

# Implement the agreed outcome

- Preserve original goal, work outcome, linked requirements and allowed scope. Reuse the pattern that owns the behavior. Optional cleanup cannot replace required results; a valid no-op needs no artificial diff.
- Return structured edits with real previousHash from current workspace evidence. AI does not write source: Executor checks scope, hashes and application. Missing caller/contract material is a named gap, not permission to invent another subsystem.
- When a touched module mixes responsibilities, identify a concrete boundary and one state owner. Judge refactoring by whether it reduces interface/coupling and makes behavior checkable through the real caller. Splitting by size or adding forwarding wrappers may only move complexity. Avoid a second lifecycle/state store and speculative generic abstractions.
- Preserve invariants, failure semantics and project conventions. Never disable a check or mask a defect with fallback. List affected requirements and necessary fresh verification; the work verdict is not PROVEN for the whole task.

## Narrow TypeScript supplement

Apply only to changed TypeScript types or runtime-data boundaries, not docs, styling or another language. Reuse public types and project compiler settings. External values remain unknown until actual runtime guards/schema validate them; as, any and non-null assertions do not validate data. Keep optional/null behavior explicit. For mutually exclusive lifecycle states, use the existing discriminated union with exhaustive handling rather than independent booleans. Choose the simplest contract-preserving type; generics need a demonstrated input/output relationship. Required typechecks do not replace malformed-input or transition checks.

Adapted from module-friction analysis in mattpocock/skills improve-codebase-architecture and selected wshobson/agents typescript-advanced-types guidance. No report, interview, auto-memory or agent lifecycle imported. Copyright (c) 2026 Matt Pocock; Copyright (c) 2024 Seth Hobson. [Matt Pocock MIT](../licenses/mattpocock-skills-MIT.txt), [wshobson MIT](../licenses/wshobson-agents-MIT.txt); sources/changes: [PROVENANCE](../PROVENANCE.json).
