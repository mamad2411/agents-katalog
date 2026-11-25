---
name: deepsearch-gap-and-segments
description: Decides what a market gap means, unmet demand or demand that cannot pay, ranks the explanations by evidence, segments the market with kill criteria, and designs the cheapest field test that settles the question, such as a refundable deposit test. Use for "pourquoi personne ne fait ça", "why so few competitors", "why is this gap empty", "océan bleu", "segmentation", "quel segment tester", "go or no-go", "kill criteria", or "how do I test demand". Part of In-depth Deep Search.
---

# Gap and segments

An empty space on the map has two opposite meanings: nobody has served this demand yet, or the demand cannot pay. This stage says which is more likely, how sure it is, and what test would settle it.

Read `../_shared/evidence-protocol.md`, then all earlier studies. Newer files win, and say so where it matters.

## Part 1: Why is the gap there? (`07-gap.md`)

**1. Correct the premise with numbers.** "Nobody does this" is rarely accurate. State how many actors exist, how many are dedicated, how many execute for the client with a stated result, and who actually spends.

**2. Rank the explanations by strength of evidence.** Each gets its evidence, a link and a confidence level. Test at least these:

| Explanation | What would show it |
|---|---|
| The law or platform rules forbid it | Primary legal sources. Say plainly when this is not the reason |
| The solvent market is small | Payer funnel |
| The client's return arrives after the contract ends | Cash curve against contract length |
| No habit of buying at this price | What they pay today, and its ceiling |
| Poor targeting on the channel | Reach against population, share of off-target audience |
| Lead quality, unrealistic budgets | Verbatims, from people who tried |
| Dedicated platforms failed | Filed accounts, insolvencies |
| Easier markets exist for sellers | Sellers' economics, with counts |
| Teaching is cheaper to deliver than results | Share of courses and coaching among dedicated actors |

Add others the files support.

**3. Ask the question that decides everything.** Lay both sides in one table, each cell with its source:

| For unmet demand | For demand that cannot pay this format |
|---|---|
| ... | ... |

Then state:
- **what is established**
- **what is most likely**, by sub-segment if the answer differs. Below one revenue level it may be measured, and above it unknown
- **your probability**, labelled as judgement, with the missing figure that weighs most
- **the cheapest test that would settle it**

Do not force a conclusion the evidence does not support. Absence of voices proves neither demand nor its absence.

## Part 2: Segments (`07-segments.md`)

These are **hypotheses to test, never finished offers.** Split or merge segments if the evidence supports it.

For each segment:
- **Size,** if known
- **Four market criteria,** from Alex Hormozi's *$100M Offers*: massive pain, purchasing power, easy to target, growing. Each scored, with the evidence behind the score
- **Dream outcome and top obstacles in their own words:** 2 to 5 exact verbatims, with speaker type and URL
- **Offer angle** per the value equation, delivery level (do it yourself, done with you, done for you), and price logic
- **Plausible guarantee,** given the pain they really voice, the legal limits from stage 4, and what competitors' contracts really say
- **Kill criterion:** the result that closes this segment

End with:
- a table ranking the segments
- one recommended segment to test first
- what would change that recommendation

Say honestly if no segment clears the bar at the intended price, and whether the honest answer is a cheaper or different offer. Do not soften a negative verdict to please the founder, and do not repeat it for effect.

Check quotes before finishing: `python3 "$IDS/scripts/bank.py" check-report 07-segments.md --bank notes/bank.json --corpus notes`.

If a scope gate says to wait on the offer, stop at the size and criteria, and describe people rather than angles.

## Part 3: The field test

Desk research ends here. Design the test before anyone builds anything. If a scope gate is on and no offer exists yet, run the cheap checks now, and leave the deposit test as a plan with its price left blank.

**Cheap checks first, for almost nothing:**
- Ask the competitor's publicly named clients what they paid, if the user is willing to contact them, and always without posing as a prospect.
- Ask a few of the target for the dates of their last 10 clients, to measure the deal cycle.
- Run five to ten conversations with the people missing from the corpus.

**Then the deposit test, the one that settles demand:**

| Element | Default |
|---|---|
| Sample | 30 named, qualified accounts from a verifiable list, split between the segments in question. For consumers, see `../_shared/adapting.md` |
| Offer | Full price, real terms. Take both from the founder, never from your own guess |
| Commitment | A refundable deposit, signed at a distance. Interest is not evidence, and only money counts |
| Cost | Two weeks, no media budget |
| Threshold | Set before starting. For example 2 or 3 deposits |

**Decode the result, written down in advance:**

| Result | Reading |
|---|---|
| Threshold reached | Unmet demand. Confirm with a pilot |
| Refused on price or budget | Demand that cannot pay this format |
| Refused because the book is full, or because of the economy | No felt need right now |
| Refused for lack of proof | Still open, if the founder has no case yet. This result alone does not close the file |

Record the reason for every refusal. If choosing between niches, run the tests one after the other, under the same rules. Get a lawyer's note before handling any lead.

## Done when

- [ ] The premise was corrected with counts
- [ ] Explanations are ranked with evidence and confidence
- [ ] The decisive question has both sides, a judgement, and a test
- [ ] Every segment has a kill criterion
- [ ] All quotes pass the check
- [ ] The field test has a threshold and a decoding table, set in advance
