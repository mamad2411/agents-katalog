---
name: cyc-correct
description: "Turn user feedback or a repeated miss into a named missing criterion and a targeted fix, instead of another variant. Use when the user says \"that's not it\", \"still wrong\", or \"this feels off\", when a revision misses the same way twice, or when feedback reveals an unstated requirement."
---

# Turn feedback into a correction

A correction is information: it tells you which criterion was missing or which mental model was wrong. Producing another variant without finding that is guessing. Follow the [handoff contract](../../docs/skill-contract.md).

## The core loop

1. **Quote the feedback exactly.** Keep the user's words separate from your interpretation.
2. **Locate the mismatch in the artifact.** Point at the part that fails. For vague feedback ("feels disconnected", "too busy"), check the structural causes first: grouping, order, transitions, and the user's path through it. Spacing and color are usually symptoms.
3. **Name the missing criterion.** Write it as an observable check: "Each section leads into the next with a visible connection." Add it to the task's criteria. Existing criteria stay unless the user removes them.
4. **Classify it.** Is it a fact about this task, the user's preference, a project convention, or a reusable rule? Only the task fact goes into the current frame by default. The others are candidates for [Reflect](../cyc-reflect/SKILL.md) and need the user's say-so before they become rules.
5. **Pick the responsible stage.** Wrong code: fix it in [Build](../cyc-build/SKILL.md). Wrong goal, missed dependency, or wrong shape: rethink the plan (`run retry --stage scout` in fast playbooks; [Frame](../cyc-frame/SKILL.md), [Impact](../cyc-impact/SKILL.md), or [Design](../cyc-design/SKILL.md) in the detailed chain).
6. **Fix the cause, then check both.** Check the new criterion and the old ones together. A fix that satisfies the feedback but breaks an earlier requirement is not a fix.
7. **If unsure what they mean, restate before revising.** Re-pitch the problem in plain language ("So the issue is that the steps don't feel like one journey, not that it looks cluttered?") rather than guessing with another draft.

## Codify manual checks

If the feedback came from the user checking something by hand ("the page jumps when it loads", "the console shows an error", "it takes three seconds"), that is a missing verification step. Add it to the project's verify recipe as a measurable check (see [Verify](../cyc-verify/references/recipe.md)) so the next run catches it without the user. During an active run, record it in `.cyc/runs/<runId>/proposed-checks.json` and apply it after the run completes.

## Done when

The feedback maps to a named criterion, the criterion is recorded with the task, the fix addresses its cause, and both new and existing criteria were checked.

## Stop rule

Two corrections on the same point that both missed: stop revising. Write down the assumption both attempts share and ask the user one sharp question that tests it.

## Anti-patterns

| Name | The tell | Fix |
| --- | --- | --- |
| Variant spray | Producing three new versions after "not quite" | Name the missing criterion first |
| Surface fix | "Feels off" answered by changing padding | Check structure and journey first |
| Silent drop | The fix quietly removes an earlier requirement | Recheck all criteria together |
| Global from local | One correction becomes a permanent rule | Classify it; ask before promoting |

## Handoff

Return the quoted feedback, the named criterion, its classification, the stage that fixed it, and the check results.
