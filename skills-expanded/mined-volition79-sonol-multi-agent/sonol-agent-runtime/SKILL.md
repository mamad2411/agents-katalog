---
name: sonol-agent-runtime
description: Sonol runtime helper skill for sub-agents participating in Sonol multi-agent orchestration. Use when a sub-agent must report progress, artifacts, completion, or session status into the shared dashboard and SQLite-backed run history.
---

# sonol-agent-runtime

This skill is for sub-agents, not for top-level orchestration.

Use it when a sub-agent is operating inside a Sonol multi-agent run and must
report state in a standard way.

This skill is a reporting and coordination overlay inside the current Sonol
subagent workflow. It does not provide a low-level provider thread control API.
Direct `report-*` helper scripts are the current default path, and JSON ingest
is the adapter-neutral fallback path. Do not rely on hooks or final-answer JSON
scraping for normal operation.

Even when `sonol-multi-agent` uses a hosted planner, runtime reporting
still belongs to the local Sonol DB and dashboard. Do not replace normal
`report-*` calls with ad-hoc remote HTTP logging.

## Required Inputs

The sub-agent should know:

- `plan_id`
- `run_id`
- `agent_id`
- `task_id`
- `purpose`
- `depends_on`
- `read_paths`
- `write_paths`
- `deny_paths`
- the current database path when overridden

## Required Reports

- `progress_event` at task start and major milestones
- `artifact_event` when a meaningful output is produced
- `completion_event` when the task ends
- `session_updated` when the sub-agent becomes `blocked` or `idle`
  - sub-agent reporting requires `agent_id`
  - use `completion_event` rather than `session_updated completed` for normal success

## Quick Commands

- Progress:
  - `node $SONOL_INSTALL_ROOT/skills/sonol-agent-runtime/scripts/report-progress.mjs --db <db_path> --plan-id <plan_id> --run-id <run_id> --agent-id <agent_id> --task-id <task_id> --step-index 1 --total-steps 3 --state running --message "조명 조정 시작" --detail "노을 톤을 먼저 맞추고 있습니다. 하늘과 바다 색을 함께 정리합니다."`
- Artifact:
  - `node $SONOL_INSTALL_ROOT/skills/sonol-agent-runtime/scripts/report-artifact.mjs --db <db_path> --plan-id <plan_id> --run-id <run_id> --agent-id <agent_id> --task-id <task_id> --artifact-type file --artifact-ref path/to/file --summary "풍경 파일 추가" --detail "새 풍경 레이어를 기록했습니다. 다음은 카메라 감각을 맞춥니다." --validation-status unchecked`
- Completion:
  - `node $SONOL_INSTALL_ROOT/skills/sonol-agent-runtime/scripts/report-completion.mjs --db <db_path> --plan-id <plan_id> --run-id <run_id> --agent-id <agent_id> --task-id <task_id> --result success --summary "풍경 보강 완료" --detail "하늘, 바다, 원경 능선을 한 흐름으로 맞췄습니다. 이제 검증 단계로 넘깁니다." --blockers "" --next-actions "handoff"`
- Session:
  - `node $SONOL_INSTALL_ROOT/skills/sonol-agent-runtime/scripts/report-session.mjs --db <db_path> --plan-id <plan_id> --run-id <run_id> --agent-id <agent_id> --task-id <task_id> --status blocked --message "선행 결과 대기" --detail "의존 작업 결과가 있어야 다음 수정을 이어갈 수 있습니다. 준비되는 즉시 다시 시작합니다." --blocked-reason "Dependency result not ready"`
- JSON ingest fallback:
  - `printf '%s\n' '{"event_type":"session_updated","payload":{"event_id":"example","schema_version":"1.0.0","plan_id":"<plan_id>","run_id":"<run_id>","agent_id":"<agent_id>","task_id":"<task_id>","status":"blocked","message":"waiting on dependency","blocked_reason":"Dependency result not ready","timestamp":"<iso>"}}' | node $SONOL_INSTALL_ROOT/skills/sonol-agent-runtime/scripts/ingest-json-report.mjs --db <db_path> --plan-id <plan_id> --run-id <run_id> --agent-id <agent_id>`
