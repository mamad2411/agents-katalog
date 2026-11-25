---
name: pdes-user-journey-map
description: Builds a User Journey Map for one group and one scenario, with stages, actions, thoughts in participants' own words, feelings, touchpoints with owners and pain points, every cell tagged to its evidence and gaps marked "not researched". Use for "run pdes-user-journey-map", "user journey map", "map the user journey", "experience map from my interview notes", "what happens before and after this screen", "where does the journey break", "journey map with evidence", "current state journey", part of the Claude for Product Designers Pack by 90n.
---

# User Journey Map

## When To Use
You design one screen of a journey nobody has drawn, and the team's picture of it is a guess. Run it when you have real notes from real people, however thin, and need to see what happens before and after your screen. It answers: what does this person go through from first trigger to the end, where does it go wrong, and which parts has nobody looked at?

## When Not To Use
If you need the steps and system responses of one task inside one product, run User Flow: the journey covers a person's experience across time and channels, with thoughts and feelings. If nobody has spoken to or observed a real user, talk to a few first; a map of what the team believes looks exactly as convincing as a researched one.

## Inputs
- Notes from real sessions, interviews, support contacts or observation, with quotes where you have them. Before pasting, replace names with P1, P2 and remove contact details and employers
- The group and scenario the map follows, for example [returning users changing a booking], and where the journey starts and ends
- The touchpoints you know of, with the team or role that owns each
If you have none of this, I start from one session's notes, mark most cells "not researched" and mark the output as a first draft.

## Approach
The experience map method in the GOV.UK Service Manual: lay out each participant's events, line up the common ones, group them into stages and name each stage, then add detail. Journey Mapping 101 from Nielsen Norman Group (Gibbons, 2018) supplies the parts: one actor, a scenario with expectations, phases, actions, mindsets and emotions, opportunities. The judgment is to show the gaps loudly instead of smoothing them over. The failure it prevents: a handsome map where half the cells are guesses and nobody, including you three weeks later, can tell which half.

## Workflow
1. Ask three questions: which one group and scenario does this map follow, where does the journey start and end, and which notes count as evidence (paste them)?
2. Lay out each participant's events in the order they happened, from the pasted notes only. One point of view per map: if the notes cover two user types, I say so and you get two maps.
3. Line up the events participants share, group them into stages, and name each stage the way people live it ("finding out the booking is wrong"), never the way the funnel names it.
4. Fill the rows per stage: actions, thoughts quoted word for word with a participant id, feelings only where someone showed or said them, touchpoints with the owning team or role, pain points.
5. Tag every cell: participant ids, "[n] of [N] participants", source. No evidence means the cell reads "not researched". One participant is a single-voice observation and is marked as one.
6. Where participants split, draw two lanes for that stage with the count on each. Then write the opportunities row as needs ("know the change went through"), never as features.
7. List the gaps with the question that would fill each, and mark the stage you are designing. Live with the draft, then revise it as new sessions come in. For a visual, Claude Design can draw the finished table; it works from what you paste.

## Output Format
```markdown
# User Journey Map
**Group:** [who] | **Scenario:** [goal and expectations] | **Starts:** [trigger] | **Ends:** [end point]
**Evidence base:** [sources, N participants, dates] | **Status:** [first draft / revised on date]
## Map
| Row | [Stage 1] | [Stage 2, the stage you are designing] | [Stage 3] |
|---|---|---|---|
| Actions | [action] ([P ids], [n] of [N]) | [action] ([P ids], [n] of [N]) | not researched |
| Thoughts | "[quote, word for word]" ([P id]) | "[quote]" ([P id]) | not researched |
| Feelings | [shown or said] ([P ids]) | [shown or said] ([P ids]) | not researched |
| Touchpoints and owner | [touchpoint], [team or role] | [touchpoint], [team or role] | [touchpoint], [owner not known] |
| Pain points | [pain] ([n] of [N]) | [pain] (single voice, [P id]) | not researched |
| Opportunities | [need] | [need] | [need, or none yet] |
## Forks
- [Stage]: lane A, [path], [n] of [N]; lane B, [path], [n] of [N]
## Gaps to research
- [Stage and row marked not researched]: [the question that would fill it]
## Decision
[Product manager] and [designer] decide which pain point the design work addresses first and which gap gets researched before design continues, by [date].
```

## Done When
- Every filled cell carries participant ids or a count, and a source
- Every empty cell says "not researched" and appears in the gaps list with a question
- The map follows one group and one scenario, splits show as lanes with counts, and opportunities read as needs

## Quality Bar
- Thoughts are word-for-word quotes with a participant id, never a paraphrase inside quotation marks
- Feelings come from what people showed or said, never from the name of a stage
- Counts read "[n] of [N] participants", never "users say" or "most people"; participants stay P1, P2
- Owners appear by team or role and are never blamed for a pain point
- Every cell traces to research with real people; gaps read "not researched" and are never filled with assumptions.

## Next
Run pdes-heart-metrics-plan (HEART Metrics Plan) to agree what success looks like for the stage you are designing.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
