---
name: cursor-interrogate
description: "Use when explicitly requesting adversarial review of a change or design, with findings proven by executed reproductions."
disable-model-invocation: true
---

## Runtime selection

Before runtime-dependent work, read [execution selection](references/runtime/selection.md). In a verified T3 host follow [the T3 contract](references/runtime/t3.md) and its method reference; the inline section below is the native Codex branch, not literal T3 dispatch. Outside T3, native Codex follows that inline branch unchanged. If the host is ambiguous or a required capability is unavailable, report the gap; a permission refusal never authorizes switching branches.

## Native Codex branch

## Codex runtime mapping

This published workflow is explicit-only through `agents/openai.yaml`. Use the native Codex subagent capability for independent read-only reviewers only when delegation is authorized. Require one immutable scope and rubric, at least two distinct model requests accepted by native spawn, separate read-only outputs, and a coordinator lead judgment before claiming a bounded review. If a configured reviewer is missing or fails, mark the aggregate PARTIAL and name the slot; never fabricate multi-model consensus or a complete configured run. Follow the standing `model-capability-router` and the operator-selected model/effort; do not force the Cursor default model table. Record requested reviewer profiles and unavailable slots, and mark effective model/effort readback unavailable unless the native surface supplies it. Keep the source rubric, lead judgment, and no-auto-apply contract.

# Interrogate

Adversaries try to break the named change or design. Keep only findings proven by an executed reproduction. Report findings; do not apply fixes.

## Frame

Freeze the user-named scope; otherwise capture the branch diff from its verified merge base, plus staged, unstaged and relevant untracked work. State the intent from the request, commits and PR description through `cursor-in-your-own-words`. Resolve material ambiguity before dispatch.

## Fan out

Use the framing and isolation of `cursor-arena` Phase A steps 3–4 and Phase B, with the configured interrogate reviewers rather than arena runners. Select actual models and efforts through `model-capability-router`; preserve explicit selections and mark unavailable reviewer slots. Each reviewer gets the same scope and intent, its own authorized scratch worktree and the scoped uncommitted changes. Reproduction permission applies only inside that worktree: preserve the user's workspace, credentials, live services and external-action boundaries. If safe isolation or execution is unavailable, report the missing proof rather than run against the user's active checkout.

Brief each bounded native reviewer: break this change, and prove every finding with a test, script, prototype or command against the real code. Report the exact command, actual output and output required by the intent. Keep reproductions in the assigned worktree. Omit unrun style, naming and hypothetical future risks. No findings is valid.

## Verify and report

Rerun each safe reproduction on the frozen candidate. Keep it only when the observed failure contradicts the intent. Distinguish base-existing failures and harness failures. Merge findings with the same root cause. Do not choose one adversary's list as a winner, graft code, or apply repairs; Arena Phases C–E do not run.

Return the intent, actual reviewers and coverage gaps, verified findings with commands and outputs, and dropped-finding counts/reasons per reviewer. Say “no verified findings” when none survive. Missing execution or reviewer diversity must remain explicit; it is not proof the change is defect-free.
