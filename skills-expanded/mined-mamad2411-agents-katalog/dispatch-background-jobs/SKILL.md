---
name: "dispatch-background-jobs"
description: "Claude Code Dispatch: run long-running tasks as background jobs with progress polling, parallel sub-agent fan-out, result aggregation, and automatic retry on failure"
---

# Dispatch — Background Job Execution

## When to activate
- User asks to run a long task "in the background" while they continue working
- Parallel batch operations that need fan-out across many inputs (e.g., process 50 files, audit 100 repos)
- Multi-step workflows where intermediate results are aggregated at the end
- CI/CD pipelines triggered from Claude Code that need non-blocking execution
- Research tasks that should run autonomously and report back when done
- When tasks exceed the interactive session timeout or context budget

## When NOT to use
- Quick single-step tasks that complete in under 30 seconds
- Interactive tasks requiring real-time user confirmation at each step
- Simple file reads/writes that don't benefit from background execution
- Tasks that depend on synchronous terminal output for the next step

## Instructions

### 1. Dispatch Architecture

Dispatch runs a task as a background sub-agent with a job ID for tracking:

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────┐
│  Main Session   │────▶│  Dispatch Job    │────▶│  Result     │
│  (interactive)  │     │  (background)    │     │  Aggregator │
└─────────────────┘     └──────────────────┘     └─────────────┘
       │                        │
       │  poll status           │  progress events
       ▼                        ▼
  "How's the job?"         45% complete, 12/27 done
```

### 2. Job Definition

Define a dispatch job with clear boundaries:

```yaml
dispatch:
  job_id: "audit-2026-06-13"
  description: "Audit all 42 workspace stacks for skill coverage"
  parallelism: 4          # max concurrent sub-tasks
  timeout_minutes: 30     # hard cutoff
  retry:
    max_attempts: 2
    backoff: exponential  # 1s, 2s, 4s
  tasks:
    - name: "validate-stacks"
      type: "batch"
      inputs: "{{stacks}}"   # fan-out across all stacks
      action: "node scripts/validate-stacks.js --stack={{input}}"
    - name: "aggregate-results"
      type: "reduce"
      depends_on: ["validate-stacks"]
      action: "summarize all validation outputs"
```

### 3. Progress Polling Patterns

**Active polling (user asks for status):**
```
User: "How's the background audit going?"
Agent: Check job status → report: "12/42 stacks validated, 3 with warnings, ETA ~8 minutes"
```

**Event-driven (agent reports when done):**
```
Agent: "Background job complete: 42/42 stacks validated. 39 pass, 3 have coverage below 60%. 
       Full report in /tmp/dispatch-audit-2026-06-13.md"
```

**Structured progress output:**
```json
{
  "job_id": "audit-2026-06-13",
  "status": "running",
  "progress": {
    "total": 42,
    "completed": 27,
    "failed": 0,
    "pending": 15
  },
  "elapsed_seconds": 184,
  "estimated_remaining_seconds": 102
}
```

### 4. Parallel Fan-Out Patterns

**Map-reduce (most common):**
1. Split input into N chunks
2. Dispatch N sub-agents in parallel
3. Collect results
4. Reduce/aggregate into final output

**Fan-out example:**
```yaml
tasks:
  - name: "process-files"
    type: "map"
    inputs: ["file1.md", "file2.md", ..., "file50.md"]
    chunk_size: 10         # 5 parallel workers, 10 files each
    action: "validate frontmatter for each file"
  
  - name: "aggregate"
    type: "reduce"
    depends_on: ["process-files"]
    action: "merge all validation results, count errors by type"
```

**Pipeline fan-out (dependent stages):**
```yaml
tasks:
  - name: "stage-1-research"
    type: "map"
    inputs: ["topic-a", "topic-b", "topic-c"]
    action: "gather sources and summarize"
  
  - name: "stage-2-synthesize"
    type: "reduce"
    depends_on: ["stage-1-research"]
    action: "cross-reference all research, identify themes"
  
  - name: "stage-3-report"
    type: "single"
    depends_on: ["stage-2-synthesize"]
    action: "write final research report"
```

### 5. Error Handling & Retry

```yaml
error_strategy:
  on_task_failure: "continue"     # continue other tasks, mark this one failed
  on_batch_failure: "retry"       # retry failed items up to max_attempts
  on_timeout: "partial-results"   # return what completed before timeout
  
  dead_letter:
    enabled: true
    path: "/tmp/dispatch-failures/"
    action: "log failed inputs with error details for manual review"
```

### 6. Result Aggregation

After all tasks complete, produce a structured result:

```markdown
## Dispatch Job Report: audit-2026-06-13

**Status:** Complete (42/42)
**Duration:** 4m 46s
**Result:** 39 passed, 3 warnings

### Warnings
| Stack | Issue | Severity |
|-------|-------|----------|
| operations_manager_stack | 0% skill coverage | HIGH |
| user_research_stack | 0% skill coverage | HIGH |
| ecommerce_operator_stack | 20% skill coverage | MEDIUM |

### Artifacts
- Full report: `/tmp/dispatch-audit-2026-06-13.md`
- Raw results: `/tmp/dispatch-audit-2026-06-13.json`
```

## Example

**Running a parallel code audit across all workspace stacks:**

```
User: "Run a background audit of all 42 stacks — check skill coverage, 
       frontmatter validity, and CLAUDE.md completeness. Report when done."

Agent dispatches:
  job_id: "stack-audit-2026-06-13"
  parallelism: 6
  tasks:
    1. fan-out: validate each stack (42 sub-tasks, 6 concurrent)
    2. reduce: aggregate coverage percentages
    3. reduce: compile frontmatter error summary
    4. single: generate final report

[5 minutes later]

Agent: "Stack audit complete.
  - 42/42 stacks validated
  - 39 pass (>60% skill coverage)
  - 3 below threshold
  - 0 frontmatter errors (new files)
  - Full report saved to stack-audit-report.md"
```

## Anti-Patterns

- **Fire-and-forget without job ID:** Dispatching without tracking means you can't check status or retrieve results
- **Unbounded parallelism:** Spawning 100 concurrent sub-agents exhausts rate limits and context — cap at 4-8 workers
- **No timeout:** Background jobs without timeouts can hang indefinitely — always set a hard cutoff
- **Ignoring failures:** If 3 of 50 tasks fail silently, the aggregated result looks healthy — always surface failures in the report
- **Result loss:** Not writing results to a file means they're lost when the session ends — persist to disk before reporting completion
- **Context overflow in reduce:** Aggregating 50 large sub-task outputs into one context window causes overflow — summarize each sub-task output before the reduce step
