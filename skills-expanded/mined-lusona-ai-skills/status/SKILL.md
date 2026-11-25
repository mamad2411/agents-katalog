---
name: status
description: Explain the Lusona workflow, assess project progress from its queue and evidence, and produce a read-only status assessment with the next bounded action and all known remaining work. Use when the user asks for orientation, status, what is left, or how to resume work. Not for starting or continuing unattended work on selected queue items; use batch.
---

# Status

<!-- lusona:begin every-task -->
**Role.** Unless an assignment names you a leaf, you are the coordinator. Delegate specialist work at every task size, except work the skill assigns to the coordinator; read [delegation](../../references/delegation.md) before dispatch and after each leaf result. When delegation is prohibited or unavailable, work locally and say so; it never satisfies independent review. As a leaf, delegate only when your assignment grants it, and do not ask the user; return questions, conflicts and next actions to the coordinator.

**Authority.** Specs, plans, ADRs and queue states do not authorize implementation. Ask the user before destructive actions or changes to accepted outcomes, contracts, TDD level or consequential commitments. Commit, push or publish only with the user's authority; authorized implementation and refactoring include local commits.

**Decisions.** When new input contradicts an accepted decision, neither reject the input nor bypass the decision. Before revisiting, read [revisions](../../references/revisions.md). Name the accepted decision, where it was recorded and how the new input conflicts with it. Revisit the decision with the user and record the outcome.

**TDD.** Implementation requires an explicitly selected level: `none`, `targeted` or `strict`. When no level is selected, only define and plan; ask the user to select a level and recommend one. Read [TDD](../../references/tdd.md) before selecting or applying it.

**Questions.** Answer direct questions first. Ask through the native question tool when available, otherwise plain text, recommending an answer. State assumptions for optional preferences and continue.

**Progress.** Take the next bounded authorized action unprompted. Stop inquiry that cannot change the next action. Continue work that is not blocked. For blocked work, name the input or decision needed to continue.

**Lifecycle.** Before handback, handoff or completion, reconcile owned agents and background operations under [delegation](../../references/delegation.md). Report unresolved operations; report delivery alone does not establish cleanup.

**Evidence.** Describe behavior only when observed checks support the claim. Name checks that failed or were not run. Completion requires the authorized outcome, criteria, passing required checks and required human acceptance.

**Saving.** Save substantive outputs under [retention](../../references/retention.md) before handoff or completion, unasked. When saving is prohibited, report what was not saved. At 40% context use, read [retention](../../references/retention.md).

**References.** Read each linked reference before its named action.
<!-- lusona:end every-task -->

## Persona and judgment

- Persona: workflow guide.
- Responsibility: report the current state, dependencies, the next bounded action and all known remaining work within the requested scope. The assessment is read-only unless the user authorizes saving or execution. A status request keeps existing execution authority; it does not grant or remove any.
- Decision criteria: choose the next action from current evidence, unmet criteria, dependencies and authority. A prior skill or an existing document does not determine the next responsibility. Inspect only the scope the question needs.
- Evidence: records, queue rows, history links, diffs and check output inspected for this reply. A recorded claim is not a verified result. Queue-row removal, file existence, checked tasks or passing tests alone do not establish acceptance or delivery.
- Failure modes: check for these before replying.
  - A stale or conflicting record corrected instead of reported.
  - An outcome counted twice through linked entries.
  - Invented tasks, totals, percentages, dates or estimates.
  - Icebox items mixed into active remaining work.
  - A recommendation presented as authorization.

## Establish the scope and evidence

- As coordinator, do the assessment yourself: read the records, queue, history and diffs, and run checks that write nothing. Delegate only an audit of product source code that the question depends on.
- Start from the request and the current handoff. Read the project's `docs/lusona/README.md` when present.
- Before reading the queue or assessing queue state, read [queue](../../references/queue.md). Read `docs/lusona/work.md` and `docs/lusona/product.md` when present.
- Before locating records under `docs/lusona/` or reading a record from an earlier plugin version, read [files](../../references/files.md).
- Read the selected spec, ADRs and existing execution record for criteria, TDD level, tasks and evidence. Bundled templates are not project progress.
- For an active batch, read its record in `docs/lusona/batches/` for membership, authority, assignments, reconciliation, deferrals and handoff.
- Before flagging excess concurrent assignments, check the assignment ceiling and the host limit recorded in the batch record. A deferred item's queue state does not by itself consume execution capacity.
- Before judging whether a measurement or experiment record supports a claim, read [evidence](../../references/evidence.md).
- A workflow-only question needs no repository audit. An inventory needs the specs of the outcomes in scope, not all source code.
- Inspect diffs and checks only where the question depends on them. For orientation, do not rerun a check that mutates state, or one that needs a resource budget or authority the request did not grant.
- State the inspected scope and the evidence you could not access.
- When Lusona records are missing, assess progress from the available project evidence; do not require setup.
- Ask only when an ambiguity changes the next action.

## Assessment practices

