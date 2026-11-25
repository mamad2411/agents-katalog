---
name: vendor-evaluation
description: Use this skill when the user asks to evaluate a vendor, score candidate SaaS or services providers, build a vendor scorecard, or decide between two or more commercial options. Trigger phrases include "evaluate this vendor", "compare these tools", "should we buy X or Y", "vendor scorecard", "due diligence on this vendor", "evaluar al proveedor", "comparar estos servicios", "comprar X o Y". Produces a scorecard tied to concrete evidence, a comparison against alternatives, and a decision memo that names post-signing review triggers.
---

# vendor-evaluation

> **Anchor:** A vendor is a commitment with a price tag. Score both.

## When to use

Use this skill when the user needs a structured read on a commercial provider. Works for:

- A SaaS purchase with a non-trivial contract.
- A services engagement being chosen between two or more firms.
- A renewal decision for an incumbent vendor.
- An acquisition or integration partner evaluation.
- A "why we chose X over Y" memo after a competitive process.

Do not use when:

- The user is responding to a vendor questionnaire sent to them. Use `security-questionnaire` or `rfp-response`.
- The user is evaluating a candidate for hire. Use `candidate-evaluation`.
- The user is scoping an engagement with a vendor that has already been chosen. Use `proposal-scoping`.

## Voice rules (apply to all outputs)

- No buzzwords: leverage, empower, synergy, resonate, tapestry, delve, elevate, captivate, explore, dynamic, testament.
- No em dashes.
- No filler openings.
- Decision-oriented over descriptive.
- High-context, no overexplaining.
- Standard sentence case for formal outputs.
- ES outputs match the register of the handbook: direct, self-aware, no reverence for process, comfortable naming failure.
- EN outputs use direct US business register. Do not soften bluntness into corporate-speak.
- Language switches based on audience, not author.

## Bilingual handling

- **ES.** Rioplatense register. Vos over tú. Keep standard terms in English: SLA, MSA, DPA, NDA, uptime, roadmap, auto-renew, termination for convenience, switching cost, incumbent, POC, TCO, payment terms, carve-out, escalation.
- **EN.** Direct US business register. Avoid "partnership" as a descriptor of a commercial relationship. Do not soften concerns.
- Vendor names and product names stay as-is.

## Method

### Step 1. Define what is being bought

A vague purchase produces a vague evaluation. Write:

- **Category.** Tool, services, platform, marketplace, infra.
- **Scope.** Specific features, seats, regions, data classes.
- **Criticality.** What fails if the vendor fails. Revenue, uptime, data, compliance.
- **Duration.** Contract length and renewal shape.
- **Incumbent, if any.** Current vendor. What moving away from them costs.

### Step 2. Pick the rubric

Default rubric has nine dimensions:

1. **Delivery risk.** Can the vendor actually deliver what they claim.
2. **Pricing fairness.** Price against market and against value returned.
3. **Technical stack fit.** Compatibility with existing systems, data, and security posture.
4. **Commercial terms.** Contract, liability, IP, termination, auto-renew.
5. **Reference quality.** Same-sector, same-scale, contactable references.
6. **Incumbent switching cost.** The real cost of moving, including hidden ones.
7. **Support and escalation.** Speed, channels, accountability, SLA enforceability.
8. **Roadmap alignment.** Their roadmap vs. your needs over the contract life.
9. **Team and culture.** Who you will actually work with. How they operate when pressured.

For each purchase, remove what does not apply, upweight what does. A one-time tool purchase downweights dimensions 8 and 9. A deep integration upweights them. Keep the rubric under 10 dimensions.

### Step 3. Score each dimension against anchors

Scoring scale: 1 to 5. Anchors below, one short paragraph per dimension.

**Delivery risk.**
- 1: Cannot produce evidence they have delivered the claimed capability at comparable scale.
- 3: Can show delivered work at comparable scale. Honest about limits.
- 5: Track record is both deep and recent. Demonstrated behavior under stress that matches what you are buying.

**Pricing fairness.**
- 1: Price is out of line with market or with value, or list is a negotiating fiction.
- 3: Price aligns with market. Negotiation was possible and produced reasonable terms.
- 5: Price is clearly favorable. The vendor is not trading long-term lock-in for short-term discount, or is transparent that they are.

**Technical stack fit.**
- 1: Integration requires rewriting your surfaces or weakening your security posture.
- 3: Integration fits existing patterns. Known workarounds are acceptable.
- 5: Integration is clean, documented, tested, and does not create new key-person risk.

**Commercial terms.**
- 1: Terms concentrate risk on you. Unlimited auto-renew, no exit, IP carve-outs favoring them, liability caps that are nominal.
- 3: Terms are balanced. Exit is possible with notice. Liability is meaningful.
- 5: Terms are client-friendly. Termination for convenience, clear IP treatment, meaningful liability, data return and destruction specified.

