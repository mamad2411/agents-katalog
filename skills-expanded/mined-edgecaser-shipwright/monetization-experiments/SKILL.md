---
name: monetization-experiments
description: "Designs and evaluates pricing, packaging, and monetization experiments including free-to-paid conversion optimization, upsell trigger testing, plan structure changes, and price sensitivity tests. Applies experimentation rigor to the highest-leverage growth lever most teams are afraid to touch."
category: pricing
default_depth: standard
---

# Monetization Experiment Design

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Designs and evaluates pricing, packaging, and monetization experiments including free-to-paid conversion optimization, upsell trigger testing, plan structure changes, and price sensitivity tests. Applies experimentation rigor to the highest-leverage growth lever most teams are afraid to touch.

## When to Use

- Optimizing free-to-paid conversion rates
- Testing new pricing tiers or plan structures
- Evaluating upsell/cross-sell triggers
- Running a price increase with controlled rollout
- Testing the impact of feature gating changes

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick sanity check on a single variable (e.g., trial length or discount offer) | Experiment Hypothesis + Metrics + Kill Criteria only |
| **Standard** | Typical pricing or packaging test with controlled rollout | All sections |
| **Deep** | High-revenue-risk change (price increase on existing customers, major packaging overhaul) | All sections + segment-level metric breakdowns, legal review checklist, customer communication plan |

**Omit rules:** At Light depth, skip Experiment Design, Risk Assessment, and Rollout Plan. Produce only Hypothesis, primary/guardrail Metrics, and Kill Criteria.

## Framework

### Step 1: Experiment Hypothesis

```markdown
## Monetization Experiment: [Name]

### Hypothesis
We believe that [change to pricing/packaging/monetization]
will [expected outcome, e.g., "increase free-to-paid conversion by 15%"]
because [reasoning, e.g., "usage data shows 60% of free users hit the current limit within 2 weeks but don't convert because the jump to paid is too large"].

### Experiment Type
| Type | Description | Risk Level |
|---|---|---|
| [ ] Price point test | Test different price levels | Medium |
| [ ] Packaging test | Change what's in each tier | Medium |
| [ ] Feature gate test | Move features between tiers | Low-Medium |
| [ ] Paywall placement | Change when/where users hit upgrade prompts | Low |
| [ ] Free tier limit | Adjust free tier boundaries | Medium |
| [ ] Trial length | Test different trial durations | Low |
| [ ] Discount/promo | Test offer effectiveness | Low |
| [ ] Billing frequency | Test monthly vs. annual incentives | Low |
| [ ] Price increase | Raise prices for new or existing customers | High |
```

### Step 2: Experiment Design

```markdown
### Design

**Audience:**
- [ ] New signups only (cleanest test, no existing contract complications)
- [ ] Existing free users (tests conversion, larger sample)
- [ ] Existing paid users (tests expansion, high risk, handle carefully)

**Sample size calculation:**
- Baseline conversion rate: [X]%
- Minimum detectable effect: [Y]% relative change
- Statistical significance: 95%
- Power: 80%
- Required sample: [N] per variant
- Estimated duration: [N] weeks at current traffic

**Variants:**
| Variant | Description | What Changes |
|---|---|---|
| Control | Current pricing/packaging | Nothing |
| Treatment A | [Change description] | [Specific change] |
| Treatment B | [Change description, if testing multiple] | [Specific change] |

**Randomization:**
- Unit: [User / Account / Organization]
- Method: [Hash-based assignment / Feature flag service]
- Sticky: [Yes, user stays in variant for entire experiment]

**Exclusions:**
- Enterprise / custom-priced accounts (can't change their pricing mid-contract)
- Internal/test accounts
- [Any other exclusions with rationale]
```

### Step 3: Metrics

```markdown
### Metrics Framework

**Primary metric:**
| Metric | Control Baseline | Target | Measurement |
|---|---|---|---|
| [e.g., Free-to-paid conversion rate] | [X]% | [Y]% | [How measured] |

**Secondary metrics:**
| Metric | What It Tells Us | Measurement |
|---|---|---|
| ARPU | Revenue per user impact | [source] |
| Trial start rate | Demand signal | [source] |
| Expansion rate | Upsell effectiveness | [source] |
| Time to convert | Purchase urgency | [source] |

**Guardrail metrics (must NOT degrade):**
| Metric | Threshold | Why It Matters |
|---|---|---|
| New user signup rate | Must not drop > [X]% | Price visibility on landing page could deter signups |
| Churn rate (30-day) | Must not increase > [X]% | Higher conversion is worthless if they churn immediately |
| Support ticket volume | Must not increase > [X]% | Pricing confusion drives support load |
| NPS / CSAT | Must not drop > [X] points | Price increases can tank satisfaction |

**Revenue projection:**
If the experiment wins at the target effect size:
- Monthly revenue impact: +$[X]
- Annual revenue impact: +$[X]
- Payback period: [N] months
```

