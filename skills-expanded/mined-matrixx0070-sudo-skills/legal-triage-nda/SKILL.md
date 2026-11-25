---
name: legal-triage-nda
version: 1.0.0
description: Triage an incoming NDA against standard terms and classify it GREEN, YELLOW, or RED with a recommended action and specific edits.
author: matrixx0070
tags: [legal, nda, triage, confidentiality, review, escalation]
capabilities: []
---

## When to use
Use this when an NDA arrives and someone needs a fast, consistent read: sign as-is, negotiate lightly, or send to counsel. It applies a standard rubric so NDAs don't silently pile up or get signed with hidden traps.

**Not for:** NDAs bundled inside a larger agreement (review the whole via `legal-review-contract`), high-stakes M&A or litigation confidentiality (escalate), or drafting an NDA from scratch. This triages incoming standalone NDAs only.

## Method
1. **Capture the basics.** Parties, one-way vs. mutual, purpose, and which disclosure direction matters to us.
2. **Check core terms** against standard: definition of confidential information, permitted use, exclusions (public, independently developed, already known), term and survival, return/destruction, governing law.
3. **Scan for red flags:** non-competes or non-solicits hidden inside, IP assignment, indemnification, unlimited/perpetual duration, unusually broad "confidential" definitions, one-sided obligations on us, residuals clauses, foreign jurisdiction.
4. **Classify.** *Decision points:* GREEN = standard, mutual, reasonable term → sign as-is. YELLOW = minor deviations fixable with playbook edits → negotiate. RED = any red-flag term, IP/indemnity/non-compete, or high-stakes counterparty → escalate to counsel.
5. **Recommend action** matching the color, with specific edits for YELLOW.
6. **Note the deadline** and who owns the next step.

## Example
Incoming: one-way NDA, we are the receiving party, purpose "evaluate a partnership." Core terms mostly standard, but two issues: term survives 7 years (standard is 3-5) and it includes an IP-assignment clause granting them rights to anything we create during discussions. Red flag: IP assignment. Classification: RED. Recommended action: escalate to counsel; do not sign. Owner: deal lead, deadline: before next partner call Thursday.

## Pitfalls
- **Skimming for the confidentiality clause only.** The trap is usually a smuggled non-compete or IP-assignment term elsewhere.
- **Calling a one-sided NDA GREEN.** If all obligations fall on us, it isn't standard — that's at least YELLOW.
- **Negotiating a RED item yourself.** IP, indemnity, and non-competes go to counsel, not playbook edits.
- **No deadline.** An untriaged NDA that "we'll get to" blocks the deal it gates.

## Output format
```
Parties / type (one-way|mutual) / purpose:
Classification: GREEN | YELLOW | RED
Term check table:
  | Term | Standard | This NDA | OK? |
Red flags (if any):
Recommended action: sign | negotiate (edits: ...) | escalate to counsel
Owner & deadline:
```

## GREEN / YELLOW / RED rubric
Classify against the criteria below. When an NDA straddles tiers, take the **highest** tier any single term triggers — one RED term makes the whole NDA RED.

### GREEN — sign as-is
All of the following hold:
- Mutual (obligations run both ways).
- Standard definition of confidential information (marked or reasonably-should-be-understood as confidential).
- Standard exclusions all present: public knowledge, independently developed, already known/rightfully received, and required-by-law disclosure.
- Term 2-5 years — or perpetual **only** for trade secrets, not ordinary confidential info.
- Governing law in a familiar US state.
- Mutual return/destruction of confidential info on request or termination.
- No obligations beyond confidentiality (no IP, no indemnity, no non-compete, no payment).

### YELLOW — negotiate with playbook edits
One-sided but fixable, or a single non-fatal deviation:
- One-directional obligations where a mutual version is reasonable.
- Term 5-7 years on ordinary confidential info.
- Exactly one standard exclusion missing (add it back).
- Overbroad "confidential information" definition (narrow to marked/should-be-understood).
- Injunctive relief permitted without requiring a bond (acceptable but note it; push for "without waiving other remedies" balance).
- No notice-of-compelled-disclosure right (add: you'll give notice before responding to a subpoena where legally allowed).
- Non-standard but **domestic** jurisdiction (negotiate toward a familiar state).

### RED — escalate to counsel, do not self-negotiate
Any one of these:
- Any IP assignment or ownership grant.
- Indemnification obligation.
- Non-compete or non-solicit / no-poach.
- Residuals clause that strips protection (lets them freely use "retained in memory" info).
- Perpetual term on ordinary confidential information.
- Liquidated damages / stipulated penalty.
- Foreign jurisdiction or foreign governing law.
- M&A, financing, or active-litigation context.
- Term > 7 years.
- Unlimited liability.
- Broad "no reverse-engineering" combined with actual source-code or system access.

## Standard term reference

| Term | Standard | Negotiate-down target |
|---|---|---|
| Confidentiality period | 3-5 years (perpetual only for trade secrets) | 2 years for ordinary info; carve trade secrets to "while secret" |
| Exclusions list | Public, independently developed, already known/rightfully received, required by law | Restore any missing exclusion; add "required by law" with notice |
| Permitted-use scope | Limited to the stated evaluation/business purpose only | Tighten a vague "any business purpose" to the specific deal |
| Return/destruction window | Within 30 days of request or termination; certification on request | 30 days; allow one archival/backup copy under continuing confidentiality |
| Residuals | Absent (preferred) | Strike entirely; if kept, limit to true unaided memory and never for trade secrets |
| Injunctive relief | Mutual, without waiving other remedies | Keep mutual; resist any admission that breach = automatic irreparable harm |
| Governing law | Familiar US state, local courts | Move foreign/unfamiliar law to a neutral US state (or escalate if they refuse) |

## Reference
- **One-way vs. mutual.** If you will disclose anything at all, prefer mutual — a one-way NDA that names you as the sole receiving party puts every obligation on you. Flip a one-way to mutual as a default YELLOW edit.
- **Perspective flips which terms matter.** As the **disclosing** party you care about broad definitions, long terms, strong return/destruction, and injunctive relief. As the **receiving** party you care about tight scope, complete exclusions, short terms, residuals, and not inheriting IP or non-compete obligations. Read the NDA from the seat you actually occupy.
- **Common smuggled traps.** Watch for a non-solicit buried inside a "no-poach" or "no-hire" sentence; an IP assignment hidden inside a "work product" or "feedback/suggestions" clause; and auto-renewing or evergreen confidentiality that quietly becomes perpetual. These are the terms that turn an apparently GREEN NDA into a RED one — scan the whole document, not just the clause labeled "Confidentiality."
