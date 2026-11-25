---
name: adopt-barrier-diagnosis
description: Builds an AI adoption barrier map from one occasion when the use happened and one when it did not, with competing explanations, evidence for and against each, the smallest respectful check and a support matched to each barrier. Use for "run adopt-barrier-diagnosis", "AI adoption barrier diagnosis", "people are not using the AI tool", "why is nobody using AI", "do we need another AI training", "find the real barrier to AI use", "barrier map", "AI adoption is stuck", part of the Claude Guide for AI Adoption Pack by 90n.
---
# AI Adoption Barrier Diagnosis
## When To Use
People are not using it, and the first proposal is another training. Before anyone books a room, you want to know whether the cause is know-how at all, or time, tools, access, permission, an unclear rule, doubt that it helps, or disagreement with the change. This skill answers: what is really in the way of this one use, and what support fits it.

## When Not To Use
Not for hearing from everyone at once: AI Starting Point Survey asks the whole group anonymously, and this diagnosis needs real episodes of one intended use. Once time is confirmed as the barrier, Adoption Capacity Check sizes the gap in detail.

## Inputs
- The intended use, as one sentence: which role does what with AI on which task.
- One occasion when that use happened and one when it did not: what the task was, what the person had to hand, what happened. No names.
- What you saw yourself and what you were told, kept apart, plus anything known about access, licences, the rules and the workload in that team.
If you have none of this, I start from the intended use and your own first explanation, and mark the output as a first draft.

## Approach
The diagnosis uses capability, opportunity and motivation, the COM-B model from Michie, van Stralen and West (2011, an open access article in Implementation Science), and it reverses the usual order of suspicion: opportunity is checked first, capability second, motivation last. Training answers only a capability barrier. The reasons non-users give in Gallup's 2026 workplace surveys (preferring the current way, privacy and compliance worries, doubt that it helps their work, ethical objection) are a useful prompt for what to listen for, not a finding about your team. The failure this prevents is the third workshop for a team whose access request has been sitting in a queue since the first one.

## Workflow
1. Ask up to three questions: what is the intended use, what happened on one occasion when it took place and one when it did not, and what is your own first explanation. I keep your explanation as one hypothesis among several.
2. Lay the two episodes side by side and separate what was observed from what was reported. The difference between them is usually the best clue: same person, same task, different week.
3. Walk the six cells in this order. Opportunity, physical: time, tools, access, licence. Opportunity, social: permission, what the manager and peers do, unclear rules. Capability, psychological: knows how. Capability, physical: can actually do it in the tool. Motivation, reflective: sees the point, doubts, disagrees. Motivation, automatic: habit, the old way is faster under pressure.
4. Write competing explanations, at least one from opportunity. For each: evidence for, evidence against, who could verify it, and the smallest respectful check, which is a question or a look at the workflow and never a test of a person.
5. Pick one or two barriers by how often they show and what they cost. Mark confidence in words (well supported, plausible, a guess). No numeric score. Disagreement with the change is recorded as a position with its reasons.
6. Match each picked barrier to a support: an access fix, time made, a clearer rule, practice on real work, a redesigned handoff, or reconsidering the change itself. Training appears only against a capability barrier. Set a check that the barrier actually reduced, with an owner and a date, and list what is still unverified.

## Output Format
```markdown
# AI Adoption Barrier Map
Status: [first draft / verified on [date]] · Intended use: [role, action, task]
## Two episodes
| | When it happened | When it did not |
|---|---|---|
| Task and situation | [description] | [description] |
| Observed | [what was seen] | [what was seen] |
| Reported | [what was said, by role] | [what was said, by role] |

## Competing explanations
| Cell | Explanation | Evidence for | Evidence against | Who could verify | Smallest respectful check |
|---|---|---|---|---|---|
| [Opportunity, physical] | [explanation] | [evidence] | [evidence] | [role] | [question or look at the workflow] |
| [Opportunity, social / Capability / Motivation cell] | [explanation] | [evidence] | [evidence] | [role] | [check] |

## Barriers picked and the support matched to each
| Barrier | How often it shows, what it costs | Confidence (in words) | Support | Owner | Check that the barrier reduced, and date |
|---|---|---|---|---|---|
| [barrier] | [in words, from the episodes] | [well supported / plausible / a guess] | [access fix / time made / clearer rule / practice on real work / redesigned handoff / reconsider the change] | [name] | [what would be seen, by [date]] |

## Still unverified
- [Explanation or assumption], to be checked by [name] by [date].
## Decision
[Sponsor or team lead name] decides by [date] which support goes ahead and whether the proposed training is still needed, after [name] has run the checks above.
```

## Done When
- Both episodes are described, with observed and reported kept apart.
- Opportunity was examined before capability and motivation, and the map shows it.
- Every explanation has evidence for and against, or is marked "no evidence yet".
- Every support answers a picked barrier and has a check, an owner and a date.

## Quality Bar
- Silence is not read as motivation: a missing use is never explained by attitude without evidence.
- The six cells describe a situation; they never become a profile or a type of person, and the map names no one.
- Nothing is invented: no observation, view, frequency or figure the user did not supply.
- One or two barriers, not six; and if the evidence points at the change itself, the map says so plainly.
- Barriers are conditions of the work, never labels for people; concerns are not called resistance.

## Next
Run adopt-ai-pilot-plan (AI Pilot Plan) to test the change with the barriers addressed.

## About the makers
This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
