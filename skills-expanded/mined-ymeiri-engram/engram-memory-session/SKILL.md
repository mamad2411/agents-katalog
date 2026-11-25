<!-- engram:harness-adapter:v1 -->
---
name: engram-memory-session
description: Use when Cursor Agent is working in a repo or project with persistent Engram memory, especially at task start, before major decisions, before final responses, or when commit preferences may matter.
---
# Engram Memory Session

Use this skill when Cursor Agent is working in a repository or project with persistent Engram memory.

Workflow (soft):
- Start by calling the Engram MCP `orient` tool with current cwd, prompt, `agent=cursor`, and
  `response_shape="lean"`; supply project only when its canonical identity is known.
- Pass `task=<exact task name or tracker key>` to `orient` when task identity is known; task names require an explicit project. If task identity or its project relationship cannot be resolved, ask instead of applying task-scoped memory.
- Treat JIRA keys, PRs/issues, known entities/services, project-state claims, final responses, and durable discoveries as concrete Engram triggers.
- Treat the returned memory cursor as the baseline for this turn.
- Keep the returned `trace_id` from `orient` or `search`; before final response, call
  `telemetry(action=submit_feedback)` with `task_success`, `preference_adhered`,
  `repeated_context_questions`, `bad_memory_used`, `missing_context`, `used_memory_ids`, and
  `rejected_memory_ids`, plus `stale_memory_ids` and `wrong_scope_memory_ids` when those
  outcomes or attribution judgments can be made. Use `used_memory_ids` for returned memory that
  shaped the answer, implementation, safety decision, or plan; leave it empty only when no returned
  memory influenced behavior.
- Before a major decision or final response, call `memory(action=changes_since,
  commit_id=<memory_cursor.commit_id>, timestamp=<memory_cursor.timestamp>,
  scope={relevance_mode:"related", project:..., cwd:...})`.
- Record source-grounded discoveries, decisions, rules, preferences, limitations, and handoffs.
- When the current method, plan, or next action should survive resume, use
  `memory(action=capture_current_plan)` with compact content and file/tool/manual-review evidence.
- Use `obligations(action=detect, project=..., cwd=...)` when documents change, tools fail,
  or source/design reading is needed; before final response, run
  `obligations(action=doctor, scope={relevance_mode:"related", project:..., cwd:...})` and resolve or explicitly skip open
  obligations.
- Before context compaction or any expected context loss, update `handoff` and record or commit
  compact durable memory for the next session.
- Use writer provenance with `writer_harness=cursor` when writing durable memory.
- For commit messages, check memory for user/project commit preferences first.
- If handoff or durable memory changes are needed, use `handoff` and `memory(action=commit)`.

This uses the soft profile. Missing lifecycle steps should be reported as warnings, not blockers.
