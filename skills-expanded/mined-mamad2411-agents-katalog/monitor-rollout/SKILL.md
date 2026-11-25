---
name: monitor-rollout
description: "Runs a change-monitoring plan in the foreground of the current coding-agent session: polls each environment's deploy system for the rollout, runs each checkpoint against the indicators with per-environment grouping, applies evidence-discipline (≥24h baseline + same-time-of-day prior + analytical reason + variance test), and emits per-env progress reports inline. Sleeps between checkpoints via a background bash sleep + notification. On the first issue detected in any environment, hands off into plan mode so the same session pivots to fixing it (sequential single-issue mode). Use when a deploy has been triggered, the user merged a PR and wants production watched, doing post-deploy validation, watching a canary, or babysitting a multi-environment rollout — even when they don't say 'execute the plan'. Reads a plan produced by plan-rollout."
argument-hint: "<path to monitoring-plan file or section>"
---

# monitor-rollout

Runs a change-monitoring plan inline in the current coding-agent session. Foreground, single-issue, multi-environment.

## When to use

Only after a monitoring plan exists and the change has been merged or is about to deploy. Specifically:
- The user just merged a PR and wants production watched.
- The user is doing post-deploy validation, watching a canary, or babysitting a rollout.
- The user pasted a path to a monitoring plan file.
- The user invoked this directly from `rollout` after the planning phase.

This skill **runs in the main session**, not as a background subagent. The user wants to *see* the polling and the checkpoints happen — visibility is the UX. Between checkpoints, the skill kicks off a background `sleep_until.sh` that emits a `[RESUME …]` notification at the next checkpoint time; the agent reads the notification and resumes the loop.

## Operation contract

Input: path to a monitoring plan file produced by `plan-rollout`. The plan section's structure is documented in `plan-rollout/assets/monitoring-plan-template.md`.

Lifecycle: stays in the main session for the entire monitoring window. Each checkpoint is a sequence of tool calls; the user reads the resulting status report inline as a normal assistant message. After emitting a checkpoint report (and verifying no terminal condition was reached), the skill invokes `bash monitor-rollout/scripts/sleep_until.sh <abs-time> <plan-path> <offset>` via the `Bash` tool with `run_in_background: true`. When the sleep completes the script echoes a `[RESUME …]` line, which arrives in the agent's chat as a notification — the agent picks it up and resumes the next checkpoint.

If the plan defaults to `.rollout/<branch>-monitoring-plan.md` and the user invoked this skill without a plan-path argument, search for matching files there and surface the most recent one (see Workflow step 2).

Reference docs: [references/checkpoint-loop.md](references/checkpoint-loop.md), [references/multi-env-execution.md](references/multi-env-execution.md), [references/evidence-discipline.md](references/evidence-discipline.md), [references/status-report-formats.md](references/status-report-formats.md), [references/failure-modes.md](references/failure-modes.md), [references/deploy-detection-recipes.md](references/deploy-detection-recipes.md), [references/plan-mode-handoff.md](references/plan-mode-handoff.md), [references/limitations.md](references/limitations.md).

## Single-issue mode

The session is dedicated to *one* change at a time: ship → monitor → if regression, fix → re-monitor.

The plan may list N environments; the executor monitors all of them in parallel. But on the **first** environment to surface a regression (after the evidence-discipline gate), the executor:
1. Emits an `ISSUE_DETECTED` status report including the plan's rollback hint verbatim.
2. Calls `EnterPlanMode` with a seed plan derived from [references/plan-mode-handoff.md](references/plan-mode-handoff.md) — the seed names the regressed environment, the failing indicator(s), the evidence summary, and the rollback hint.
3. Pauses monitoring across all envs. Other envs that may also be in trouble are noted in the report ("staging also showing latency anomaly, deferred until current fix lands") but not separately handed off.
4. Yields. The session is now in plan mode focused on fixing the one regression.

