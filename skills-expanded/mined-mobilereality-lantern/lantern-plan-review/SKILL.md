---
name: lantern-plan-review
description: Show a Lantern plan to the user one section at a time and record each approval, then the plan-level approval. Use at steps 5 and 6 of `lantern-plan`, and whenever the user asks to "show me the plan", "review the plan", "approve the plan", "go through the plan with me", "pokaż plan", "zatwierdź plan", or when a plan has sections changed since they were approved. An approval is the user's explicit yes to what was shown; nobody else gives it. Not for writing the plan (`lantern-plan-stages`) or running it (`lantern-plan-handoff`).
---

# Lantern plan: review and approve

The plan is reviewed in pieces so the user can say yes to a goal and no to a stage. Sections, in order:
`title`, `goal`, `scope`, `impact`, one per stage (`s1`, `s2` ...), `risks`. `$P` is the `lantern-plan` folder.

## One section at a time

When you edit or add plan text, write it in the map's primary language (`node $L/scripts/lang.mjs .`); keywords, ids and file paths stay as they are.

1. `plan.mjs show <slug>` prints each section with its state (`pending`, `approved`, or `stale` when it
   changed after approval) and names the next one to review.
2. `plan.mjs show <slug> <section>` prints that section as written. Show **only that section**, in plain
   words, short: what it says, and for a stage its items with their checks and its open questions. Do not
   paste the whole plan and do not show the next section yet.
3. Ask for one of three answers: approve, change, question. Wait for it.
4. **Approve**: `plan.mjs approve <slug> <section> --by <name>`. `<name>` is how the user wants to be
   recorded; ask once and reuse it. Then show the next pending section.
5. **Change**: edit with `plan.mjs add` or by hand, run `plan.mjs check <slug>`, show the section again.
   Editing a section takes its approval back; that is intended.
6. **Question**: answer from the map and the plan. If the answer changes the plan, it is a change.

A section with no lines (a plan with no risks) is still shown, as "none named", and approved.

A stage's open questions belong in its review: ask them there. If the user answers, record it with
`plan.mjs add <slug> answer <question id> <who> <text>`; if not, leave it open. It will be asked again
before that stage is delegated, and it does not stop the approval. The user may instead answer in Lantern
and paste the text it copies; handle that as `lantern-plan-stages` says ("Answers pasted from Lantern").

## The plan

When every section is `approved`, `plan.mjs show <slug>` says so. Ask once more for the whole plan, then
`plan.mjs approve <slug> plan --by <name>`. It refuses while any section is pending or stale.

Then commit the plan file with the `lantern-commit` skill (`docs: plan <slug>`), and push only if the user says so.
An approved plan is what `lantern-delegate` forks from; it has to be on the base the delegates fork from.

## Rules

- **Only the user approves.** Never run `approve` on your own judgement, for a section they did not see,
  or on a silence. "Looks good" after a section is a yes to that section only.
- **"Approve everything"** is fine after the user has seen every section in this conversation. Show a list
  of the sections first, then approve each one.
- **A stale section is shown again** before the plan can be approved. If the plan was already approved and
  you edit it, `check` fails until the changed sections and then the plan are approved again.
- Do not soften what is open. Say how many questions are unanswered and in which stage.
