---
name: impact-analysis
description: Assess change risk before modifying a function. Maps blast radius, surfaces hidden dependencies, community cohesion, and unexpected cross-module connections.
argument-hint: "<function name or node_id>"
allowed-tools:
  - mcp__loom__search_code
  - mcp__loom__get_context
  - mcp__loom__get_blast_radius
  - mcp__loom__get_neighbors
  - mcp__loom__get_community
  - mcp__loom__shortest_path
  - mcp__loom__get_surprising_connections
  - mcp__loom__god_nodes
  - mcp__loom__suggest_questions
  - Read
---

# Impact Analysis

Map the blast radius of a proposed change before touching any code.

## Steps

### 1. Find the target node

```
search_code("<function name or user argument>")
```

Pick the most relevant result and copy its `node_id`.

### 2. Get full context

```
get_context("<node_id>")
```

Read: summary, signature, direct callers, direct callees. Note if `summary_stale: true`.

### 3. Blast radius (transitive callers)

```
get_blast_radius("<node_id>", depth=3)
```

Depth 3 covers most real-world chains. If result is large (>50 nodes), note which modules appear most.

### 4. Direct callers (one-hop)

```
get_context("<node_id>", callees_limit=0)
```

Returns the immediate dependents — the minimum surface area affected.

### 5. Surprising connections

```
get_surprising_connections(limit=10)
```

Look for entries that involve the target node or its module. These are the hidden risks engineers miss.

### 6. Community cohesion

```
graph_stats(include_cohesion=True)
```

Find the target's community. If cohesion < 0.2, the cluster is poorly bounded and changes propagate unexpectedly.

### 7. God node check

```
god_nodes(limit=20)
```

If the target appears in top 20, it has many callers — high risk, needs extra care.

### 8. Synthesize risk report

Report to the user:

**Target:** `node_id`, what it does (summary), signature

**Direct impact:**
- N direct callers (list them)
- N direct callees (what it depends on)

**Transitive impact:**
- Total blast radius: N nodes across M modules
- Heaviest-hit modules: list top 3

**Hidden risks:**
- Surprising connections involving target or its module
- Community cohesion score
- Whether it's a god node (top 20 most-called)

**Risk level:** Low / Medium / High / Critical

**Recommendation:**
- Safe to change with existing tests
- Needs new tests for specific callers
- Needs coordination across teams/modules
- Consider interface-preserving refactor first

### 9. Trace hidden paths if needed

When two distant modules both appear in blast radius:
```
shortest_path("<module_a_entry>", "<module_b_entry>")
```
Reveals the hidden chain connecting them.
