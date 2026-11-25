---
name: blast-radius
description: Analyze the blast radius of code changes using GitLab Orbit's knowledge graph. Trace cross-file dependencies and assess impact before making changes.
---

# Blast Radius Analysis

Use GitLab Orbit's knowledge graph to find all code that depends on a given file, function, or class. This helps developers understand what will break before they make changes.

## When to Use

- A developer wants to know the impact of changing a specific file or function
- Someone mentions `@blast-radius <file-path>` in an issue or MR comment
- You're asked to assess risk before a refactor or migration

## Query Pattern

### Step 1: Understand the Schema

Use `get_graph_schema` to list available node types and relationships in the Orbit knowledge graph. Key types:
- `gl_definition` — files, functions, classes, modules
- `gl_reference` — edges connecting definitions (source depends on target)

### Step 2: Find the Definition (SQL mode — Orbit CLI)

Query `gl_definition` nodes matching the target file or function:

```sql
SELECT * FROM gl_definition WHERE path LIKE '%target_file%' OR name = 'functionName';
```

### Step 2b: Find the Definition (Cypher mode — Orbit Remote/MCP)

```
query_graph("MATCH (d:gl_definition) WHERE d.path CONTAINS 'target_file' RETURN d.id, d.name, d.path")
```

Note: The SQL syntax is used with Orbit CLI (`orbit sql ...`). The Cypher-style syntax is used with Orbit Remote (`query_graph` MCP tool). Pick the one that matches your Orbit access mode.

### Step 3: Trace Direct References

Find all `gl_reference` edges pointing TO the definition. These are the direct dependents:

```sql
-- What depends on target?
SELECT DISTINCT t2.name, t2.path, t2.language
FROM gl_definition t1
JOIN gl_reference ON t1.id = gl_reference.target_id
JOIN gl_definition t2 ON gl_reference.source_id = t2.id
WHERE t1.path LIKE '%target_file.py%'
```

### Step 4: Trace Transitive Impact

For each direct dependent, repeat Step 3 to find files that depend on THEM:

```sql
-- Full transitive chain (2 levels)
WITH direct AS (
  SELECT t2.id, t2.name, t2.path
  FROM gl_definition t1
  JOIN gl_reference ON t1.id = gl_reference.target_id
  JOIN gl_definition t2 ON gl_reference.source_id = t2.id
  WHERE t1.path LIKE '%target_file.py%'
)
SELECT DISTINCT t3.name, t3.path, t3.language
FROM direct d
JOIN gl_reference ON d.id = gl_reference.target_id
JOIN gl_definition t3 ON gl_reference.source_id = t3.id
WHERE t3.id NOT IN (SELECT id FROM direct)
```

### Step 5: Assess Cross-Project Impact

If the knowledge graph spans multiple projects, identify which projects contain dependents:

```sql
SELECT DISTINCT t2.project_path
FROM gl_definition t1
JOIN gl_reference ON t1.id = gl_reference.target_id
JOIN gl_definition t2 ON gl_reference.source_id = t2.id
WHERE t1.path LIKE '%target_file.py%'
```

## Risk Classification

Risk is classified from the **total** dependent count (direct + transitive)
using inclusive lower bounds, so every count maps to exactly one level (no
overlapping boundaries). Thresholds are configurable via `.env`.

| Risk Level | Total dependents | Also Critical if |
|---|---|---|
| **Low** | 0–2 | — |
| **Medium** | 3–10 | — |
| **High** | 11–50 | — |
| **Critical** | 51+ | dependents span 3+ projects (shared hub) |

The reference implementation of these rules lives in `blast_radius/risk.py`
and is covered by boundary tests in `tests/test_risk.py`.

## Response Format

Always structure your findings as:

```
DIRECT IMPACT:
- <file>:<line> — <how it references the target>
...

TRANSITIVE IMPACT:
- <file> — depends on <direct-dependent>
...

PROJECT IMPACT:
- <project-path>

RISK SCORE: <Low|Medium|High|Critical>
RECOMMENDATION: <suggested action before landing the change>
```

## Orbit CLI Quick Reference

For local mode (Orbit CLI):

```bash
# Index a project
orbit index /path/to/project

# Basic query — all definitions
orbit sql "SELECT * FROM gl_definition LIMIT 20"

# Dependencies of a file
orbit sql "SELECT t2.path, t2.name FROM gl_definition t1 JOIN gl_reference ON t1.id = gl_reference.target_id JOIN gl_definition t2 ON gl_reference.source_id = t2.id WHERE t1.path LIKE '%target%'"

# List relationship types
orbit sql "SELECT DISTINCT relationship_type FROM gl_reference"

# Count dependents per file (hotspot analysis)
orbit sql "SELECT t1.path, COUNT(gl_reference.source_id) as dependents FROM gl_definition t1 JOIN gl_reference ON t1.id = gl_reference.target_id GROUP BY t1.path ORDER BY dependents DESC LIMIT 20"
```

## Target Resolution

### Zero matches

If `query_graph` returns no matching `gl_definition` nodes:

1. Confirm the file path is relative to the repository root
2. Try searching by file name only (e.g., `tokens.py` instead of `src/auth/tokens.py`)
3. Try searching by function/class name instead
4. If still no match, the repository may not be fully indexed. Run `orbit index` (local) or check Orbit Remote indexing status.
5. Return: `{error: "No matching definition found for '<query>'. Try a different path or function name."}`

### Multiple matches

If the query matches multiple definitions (e.g., `auth.py` matches `src/auth/auth.py` and `tests/auth/auth.py`):

1. List all matches with their full paths
2. Ask the developer to specify a more precise path
3. Return: `{ambiguous: true, matches: [path1, path2, ...], message: "Multiple matches found. Use the full path from repository root."}`

### File not in graph (not yet indexed)

Some files may not appear in the knowledge graph if they were added after the last index run. Inform the developer and suggest re-indexing.

## Pitfalls

- **Cyclic dependencies**: The graph can contain cycles. The engine prevents loops by seeding the visited set with the target and marking every node visited on discovery (before recursing), in addition to a depth limit. See `blast_radius/engine.py` and the cycle test in `tests/test_engine.py`.
- **Ambiguous targets**: If a path matches multiple distinct files and no function name is given, ask for disambiguation rather than guessing. If nothing matches, say so explicitly. See `resolve_target` in `blast_radius/engine.py`.
- **Dynamic imports**: `import()` and `require()` may not appear in static analysis. Flag these as "unanalyzed."
- **Test files**: Dependencies to/from test files may inflate blast radius. Consider filtering `*test*` and `*spec*` paths.
- **Generated code**: Auto-generated files create false positives. Filter `*.generated.*` and `__generated__/` paths.
