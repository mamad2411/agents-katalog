---
name: sbtd-task
description: Use for SBTD task execution and continuation, explicit default/lite/strict mode selection, task records and status changes, cross-session recovery, and task handoffs. Load strict gates only for strict tasks; ordinary questions and read-only work do not create task files.
---

# SBTD Task

Use host-native tools to carry out the user's task. This Skill supplies task rules, not a scheduler, daemon, hook system, or new CLI. Project rules and explicit delivery requirements remain binding. Do not invent commands or claim unavailable helpers ran.

## Route before work

1. Identify the task, authorized project root, branch, and read-only constraints using only necessary reads. An existing task's branch mismatch pauses business and metadata writes: offer its correct worktree, explicitly authorized rebinding, or read-only inspection. "Continue" or choosing a mode does not authorize rebinding.
2. Mode precedence: the user's current explicit choice; otherwise the same task's confirmed/effective record; otherwise `default` for a genuinely new task. A missing, invalid, or ambiguous old record is not a new task: ask which task or mode to use. Do not choose by mtime. A valid task outranks an old handoff.
3. Assess fit without implementing first. If another mode is preferable, explain the current mode, recommendation and reason, and the option to keep the current mode; pause substantive work for the user's decision. Upgrades and downgrades use the same confirmation rule. Never infer a mode from output compression, installed tools, task complexity, or an existing task directory.
4. Honor a refusal, preserve its reason where writing is allowed, and continue in the selected mode. Do not repeatedly recommend the same change without new substantive risk. Same-task continuation preserves its choice; a new unrelated task does not inherit it.
5. For a writable project task with no branch conflict, save the confirmed mode and source promptly using [task state](references/state.md). Do not wait for handoff. If saving fails, keep the current-session choice, report that it was not persisted, and do not promise reliable recovery. `default/lite` may continue unrelated safe work; required `strict` artifacts remain incomplete.
6. Then assess clarification. Read facts the project can answer. If requirements are clear, explain why full `grill-with-docs` was not needed and proceed. For consequential domain ambiguity, explain the unresolved point and ask about grill. Declining a method does not authorize guessing required answers.
7. After every completed full `grill-with-docs` session, invoke `book-ddd-distilled-modeling` and present its separate visible `DDD Boundary Review` in every mode. Follow that Skill's result and correction loop: advance requirement confirmation/design only at `confirmed`; `needs-clarification` returns to clarification and `blocked` stops the dependent step. An unavailable/unreadable reviewer or missing required evidence is blocked for default, lite and strict until the gate can run and pass. Interview-time modeling and informal substitute checks do not satisfy this post-grill gate. This gate has no default/lite substitute; it does not disable fallback for unrelated optional tools.

Pure questions and explicitly read-only tasks keep mode and progress in the conversation. Do not create or update task, active pointer, handoff, identity, ignore, or tool caches for them. Do not run queries with unverified cache or wiring side effects. Explain that conversational state is not persisted recovery.

## Execute the selected mode

| Mode | Working contract |
|---|---|
| `default` | Understand, inspect relevant facts, implement, run focused verification, deliver. Keep only the needed local task record; do not load every gate or generate an entire task packet. |
| `lite` | Use the short checklist below and a shared short task card, with only needed artifacts. Do not mechanically add PRD/design/implement files. |
| `strict` | Load [strict gates](references/strict.md) and complete the applicable before-dev, check and finish-work obligations. Mark genuinely inapplicable items explicitly; never turn missing required evidence into a pass. |

The `lite` checklist:

- State the goal, scope, confirmed mode and acceptance conditions.
- Inspect the smallest relevant source/specification and risk surface.
- Implement the whole requested behavior; keep authorization and data safety intact.
- Exercise the changed path, verify the affected scope, and state evidence limits.
- Update the necessary task record and deliver results, open risks and next action.

