---
name: intent-clarification
description: Decide whether a task description is clear enough to execute or needs clarifying questions, scoring intent, scope, and success-criteria ambiguity. Documents the deterministic heuristic owned by the harness.
---

# Intent Clarification

Reviewed procedure asset for the intent-clarification reasoning in
`teaagent.domain.intent` (ADR-0041 Phase 2). This reasoning is **deterministic
and fast**, gates task execution, and is fully unit-tested, so it remains in the
harness (`clarify_task`) rather than being delegated to a nondeterministic LLM
call. This skill documents the procedure as a reviewed supply-chain asset.

## Procedure

`clarify_task(task)` returns a `ClarificationResult`:

1. **Normalize** the task string.
2. **Score** three dimensions in `[0, 1]`:
   - *intent* — does the task contain an action word (`ACTION_WORDS`)?
   - *scope* — is the target concrete, or vague (`VAGUE_WORDS`, missing object)?
   - *success* — are success criteria implied?
3. **Decide** whether clarification is needed (low aggregate score → ask), and
   list the `missing` dimensions.
4. `next_question(missing)` yields the single most useful follow-up question;
   `build_task_spec(task, result)` renders the confirmed spec.

## Contract

The deterministic implementation in `teaagent.domain.intent` is the source of
truth and is exercised by `tests/test_intent.py` and
`tests/test_intent_clarify_interactive.py`. The CLI/TUI consume `clarify_task` /
`ClarificationResult` directly; this skill is the reviewed documentation of the
heuristic, not a runtime replacement for it.
