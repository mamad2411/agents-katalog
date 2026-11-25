---
name: design-explore
description: Explore 2-4 design options with pros/cons/criteria matrix before writing code. Use for L3-L4 tasks (refactors, architecture, new subsystems). Pairs with save_decision MCP tool.
---

# design-explore

Use this skill when the user asks for "design", "architecture", "approach", "options", "trade-offs", "how should we do X", or when task classifier returns level >= 3.

## Workflow

1. **Discover prior art** — `memory_recall(query="<task keywords>", mode="index", limit=10)` + `analogize(query="<task description>", exclude_project=None)` — check if similar decision was made before.

2. **Generate 2-4 options** for the design space. For each option, fill:
   - **Core approach** (1 sentence)
   - **Implementation sketch** (3-5 lines)
   - **Pros** (3 bullets)
   - **Cons** (2-3 bullets)
   - **Unknowns** (what we don't yet know)

3. **Build criteria matrix** — list 3-5 criteria that matter (e.g. performance, maintainability, migration risk, team familiarity). Rate each option 1-5 per criterion.

4. **Pick one** with justification referring to matrix. Name what was **discarded** and why.

5. **Save** — `save_decision(title, options, criteria_matrix, selected, rationale, discarded, project)`.

6. **Only then** proceed to implementation — with a clear decision in memory for next session.

## Output template

```markdown
## Decision: {title}

### Prior art
{memory_recall/analogize results — 1-2 sentences}

### Options

#### 1. {option name}
- **Approach:** {1 sentence}
- **Implementation:** {sketch}
- **Pros:** {3 bullets}
- **Cons:** {3 bullets}
- **Unknowns:** {bullets}

#### 2. {option name}
... (same structure)

### Criteria matrix

| Criterion | Option 1 | Option 2 | ... |
|---|:-:|:-:|:-:|
| {criterion} | 5 | 3 | ... |

### Selected: {option name}

{rationale — 2-3 sentences referencing matrix}

### Discarded

- **{option name}**: {1-sentence reason}
```

## When NOT to use

- L1/L2 tasks (quick fixes, straightforward additions) — overkill, just do it.
- Single-option situations (no real trade-off).
- Implementation bugs (debug first, design later).
