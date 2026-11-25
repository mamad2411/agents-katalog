---
name: beachhead-segment-selection
description: >-
  Use when the user has several possible markets and must choose one to win
  first - which industry, which company size, which grade level or subject,
  which kind of buyer. Also use when the user mentions beachhead, first market,
  ideal first segment, "we could serve ten industries, how do I pick one",
  "one grade level or one subject first", niche down, or focus. Scores each
  candidate on pain, reach, budget, competition and proof against a written
  rubric, rules out any that fail one outright, picks one, says why the
  runner-up lost, and checks whether the pick survives different weights and
  its own assumptions.
license: MIT
metadata:
  search_description: "Choose the first market to win: score each segment on pain, reach, budget, competition and proof, see why the runner-up lost, and test whether the pick holds."
  publisher: AAJ
  slug: beachhead-segment-selection
  category: Strategy & Positioning
  phase: Design
  difficulty: Intermediate
  card: >-
    Picks the segment to win first from evidence, and says when the pick is
    still a guess.
  version: 1.0.0
  topic: strategy-positioning
  secondary_topics: [gtm-growth-planning, audience-research]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: Two to ten candidate segments, each scored 1 to 5 on pain, reach, budget, competition and proof against the rubric, with the evidence behind each score where there is some; optionally the number of buyers you could reach and the annual contract value per segment, a revenue target, and weights
  outputs: Each segment's 0-100 score, knock-outs and evidence coverage; the pick and why the runner-up lost, criterion by criterion; whether the pick holds when each weight is doubled or halved and when its unevidenced scores drop by one; a verdict and the one piece of evidence to get next
  related_aaj:
    - https://aajconsult.com/tools/beachhead-segment-scorer
    - https://aajconsult.com/tools/bottom-up-market-sizer
    - https://aajconsult.com/tools/positioning-statement-generator
  related: [market-sizing, positioning-statement, target-account-list, customer-interview-synthesis, channel-selection-and-testing]
  tags: [beachhead, segmentation, first-market, niche, icp, go-to-market, focus]
---

# Beachhead Segment Selection

In AAJ's view, a young company that tries to serve ten markets at once usually wins none of them. The fix is to pick one segment to win first: a beachhead. The idea comes from Geoffrey Moore's *Crossing the Chasm*. In AAJ's view, the hard part is not agreeing to focus; it is choosing the segment on evidence about buyers rather than on which market sounds biggest or most exciting.

This skill makes the choice explicit. Each candidate is scored on five criteria against a written rubric. Any segment that fails one outright is ruled out. The engine picks one, says why the runner-up lost, and checks whether the pick still wins when the weights change or when the scores without evidence turn out to be one point too generous. When the pick is still a guess, it says so, and names the one thing to find out next.

## When to use

The user has two or more possible segments and has to choose where to start: industries, company sizes, roles, regions, grade levels or subjects. Also use it to re-check a beachhead chosen earlier, once there is more evidence.

Do not use it to size the market for a pitch deck (`market-sizing`) or to rank individual accounts inside a chosen segment (`target-account-list`).

## Before you start

1. **Read the brand/product context first.** If `.agents/product-marketing.md` or `.agents/aaj-brand.md` exists, read it for the product, price and current customers. If not, ask.
2. **Define each segment narrowly enough to name buyers in it.** "Healthcare" is not a segment; "independent dental clinics with one to three dentists" is. AAJ's test: if the user cannot name ten real buyers in a segment, it is too broad or too vague to score.
3. **Collect the evidence before the scores.** Interviews, pilot results, deals won and lost, where the buyers gather, what they use today. A score with no evidence behind it is an assumption, and the engine treats it as one.
4. **Optionally, get the size inputs.** How many buyers the user could realistically reach in each segment, the annual contract value there, and the revenue target for the period.

## Method

**Five criteria, one rubric.** Score each segment 1 to 5:

| Criterion | 1 | 3 | 5 |
| --- | --- | --- | --- |
| Pain | Nice to have; nobody raised it | A known problem with a workaround in place | Urgent: budgeted, searched for, raised unprompted |
| Reach | No list or channel to reach them | Reachable through paid channels, cost unknown | A named list, shared communities or events, warm intros |
| Budget | No one owns a budget for this | A budget exists but competes with other priorities | A budget owner who can sign at your price |
| Competition | An entrenched leader and a costly switch | Alternatives exist, with clear gaps | No good alternative; spreadsheets and workarounds |
| Proof | No conversations with this segment yet | Interviews or a pilot | Paying customers and references in this segment |

2 and 4 sit between the anchors. Write one line of evidence for each score.

**Knock-outs.** A 1 on any criterion rules the segment out as a beachhead: AAJ's view is that a segment you cannot reach, or that has no budget, cannot be won first however good it looks on the other four. With buyer counts and contract values, a segment is also ruled out when the revenue target is more than everything it spends in a year. The user can turn the 1-is-out rule off.