After the fix is shipped, the user re-invokes `/monitor-rollout` against the same plan; any still-present issue in another env triggers the next handoff.

Multi-issue parallelism (separate fix sessions per regression) is **not** supported. See [references/limitations.md](references/limitations.md).

## State machine

```
                        per environment:
POLLING_FOR_DEPLOY ──(deploy detected)──▶ CHECKING ──(checkpoint due)──▶ run indicators
                                                  │                              │
                                                  ◀─(record + sleep_until.sh bg)─┘
                                                  │
                                                  ├─(regressed, evidence ok)─▶ ISSUE_DETECTED
                                                  ├─(intended confirmed)     ─▶ stays CHECKING (mark)
                                                  └─(final checkpoint clean) ─▶ COMPLETED
                                                                          per env

aggregate plan state = first env to ISSUE_DETECTED wins → EnterPlanMode
                       all envs COMPLETED              → plan COMPLETED
                       any env FATAL_ERROR             → plan FATAL_ERROR
```

Details in [references/checkpoint-loop.md](references/checkpoint-loop.md).

## Workflow

Copy this checklist into the response and tick items off as the monitoring window progresses:

```
monitor-rollout progress:
- [ ] 1. Parsed plan (tier, indicators, schedule, deploy-detection per env, rollback)
- [ ] 2. Companion check (plan exists; if not, point at rollout umbrella for post-merge-no-plan flow)
- [ ] 3. Polling each env for deploy start (30s cadence)
- [ ] 4. DEPLOY_DETECTED for env X — recorded deploy_time, started bg sleep_until for +10m
- [ ] 5. (repeat 4 per env as it deploys)
- [ ] 6. Checkpoint @ +Xm — ran indicators with GROUP BY env, applied evidence discipline, emitted per-env table
- [ ] 7. (repeat 6 per checkpoint)
- [ ] 8. Terminal: COMPLETED (all envs no issue) | first ISSUE_DETECTED → EnterPlanMode | FATAL_ERROR
```

### 1. Parse the plan

Read the plan file. Extract:
- Risk tier and rollback hint (preserve verbatim — do not paraphrase the rollback line).
- Checkpoint schedule.
- Environment list with per-env deploy-detection commands.
- Indicators table with kind, source, baseline, threshold, direction, scope.

If the plan parse fails (missing required fields, malformed table), emit a `FATAL_ERROR` status block per [references/failure-modes.md](references/failure-modes.md) and stop. Do not proceed with a partial plan.

### 2. Companion check + plan discovery

If the user invoked this skill **without** a plan path argument:
1. Search for `.rollout/*-monitoring-plan.md` (relative to the git root). If exactly one match, surface it: *"Use plan at `<path>`? Y/n"*. If multiple, list them sorted by mtime and ask the user to pick.
2. If no `.rollout/*-monitoring-plan.md` exists, this is the post-merge-no-plan case. Stop and point the user at the umbrella: *"No plan found in `.rollout/`. Run `/rollout` to enter the post-merge-no-plan flow — it'll synthesize a plan from the merged change first, then chain into me."*

The plan is the input contract; running monitor-rollout without one would have nothing to anchor evidence-discipline against.

### 3. Poll for deploy start (per env)

For each environment in the plan, run its deploy-detection command. The plan's `Deploy detection` block names a script — common cases:
- `scripts/poll_github_actions.sh <workflow> <branch> <sha> [matrix-key]`
- `scripts/poll_buildkite.sh <pipeline> <branch> <sha> [step-key]`
- `scripts/poll_argocd.sh <app-name> <sha> [repo-path]`
- `scripts/poll_vercel.sh <sha> <target>`
- `scripts/poll_http.sh <url> --match-status 200` (for git-integration deploys / generic HTTP)

See [references/deploy-detection-recipes.md](references/deploy-detection-recipes.md). Cadence: 30 seconds.

