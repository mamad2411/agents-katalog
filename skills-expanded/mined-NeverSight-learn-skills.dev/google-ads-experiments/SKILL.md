---
name: google-ads-experiments
description: "When the user wants to set up or analyze a Google Ads experiment, A/B test, ad variation test, campaign draft, split test, or bid strategy experiment. Also triggers on 'Google Ads experiments', 'campaign experiment', 'ad variation test', 'split test', 'test bid strategy', 'A/B test ads', 'test landing page', 'statistical significance', 'experiment setup', 'control vs treatment', 'uplift test', or 'test new campaign structure'. For ongoing keyword and ad copy optimization see google-ads-search. For bid strategy choices see google-ads-bidding."
metadata:
  version: 1.0.0
---

# Google Ads — Experiments & A/B Testing

You are a Google Ads testing specialist. Your goal is to design experiments that produce reliable, actionable answers — not just results that feel like they're working. Every test should have a clear hypothesis, the right sample size, and a decision framework before a single dollar is spent.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it before asking questions.

Gather this context:

### 1. What are you testing?
- Ad copy variation (headline, description)?
- Landing page (URL swap)?
- Bid strategy (manual → Smart Bidding, or tCPA vs tROAS)?
- Audience or targeting change?
- Campaign structure (SKAG vs themed ad groups)?
- Budget or match type?

### 2. Baseline metrics
- Current conversion rate or CVR?
- Current CTR?
- Current CPA or ROAS?
- Monthly conversion volume? (determines how long the test needs to run)

### 3. Success criteria
- What improvement are you looking for? (minimum detectable effect)
- Primary metric: CVR, CPA, ROAS, CTR?
- Any guardrail metrics that shouldn't get worse? (e.g., CTR can drop if CVR improves)

---

## The Testing Mindset

Most Google Ads "tests" fail for one of three reasons:
1. Called too early (no statistical significance — just noise)
2. Testing the wrong thing (too small a change to produce a measurable difference)
3. No hypothesis — no way to learn even if the result is clear

**A good test answers a specific question about why performance changes, not just whether it changes.**

Bad hypothesis: "Let's try a new headline."
Good hypothesis: "Adding a specific outcome to Headline 1 ('Close Deals Faster') will increase CTR compared to our current feature-led headline ('CRM with Pipeline Tracking') because benefit-led copy outperforms feature-led copy for our ICP."

---

## Google Ads Experiment Types

### 1. Campaign Experiments (most powerful)
A 50/50 traffic split between a control campaign and an experimental variant. Google uses a cookie-based split to ensure the same user doesn't see both — critical for unbiased results.

**What you can test:**
- Bid strategy changes (Manual CPC → Smart Bidding is the classic use case)
- Match type changes
- Ad copy (via adding/pausing RSA assets in the experiment arm)
- Landing page URLs
- Audience targeting changes
- Campaign structure changes (one campaign vs multiple)

**How to create:**
Drafts & Experiments → Experiments → + New Experiment → Choose campaign → Set split % → Apply changes → Launch

**Key settings:**
- **Traffic split:** 50/50 is standard. Use 80/20 only if the test is risky and you want minimal exposure to the variant.
- **Sync budget:** Experiment arm uses a proportional share of the campaign's budget automatically.
- **Experiment duration:** Set based on sample size calculation (see below), not gut feel.

---

### 2. Ad Variation Tests
Tests specific RSA headline or description changes across all ads in a campaign or account simultaneously. Easier to set up than campaign experiments but less precise.

**How to create:**
Ads & Assets → Ad Variations → + New Variation → Choose rule (find text / update text / swap headlines) → Apply to campaign(s)

**Best for:**
- Testing a specific copy change across many ads at once
- High-traffic accounts where campaign experiments would take too long to reach significance
- Copy swaps that don't require landing page or structural changes

**Limitation:** Ad Variations can't test landing pages, bid strategies, or structural changes — use Campaign Experiments for those.

---

### 3. Custom Experiments (formerly Drafts & Experiments)
More flexible structure — allows you to test almost any campaign-level or ad group-level change.

Available experiment types in the UI:
- **Search Custom Experiment:** Full campaign-level split test
- **Performance Max Experiment:** Test PMax vs existing Search campaigns, or test two PMax variants
- **Video Experiment:** Test video creatives with statistical significance tracking

---

## Sample Size and Duration Calculation

This is the step most people skip — and it's why most tests produce misleading results.

### Step 1 — Define minimum detectable effect (MDE)
What's the smallest improvement worth acting on?

| Test type | Typical MDE |
|-----------|------------|
| Ad copy CTR test | 10-15% relative improvement |
| Landing page CVR test | 15-20% relative improvement |
| Bid strategy test | 20% relative improvement in CPA/ROAS |

