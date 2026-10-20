---
name: "graph-augmented-context"
description: "Claude Code Graph-Augmented Context (GAC): local SQLite codebase knowledge graph builder. Maps files, classes, functions, and import/dependency edges for advanced codebase RAG and contextual navigation"
---

# Graph-Augmented Context (GAC) — Knowledge Graph Repository Mapping

## When to activate
- Analyzing large or legacy codebases with complex file structures and deep directory hierarchies.
- Mapping code dependencies, class hierarchies, import structures, or shared utilities.
- Troubleshooting circular dependency warnings or tracking down side effects of a proposed signature change.
- Onboarding to an unfamiliar codebase and building a mental model of how components interlock.

## When NOT to use
- Small, single-file projects or simple scripts with zero external or cross-file dependencies.
- Static content repositories (e.g. pure markdown documentation directories).
- Non-code directories containing only assets or media.

## Instructions

Graph-Augmented Context maps the repository as a structured directed graph using a local SQLite database (`.claude/gac.db`). This allows Claude to execute semantic code path tracing, complex relation filtering, and downstream impact analysis.

```
       ┌───────────────┐
       │   File Node   │
       └───────┬───────┘
               │ DEFINES
               ▼
       ┌───────────────┐  INHERITS  ┌───────────────┐
       │  Class Node   ├───────────►│ Parent Class  │
       └───────┬───────┘            └───────────────┘
               │ DEFINES
               ▼
       ┌───────────────┐    CALLS   ┌───────────────┐
       │ Function Node ├───────────►│ Other Function│
       └───────────────┘            └───────────────┘
```

### 1. SQLite Database Schema
Construct a local graph database at `.claude/gac.db` with the following structure:

```sql
-- Schema for .claude/gac.db

CREATE TABLE IF NOT EXISTS nodes (
  id TEXT PRIMARY KEY,          -- Fully qualified identifier (e.g., 'src/utils/auth.ts:generateToken')
  name TEXT NOT NULL,           -- Base name of the symbol (e.g., 'generateToken')
  type TEXT NOT NULL,           -- 'FILE', 'CLASS', 'INTERFACE', 'FUNCTION', 'VARIABLE'
  filepath TEXT NOT NULL,       -- Relative file path (e.g., 'src/utils/auth.ts')
  line_number INTEGER,          -- Declaration line number (1-indexed)
  docstring TEXT                -- Extracted docstring, description, or parameter signature
);

CREATE TABLE IF NOT EXISTS edges (
  source TEXT,                  -- Node ID (origin of relationship)
  target TEXT,                  -- Node ID (destination of relationship)
  relationship_type TEXT,       -- 'IMPORTS', 'DEFINES', 'INHERITS', 'CALLS', 'IMPLEMENTS'
  PRIMARY KEY (source, target, relationship_type),
  FOREIGN KEY (source) REFERENCES nodes(id) ON DELETE CASCADE,
  FOREIGN KEY (target) REFERENCES nodes(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_nodes_type ON nodes(type);
CREATE INDEX IF NOT EXISTS idx_nodes_filepath ON nodes(filepath);
CREATE INDEX IF NOT EXISTS idx_edges_relationship ON edges(relationship_type);
```

### 2. Node & Edge Extraction Workflow

For the codebase languages, scan files and insert entities using parser tools or helper shell scripts:
*   **Files:** Create a node for every code file.
*   **Imports:** Parse import declarations to create `IMPORTS` edges between files.
*   **Definitions:** Identify classes, interfaces, and functions, inserting them as nodes and linking them to their host file using `DEFINES` edges.
*   **Calls:** Parse function call sites to link the caller function to the callee function using `CALLS` edges.
*   **Inheritance:** Link classes inheriting from parents or implementing interfaces via `INHERITS` or `IMPLEMENTS` edges.

### 3. Traversal Patterns (Context Enrichment Queries)

Run these queries to gather context before editing:

#### A. Downstream Impact ("Blast Radius")
Determine what will break if a function's signature is changed:
```sql
SELECT n.filepath, n.name, n.type, n.line_number 
FROM nodes n
JOIN edges e ON n.id = e.source
WHERE e.target = 'src/services/db.ts:queryUser'
  AND e.relationship_type = 'CALLS';
```

#### B. Complete Component Call-Graph
Trace execution pathways for debugging:
```sql
WITH RECURSIVE call_path(source, target, depth) AS (
  SELECT source, target, 1 FROM edges WHERE source = 'src/routes/users.ts:getUserHandler' AND relationship_type = 'CALLS'
  UNION ALL
  SELECT e.source, e.target, cp.depth + 1
  FROM edges e
  JOIN call_path cp ON e.source = cp.target
  WHERE e.relationship_type = 'CALLS' AND cp.depth < 5
)
SELECT cp.depth, n_src.name AS caller, n_tgt.name AS callee, n_tgt.filepath
FROM call_path cp
JOIN nodes n_src ON cp.source = n_src.id
JOIN nodes n_tgt ON cp.target = n_tgt.id
ORDER BY cp.depth;
```

#### C. Find Orphan/Dead Code
Locate nodes defined but never imported or called:
```sql
SELECT id, name, filepath 
FROM nodes 
WHERE type IN ('FUNCTION', 'CLASS')
  AND id NOT IN (SELECT DISTINCT target FROM edges WHERE relationship_type IN ('CALLS', 'IMPORTS', 'INHERITS', 'IMPLEMENTS'));
```

---

## Example

**Analyzing a React project's authentication flow using GAC:**

```bash
# 1. Run the local parser and query the graph
sqlite3 .claude/gac.db "SELECT source, target, relationship_type FROM edges WHERE source LIKE '%useAuth%';"
```

**Results Output:**
```
src/hooks/useAuth.ts | src/contexts/AuthContext.ts | IMPORTS
src/hooks/useAuth.ts:useAuth | src/contexts/AuthContext.ts:AuthContext | CALLS
src/components/Navbar.tsx | src/hooks/useAuth.ts | IMPORTS
src/components/Navbar.tsx:Navbar | src/hooks/useAuth.ts:useAuth | CALLS
src/pages/Dashboard.tsx | src/hooks/useAuth.ts | IMPORTS
src/pages/Dashboard.tsx:Dashboard | src/hooks/useAuth.ts:useAuth | CALLS
```

**Claude Action:**
Through these outputs, Claude realizes that modifying `useAuth` affects `Navbar` and `Dashboard`. It loads only those two file contexts for verification, saving thousands of input tokens while avoiding breaks in downstream files.
