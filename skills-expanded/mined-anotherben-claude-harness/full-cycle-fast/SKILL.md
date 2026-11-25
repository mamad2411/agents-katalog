---
name: full-cycle-fast
description: Lightweight rapid development workflow. Agent Harness with minimal ceremony. No research agents, no review agents, no TDD enforcement. Just analyze, plan, build, verify. Use for small features, config changes, quick fixes that are too big for "just do it" but don't need the full pipeline. Invoked with /full-cycle-fast followed by a description.
---

# Full Cycle Fast — Minimal Ceremony Workflow

Agent Harness execution stripped to essentials. No research. No review agents. Just build.

## Philosophy

```
Analyze → Plan → Build → Test → Ship. Nothing else.
```

For tasks where the full pipeline is overkill but you still want structure.

## When to Use

- 3-10 file changes with clear requirements
- Bug fixes where you know the cause
- Adding a feature that follows an existing pattern exactly
- Config changes, migrations, endpoint additions
- Anything that takes 15-60 minutes

## When NOT to Use (upgrade to /full-cycle or /full-cycle-research)

- New technology or pattern you haven't used before
- Security-sensitive changes
- Architectural decisions
- Changes touching 10+ files

---

## WORKFLOW (No separate modes — straight through)

### 1. Context Recall (30 seconds)

```
# Query knowledge graph for prior context on [task keywords] (if configured)
```

Note any gotchas. Move on.

### 2. Quick Analysis (2 minutes)

No formal document. Just output:

```
TASK: [one sentence]
DONE WHEN: [success criteria]
FILES: [list of files to touch]
RISK: [what could break]
```

### 3. Build (the bulk of the time)

- Read existing patterns in the codebase
- Implement following those patterns exactly
- Write tests for new behavior
- Run test suite after each file change

### 4. Verify + Ship

- Run full test suite
- `git diff --stat` — review what changed
- Commit with conventional message
- Compound any gotchas to knowledge graph

No review agents. No research agents. No ceremony. Just working software.

---

## QUICK REFERENCE

```
/full-cycle-fast add the margin column to the orders table
```
→ Check gotchas → Quick analysis → Build → Test → Commit

```
/full-cycle-fast fix the null pointer in orderRouteService
```
→ Search past sessions → Analyze → Fix → Test → Commit
