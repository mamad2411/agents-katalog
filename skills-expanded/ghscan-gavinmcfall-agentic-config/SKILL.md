---
name: game-dev
description: Parent skill for all game development work. Routes to the right sub-skill based on what you need. Invoke this instead of remembering 14 individual game dev skills.
zones: { knowledge: 20, process: 30, constraint: 10, wisdom: 40 }
---

# Game Dev — Skill Router

You're working on game development. This skill helps you pick the right sub-skill for the task at hand.

## Quick Router

| What you need | Invoke |
|--------------|--------|
| **Start or end a work session** | `session-planner` |
| **Plan a sprint or manage tasks** | `sprint-manager` |
| **Evaluate scope / say no to ideas** | `scope-guardian` |
| **Record or revisit a decision** | `decision-journal` |
| **Plan what to learn next** | `learning-planner` |
| **Navigate boot.dev courses** | `boot-dev-companion` |
| **Write or update the GDD** | `gdd-writer` |
| **Scope or evaluate a prototype** | `prototype-coach` |
| **Research a game dev topic** | `game-research` |
| **Organize art assets or pipeline** | `art-pipeline` |
| **Source or organize audio** | `sound-designer` |
| **Steam store, builds, or publishing** | `steam-publisher` |
| **Plan or run a playtest** | `playtest-coordinator` |
| **Manage Plane tickets/epics** | `plane` |

## Composition Patterns

```
session start → session-planner → adhd-coach (energy check)
sprint planning → sprint-manager → scope-guardian (prevent overcommit)
learning path → learning-planner → boot-dev-companion (course selection)
design question → gdd-writer ↔ prototype-coach (validate via prototype)
release planning → steam-publisher → playtest-coordinator (Next Fest)
```

## Cross-Domain Links

- **Struggling emotionally?** → `inner-ally` (wellbeing group, not game-dev)
- **ADHD blocking you?** → `adhd-coach` (wellbeing group)
- **Need to deploy something?** → `home-ops-deployer` (infrastructure group)
- **Cluster issues?** → `k8s-operator` (infrastructure group)
- **Automate a workflow?** → `n8n-workflow-builder` (infrastructure group)

## Sub-Skills Reference

### Session & Planning
- `session-planner` — Start/end rituals. Bridges ADHD energy with sprint tickets.
- `sprint-manager` — Solo dev sprint planning with Plane. ADHD-adapted, not Agile.
- `scope-guardian` — Protect scope at feature/sprint/project level. The external "no."
- `decision-journal` — Record decisions with context. Prevents re-evaluation loops.

### Learning & Growth
- `boot-dev-companion` — boot.dev courses mapped to game dev readiness gates.
- `learning-planner` — Structure learning paths. Prevents tutorial hell.

### Game Design & Production
- `gdd-writer` — Lean, living Game Design Documents.
- `prototype-coach` — Scope and evaluate prototypes. Kill or commit.
- `game-research` — Research with solo-dev feasibility filtering.

### Asset Pipeline
- `art-pipeline` — Sprites, source files, folder structure, asset production.
- `sound-designer` — Audio sourcing, organization, format specs, licensing.

### Publishing & Testing
- `steam-publisher` — Steamworks through post-launch.
- `playtest-coordinator` — Playtests, feedback, Next Fest prep.

### Project Management
- `plane` — Plane project management operations.
