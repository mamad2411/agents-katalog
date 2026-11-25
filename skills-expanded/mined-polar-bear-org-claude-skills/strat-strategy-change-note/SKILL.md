---
name: strat-strategy-change-note
description: Draft the note that tells the teams a strategy change was decided, with what changed and what did not, the bet that broke and its evidence, what stops and starts per team, and the effect on the roadmap and on dated commitments. Use for "run strat-strategy-change-note", "strategy change note", "announce the strategy change", "tell the teams what changed", "we are changing direction", "explain the change of direction", "what did not change", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Strategy Change Note

## When To Use
The strategy shifts and the teams learn it from a reshuffled roadmap. Use this once the owner has decided a change, before any board or backlog moves. It answers: what changed, what still stands, why now, and what does each team stop, start and keep doing?

## When Not To Use
No change decided by the owner means no note: run Quarterly Strategy Review to get to a decision first. To keep the reasoning on file, run Strategy Decision Record. To restate the standing strategy for the teams, run One-Page Strategy once the strategy document is signed again.

## Inputs
- The decision: what changes, who decided (role) and from when, ideally the new decision record
- The quarterly review or other evidence showing which bet broke, against which kill criterion
- The current roadmap and the list of dated commitments made to customers or partners
If you have none of this, I start from the owner's one-sentence statement of the change and mark the output as a first draft, with every evidence slot left open.

## Approach
Two conventions carry the note. From decision records (Michael Nygard, "Documenting architecture decisions", 2011, cognitect.com/blog/2011/11/15/documenting-architecture-decisions): a changed decision never overwrites the old one, it supersedes it with a link. From US Army Regulation 25-50 (armypubs.army.mil/epubs/DR_pubs/DR_a/ARN42124-AR_25-50-007-WEB-13.pdf): the main point goes first. The judgment is that "what did not change" matters as much as the news, because a team told only what moved assumes everything is in play and stops trusting the rest. In Claude Docs the draft is one shared document. It works the same in a plain chat.

## Workflow
1. I ask up to three questions: what changed, in the owner's words; who decided it and from what date it applies; and which teams and dated commitments it touches.
2. I write the first line: what changed, decided by whom (role), effective when. If it takes more than one sentence, the change is not yet clear enough to send, and I say so.
3. I write "what did not change" second, and it is mandatory: the parts of the strategy, the bets and the "we will not" lines that still stand.
4. I state the trigger: which bet broke, against which kill criterion written in advance, with the evidence and its source, pointing to the quarterly review. If no bet broke and the change comes from somewhere else (a new constraint, a decision above the team), I write that in plain words and do not dress it up as evidence. The note explains a bet, never who is to blame.
5. Per team, by role, I list what stops, what starts and what continues. A team with nothing changing is still listed, with "continues as planned".
6. I list the roadmap effects: items moved, added or removed. Then each dated commitment affected, one by one, with the role that made it and the role that tells the customer. For anything bound by a contract, check with a qualified adviser.
7. I name the decision record this supersedes and where questions go. A human reviews and sends the note. Claude sends nothing.

## Output Format
```markdown
# Strategy Change Note
**[What changed, in one sentence.]** Decided by [role] on [date], effective [date].
## What did not change
- [Part of the strategy, bet or "we will not" line that still stands]
## Why now
| Bet that broke | Kill criterion (written on [date]) | Evidence | Source |
|---|---|---|---|
| [bet, or "no bet broke" with the real trigger in plain words] | [criterion, or none] | [what happened] | [quarterly review, section] |
## What this means per team
| Team (by role) | Stops | Starts | Continues |
|---|---|---|---|
| [team] | [work] | [work] | [work] |
## Roadmap and commitments
| Item or dated commitment | Change | Made by (role) | Who tells the customer |
|---|---|---|---|
| [item] | [moved / added / removed / date at risk] | [role] | [role or not applicable] |
## Record and questions
Supersedes [old record, link], now marked superseded; new record [link]. Questions go to [role] in [channel].
## Decision
[Owner, by role] approves the wording and sends the note by [date]. [Role] confirms each affected customer commitment by [date].
```

## Done When
- The first line can be read alone and says what changed, who decided and from when
- "What did not change" comes second with at least one line, and the trigger names one bet, its pre-written criterion and a source a reader can open, or says plainly that no bet broke
- Every affected team has a stops, starts and continues row, and each dated commitment has a role that tells the customer
- The superseded record is linked, not edited

## Quality Bar
- The first line states the change as a change, with no softening words.
- Evidence slots with no source stay open and visible, never filled with a plausible figure.
- Teams appear by role, and the note never ranks them or names who got it wrong.
- Roadmap items are listed as affected, not re-ordered here. Placing the work is a separate step.
- The note reports a change a named person decided, with the evidence that triggered it. Claude never announces a change nobody made.

## Next
Run strat-product-roadmap (Product Roadmap (Now, Next, Later)) to re-place the work under the changed strategy.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
