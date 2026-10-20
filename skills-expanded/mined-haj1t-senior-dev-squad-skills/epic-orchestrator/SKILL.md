---
name: epic-orchestrator
description: "Multi-squad orchestration: task decomposition, resource optimization, routing, error recovery, cross-squad dependencies. Use when planning or managing large epics."
version: 2.0.0
platforms: [linux, macos]
---

# Epic Orchestrator v2

## Overview

Epic Orchestrator is the orchestration skill for large-scale projects that run for days or weeks, require 5-50+ sub-agents, and involve the coordinated effort of multiple independent squads. **Benchmark-proven: without structured decomposition rules, models produce vague timelines with no dependency DAGs, token budgets, or failure recovery strategies.**

**Core Principle:** FOR SMALL TASKS, USE SUBAGENT-ORCHESTRATOR; FOR LARGE TASKS, USE EPIC ORCHESTRATOR.

## The Iron Law

Seven rules that are never violated:

1. **Never begin without epic decomposition** — Do not spawn the first sub-agent before breaking the project down into epics, epics into stories, and stories into atomic tasks.
2. **Give each squad only the context it requires** — Each squad receives memory and context restricted to its assigned epic.
3. **Each squad must be able to work independently** — If two squads block each other's output for more than 1 hour, the decomposition was designed incorrectly.
4. **Failure is a data point, not an endpoint** — Every error is routed through automatic retry, circuit breaker, and fallback patterns.
5. **Every epic produces a learning artifact** — Conduct a post-mortem, update the pattern catalog, and define new skills as necessary.
6. **Token budgets are hard contracts** — Enforce a maximum token limit for each squad: issue a warning at 80%, and halt execution at 95%. Budget overruns indicate decomposition failures.
7. **Monitoring is always active** — Maintain a 15-minute check interval; 3 consecutive silent periods triggers a stall alarm and activates the automatic circuit breaker.

## When to Use

**USE WHEN:**
- The project can be divided into 5+ independent workflows (each with at least 3-4 sub-tasks).
- Total estimated token usage is 1M+ (exceeds single-agent context limits).
- The work requires distinct areas of expertise (e.g., frontend squad + backend squad + DevOps squad + security squad).
- Time is critical and parallel execution is required (e.g., executing 3 days of work in 1 day).
- The project runs for multiple days and requires precise milestone/checkpoint tracking.
- Similar projects were completed successfully, providing valid post-mortem patterns.

**DO NOT USE (use `subagent-orchestrator` instead):**
- The work can be divided into 3-5 sub-tasks and a single area of expertise is sufficient.
- Estimated token usage is under 200K.
- All tasks are strictly linear (parallelism is impossible).
- The work completes in 1-2 hours.
- A single squad is sufficient.

**NEVER USE (delegate to human instead):**
- The project scope is completely undefined (run `grill` first).
- Critical business decisions are still outstanding (run `opportunity-solver` + `validation-designer` first).
- Domain knowledge is entirely absent (run `research-first` to discover domain context first).

## Orchestration Workflow

Every run follows a strict 10-phase sequence. The full per-phase protocol — with YAML schemas and worked examples for each phase — is in [REFERENCE.md](REFERENCE.md).

| Phase | Name | Key output |
|-------|------|-----------|
| 0 | Project Ingestion & Scoping | Validated brief, success criteria, constraints — **no agents spawned** |
| 1 | Epic Decomposition | Epic/story/task hierarchy, dependency DAG, critical path |
| 2 | Squad Design | Role assignments, handoff contracts, token budgets |
| 3 | Resource Planning | Timeline, bottleneck analysis, parallelism map |
| 4 | Squad Spawn & Monitoring Init | Live squads, alert rules, human checkpoints |
| 5 | Mid-Flight Steering | Task injection, rebalancing, scope cuts |
| 6 | Error Recovery & Resilience | 3-tier retry → fallback → escalate per failure type |
| 7 | Result Consolidation & Verification | Integration tests, consistency checks, quality gates |
| 8 | Post-Mortem & Learning | Planned-vs-actual, extracted patterns, skill updates |
| 9 | Closing & Archiving | Packaged deliverables, benchmarks, final summary |

