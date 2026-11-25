---
name: adopt-local-adaptation-review
description: Reviews one team's variation on the agreed way of using AI and drafts a versioned adaptation note with what changed and why, the safeguard it must keep, a bounded test with a rollback, and the owner's decision. Use for "run adopt-local-adaptation-review", "local adaptation review", "teams are changing the AI process", "is this workaround OK", "a team skipped the AI output check", "adaptation or workaround", "review a team's variation on our AI process", "should everyone adopt this team's change", part of the Claude Guide for AI Adoption Pack by 90n.
---
# Local Adaptation Review
## When To Use
Teams are quietly changing the agreed way of working with AI and nobody knows which changes are improvements. One team shortened the output check, another rewrote the shared prompt, a third uses the tool for a task nobody planned. The question this answers: does this one variation still serve the purpose of the step it changed, and who decides whether it stays?

## When Not To Use
Not for looking at the whole practice across teams: that is the AI Habit Review, each quarter. Not for a tweak that touches no check, no rule and no agreement: let it be. You set what counts as worth a note, and most small changes do not.

## Inputs
- The agreed way, as written (the team agreement, the job aid, the library entry, the output check).
- The variation: what the team does instead, since when, and on which work.
- What prompted it, in the team's own words, any results so far, and who owns the process.
If you have none of this, I start from one sentence on what the team does differently, and mark the output as a first draft.

## Approach
The record follows FRAME, the framework for reporting adaptations and modifications published by Wiltsey Stirman, Baumann and Miller in Implementation Science in 2019: what was modified, when, by whom, at what level, whether it was planned, and why. The judgement is that fidelity means keeping the purpose of a step, never copying its surface. Two mistakes sit on either side. Treat every variation as a breach and teams stop telling you what they changed. Wave every variation through and one day the check that caught wrong figures is gone, and nobody decided that.

## Workflow
1. Ask at most three questions: what exactly does the team do differently and since when, what prompted it, and who owns the process this step belongs to.
2. Describe the old action and the new one side by side, exactly, with the local circumstance. Ask the team why before anything else: a workaround is information about the work, not about who broke a rule.
3. Fill the FRAME record: when and how the change was made, planned (an adaptation) or unplanned and reactive (a workaround or a dropped step), who decided, what was modified, at what level (one person's practice, a team, several teams), the nature of the change, and the reason, with the goal and the local circumstance.
4. Name the purpose of the original step and any safeguard it carries: a check, a never-put-in rule, a sign-off. Mark as untested any assumption about what is "core". If the change removes a required safeguard, I mark it paused for the owner's review and go no further on that point.
5. Compare the options (the agreed way, the variation, a third way) on workability, burden, quality and the original purpose. Look for evidence against rigid standardisation and against free customisation alike.
6. Propose a bounded test: which work, for how long (you set it), what is looked at, and a clear rollback condition.
7. Set out the owner's three choices, keep locally, adopt for everyone or revert, and draft the note with its version and date. If the choice is "adopt for everyone", the team agreement needs revising, and the note says so.

## Output Format
```markdown
# Local Adaptation Note
**Step concerned:** [step of the agreed way] · **Team:** [team] · **Process owner:** [name] · **Version:** [n], [date]
## What changed
| | Agreed way | Variation |
|---|---|---|
| Action, and on which work | [what the step says, scope] | [what the team does, scope] |

## The record
| Question | Answer |
|---|---|
| When and how it was made, planned or reactive | [date, how], [adaptation / workaround / dropped step] |
| Who decided, and at what level | [role or team, never a person singled out], [one person's practice / a team / several teams] |
| What was modified, and the nature of the change | [content of the step, order, tool, prompt, check], [shortened, added, replaced, removed, reordered] |
| Reason | [goal, and the local circumstance] |

## Purpose and safeguard
Purpose of the original step: [purpose]. Safeguard it carries: [check, never-put-in rule, sign-off, or none]. Faithful to the purpose: [yes / partly / no], because [reason]. Paused for the owner's review: [yes, which point / no].
## Options
| Option | Workability | Burden | Quality | Serves the purpose |
|---|---|---|---|---|
| [agreed way / variation / third way] | [in words] | [in words] | [in words, with evidence] | [yes / partly / no] |

## Test and rollback
Test on [work] from [date] to [date]. Looked at: [what, from which source]. Roll back if: [condition]. Back to: [the agreed way, how].
## Decision
[Process owner name] decides by [date]: keep locally, adopt for everyone, or revert. If adopted for everyone: [who revises the team agreement, by when].
```

## Done When
- Old and new actions are described exactly enough that a third team could do either.
- Every row of the record is filled or marked unknown, with who could say.
- The purpose and the safeguard are named, any removed safeguard is marked paused, and the test has an end date and a rollback condition.

## Quality Bar
- The team is asked why first. Their reason goes in the note in their words.
- "Core" is a claim to test with the process owner, and the note records a team's practice: it never names who skipped a step.
- A variation that works for one team is not shown as working for all until it has been tried elsewhere.
- The team that adapted is asked why, not blamed; the process owner decides and no safeguard is dropped quietly.

## Next
Run adopt-ai-rollout-decision (AI Rollout Decision) to carry what teams learned into the decision to expand.

## About the makers
This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).