Smaller MDEs require more data. If you only care about improvements >20%, you need less data than if you want to detect a 5% improvement.

### Step 2 — Calculate required conversions

**For conversion-based tests (CVR, CPA, ROAS):**

Approximate formula:
```
Required conversions per variant = 16 / (MDE)²

Example: Detecting a 20% CVR improvement (MDE = 0.20)
Required conversions per variant = 16 / (0.20)² = 16 / 0.04 = 400 conversions per variant
Total conversions needed = 800 (400 control + 400 variant)
```

For 95% confidence, 80% statistical power — the standard threshold.

**For CTR-based tests:** You need fewer events since clicks are far more frequent than conversions. Use click volume instead, with the same formula.

### Step 3 — Estimate test duration

```
Days needed = Required conversions per variant / (Current daily conversions × 0.5)
```
(÷ 0.5 because each variant gets half the traffic)

**Example:**
- Current daily conversions: 15
- Required per variant: 400
- Days needed: 400 / (15 × 0.5) = 400 / 7.5 = 53 days

**Minimum duration regardless of sample size: 2 weeks.** Weekly seasonality patterns need time to even out — a test starting on Monday and ending the following Monday over-indexes on Mondays.

**Maximum recommended duration: 8 weeks.** Beyond 8 weeks, external factors (seasonality, competitor changes) contaminate the results.

### Quick reference table

| Daily conversions (full campaign) | Days to detect 20% improvement |
|----------------------------------|-------------------------------|
| 5 | 160 days (probably not worth running) |
| 10 | 80 days (borderline) |
| 20 | 40 days |
| 40 | 20 days |
| 80+ | ~14 days (viable) |

**Implication:** Campaign experiments are most useful for accounts with 20+ conversions per day in the tested campaign. For low-volume campaigns, use macro-level changes and evaluate over 60-90 day windows instead of a formal split test.

---

## Reading Experiment Results

Google Ads shows experiment results in the Experiments dashboard.

### Key statistics to check:

**Confidence level:** How certain is the result?
- 95%+ confidence: reliable — act on it
- 80-95% confidence: trending — consider extending the test
- <80% confidence: noise — do not call a winner

**Relative change:** The % difference between control and experiment.
- Look at both point estimate AND confidence interval
- A result of "+15% CVR (±25%)" means the range is -10% to +40% — that's inconclusive despite a positive point estimate

**Primary metric + guardrail metrics:** Check that the winning metric improved WITHOUT a meaningful decline in other important metrics.
```
Example: Experiment shows +18% CTR (significant)
Check: Did CVR stay flat or improve? → If CVR dropped 25%, you got more clicks that don't convert
```

### Interpreting Google's "Experiment score"
Google displays a colored indicator (green/yellow/red) for each metric in the experiment. Green = statistically significant improvement. Yellow = trending. Red = significant decline. These are directional — always check the confidence level number directly.

---

## What to Test and in What Order

Not all tests are equal. Prioritize by potential impact, then by ease of setup.

### High-impact tests (run first)

| Test | Why high impact |
|------|----------------|
| Bid strategy (Manual → Smart Bidding) | Largest potential CPA/ROAS improvement |
| Landing page (generic → intent-matched) | CVR improvements of 20-50%+ possible |
| Headline angle (feature-led vs benefit-led) | CTR differences of 15-30% common |
| Match type (phrase → broad with Smart Bidding) | Volume expansion if CPA holds |

### Medium-impact tests

| Test | Notes |
|------|-------|
| Ad copy description variations | Smaller CTR effect than headlines |
| Sitelink and callout copy | 5-15% CTR contribution |
| Audience exclusions vs inclusions | Depends on audience size |
| Ad schedule changes | Test expanded vs restricted hours |

### Low-impact tests (run later)
- Minor headline wording tweaks
- Callout reordering
- Structured snippet header changes

---

## Specific Test Playbooks

### Bid Strategy Test: Manual CPC → Target CPA

**When to run:** When you have 30-50 conversions/month and want to test Smart Bidding without risking the full campaign.

**Setup:**
1. Set tCPA in the experiment arm at 10-15% above your current average CPA
2. Split: 50/50
3. Duration: 4-6 weeks minimum
4. Success criteria: Experiment CPA ≤ control CPA, with ≥ equal conversion volume

**Learning period:** Smart Bidding takes 2-4 weeks to exit learning mode. The first 2 weeks of results may look worse — don't call the experiment early.

**Common mistake:** Calling the test after 10 days when Smart Bidding is still in learning mode.

---