**Reference quality.**
- 1: References are not contactable, not same-sector, or obviously curated.
- 3: Two or more same-sector references, contactable, with consistent signal.
- 5: References volunteer specific failure modes the vendor handled well. Willing to be contacted again.

**Incumbent switching cost.**
- 1: Switching cost was not measured, or was measured optimistically.
- 3: Switching cost is measured in dollars, weeks, and disruption. The new vendor's value clears it.
- 5: Switching cost is small, or the new vendor helps absorb the switch explicitly.

**Support and escalation.**
- 1: Support is an email address. SLAs exist on paper only.
- 3: Clear channels, named escalation path, SLAs you believe.
- 5: Named humans, time-boxed escalation, support that understands your specific setup, SLAs tied to real credits.

**Roadmap alignment.**
- 1: Vendor roadmap conflicts with your needs or is opaque.
- 3: Roadmap aligns over the contract life. Vendor is transparent about priorities.
- 5: Roadmap is directly relevant. Vendor is willing to share pre-release access or influence on priority.

**Team and culture.**
- 1: Sales team disappears after signing. Post-sale team is a different company in behavior.
- 3: Consistent team across sales and post-sale. Professional under pressure.
- 5: Team operates as collaborators who name their own limits. They flag their risks without being asked.

Every score carries evidence, as with candidate evaluation. A score without evidence is a vibe.

### Step 4. Compare against at least one real alternative

A single-vendor evaluation is not an evaluation. Name:

- **Alternative A.** The other serious option considered.
- **Alternative B.** The build-in-house or stay-with-incumbent option, with its real cost.
- **Do nothing.** The consequences of not buying anything.

For each alternative, run a condensed version of the scorecard (top three dimensions that differ from the primary candidate).

### Step 5. Run the "what if they fail" check

Ask explicitly:

- What happens if the vendor is acquired and the acquirer shuts down the product.
- What happens if the vendor goes bankrupt mid-contract.
- What happens if the vendor raises prices 2x at renewal.
- What happens if the vendor has a security incident involving your data.
- What happens if the vendor's best engineer for your account leaves.

For each, name the mitigation. "We'll cross that bridge" is not a mitigation.

### Step 6. Write the decision memo

Structure:

- **Recommendation.** Buy, do not buy, or buy a smaller scope to prove it out.
- **Summary.** Two sentences on why.
- **Scorecard.** Dimension by dimension, with evidence.
- **Comparison.** Against alternatives.
- **Concerns.** Even for buy recommendations, at least two.
- **Negotiation priorities.** The top three terms to push on if the deal advances.
- **Post-signing review triggers.** What would cause a mid-contract renegotiation or exit.

### Step 7. Define the review cadence

A signed contract is not the end of the evaluation. Before signing, define:

- **Health review cadence.** Monthly or quarterly.
- **Exit triggers.** Concrete signals that would cause non-renewal.
- **Escalation procedure.** Who in your company calls who at the vendor when something breaks.
- **Renewal readiness.** When the evaluation for renewal starts, relative to the renewal date. Earlier than you think.

## Templates

- `templates/en/scorecard.md`: per-vendor scorecard with evidence and comparison.
- `templates/en/decision-memo.md`: buy or do-not-buy decision memo.
- `templates/es/scorecard.md`: scorecard por proveedor con evidencia y comparación.
- `templates/es/decision-memo.md`: memo de decisión comprar o no comprar.

## Related skills

- `security-questionnaire`: use it when you are the vendor answering a buyer's assessment, not scoring vendors.
- `rfp-response`: use it when responding to a procurement document rather than evaluating providers.
- `candidate-evaluation`: the same scorecard discipline applied to hiring a person, not buying a vendor.
- `proposal-scoping`: move to it once the vendor is chosen and the engagement needs scoping.

## Anti-patterns

This skill must never produce:

- A scorecard for a single vendor with no alternative considered.
- A score without evidence.
- A memo that uses "strategic partnership" as a descriptor.
- A memo that recommends buying based on demo polish.
- Incumbent comparisons that ignore switching cost.
- Recommendations without named post-signing review triggers.
- Evaluations that score demo teams rather than post-sale teams.
- A recommendation that treats the vendor's roadmap as guaranteed.

## Checklist before delivery

- [ ] Category, scope, criticality, duration, and incumbent are named.
- [ ] Rubric is chosen with purchase-specific weighting.
- [ ] Every score has concrete evidence.
- [ ] At least one real alternative is scored in comparison.
- [ ] "What if they fail" scenarios are written with mitigations.
- [ ] Memo names concerns even in buy recommendations.
- [ ] Negotiation priorities are listed.
- [ ] Post-signing review triggers are defined.
- [ ] No buzzwords from the voice rules appear.
