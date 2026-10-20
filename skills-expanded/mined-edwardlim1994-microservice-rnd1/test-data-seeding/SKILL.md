# Test Data Seeding

## Purpose
Creates and runs test data seed scripts for the UAT environment based on QA's test data strategy.

## Role
Data Engineer

## Phase
UAT

## Triggered By
Story deployed to UAT, before QA begins testing.

## Inputs
Reads: `openspec/changes/{slug}/test-data/strategy-{KAN-N}.md` (QA's strategy)

## Process
1. Read QA's `test-data-strategy` document.
2. Identify all data states needed for each test case.
3. Write seed scripts (SQL for PG, proto-encoded events for Kafka, etc.).
4. Run seed scripts against UAT environment.
5. Verify data exists correctly (spot-check key records).
6. Document seed state in `seed-{KAN-N}.md`.
7. Signal QA: test data ready, seed document location provided.

### Seeds
- PostgreSQL: test records in relevant tables
- Kafka: test events (if testing event-driven flows)
- Meilisearch: test documents (if testing search)
- ClickHouse: test analytics rows (if testing analytics)

## Outputs
Location: `openspec/changes/{slug}/test-data/seed-{KAN-N}.md` — documents exactly what data exists, IDs, states, so QA knows what to test against.

## Quality Gates
- [ ] All data states from QA strategy are seeded
- [ ] Seed documentation written (QA knows exactly what exists)
- [ ] Data verified in UAT environment
- [ ] QA signalled that seeding is complete

## References
- `.claude/skills/qa-engineer/test-data-strategy/SKILL.md`
- `.claude/skills/qa-engineer/uat-deployment-verification/SKILL.md`
