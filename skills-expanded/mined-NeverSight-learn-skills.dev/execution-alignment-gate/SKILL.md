---
name: execution-alignment-gate
description: Detects materially ambiguous or under-specified requests, selects the right clarification target, and enforces bounded alignment before execution, including spec-governed continuations and approval-gated manager handoffs. Use when ambiguity could cause wrong deliverables, wrong scope, wrong implementation path, avoidable rework, or token waste from repeated follow-up.
license: Apache-2.0
metadata:
  author: Mike Willbanks
  repository: https://github.com/mwillbanks/agent-skills
  homepage: https://github.com/mwillbanks/agent-skills
  bugs: https://github.com/mwillbanks/agent-skills/issues
  purpose: Reduce ambiguity, rework, and token waste before execution
  posture-default: conservative
---

# execution-alignment-gate

Use this skill when ambiguity is material enough that proceeding without alignment is likely to produce the wrong result, force rework, or waste tokens through repeated follow-up.

Do not use this skill as a crutch for failing to read the specification, follow an approved plan, obey repository rules, or comply with an active execution mode already in force.

## Primary objectives

* Reduce materially harmful ambiguity before implementation starts.
* Reduce wrong-path execution.
* Reduce token waste from avoidable rework and repeated clarification.
* Improve clarity and alignment while preserving forward progress.
* Keep clarification bounded, concise, and high leverage.

## Non-objectives

* Maximizing certainty.
* Asking every plausible question.
* Replacing execution discipline.
* Interrupting obvious continuation messages.
* Adding approval ceremonies to trivial or low-risk work.

## Default posture

Default posture is **conservative**.

Only activate when ambiguity is likely to cause one or more of the following:

* wrong deliverable
* wrong scope
* wrong implementation path
* wrong validation target
* avoidable rework
* materially increased token usage from likely follow-up and correction

Posture may be elevated to **moderate** or **aggressive** only through explicit invocation or a higher-priority instruction. Do not self-escalate posture by agent whim.

## Workflow

Follow this sequence:

1. Perform a silent ambiguity assessment before asking anything.
2. Check [activation rules](references/ACTIVATION_RULES.md) and [bypass rules](references/BYPASS_RULES.md).
3. If the request is clearly a continuation, approval, or low-risk correction, bypass this skill and proceed.
4. If alignment is required, route to the correct target mode using [target modes](references/TARGET_MODES.md).
5. Ask the fewest high-leverage questions needed using [question patterns](references/QUESTION_PATTERNS.md).
6. After answers arrive, synthesize a concrete plan, lock any remaining material assumptions, and apply [approval flow](references/APPROVAL_FLOW.md) when required.
7. If the user is unavailable, apply [unattended behavior](references/UNATTENDED_BEHAVIOR.md).
8. If clarification reveals no true blocker, proceed. Do not reopen broad clarification loops.
9. Apply [token economics](references/TOKEN_ECONOMICS.md) and avoid spending more clarification tokens than the expected rework would cost.

## Hard limits

* Prefer 1 to 3 questions.
* Maximum 5 questions in a clarification round.
* Maximum 4 options per question, plus freeform when helpful.
* Allow at most one blocker-only follow-up after the bounded clarification round.
* Do not open repeated wait windows in unattended mode.
* Do not retain verbose per-run narrative history.

## Required behaviors

* Clarify only when answers materially affect execution.
* Treat approved spec or plan updates as governing context; do not reopen alignment for the same decision unless a new material contradiction appears.
* Prefer safe defaults when ambiguity is minor and risk is low.
* Use short assumption blocks when proceeding under defaults, refusal, or unattended fallback.
* For manager escalation, use the compact blocked packet in [assets/TEMPLATE_MANAGER_PACKET.md](assets/TEMPLATE_MANAGER_PACKET.md).
* For plan confirmation, use the compact structure in [assets/TEMPLATE_PLAN_CONFIRMATION.md](assets/TEMPLATE_PLAN_CONFIRMATION.md).
* For assumption locking, use [assets/TEMPLATE_ASSUMPTIONS_BLOCK.md](assets/TEMPLATE_ASSUMPTIONS_BLOCK.md).

## Prohibited behaviors

* Do not blame the user for ambiguity.
* Do not defend the model.
* Do not mirror hostile tone.
* Do not ask the user to restate the whole task.
* Do not ask questions already answered by context.
* Do not use this skill to compensate for ignoring specs, plans, repo rules, or execution mode.
* Do not ask low-value questions that do not change execution materially.
* Do not demand approval when it adds no value.
* Do not ask the user for a manager-owned decision simply because a subagent is approval-gated or unavailable; route through manager mode instead.
* Do not retain large clarification logs or other garbage that costs more than it saves.

## Complement to execution mode

Apply this skill before implementation when material ambiguity would otherwise force low-confidence execution. Do not use it to excuse failure to follow existing plans, repository rules, or execution-mode requirements already in force.

See also:

* [activation rules](references/ACTIVATION_RULES.md)
* [target modes](references/TARGET_MODES.md)
* [bypass rules](references/BYPASS_RULES.md)
* [question patterns](references/QUESTION_PATTERNS.md)
* [approval flow](references/APPROVAL_FLOW.md)
* [unattended behavior](references/UNATTENDED_BEHAVIOR.md)
* [failure modes](references/FAILURE_MODES.md)
* [token economics](references/TOKEN_ECONOMICS.md)
* [examples](references/EXAMPLES.md)