### Step 4: Risk Assessment

```markdown
### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Negative PR from price change | [H/M/L] | [H/M/L] | [Grandfather existing users, transparent communication] |
| Conversion drops instead of increases | [H/M/L] | [H/M/L] | [Kill criteria: stop if conversion drops >X% for >Y days] |
| Support overwhelm from confusion | [H/M/L] | [H/M/L] | [Pre-brief support team, prepare FAQ] |
| Revenue cannibalization | [H/M/L] | [H/M/L] | [Monitor ARPU alongside conversion] |
| Legal/contractual issues | [H/M/L] | [H/M/L] | [Legal review before launch, exclude contracted accounts] |

### Kill Criteria
Stop the experiment immediately if:
1. Primary metric drops > [X]% below control for > [N] consecutive days
2. Any guardrail metric crosses its threshold
3. Support ticket volume spikes > [X]% above normal
4. [Other condition specific to this experiment]
```

### Step 5: Rollout Plan

```markdown
### Rollout Plan

**Phase 1: Internal (Week 1)**
- Enable for internal team
- Verify tracking, billing integration, and edge cases
- Support team briefed

**Phase 2: Small Test (Weeks 2-3)**
- [10]% of new signups
- Monitor all metrics daily
- Check for SRM and data quality issues

**Phase 3: Full Test (Weeks 4-N)**
- Expand to full randomized split
- Run for minimum [N] weeks / [N] full business cycles
- Weekly metric reviews

**Phase 4: Decision (Week N+1)**
- Analyze results (use A/B Test Analysis skill)
- Ship, iterate, or kill

**If shipping the winner:**
- [ ] Migrate all users to new pricing (or grandfather existing)
- [ ] Update pricing page, docs, and marketing materials
- [ ] Brief sales team on new pricing/packaging
- [ ] Update billing system configuration
- [ ] Monitor for 30 days post-rollout
```

## Minimum Evidence Bar

**Required inputs:** Baseline conversion rate (or relevant monetization metric), current pricing/packaging structure, and traffic volume sufficient to estimate sample size. At Light depth, baseline metric and current pricing/packaging structure are sufficient, traffic volume for sample sizing is deferred.

**Acceptable evidence:** Product analytics (conversion funnels, ARPU, churn cohorts), prior experiment results, customer support ticket themes around pricing, competitive pricing data, user research on upgrade friction.

**Insufficient evidence:** If a baseline is unavailable, return a measurement and experiment-design draft with the baseline and sample-size calculation blocked. Set collection duration from traffic, variability, business cycles and minimum detectable effect; do not prescribe an arbitrary waiting period.

**Hypotheses vs. findings:**
- **Findings:** Baseline metrics, sample size requirements, guardrail thresholds, and kill criteria must be grounded in actual data.
- **Hypotheses:** Expected effect size and revenue projections are forward-looking estimates, must be labeled as such with stated assumptions.

## Output Format

Produce a Monetization Experiment Plan with:
1. **Hypothesis**, what we're testing and why
2. **Design**, variants, sample size, randomization
3. **Metrics**, primary, secondary, guardrails, revenue projection
4. **Risk Assessment**, risks with mitigations and kill criteria
5. **Rollout Plan**, phased deployment with checkpoints

**Shipwright Signature (required closing):**
6. **Decision Frame**, Ship/iterate/kill recommendation, revenue vs. churn trade-off, confidence level with evidence quality, experiment owner, decision date, revisit trigger (e.g., metric drift post-rollout)
7. **Unknowns & Evidence Gaps**, Segments not yet tested, long-term retention effects, price elasticity beyond tested range
8. **Pass/Fail Readiness**, PASS for launch if the hypothesis is falsifiable, sample size is achievable within a justified precommitted duration, and guardrails and kill criteria are defined. Light depth may PASS as a concept with sample sizing explicitly deferred, never as a launch-ready experiment.
9. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Testing price in isolation**, Price changes interact with packaging, messaging, and positioning; test holistically
- **No guardrails**, A pricing experiment that increases conversion but tanks NPS is a net loss
- **Excluding revenue metrics**, Conversion up + ARPU down = possibly net negative revenue
- **Forgetting existing customers**, Price experiments on new users are clean; changing prices for existing users requires careful communication
- **Too short**, Pricing decisions need at least one full billing cycle to evaluate properly

## Weak vs. Strong Output

**Weak:**
> "We believe changing the pricing will improve conversion."

No specificity on what changes, what conversion baseline is, or why the change should work. Unfalsifiable.

**Strong:**
> "We believe that reducing the free-to-paid jump from $49 to $29/mo (with a new $49 Pro tier) will increase free-to-paid conversion from 3.2% to 4.5%, because 62% of churned free users cited 'too expensive' in exit surveys and median WTP in our segment is $25-35/mo."

Testable, grounded in data, with a specific mechanism and measurable target.
