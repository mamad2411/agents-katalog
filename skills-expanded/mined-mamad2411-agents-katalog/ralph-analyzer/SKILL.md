---
name: ralph-analyzer
description: >-
  Analyzes Ralph Wiggum loop outputs for completion detection, stuck loop
  identification, and progress tracking. Implements dual-condition exit logic.
  Use when: @ralph-executor needs to analyze Claude responses.
  Not for: Direct invocation, used internally by Ralph components.
---

# Ralph Analyzer Skill

## Overview

This skill provides analysis capabilities for Ralph Wiggum loops:
- Parse RALPH_STATUS blocks from Claude output
- Detect completion using dual-condition logic
- Identify stuck loops and stagnation
- Track progress across iterations

## RALPH_STATUS Block Format

Claude MUST output this block at the end of each response:

```
---RALPH_STATUS---
STATUS: IN_PROGRESS | COMPLETE | BLOCKED
TASKS_COMPLETED_THIS_LOOP: <number>
FILES_MODIFIED: <number>
TESTS_STATUS: PASSING | FAILING | NOT_RUN
WORK_TYPE: IMPLEMENTATION | TESTING | DOCUMENTATION | REFACTORING
EXIT_SIGNAL: false | true
RECOMMENDATION: <one line summary>
---END_RALPH_STATUS---
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| STATUS | enum | Current work status |
| TASKS_COMPLETED_THIS_LOOP | int | Stories marked passes=true this iteration |
| FILES_MODIFIED | int | Count of files changed |
| TESTS_STATUS | enum | Test suite status |
| WORK_TYPE | enum | Category of work performed |
| EXIT_SIGNAL | bool | **Explicit exit indicator** |
| RECOMMENDATION | string | Next action or completion message |

### STATUS Values

| Value | Meaning | Loop Action |
|-------|---------|-------------|
| IN_PROGRESS | Work ongoing | Continue |
| COMPLETE | All stories done | Exit loop |
| BLOCKED | Cannot proceed | Exit with code 2 |

### WORK_TYPE Values

Used for analytics and stuck loop detection:

| Value | Description |
|-------|-------------|
| IMPLEMENTATION | Writing new code |
| TESTING | Writing or fixing tests |
| DOCUMENTATION | Updating docs |
| REFACTORING | Improving existing code |

## Dual-Condition Exit Logic

The exit decision uses **both** completion indicators AND explicit EXIT_SIGNAL:

```
completion_indicators = count_matches([
    "all tests pass",
    "all stories complete",
    "project complete",
    "nothing left to do"
])

IF completion_indicators >= 2 AND EXIT_SIGNAL == true:
    → Exit: project_complete
ELIF completion_indicators >= 2 AND EXIT_SIGNAL == false:
    → Continue (Claude explicitly says more work needed)
ELIF EXIT_SIGNAL == true:
    → Exit: project_complete (explicit signal)
ELIF STATUS == BLOCKED:
    → Exit: blocked
ELSE:
    → Continue
```

**Key insight**: EXIT_SIGNAL has priority over heuristics. If Claude says
`EXIT_SIGNAL: false`, the loop continues even if completion patterns match.

## Completion Patterns

The analyzer detects these patterns (case-insensitive):

```python
COMPLETION_PATTERNS = [
    r"all tests pass",
    r"all.*stories.*complete",
    r"project.*complete",
    r"implementation complete",
    r"nothing.*left.*to.*do",
    r"all tasks completed",
    r"COMPLETE",
    r"100%.*complete"
]
```

## Stuck Loop Detection

Identifies when the loop is making no progress:

### Indicators

| Indicator | Threshold | Action |
|-----------|-----------|--------|
| No file changes | 3 iterations | Circuit breaker → HALF_OPEN |
| Same error repeated | 5 iterations | Circuit breaker → OPEN |
| Test-only work | 3 iterations | Exit with "test_saturation" |
| Output declining | 70% reduction | Warning logged |

### Detection Algorithm

```python
def detect_stuck_loop(outputs: List[str]) -> bool:
    # Check last 3 outputs for same error signature
    error_hashes = [
        hash(extract_errors(o))
        for o in outputs[-3:]
    ]
    return len(set(error_hashes)) == 1
```

## Progress Tracking

Track progress across iterations in `.ralph-session.json`:

```json
{
  "session_id": "ralph-2025-01-13-103000",
  "started_at": "2025-01-13T10:30:00Z",
  "iterations": [
    {
      "number": 1,
      "timestamp": "2025-01-13T10:30:15Z",
      "status": "IN_PROGRESS",
      "tasks_completed": 1,
      "files_modified": 3,
      "exit_decision": "continue"
    }
  ],
  "total_tasks_completed": 5,
  "total_files_modified": 15,
  "total_commits": 4
}
```

## Hook Mode Analysis

For hook mode (`--mode hook`), also detect:

```markdown
<promise>COMPLETE</promise>
```

This Anthropic-style completion promise triggers immediate exit.

## Analysis Output

The analyzer returns structured JSON:

```json
{
  "timestamp": "2025-01-13T10:45:00Z",
  "iteration": 5,
  "ralph_status": {
    "found": true,
    "status": "IN_PROGRESS",
    "tasks_completed": 1,
    "files_modified": 2,
    "tests_status": "PASSING",
    "work_type": "IMPLEMENTATION",
    "exit_signal": false,
    "recommendation": "Continue to US-006"
  },
  "completion_indicators": 0,
  "exit_decision": "continue",
  "stuck_loop_detected": false,
  "circuit_breaker_state": "CLOSED"
}
```

## Integration Points

### With Circuit Breaker

```bash
# After each analysis
record_loop_result $iteration $files_modified $has_errors
```

### With @ralph-executor

The executor calls analyzer after each Claude response:

```python
analysis = analyze_response(claude_output, iteration)
if analysis.exit_decision == "continue":
    continue_loop()
elif analysis.exit_decision == "project_complete":
    exit_success()
elif analysis.exit_decision == "blocked":
    exit_blocked(analysis.recommendation)
```

### With Response Analyzer Script

The bash script `lib/response_analyzer.sh` implements this skill's logic
for script mode execution.

## Error Handling

| Scenario | Behavior |
|----------|----------|
| RALPH_STATUS missing | Fallback to heuristic detection |
| Malformed JSON | Parse as text, extract key fields |
| EXIT_SIGNAL ambiguous | Default to false (continue) |
| Multiple STATUS blocks | Use last one |

## Best Practices for Claude

When implementing stories, Claude should:

1. **Always output RALPH_STATUS** at response end
2. **Set EXIT_SIGNAL accurately**:
   - `false` if more work needed
   - `true` only when ALL stories pass
3. **Use STATUS: BLOCKED** for issues requiring human help
4. **Include actionable RECOMMENDATION**

## See Also

- `lib/response_analyzer.sh` — Bash implementation
- `lib/circuit_breaker.sh` — Stagnation detection
- `@ralph-executor` — Story execution agent
- `/ralph` — Main command
