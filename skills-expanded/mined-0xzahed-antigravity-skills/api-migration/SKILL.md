---
name: api-migration
description: Migrate APIs without breaking consumers. Use when moving between
  API generations or technologies.
metadata:
  tags: api, migration
---

# API Migration

## Use this skill when
- Migrating REST v1→v2 or to GraphQL
- Shifting internal implementations with stable contracts
- Coordinating old/new code coexistence

## Do not use this skill when
- Minor additive feature work
- Non-API backend migration

## Instructions
1. Identify consumers and their traffic before migrating.
2. Keep the old version live until the new one is proven.
3. Add a compatibility layer where warranted.
4. Shadow/dual-run new and old implementations and compare.
5. Redirect consumers gradually; watch errors and latency.
6. Set a sunset date and remove old code only after total cutover.
7. Document what changed and what stayed (diff contract).

## Output Format
- Consumer inventory | migration phases | cutover checklist | rollback plan

## Common Mistakes
- Big-bang cutover without rollback
- Migrating silently under the same version
- Forgetting downstream consumers
