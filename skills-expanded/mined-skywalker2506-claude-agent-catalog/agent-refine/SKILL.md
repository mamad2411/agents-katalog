---
name: agent-refine
description: "Refine agent system per project — detect missing agents, split wide ones, define new agents, update registry. Triggers: agent-refine, agent refine, add agent, split agent, agent missing."
argument-hint: "[analyze | split <agent-id> | create <name>]"
---

# /agent-refine — Agent System Refinement

Detects agent system gaps during projects and automatically fixes them.

## Modes

### 1. Analyze mode (default)

```
/agent-refine
```

Scan current project, compare with agent-registry.json:
- What technologies are used in the project? (pubspec.yaml, package.json, etc.)
- Which capabilities are needed?
- Which existing agents are suitable, which are missing?
- Are existing agents too wide in scope?

Output:
```
## Agent Analysis Report — [project name]

### Suitable agents
- B15 Mobile Dev (Flutter + Dart compatible)
- B5 Database Agent (Firestore)

### Missing capabilities
- "stripe-payment" — not in any agent
  Suggestion: Add "stripe" capability to B4 API Integrator
  OR new agent: B22 Payment Agent

### Overly broad agents
- B2 Backend Coder: 6 capabilities, 3 languages — REST + GraphQL + migration + dto could be separate
  Suggestion: keep for now, split when usage increases
```

### 2. Split mode

```
/agent-refine split B2
```

Analyze capabilities of specified agent, split into logical subgroups:
1. Read agent .md file
2. Identify capability clusters
3. Create new agent .md files
4. Update registry
5. Narrow capabilities of old agent

### 3. Create mode

```
/agent-refine create "Payment Agent"
```

Create new agent:
1. Assign appropriate ID (category prefix + next number)
2. Write agent .md file (from template)
3. Add to registry (status: pool)
4. Update agents/README.md
5. Update CLAUDE.md §11 counts

## Rules

- Report current state before making changes
- Every new/split agent starts as `status: pool`
- Registry JSON and .md file must be in sync
- Create git commit: `feat: agent-refine — [what was done]`
- Also update GitHub repos (marketplace README agent counts)
- Max 15 tool calls
