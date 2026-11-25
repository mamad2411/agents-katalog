---
name: task-review
description: >-
  Review an existing task, issue, ticket, story, bug report or epic for missing context, unsupported assumptions, unverifiable criteria and scope. Use when asked to assess or refine work-item text before implementation; use task-specification to write a new item and change-review to review code.
---

# Task review

## When to use

When a task already written by anyone must be judged ready or improved before someone
implements it. To write a task from a request use `task-specification`. To review code
that implements a task use `change-review`.

## Required context

None is required. Read the same context `task-specification` reads (product, domain,
feature map, architecture, rules, verification profile), because the review judges the
task against what the repository says.

## Preconditions

- The task text is available: pasted by the user, or read through a tracker integration
  when the user gives a link or identifier and the agent has one. Otherwise ask for the
  text.
- The task concerns this repository. If its code lives elsewhere, review only its form
  and say the repository could not be checked.

## Procedure

1. **Read the task** whole, including comments or subtasks the user supplied, and state
   its intent in one sentence. Everything below is judged against that intent.
2. **Check the form** against the template and the per-section bar of the
   `task-specification` skill, in its directory next to this one
   (`../task-specification/references/task-template.md` and
   `../task-specification/references/task-quality.md`). Use the template that file's
   precedence selects, so a repository with its own issue template is judged by it:
   sections present, type consistent with the content, criteria observable and one per
   line, steps to reproduce for a bug, and the ready-to-implement bar.
3. **Check it against the repository.** With `core.repository.structure` and
   `core.repository.files`, confirm that each path, component, endpoint, screen or
   configuration the task names exists or is marked as new. Look for premises the code
   contradicts, other consumers of the affected area the task ignores, rules or
   boundaries the described change would break, and a pattern to follow it should name.
4. **Check the size** with the split criteria. A task that fails them gets the vertical
   slices `task-specification` would propose.
5. **Classify** each candidate. A *blocking* finding stops someone from implementing the
   task as written: a missing expected result or criteria, a criterion no one could
   verify, a premise the code contradicts, a change a project rule forbids, a missing
   reproduction for a bug, or a size that needs splitting. Any other candidate is a
   *note*. Discard candidates that are preferences, or that depend on facts you cannot
   point at in the task or the repository.
6. **Validate** each blocking finding before recording it: re-open the file or rule it
   cites and confirm the problem exists as stated. Drop what fails. Each finding names
   its source: the task section, the path or the rule.
7. **Decide the verdict**: `ready` (no blocking finding), `needs changes` or
   `needs split`.
8. **Rewrite** the task in the template, fixing every finding the repository or the task
   itself can settle, or propose the split tasks. Keep the author's intent and wording
   where they were fine; never add a fact the task, the user or the repository does not
   support. A finding only a human can settle becomes an open question in the rewritten
   task, or, when the repository shows a few plausible answers, a short set of options
   for the user to choose from.
9. **Present it in the preview.** Put the verdict, the findings, what changed and the
   rewritten task in one Markdown file under `.paved/generated/tasks/`; for a split, use
   a folder with the review as its first file and one file per proposed task. Open it
   with `paved preview start <file-or-folder> --json` and reply in the chat with the
   URL, the verdict and the count of blocking findings only. Run the preview loop from
   the workflow instructions, applying each comment and resolving it with a reply,
   until the user says the review is finished. Fall back to the chat only when the user
   asks for it or the preview fails to start, and say which.
10. **Apply** only after an explicit yes in the chat to the exact text; the preview
    approves nothing. If a tracker integration is available, then update the task's
    description. Never close, move, reassign or delete the task.

## Tools

`core.repository.structure` and `core.repository.files` for step 3. A tracker
integration, when the agent has one, reads the task in the preconditions and updates it
in step 10 only after the user confirms.

## Rules

`core.quality.unknowns-stay-unknown`: a gap the repository cannot fill is an open
question, never a guessed answer in the rewrite. `core.architecture.follow-existing-patterns`
decides which sibling the rewritten technical context points at.

## Verification

None is required of the review. The rewritten task states how each criterion would be
verified.

## Evidence

A review artifact: the verdict, blocking findings with their source, notes listed
apart, and what was checked in the repository.

## Completion criteria

- The verdict is one of `ready`, `needs changes` or `needs split`.
- Every blocking finding names its source and was validated against it.
- The rewrite or the split tasks meet the quality bar and keep the author's intent.
- Open questions only a human can settle are listed, not answered by guess.
- The review was presented in the preview, or the reason it was not is stated.
- The tracker was changed only after the user confirmed the exact text.

## Failure modes

| Failure | Signal | Response |
|---|---|---|
| Rubber stamp | `ready` for a task with vague criteria | Apply the verifiable criteria bar line by line |
| Pedantry | Findings are about wording while criteria are unverifiable | Revisit steps 2 and 3 first |
| False contradiction | A finding says something is missing, but it lives in another repository | Say the repository could not confirm it; ask |
| Silent rewrite | The corrected task changes scope without a finding explaining why | Add the finding or restore the author's scope |
| Invented fix | The rewrite fills a gap with a plausible answer no source supports | Make it an open question or offer options |
| Review dumped in the chat | The findings and rewrite were printed instead of previewed | Write them to the file, open the preview, reply with the URL |
| Unconfirmed write | The tracker changed before the user saw the text | Stop; always show and ask first |
| Template conflict | The project addendum and the template disagree | Follow the addendum |

## References

- `examples/task-review.md`: a weak task, its findings and its rewrite.
