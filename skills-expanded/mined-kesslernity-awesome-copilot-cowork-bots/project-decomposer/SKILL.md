---
name: project-decomposer
description: Breaks a project, initiative or goal into owned tasks, each carrying its own verification criteria and a named owner, and returns one Adaptive Card per task. It plans and does not execute. Use when the user asks to break down a project, decompose an initiative, turn a goal into tasks, work out who does what, or says a project is too big to start.
---

# Project Decomposer

Turns a project into tasks somebody can actually finish, each with a stated way to tell it is done.

**This skill does no work.** It decomposes and stops. If a task it produces looks like something
Cowork could do, that is a separate request the user makes deliberately.

## Inputs

- A project description from the user, or a named document found through **Enterprise Search**
- Existing context: prior decisions, related threads, the people already involved
- `references/config.md` for team names, the default task size and the house verification bar

## Procedure

1. **Read the goal.** Restate it in one sentence. If the restatement is longer than one sentence,
   the project is two projects: say so and ask which one to decompose.
2. **Find the real constraints.** Search mail and files for stated dates, named owners, approvals
   already given, and anything previously tried. Decomposing against invented constraints is worse
   than not decomposing.
3. **Break into tasks** at the level where one named person could finish one task in the default
   size from config. Not phases. Not workstreams. Tasks.
4. **For every task, write all five fields.** A task missing any of them is not a task yet:
   - **What** happens, in a verb phrase
   - **Owner**, a named person or a stated vacancy. Never "the team"
   - **Done when**, the verification criteria: what somebody checks to agree it is finished
   - **Blocked by**, naming the task or decision it waits on, or "nothing"
   - **Evidence**, the link to where the requirement came from, or "assumed" if you inferred it
5. **Order** by dependency, then write the critical path in one line.
6. **Return one Adaptive Card per task**, plus a summary card carrying the goal, the task count,
   the critical path and every open vacancy.

## The verification bar

"Done when" is where most decomposition fails. These are not acceptable:

- "When it's finished"
- "When the team is happy"
- "When reviewed"

These are:

- "When the signed PDF is in the contracts library"
- "When the test suite passes on main and the owner has posted the run link"
- "When three named stakeholders have replied approving in writing"

If you cannot write a checkable "Done when" for a task, the task is still too vague. Split it or
say plainly that it needs a decision before it can be planned.

## Output

One summary Adaptive Card, then one card per task. Also write the whole set to
`/Documents/Cowork/output/decomposition-<project>-YYYY-MM-DD.md` so it survives the session.

## Definition of done

Every task has all five fields, every "Done when" is checkable by someone other than its owner,
and the critical path is one line.

**Returning fewer tasks is usually better.** A decomposition with 9 real tasks beats one with 30
where half are "coordinate" and "follow up". If the project genuinely resists decomposition, say
what is missing rather than padding the list.

## When there is no data

- The goal is unclear: ask one question and stop. Do not decompose a guess.
- No owners can be identified: write the vacancies explicitly as "OWNER NEEDED" and count them in
  the summary. A plan with named gaps is useful; a plan with invented owners is not.
- No dates found anywhere: say so. Do not invent a schedule.

## Boundaries

- **Plans only.** Never create tasks in Planner or To Do, never send anything, never book time.
- Never assign a named person who has not already been associated with this work in the evidence.
  Proposing an owner is fine when it is labelled as a proposal.
- Never state a date as agreed unless the evidence shows it was agreed.

## Self-check before returning

- Does every task have all five fields?
- Could a stranger check every "Done when" without asking the owner?
- Is every owner evidenced, or labelled as proposed, or marked OWNER NEEDED?
- Did I avoid creating anything, and only plan?
