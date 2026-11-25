---
name: knowledge-generator
description: >
  Generates and accumulates structured project knowledge during the delivery process.
  Produces design baseline documents, ADRs, and project CLAUDE.md from Agent activities.
trigger: when completing design phases, making architectural decisions, or discovering constraints
tags: [knowledge, documentation, baseline, adr, learning]
version: "1.0"
scope: workspace
category: delivery
---

# Knowledge Generator

## Purpose

Accumulate structured project knowledge as the Agent works through delivery stages.
Unlike ad-hoc documentation, this skill produces knowledge in standardized formats
that compound across sessions.

## Knowledge Artifacts

### 1. Design Baseline Document

Generated after codebase analysis or architecture design. Uses the format from
`codebase-profiler` skill (§1-§6 sections). Updated incrementally as the project evolves.

**When to generate:**
- After running `analyze_codebase` on a new repository
- After completing an architecture design session
- When significant structural changes are made

**Storage:** `design-baseline.md` in workspace root

### 2. Architecture Decision Records (ADR)

Capture key decisions made during development.

**Format:**
```markdown
## ADR-{N}: {Title}

**Status:** Accepted | Superseded | Deprecated
**Date:** YYYY-MM-DD
**Context:** Why this decision was needed
**Decision:** What was decided
**Consequences:** Trade-offs and implications
```

**When to generate:**
- When choosing between multiple valid approaches
- When overriding a default convention
- When introducing a new dependency or pattern

**Storage:** Append to `decisions.md` in workspace root

### 3. Constraints & Pitfalls

Track discovered constraints and gotchas for the specific project.

**When to generate:**
- When a build/test fails due to environment specifics
- When discovering undocumented API behavior
- When hitting framework limitations

**Storage:** Update workspace memory via `update_workspace_memory`

## Integration with Delivery Stages

| Stage | Knowledge Output |
|-------|-----------------|
| Planning | Initial design baseline from codebase analysis |
| Design | ADRs for architectural decisions |
| Development | Constraint discoveries, updated baseline |
| Testing | Test coverage metrics, quality insights |
| Ops | Deployment notes, operational constraints |

## Relationship to Memory System

- **Workspace Memory** (Layer 1): Short-term cross-session context (4000 char limit)
- **Stage Memory** (Layer 2): Profile-scoped aggregation across sessions
- **Session Summary** (Layer 3): Structured summary per session
- **Design Baseline**: Long-term structural knowledge (this skill's primary output)
- **ADR Log**: Decision history (this skill's secondary output)

The knowledge generator bridges the gap between ephemeral memory and permanent documentation.
