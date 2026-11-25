---
name: coding-workflow
description: Guide implementation, bug fixes, scripts, and small projects through a proportionate brief, scoped changes, fresh verification, and independent read-only review. Use when Codex is asked to change code; keep tiny edits lightweight and do not activate for explanation-only or review-only requests.
---

# Coding workflow

Turn a coding request into a small, verifiable change without taking control away from the implementer. Constrain scope and completion claims; leave ordinary technical choices open unless the user or repository already decided them.

## Respect the working context

- Read applicable repository instructions and inspect the existing structure before choosing files, commands, or conventions.
- Preserve unrelated user changes. Do not add features, dependencies, refactors, migrations, deployment, publishing, or external writes that the request does not require.
- This workflow does not grant permissions beyond the user's request. Stop when a required action needs new authority or a high-impact product decision.

## Choose the lightest sufficient mode

Use judgment rather than file counts alone.

- **Tiny:** Obvious, low-risk edit with narrow impact, such as a typo, copy change, or one-line configuration correction. State a short inline brief and run a proportionate check. A separate task file or reviewer is normally unnecessary.
- **Standard:** Behavior change, bug fix, new script, or change spanning meaningful logic. Record a compact brief in the repository's existing convention or `TASK.md` when a durable record helps; a short, contained task can keep it in the conversation. Test the behavior, run fresh verification, and request independent review when available.
- **High-risk:** Authentication, authorization, money, sensitive data, destructive behavior, public APIs, migrations, or difficult rollback. Use a detailed task brief, explicit risk notes, focused regression tests, all required checks for the affected behavior, and independent review. Obtain user direction before choices that materially change product behavior or permissions.

Escalate the mode when uncertainty or blast radius is higher. Do not make a tiny task heavy merely because this skill is active.

## Establish the task contract before editing

For Tiny and short Standard work, state these items briefly in the conversation. For longer Standard and High-risk work, reuse the repository's planning convention or create `TASK.md` when no suitable record exists:

1. **Goal** — the observable outcome.
2. **Non-goals** — tempting adjacent work that is deliberately excluded.
3. **Done when** — specific, checkable acceptance conditions.
4. **Scope** — expected files or components, updated if inspection reveals a justified change.
5. **Verify** — exact commands or manual checks that can prove completion.
6. **Risks or assumptions** — only those that could change the result.

Read [references/task-brief.md](references/task-brief.md) for the template. When useful, generate it with `python <skill-dir>/scripts/init_task.py --help`. Do not overwrite an existing task file.

## Implement narrowly

- Prefer the smallest coherent change that meets the task contract.
- Follow established project patterns before introducing a new abstraction.
- For a bug, reproduce the failure with a focused test when practical before fixing it.
- For new behavior, add or update automated tests when the repository has a suitable test surface.
- Do not require strict test-first development for throwaway exploration, generated code, documentation, or configuration. Record the alternative verification used.
- If the task contract must change, update it and explain why before expanding implementation.

## Require fresh verification

Before claiming success:

1. Identify what command or observation proves each acceptance condition.
2. Run the complete relevant command after the final change.
3. Read the output and exit status; do not infer a full pass from a partial check.
4. Report the actual evidence. If verification cannot run, state the limitation and do not describe the work as fully verified.

Use focused tests during iteration, then complete the affected behavior's relevant tests and repository-required checks after the final change. Once those pass, expand or repeat verification only for new changes, failures, or unresolved concerns. Never treat “should pass,” an earlier run, a diff, or another agent's success message as proof.

## Parallel work

Delegate independent exploration, test analysis, or read-only review when it materially helps quality or elapsed time and the harness permits it. Prefer at most two subagents unless the user requests otherwise. Keep dependent steps and overlapping file edits sequential; the main agent integrates and verifies the result. Keep tiny tasks single-agent.

## Review independently and proportionately

For Standard and High-risk modes, request an independent read-only reviewer when the harness supports delegation and the task permits it. Give the reviewer the task contract, relevant diff, fresh verification output, and only the source context needed to judge the change. Do not prime the reviewer with the implementer's conclusion.

Use [references/review-contract.md](references/review-contract.md). Classify findings as:

- **Blocker:** Incorrect, unsafe, destructive, or outside the task contract. Must be fixed and re-reviewed.
- **Important:** Material reliability, maintainability, or coverage problem. Resolve before completion unless the user explicitly accepts the tradeoff.
- **Suggestion:** Non-blocking improvement. Record briefly; do not expand scope automatically.

If independent review is unavailable, perform the same checklist as a self-review and clearly label that limitation. Do not pretend self-review is independent.

## Finish with a compact evidence report

Report the result, the key verification evidence, and any unresolved findings or limits. Include a run command or unchanged behavior only when it helps the user use or assess the result; do not produce a fixed checklist of empty sections.

Do not create a handoff document unless the task is large enough that another session would need it.

## Design provenance

This skill intentionally incorporates selected patterns from established public workflows while remaining lightweight. Read [references/provenance.md](references/provenance.md) when auditing design choices or updating the workflow.
