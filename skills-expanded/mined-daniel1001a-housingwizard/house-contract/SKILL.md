---
name: house-contract
description: Read a home purchase contract, riders, addenda, disclosures or an attorney engagement letter from the buyer's side and sort every clause into standard, risky, or not worth raising - then produce questions for the buyer's attorney phrased as confirmations, and a deadline list. Checks that the seller named is the owner of record, what the buyer waives (inspection or lead paint periods), what survives closing, environmental and certificate-of-occupancy clauses, notice addresses, and that promised repairs are written in. Use when a buyer shares a contract, rider, addendum, disclosure form or retainer letter, or asks "is this normal", "can we sign", "what did we agree to".
---

# House contract

The contract is where earlier promises either become enforceable or disappear. It is also written by people handling many deals at once, so small errors survive. This skill reads it clause by clause for the buyer and prepares a calm, short conversation with their attorney.

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

## First, which document is this

| Document | Between | Seen by the seller |
|---|---|---|
| Engagement or retainer letter | Buyer and their attorney: scope, fee, termination | No |
| Contract of sale, purchase agreement | Buyer and seller | Yes |
| Riders, addenda, amendments | Buyer and seller, attached to the contract | Yes |
| Disclosures (property condition, lead paint, others by state) | From the seller | Yes |
| Loan documents | Buyer and lender | No |

An engagement letter is not a contract review with the seller; questions about it only affect the buyer and their attorney.

Then identify the market: attorney-drafted (New York is one; read `references/new-york.md`) or a state standard form (California and Texas are examples). For a location without a reference file, work in generic mode: read what the document says, explain it plainly, and make every "is this normal here" a question for the attorney or agent.

## Three tiers

Read `references/checklist.md` for the full clause list. Sort every clause:

1. **Standard: confirm it is there.** Price, deposit and escrow holder, loan terms and commitment date, closing date and place, who pays which taxes, violations cleared by the seller, systems working at closing, included items, required disclosures.
2. **Risky: must be handled.** Anything that makes the buyer lose money or options without noticing. The recurring ones:
   - Seller named is not the owner of record, or their capacity (individual, heir, executor, trustee) is not stated.
   - A waived inspection period (for example the federal lead paint window for pre-1978 homes).
   - "As is" plus environmental risk transferred to the buyer and surviving closing (oil tanks, radon, asbestos).
   - A seller right to cancel if fixing violations or getting a certificate of occupancy costs more than a small cap.
   - Seller statements that do not survive closing, while the contract says unwritten promises end at closing.
   - Agreed repairs or the items a price cut replaced, not listed item by item.
   - Wrong notice addresses or emails for the buyer's side.
   - Deadlines that do not line up (loan commitment date after the closing date, a short cancellation window).
3. **Do not raise.** Cosmetic issues, re-negotiating price, repair items the buyer already gave up. After a seller has moved on price, a long list of new asks can end the deal.

When a point is customary to ask for, say why; when unsure whether it is customary, say that and make it a question.

## Deadlines

Compute every date the contract creates: signing, deposit, loan commitment, the notice window after it, inspection or disclosure windows, closing. Show the calendar math (for example, "60 days after both signatures; signing after October 16 pushes the commitment date past the December 15 closing"). These go into the case file and the buyer's calendar.

## Questions for the attorney

Phrase them as confirmations, not demands, and group them. Suggest the buyer first ask the attorney for their standard buyer rider, how they prefer to communicate, and which searches they run before signing, then send `assets/attorney-brief.md` filled in. End the brief with: "If anything we ask for is not customary, please tell us and we will drop it."

## Output

1. What each document is, in one table.
2. Must handle (tier 2), numbered, each with the clause location and why it matters.
3. Confirm only (tier 1) as a short list.
4. Do not raise (tier 3).
5. Deadlines.
6. Questions for the attorney, and an optional message draft for the buyer to send.
7. Human check: the attorney decides legal meaning; the buyer decides what to accept.

This is not legal advice. Record what the attorney answers in the case file.
