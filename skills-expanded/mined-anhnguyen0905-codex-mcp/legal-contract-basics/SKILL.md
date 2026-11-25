---
name: legal-contract-basics
description: Contract review fundamentals (not legal advice) — contract structure, key clauses checklist (term and termination, liability caps, indemnification, IP ownership, confidentiality/NDA, payment terms, warranties, governing law, auto-renewal), redline etiquette, red-flag review and risk flagging for business review, renewal terms, vendor agreement and NDA triage, plain-language clause summaries, first-pass data privacy compliance checklists (GDPR). Use for first-pass contract/NDA review and flagging clauses for counsel.
---

# Contract Review Basics (first-pass business review, not legal advice)

**This is not legal advice.** The output of this skill is a *flag list for counsel review*, never a
legal opinion or a sign-off. Anything marked HIGH must go to a qualified lawyer before signature;
never state that a contract is "safe to sign."

## Method — read in this order

1. **Parties and defined terms.** Confirm the legal entity names match who you think you're
   contracting with (parent vs subsidiary matters for enforcement). Skim the Definitions section
   first — a benign clause can hide behind a hostile definition ("Confidential Information",
   "Services", "Deliverables").
2. **Commercials.** Price, payment terms (net-30/60/90), late fees, price-increase mechanics,
   minimum commitments, true-up clauses.
3. **Term and exit.** Initial term, renewal mechanics, termination for convenience vs for cause,
   cure periods, what survives termination, data return/deletion on exit.
4. **Risk allocation.** Liability cap, carve-outs from the cap, indemnification (who indemnifies
   whom, for what), warranties and disclaimers, insurance requirements.
5. **Ownership and confidentiality.** IP in deliverables (assignment vs license), background IP,
   feedback clauses, confidentiality scope and duration, residuals clauses.
6. **Boilerplate that isn't.** Governing law and venue, dispute resolution (arbitration?),
   assignment on change of control, force majeure, entire-agreement, amendment mechanics.

## Clause checklist — what "market" roughly looks like

```
Liability cap        : commonly 12 months of fees paid; uncapped = HIGH flag
Cap carve-outs       : typical — confidentiality breach, IP infringement, gross negligence;
                       carve-outs that swallow the cap (e.g. "any breach") = HIGH flag
Indemnification      : mutual for third-party IP/bodily-injury claims; one-way broad
                       indemnity from you = HIGH flag
Term / auto-renewal  : auto-renew with 30–60 day non-renewal notice window; note the
                       calendar deadline explicitly in the summary
Termination          : for-convenience with 30–90 days notice is buyer-friendly;
                       no exit before end of term = MEDIUM flag
IP ownership         : work-for-hire/assignment for paid custom work; vendor keeping
                       ownership of paid deliverables = HIGH flag
Confidentiality      : mutual, 2–5 year term (trade secrets often perpetual); one-way
                       NDA where both sides disclose = MEDIUM flag
Payment              : net-30 typical; prepayment of >3 months or non-refundable fees = MEDIUM
Warranties           : conformance to spec + non-infringement; "AS IS" in a paid B2B
                       deal = MEDIUM flag
Governing law/venue  : neutral or your jurisdiction preferred; foreign law + mandatory
                       foreign venue + arbitration = flag for counsel, always
```

"Market" ranges above are heuristics for triage, not standards — counsel decides what is acceptable.

## Risk flagging format

For each flagged clause produce: **section reference → plain-language summary (one sentence) →
why it matters to the business → severity (HIGH / MEDIUM / LOW) → suggested ask** (the redline
position, e.g. "cap at 12 months fees, mutual"). HIGH = can't sign without counsel; MEDIUM =
negotiate if leverage allows; LOW = note and accept.

## Redline etiquette

- Edit with tracked changes; never retype the document or edit silently.
- Change the minimum text that achieves the position; don't rewrite whole clauses for style.
- Every redline carries a one-line rationale in a comment — naked deletions stall negotiations.
- Concede LOW items explicitly to buy movement on HIGH items; keep a concessions log.
- Round-trip the same document version; parallel edited copies create "which draft governs" disputes.

## Failure modes

- Reading clauses without the Definitions section — the definition is where the trap lives.
- Treating a liability cap as protection without checking the carve-outs that gut it.
- Missing the auto-renewal notice window and getting locked in for another year.
- Reviewing the MSA but not the order form/SOW/DPA that overrides it ("order of precedence" clause).
- Summarizing what a clause *says* instead of what it *does to this deal* — context-free summaries
  are noise.
- Letting an LLM or template review substitute for counsel on HIGH-severity items.

## Reviewer checklist

- [ ] Output framed as flags for counsel, with an explicit not-legal-advice note
- [ ] Parties, term, renewal deadline, and total commitment stated up front
- [ ] Liability cap, carve-outs, and indemnity direction all captured together
- [ ] IP ownership of paid deliverables confirmed, not assumed
- [ ] All attached documents reviewed (order form, SOW, DPA, referenced URLs/policies)
- [ ] Every flag has severity + plain-language impact + suggested ask
- [ ] HIGH flags routed to counsel before any signature recommendation

## Provenance

Common B2B contracting heuristics. "Market" ranges are **derived, unverified** defaults that vary
by jurisdiction, industry, and leverage — counsel's judgment always overrides this skill.
