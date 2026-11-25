---
name: ccuh-doctor
description: Diagnose Computer Use initialization, authentication, permission, connection, and target errors when they block work or leave the outcome of a change unclear. Identify the cause and who should take the next step. Also use when diagnosis is requested explicitly. Skip routine UI work.
---

# CCUH Doctor

Use errors and diagnostic procedures from the official Computer Use tools to narrow down the problem. Apply this skill when an error blocks work, even if the user did not invoke it explicitly. A request for diagnosis gives no automatic approval to change settings, install anything, or resend input whose outcome is unclear.

When diagnosing or recovering a task, describe the observed error and the next check in plain language. For example, “The browser couldn't open the page. I'll check whether the tab was created.” Leave the name and use of this skill out of routine progress and results. Explain the guidance when the user asks about it.

## Start the diagnosis

1. Start with the error response already received, the requested target, the last verified step, and whether the change was sent. If that evidence is sufficient, finish the analysis without initializing the UI or retrieving its contents.
2. Read [Diagnosis and handoff](references/diagnosis-and-handoff.md). Distinguish observed facts, possible causes, and what remains unverified. When taking over from a routine task, carry forward any change in progress or whose outcome is unclear.
3. If more evidence is needed, use only the official diagnostics on the current host that are necessary to distinguish the possible causes. Leave unrelated logs, the full environment, other apps, and other chats untouched. Do not build a separate installation checker or error classifier.
4. Identify who should take the required action and check what is already authorized. The AI handles any official recovery it can perform and guides the user through steps only they can perform, one at a time.

## Before observing the UI or attempting recovery

Keep the UI untouched during diagnostic analysis. If the current host restricts Doctor to read-only access, honor that restriction and hand recovery over to the supported standard workflow.

Before observing or interacting with the UI, apply the selection criteria in the [Codex Computer Use Helpers](../codex-computer-use-helpers/SKILL.md) skill and the following guidance.

- [Execution state](../codex-computer-use-helpers/references/execution-state.md) covers who executes the work, changes in progress or with unclear outcomes, connection, and shutdown.
- [Work target](../codex-computer-use-helpers/references/target.md) covers the original app, window, document, or tab and the scope of the request.
- [User work protection](../codex-computer-use-helpers/references/user-work-protection.md) covers avoiding interference in default mode and when to show the work window in watch mode.
- [Input target](../codex-computer-use-helpers/references/input-target.md) covers choosing a target from the most recent observation when input is needed.

Carry unresolved changes and existing safeguards across a new connection or handoff. Do not resend an unresolved change or clear those safeguards simply because the connection or person responsible changed. Follow the official tool's current safeguards and recovery contract.

## Finish diagnosis and resume work

- Once the cause and next step are clear, skip repeat diagnosis during routine work. After user action or recovery, verify the state and resume only the remaining work.
- If the issue remains unresolved, briefly report the observed error, the last verified step, whether the change's outcome is known, and the next action needed. Label suspected causes as such and report connection recovery separately from task completion.
- Follow the execution-state guidance and the official lifecycle for normal cleanup. Keep safeguards in place for work in progress or with an unclear outcome.
