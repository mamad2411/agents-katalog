---
name: speckit.migrate
description: Legacy Code Migrator - Reverse-engineer existing systems into safe SDD migration artifacts.
---

## Mission
Document current behavior, risks, and a reversible migration path before changing legacy code.

## Inputs and Outputs
- Read source, configs, schemas, runtime/deployment files, tests, maps, and constitution.
- Write `.agents/specs/migration/spec.md`, `migration-risk.md`, and a staged migration plan with evidence and rollback notes.

## Protocol
1. Inventory stack, entrypoints, routes, data models, integrations, deployment, ownership, and test coverage; record tool/version confidence.
2. Reverse-engineer observable behavior into scenarios and entities. Label inferred behavior and preserve unknowns for clarification.
3. Classify risks by impact and likelihood: security/data loss/availability/contract breakage, then operational and editorial debt. Cite file:line evidence.
4. Design strangler or in-place stages with seams, backfill/dual-read/dual-write rules, feature flags, rollback triggers, and exit criteria.
5. Convert each stage into atomic tasks linked to risks and acceptance checks. Re-scan after each stage; never delete legacy paths without verified replacement.

## Completion Gate
Current behavior, risks, dependencies, migration stages, rollback, and verification evidence are documented; no implementation is performed in this skill.

## Guard Rails
Read-only analysis. Do not delete data/code, silently change behavior, or mark inferred behavior as fact.