A user's explicit PRD, scenarios, tests, report, history or completion-time requirement applies in every mode. Existing project compliance and CI requirements are not weakened. Read-only constraints override persistence even in strict work; completing that read-only review is not completing a full development lifecycle.

## Common safety and proof

- Use one writer per responsibility and one controller per validation environment. Native independent review is available; do not automatically dispatch implementation/check roles for every task.
- Missing nonessential tools, Skills or indexes should not freeze unrelated safe default/lite work. Use actual source, contracts and available tools as alternatives; do not loop on installation or claim unavailable capabilities. Data loss risk, missing authorization and unproven required facts still constrain the affected action in every mode.
- Graft is optional structural evidence, not complete compiler semantics or business validation. Never use a parent directory as a multi-project entry; aggregate independent authorized-root reads only. Do not enable LLM/cloud enrichment or upload project data. Managed commands require the established privacy and side-effect safeguards; without them use source inspection instead. A stale/empty graph is not proof of no impact.
- A real formal validation run obeys the project's report, privacy and evidence contract regardless of mode. Distinguish diagnostics, mocks, local/CI evidence and full-stack proof. Preserve failure reports; a generated report is not a passing test. Use `project-validation` when applicable; do not require unrelated tools merely to fill a report table.
- Use the simplest correct implementation and protect readability, real seams and security. Do not rewrite third-party mirrors or add an abstraction merely to shorten a function.
- New task records do not require developer identity. Identity is only needed for a lesson write: ask for it when needed, preserve historical IDs/markers, and never guess a name. Missing identity does not stop unrelated safe default/lite work.
- Onboarding, global installation, migration, cleanup, workflow sync and release are separate authorizations. Mode choice or a task completion does not grant any of them. Preserve user data and unknown ownership; a Git tag is not a backup of ignored data or HOME.

## Continue, change mode, finish

Read [task state](references/state.md) when persisting, resuming, reopening, resolving blocked history, promoting or archiving a task. Read [handoff](references/handoff.md) only when a real pause/context switch or continuation need warrants it. Do not load all references for an ordinary answer.

Persistent task operations use the Python helpers installed with `sbtd-workflow-onboard` (`scripts/sbtd_task_state.py`, `scripts/sbtd_task_routing.py` and `scripts/sbtd_handoff.py`, with the dependencies declared in its `requirements.txt`); [task state](references/state.md) describes `TaskStore` operations and boundaries, [handoff](references/handoff.md) describes `HandoffStore`. `TaskRouter` only turns facts you have already made explicit — intent, task choice, mode choice, recommendation response, read-only and confirmation flags — into a deterministic `RouteDecision` (`ready`, `needs-task-choice`, `needs-mode-choice`, `needs-mode-decision`, `needs-branch-choice`, `needs-persistence-confirmation`, `persistence-failed`, `blocked`); it never classifies natural language or guesses intent, and a `needs-*` / failed status is a prompt for the user, not an executed action. The helpers are host-native libraries, not a new CLI or daemon. If an installed helper copy or its declared dependencies are unavailable, report that persistence did not run instead of claiming a write, and keep the limitation explicit in the final report.

For a relevant specialized engineering method, read [method routing](references/methods.md). For tool availability, installation, privacy or formal test evidence, read the applicable section of [tool boundaries](references/tooling.md). For an explicit presentation request or a global-rule-defined automatic style trigger, read [presentation](references/presentation.md); style never changes execution mode. Do not infer a missing global automatic-style state machine from a project-only fallback.

A mid-task mode change takes effect after the user chooses it and is saved where allowed. Switching to strict requires valid evidence for the following gates; it does not fabricate earlier passes. Switching down does not delete shared records or their history.

Before marking done, compare actual results with every requested acceptance condition and the selected mode's obligations. Append the real completion event and timestamp using task-state rules. Do not auto-archive, publish, commit, migrate or delete backups. Report what changed, what was exercised, what remains unverified and any recovery limitations. Never promise automatic session-start restoration without an observed host capability.