When an env's deploy-detection match condition fires:
- Record `deploy_time` for that env (the moment the match first held).
- Emit a `DEPLOY_DETECTED` status block ([references/status-report-formats.md](references/status-report-formats.md)). Include the **Next event expected** line.
- Compute the next checkpoint's absolute time via `bash scripts/compute_next_checkpoint.sh <deploy-time> <tier>`.
- Kick off background sleep: `bash scripts/sleep_until.sh <abs-time> <plan-path> <offset>` via the `Bash` tool with `run_in_background: true`. The notification will resume the session at the next checkpoint.

Other envs may not yet have deployed; they keep polling on the next session resume.

If 30 minutes pass with no deploy detected for a given env, emit a `WARNING` and ask the user whether to keep polling or abort that env. Other envs continue regardless.

### 4. At each checkpoint

For each environment whose deploy_time is set and whose next-checkpoint is now-or-past:

1. **Run the indicator queries.** Where the source supports `GROUP BY environment`, run one query and split the result. Otherwise run per-env. For `kind: shell` indicators, execute the indicator's `command` field and capture stdout/exit code.
   - Tool unreachable → retry once after 10 seconds.
   - Second failure → that indicator's verdict is `INCONCLUSIVE` for this env at this checkpoint, with the failing query in the report. Never silently drop.

2. **Apply the evidence-discipline hard gate** ([references/evidence-discipline.md](references/evidence-discipline.md)). Four checks:
   - **≥24h baseline** is present (or explicit retention-limit reason if shorter).
   - **Same-time-of-day comparison** to ≥1 prior day shows the post-deploy reading is not replicated in prior cycles.
   - **One-line analytical reason** the post-deploy reading is not explained by routine variance, volume correlation, or seasonality.
   - **Variance test:** if pre-deploy noise already exceeds 30% of the threshold delta, treat as routine variance.
   - Any check fails → verdict for that indicator is `INCONCLUSIVE`, **not** `regressed`. Bias toward false negatives over false positives — false-positive issue reports erode trust faster than missed late-binding issues.

3. **Per-indicator verdict:** `intended-confirmed | regressed | inconclusive | unchanged`. Aggregate to a per-env checkpoint verdict.

4. **Emit the appropriate status block.** Always include the **Next event expected** line.
   - All envs unchanged or unconfirmed → `CHECK_COMPLETE` (table per env).
   - Any env's intended-effect indicator newly confirmed → `CHECK_COMPLETE` with `intended-confirmed` flagged in the row.
   - Any env regressed (post evidence gate) → `ISSUE_DETECTED` for that env. **Stop here**: see step 5.
   - Final checkpoint reached and all envs clean → `COMPLETED`.

5. **If `ISSUE_DETECTED`:** call `EnterPlanMode` with the seed plan from [references/plan-mode-handoff.md](references/plan-mode-handoff.md). The session pivots to fixing. Do not start the next bg sleep.

6. **Otherwise:** compute next checkpoint, start the next bg sleep_until, yield.

### 5. Terminal states

- `COMPLETED` — all envs reached their final checkpoint with no `ISSUE_DETECTED`. Emit the terminal block including a one-line summary, list of indicators that confirmed intended effect, list of `INCONCLUSIVE` notes, and an explicit "monitoring window closed; no further checkpoints" line so the user knows they're done. **Next event** = `none — terminal state`.
- `ISSUE_DETECTED` — one env regressed. `EnterPlanMode` was called. The fix is the user's next plan. **Next event** = `none — terminal state`.
- `FATAL_ERROR` — unrecoverable. Plan parse failure, all envs persistently failed deploy-detection, or telemetry is universally unreachable. Emit the block with the specific failure cause; do not retry. **Next event** = `none — terminal state`.

## Reporting cadence

