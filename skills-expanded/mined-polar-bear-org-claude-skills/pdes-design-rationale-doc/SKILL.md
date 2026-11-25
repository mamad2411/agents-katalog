---
name: pdes-design-rationale-doc
description: Writes a Design Rationale Doc with the decision in one line, the options considered and why each lost, the principles applied, every claim linked to real evidence or marked as a gap, the trade-offs accepted, two or three pre-mortem risks and the signal that would reopen it. Use for "run pdes-design-rationale-doc", "write up why we chose this design", "why is it like this", "I keep explaining the design again", "design rationale", "document this design decision", "it felt right is not an answer", "rationale for the review", part of the Claude for Product Designers Pack by 90n.
---

# Design Rationale Doc

## When To Use
You are asked "why is it like this?" in every meeting, and the honest answer keeps coming out as "it felt right". Run it when the decision is made, while the reasons and the evidence are still fresh. It answers: what did we choose, what did we reject and why, what are we betting on, and what would reopen it?

## When Not To Use
If the options are still open, use Design Options Trade-off Table; a rationale written before the choice is a pitch. If you only need a short dated entry in a running record, use Design Decision Log.

## Inputs
- The decision, and who made it, by role
- The options you considered, the criteria you used and the principles you applied, as a table or from memory
- The research, data and frames behind it, with personal data removed
If you have none of this, I start from the decision and the options you remember and mark the output as a first draft.

## Approach
Design rationale in Questions, Options and Criteria form (MacLean, Young, Bellotti and Moran, 1991, described on the NAVER LABS Europe page on Design Space Analysis), which keeps the reasoning and not only the final screen, plus a pre-mortem (Klein, Harvard Business Review, September 2007): assume the design shipped and failed, then work out believable reasons why. The judgment is timing. Written at the moment of the decision it is a record; written months later it is a defence. The failure it prevents is the doc that cites "user research" for a choice no study ever looked at. Claude Docs is an optional place to write it, so the team can comment in the document; the Figma connector, also optional, reads the frames you point to.

## Workflow
1. Ask three questions: what was decided and by which role, which options were on the table, and what evidence was in front of you when you chose?
2. Write the decision in one line, then the problem and the outcome it serves, taken from the brief. If you cannot write the line, the decision is not made yet; stop and say so.
3. Compress the Question, the Options considered and the Criteria. Give each rejected option one sentence on why it lost, naming the criterion.
4. Name the principles applied and how each tipped the choice. Where taste decided, write "designer's judgement"; that is a legitimate reason when it is labelled.
5. Fill the evidence table: claim, source, status. A claim with no source reads `[evidence gap]` and stays visible.
6. List the trade-offs accepted and who bears each, as a user group or a role. Then run the pre-mortem and keep two or three reasons, each with an owner and an early sign.
7. Write the reopen signal: the observable result that would make the team revisit (a metric moving, a finding, a constraint lifting) and who watches for it. Leave the confirmation to the decider.

## Output Format
```markdown
# Design Rationale Doc
**Decision:** [one line] | **Written by:** [role] | **Decided by:** [role] | **Date:** [date] | **Status:** [draft / confirmed]
**Problem and outcome:** [the problem, for whom, and the outcome it serves]
## Options considered
| Option | Chosen or rejected | Why, in one sentence | Criterion that decided it |
|---|---|---|---|
| [option] | [chosen / rejected] | [reason] | [criterion] |
**Principles applied:** [principle and how it tipped the choice, or "designer's judgement"]
## Evidence
| Claim | Source | Status |
|---|---|---|
| [claim] | [research, data or frame link] | [linked / evidence gap] |
## Trade-offs accepted
- [What this design gives up, and the user group or role that bears it]
## Risks (pre-mortem)
| If it shipped and failed, a believable reason | Owner (role) | Early sign |
|---|---|---|
| [reason] | [role] | [observable sign] |
**What would reopen it:** [the observable signal, and the role who watches for it]
## Decision
[Role who decided] confirms the rationale by [date]; [designer] files it in the decision log the same day.
```

## Done When
- The decision fits in one line and every rejected option has a reason it lost
- Every claim has a source or a visible evidence gap
- Two or three risks each have an owner and an early sign, and the reopen signal is observable with a role watching

## Quality Bar
- Reasons are the ones you had at the time; a reason found afterwards is dated and labelled as later
- Nothing reads as tested with users unless you pasted the sessions it came from
- Trade-offs name a user group or a role, never a colleague's failing
- A claim with no source reads "evidence gap"; "it felt right" is recorded as judgement, never dressed as research.

## Next
Run pdes-design-decision-log (Design Decision Log) to file the decision where it can be found.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
