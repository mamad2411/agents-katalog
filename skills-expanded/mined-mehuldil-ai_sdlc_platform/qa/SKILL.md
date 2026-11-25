---
name: qa
description: QA atomic skills - delegates to orchestrator/qa/ for test coordination
type: reference
---

# QA Skills

This is a **skill reference**. Orchestration logic lives in `orchestrator/qa/ORCHESTRATOR.md`.

## Atomic Skills

| Skill | Purpose | Single Responsibility |
|-------|---------|----------------------|
| test-plan-creator | Generate test plans from acceptance criteria | Test design |
| test-case-generator | Create test cases (happy, edge, error) | Case generation |
| defect-logger | P0-P3 severity classification, root cause | Bug triage |

## Consolidated QA Agents

6 agents coordinated via orchestrator:
qa-engineer, analysis-agent, test-builder-agent, test-runner-agent, defect-agent, qa-ops-agent

## Orchestration

For full test lifecycle (5 categories, SIT/PP certification, automation):
→ See `orchestrator/qa/ORCHESTRATOR.md`
