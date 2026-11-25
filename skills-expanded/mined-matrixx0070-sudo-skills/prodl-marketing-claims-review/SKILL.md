---
name: prodl-marketing-claims-review
version: 1.0.0
description: Vet marketing claims for substantiation and truthfulness under FTC standards, flagging each as supported, needs-proof, or unlawful with a fix.
author: matrixx0070
tags: [product-legal, marketing, claims, ftc, substantiation, advertising]
capabilities: []
---

## When to use
Use this to review advertising and marketing copy — landing pages, ads, email, packaging, in-app promos — claim by claim, for truthfulness and substantiation. It catches the phrases that draw FTC and state-AG enforcement and NAD challenges before they ship.

**Not for:** whole-launch sign-off (use `prodl-launch-review`), feature/data risk (use `prodl-feature-risk-assessment`), or a one-line gut check (use `prodl-is-this-a-problem`).

## Method
1. **Extract every claim verbatim.** Split copy into discrete objective statements; ignore pure puffery (subjective, non-measurable praise) but flag anything a consumer could take literally.
2. **Classify each claim.** Establishment ("clinically proven"), comparative ("2x faster than X"), superlative ("#1", "best"), pricing ("was/now", "free"), or guarantee.
3. **Demand the basis.** For each objective claim, ask what evidence exists *now* and whether it fits the claim type.
4. **Rate each claim:** Supported (evidence on file, on point) / Needs-proof (plausible but unsubstantiated) / Unlawful (false, or a type of claim you can't back).
5. **Check disclosures.** Material terms, conditions, and "results not typical" qualifiers must be clear and conspicuous, not buried.
6. **Prescribe a fix.** Soften, substantiate, or drop — give the compliant alternative wording.

## Example
Copy: "The #1 dentist-recommended whitener — removes 10 years of stains, guaranteed." Review: "#1 dentist-recommended" = establishment/superlative, needs a survey on file → Needs-proof; "removes 10 years of stains" = quantified efficacy, needs a study → Unlawful without one; "guaranteed" = needs stated refund terms → Needs-proof. Fix: cite the survey or drop "#1"; replace the stain claim with a substantiated one; attach guarantee terms clearly.

## Pitfalls
- **Confusing puffery with a claim.** "Amazing taste" is puffery; "clinically shown to improve X" is not — the second needs proof.
- **Accepting future proof.** Substantiation must exist *before* the claim runs, not "we'll get the study later".
- **Missing implied claims.** A before/after image implies a typical result even with no words.
- **Buried disclosures.** A material qualifier in 6pt gray footer text is not clear-and-conspicuous.

## Output format
```
Claim (verbatim):
Type: establishment | comparative | superlative | pricing | guarantee
Evidence on file:
Rating: Supported | Needs-proof | Unlawful
Fix / compliant wording:
Disclosure check:
```

## Reference
**FTC substantiation.** Advertisers must have a reasonable basis for objective claims *before* dissemination (FTC Policy Statement on Advertising Substantiation). Health, safety, and efficacy claims require competent and reliable scientific evidence — typically well-designed human studies for health claims. Comparative claims need head-to-head support; establishment claims ("proven", "tested") need evidence matching the claimed level of proof. Endorsements and testimonials must reflect typical results and disclose material connections (FTC Endorsement Guides). Disclosures must be clear and conspicuous (FTC .com Disclosures / dark-patterns guidance).

**Launch-risk rubric.** Any Unlawful claim → Stop/No-go until fixed. Needs-proof → hold pending substantiation. Health, financial, and to-minors claims raise the floor regardless of company risk tolerance.

**When to escalate to counsel.** Escalate every Unlawful claim, all health/medical/financial-performance claims, comparative claims naming a competitor (Lanham Act exposure), and any claim you intend to run despite thin proof. This skill applies FTC standards for issue-spotting; it is not legal advice, and an attorney owns approval of contested or high-exposure claims.
