---
name: smb-contract-review
version: 1.0.0
description: Lightweight NDA, MSA, and vendor-contract first pass that flags non-standard terms in plain English and outputs a redline — not legal advice.
author: matrixx0070
tags: [legal, contracts, review, risk, operations, redline]
capabilities: []
---

# Contract Review

## When to use
Use this for a fast first pass on an NDA, MSA, or vendor agreement before it reaches a lawyer or your signature. It catches unusual, one-sided, or risky terms and explains them plainly.

**Not for:** legal advice, litigation, regulated or high-value deals where counsel is required, or anything you're about to sign without review. It flags and redlines; it does not approve, sign, or replace a lawyer.

## Method
1. Read the full document and identify its type and the parties.
2. Check the standard risk areas: liability caps, indemnification, termination, auto-renewal, payment terms, IP ownership, confidentiality scope, non-compete, governing law, and data handling.
3. Flag each clause that is missing, non-standard, or unfavorable. Decision point: rate severity high/medium/low by real-world exposure — an uncapped indemnity is high; an odd notice address is low.
4. Propose specific redline edits or alternative language for the worst terms.
5. State clearly this is a preliminary review, not legal advice, and recommend a lawyer for high-severity items. The owner decides what to accept, negotiate, or escalate — nothing is signed here.

## Example
Vendor MSA, overall risk: High. Findings include: liability cap absent (High — vendor's exposure is unlimited against you); auto-renews for 12 months with 90-day notice (Medium — easy to miss the window). Redline for the cap: "Each party's total liability shall not exceed the fees paid in the 12 months preceding the claim." Recommend a lawyer for: the indemnification and IP-assignment clauses.

## Pitfalls
- **Presenting flags as legal advice.** Always mark it preliminary and route high-severity items to counsel.
- **Rating by clause name, not exposure.** Severity is about what it costs you if invoked, not how unusual the wording is.
- **Missing what's absent.** The dangerous term is often the missing liability cap, not the one that's written.
- **Vague redlines.** "Make this fairer" is useless; give exact before/after language.

## Output format
```
Summary: <contract type> — overall risk <High/Med/Low>
Findings:
| Clause | Severity | Plain-English concern | Suggested change |
Redlines:
  <clause>: BEFORE "..." / AFTER "..."
Recommend a lawyer for:
  - <high-severity items>
Reminder: preliminary review, not legal advice; owner approves any signature.
```

## Reference

### SMB red-flag catalog (what to hunt for)
For each clause, the table shows the balanced/standard position and the red flag that warrants a High or Medium flag:

| Clause | Standard / balanced | Red flag (severity) |
|---|---|---|
| **Limitation of liability** | Cap = fees paid in prior 12 months; mutual | No cap or one-sided cap; you uncapped, them capped (**High**) |
| **Indemnification** | Mutual, tied to each party's own fault/IP | You indemnify them broadly, no reciprocity, no cap, covers their negligence (**High**) |
| **Consequential-damages waiver** | Mutual waiver of indirect/consequential damages | Waiver protects only them (**Medium-High**) |
| **Payment terms** | Net-30, clear invoice/dispute process | Net-15 or on-receipt to you but net-60 from them; high late fees; auto-charge with no cap (**Medium**) |
| **Term & auto-renewal** | Renews with 30-day opt-out notice | Auto-renews 12 mo with 60-90 day notice window (evergreen trap) (**Medium**) |
| **Termination** | Either party for convenience (30-60 day) + for cause | Only they can terminate; you're locked in; no termination-for-cause (**High**) |
| **IP ownership** | You keep your pre-existing IP; work-product ownership defined | Broad assignment of your background IP; "work made for hire" grabbing your tools (**High**) |
| **Confidentiality / NDA** | Mutual, 2-3 yr term, standard carve-outs | One-way when it should be mutual; perpetual; no carve-out for public/independently-developed info (**Medium**) |
| **Non-compete / non-solicit** | Narrow, time-boxed (≤1 yr), reasonable geography | Broad non-compete blocking your normal business; solicit ban on all their contacts (**High**) |
| **Governing law / venue** | Your state or a neutral one | Distant state/country forcing costly travel to litigate (**Medium**) |
| **Data / privacy** | Defined data use, breach notice, deletion on exit, DPA if PII | No breach-notice duty; they can use/resell your data; no return/deletion (**High** if PII) |
| **Warranty / SLA** | Basic uptime/quality warranty with remedy | "As-is," no warranty, no SLA credits (**Medium**) |
| **Assignment** | Consent required to assign | They can assign to anyone (incl. a competitor) without consent (**Medium**) |
| **Price changes** | Fixed for term, or capped annual increase w/ notice | Unilateral price increases anytime (**Medium**) |
| **Exclusivity** | None, or narrowly scoped | Forces you to buy only from them / not serve their competitors (**High**) |

### Severity is about exposure, not oddness
Rate by "what does it cost me if invoked?": an uncapped indemnity can exceed the whole contract value → **High**; a wrong notice address is a nuisance → **Low**. The most dangerous clause is often the one that's *missing* (no liability cap, no termination right, no data-deletion duty), so always check for absence, not just bad wording.

### Redline library (paste-ready alternatives)
- **Add a liability cap:** "Except for [confidentiality / indemnity / gross negligence], each party's total aggregate liability shall not exceed the total fees paid or payable in the twelve (12) months preceding the event giving rise to the claim."
- **Make indemnity mutual:** "Each party shall indemnify the other against third-party claims to the extent arising from the indemnifying party's breach, negligence, or infringement."
- **Kill the evergreen trap:** "This Agreement renews for successive one-year terms unless either party gives written notice of non-renewal at least thirty (30) days before the end of the then-current term."
- **Add termination for convenience:** "Either party may terminate this Agreement for convenience upon thirty (30) days' prior written notice."
- **Protect your background IP:** "Each party retains all right, title, and interest in its pre-existing intellectual property. Nothing herein assigns Provider's tools, methods, or know-how."
- **Add breach notice:** "Provider shall notify Customer within seventy-two (72) hours of becoming aware of any breach of Customer data."

### Always-escalate-to-counsel list
Route to a lawyer (not just flag) when the contract involves: personal-injury or product-liability risk, PII/PHI/regulated data, a personal guarantee, equity or revenue-share, IP assignment of core products, exclusivity, non-competes, deal value large relative to the business, or anything with criminal/regulatory exposure.

### Owner-approval and not-legal-advice gate
Every output must state, plainly, that this is a preliminary business review and not legal advice. The skill flags, explains, and proposes redlines — it never approves terms, signs, or tells the owner a clause is "fine to accept." High-severity items go to counsel; the owner decides what to accept, negotiate, or escalate, and the owner alone signs.