Every plan must be expressed in the mandatory YAML schema and must pass the bad/good output contrast check. See [REFERENCE.md](REFERENCE.md) for the full schema, a concrete bad/good example pair, and model-specific calibration notes.

## Red Flags — STOP and Follow Process

Stop immediately and rerun decomposition if any of these appear mid-flight:

- A squad cannot make progress without output from a squad that is still running (circular or missed dependency).
- Token consumption hits 80% before Phase 6 is complete.
- The same task fails identically across three retry attempts (deterministic error, not transient).
- Two squads produce conflicting technical decisions (timezone, auth format, error schema) that were not resolved in handoff contracts.
- A circuit breaker has been open for more than 30 minutes.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "This project is too simple, epic decomposition is overkill" | What starts simple today easily scales to 3 epics and 15 stories tomorrow. Plan first. |
| "We will resolve inter-squad dependencies as we go" | Resolving dependencies ad-hoc is a direct route to project deadlock. Map them in a DAG. |
| "Estimating token budgets is a waste of time" | 70% of projects launched without token budgeting stall due to context exhaustion. |
| "Let's run 10 squads simultaneously to speed up delivery" | The coordination cost of 10 concurrent squads consumes twice the output speed of 5 squads. |
| "We will conduct the post-mortem once the project finishes" | At the end of the project, exhaustion sets in and critical lessons are forgotten. Run post-mortems after each epic. |
| "Let's give all squads access to the entire repository" | Spawning 50 sub-agents with 100K token contexts consumes 5M tokens immediately. Budget will run out. |

## Your Human Partner's Signals You're Doing It Wrong

**Escalate immediately when:**
- Architecture disagreements between squads (REST vs. GraphQL, SQL vs. NoSQL) cannot be resolved automatically.
- Token consumption reaches 95% of the allocated budget while critical tasks remain incomplete.
- A circuit breaker remains open for more than 30 minutes, indicating a systematic environment failure.
- Doubts regarding data integrity (missing records after migration, hash mismatch).
- A security vulnerability is identified that cannot be patched automatically.

**Inform at checkpoints:**
- Progress summary: % completion, remaining estimated duration, and critical path status.
- Token expenditure: spent / budget ratios, including justifications for any deviations.
- Risk registry: newly identified risks and mitigation statuses.
- Open questions: outstanding items requiring business/design decisions.

## Related Skills

- **subagent-orchestrator** — Sub-task parallelization. Used inside each squad under Epic Orchestrator.
- **squad-builder** — Squad composition design. Referenced during Phase 2.
- **task-lifecycle-manager** — Kanban task tracking. Powers the monitoring dashboard.
- **agent-teammate** — Persistent AI teammate. Squad members are created using this skill.
- **grill** — Discovery and requirement scoping. Executed BEFORE Epic Orchestrator.
- **architecture-planner** — Architectural planning. Guides the technical decisions made by squads.
- **spec-first-development** — Specification authoring. Helps break epics into user stories.
- **agent-introspector** — Agent behavior debugging. Used to triage squad performance bottlenecks.
- **session-memory** — Cross-session memory. Essential for post-mortems and learning loops.
- **skill-marketplace** — Skill discovery and versioning. Used to publish newly extracted patterns as active skills.

**Recommended chaining after completion:** `squad-builder` → `task-lifecycle-manager` → `agent-teammate` → `skill-marketplace` → `post-mortem` → `skill_manage`.

## Verification

- [ ] Epic decomposition is complete; INVEST criteria met for all stories.
- [ ] Dependency DAG is mapped; critical path is calculated.
- [ ] Role assignments, token budgets, and handoff contracts are defined for each squad.
- [ ] Resource plan is finalized (timeline + bottleneck analysis).
- [ ] Monitoring dashboard is established (metrics + alert conditions).
- [ ] Error recovery strategy is defined per failure type (retry, fallback, escalate).
- [ ] Mid-flight steering mechanisms are ready (inject, rebalance, reprioritize, rescope).
- [ ] Cross-squad integration tests are passing.
- [ ] Quality gates are satisfied (coverage, security, performance, accessibility).
- [ ] Post-mortem is documented; extracted patterns are registered in the skill system.
- [ ] Final summary report is delivered and approved by human partner.
- [ ] Squad contexts are archived; historical benchmarks are registered.
