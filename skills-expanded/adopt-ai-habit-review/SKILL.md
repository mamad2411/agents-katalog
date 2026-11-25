---
name: adopt-ai-habit-review
description: Prepares a quarterly AI habit review with the original need, current evidence against the same definitions, what changed in the tool and the work, and what to keep, simplify, refresh or retire. Use for "run adopt-ai-habit-review", "AI habit review", "quarterly AI adoption review", "people went back to the old way", "is our AI rollout still working", "what should we retire from the AI programme", "refresh our AI training materials", "AI adoption six months later", part of the Claude Guide for AI Adoption Pack by 90n.
---
# AI Habit Review
## When To Use
The launch was six months ago, the tool has changed three times, and half the team is back to the old way. Nobody has looked since at whether the practice still fits the work, and the materials describe a product that no longer exists. The question this answers: does this practice still earn its place, and what do we keep, simplify, refresh or retire?

## When Not To Use
Not for one team's variation on the agreed way: that is the Local Adaptation Review. Not for the first full read of results after the pilot: that is the AI Adoption Evidence Review. This review comes later, each quarter, and re-reads against the same definitions.

## Inputs
- The original brief: the need, and the work change per role.
- Current evidence on the agreed measures, from the team's own records, at team level.
- What changed since launch in the tool, the rules, the work and the team, the materials in use, and who owns the practice.
If you have none of this, I start from one paragraph on what was launched and what you see now, and mark the output as a first draft.

## Approach
The questions come from the ten factors of the Sustainability Model, a public guide from the NHS Institute for Innovation and Improvement, grouped under process, staff and organisation, with the maintenance question of RE-AIM: is it still in use after a period you set. The source model has a scoring system. I do not use it, and the review produces no total, because a number invites people to argue about the number. The failure this prevents is the review that defends the launch: it counts what is still running, calls permanence success, and never asks whether the need has moved.

## Workflow
1. Ask at most three questions: what do you believe has changed since launch, which measures and definitions were agreed at the start, and who owns the practice now.
2. Start from the original need in the brief, before defending what was installed. If the need has moved, say so first: everything after is read in that light.
3. Read current evidence against the SAME measure definitions as before, and answer the maintenance question at team level: still in use after [period], on which work. A changed definition is flagged, never silently compared.
4. Put the ten factors as questions and answer each in words with the evidence behind it. Process: are there benefits beyond the main aim, are the benefits credible to the people doing the work, can the practice adapt when the tool or the work changes, is progress of the change still being followed. Staff: were people trained and involved, do they feel able to raise problems and try changes, are senior leaders still engaged, are respected practitioners still engaged. Organisation: does it fit goals and culture, is the infrastructure in place (access, time, roles, materials).
5. List what changed in the tool and in the work since launch, then test the materials: could a new starter learn the practice from them as they are today?
6. Sort into four lists: keep, simplify, refresh, retire. Materials, library entries, temporary rules that became permanent by accident, reports nobody reads. The owner checks dependencies and retention needs before anything is deleted. I delete nothing.
7. Name the owner and the next trigger: a date and an event (the tool changed, the rules changed, the team changed). Where people went back to the old way, record what that tells you about fit, not who did it.

## Output Format
```markdown
# AI Habit Review
**Practice reviewed:** [role, action, task] · **Quarter:** [period] · **Owner:** [name] · Draft status: [first draft / agreed on date]
## The original need and what changed
[The need in the brief.] Still the need today: [yes / partly / no], because [reason].
Changed in the tool: [changes]. Changed in the work: [changes]. A new starter can learn it from the current materials: [yes / partly / no, what is missing].
## Evidence against the same definitions
| Measure (definition unchanged) | At launch or last review | Now | Source and date | Other explanations |
|---|---|---|---|---|
| [measure, team level] | [value or description] | [value or description] | [source, date] | [case mix, timing, team change] |

Still in use after [period]: [where yes, where not, at team level]. What this does not show: [limits].
## The ten questions
| Group | Each question, answered in words with its evidence |
|---|---|
| Process | Benefits beyond the main aim: [answer, evidence]. Benefits credible to the people doing the work: [answer, evidence]. Able to adapt when the tool or the work changes: [answer, evidence]. Progress of the change still followed: [answer, evidence]. |
| Staff | People trained and involved: [answer, evidence]. People able to raise problems and try changes: [answer, evidence]. Senior leaders still engaged: [answer, evidence]. Respected practitioners still engaged: [answer, evidence]. |
| Organisation | Fits goals and culture: [answer, evidence]. Infrastructure in place (access, time, roles, materials): [answer, evidence]. |

## Keep, simplify, refresh, retire
| Item | List | Reason | Dependency checked by |
|---|---|---|---|
| [material, library entry, temporary rule, report] | [keep / simplify / refresh / retire] | [reason] | [name, date] |

## Decision
[Owner name] decides by [date] what is kept, simplified, refreshed and retired. Next review: [date], or earlier if [the tool, the rules or the team changes].
```

## Done When
- The original need is restated and a line says whether it still holds.
- Every measure is read against its original definition, or the change of definition is flagged, and all ten questions have an answer in words with evidence or "not known, ask [role]".
- Every item on the retire list has a dependency check with a name against it, and the next trigger is a date and an event.

## Quality Bar
- No sustainability score, no total, no traffic lights standing in for one. "Progress followed" means the change: no list of who went back to the old way.
- Evidence is the team's own records at team level; small groups are merged or left out, and counts sit beside percentages.
- Retiring something is a result. A practice that no longer fits can be stopped, and the review says so plainly.
- No saving is reported unless your own evidence shows it, with its source and date.
- The review asks whether the practice still earns its place, at team level; going back to the old way is read as information, never as a failing of people.

## Next
Run adopt-ai-adoption-brief (AI Adoption Brief) to write the brief for the next change when the review shows the need has moved.

## About the makers
This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).