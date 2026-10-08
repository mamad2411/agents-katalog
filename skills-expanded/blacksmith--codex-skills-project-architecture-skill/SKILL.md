---
name: project-architecture
description: Enforce architectural boundaries, dependency rules, store separation, provider separation, capability safety, and Clean Architecture conventions for the Agent Execution Platform.
---

# Project Architecture

## Purpose
Use this skill for architecture-sensitive implementation, refactoring, module moves, integration, or review.

## Required inputs
Read `AGENTS.md`, `docs/architecture.md`, the active roadmap, relevant ADRs, actual code, and tests.

## Dependency direction
`interfaces -> application/platform application -> domain`
`infrastructure -> application ports/domain`
`bootstrap -> all layers for composition only`

## Layer rules
- Domain: no SQLite, Ollama, protobuf, CLI, infrastructure, or environment access.
- Application: depend on domain and ports, not concrete adapters.
- Infrastructure: implement ports and translate external protocols; do not own policy.
- Interfaces: translate I/O and call application services; no SQL or provider protocol logic.
- Bootstrap: composition only.

## Store invariants
Keep these concerns separate:
- ConversationStore
- AuditStore
- ExecutionStore
- KnowledgeStore

KnowledgeStore is derived and rebuildable.

## Provider invariants
`ModelProvider != EmbeddingProvider`.

## Capability invariants
The planner sees abstract capabilities, never executor/protocol details.
The platform owns capability availability, permissions, budgets, execution order, confirmation, audit, and completion state.

## C toolserver boundary
C toolserver is a privileged local executor only. It does not own planning, authorization, or orchestration. Python validation never replaces independent C-side validation.

## Security
Preserve deny-by-default, workspace confinement, payload/time limits, sanitized errors, sensitive-path restrictions, and explicit human gates.

## Workflow
1. Identify touched modules.
2. Read applicable ADRs.
3. Map dependencies.
4. Place each responsibility in the correct layer.
5. Prefer ports over inward concrete imports.
6. Preserve store/provider/capability separation.
7. Implement the smallest compatible change.
8. Run architecture-focused tests.
9. Report any required ADR.

## Final checks
- no inward infrastructure dependency
- no merged store responsibilities
- no merged provider responsibilities
- no policy bypass
- no ADR contradiction