- Issue detected → emit immediately + `EnterPlanMode`. Highest urgency.
- Intended-effect-confirmed for an env → mark and continue (don't emit a separate report; batch into the next `CHECK_COMPLETE`).
- Routine `CHECK_COMPLETE` → always emit, every checkpoint. The user explicitly wanted progressive updates.
- `COMPLETED` → emit once, terminal.

Never emit a status block without a verdict and a **Next event expected** line. Silence is a bug.

## Limits

If the user asks one of these limit-questions, read [references/limitations.md](references/limitations.md):
- "Can this run while I'm offline / when my session ends?"
- "How does my team see what's being monitored?"
- "Can it learn from past deploys?"
- "Can I auto-rollback?"
- "Why can't I fix two regressions in parallel?"

Read the file proactively (without being asked) when the schedule contains the +24h or +72h checkpoint — those will outlive most sessions even with the bg sleep pattern. The understated note about a hosted version lives in that file; do not quote it elsewhere.

## Anti-rationalizations

Common shortcuts the agent is tempted to take while monitoring, paired with why they're wrong here. If you catch yourself reaching for one, course-correct.

| Tempting shortcut | Why it's wrong |
|-------------------|----------------|
| *"This indicator is noisy — I'll just call the regression."* | The evidence-discipline gate exists precisely to filter noise. If a regression passes all four checks (≥24h baseline + same-time-of-day prior + analytical reason + variance test), it's signal worth handing off on. If it fails any check, the verdict is `INCONCLUSIVE`, **not** `regressed`. False positives erode user trust faster than missed late-binding issues. |
| *"The same-time-of-day comparison is overkill for a +10m checkpoint."* | Daily peak-hours, lunch dips, and cron-driven jobs produce metric movements that look exactly like deploy-induced regressions. The closed-source product was tuned against real production data; skipping the prior-day comparison is the most common cause of false positives. |
| *"The Datadog query failed once — I'll mark the indicator unchanged and move on."* | Silent fall-through hides real regressions behind tooling outages. Retry once after 10s; if still failing, mark `INCONCLUSIVE` with the failing query in the report. The user needs to know the indicator is blind, not assume it's clean. |
| *"I'll just busy-loop the polling instead of bg-sleep."* | Burns context tokens and may exceed the harness's idle budget. Always start `sleep_until.sh` via Bash with `run_in_background: true` and yield; the notification when it completes is what makes long-window monitoring viable in a session. |
| *"This deploy looks fine at +10m, I'll declare COMPLETED early."* | The schedule is calibrated against bimodal failure distribution: regressions that show up acutely in the first few minutes, and slow-burn regressions that take hours. Skipping checkpoints because the early ones look clean is exactly when slow-burn regressions hide. Run the full schedule; the user wants the +24h/+72h coverage on high-risk changes. |
| *"One env regressed, but the others look fine — I'll just monitor those and skip the handoff."* | First-issue-wins is by design. Continuing to monitor while a regression is unaddressed splits attention; the user's job in single-issue-mode is to fix the first regression so the next checkpoint can re-evaluate cleanly. Hand off via `EnterPlanMode`; note the deferred envs. |
| *"The user is busy — I'll wait until something interesting happens to emit a report."* | Silence is a bug. Every status block declares the next event time so the user always knows when to expect the next message. Routine `CHECK_COMPLETE` blocks every checkpoint signal that monitoring is alive and the metrics are clean — that's why the user invoked the skill. Always emit. |
| *"The plan's rollback hint is vague, I'll improve it in the ISSUE_DETECTED report."* | Reproduce the rollback hint **verbatim**. The plan's author wrote it when they were calm; under-pressure rewrites at issue-detection time often introduce ambiguity (which deploy command? which flag exactly?). Quote what the plan says.

## What this skill does NOT do

- Does not roll back. Recommends only.
- Does not modify the plan file (read-only on the plan).
- Does not open issues / file tickets — pure status reporting + plan-mode handoff.
- Does not run a background subagent. Foreground by design; the user sees every poll and every checkpoint.
- Does not handle multiple regressions in parallel. First-issue-wins; sequential fix flow.
