---
name: prodl-launch-review
version: 1.0.0
description: Run a full go/no-go legal review of a product launch across claims, data, commitments, and audience, producing a tiered verdict with conditions.
author: matrixx0070
tags: [product-legal, launch, review, go-no-go, compliance, verdict]
capabilities: []
---

## When to use
Use this for the comprehensive pre-launch pass — the review that produces a go / go-with-conditions / no-go verdict for a feature, product, or campaign. It pulls together the intake, per-feature risk, and claim reviews into one defensible decision the launch team can act on.

**Not for:** a quick gut check (use `prodl-is-this-a-problem`), initial fact-gathering (use `prodl-cold-start-interview`), or sizing a single feature or claim (use `prodl-feature-risk-assessment`, `prodl-marketing-claims-review`).

## Method
1. **Load the intake and profile.** Start from the `prodl-cold-start-interview` record and the `prodl-customize` profile; if either is missing, gather it first.
2. **Review each domain.** Claims (substantiation on file?), data (consent, disclosure, transfers), commitments (pricing, renewal, trial, refund), audience (minors, jurisdictions), IP (marks, third-party content).
3. **Rate each finding** by severity × likelihood; carry Critical/High items forward.
4. **Assign conditions.** Each material finding gets a required fix, owner, and deadline relative to go-live.
5. **Compute the verdict.** Go (no open material findings) / Go-with-conditions (findings with owned fixes before launch) / No-go (an unresolved Critical).
6. **Record the escalation trail.** Which findings went to counsel and their disposition.
7. **Set a post-launch review trigger.**

## Example
A campaign launches "the most accurate tracker on the market" with a 30-day free trial auto-billing $120. Findings: (1) superlative accuracy claim, no comparison data on file — High; (2) trial auto-conversion lacks the clear-and-conspicuous disclosure ROSCA requires — Critical. Verdict: Go-with-conditions → drop or substantiate the superlative (owner: Marketing) and add a compliant renewal disclosure + easy cancel (owner: Product), both before go-live; the Critical routed to counsel who signed off on the disclosure copy.

## Pitfalls
- **Reviewing copy without the data and commitments.** A launch fails on renewal terms as often as on claims.
- **Conditions without deadlines.** "Fix before launch" with no owner slips past go-live.
- **Passing a Critical as a condition.** An unresolved Critical is a no-go, not a condition.
- **No paper trail.** Record what counsel saw and decided; verdicts get questioned later.

## Output format
```
Launch: <name> — go-live: <date>
Findings:
  - <domain>: <issue> — Sev/Like — Tier — condition — owner — by
Verdict: Go | Go-with-conditions | No-go
Conditions outstanding:
Escalated to counsel: <items + disposition>
Post-launch review trigger:
```

## Reference
**FTC substantiation.** Every objective claim needs a reasonable basis before dissemination; efficacy/health claims need competent, reliable scientific evidence. Comparative and superlative claims need head-to-head support. A claim with no evidence on file is a material finding, minimum High.

**Launch-risk rubric.** Verdict = worst unresolved finding. Any unresolved Critical → No-go. Any Severity-5 is at least High. Audience vulnerability (minors, health, finance) and mandatory disclosures (auto-renewal/ROSCA, privacy) raise the floor regardless of company risk tolerance.

**When to escalate to counsel.** Every Critical, every Severity-5, and any regulated-category finding (health, kids, fintech, new jurisdiction, data transfers) goes to an attorney before the verdict is final. This skill structures the review and records the decision; it is not legal advice, and an attorney owns sign-off on all escalated findings.
