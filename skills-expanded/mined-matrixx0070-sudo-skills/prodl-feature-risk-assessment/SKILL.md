---
name: prodl-feature-risk-assessment
version: 1.0.0
description: Assess the legal and regulatory risk of a single product feature by severity and likelihood, then assign owned mitigations and an escalation path.
author: matrixx0070
tags: [product-legal, feature, risk, assessment, mitigation, escalation]
capabilities: []
---

## When to use
Use this to size the risk of one product feature — an AI recommendation, a data-sharing toggle, a dark-pattern-prone flow, a new payment mechanism — before it ships. It converts "this feels risky" into a rated, owned item that leadership can weigh against the launch date.

**Not for:** whole-launch sign-off (use `prodl-launch-review`), marketing copy (use `prodl-marketing-claims-review`), or a fast yes/no gut check (use `prodl-is-this-a-problem`). Run this once per feature.

## Method
1. **State the feature and its behavior.** What it does, to whom, and what data or money moves.
2. **Identify the legal hook.** Which regime touches it: consumer protection, privacy, dark patterns, accessibility, IP, sector rules.
3. **Rate severity (1-5).** Financial exposure, regulatory penalty, litigation, reputational harm. Name the driver.
4. **Rate likelihood (1-5).** Base it on precedent, enforcement trends, and how the feature is actually used. Note the basis.
5. **Derive the tier** from severity × likelihood: Low / Medium / High / Critical.
6. **Assign mitigation.** For each material risk, an action that lowers one axis, with owner and date.
7. **Set escalation and a review trigger.** Who acts by when; what event forces re-assessment.

## Example
Feature: a pre-checked "share my data with partners" box. Legal hook: FTC dark-pattern / consent guidance and CPRA opt-out. Severity: 4 (regulatory penalty, class-action exposure). Likelihood: 4 (pre-checked consent is an active enforcement target). Tier: Critical → counsel same day. Mitigation: default the box to unchecked and add an affirmative opt-in (owner: Product, before launch). Residual: Low. Review trigger: any change to the consent flow.

## Pitfalls
- **Scoring on gut feel.** Likelihood needs an evidence basis — cite precedent or enforcement data.
- **Bundling features.** One assessment per feature, or the tier blurs.
- **Mitigations without an owner or date.** An unowned control is a wish.
- **Ignoring how users actually behave.** Intended use and real use diverge; rate the real one.

## Output format
```
Feature: <what it does>
Legal hook:
Severity: <1-5> — driver:
Likelihood: <1-5> — basis:
Tier: Low | Medium | High | Critical
Mitigation: <action> — owner: <name> — by: <date>
Escalation: <who> by <when>
Residual risk / review trigger:
```

## Reference
**FTC substantiation.** If the feature makes or implies a claim (an AI "detects fraud", a filter is "medical-grade"), the claim needs a reasonable basis before launch; efficacy and health claims need competent, reliable scientific evidence.

**Launch-risk rubric.** Any Severity-5 feature is at least High; Sev5 with Likelihood 3+ is Critical. High severity or a high severity×likelihood product pushes the tier up. Audience vulnerability (minors, health, finance) raises the floor.

**When to escalate to counsel.** Escalate any Critical tier, any Severity-5, dark-pattern/consent flows, children's data, or a novel feature with no precedent. This skill spots and sizes issues; it is not legal advice, and an attorney owns the go/no-go on flagged features.
