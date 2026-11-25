---
name: workflow-review
description: Explain, test, simplify, and improve an existing workflow. Use when reviewing behavior, finding edge cases or failure points, validating sample data, or improving reliability, clarity, and performance.
license: Apache-2.0
compatibility: Tines 3B
---

# Workflow review

Read the workflow files and recent execution evidence before proposing changes.

When the workflow uses named volumes or filesystem-backed state, use `workflow-volume-design` and inspect volume declarations, actual usage, and the steps on the common request path.

Review the workflow as one program:

1. Explain its trigger, data flow, side effects, and result.
2. Test representative success, empty, malformed, duplicate, and dependency-failure inputs.
3. Identify failures that can be handled locally and failures that must remain visible.
4. Remove redundant work and simplify boundaries before adding retries or branches.
5. Run affected steps and tests after changes.

For volume-backed workflows, check that frequent requests do not scan growing directories, mount unrelated state, or start unnecessary downstream executions. Check that every pair of writers to the same file is safe when one loses a volume conflict, that request steps report pending rather than success for writes that can still lose, that writers select bounded batches before scanning or parsing, retain input until derived changes are durable, and drain pending work under sustained input. Compare request latency, waiting executions, oldest pending age, and volume usage before and after a change.

Prioritize concrete issues supported by code or execution results. Preserve intentional behavior, and do not add logging, retries, or abstractions without a specific failure they address.