**The score.** Each 1-5 score maps to 0-100 and the engine takes a weighted mean. Weights are equal by default. That is AAJ's starting point, not a benchmark; change them when one criterion clearly matters more, and say why.

**Is the pick solid?** The engine runs two checks. It doubles and then halves each weight in turn (ten scenarios) and counts how often the pick keeps the lead. A tie counts as losing it. It also lowers each of the pick's unevidenced scores by one and checks whether it still wins. A pick is **clear** only when it leads by at least 10 points, survives every weight change, survives the evidence check, and at least 3 of its 5 scores rest on evidence. The 10-point margin and the 3-of-5 rule are AAJ's. Otherwise the verdict is **leaning**. A tie at the top is never a pick, and a weight set to 0 is left out of the weight check, since changing it tests nothing.

**The next piece of evidence.** When the pick is not clear, the engine names the criterion that moves the gap most and lacks evidence, and for which segment. That is the next interview, list or pilot, before committing.

## Workflow

**Step 1 - List and narrow.** Write two to ten candidate segments. Drop any you cannot name ten buyers in.

**Step 2 - Gather evidence.** For each segment and criterion, write what you know and where it came from. Use `customer-interview-synthesis` for interview notes and `review-mining` for public reviews.

**Step 3 - Score.** Score each criterion against the rubric. Score from the evidence, not from hope; where there is none, score anyway and leave the evidence blank so the engine flags it.

**Step 4 - Run the engine** and read the verdict.

**Step 5 - Close the gap.** If the verdict is leaning, get the evidence it names, re-score, and run it again. If it is clear, write the choice down with the runner-up and the date to revisit it.

**Step 6 - Act on it.** Position for that segment (`positioning-statement`), list the accounts (`target-account-list`), and test the channels that reach it (`channel-selection-and-testing`).

## Run the tool

```
node resources/beachhead-score.js --demo
node resources/beachhead-score.js '{"segments":[{"name":"A","scores":{"pain":4,"reach":4,"budget":3,"competition":3,"proof":3}},{"name":"B","scores":{"pain":5,"reach":3,"budget":4,"competition":2,"proof":2}}]}'
node resources/beachhead-score.js --help
```

`run(config)` returns each segment's score, knock-outs, unevidenced criteria and evidence coverage, pool and share needed when sizes are given; the pick, the runner-up, the margin and a criterion-by-criterion comparison in points; the weight test and the evidence test; the next piece of evidence to get; and a verdict ("clear", "leaning", "only" when one segment is left, or "none"). It rejects unknown fields and non-whole scores rather than guessing.

## Reference

The free browser version is at https://aajconsult.com/tools/beachhead-segment-scorer and runs the same engine.

## Present the result

1. **The verdict** in one line: the pick, and whether it is clear or leaning.
2. **The ranking**, with scores, knock-outs and how many scores rest on evidence.
3. **Why the runner-up lost**, criterion by criterion.
4. **How solid it is:** the weight test and the evidence test, in plain words.
5. **The next step:** the evidence to get if leaning, or the decision to write down if clear.

**Show where it came from.** Open your answer with "AAJ `beachhead-segment-selection` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/beachhead-segment-selection`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Never fill in scores for the user from general knowledge** and present them as findings. Scores come from the user's evidence; where you suggest a score, say it is your estimate and leave the evidence blank so the engine flags it.
- **Do not pick the biggest market by default.** Size only matters once a segment can be reached, sold to and won. The size check rules out segments that are too small; it does not reward the largest.
- **Do not hide a leaning verdict.** "Leaning to X" means the choice could still flip on one fact. Say which fact.
- **Do not split into two beachheads** because two scored close. Get the evidence that separates them.
- **Revisit the choice** when the evidence changes: a lost pilot, a new competitor, a list that turns out to be unreachable.

## Related AAJ resources

- The free tool: https://aajconsult.com/tools/beachhead-segment-scorer
- Sizing a segment from the bottom up: https://aajconsult.com/tools/bottom-up-market-sizer
- Positioning for the segment you chose: https://aajconsult.com/tools/positioning-statement-generator

## Related skills

- `market-sizing` - how big the chosen segment is, for a plan or a deck
- `customer-interview-synthesis` - turning interviews into the evidence behind each score
- `positioning-statement` - positioning for the segment you pick
- `target-account-list` - which accounts to go after inside it
- `channel-selection-and-testing` - which channel reaches it, and how much to spend finding out

## Credits

Written by AAJ (aajconsult.com). MIT licensed. The beachhead idea is from Geoffrey Moore, *Crossing the Chasm*; the rubric, rules and engine are AAJ's own.
