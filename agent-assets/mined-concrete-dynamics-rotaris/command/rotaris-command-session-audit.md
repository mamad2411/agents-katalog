---
description: Audit Rotaris run logs in .rotaris/sessions and report ranked, evidence-backed optimization points
argument-hint: "[latest | all | <session-id> | last:<N>] [focus: cost|latency|errors|delegation|context|permissions|verifier]"
allowed-tools: Read, Glob, Grep, Bash(rtk *), Bash(uv run *), Write, Edit
---

# Rotaris session audit

Audit real run telemetry under `.rotaris/` and produce a ranked list of concrete
optimization points, each anchored to evidence from the logs and to the code or
config that would change.

Arguments: `$ARGUMENTS`
(empty → audit the 5 most recent sessions; `latest` → newest only; `all` → every
session; `last:N` → N newest; a bare session id → just that one; a trailing
`focus: <theme>` narrows the finding categories.)

## Scope

Read-only over these paths. Do not modify, delete, or rerun anything under
`.rotaris/sessions/`, `.rotaris/worktrees/`, or `.rotaris/litellm_cache/`.

```
.rotaris/agents.yaml                        # runtime knobs — the main tuning surface
.rotaris/sessions/<id>/metadata.json        # status, worktree, task title, schema_version
.rotaris/sessions/<id>/summary.md           # per-agent rollup, warnings, slowest tools
.rotaris/sessions/<id>/metrics.json         # the numbers (fields below)
.rotaris/sessions/<id>/issues.json          # structured issues with kind/actor/evidence_ref
.rotaris/sessions/<id>/timeline.jsonl       # ordered lifecycle events (types below)
.rotaris/sessions/<id>/evidence/*.jsonl     # tool-calls, permissions, events, model-input,
                                            #   context-selection, report-validation, memory
.rotaris/sessions/<id>/artifacts/           # published artifacts + index.json
.rotaris/sessions/<id>/state/               # resume.json, run_config.json, ui_transcript.json
.rotaris/improvement_artifacts/*.json       # prior proposals + history/ (do not repeat these)
```

## Method

1. **Never bulk-read the big blobs.** `state/ui_transcript.json`,
   `state/run_config.json` and `evidence/tool-calls.jsonl` run to hundreds of KB
   or MB. Extract from them with a script, never with `Read`.
2. Write throwaway analysis scripts into the session scratchpad directory and run
   them with `uv run python <script>.py > <out>.txt`, then read the output file.
   Redirect to a file rather than piping — piping through the uv trampoline is
   unreliable on this machine.
3. Aggregate **across** sessions first (counts, medians, top-N), then drill into
   the two or three worst offenders for concrete excerpts.
4. Cross-check the prior `improvement_artifacts/` proposals. A finding already
   proposed there is only worth reporting if it recurred after the proposal date —
   say so explicitly and cite both.
5. When a finding implicates code, locate it with tokensave (`tokensave_context`,
   `tokensave_search`, `tokensave_callers`) — not with an Explore agent — and cite
   `path:line`. Prefix shell commands with `rtk`.

## Signals to mine

**`metrics.json` fields:** `global_tool_call_count`, `global_token_usage`
(`prompt_tokens`, `completion_tokens`, `cache_read_tokens`, `cache_write_tokens`,
`reasoning_tokens`), `global_cost`, `global_compressions`, `agents` (per-agent
`tool_calls` histogram, tokens, cost, `last_prompt_tokens`), `tool_call_records`,
`tool_outcomes`, `terminal_shell_failures`, `terminal_suspicious_successes`,
`terminal_timeouts`, `slowest_tools`, `model_input_records`,
`stale_system_messages_dropped`, `stale_tool_descriptions_dropped`,
`context_selection_records`, `artifact_injected_count`, `artifact_elided_count`,
`report_validation_records`, `report_validation_downgrades`,
`permission_decision_records`, `permission_denials`, `permissions_by_decision`,
`permissions_by_source`, `permission_mode_changes`, `issue_count`, `issues_by_kind`.

**`issues.json` kinds seen in this repo:** `tool_error`, `terminal_shell_failure`,
`child_exception`, `terminal_timeout`, `child_force_cancelled`,
`terminal_suspicious_success`, `permission_denied`, `incomplete_execution`,
`circuit_breaker_escalation`, `stall`.

