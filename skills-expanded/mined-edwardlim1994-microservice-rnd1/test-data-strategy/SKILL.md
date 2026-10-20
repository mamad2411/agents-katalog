# Test Data Strategy

## Purpose
Defines what test data states are needed and where the data comes from, for inclusion in the PRD.

## Role
QA Engineer

## Phase
Planning (Stage 5 — contributes to PRD)

## Triggered By
PRD drafting begins.

## Inputs
- Story AC and test strategy

## Process
1. Identify required test data states for the story.
2. Cover all relevant data stores: PostgreSQL records, Kafka events, Meilisearch documents, ClickHouse rows.
3. Document source of each data state (seed script, fixture, generated).
4. Commit strategy document.

This document feeds Data Engineer's `test-data-seeding` skill in UAT.

## Outputs
Location: `openspec/changes/{slug}/test-data/strategy-{KAN-N}.md`

## Quality Gates
- [ ] All relevant data stores covered
- [ ] Data source specified per state
- [ ] Document ready to feed Data Engineer test-data-seeding

## References
- `.claude/skills/pm/prd-writing/SKILL.md`
- Data Engineer `test-data-seeding`
