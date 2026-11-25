---
name: smb-review-contract
version: 1.0.0
description: Review a contract in plain English, flag red flags by severity, and return a marked-up redline with suggested edits.
author: matrixx0070
tags: [contract, legal, review, redline, risk, negotiation]
capabilities: []
---

# Review Contract

## When to use
Run this when the owner receives a contract, lease, vendor agreement, or client SOW and wants to understand it and negotiate before signing.

**Not for:** legal advice or high-stakes deals on its own — this is a plain-English review; recommend a lawyer when the stakes are high. Not for signing or sending anything on the owner's behalf.

## Method
1. **Read the whole document.** Identify the parties, the deal, term length, renewal, and termination mechanics.
2. **Explain in plain English.** What the owner is agreeing to, what they get, and what they owe.
3. **Scan for risk clauses.** Auto-renewal, unilateral changes, liability/indemnification, exclusivity, non-compete, payment terms, late fees, IP ownership, dispute venue.
4. **Rate each red flag.** Severity High/Medium/Low, a one-line "why it matters," and a suggested fix. Decision point: if any High-severity clause is present (uncapped liability, broad IP assignment, auto-renew with a long notice window), say plainly that a lawyer should see it before signing.
5. **Produce a redline.** Original text with proposed edits marked and short margin comments.
6. **Hand back the decision.** The owner decides what to accept, push back on, or walk away from. Nothing is signed or sent on their behalf without approval.

## Example
A SaaS vendor agreement: 12-month term, **auto-renews for 12 months unless cancelled 90 days out** (High — long lock-in, easy to miss; fix: 30-day notice, month-to-month after year one). Liability capped at fees paid (Medium — acceptable). **Vendor may change pricing "at any time" (High** — fix: cap increases at 5%/year with 60-day notice). Plain-English summary: you commit for a year, hard to exit, and price can jump. Redline marks the two High clauses with suggested language; note recommends a lawyer given the auto-renew lock-in.

## Pitfalls
- Summarizing only the friendly clauses and glossing over indemnification or IP ownership buried at the back.
- Rating everything "Medium" — severity has to discriminate or it's noise.
- Flagging a problem with no suggested fix, leaving the owner nothing to negotiate with.
- Presenting the review as legal advice; always steer high-stakes deals to a licensed lawyer.

## Output format
- **Plain-English summary** (5-8 sentences).
- **Red-flag table:** clause | severity | why it matters | suggested change.
- **Redline block:** tracked edits + margin comments.
- **Closing note:** recommend professional legal review when stakes are high; nothing signed or sent without owner approval.

## Reference

### SMB contract red-flag catalog
| Clause | Red flag | Severity | Owner-friendly fix |
|--------|----------|----------|--------------------|
| **Auto-renewal** | Renews for a full term unless cancelled 60-90 days out | High | 30-day notice; month-to-month after year one |
| **Unilateral price change** | Vendor may raise fees "at any time" | High | Cap increases (e.g. 5%/yr) with 60-day notice |
| **Uncapped liability** | No limit on what the owner owes if something goes wrong | High | Cap at fees paid in trailing 12 months |
| **Broad indemnification** | Owner covers vendor's losses, including third-party claims | High | Mutual indemnity, limited to each party's own fault |
| **IP assignment** | Vendor/client owns everything the owner creates | High | Owner retains pre-existing IP and tools; license only the deliverable |
| **Non-compete / exclusivity** | Owner can't work with competitors or other clients | High | Narrow scope, geography, and duration; or strike |
| **Personal guarantee** | Owner personally liable beyond the business | High | Remove; keep liability with the entity |
| **Evergreen term** | No end date | Medium | Fixed term with renewal option |
| **Net-60/90 payment** | Owner waits months to get paid | Medium | Net-30 or net-15; deposit up front |
| **No late-fee / interest** | Owner has no leverage on slow payers | Medium | 1.5%/mo interest on overdue |
| **Unilateral termination** | Vendor can exit anytime; owner can't | Medium | Symmetric termination for convenience |
| **Governing law / venue far away** | Disputes must be litigated across the country | Medium | Owner's home state, or arbitration nearby |
| **Confidentiality one-way** | Only owner bound to secrecy | Low | Make mutual |
| **Assignment without consent** | Contract can be sold to anyone | Low | Require consent to assign |

### Severity guide (make it discriminate)
- **High** = could cost real money, lock the owner in, or transfer ownership/liability. Any High → recommend a lawyer before signing.
- **Medium** = worth negotiating; not a dealbreaker alone.
- **Low** = nice-to-fix; note it, don't die on it.
If everything is "Medium," the review is noise — force the ranking.

### Plain-English translation cheatsheet
- "Indemnify and hold harmless" → *you pay their legal bills if they get sued over this.*
- "Sole discretion" → *they decide, you don't get a say.*
- "Time is of the essence" → *deadlines are legally binding, not aspirational.*
- "Liquidated damages" → *a pre-agreed penalty if you break the deal.*
- "Perpetual, irrevocable, worldwide license" → *they can use it forever, everywhere, and can't be taken back.*
- "Net 60" → *payment due 60 days after invoice.*
- "Auto-renew" → *it continues and re-bills unless you actively cancel in a specific window.*

### Contract-type quick focus
- **Commercial lease:** term, renewal, CAM/operating-expense pass-throughs, personal guarantee, assignment/sublease rights, escalation clause.
- **Vendor / SaaS:** auto-renew, price changes, data ownership + export on exit, uptime SLA, liability cap.
- **Client SOW:** scope creep / change-order process, payment schedule + deposit, IP ownership of deliverables, kill fee.
- **Employment / contractor:** classification (W-2 vs 1099), non-compete enforceability (varies by state — many are void), IP assignment, at-will language.

### Boundaries
This is a plain-English review, not legal advice. Always steer high-stakes or High-severity deals to a licensed attorney. Never sign, initial, or send the contract on the owner's behalf — the owner decides what to accept, counter, or walk from.
