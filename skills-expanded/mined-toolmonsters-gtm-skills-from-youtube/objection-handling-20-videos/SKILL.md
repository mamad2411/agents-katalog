---
name: objection-handling-20-videos
description: Helps you answer sales objections (price, timing, "send me info", competitors, stalls) using rules weighted by how many of the 20 most-watched videos on the topic repeat each one, and flags where the experts disagree so you can A/B test instead of guessing. Use when the user says "handle this objection", "they said it's too expensive", "they want to think about it", "they asked me to send info", "they're going with a cheaper competitor", "the prospect is stalling", or "how do I respond to this pushback".
author: Yonathan Cohen (Tool Monsters)
version: 1.0.0
updated: 2026-09-14
license: MIT
---

# /objection-handling

Built from the transcripts of the 20 most-watched videos on handling sales objections in the last 12 months (550,785 views, 93,159 words), which produced 461 pieces of advice, of which 388 were kept because their verbatim quote was found, grouped into 207 distinct themes. The number next to each rule is how many of the 20 videos say it, and all sources are listed in sources.md.

The most repeated rule reached 6 of 20. Treat weights as odds, not laws.

## Inputs
1. The offer and its exact price, as you would say it on the call.
2. The objection, word for word, and when it came up (before price, after price, at the close, on follow-up).
3. What you actually know about the prospect: who else is involved in the decision, any competitor quote they mentioned, and the goals they stated.
4. Optional: your log of recurring objections, how often each one shows up, and the deal value lost.

Refuse to invent the prospect's words, their reasons, competitor prices, or any close rate the user has not given.

## The rules, by weight
### Strong (5 to 6 of 20)
- **Raise and prevent likely objections before prospects voice them.** (6/20) List your top 5 questions in the order they usually come up (price, timeline, start date) and say "you might be thinking this" before you answer it yourself.
- **Keep responses brief and avoid over-explaining.** (6/20) Skip the 20 to 25 minute numbers-heavy walkthrough. Ask what happened, or what would prove you're different.
- **Own objections as your failure, not the prospect's.** (6/20)
- **Establish value and fit before discussing price.** (6/20) Ask "Does this look like the system you want?" before money comes up.
- **Ask permission before pitching, probing, or inspecting.** (5/20) "Do you mind if I ask you a question about that?"
- **Never argue; stay respectful with prospects.** (5/20)

### Solid (4 of 20)
- **Deliver objection responses with confident, unhedged language.** (4/20)
- **Have prospects state why it would work.** (4/20) "Sell me on why you feel this is going to help you."
- **Delay or deflect early price requests.** (4/20) Ask a scoping question first, for example which option they want, before you quote.
- **Treat first objections as smokescreens and probe deeper.** (4/20) "I need to speak with my partner" can really mean "$10,000 is a lot, what if I don't succeed."
- **Acknowledge and validate objections before responding.** (4/20) Acknowledge it, get consent to ask a question, then explore with a closed question.

### Mentioned (3 of 20)
State price flatly without explaining, itemizing, or justifying it · Track recurring objections, their frequency, and cost · Sort objections into a few core categories · Avoid clichéd or salesy phrasing · Isolate the objection with a neutral "X aside" question · Ask what funds they can access, reflecting their reasons · Ask consequence questions about the cost of inaction · Never discount or match competitor prices · Persist and keep qualifying through stalls · Ask early who else is involved in the decision · Stay calm and composed when objections arise · Sell business outcomes in their language, not features · Reframe cheaper bids as less scope and more risk

## Where the experts disagree: do not pick, test
| Choice | Side A | Side B |
|---|---|---|
| How to present price | State price flatly without explaining, itemizing, or justifying it (3/20) | Justify price through team quality, training, and backing (2/20) |
| When a decision-maker is missing | Schedule a joint follow-up call with the partner (2/20) | Get the absent decision-maker on the call now (2/20) |

## Steps
1. Write down the user's objection exactly as the prospect said it, and note where in the call it came up. If it came before value and fit were confirmed, say so first: the Strong rule is to establish value and fit before price (6/20).
2. Check whether this objection could have been raised earlier. If it recurs, add it to a numbered "you might be thinking this" list for the start of future calls (6/20), and log how often it happens and what it costs (3/20).
3. Draft a short opening line that acknowledges and validates the objection (4/20), then asks permission to dig in (5/20). Keep it brief, with no over-explaining (6/20), and no arguing (5/20).
4. Write one probing question that treats the objection as a possible smokescreen (4/20). Add a neutral "X aside" isolating question only if it fits (3/20), such as "Money aside, do you feel like this could be the answer for you?"
5. Add a question that has the prospect say, in their own words, why it would work (4/20). Use only goals the user has actually given.
6. If the objection is about price or a competitor, do not offer a discount or a price match (3/20). Pick one side of the price disagreement from the table for this call and write the response in confident, unhedged language (4/20).
7. If another decision-maker is involved, pick one side of the decision-maker disagreement from the table, and write the question for asking earlier who else is involved on future calls (3/20).
8. Output the final script, then list every rule applied with its weight (for example "Acknowledge and validate objections before responding, 4/20") and name which disagreement choice is being A/B tested and which side this version uses.

## Never
- Never claim a script will raise close rates or save deals unless the user has measured it.
- Never invent facts about the prospect or customer, including their real objection, budget, partner, or competitor quote.
- Never recommend discounting or matching a competitor's price to overcome an objection.
