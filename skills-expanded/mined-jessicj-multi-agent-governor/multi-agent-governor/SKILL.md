---
name: multi-agent-governor
description: Plan, record, or execute evidence-based homogeneous Agent scaling. Start with one measured Agent, decide whether to admit another, preserve append-only advisory checkpoints for externally executed tasks, select centralized or independent collaboration, enforce supported runtime budgets, and stop when verified marginal value is too low. Use when a user asks whether multi-agent work is worthwhile, requests an auditable advisory Agent session or adaptive code-review run, wants an Agent budget, or asks whether another Agent justifies its coordination and token cost.
---

# Multi-Agent Governor

Treat multi-agent use as an evidence-based admission decision, not a default.
The product is a budget controller for verifiable code review, not an oracle
for a universally correct Agent count. Treat the user's Agent cap as a safety
boundary, not evidence that the cap is sufficient.
The deterministic core has three modes:

- `plan`: return an advisory decision from a measured external baseline.
- `advisory`: record externally executed Agents and replay policy checkpoints
  without claiming runtime enforcement.
- `run`: let the Governor-owned runtime execute the baseline and admit one
  additional homogeneous Agent at each checkpoint.

The first executable verifier is intentionally limited to structured code
review. For other task types, use `plan` until a task-specific external
verifier exists.

## Advisory workflow

1. Record the user's available total-agent cap. Count the original baseline
   Agent in that total.
2. Run or inspect exactly one single-Agent baseline before recommending
   scale-out. If no baseline exists, label any answer preliminary.
3. Derive task signals from observable structure and verifier evidence. Never
   use the model's self-reported confidence as baseline confidence.
4. Read [references/input-schema.md](references/input-schema.md) when creating
   the policy JSON.
5. Run:

   ```bash
   python3 scripts/run_governor.py plan INPUT.json
   ```

6. Explain `mode`, `total_agents`, `stop_reason`, expected quality, expected
   cost multiplier, and the strongest two reasons in plain language.
7. If `mode` is not `single`, admit only the next Agent. After it returns,
   compare verified quality, coverage, unresolved conflicts, novel evidence,
   and actual cost before admitting another.
8. When the user asks to execute or audit an advisory multi-Agent task, read
   [references/advisory-session-schema.md](references/advisory-session-schema.md).
   Create the receipt before the first additional Agent:

   ```bash
   python3 scripts/run_governor.py advisory start INPUT.json \
     --events SESSION.events.jsonl
   ```

9. Append exactly one checkpoint after each external Agent, then follow only
   the receipt's next one-Agent admission:

   ```bash
   python3 scripts/run_governor.py advisory checkpoint \
     SESSION.events.jsonl CHECKPOINT.json
   ```

10. Use `null`, not zero, for unavailable usage or timing. Finish by running:

   ```bash
   python3 scripts/run_governor.py advisory report SESSION.events.jsonl
   ```

An advisory receipt keeps the forecast stop separate from the observed final
stop. It remains caller-supplied evidence and must say `runtime_enforced:
false`.

## Executable code-review workflow

Only use this workflow when the user explicitly asks the Governor to execute
the review, the task can be isolated in one working directory, and `codex exec`
is installed and authenticated.

1. Read [references/runtime-schema.md](references/runtime-schema.md).
2. Put the exact supported `policy.version`, review instructions, structural
   signals, changed files, high-risk files, budgets, and Codex runtime
   configuration in one run JSON file.
3. Keep truth cards, hidden tests, previous Agent output, and the event log
   outside the Agent working directory.
4. Ensure every extra Agent is launched by `magov run`; do not also use the
   surrounding session's native sub-Agent controls for the same run.
5. Run:

   ```bash
   python3 scripts/run_governor.py run RUN.json \
     --events RUN.events.jsonl > RUN.report.json
   ```

6. Inspect `actual_total_agents`, `stop_reason`, `verification`, `usage`,
   `checkpoints`, and `receipts`. A process-coverage score is not hidden-truth
   correctness.
7. Use `replay` for an interrupted run log and `report` to summarize completed
   report JSON files.

## Guardrails

- Preserve a forced single-Agent baseline.
- Reject unknown or mismatched policy versions; never silently fall back.
- Under `pilot-v2`, count independent replication as a separable code-review
  unit and require one independent review before an unverified review may stop,
  including single-file reviews, unless a budget blocks admission.
- Treat `total_agents` as including the baseline Agent.
- Respect the user's cap even when the policy proposes more Agents.
- Under `pilot-v2`, treat the initial planned Agent count as a forecast. Admit
  beyond it one Agent at a time when live non-truth evidence remains valuable,
  but never exceed the user or resource cap.
- Prefer two Agents as the first real scale-out step; add later Agents one at
  a time.
- Use `centralized` when shared constraints or failure impact require one
  coherent result. The executable review mode uses deterministic JSON
  aggregation; another runtime must count and measure a model coordinator if
  it launches one.
- Use `independent` when work units and evidence can stay isolated until final
  aggregation.
- Stop when verified coverage is complete, no unresolved conflict remains,
  and the newest Agent contributes little novel evidence.
- Also stop at the quality target, user cap, cost cap, or an observed
  marginal-value plateau. Preserve the planned-cap stop only for historical
  `pilot-v1` compatibility.
- If the user cap is reached before the observable target or plateau condition,
  return `cap_reached_incomplete` with an incomplete run. Never describe that
  outcome as enough Agents or completed verification.
- The executable runtime must own admission. A prose recommendation that the
  surrounding runtime may ignore is advisory mode, not enforced control.
- Advisory checkpoints must increment the total Agent count by one, use unique
  Agent IDs, preserve a homogeneous known model, and include non-policy
  observable evidence. Never rewrite missing usage as zero.
- Never place Codex JSONL artifacts inside the Agent workspace; later Agents
  must not read earlier traces.
- Keep native Codex multi-agent tools disabled inside every Governor-owned
  `codex exec` process so `actual_total_agents` remains auditable.
- Never pass `--dangerously-bypass-approvals-and-sandbox` or an equivalent
  unrestricted execution option through the runtime adapter.
- Do not claim that the current default weights are universally optimal. Refer
  to them as an experimental, inspectable policy.

## Result boundary

In plan-only mode, return a decision receipt and suggested checkpoint. In an
externally executed advisory task, return the replayed append-only session
receipt and its explicit limitations. In executable code-review mode, return
the runtime report and replayable event log. Do not claim effectiveness until
an unseen evaluation set passes the predeclared quality and total-usage
guardrails.
