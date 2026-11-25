# E2E Test Case Design

## Purpose
Designs full-stack end-to-end test cases covering critical paths from browser through to persistence and async propagation.

## Role
QA Engineer

## Phase
Planning (Stage 6)

## Triggered By
Stage 6 begins.

## Inputs
- Story AC
- Architect's sequence diagram

## Process
1. Identify critical paths only (not exhaustive coverage).
2. Design tests spanning the full stack: browser click → Apollo → subgraph → gRPC → PostgreSQL, and for async flows: → Kafka → Debezium → downstream service.
3. Use real services and real data flow — not mock data.
4. Implement using Playwright.

## Outputs
Location: `test/e2e/`

Runs: on merge to `main` (not every PR). Weekly: full suite.

## Quality Gates
- [ ] Only critical paths covered (not exhaustive)
- [ ] Real services and real data flow used
- [ ] Async flows (Kafka/Debezium) covered where applicable
- [ ] Tests run on merge to main

## References
- `.claude/skills/qa-engineer/integration-test-case-design/SKILL.md`
- `.claude/skills/solution-architect/story-diagram-design/SKILL.md`