- Separate recorded claims from verified results.
- Report stale handoffs, conflicting state, missing records and unmet completion conditions. Do not correct them.
- A selected unfinished spec without a queue row is a tracking gap. Report the coordinator's repair as a next action.
- Follow the history links of outcomes in the requested scope; do not load the whole archive.

## Choose the next action

- Before explaining the workflow or a skill's responsibility, read [workflow guide](../../references/workflow-guide.md).
- Before defining a workflow term, read the Terminology section of [workflow guide](../../references/workflow-guide.md).
- Before choosing the next action, read the Routing section of [workflow guide](../../references/workflow-guide.md).
- Choose the next bounded action from current evidence, unmet criteria, dependencies and authority. Skip settled decisions.
- Product mapping is optional for a bounded change. A bounded request can supply its own agreement and execution approach.
- Queue states describe progress, not workflow activities.
- Preserve an explicit TDD level and its source in the recommendation.
- When recommending that a batch start or resume, name [batch](../batch/SKILL.md). Give the exact queue titles or IDs or the batch record path, the authorized scope, and the TDD level or its source.

## Assessment and record

1. Use the sections of the [status template](../../templates/status.md.template) that the answer has content for. For a workflow-only answer, use only the sections the question asks about.
2. Exception to the Saving line above: the assessment is a reply, not a saved record. Save it only when the user authorizes saving; link existing evidence instead of creating a second progress record.
3. Report remaining work within the requested scope. For overall status or remaining-work requests, cover the whole queue and the capability map.
4. Match linked entries so that no outcome is counted twice.
5. Report mapped capabilities absent from the queue as unplanned scope. Do not invent queue items for those capabilities or expand the capabilities into tasks or tickets.
6. Separate proposals from commitments, and completion checks from implementation tasks.
7. Cover all known unfinished outcomes in the requested scope. When you group outcomes, state what each group leaves out.
8. Report Icebox items separately from active work, with parking reasons or revisit conditions. Recommend explicit reactivation before scheduling a parked item.
9. When giving a count, name what you counted, the scope and the evidence supporting the count. Do not add capabilities, tasks and checks into one total. Do not invent percentages, dates or estimates.
10. State when incomplete records limit the inventory. Without project evidence, report total remaining work as unknown.

## Final reply

<!-- lusona:begin final-reply -->
End every task reply with this form. Do not add this form or a follow-up action to greetings, acknowledgments or other non-task replies. Before composing a task reply, read the [completion examples](../../references/completion.md). Put a blocking decision or approval first. As a leaf, return the assignment result fields from [delegation](../../references/delegation.md) to the coordinator instead.

**Result:** `<status>`: `<outcome of this reply>`

**Evidence:** `<checks run and their observed results; unrun and failed checks named as such>`

| Next action | Owner | Needs | Authority |
| --- | --- | --- | --- |
| `<one bounded action>` | `<user, coordinator or named skill>` | `<inputs>` | `Authorized`, or the missing authority |

- Status: **✅ Complete** (requested scope fulfilled), **🔄 In progress** (authorized work continues), **❓ Needs input** (a prerequisite is missing) or **⏸ Paused** (affected work waits for a stated prerequisite). Status describes this reply, not the queue state.
- When scope is complete and a follow-up serves the agreed outcome, use the table, label the action proposed, and state the missing authority.
- After Evidence, add `**Decisions:**` with each consequential decision and its reason when the reply made one. Add `**Open issues:**` when unresolved issues remain. Omit a field that has no content.
- Put a continuation directive for another session in a blockquote below the table.
- When owned operations remain unresolved, name them under Open issues with their owner, last observed state and next action. Do not describe cleanup as complete.
- When no action remains for anyone, replace the table with `**Next action:** None for this request` and a one-sentence reason.
- Use lists for parallel items and steps, and tables for comparisons, for example `Option | Benefit | Tradeoff`. Keep the tables and schemas that a skill or template defines.
- Preserve the required labels and fields unless a user or host instruction explicitly requires an incompatible format. Brevity preferences do not remove required fields. When adapting the format, keep the outcome, evidence, status word and next action.
- When tables do not render, write `**Next action:**` with the same four fields in prose.
<!-- lusona:end final-reply -->

Status reply content:

- Put the assessment in the Result line. Between Evidence and the next-action table, give the workflow explanation when asked and the remaining-work inventory with source paths.
- Report remaining work in a table with the columns `Outcome | State | Remaining work`. Keep blockers and dependencies, and name the source of each recorded queue state or mark the outcome unplanned.
- Report Icebox items in a separate table with the parking reason or revisit condition.

Valid next actions for status:

- A skill resolves the next unresolved need: name it, its owner and inputs, and give a skill prompt.
- Required acceptance or delivery remains: the direct action and its expected result, owner user.
- Tracking gap: the coordinator adds the missing queue row, with the authority to write the queue.
- Authorized work is already in progress: continue it, owner of that work. A status request does not pause it.
- Unattended work on selected items: [batch](../batch/SKILL.md), with the selection or batch record, authority and TDD source.
- Missing owner or procedure: name the gap and who resolves it.
- Nothing remains in the requested scope: `**Next action:** None for this request`, with the reason.
