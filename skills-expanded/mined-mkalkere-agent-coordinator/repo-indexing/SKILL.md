---
name: repo-indexing
version: 1.0.0
description: Index repository for deep codebase understanding
uses: []
requires:
  tools: []
  env: []
security:
  risk_level: read
  capabilities:
    - repo:read
  requires_approval: false
---

# Repository Indexing

Build comprehensive codebase understanding through systematic analysis. This runs in the background when the agent is idle, maintaining an up-to-date picture of the repository structure, dependencies, and patterns.

## Execution Model

This is a **builtin skill** (`handler: type: builtin`). When `index_repo` is invoked, the executor runs analysis scripts against the repository and writes structured results to the agent's memory directory. The tool schema in tool.yaml defines the external contract; the executor handles the scanning and output directly.

**Interruptibility**: Indexing is low-priority. If a higher-priority task arrives (e.g., review request), indexing pauses and resumes when idle.

## When to Use

- Agent starts and the index is stale (older than 24 hours)
- Agent is idle for 10+ minutes
- Manually triggered when codebase understanding is needed
- After major changes (large merges, refactors) that invalidate the existing index

## Methodology

### 1. Check Freshness

Before indexing, check if the existing index is still valid:
- Read `.last_indexed` timestamp from agent memory
- Compare to current time — skip if indexed within the configured interval
- Compare to latest commit — skip if no new commits since last index

### 2. Build File Inventory

Scan all source files and record:
- File path
- Language (detected from extension)
- Line count
- Last modified date

Exclude configured paths (`.venv`, `node_modules`, `.git`, `__pycache__`).

### 3. Build Import/Dependency Graph

For each source file, extract dependencies:
- Python: `import` and `from ... import` statements
- JavaScript/TypeScript: `import` and `require` statements
- Other languages: language-appropriate dependency declarations

Record which files depend on which, enabling impact analysis.

### 4. Map Tests to Implementations

For each implementation file, find its corresponding test file:
- Convention-based matching (`test_{name}.py`, `{name}_test.py`, `{name}.test.ts`)
- Directory-based matching (`src/foo.py` → `tests/test_foo.py`)
- Mark files with missing tests as `missing_test`

### 5. Detect Patterns and Issues

Scan for common patterns and potential problems:
- Async/await usage patterns
- Blocking I/O in async code (potential issue)
- Test framework and conventions
- Type hint coverage
- Error handling patterns
- Known anti-patterns

### 6. Write Index Files

Output structured files to agent memory:

| File | Content |
|------|---------|
| `file_inventory.yaml` | All source files with metadata |
| `import_graph.yaml` | Dependency relationships |
| `test_mappings.yaml` | Implementation-to-test file mapping |
| `detected_patterns.yaml` | Patterns and potential issues |
| `index_summary.md` | Human-readable summary |
| `.last_indexed` | Timestamp for freshness checking |

## Output Format

```
## Repository Index

### Statistics
- Source files: [count]
- Languages: [list]
- Test files: [count]
- Files missing tests: [count]
- Async functions: [count]

### Patterns Detected
- [pattern]: [count] occurrences
- [potential issue]: [count] locations

### Test Coverage Gaps
- [file]: missing test
- [file]: missing test

### Index Files Written
- [path]: [description]
```

## Quality Criteria

- All source files are inventoried (no missing files)
- Excluded paths are respected (no `.venv` or `node_modules` entries)
- Import graph captures actual dependencies (not false positives)
- Test mappings use the project's actual naming conventions
- Pattern detection identifies real issues (not noise)
- Index files are parseable YAML/Markdown
- Freshness check prevents unnecessary re-indexing

## Common Mistakes

- **Indexing too often**: Re-indexing every session when nothing has changed wastes time. Check freshness first.
- **Not excluding build artifacts**: Including `node_modules`, `.venv`, or `__pycache__` in the index creates enormous, useless files.
- **Wrong test naming conventions**: Assuming `test_{name}.py` when the project uses `{name}_test.py` or a different convention. Check actual test files first.
- **Blocking on indexing**: Running a full index during a time-sensitive task. Indexing is interruptible — pause for higher-priority work.
- **Stale index treated as current**: Using index data from 3 days ago without checking if the codebase has changed significantly since then.
- **Not writing the timestamp**: Forgetting to update `.last_indexed` means the next session will re-index unnecessarily.

## Completion

Repository indexing is complete when:
- All source files are inventoried
- Import graph is built
- Test mappings are established
- Patterns and potential issues are detected
- Index files are written to agent memory
- Freshness timestamp is updated