- Diagnostics:
  - `node $SONOL_INSTALL_ROOT/skills/sonol-multi-agent/scripts/show-run-diagnostics.mjs --run-id <run_id> --db <db_path>`

## Rules

- Use schema version `1.0.0`.
- Do not invent new event shapes.
- Every runtime report must carry the exact `plan_id` that came with the
  current dashboard-approved run packet.
- Sonol v1 runtime supports one active task per agent. Do not report multiple
  concurrent task ids for the same agent.
- Prefer direct `report-*` helper script calls while working.
- When a generated run-scoped prompt file or command file exists, treat it as
  authoritative. Do not manually retype or simplify the command flags.
- In particular, do not omit `--db` when the generated command includes it.
  Reconstructed commands can silently point at the wrong SQLite file.
- If local helper commands are unavailable in the current provider runtime, use
  `ingest-json-report.mjs` with the same identifiers and schema fields.
- `task_id` is required for `progress_event`, `artifact_event`, and
  `completion_event`.
- `task_id` is optional for `session_updated`, but include it when the current
  task is known.
- Emit the first `progress_event` immediately when the task actually starts.
- After that, report each meaningful small work unit instead of waiting only for large milestones.
- If the current assigned unit is finished and there is no immediate next action,
  emit `session_updated --status idle`.
- Use `session_updated` for `blocked` or `idle`.
- Use `completion_event` for normal success or failure.
- Keep `message`, `summary`, and `blocked_reason` short and factual.
- Use `message` as a short headline.
- When useful, also send `detail` as `1` to `3` short sentences explaining what
  changed, what file or area is involved, and what happens next.
- Avoid generic lines like `working`, `step 1`, or `integrating`.
- Prefer concrete lines like `폭포 협곡 레이어를 추가했습니다. 물 안개와 원경 능선을 함께 맞추고 있습니다.`
- Treat the generated runtime context files as the source for long instructions;
  do not restate them in full inside normal reports.
- If blocked, include a clear reason in the message and `--blocked-reason` when possible.
- If a file or artifact matters to later agents, emit an `artifact_event`.
- Typical small work units:
  - opened and confirmed the target files
  - created or edited a meaningful file
  - changed a scene/system/module
  - finished a validation or test step
  - handed work to the next role
- Use `idle` only for “current unit done, waiting for next instruction”.
- Use `queued` only before the first real task start.
- Use `blocked` when a concrete dependency or missing input is preventing progress.
- If you do not emit the first runtime report after your turn becomes available,
  Sonol may automatically mark your agent as blocked for missing runtime reports.
  In manifest-only adapters, that safeguard starts after launch acknowledgement
  or another first agent session event makes the agent look live in the DB.
- Emit completion before yielding final task output to the Main Agent.
- If you need new instructions, raise that through `session_updated` or normal
  Main Agent follow-up. Do not assume external text will be injected directly
  into your thread.
- Every `report-*` call also writes a structured log line to
  the Sonol log directory, typically `<data_dir>/logs/sonol-runtime-YYYY-MM-DD.jsonl`.
- Treat Sonol path rules as hard coordination boundaries even when Codex itself
  is not providing native path ACL enforcement.
- Receive new steering through the normal main conversation or `/agent`, not
  through dashboard push messages.
- Do not assume peer-to-peer sub-agent messaging exists.
- Do not spawn child sub-agents in v1.

## What This Skill Can And Cannot Do

This skill can:

- make sub-agent progress visible in the dashboard
- standardize blocked reasons and completion summaries
- persist artifacts and state transitions in SQLite
- improve coordination discipline across parallel work

This skill cannot by itself:

- spawn or terminate a provider sub-agent
- inject text into a provider thread
- override provider approval UX
- enforce native file ACLs inside the host agent runtime

## References

- Read [references/reporting-contract.md](references/reporting-contract.md) for field meanings.
- Read [references/subagent-checklist.md](references/subagent-checklist.md) for the required reporting sequence.
