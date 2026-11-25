---
name: top-down-memo
description: Answer-first writing using the Minto Pyramid Principle. Lead with the conclusion, then 2–4 MECE supporting arguments, then evidence under each. Use whenever you have a recommendation, finding, or assessment to communicate in writing — memos, emails to execs, Slack updates that need to land, briefing docs. Different from the Decision Memo Builder (which is a specific 1-page decision artifact); this is the general writing method.
---

# Top-Down Memo

The McKinsey writing rule: **lead with the answer.** Chronological narratives ("first we did X, then Y, then Z, and concluded W") are how thinking happens, not how communication should land. Top-down inverts the order — conclusion first, then the structure that supports it, then the evidence.

This is also called **BLUF (Bottom Line Up Front)** in military writing and **Minto Pyramid** in consulting. Same idea. Different name.

The test: can the reader stop after the first paragraph and still know what you think and what you want? If yes, top-down. If they need to read to the end to find the answer, you wrote a story.

---

## Why people don't do this naturally

The way you *thought* about something is the opposite of how the reader needs to *hear* it.

| You (writer) | Reader |
|--------------|--------|
| Gathered data → found patterns → drew conclusion | Wants the conclusion → then patterns → then data only if they push back |

Chronological narrative is easier to write because it matches your discovery path. It's harder to read because the reader doesn't know where you're going. Reversing the order is unnatural but obviously correct.

---

## Design choices

- **Lead is the answer, not the setup.** The first sentence states what you think. The reader can stop here.
- **2–4 supporting arguments.** Rule of 3 is best. >4 means you haven't synthesized; <2 means it's a one-liner, not a memo.
- **MECE at the argument level.** The supports should not overlap and should jointly defend the lead.
- **Evidence under each argument, not in a separate section.** Reader skims to the argument they doubt, then drops down for proof.
- **Background last (if at all).** Most "background" sections exist because the writer felt anxious about jumping to the answer. Cut.
- **One memo, one answer.** If you have two recommendations, write two memos.

---

## The pyramid structure

```
                    [LEAD]
                  The answer.
                One sentence.
                      │
       ┌──────────────┼──────────────┐
       │              │              │
   [ARG 1]        [ARG 2]        [ARG 3]
   Because…       Because…       Because…
       │              │              │
   • evidence      • evidence      • evidence
   • evidence      • evidence      • evidence
   • evidence      • evidence      • evidence
```

The three arguments must **jointly support** the lead — if all three are true, the lead must be true. Cut anything that doesn't ladder up.

---

## Output format

```
[LEAD — one sentence with the answer]

[OPTIONAL: 1 sentence on the ask or so-what if the lead is a finding]

ARGUMENT 1: [Headline claim that supports the lead]
• [Evidence: specific data, source]
• [Evidence: specific data, source]
• [Evidence: specific data, source]

ARGUMENT 2: [Headline claim]
• [Evidence]
• [Evidence]
• [Evidence]

ARGUMENT 3: [Headline claim]
• [Evidence]
• [Evidence]
• [Evidence]

[OPTIONAL: Risks or open questions — max 3 bullets]

[OPTIONAL: Background / context — only if reader genuinely lacks it]
```

---

## Inputs needed (interview if missing)

1. **The answer.** What do you actually think? If unclear, the memo isn't ready — use Synthesis or Decision Memo first.
2. **Reader.** Exec / peer / team. Changes vocabulary and depth.
3. **The decision the reader needs to make** (if any).
4. **The 2–4 reasons you believe the answer.** If you can't list them, you haven't synthesized.
5. **Evidence for each reason.** Specific, sourced.

---

## Process

1. **Write the lead in one sentence.** If it takes two, you have two leads — split.
2. **List the 2–4 arguments.** Test: if all true, is the lead provably true?
3. **MECE-check the arguments.** Overlapping → merge. Missing a defense → add. Independent of lead → cut.
4. **Stack evidence under each.** 2–4 bullets, specific and sourced. No "many people" or "it's clear that."
5. **Read top-to-bottom and test the stop-anywhere principle:** can the reader stop at the lead alone, the lead + arguments, or the full memo, and walk away with the right takeaway at each level?
6. **Cut everything that doesn't ladder up.** Especially: backstory, process notes, "by way of context."

---

## Worked example 1: Memo to CEO on potential acquisition

**LEAD:** We should not acquire Vega Labs. Their tech is real but the cultural fit and price preclude a deal that creates value.

