---
name: teach-test
description: "Quiz the user on a topic or workflow through native multiple-choice question dialogs, with feedback and adaptive practice. Use for interactive assessment after checking native dialog support; teach handles lessons without assessment."
---

# teach-test

Quiz the user on a topic or workflow through native multiple-choice question dialogs, with feedback and adaptive practice.

## Choose this workflow

Use for interactive assessment after checking native dialog support; teach handles lessons without assessment.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [General methods](../../references/packs/general.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; a topic, workflow, or recent lesson plus optional experience, question count and practice/test preference. Requires an available native question tool permitted for this interaction in the current host mode.

**Pack prerequisites:** Resolve the user brief and inspect the relevant project or supplied evidence. External capabilities are optional unless the selected action actually needs them.

- **Infer from evidence:** Resolve the named files, existing scripts, current task and earlier corrections from the conversation and repository.
- **Reasonable default:** Use the narrowest interpretation that completes a reversible local task; state a consequential assumption once.
- **Ask only when needed:** Ask when competing targets or incompatible success conditions would change the result; continue independent inspection first.

Declared evidence requirements: `user.questions`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Assess understanding through one native dialog question at a time. Do not render quiz questions inline, implement the named tool, alter project files, or change host mode/settings automatically.

No project or external-service writes. Keep quiz state in session context; on an explicit save request, write the quiz report to the path the user names or save it with project checkpoint NAME.

## Execute

1. Read ../../references/teaching.md and ../../references/teach-test.md. Resolve the topic from the complete brief or immediately preceding lesson; ask for it only if unresolved.
2. Inspect actual callable tools. Prefer request_user_input_async in a Codex environment that exposes and permits it, otherwise request_user_input only in its supported mode; use AskUserQuestion in Claude when available. Follow the actual host schema and restrictions. If no suitable dialog is available, explain that native interactive testing is unavailable here and stop without inline questions.
3. Create quiz state with toolkit quiz create. Generate a question grounded in the lesson or target workflow, with exactly three short neutral choices, a correctOptionId, concept, and explanation. Keep this answer material out of the user-facing question.
4. Call toolkit quiz present to validate and shuffle the choices and produce a presentation payload for the observed dialog. Actually invoke that native host tool with presentation.arguments. Merely printing the payload does not ask the question.
5. For asynchronous tools, retain the quiz as awaiting-answer and wait for a user response; a returned pending tool call or preselected option is not submission. Do not advance, reveal the answer, or end with an inline replacement question while waiting.
6. Normalize the actual response into questionId, submitted, selection/freeText, skipped/cancelled and call toolkit quiz answer. For a free-text explanation, use quiz review only after assessing its meaning; preserve the actual response and explain the judgment.
7. Show returned feedback after answers in practice mode; withhold correctness in test mode until finished. Generate the next question using demonstrated misconceptions and remaining budget, then repeat through the native tool. Use quiz report for the final assessment; report sample limits and optional review topics.
8. Test one concept at a time, mixing a state prediction with an application when useful. Adapt to the specific misconception; a short quiz cannot establish mastery.

## Technical method

- **Inspect:** Inspect requested topic, level, previous answers and availability of the host's native question dialog.
- **Method:** Ask one discriminating multiple-choice question in the dialog, wait for the answer, explain why choices differ and adapt the next question.
- **Avoid misdiagnosis:** Inline questions or an early answer key defeat native assessment; if the host forbids quiz dialogs, explain the limit and stop the quiz without disguising it as clarification.
- **Check the result:** Verify that questions wait for a real answer and that a misconception changes subsequent practice without claiming mastery from one guess.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [General worked example](../../references/examples/general.md).


## Decision branches

- **When question tool is missing or restricted to clarification:** Report that assessment is unavailable in this mode; do not disguise quiz questions as implementation clarifications.

## Deliver and verify

- Native multiple-choice question dialogs, answer-dependent feedback, and a final short assessment with concepts to revisit. Question text stays in the dialog; explanations may appear in normal conversation after answers.
- Submitted-answer evidence, grading rationale, skips, and a scoped assessment of demonstrated knowledge.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- The host receives question/options only, with no answer key or explanation in the native payload. A second question cannot be presented before the pending answer is resolved.
- Empty, absent, default-only and delayed async responses do not advance or grade the quiz. Skips/cancellations do not count as incorrect; stale answers cannot answer a newer question.
- A linked-list quiz checks traversal, known-node insertion and pointer order. An ml-split quiz checks temporal/entity leakage and never starts training. If native dialogs are unavailable, the workflow reports that limitation and does not substitute inline quiz questions.

## Stop and recover

- Stop on the requested question limit, cancellation, missing native-dialog capability, ambiguous topic, or an unresolved answer. Respect tool-specific host/mode restrictions; do not force Plan mode, grant permissions, or simulate a native dialog by printing JSON or markdown.

## Example requests

- **Normal (inspect):** Quiz me on linked lists using the native question dialog, one question at a time.
- **Edge (inspect):** Test linked-list operations; skip one question and explain only at the end.
- **Blocked (inspect):** Inspect whether this host permits native assessment dialogs; do not print an inline quiz.
