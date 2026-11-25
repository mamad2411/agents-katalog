---
name: sideroom-user-stories
description: "Write, revise, review, or split user stories and their acceptance criteria from a brief or existing ticket. Use for functional stories and technical enablement tickets, independent of the issue tracker. Use sideroom-grill for an open feature plan; this skill owns the resulting story, not implementation or ticket publication."
license: MIT
metadata:
  author: RMRdeveloper
  version: "1.0"
---

# Sideroom user stories

## Scope and authority

Produce stories that product, development, and QA can interpret alike without
reconstructing the conversation. Write in the user's language, preserving the
project's domain terms.

Writing or reviewing a story authorizes text in the conversation only. Save a
file, publish or edit a remote ticket, set metadata, or change workflow state
only when the user requests that action. Story work does not authorize
implementation, glossary edits, or architectural decisions.

## Workflow

1. **Read the available facts.** Start with the brief or existing ticket and
   the relevant project conventions, glossary, approved specs, and linked
   dependencies. Inspect code only for facts needed to distinguish current
   behavior from the requested change; code does not establish product intent.
   Reuse local ticket conventions, including required fields, without
   importing another project's roles, boards, labels, estimates, or priorities.
   If the tracker is available, search the relevant project for duplicates
   before proposing a new ticket. Otherwise state that duplicates were not
   checked; do not claim uniqueness or invent issue keys.
2. **Identify the need.** State the actor receiving value, the capability,
   the useful result, and the boundaries. Prefer a complete user outcome over
   separate UI, API, and persistence stories. Split independently valuable
   outcomes; use technical tasks for coordination or honor an explicitly
   approved project split. Each proposed story must retain a clear result and
   explain any real dependency.
3. **Resolve material gaps.** Ask through `sideroom_ask` only about missing
   facts or decisions that change scope or acceptance. Load
   `../sideroom-grill/SKILL.md` when the broader feature plan is open, or
   `../sideroom-architecture/SKILL.md` for an unresolved architectural choice.
   Reuse settled answers rather than repeating an interview. If clarification
   is unavailable or the user wants a draft, mark it as a draft and list open
   questions separately. Never turn a proposed permission, rule, metric,
   dependency, or error response into an agreed requirement.
4. **Draft the story.** Read [templates](references/templates.md) before
   drafting or rewriting. The normal output is a result-oriented title, a
   story sentence, scope, and acceptance criteria. Add other sections only
   when they clarify a real condition. A technical enablement story names
   its consumer and the capability it enables. For a bug, use the bug format
   instead of forcing a story sentence.
5. **Review the result.** Read [review guidance](references/review.md) before
   returning a draft or review. Trace each criterion to scope or a business
   rule; remove accidental new work and repeated content. Check the successful
   path and only the failure or boundary cases that can change the result.
   A story is ready for review when each criterion has an objective pass/fail
   result and no unresolved question changes the promised behavior. If that
   gate fails, return the draft with its blockers, not a readiness claim.

## Output boundaries

For a review, report concrete ambiguities, missing outcomes, or unsupported
requirements; propose corrected wording without silently expanding scope.
For a split, show each story and explain the actual dependency between them.

Keep the ticket focused on need, behavior, rules, and observable results.
Implementation steps, source paths, logs, and routine lint/build commands
belong in implementation records. Link approved design decisions when needed;
include their relevant behavioral consequences in the ticket itself. Technical
contracts belong in acceptance only when they define the agreed deliverable.

When publication is requested, confirm the destination and required metadata
from project facts or the user, check duplicates, and explain blocking links
in the correct direction: the prerequisite blocks the dependent. Report what
was actually saved; if access or required facts are missing, return the draft
and the missing information instead of claiming publication.
