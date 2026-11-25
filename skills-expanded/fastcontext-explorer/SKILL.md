---
name: fastcontext-explorer
description: Use Microsoft FastContext as the default read-only code exploration subagent before answering, editing, reviewing, or debugging code you are not already certain about. Trigger when a task requires reading more than one file, tracing logic across modules, locating files/symbols/call paths/tests, mapping dependencies, assessing change impact, or finding where behavior is implemented. Use it instead of manual grep/glob/read chains when broad exploration would consume main-agent context. Do not use for already-read exact files, a single obvious grep in one known file, pure generation tasks with no exploration need, tiny single-file tasks, or non-code questions.
---

# FastContext Explorer

## Workflow

1. Check availability first with the MCP tool `fastcontext_health`.
2. If health is usable, call `fastcontext_explore` with a specific query and the repository root.
3. Treat returned citations as candidate evidence, not proof. Read the cited files and line ranges yourself before editing or answering.
4. If citations are sparse, off-target, or missing, refine the query once with concrete terms from the task, error, subsystem, or nearby filenames.
5. For debugging poor searches, use `fastcontext_explore_with_trace` and inspect the saved trajectory.

## When to Use

- Understand unfamiliar code before editing, reviewing, debugging, or explaining it.
- Trace logic across layers, such as request to handler to service to storage.
- Answer code questions like "How does X work?", "Where is Y defined?", or "What calls Z?".
- Map what a symbol depends on or what depends on it.
- Assess which files are likely affected by a change.

When unsure and the answer needs more than one file, run FastContext first.

## When Not to Use

- You already read the exact file and surrounding context in this session.
- One known file and one obvious search will answer the question.
- The task is pure writing or generation with no repository exploration.
- The task is non-code.

## Query Shape

Write concise exploration requests that name behavior and intent:

```text
Find where OAuth access tokens are refreshed and which tests cover expired token handling.
```

Prefer subsystem and failure language over generic searches:

```text
Locate the request validation path that rejects oversized uploaded files.
```

Avoid asking FastContext to solve or patch:

```text
Fix the upload bug.
```

## MCP Tools

Use `fastcontext_explore`:

```json
{
  "repo_path": "/absolute/path/to/repo",
  "query": "Locate the request validation path that rejects oversized uploaded files.",
  "max_turns": 6,
  "citation": true
}
```

Use `fastcontext_explore_with_trace` when a trajectory is needed:

```json
{
  "repo_path": "/absolute/path/to/repo",
  "query": "Find where CLI config files are loaded and validated.",
  "max_turns": 8,
  "trajectory_path": ".fastcontext/trajectory.jsonl"
}
```

## Interpreting Results

FastContext normally returns a `<final_answer>` citation block such as:

```text
src/router.py:42-58
tests/test_router.py:101-119
```

After receiving citations:

- Read the cited ranges and surrounding context.
- Verify that the cited code actually controls the requested behavior.
- Search locally if the citations reveal a symbol but not all call sites.
- Keep FastContext outputs out of final answers unless the user asked about the exploration itself.

## Failure Handling

If `fastcontext_health` reports that `fastcontext.cli` is unavailable, reinstall `fastcontext-agent-tools`; Microsoft FastContext is included as a package dependency.

If `BASE_URL` or `MODEL` is missing, ask the user to configure the FastContext endpoint.

If `repo_path` is rejected, use a path under `FASTCONTEXT_ALLOWED_ROOTS` or ask the user to update that allowlist.

If FastContext times out, retry once with a narrower query or lower `max_turns`.
