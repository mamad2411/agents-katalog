---
name: verification-before-completion
description: "Use before claiming work is done, fixed, passing, or ready. Requires a final evidence check and residual-risk statement."
---

# Verification Before Completion

## Checklist

- Requirement or user request is satisfied.
- Changed files are scoped to the task.
- No placeholders, dead references, stale names, or broken links remain.
- Tests, build, browser checks, or static validation were run where appropriate.
- Failed or skipped verification is explicitly reported.
- If files changed, `implementation_self_review` or delegated `artifacts.self_check` exists and covers changed files, diff review, acceptance match, scope check, regression risk, verification evidence, and unresolved risk.
- If changed files lack self-review evidence, do not report normal `DONE`; return to self-review or report `DONE_WITH_CONCERNS missing_self_review`.
- Residual risk and next steps are clear.
- If the current role is delegated, the handback includes `task_id`, `current_stage`, `status`, `summary`, `artifacts`, `risks`, `uncovered_items`, and `recommended_next_stage`.
- If a delegated handback uses `status=NEEDS_CONTEXT`, it also includes `clarification_request` and `pm_action: "pm_clarify"`.
- If the current role is the top-level session or PM/coordinator and is about to end the turn, native closeout or continuation evidence exists unless the latest user message already came from that native gate and chose to end.
- Follow the Specialist Ask Boundary and Native Ask Contract from `core-workflow-contract`.
- If the task exposed a reusable workflow weakness, include an `evolution_signal` instead of silently moving on.

## Native Closeout UI Hard Gate

- A final prose response is allowed only after verification evidence is ready and closeout/continuation state is valid.
- Follow the **Native Ask Contract**, **PM Trigger Guidance**, and **Specialist Ask Boundary** from `core-workflow-contract`. All trigger types — review fan-in, verification results, `NEEDS_USER_INPUT` handbacks, branch/worktree choices, and closeout — use the same native ask path.
- Ordinary prose questions, "reply A/B/C" instructions, and summary-plus-question endings are not valid closeout evidence.
- If native ask UI is unavailable and a human choice is still required, report `BLOCKED` or `DONE_WITH_CONCERNS` with `missing_native_ask_ui`; do not claim normal completion.

## Adapter Integration Requirement

- PM/coordinator adapters must invoke this skill before their final user-facing response, not only when they happen to remember it.
- Specialist adapters must invoke this skill before any completion claim or turn-ending summary, but they must not open native user prompts themselves.
- Agent or skill text must not weaken this requirement into "may use native ask" or "use ask when required" without the turn-ending hard gate.
- Agent or skill text must not weaken the shared handback contract by renaming owner-controlled fields or making them runtime-specific.

## Final Evidence Format

```markdown
## Final Verification
- checks_run:
- passed:
- skipped:
- self_review:
- residual_risk:
```

Do not say “complete” before this check is done.
