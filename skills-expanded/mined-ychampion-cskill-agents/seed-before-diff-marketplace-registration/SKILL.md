---
name: seed-before-diff-marketplace-registration
description: "Register seeded extension sources before diffing materialized state so bootstrap content is treated as present instead of missing."
metadata:
  author: ychampion
---

# SKILL: Seed-Before-Diff Marketplace Registration
**Domain:** extensions-mcp
**Trigger:** Use when bootstrap or pre-seeded extension sources should participate in reconcile logic without being recloned or reported as missing.
**Source Pattern:** Distilled from reviewed seeded-source bootstrap and reconcile flows.

## Core Method
Insert seeded or bootstrap sources into the materialized registry before computing the install diff. That lets the reconciler classify seeded entries as already present instead of missing, which avoids redundant installs and aligns early cache behavior with the real source set. If seed registration changes the materialized registry, propagate that as a real change and clear dependent caches immediately.

## Key Rules
- Register seeds before diffing so bootstrap content is not misclassified as missing.
- Keep seed registration idempotent so repeated startups can re-run it safely.
- Treat seed registration as a real materialized change when it alters registry state.

## Example Application
If a headless runtime starts with a mounted seed directory of official sources, register those seeds first so the reconcile pass skips unnecessary clone work.

## Anti-Patterns (What NOT to do)
- Do not diff before seed registration.
- Do not skip cache invalidation when seed registration changed the materialized state.
- Do not maintain seeded sources outside the normal registry contract.
