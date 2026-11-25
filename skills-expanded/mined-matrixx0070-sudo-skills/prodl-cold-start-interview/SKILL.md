---
name: prodl-cold-start-interview
version: 1.0.0
description: Run a structured intake interview to surface a launch's legal-risk surface before any review starts, capturing facts, claims, and open questions.
author: matrixx0070
tags: [product-legal, launch, intake, interview, risk, discovery]
capabilities: []
---

## When to use
Use this at the very start, when a team brings you a launch, feature, or campaign and you know almost nothing yet. It pulls the facts you need — what ships, to whom, what you claim, what data flows — so later reviews rest on evidence instead of guesses.

**Not for:** rendering a verdict (use `prodl-launch-review` or `prodl-is-this-a-problem`), sizing one specific risk (use `prodl-feature-risk-assessment`), or vetting marketing copy line by line (use `prodl-marketing-claims-review`).

## Method
1. **Name the thing.** One sentence: what launches, when, and the go/no-go date.
2. **Map the audience.** Who sees it — consumers, minors, EU/CA residents, regulated segments (health, finance, kids)? Jurisdictions drive rules.
3. **List every claim.** Capture verbatim each performance, comparison, pricing, or guarantee statement. Flag superlatives ("best", "#1", "guaranteed").
4. **Trace the data.** What personal data is collected, shared, or sold; consent mechanism; third-party SDKs.
5. **Surface commitments.** Pricing, auto-renewal, free-trial terms, refund promises, availability SLAs.
6. **Log open questions.** Anything unknown becomes a tracked question with an owner, not a silent assumption.
7. **Produce the intake record.** Hand off a single fact sheet the downstream skills consume.

## Example
A team launches a "clinically proven" sleep app to US consumers in three weeks. The interview extracts: audience = US adults, no minors gate; claims = "clinically proven", "fall asleep 2x faster"; data = sleep audio to a third-party analytics SDK; commitments = 7-day trial auto-converting to $79/yr. Open questions: Is there a study backing "2x faster"? Is the SDK disclosed in the privacy policy? These become owned action items before review.

## Pitfalls
- **Accepting "it's fine" as an answer.** Record the underlying fact, not reassurance.
- **Skipping audience/jurisdiction.** The same claim is legal in one market, unlawful in another.
- **Paraphrasing claims.** Capture marketing language verbatim; nuance lives in exact words.
- **Treating unknowns as zeros.** An unanswered question is a red flag, not a pass.

## Output format
```
Launch: <one sentence> — go-live: <date>
Audience / jurisdictions:
Claims (verbatim): 1) ... 2) ...
Data flows: <collected / shared / consent>
Commitments (pricing, renewal, trial, refund):
Open questions: <question> — owner: <name>
Recommended next skill:
```

## Reference
**FTC substantiation.** Any objective product claim needs a "reasonable basis" *before* it runs; health, safety, and efficacy claims require competent and reliable scientific evidence. Log whether each claim has substantiation on file — absence is itself a finding.

**Launch-risk rubric.** Score the intake on four axes: claim aggressiveness, data sensitivity, audience vulnerability (minors, health, finance), and reversibility of the launch. High on any axis routes to a full review.

**When to escalate to counsel.** Route to an attorney when the intake reveals health/medical claims, children's data (COPPA), a new jurisdiction, or a commitment you cannot substantiate. This skill is intake and issue-spotting; it is not legal advice, and an attorney owns the final call on any flagged item.
