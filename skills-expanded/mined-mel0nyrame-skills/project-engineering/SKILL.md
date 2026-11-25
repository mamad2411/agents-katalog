---
name: project-engineering
description: Use when investigating or implementing project changes, or maintaining engineering knowledge.
---

# Project Engineering

Implement the authorized change using the project's rules, existing capabilities, and verified change entry points.

## 1. Establish the change context

Read instructions applying to the target paths and follow their documentation entry points. For work across subtrees, establish each subtree's rules. Inspect relevant implementation, callers, and focused validation. A local change needs enough context to identify its target module, editing entry point, reusable code, and check; expand investigation when architecture, generation, infrastructure, or data boundaries are affected.

Before choosing an approach, search active decisions by the affected topic, paths, constraints, symbols, and configuration. Read matching choices, proposals, rejection reasons, and open questions. Refresh discovery when new scope or evidence could reveal another relevant record. State changed conditions before reopening an earlier choice; consult archives when historical evidence is needed.

During design, use `project-adr` to preserve meaningful constraints, evaluated alternatives, and substantial proposals with future value, including when implementation is deferred. Existing proposals provide context; execution still follows the current authorization.

## 2. Verify the editing boundary

Distinguish explicit project rules from observed implementation patterns and unresolved claims. Cite the authority for a rule; use patterns as investigation leads. Verify a claim's scope before treating an asset as mandatory or a store as authoritative. Resolve material unknowns from project evidence; ask the user when an unresolved unknown changes correctness or scope.

Follow architecture boundaries, dependency direction, and shared entry points. Extend suitable existing capabilities through their supported extension points. Add parallel infrastructure only when the existing capability does not own the responsibility or cannot meet a verified requirement. Leave mechanical style to project tooling.

Distinguish the runtime source of truth from the manual editing entry point: a database may own runtime facts while schemas and migrations own schema changes.

Read the matching branch before implementation:

| Change | Reference |
| --- | --- |
| Generated or derived artifacts | [Generated artifacts](references/CHANGE-BOUNDARIES.md#generated-artifacts) |
| Persistent schema, ownership, flow, isolation, lifecycle, deletion, or rebuilds, including agent stores | [Persistent data](references/CHANGE-BOUNDARIES.md#persistent-data) |

## 3. Implement and preserve useful knowledge

Make the smallest change within the verified boundaries. When documentation and implementation disagree, compare rules, decisions, configuration, tests, and generation sources. Correct a rule violation, update stale facts, or describe the unresolved or transitional state with evidence. Git history can explain a change; current sources establish current behavior.

Persist findings future maintainers need and cannot readily recover from code, configuration, or tests: boundaries, reuse conditions, editing entry points, data lifecycle, and non-obvious validation limits. Update an existing owner and reuse accurate records. Each finding needs scope, conclusion, evidence, confidence, and applicable conditions. Make it discoverable through a project entry point or a conditional local link.

When creating or extending instructions, engineering documents, capability entries, indexes, or gates, read [knowledge governance](references/PROJECT-GOVERNANCE.md). It supplies ownership rules and fallback locations. Create files only for actual content. For read-only tasks, report findings and proposed destinations without writing them.

## 4. Validate and deliver

Run focused project checks and inspect the results, including affected generated outputs, data migrations, and recovery or rollback effects. Synchronize affected decision facts and replacement relationships with `project-adr` in the same change. Keep selected but unfinished work distinct from implemented behavior.

Complete when the authorized behavior is verified, required knowledge is saved and discoverable, affected decisions are synchronized, and required checks pass. Report the change, checks actually run, knowledge locations, and unresolved limits; explain when no knowledge or decision update is needed.

Use `project-prose` for technical prose and `project-git` for requested Git or PR/MR delivery. If a companion is unavailable, follow project rules for its required checks and report any remaining delivery dependency.
