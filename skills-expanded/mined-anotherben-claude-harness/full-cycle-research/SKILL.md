---
name: full-cycle-research
description: Research-heavy development workflow. Agent Harness + Compound Engineering deep research. 8+ parallel research agents explore best practices, framework docs, security patterns, and performance before any code is written. Use for unfamiliar territory, new integrations, architectural decisions, or when you want maximum confidence before building. Invoked with /full-cycle-research followed by a description.
---

# Full Cycle Research — Deep Research Development Workflow

Agent Harness execution with Compound Engineering's parallel research pipeline.

## Philosophy

```
Research deeply BEFORE building. The cost of research is hours.
The cost of building the wrong thing is days.
```

Every feature gets 8+ parallel research agents exploring best practices, framework docs,
security patterns, and real-world examples before a single line of code is written.

## Prerequisites

1. Agent Harness (`.claude/AGENT_HARNESS.md`)
2. Compound Engineering plugin (workflows: plan, deepen-plan, work, review)
3. Memory/knowledge MCP servers (if configured)
4. Context7 MCP for framework docs

---

## PLANNING MODE (Interactive + Deep Research)

### Phase 1: Define

1. Load Agent Harness Phase 0 — query knowledge graph for prior context
2. Invoke `compound-engineering:workflows:brainstorm` — collaborative dialogue
3. Save design to `.claude/designs/[feature-name].md`

### Phase 2: Create Plan

Invoke `compound-engineering:workflows:plan` with the design document.
This creates a structured plan at `docs/plans/[date]-[feature]-plan.md`.

### Phase 3: Deep Research (THE DIFFERENTIATOR)

Invoke `compound-engineering:deepen-plan` on the plan file.

This launches 8+ parallel research agents:
- **Best practices researcher** — industry standards, conventions
- **Framework docs researcher** — Context7 queries for exact API docs
- **Architecture strategist** — pattern compliance, coupling analysis
- **Performance oracle** — bottlenecks, optimization opportunities
- **Security sentinel** — OWASP risks, input validation, auth gaps
- **Code simplicity reviewer** — YAGNI check, scope cut recommendations
- **Agent-native reviewer** — are features accessible to agents?
- **Data integrity guardian** — transaction safety, cascade risks

Each agent enriches the plan with concrete recommendations, code examples, and warnings.

### Phase 4: Spec Flow Analysis

Run `compound-engineering:workflow:spec-flow-analyzer` to identify:
- Missing user flows
- Edge cases not covered
- Gap analysis against requirements

### >>> SINGLE CHECKPOINT <<<

Present the deepened plan with all research findings. Wait for "go".

---

## EXECUTION MODE (Autonomous)

### Execute with Compound Work

Invoke `compound-engineering:workflows:work` with the deepened plan file.

This follows the Agent Harness execution model:
- Work through tasks autonomously
- Don't stop between tasks
- Track progress in the plan file
- Use Agent Teams for [TEAM] tasks

### Post-Execution Review

Invoke `compound-engineering:workflows:review` — launches 12+ review agents:
- All agents from the research phase re-check the implementation
- Plus: pattern recognition, data migration expert, schema drift detector
- Creates todos for any findings

### Fix Critical Findings

Invoke `compound-engineering:resolve_todo_parallel` to fix all P1/P2 findings in parallel.

### Compound Learnings

1. Invoke `compound-engineering:workflows:compound` — document what was learned
2. Save patterns, gotchas, decisions to knowledge graph
3. Index session in knowledge graph (if configured)

---

## WHEN TO USE THIS vs /full-cycle

| Use `/full-cycle-research` when... | Use `/full-cycle` when... |
|-------------------------------------|--------------------------|
| New technology or integration | Familiar codebase patterns |
| Security-sensitive feature | Internal tooling |
| External API integration | Well-understood domain |
| Architectural decision needed | Small-medium features |
| First time doing X in this project | Repeat of established pattern |
| High-stakes / hard to reverse | Easy to iterate on |

---

## QUICK REFERENCE

```
/full-cycle-research integrate Stripe payments
```
→ Brainstorm → Plan → 8 research agents → Deepen → SpecFlow → "go" → Build → 12 reviewers → Fix → Ship

```
/full-cycle-research add WebSocket real-time updates
```
→ Deep research on WS patterns → Framework docs → Security review → Build with confidence
