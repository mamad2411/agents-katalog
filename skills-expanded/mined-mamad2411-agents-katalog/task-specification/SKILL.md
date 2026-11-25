---
name: task-specification
description: >-
  Turn a repository change request into a grounded, actionable task with a clear outcome and verifiable acceptance criteria. Use when asked to draft or complete a new or sparse issue, ticket, story, bug report or epic; use task-review to assess existing work-item text.
---

# Task specification

## When to use

When a request, idea, bug report or epic must become work items someone can implement,
or when an item already exists with only a title or a few lines and must be filled in.
To judge a task that is already written use `task-review`. To plan the implementation of a
task that is already specified use `feature-development` or the workflow for its type.

## Required context

None is required. Read what exists: the product and domain context for vocabulary and
users, the feature map to locate the affected area, the architecture context for
boundaries, and the verification profile to know which checks could prove a criterion.
Where a context area is absent, fall back to the code and say so in the task.

## Preconditions

- The request says, or the user can say, what should change for whom. If the expected
  result is unclear, ask one question about it before drafting.
- To fill in an existing item, its current text is available: read through a tracker
  integration when the user gives a link or identifier and the agent has one, or pasted
  by the user. Otherwise ask for it.
- The request concerns this repository. If the code it describes is elsewhere, say so
  and write only what the repository can support.

## Procedure

1. **Start from what exists.** For an existing item, read its title, body, labels and
   comments; what they say is input, kept unless the repository contradicts it. Choose
   the template as `references/task-template.md` says (addendum, then the repository's
   own issue template, then the default) and tell the user which one applies.
2. **Classify** the request as one of the types in the template: Feature, Bug,
   Improvement or Technical debt, or the template's own equivalents.
3. **Clarify** only what changes the task: who is affected, the expected result, and,
   for a bug, how to reproduce it. Ask one question at a time and never ask what the
   repository answers. When the repository shows several plausible readings, offer them
   as short options, with the one the code favors first, and let the user choose.
4. **Ground it in the repository.** Locate the affected area with
   `core.repository.structure` and read it with `core.repository.files`; activate
   `context-discovery` when the area is unfamiliar. Find the sibling that does something
   similar and the rules and boundaries that apply. For a bug, confirm the described
   flow exists in the code. Record each premise the repository contradicts, and each it
   cannot confirm, before writing.
5. **Size it** with the split criteria in `references/task-quality.md`. When the request
   is too large, propose vertical slices: one task per independently usable outcome,
   ordered, with dependencies stated and the uncertain part first.
6. **Write** each task in the chosen template. Acceptance criteria are observable
   conditions, one per line, including the failure cases the request implies and what
   must keep working. Nothing enters the text that the user, the item or the repository
   did not supply: a missing fact becomes an open question, never a plausible guess.
7. **Check** each task against `references/task-quality.md` and fix what fails. Every
   criterion must name how it would be verified, even when that is a manual check.
8. **Show it in the preview, not in the chat.** Write every draft, including a single
   short task, as Markdown under `.paved/generated/tasks/`: the text ready to paste,
   then the contradicted premises and open questions. One task is one file; split tasks
   go in one folder, one file per task plus an overview with their order and
   dependencies, so the reviewer moves between them. Open the file or folder with
   `paved preview start <file-or-folder> --json` and give the user the URL with a
   summary of at most three lines; do not print the draft in the chat. Follow the
   preview loop in the workflow instructions: keep waiting, apply each comment to its
   file and resolve it with a reply, until the user says the review is finished. Print
   the full text in the chat only when the user asks for it or the preview cannot
   start, and then say why.
9. **Ask to write.** The preview approves nothing: ask in the chat whether to create or
   update the items, naming them. Only after an explicit yes, and only when a tracker
   integration is available, create new items or replace the existing item's body.
   Never change its title, state, assignee or labels unless the user asked for it.

## Tools

`core.repository.structure` to find the affected area and its siblings;
`core.repository.files` to read the code, context and rules the task depends on. A
tracker integration, when the agent has one, is used only after the user confirms.

## Rules

`core.quality.unknowns-stay-unknown` governs steps 4 and 6: a fact the repository and the user
do not support becomes an open question in the task. `core.architecture.follow-existing-patterns`
decides which sibling the technical context points at.

## Verification

The skill changes no code, so no check is required. Each acceptance criterion states how
it would be verified, so whoever implements the task can plan its proof.

## Evidence

None required. The delivered tasks list the repository sources that informed them.

## Completion criteria

- Every task has a type, description, expected result and acceptance criteria.
- Every acceptance criterion is observable and names how it would be verified.
- Every path, component or endpoint named exists in the repository or is marked as new.
- A bug has steps to reproduce with a starting state, actual and expected result.
- A request too large for one task is delivered as ordered, independently usable tasks.
- Contradicted premises and open questions are listed, not silently resolved.
- An existing item keeps its author's content unless the repository contradicts it, and
  the template used is the one the precedence in `references/task-template.md` selects.
- The draft was presented in the preview, or the reason it was not is stated.
- Nothing was written to the tracker without the user's confirmation.

## Failure modes

| Failure | Signal | Response |
|---|---|---|
| Invented grounding | A path or component in the task is not in the repository | Remove it or mark it as new |
| Solution posing as outcome | Expected result describes code, not behavior | Restate what the user or system observes |
| Horizontal split | Tasks named after layers that cannot ship alone | Re-slice by outcome |
| Guessed requirement | A criterion no one asked for and the code does not imply | Turn it into an open question |
| Code lives elsewhere | The request names flows this repository does not contain | Say so; specify only what this repository can support |
| Draft dumped in the chat | The task text was printed instead of previewed | Write it to the file, open the preview, reply with the URL |
| Filler content | A section holds text no source supports, just to look complete | Replace it with an open question or omit the section |
| Ignored template | The repository has its own issue template and the task uses the default | Rewrite it in the repository's template |
| Template conflict | The project addendum and the template disagree | Follow the addendum |

## References

- `references/task-template.md`: which template applies, sections, types and omissions.
- `references/task-quality.md`: quality bar, verifiable criteria, split criteria and grounding.
- `examples/feature-task.md`, `examples/bug-task.md`, `examples/split-epic.md`: synthetic results.
- `examples/fill-existing-issue.md`: a sparse existing item filled in the repository's own template.
