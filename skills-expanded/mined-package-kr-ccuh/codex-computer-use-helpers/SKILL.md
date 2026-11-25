---
name: codex-computer-use-helpers
description: Select CCUH guidance for the task when using Computer Use to observe or operate apps or browsers. Skip general questions and coding work that do not use Computer Use.
---

# Codex Computer Use Helpers

Use alongside the official Computer Use skill. Follow the selection criteria below to read the relevant guidance, then use official Computer Use to carry out the user's task. Proceed without asking the user to explicitly invoke CCUH each time.

Use this automatically supplied guidance as part of the requested task. In routine updates, describe the next user-visible action, such as “I'll open the requested window.” When an error occurs, report what failed and what you can verify next. Leave skill names, explanations about loading or applying guidance, and raw tool codes out of those updates. Explain those details when the user asks about them.

## Before starting

1. Identify the requested task, its target, and the authorized scope. Use the request and approvals already established.
2. Read the official Computer Use setup procedure and usage instructions for the current host. Use the table below to select and read the relevant guidance before the first UI observation or input.
3. Apply the selected guidance and do the work with the official tools. Verify the requested effect on the same target and follow the official cleanup procedure before reporting completion.

## Selecting supporting guidance

Resolve paths relative to this `SKILL.md`. If multiple conditions apply, follow all relevant guidance.

| When to apply | What to read | What it covers |
| --- | --- | --- |
| Before the first UI observation or operation. Apply again if the connection, the agent performing the operation, or the task state changes. | [Execution state](references/execution-state.md) | Who may act, known conflicts, unclear outcomes, ending a session, and reconnecting |
| Before selecting the initial target or observing the UI. Recheck if the requested target, window, document, or tab changes. | [Work target](references/target.md) | Identifying and reusing the exact target, checking scope and support for the window state |
| Before the first UI observation or operation. Reassess if the input method or the conditions for interference with the user change. | [User work protection](references/user-work-protection.md) | Protecting keyboard input, mouse, screen, and clipboard |
| Before sending input such as clicking, typing, changing a value, or scrolling. | [Input target](references/input-target.md) | Using an input target from the latest observation |
| If an error blocks the task, the outcome of a submitted change is unclear, or the user requests diagnosis. | [Doctor](../ccuh-doctor/SKILL.md) | Who diagnoses and who takes action, and supported recovery procedures |

## Applying the selected guidance

- For read-only work, apply the first three references. Add the input target guidance when input is needed. Reserve Doctor for tasks that meet the diagnosis criteria.
- If the guidance is already in the current context, keep applying it without rereading it for every operation. Recheck the relevant conditions when the target or state changes.
- If context summarization or resuming a task leaves required guidance unavailable in the current context, reread it before the next UI action. A record of having read it earlier is insufficient to confirm the current rules.
- Apply the same selection criteria if Doctor moves from diagnosis alone to UI observation or a recovery operation. Keep the work off the UI when the error response is sufficient for diagnosis.

## Protection rules that always apply

- Preserve the user's specified target. If it cannot be located, do not silently substitute another window, tab, or browser. Distinguish user-requested creation of a new target or navigation from a substitute.
- In default mode, choose a method that avoids interfering with the user's work. Watch mode is an option that shows the actual work window with the same capabilities and permissions. Use only supported operations in either mode.
- Follow the current host's rules for who may act, its session contract, and the official tool's support requirements. Base actions on the latest observations and respect confirmed ownership or conflicts.
- Distinguish an operation rejected before dispatch from a dispatched operation with an unclear outcome. Do not resend a change whose execution is uncertain or use a reset, another connection, or another chat to bypass existing protections.
- Stop further operations and classify the state when you detect actual interference or a signal to stop. Before-and-after checks alone cannot establish continuous non-interference. Report completion only for effects you have verified.

## When required guidance cannot be read

Check that the selected file exists in the actual bundle and is readable. If required guidance is missing or unreadable, treat it as unapplied. Do not start any UI observation or operation that requires it. Briefly report which guidance is missing and the last step you verified.

Keep the existing plugin settings and protection state. Do not replace missing guidance with code from a failed prototype or another installation.