**(If we want to revisit in 6 months at a 40% lower valuation and after their senior team has stabilized, the math could work — happy to set that revisit on the calendar.)**

**ARGUMENT 1: The price ($380M) is 2.4x what the asset is worth on a standalone basis.**
- Vega's TTM ARR is $22M growing 45% — implied 17x ARR multiple at ask vs. 7x median for our peer group (Q1 2026 SaaS comps, KeyBanc).
- DCF at our cost of capital (12%) and the founders' own projections (which we discount 30%) supports $160M.
- No realistic synergy story closes the $220M gap. Closest is cross-sell to our 4,200 customers; sensitivity says max $35M NPV.

**ARGUMENT 2: 60% of their senior eng team is at <12-month vest cliff and is the actual asset.**
- 7 of 12 senior engineers vest between Q3 FY26 and Q1 FY27.
- Two of the three named co-founders have publicly stated (podcasts, Q4 2025) that they want to "do another zero-to-one."
- Acquirer history: 4 of the last 5 startups acquired by similar companies in our space lost >50% of senior eng within 18 months.

**ARGUMENT 3: The integration risk is concentrated in the part of our stack we cannot afford to break.**
- Vega's product would have to integrate into our billing platform, which carries 92% of revenue and had two P0 incidents in Q4.
- Their stack is Rust + custom DB; ours is Go + Postgres. Re-platforming estimate: 9–12 engineer-years.
- The CTO's own pre-LOI risk memo flagged this as "non-trivial and likely to slip ≥6 months." Nothing has changed since.

**RISKS OF NOT ACQUIRING**
- A competitor (likely Brava) buys them within 6 months and we lose distribution leverage. Mitigation: deepen our own roadmap on this surface area; we've already greenlit Q2 investment.
- Brand signal that we're "passing on AI." Mitigation: we're acquiring [other target] this quarter — net story is selectivity, not absence.

(No background section needed — you've been in every Vega meeting since Jan.)

---

## Worked example 2: Slack message to a peer that needs to land

```
TL;DR: I think we should kill the Pro tier and merge everything into Team.

Three reasons:
1. Pro is <8% of revenue and 40% of pricing-page complexity (data in #pricing-experiments thread)
2. Every Pro customer we've talked to (n=14 in Q1) would happily move to Team at the same price
3. We're about to add 4 new add-ons that won't fit on a 3-tier page — collapsing now buys us room

Risk: ~30 legacy Pro accounts on a grandfathered price. Easy to migrate — I have the script.

Want to align before Friday's pricing review?
```

That's a top-down Slack message. Lead → reasons → risk → ask. ~120 words. The reader can stop after line 1 and still know what to do.

---

## Common mistakes to avoid

- **Burying the lead.** "Over the last 6 weeks, the team explored three options, and after careful consideration..." Cut. Lead with the answer.
- **"As you know" / "to provide context" preambles.** If the reader knows, don't tell them. If they don't, the evidence will surface it.
- **Topic-shaped arguments.** "Pricing" is a topic. "Pricing is 2.4x the standalone value" is an argument. Argument = claim, not subject.
- **Evidence that doesn't defend the argument above it.** Common when copy-pasted from earlier drafts. Each bullet should clearly serve the headline.
- **More than 4 arguments.** You haven't synthesized. Go back to Synthesis skill.
- **Recommendation hiding in "considerations."** Decision-averse hedging. Recommend, or don't write the memo.

---

## When to use

- Any written communication where you have a recommendation or finding
- Emails to executives
- Slack messages that need a yes/no response
- Briefing docs and pre-reads
- Status updates that should drive a decision
- Internal blog posts / wiki pages with a take

## When NOT to use

- Genuinely exploratory thinking ("here's what I'm noodling on") — narrative form is fine
- Personal narratives, retrospectives, postmortems where chronology matters
- Decision artifacts that need a formal structure — use **Decision Memo Builder** instead
- Status updates with no recommendation — just use a clean list

---

## Pairs well with

- **Synthesis** — synthesis output (3 insights with so-whats) maps directly to top-down (lead = overall recommendation, insights = arguments)
- **Decision Memo Builder** — top-down is the general method; Decision Memo is the constrained 1-page form for yes/no calls
- **McKinsey Critic** — run the draft through the critic to catch buried leads and topic-shaped arguments
- **Storyline Builder** — pyramid principle works for slide titles too; each slide title is a "lead" that the slide proves
