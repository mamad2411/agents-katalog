<!-- engram:harness-adapter:v1 -->
---
name: engram-resume-session
description: Use when Cursor Agent resumes, continues, or loads prior project context from Engram memory and rolling handoffs.
---
# Engram Resume Session

Use this skill when the user asks Cursor Agent to continue, resume, or load prior Engram context.

Steps:
- Call the Engram MCP `orient` tool with `response_shape="lean"` before reading broad files.
- Pass `task=<exact task name or tracker key>` to `orient` when task identity is known; task names require an explicit project. If task identity or its project relationship cannot be resolved, ask instead of applying task-scoped memory.
- Inspect project/repository resolution and ask only if ambiguity cannot be resolved.
- Keep returned `trace_id` values from `orient` or `search`; submit telemetry feedback with
  outcome, gap, and attribution fields before final response when memory quality can be judged.
  Include `used_memory_ids` for returned memory that shaped behavior and `rejected_memory_ids` for
  returned memory considered but not used. Include `stale_memory_ids` and
  `wrong_scope_memory_ids` for rejected memory specifically judged stale or out of scope.
- Use `handoff(action=get, scope={relevance_mode:"related", project:..., cwd:...})` when available.
- Poll `memory(action=changes_since, commit_id=<memory_cursor.commit_id>,
  timestamp=<memory_cursor.timestamp>, scope={relevance_mode:"related", project:..., cwd:...})` before major decisions
  and final response.
- Poll `obligations(action=detect)` and close or explicitly skip open obligations before final
  response.
- Store compact, evidenced memory if the session discovered something future agents need.
- Use `memory(action=capture_current_plan)` for compact current method, plan, or next-action
  guidance that should surface on the next resume.
- If resuming after compaction, read `handoff(action=get, scope={relevance_mode:"related", project:..., cwd:...})` and
  recent `memory(action=changes_since, commit_id=<memory_cursor.commit_id>,
  timestamp=<memory_cursor.timestamp>, scope={relevance_mode:"related", project:..., cwd:...})` before continuing.
- Use writer provenance with `writer_harness=cursor` for durable memory writes.
