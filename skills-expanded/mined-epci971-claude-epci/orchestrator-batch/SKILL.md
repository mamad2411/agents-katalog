---
name: orchestrator-batch
description: >-
  Orchestrates batch execution of EPCI specs with DAG dependency management,
  priority sorting, auto-retry, and dual journaling (Markdown + JSON).
  Use when: executing multiple specs overnight, batch processing after /decompose.
  Not for: single feature execution (use /epci or /quick).
---

# Orchestrator Batch

## Overview

This skill provides the core logic for the `/orchestrate` command. It manages
the automated execution of multiple EPCI specs from a directory, handling
dependencies, priorities, retries, and comprehensive logging.

**Key capabilities:**
- DAG-based dependency ordering
- Priority sorting with effort-based tiebreaker
- Auto-retry with context-aware error handling
- Dual journaling (MD for humans, JSON for tools)
- Real-time INDEX.md progress updates
- Checkpoint/resume for interrupted runs

## Configuration

| Element | Value |
|---------|-------|
| **Command** | `/orchestrate` |
| **Invokes** | `/brief`, `/epci`, `/quick` (internally) |
| **Reuses** | `dag_builder.py`, `wave_context.py`, `hooks/runner.py` |

## Core Concepts

### INDEX.md Format

The orchestrator expects an INDEX.md file with this structure:

```markdown
# Specs Overview

| ID | Title | Effort | Priority | Dependencies | Status |
|----|-------|--------|----------|--------------|--------|
| S01 | Core logic | 4h | - | - | Pending |
| S02 | Techniques | 2h | 1 | - | Pending |
| S03 | Integration | 3h | - | S01, S02 | Pending |
```

**Fields:**
- **ID**: Unique identifier (e.g., S01, S02)
- **Title**: Short description
- **Effort**: Estimated time (maps to TINY/SMALL/STANDARD/LARGE)
- **Priority**: Optional 1-99 (1 = highest), empty = default
- **Dependencies**: Comma-separated IDs or "-" for none
- **Status**: Pending, Running, Success, Failed, Skipped

### Execution Order Algorithm

```
1. Build DAG from dependencies
2. Detect and reject cycles
3. Topological sort (dependencies first)
4. Within same DAG level, sort by:
   a. Priority (1-99, lower wins)
   b. Effort (TINY < SMALL < STANDARD < LARGE)
   c. Alphabetical (tiebreaker)
5. Propagate priority: if S03 (priority 1) depends on S01 (priority 5),
   then S01 inherits priority 1
```

### Timeout by Complexity

| Complexity | Timeout | Based on |
|------------|---------|----------|
| TINY | 15 min | < 50 LOC, 1 file |
| SMALL | 30 min | < 200 LOC, 2-3 files |
| STANDARD | 1 hour | < 1000 LOC, 4-10 files |
| LARGE | 2 hours | 1000+ LOC, 10+ files |

## Process

### Step 1: Parse INDEX.md

```python
# Pseudo-code
specs = parse_index_md(specs_dir / "INDEX.md")
for spec in specs:
    validate_spec_file_exists(specs_dir / f"{spec.id}.md")
```

### Step 2: Build DAG

**Reference**: [dag-building.md](references/dag-building.md)

Uses existing `dag_builder.py` infrastructure:
- `DAGBuilder.add_agent()` for each spec
- `DAG.topological_sort()` for order
- `CycleDetectedError` for cycle rejection

### Step 3: Sort by Priority

**Reference**: [priority-sorting.md](references/priority-sorting.md)

Applies multi-criteria sort within same DAG level.

### Step 4: Execute Loop

**Reference**: [auto-retry-strategy.md](references/auto-retry-strategy.md)

For each spec:
1. Check dependencies resolved
2. Invoke workflow (brief → epci/quick)
3. Validate (tests, lint)
4. Retry on failure (max 3)
5. Commit on success
6. Update progress
7. Clear context

### Step 5: Journal

**Reference**: [dual-journaling.md](references/dual-journaling.md)

Write MD and JSON journals in real-time.

### Step 6: Report

Generate final summary with metrics.

## Agents

This skill does not define new agents. It invokes existing EPCI agents through
the `/brief`, `/epci`, and `/quick` commands.

**Agents invoked indirectly:**
- `@plan-validator` (via /epci Phase 1)
- `@code-reviewer` (via /epci Phase 2)
- `@security-auditor` (via /epci Phase 2, conditional)
- `@doc-generator` (via /epci Phase 3)

## Hooks

| Hook | Trigger | Use |
|------|---------|-----|
| `pre-orchestrate` | Before execution loop | Validate environment |
| `post-spec` | After each spec | Update external trackers |
| `post-orchestrate` | After completion | Notify, deploy |

**Reference**: [hooks-integration.md](references/hooks-integration.md)

## Project Memory Integration

**Reference**: [project-memory-integration.md](references/project-memory-integration.md)

- Checkpoint saves to `.project-memory/orchestration/`
- Each spec result saved to feature history
- Velocity metrics updated after completion

## References

| Topic | File |
|-------|------|
| DAG Construction | [dag-building.md](references/dag-building.md) |
| Priority Algorithm | [priority-sorting.md](references/priority-sorting.md) |
| Retry Strategy | [auto-retry-strategy.md](references/auto-retry-strategy.md) |
| Journal Formats | [dual-journaling.md](references/dual-journaling.md) |
| Memory Integration | [project-memory-integration.md](references/project-memory-integration.md) |
| Hook Points | [hooks-integration.md](references/hooks-integration.md) |

## Examples

### Basic Usage

```bash
/orchestrate ./docs/specs/my-project/
```

### Dry Run

```bash
/orchestrate ./docs/specs/my-project/ --dry-run
```

### Resume After Interruption

```bash
/orchestrate ./docs/specs/my-project/ --continue
```

### Skip Problematic Specs

```bash
/orchestrate ./docs/specs/my-project/ --skip S03,S05
```

### Execute Single Spec (Testing)

```bash
/orchestrate ./docs/specs/my-project/ --only S01
```

## Error Recovery

| Scenario | Recovery |
|----------|----------|
| Interrupted mid-spec | `--continue` resumes |
| Spec keeps failing | After 3 retries, skip and continue |
| Git conflict | Abort, manual resolution required |
| Memory pressure | Aggressive context clear between specs |

## See Also

- Command: `/orchestrate`
- Related: `/decompose` (generates specs), `/epci` (single execution)
