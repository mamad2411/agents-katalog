---
name: follow-parallel
description: Group independent operations into parallel execution to cut time and increase efficiency
argument-hint: "[scope]"
related:
  - follow-math-concepts
  - deep-review-codebase

---

## Goal

Group independent operations into parallel execution to reduce total execution time and increase efficiency without breaking determinism and safety

## Scope

Use for managing parallel execution at 3 levels: tool calls, script execution, and workflow orchestration — does not cover concurrent programming in application code (use `/deep-review-codebase`)

## Execute

### 1. Identify Parallelizable Operations

> Goal: analyze the operations that can run in parallel

1. Group operations into independent sets — each set has no data dependency between them
2. Identify dependencies: if operation B needs the result of operation A → sequential
3. Identify side effects: if operations share mutable state or a resource → sequential
4. Identify read-only operations: reading files, searching, scanning → can parallelize
5. Identify write operations: editing files, creating files → sequential if they write the same file

### 2. Batch Tool Calls

> Goal: group independent tool calls into a parallel batch

1. Group independent `read_file` calls into one batch — read several files at once
2. Group independent `grep_search` calls into one batch — search several patterns at once
3. Group independent `find_by_name` calls into one batch — search several patterns at once
4. Group independent `run_command` calls into one batch — run commands with no dependency at once
5. If tool call B needs the result of tool call A → split into sequential, don't batch

### 3. Parallel Script Execution

> Goal: use `Promise.all` and `Promise.allSettled` in scripts for parallel data processing

1. Use `Promise.all` when every operation must succeed — if one fails, all fail
2. Use `Promise.allSettled` when you must keep both success and failure results — each operation is independent
3. Use `Bun.$` template literals for parallel shell commands: `await Promise.all([await $\`cmd1\`, await $\`cmd2\`])`
4. Use `Bun.spawn` for parallel subprocesses while capturing exit codes
5. Limit concurrency with a simple pool pattern when operations exceed 10, to avoid consuming all resources

### 4. Parallel Workflow Orchestration

> Goal: run independent workflows in parallel within orchestrator workflows

1. Identify the independent sub-workflows — no data dependency between them
2. Run independent sub-workflows at once, e.g. `/deep-review-codebase`, `/follow-tool-knip`
3. Run dependent sub-workflows sequentially, e.g. `/deep-validate` after `/review-*`
4. Collect results from every sub-workflow before aggregating the report
5. If one sub-workflow finds a critical issue → stop and validate before continuing

### 5. Verify And Report

> Goal: check the results and report

1. Check that every parallel operation returned a result — no operation missing
2. Check errors from `Promise.allSettled` — separate fulfilled and rejected
3. If there are rejected operations → identify the cause and retry, or report
4. Run `/report` to summarize the results as a table
5. Note in the report which operations ran in parallel and how long they took

## Rules

### 1. When To Parallelize

- independent read operations, independent searches, independent scans, independent checks
- operations that don't share mutable state or a resource
- Sequential: operation B needs the result of operation A
- Sequential: operations that write the same file or modify the same state
- Sequential: operations with an ordering requirement, e.g. build before test

### 2. Error Handling

- `Promise.all`: if one rejects, all reject — use when everything must succeed
- `Promise.allSettled`: all complete whether successful or failed — use when you must keep every result
- Check `result.status` for `fulfilled` or `rejected` from `Promise.allSettled`
- If a parallel operation fails → retry once; if it still fails → report and continue or stop per severity
- Don't hide errors from parallel operations — report every failure

### 3. Concurrency Limits

- Limit parallel operations to no more than 10 per batch to avoid consuming all resources
- If operations exceed 10 → split into batches or use a pool pattern
- Use `BUN_CONFIG_MAX_HTTP_REQUESTS` to limit concurrent HTTP requests
- Check the rate limits of external APIs before parallel calls

### 4. Deterministic Guarantees

- The result of parallel execution must match sequential execution — just faster
- Don't rely on the ordering of parallel results — use a key or label to identify each result
- If results must be ordered → sort after collecting, don't rely on execution order
- Parallel execution must not create duplicate side effects — each operation works independently

### 5. High Impact Content

- Always group independent tool calls into parallel batches when possible — reduces context accumulation
- Identify parallelizable tasks in `/plan`
- Use parallel execution in `/run-verify` for lint, typecheck, scan
- Don't parallelize operations that have dependencies without need

- Use /follow-math-concepts if needed

## Expected Outcome

- Independent operations run in parallel, reducing total execution time
- Tool calls are batched, reducing round trips and context accumulation
- Scripts use `Promise.all` and `Promise.allSettled` correctly
- Errors from parallel operations are fully reported
- Deterministic results — parallel and sequential give the same outcome
