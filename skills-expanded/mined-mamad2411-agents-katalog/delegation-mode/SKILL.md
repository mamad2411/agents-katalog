---
name: delegation-mode
description: Use when delegated work must survive a worker, Code Execution interruption, or session boundary and resume from durable plan files.
---

# Delegation Mode

Delegation mode makes the filesystem the source of truth for delegated work.
The chat transcript is useful for progress updates, but it is never the only
handoff. A coordinator creates an executable plan, each worker writes its own
result directly to `.agents/plans/`, and a later session reruns the same plan
with completed task IDs skipped. The reusable runner validates the result file,
not just the worker's response, before it confirms a task.

Use this mode for work that is large, multi-step, parallelizable, likely to
outlive one context window, or valuable as a durable plan for the next agent.
Do not use it for a small interactive answer that has no durable output.

## Source of truth

Use one plan script per run:

```text
.agents/plans/
├── YYYY-MM-DD-<slug>.js              # executable dispatcher and resume state
├── YYYY-MM-DD-<slug>-<task-id>.md    # one durable result per task
└── YYYY-MM-DD-<slug>-FINAL.md        # optional aggregation plan
```

Copy `scripts/delegation-plan.template.js` to the first path and fill in the
project context and task definitions. The script must contain:

- a stable run date and slug;
- a stable, unique ID for every task;
- an exact output path for every task;
- `MODE = "sequential"` or `MODE = "parallel"`;
- `DONE_IDS`, initially empty and updated when resuming;
- an optional final aggregation task controlled by `FINAL_DONE`.

Keep the plan script in `.agents/plans/` so another session can execute the
same file without reconstructing the dispatch logic from chat. Fill in every
placeholder before running it. The plan's `DATE`, `SLUG`, task IDs, and output
paths are part of its identity; create a new slug when the scope changes.

The reusable template loads `scripts/plan-validation-core.js`, which is the
single source for plan identity checks, safe output paths, `DONE_IDS`, Markdown
frontmatter, completion markers, and durable-file validation. The loader checks
the publishable source tree and installed skill tree so a copied plan remains
usable after installation.

## Worker contract

Every delegated worker must:

1. Read the complete task prompt and relevant source files.
2. Stay within its assigned scope and avoid editing application source unless
   the plan explicitly assigns implementation ownership.
3. Write its complete result directly to the exact output path in the prompt.
4. Use Markdown plan frontmatter with `kind: plan`, a meaningful `id`, and a
   truthful `status`. A completed result uses `status: done`; a blocked or
   incomplete result must not claim completion.
5. Include actionable findings, decisions, blockers, or delivered changes.
6. Include the exact `FILE_WRITTEN:` line as the final non-empty line in the
   result file as well as in the response. This makes a result auditable if the
   dispatcher is killed after the worker writes but before its response is
   returned.
7. End its response with exactly:

   ```text
    FILE_WRITTEN: <exact-output-path>
   ```

    The response marker is valid only after the file exists and passes the
    result-file checks. The response marker is a useful liveness signal; the
    file marker is the durable completion signal.

For implementation tasks, the result plan should record what changed, files
affected, verification performed, remaining risks, and the next action. For
analysis tasks, it should record scope, evidence, conclusions, and recommended
work. Empty results are valid when the worker explicitly records that it
checked the scope and found nothing.

## Sequential and parallel dispatch

The default is sequential:

```js
const MODE = "sequential";
```

The runner awaits each pending task before dispatching the next. Use it when:

- tasks may compete for shared resources;
- one task depends on another;
- workers may edit overlapping files;
- the repository or tool budget is constrained;
- predictable failure boundaries are more useful than wall-clock speed.

Use parallel only when all pending tasks are independent:

```js
const MODE = "parallel";
```

Parallel tasks must be read-only with respect to application source, write
different output files, and not depend on another task's result. The runner
uses `Promise.allSettled`, so one failed worker does not hide results from the
others. Aggregation is blocked until every task has a validated result file.
If a task declares `dependsOn`, it must run after those task IDs are confirmed;
parallel mode is valid only when the dependency graph permits independent
dispatch.

Every writable delegated task uses:

```js
config: { $kind: "general" }
```

Do not use an explore-only worker for a task whose completion requires writing a
file. Use specialized worker kinds only when the composition skill explicitly
defines a compatible file-writing contract.

## Resume after interruption

A killed Code Execution run does not invalidate files already written by
workers. Resume from the plan, not from the transcript:

1. Inspect the plan's output files.
2. Confirm each candidate result is complete, has truthful plan frontmatter,
   and contains its exact `FILE_WRITTEN:` marker as the final non-empty line;
   use the worker response as additional confirmation when it is available.
3. Put only confirmed task IDs in `DONE_IDS`. The runner rejects unknown,
   duplicate, or stale IDs and revalidates every listed output file.
4. Rerun the complete `.js` plan.
5. The runner skips `DONE_IDS` and dispatches only missing or unresolved tasks.
6. Run final aggregation only after all task IDs are confirmed.

Do not infer completion from a worker's silence, a partial file, or an old chat
message. If a result file exists but its completion marker or required content
is missing, leave the ID out of `DONE_IDS` and rerun that task. If the review
scope changes, create a new slug instead of reusing old results.

`DONE_IDS` is intentionally explicit rather than inferred by an in-script
filesystem scan. This makes the resume decision auditable and prevents a
truncated or stale file from being treated as complete.

## Composition with larger skills

Delegation mode is an execution layer, not a review methodology. A larger
skill can define its own task list and result schema while using this contract.
For example, `code-review-axes-and-quality`:

- defines ten independent review axes;
- uses one stable task ID and one `.agents/plans/` file per axis;
- supports sequential or parallel dispatch;
- runs a final deduplicating aggregation only after all ten axes confirm.

For hard tasks, decompose the work into tasks with explicit dependencies,
select sequential mode where needed, and make the final task read the earlier
plan files instead of depending on chat context.

## Failure and terminal states

The result file is the durable record. Use these meanings in its frontmatter or
body:

| State | Meaning |
| --- | --- |
| `pending` | Task has not been dispatched. |
| `running` | Work is in progress; partial progress is recorded when useful. |
| `blocked` | A specific missing decision, input, or environment condition prevents safe progress. |
| `done` | The task output is complete and verified. |

Never mark a task `done` merely because most of it is complete. A plan script
should report unresolved tasks and skip final aggregation when any task throws
or lacks its marker.

## Final validation

Before reporting a delegated run complete:

1. Confirm every expected task result exists, is inside `.agents/plans/`, and
   follows its required schema.
2. Confirm every task ID is represented in `DONE_IDS` or was completed in the
   current run.
3. Confirm the final aggregation file exists when the plan defines one, and
   revalidate it before setting `FINAL_DONE = true`.
4. Check links, frontmatter, and `git diff --check`.
5. Run relevant tests, lint, type checks, or builds for implementation work.
6. Record verification and remaining risks in the final plan.

Do not claim approval while unresolved critical blockers remain.

## Included resources

- `scripts/delegation-plan.template.js` — generic resumable dispatcher.
- `references/delegation-modes.md` — mode selection and resume checklist.