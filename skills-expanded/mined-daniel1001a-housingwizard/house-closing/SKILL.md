---
name: house-closing
description: Get a home purchase from signed contract to keys without losing money on a missed deadline - loan commitment and cancellation windows, rate lock timing, appraisal, title and survey, homeowner's insurance binder, utilities, final walkthrough, closing-day wire fraud protection, and the first week after closing. Use when a buyer has signed or is about to sign, asks "what happens now", "when do we lock", "what is clear to close", "how do we wire the money safely", "what do we do after we get the keys", or needs a dated checklist to closing.
---

# House closing

After signing, most of the work belongs to the lender, the attorney or title company, and the insurer. The buyer's job is to hit deadlines, not change their financial profile, and not wire money to a fraudster. This skill builds the dated checklist and keeps it honest.

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

## Build the calendar

From the contract (house-contract) and lender, compute and list with dates:

- Loan commitment date, and the last day to send written cancellation if the loan is not approved.
- Rate lock expiry, and whether the lock covers the closing date plus a buffer.
- Appraisal date; what happens if it comes in low given the loan terms.
- Title search and survey ordered; any title issue that could delay (estates, life estates, liens, open permits).
- Insurance binder due to the lender.
- Final walkthrough (usually within 24 to 48 hours of closing).
- Closing date, time and place; what to bring (ID, certified funds or wire confirmation).

Mark which dates the buyer controls and which they must chase.

## Rules for this stretch

- Do not change jobs, open new credit, finance furniture or cars, or move large unexplained sums. Ask the lender before any gift money moves.
- Keep deposits for furniture or custom orders refundable until clear to close.
- Answer lender document requests the same day.

## Wire fraud

Closing funds are a target. Before sending any wire: call the title company or attorney at a phone number the buyer found independently (their website, the engagement letter), not one from an email, and confirm the account details verbally. Treat any "updated wiring instructions" email as suspicious by default. A wire to the wrong account is usually not recoverable.

## Final walkthrough

Use the final walkthrough section of house-visit's checklist: run the heat, run the appliances, check for new water marks, confirm every agreed repair with its receipt or warranty, confirm included items and that the seller's things are gone.

## First week after closing

- [ ] Change or rekey all locks
- [ ] Find and label the main water shutoff, gas shutoff and electrical panel
- [ ] Utilities, internet and mail in the buyer's name
- [ ] Test smoke and carbon monoxide alarms; change HVAC filters
- [ ] File for any property tax exemptions or credits the buyer qualifies for (they often must be applied for)
- [ ] Save the deed, title policy and closing statement electronically
- [ ] If unpermitted work exists, decide the legalization order before pulling any other permit (house-renovation)

## Output

A dated checklist in order, each line tagged with who does it, plus the three dates that cost money if missed at the top. Write it into the case file.

Human check: the buyer confirms every date against the signed contract and the lender's commitment letter; the AI's date math is a draft.
