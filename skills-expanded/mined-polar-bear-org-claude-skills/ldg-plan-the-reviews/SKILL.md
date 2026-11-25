---
name: ldg-plan-the-reviews
description: Drafts a review plan to agree before the build, with who reviews what at each of four gates, one named decider, rounds and dates, a feedback log and a change rule for late requests. Use for "run ldg-plan-the-reviews", "SME review process", "the revisions never end", "too many reviewers", "conflicting feedback", "review and sign-off plan", "scope creep on the course", "who signs off the course", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Plan the Reviews

## When To Use
Six departments review one course and the revisions never end. Use this before the build starts, while scope is still agreed and nobody has a draft to rewrite, or mid-project when the comments have started to contradict each other. It answers: who checks what at which gate, who breaks a tie, how many rounds there are, and what a late request costs.

## When Not To Use
If you need the whole schedule, with phases, owners, durations and risks, run Plan the Build, which points to these gates. If you want the content itself checked for accuracy and alignment, that is Check the AI Draft. One expert reviewing one short piece once needs a sign-off line, not a plan.

## Inputs
- The programme, its deliverables and the launch date
- Every reviewer by role (the expert, legal, brand, the sponsor, a learner representative) and what each one cares about
- The comments so far, as they are, if a project is already stuck
If you have none of this, I start from the launch date and the reviewer roles you name, and mark the output as a first draft.

## Approach
Review gates from iterative course development: a first proof of the design, a full draft, a corrected version tried in the real delivery setting, and a final version where only defects are fixed. Each gate asks a narrower question than the last. Endless review is rarely about quality; it comes from everyone being invited to comment on everything, with nobody allowed to say "that was settled two gates ago". The failure this prevents: the wording the expert approved is rewritten by a second reviewer, restored by the expert, and the designer spends launch week carrying messages between them.

## Workflow
1. Ask up to three questions: who sponsors the programme, which reviewer roles must sign, and the launch date.
2. Set the four gates and the one question each asks. Design proof: are the look, the structure and one sample interaction right? Full draft: is all the content correct and complete? Corrected version: does it work in the real delivery setting? Final: are there defects? Structure is closed after the first gate, and the plan says so.
3. Give each reviewer role a lane per gate: accuracy to the expert, legal points to legal, brand to brand, learner fit to a learner representative. A reviewer comments only in their lane; a comment outside it is logged and passed to the lane's owner.
4. Name one decider by role, who resolves conflicting comments within a turnaround you set. Reviewers advise, the decider decides. Two deciders is the same problem again.
5. Set rounds per gate and dates, both yours, counted back from launch. A missed window counts as approval only if the sponsor agreed that rule up front; otherwise the plan states what a late review moves.
6. Set up the feedback log: comment, reviewer role, gate, decision (accept, reject, park), reason. A rejection without a reason comes back as a new comment at the next gate.
7. Write the change rule for any request after a signed gate: new content costs more time, more budget, or something cut. The sponsor picks one, in writing.

## Output Format
```markdown
# Review Plan
## Gates
| Gate | The question it asks | What reviewers see | Closed after sign-off | Rounds | Window |
|---|---|---|---|---|---|
| Design proof | Is the approach right? | [Look, structure, one sample interaction] | [Structure, objectives] | [n] | [dates] |
| Full draft | Is the content correct and complete? | [All content] | [Content scope] | [n] | [dates] |
| Corrected version | Does it work where it will run? | [Corrected build, real setting] | [Wording, flow] | [n] | [dates] |
| Final | Are there defects? | [Final version] | [Everything] | [n] | [dates] |
## Lanes
| Reviewer role | Comments on | Does not comment on | Gates | Signs |
|---|---|---|---|---|
| [The expert] | [Accuracy] | [Brand, layout] | [Gates] | [Name] |
## Decider and rules
[Role, name] resolves conflicting comments within [turnaround]. A missed window means [rule the sponsor agreed].
## Feedback log
| No. | Comment | Reviewer role | Gate | In lane? | Decision (accept / reject / park) | Reason |
|---|---|---|---|---|---|---|
| [1] | [Comment] | [Role] | [Gate] | [Yes / passed to ...] | [Decision] | [Reason] |

After a signed gate, a new request costs [more time / more budget / a named cut]. The sponsor chooses in writing.
## Decision
[Sponsor name] approves the gates, the decider and the change rule by [date], before the build starts; [expert name] signs each gate.
```

## Done When
- Every reviewer role has a lane and its gates, and no role reviews everything
- One decider is named, with a turnaround for conflicts
- The missed-window rule and the change rule are written and seen by the sponsor

## Quality Bar
- Parked comments have an owner and a date, or they return as late requests
- The log records comments and decisions, never a scorecard of reviewers
- Legal points go to legal and are not settled in the log: check with a qualified adviser
- Claude drafts the plan and keeps the log; a named expert signs each gate and one named decider breaks ties

## Next
Run ldg-write-the-objectives (Write the Objectives), since the first thing reviewers sign is what the course must achieve.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
