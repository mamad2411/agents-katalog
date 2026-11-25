---
name: house-inspection
description: Turn a home inspection report (and pest, sewer, chimney, radon or other specialty reports) into a short, credible request to the seller - sorted into tiers with page numbers and cost ranges, split between repairs, credits and documents, plus which specialty tests must happen before the buyer loses the right to walk away. Use when a buyer uploads or pastes an inspection report, asks "what can we ask the seller for", "how much credit is reasonable", "is this a deal breaker", "what else should we test", or wants a request letter drafted for their agent.
---

# House inspection

An inspection report lists everything. A request to the seller should not. Every weak item on the list lowers the credibility of the strong ones, and a seller who has already given ground can walk away from a long list. This skill sorts the report and drafts the one request that decides the deal.

<!-- shared:rules -->
## Ground rules (shared by every HousingWizard skill)

Each one guards against a common, expensive mistake. They apply to every answer.

1. **Tag where each fact came from.** Use `[record]` public record, `[document]` contract, report, disclosure or listing, `[seen]` observed on site by the buyer, `[seller said]` anything relayed from the seller or listing agent, `[estimate]` your arithmetic or market ranges, `[assumption]` a placeholder. Never promote a seller statement or an estimate to a fact.
2. **Zero rows is not clean.** An empty database result means the online dataset has nothing, not that nothing happened. Compare with neighbors before calling anything unusual.
3. **Give the honest counter-case.** For every red flag, first write the innocent explanation and the evidence for it, then why it still deserves a check, and how to check it.
4. **End with a human check.** Close every substantive answer with a short "Human check" list: what must be measured, seen, confirmed or decided by a person, by whom (buyer, inspector, attorney, lender, licensed trade), and what must not happen until it is done.
5. **You are not the buyer's lawyer, agent, inspector or lender.** Turn legal and licensing points into questions for the buyer's attorney, phrased as confirmations, not demands. Cost figures are ranges with a source, never quotes.
6. **Name the jurisdiction.** Say which state and city rules you are applying. If this skill has no reference file for the location, work in generic mode: do not state local rules as facts, ask for the local forms, and route the question to a local professional.
7. **Draft, never act.** Write messages, letters and checklists for the buyer to send or use. Do not send, sign, pay, accept terms, or fill forms on their behalf.
8. **Stop at walls.** At a CAPTCHA, login or paywall, stop and give the buyer the exact steps: URL, what to click, what to type, what to copy back.
9. **Keep the case file true.** Write new facts into the buyer's case file (see house-case-file). When a new fact overturns an old conclusion, change the conclusion and log what changed, instead of appending a note under a stale answer.
10. **Re-check anything time-sensitive.** Rates, taxes, fees, tariffs and code section numbers change. Quote them with the date you checked them, and re-check anything older than two weeks before relying on it.
<!-- /shared:rules -->

## Before sorting

1. Read the whole report, including the summary, the limitations section (what the inspector could not access), and any pest report sections listing obstructed areas.
2. Check the negotiation state in the case file: has the seller already reduced the price or agreed to repairs? If yes, default to asking only for what is necessary and customary.
3. Keep price and condition as separate conversations. Do not let the seller trade "we will fix these" for "the price does not move", or the reverse.

## The four tiers

| Tier | What belongs | How to ask |
|---|---|---|
| 1. Must have | Safety hazards the inspector flagged (burn, fall, fire, shock, gas), work that needs a licensed trade, anything that affects insurance or the loan | Seller repairs before closing with licensed receipts, or a documented credit |
| 2. Can ask | Major systems at end of life (old, not broken): roof, boiler or furnace, water heater, sewer line | Money, not repairs. A seller hired repair tends to be the cheapest minimal fix |
| 3. Bundle | Small safety items | One combined number or one repair line |
| 4. Do not raise | Cosmetic, landscaping, paint, items the inspector said to "monitor" | Leave out, or cover with a contract clause or written explanation |

For each item give: report page, the inspector's own words, tier, cost range with source, and whether it needs a licensed trade or permit where the house is.

Read `references/tiers.md` for worked examples and common traps.

## Tests before the right to walk away ends

Check the contract structure (house-contract) or local practice. Where there is no inspection contingency after signing, these must happen before signing. Where there is an inspection or option period, they must happen inside it.

| Test | When it matters | Rough cost |
|---|---|---|
| Sewer line camera | Houses older than about 1960, big trees, cast iron or clay lines | $300 to $600 |
| Oil tank sweep | Built before about 1970 or ever heated with oil | $300 to $500 |
| Chimney inspection with camera | Old chimneys, especially after a fuel change | $400 to $800 |
| Structural engineer | Sloping floors, pest damage near framing, walls to be removed | $500 to $900 |
| Lead, asbestos, radon, mold | Age and region dependent | Varies |
| Insurance quote | Always | Free |

Two cheap tests (sewer and oil tank) protect against five- and six-figure problems. Suggest not signing until they are back.

## Credit or repair or price

- Safety items: ask for the repair and the paper (licensed receipt, permit sign-off, transferable warranty). The paper is what the buyer needs.
- System items: ask for money. It is worth more in the buyer's hands.
- Credits are capped by loan rules and closing costs (house-money). Beyond the cap, it has to be a price reduction.
- Market context helps: many buyers request concessions after inspection; typical credits are a small percentage of price. Quote any statistic with its source and date.

## The request letter

Draft it for the buyer's agent to send, not directly to the listing agent. Use `assets/request-letter.md`. One page: repairs with page numbers, at most one credit item with a floor, documents the seller can give at no cost, access for tests the buyer pays for, and a closing line that is true ("if this does not work for the seller, we understand and will step aside"). Do not attach the full report; attach the one-page sorted list, the pest report, and licensed contractor quotes where they exist.

## Output

1. One-line verdict: proceed, proceed with this request, or reconsider the price.
2. The tier table.
3. Tests to schedule, with the deadline.
4. The draft letter.
5. Human check.

Record the request and the seller's answer in the case file, item by item, so the contract can include them.
