---
description: "Nexi Agency's autonomous workflow engine (plan/research/tool/verify/reflect passes over voice dialogue). Use when debugging a stuck, misreporting, or wrongly-gated agency run."
license: "MIT"
---
# Nexi Workflow Dialogue

`engine/agency/workflow_engine.py` is the clean-room (no CrewAI/LangChain)
autonomous workflow layer behind `NEXI_AGENCY_*` env flags. One file = state
+ plan + memory + events + runner, by design (ponytail: pass-functions, not
a class hierarchy).

## Pass pipeline

Planner -> Research -> ToolOperator -> Verifier -> Reflection -> Report,
implemented as `_plan`, `_research`, `_tool_step`, `_verify`, `_reflect`,
`_report_body` in `workflow_engine.py`. Each pass signature is `(run, ctx)` —
upgrade a pass in place rather than restructuring the pipeline.

## Autonomy gating

- `autonomy_enabled()` reads `NEXI_AGENCY_AUTONOMY` (1/true/yes/on) — when
  unset/false, passes use deterministic stubs (safe, offline, test-stable),
  NOT the Gemini brain. If a run "isn't reasoning," check this flag before
  assuming the brain call is broken.
- `autonomy_mode()` reads `NEXI_AGENCY_MODE` (default `supervised`): one of
  `locked | manual | supervised | autonomous_safe`. This is the dial between
  "never runs" and "runs without asking" — check it before assuming a stuck
  run is a bug rather than the intended gate.

## Run lifecycle

- `WorkflowRun` (dataclass) carries `status` (pending → ... → one of
  `_TERMINAL = {completed, failed, cancelled}`), `plan`, `logs`, `events`,
  `artifacts`, `findings` (run-local memory), and `waiting_for` (set when a
  run needs a human decision).
- Runs persist to JSONL at `data/nexi/agency/workflow_runs.jsonl` via
  `_persist(run)` so state survives a process restart — a run that "lost its
  history" usually means this file wasn't written, not that memory was
  cleared.
- `WORKFLOW_TYPES = {router_audit, codebase_research, test_generation,
  integration_plan}` — new workflow types register via
  `register_workflow_type()` with a `WorkflowDefinition(runner, continuer,
  canceller, restart_policy)`.
- `EVENT_SINK` is the HUD hook (`callable(run_id, event_dict)`, no-op by
  default) — if the UI isn't reflecting a run's progress, check this is wired
  to `engine/ui_event_bridge.py`, not that events aren't firing
  (`_publish_event` prints `[NEXI_AGENCY] <run_id> <type> <message>`
  regardless).

## Debugging checklist

- Run stuck in `pending`? Check `autonomy_mode()` before assuming the runner
  crashed — `locked`/`manual` intentionally wait for a human.
- Tool step doing nothing? Tool calls route through `nexi_tool_proxy` +
  approval, same gate as the rest of Nexi (see the safety-gate skill) — not
  a separate agency-only bypass.
- Background execution keeps the voice thread free; a slow pass should never
  block ASR/TTS. If it does, that's the bug, not "agency is just slow."