### Ad Copy Test: RSA Headline Angle

**When to run:** When RSA asset ratings are "Learning" or "Low" for key headlines, or CTR is below benchmark.

**Setup:**
1. Create an ad variation (Ads & Assets → Ad Variations)
2. Replace the headline you're testing with the new angle
3. Run until statistical significance or 4+ weeks

**Good headline angles to test:**
- Feature-focused vs. benefit-focused
- Question headline vs. statement
- Social proof ("10,000+ Companies") vs. outcome ("Cut Costs by 30%")
- Generic CTA ("Get Started") vs. specific CTA ("Book a 15-Min Demo")

---

### Landing Page Test

**When to run:** When CTR is strong but CVR is underperforming.

**Setup:**
- Use a Campaign Experiment, swapping the final URL in the experiment arm
- Ensure the new page is technically identical except for the variable being tested
- Track the same conversion action on both pages

**Variables worth testing:**
- Hero headline (matches keyword intent vs. brand statement)
- CTA copy and button ("Get Started" vs. "See a Demo" vs. "Get My Free Trial")
- Form length (short 3-field vs. full qualification form)
- Social proof placement (above the fold vs. below)
- Video vs. static hero section

---

### PMax vs Search Experiment

**When to run:** When considering adding PMax to an account that currently runs only Search, or when evaluating whether to shift budget from Search to PMax.

**Setup:**
- Use the PMax Experiment type in Google Ads
- Define which campaigns are in scope
- Run for 4+ weeks

**What to watch:**
- Incremental conversions (the key metric — are PMax conversions truly new, or stealing from Search?)
- Brand vs. non-brand mix in PMax (check Search Themes + Insights tab)
- CPA comparison at account level, not just campaign level

---

## Post-Test Decision Framework

After a test reaches significance, apply this decision tree:

```
Experiment shows significant improvement?
├── YES → Roll out to full campaign; document the learning; queue next test
├── NO (inconclusive) → Extend by 2 weeks if close to significance; otherwise end with no change
└── NEGATIVE result → Do NOT roll out; document why the hypothesis was wrong; learn from it

```

**Documenting the learning is not optional.** A testing program without a log of results repeats the same tests over and over. Maintain a simple log:

| Date | Campaign | Hypothesis | Result | Confidence | Decision |
|------|----------|-----------|--------|-----------|----------|
| 2025-03 | Non-Brand Search | Benefit-led H1 will increase CTR | +12% CTR | 96% | Rolled out |
| 2025-04 | Non-Brand Search | Removing form on LP will improve CVR | -8% CVR | 91% | Not rolled out |

---

## Optimization Checklist

### Before launching any test
- [ ] Written hypothesis documented
- [ ] Primary metric and guardrail metrics defined
- [ ] Sample size and duration calculated (not guessed)
- [ ] Test log entry created with start date

### During the test
- [ ] Check weekly — is either variant showing a dramatic negative result? (If so, end early)
- [ ] Do NOT adjust bids, budgets, or targeting on either arm mid-test — it contaminates results
- [ ] Note any external events (holiday, competitor news) that could affect results

### After the test
- [ ] Check primary metric confidence level
- [ ] Check all guardrail metrics
- [ ] Document result in test log
- [ ] If winner: apply and queue next test
- [ ] If loser: document the learning

---

## Common Mistakes

**Calling the test too early**
Checking results daily and calling a winner when you see a positive trend at 10 days. Statistical significance requires reaching the pre-calculated sample size — not just a positive direction. p=0.15 is not a winner.

**Changing the experiment mid-run**
Adjusting the budget, swapping the landing page URL, or pausing keywords mid-test contaminates the results. If you change anything, restart the test.

**Testing too many things at once**
An experiment that changes the headline, the landing page, and the bid strategy at once cannot attribute the result to any single variable. Test one thing at a time.

**Testing meaningless variations**
Changing one word in a headline ("Great" → "Excellent") is unlikely to produce a statistically detectable difference. Test meaningful angle changes.

**Not accounting for the Smart Bidding learning period**
If the experiment arm uses a new Smart Bidding strategy, the first 2-4 weeks will look worse as the algorithm learns. Calling the test during learning period guarantees a false negative.

---

## Related Skills

- **google-ads-bidding**: Bid strategy experiments are the highest-impact tests most accounts can run
- **google-ads-search**: Ad copy and RSA structure form the basis of most ad variation tests
- **google-ads-quality-score**: Experiments can directly test QS-improvement hypotheses (better landing page, tighter ad group)
- **google-ads-pmax**: Google's PMax Experiment type lets you measure whether PMax drives incremental conversions vs. cannibalizing Search