**`timeline.jsonl` types:** `intent_classified`, `iteration_start`, `iteration_end`,
`child_start`, `child_result`, `child_end`, `child_conversation_closed`,
`artifact_published`, `completion_gate_decision`, `verifier_run_skipped`,
`verifier_run_completed`, `permission_approved`, `permission_mode_changed`,
`checkpoint_created`, `issue`.

Hunt specifically for:

- **Repeated failure modes** — the same `tool_name` erroring across sessions or
  actors (e.g. a tool that is misconfigured, not a one-off). Group by
  `tool_name` × `actor` × `failure_kind`, not by raw count.
- **Wasted work** — identical or near-identical tool calls repeated inside one
  agent; re-reading files already in context; re-exploring after a handoff.
- **Token and cost shape** — cache read vs prompt token ratio (low cache reuse =
  prompt churn), cost concentrated in one agent or one persona, large-model slots
  doing work a small model could do (`agents.yaml` `large_model` / `medium_model` /
  `small_model` and per-persona overrides).
- **Latency** — `slowest_tools`, long `elapsed_s` in `child_result`, stalls near
  `stall_timeout_s`, children hitting `timeout_s` or `child_force_cancelled`.
- **Loop health** — iterations that end with no artifact and no edit, recovery
  prompts with no follow-through, `completion_gate_decision` rejections,
  `circuit_breaker_escalation`, `incomplete_execution`, sessions whose stop reason
  is not a clean completion.
- **Delegation shape** — fan-out vs `max_active_children`, depth vs `max_depth`,
  children that produce nothing, orchestrator turns spent on non-delegating tools.
- **Context handling** — `artifact_elided_count`, dropped stale system messages or
  tool descriptions, compressions and where they land relative to
  `compressor.threshold_percentage`.
- **Permissions** — denials, `permission_mode_changed` mid-run, rules resolving to
  `preset:autonomous` fallback for tools that deserve an explicit rule.
- **Verifier** — `verifier_run_skipped` reasons, checks that time out against
  `verifier.suite_timeout` or their own `timeout`, advisory checks that always fail.
- **Measurement gaps** — buckets like `tool_outcomes: unknown` that make other
  metrics untrustworthy. Flag these as measurement findings, not run bugs. Note
  that sessions written before SWR-2911 have a `tool_outcomes` histogram where
  every non-terminal call reads `unknown`; recompute it from
  `evidence/tool-calls.jsonl` rather than trusting the stored value.

## Output

Print a report to chat, ranked by expected payoff:

```
## Session audit — <N> sessions, <date range>

<3-6 line orientation: totals, cost, issue counts, the through-line>

### 1. <finding title>  ·  impact: high|med|low  ·  effort: S|M|L
Category: <one of documentation_update | agents_md_update | workspace_note |
config_change | tool_enablement | dependency_install |
persona_or_prompt_adjustment | persona_memory_update | preflight_check>
What the logs show: <specific, quantified>
Evidence: <session-id>/issues.json#<issue-id>, timeline @<ts>, metrics.<field>=<value>
Where to fix: <path:line or .rotaris/agents.yaml key>
Fix: <one concrete change>
Risk: low|medium|high

### 2. ...

### Not worth acting on
<signals that look bad but are explained — say why, briefly>

### Already proposed
<matches in .rotaris/improvement_artifacts/ — artifact id, whether it recurred>
```

Rules for the report:

- Every finding carries at least one hard number and one file-anchored reference.
  No finding may rest on intuition; if the logs do not support it, drop it.
- Distinguish "this run was interrupted by the user" from "the system failed".
  Sessions with `stop reason: interrupted by user` are weak evidence for loop bugs.
- Prefer few strong findings over a long list. Five well-evidenced items beat twenty.
- State sample size and its limits — a signal from one session is a hypothesis.

## After the report

Stop there by default. Apply nothing.

If the invocation includes `--write`, additionally save the report to
`.tmp/session-audit-<YYYYMMDD-HHMM>.md`. If it includes `--swr`, draft requirement
files for the top findings under the matching `docs/requirements/<area>/` directory
following `docs/requirements/README.md` (improvement-loop findings → `1600-improvement-loop/`,
diagnostics → `1500-sessions-diagnostics/`, safeguards → `900-runtime-safeguards/`),
and list the SWR ids you created. Never edit `.rotaris/agents.yaml` or any persona
config as part of this command — propose the diff in the report and let the user decide.
