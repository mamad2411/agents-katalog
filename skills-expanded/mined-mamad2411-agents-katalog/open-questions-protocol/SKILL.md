---
name: open-questions-protocol
category: architecture
description: Use when an analiz question needs the human, not the code, to decide - recording it with record_open_questions, judging blocking vs non-blocking, and resuming the report after an answer
---
# Open Questions Protocol

## Overview

A genuine product decision the code cannot settle is recorded with `record_open_questions`, never written into the report as prose and never asked with `ask_user` — you hold no `ask_user` tool on an analiz task. The system shows every open question as an answer box above the report; the human answers there, not in chat. The report's `risks` section (analiz-html-report) is risks only — it never carries open questions.

A question the codebase already answers is not a question. Exhaust `codebase_search` / `grep_code` / `get_symbol_skeleton` / `expand_symbol_context` and the project's own docs (technical-analysis-workflow) before concluding only the human can settle it.

## Recording a question

`record_open_questions` takes three independent operations in one call:

- `questions` — up to 10 NEW questions: `{prompt, kind: product|technical, blocking, recommended_answer?}`. The server assigns the key (`Q1`, `Q2`, …) in creation order — never invent one.
- `update` — edits to questions you already recorded, by `key`: any of `prompt`, `kind`, `blocking`, `recommended_answer`. Refused once the question is **answered** if you try to change its `prompt` — the human answered that exact wording; withdraw it and add a new one instead of rewriting underneath their answer.
- `withdraw` — keys an answer or further reading made moot. A withdrawn question stays on the record (status `withdrawn`) and never blocks anything again.

`recommended_answer` is required whenever `blocking` is `false` — refused otherwise. There is no such thing as a non-blocking question with no answer to proceed on.

The call returns the task's full current list (key, kind, blocking, status, answer) as text — read it to confirm the key a new question got before referencing it later in the same run. `list_open_questions` returns the same list on demand, with every answer, for a run that did not just write one (a revision, a resumed run).

## Blocking vs non-blocking

**Default to non-blocking.** A reasonable default almost always exists: record it with `recommended_answer` and keep working. Blocking is the exception, reserved for a question where proceeding on ANY guess would waste the implementation, not merely a question you'd rather not guess at.

| | Example |
|---|---|
| ✅ Non-blocking | "Should archived tasks be included in the export?" — kind `product`, `recommended_answer`: "No — archived tasks are excluded from every other board export." A wrong guess here costs one column in a CSV, not a redesign. |
| ✅ Non-blocking | "Keep the existing 30-day retention or extend it?" — kind `product`, `recommended_answer`: "Keep 30 days — no stated reason to change it." |
| ✅ Blocking | Two incompatible product behaviours with no basis in the code or the brief to choose between them (e.g. "on conflict, does the import overwrite the existing row or skip it?" when both are one-line changes but produce silently different data). |
| ✅ Blocking | An external system or contract you cannot see (e.g. the brief assumes a partner API's rate limit or auth model you have no access to confirm). |
| ✅ Blocking | A scope choice that changes WHICH repositories are touched (e.g. "real-time" meaning push notifications vs. polling — one adds a websocket service, the other doesn't). |
| ❌ Should be non-blocking, not blocking | "What should the CSV column order be?" when nothing in the brief or the code implies an order — pick one, state it, recommend it. Guessing wrong here is a one-line fix later, not a wasted implementation. |
| ❌ Should not be a question at all | "What does `TaskRepository.ListByProject` return?" — `get_symbol_skeleton` answers this; escalating it is the Red Flag technical-analysis-workflow already names. |

## Ending the run on a blocking question

A blocking question does not end the run early. Explore everything else first — the report attaches "as far as it got": `summary`, `context`, and as much of `design`/`plan`/`split` as the unanswered question doesn't gate. Then:

1. `record_open_questions` with the blocking question(s) (and any non-blocking ones you also found).
2. `add_task_document` (new) or `update_task_document` (revision) with the partial report.
3. A summary comment stating what's blocked and on what.
4. STOP. The run ending with a pending blocking question parks the task in `blocked` instead of `analiz_review` — do not move it yourself either way.

## Resuming after an answer

You are re-dispatched with payload `{"resumed": "questions_answered", ...}` once the human sends answers, or you see new answers in your run context's "Open questions" block on any later run. Either way:

1. `list_open_questions` if you need the full picture (keys, kinds, every answer) beyond what the context block shows.
2. Continue the report from where it stopped — do not restart it. Revise the SAME document with `update_task_document`, never a second `add_task_document`.
3. Withdraw or replace any question an answer made moot (e.g. answering Q1 removes the premise of Q2).
4. Finish the report and present it the normal way (analiz-human-review-gate).

## In `need_revision` and `done`

Honour every human answer in the revised report, the same way you honour review comments. An **unanswered non-blocking** question means its `recommended_answer` stands as written — do not re-ask it, do not treat silence as a rejection.

In `done` (decomposition, task-decomposition): if a human's answer contradicts the approved `split` or plan in a way the decomposition cannot absorb without re-deciding the design, do NOT decompose. `add_task_comment` naming which answer conflicts with which part of the plan, and stop — the human resolves the plan before you split it.

## Red Flags

- Writing a question into the report's text, or into a task comment, instead of `record_open_questions` — the human never sees an answer box for it.
- Calling (or planning to call) `ask_user` on an analiz task — you do not hold it here.
- A non-blocking question with no `recommended_answer` — refused; you have not actually decided what to do if nobody answers.
- Marking a question blocking because it is inconvenient to guess, not because every guess would waste the implementation.
- Editing an answered question's `prompt` with `update` instead of withdrawing and adding a new one.
- Decomposing in `done` while a human's answer still contradicts the approved split.
- Re-asking an already-answered question, or treating an unanswered non-blocking question as a rejection of your recommendation.
