---
name: product-conjoint-analysis
description: Run a product-analysis focused revealed-preference logistic conjoint workflow (product specs + reviews/transactions, stacked binary choice, logistic estimation) — from attribute design through business insights (importance, willingness-to-pay, optimal product configuration, pricing and cost-benefit). Use this skill when the goal is to analyze products and infer multi-attribute preferences from observed market behavior, not a generic survey-only conjoint setup.
---

# Product Conjoint Analysis

A reusable end-to-end workflow for conjoint analysis, distilled from a working case study (safety glasses on Amazon, N=160). It covers data acquisition, attribute engineering, experimental design, logistic regression estimation, and the four canonical insight transforms (importance, WTP, choice probability, cost-benefit ROI).

The skill is opinionated about **decisions that beginners commonly get wrong** — choice of reference levels, when to split models for collinearity, why price needs special handling for importance, when WTP is meaningful, etc. Read this file fully on first use, then consult the `references/` folder when you hit a specific decision point.

---

## When to use this skill

Trigger on any of these intents:

- "I want to know which product attributes matter most to customers"
- "How much would customers pay for [feature X]?"
- "Help me design a conjoint study / choice experiment"
- "Analyze this product/review data to figure out optimal configuration"
- "I have purchase records — can you reverse-engineer preferences?"
- Any mention of: conjoint, part-worth utility, trade-off analysis, discrete choice, attribute importance, willingness-to-pay (WTP), 聯合分析, 屬性重要性, 願付價格

Do **not** use this skill for: simple A/B testing, pure descriptive statistics, recommendation systems based on collaborative filtering, or single-attribute pricing studies.

---

## The 5-phase architecture

Every conjoint study — regardless of domain — follows this structure. Always show the user this map at the start so expectations are clear.

```
I. Data Acquisition  →  II. Attribute Engineering  →  III. Experimental Design
                                                                ↓
   V. Insight Translation  ←  IV. Model Estimation  ←──────────┘
```

| Phase | Purpose                                    | Key output                           |
| ----- | ------------------------------------------ | ------------------------------------ |
| I     | Get supply-side specs + demand-side signal | Attribute candidate pool             |
| II    | Filter, define levels, encode              | Coded design matrix                  |
| III   | Build product cards + response variable    | Stacked observation table            |
| IV    | Estimate part-worth utilities              | Coefficient table                    |
| V     | Translate utilities to decisions           | Importance / WTP / Probability / ROI |

For each phase below, the SKILL.md gives the workflow and the **"why"**. When you need formulas, code, or edge-case handling, jump to the referenced file.

---

## Phase I — Data acquisition

### Decide the data source first

Conjoint can run on three kinds of data, each with different downstream consequences. Confirm which one you have **before** designing anything else:

1. **Survey data with rating scores** — classic conjoint. Respondent rates each card 1–7. Use OLS regression in Phase IV.
2. **Survey data with stated choice** — choice-based conjoint (CBC). Respondent picks one card from each set. Use logistic / multinomial logit.
3. **Observed market data (transactions, reviews, clicks)** — revealed preference. Use logistic regression with stacked data structure. **This is what the case study uses.**

The skill defaults to **revealed-preference logistic conjoint** because it's the most common real-world scenario when full surveys aren't available. If the user has rating data instead, switch to OLS — see `references/model_estimation.md` § "Rating-based variant".

### Two-track collection (when using market data)

If the user is scraping from an e-commerce platform or similar, always collect from both tracks. Don't let them rely on one.

| Track       | Source                                         | Purpose                                    |
| ----------- | ---------------------------------------------- | ------------------------------------------ |
| Supply-side | Product pages, spec sheets, catalogs           | What attributes exist; what levels appear  |
| Demand-side | Reviews, ratings, forum posts, support tickets | What attributes consumers actually mention |

The supply track tells you what's _encodable_; the demand track tells you what's _salient_. An attribute must score on **both** to enter the model. This is triangulation — it materially improves attribute validity over either source alone.

For text mining of reviews, see `references/review_mining.md` for the topic extraction recipe (the case study used a Maslow-needs framework, but topic modeling, BERTopic, or LLM-based theme extraction all work).

---

## Phase II — Attribute engineering

This phase makes or breaks the study. Three sub-steps, in order.

### Step 1: Universality filter (supply side)

For each candidate attribute, compute the share of products in the sample that explicitly list it. **Drop attributes with universality > 95% or < 5%** — they have no variation across cards and the model cannot estimate their effect (the coefficient gets absorbed by the intercept).

Concrete example from the case study: anti-fog feature appeared on ~100% of products. Even though customers mentioned it heavily in reviews, it was dropped because it had no level variation. **High salience does not save an attribute that has no variance.**

### Step 2: Triangulate against demand signal

Cross-check the attributes that survived Step 1 against the high-frequency themes from review mining. Keep attributes that show up on **both** sides. This typically yields 4–8 final attributes.

### Step 3: Define levels and encode

For each surviving attribute, define its levels:

- **Categorical (e.g., brand, color)** — list the actual market levels (typically 2–4 per attribute).
- **Continuous (e.g., price, size in mm)** — either keep as continuous, or bin into 3 levels covering low/mid/high market range.
- **Binary (e.g., feature on/off)** — just 0/1.

Then encode using **dummy coding**, not one-hot:

| Attribute type            | Encoding                     | Why                                                                  |
| ------------------------- | ---------------------------- | -------------------------------------------------------------------- |
| Categorical with k levels | (k−1) dummies, one reference | Avoids the dummy variable trap (perfect collinearity with intercept) |
| Binary                    | Single 0/1 column            | Simplest case                                                        |
| Continuous                | Keep raw value               | Coefficient = marginal effect per unit                               |

**Choose the reference level deliberately.** Pick the most "baseline" or "default" version (e.g., black for color, the smallest size, the lowest-tier brand). All other coefficients will be interpreted _relative to this reference_, so a sensible reference makes the output readable.

Full encoding rules and edge cases: `references/encoding.md`.

---

## Phase III — Experimental design

### Two design philosophies

| Approach              | When to use                                                              | Trade-off                                                               |
| --------------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| **Orthogonal design** | You can run a real survey and want maximum statistical efficiency        | Generates synthetic combinations that may not exist in the market       |
| **Realistic cards**   | You're using observed market data; combinations must match real products | Attributes will be partially correlated → must split models in Phase IV |

The case study used realistic cards because reviews can only be tied to actual SKUs. If you go this route, **you commit yourself to split-model estimation in Phase IV** — flag this clearly to the user.

For orthogonal design generation, see `references/orthogonal_design.md`.

### Define the response variable

| Data type                     | Response variable             | Model          |
| ----------------------------- | ----------------------------- | -------------- |
| Rating survey                 | Score 1–7                     | OLS            |
| Stated choice                 | Chosen card = 1, others = 0   | Logistic / MNL |
| Reviews as proxy for purchase | Reviewed card = 1, others = 0 | Logistic       |
| Clickstream                   | Clicked = 1, not = 0          | Logistic       |

**The reviews-as-purchase proxy** is a useful shortcut but carries two biases — declare them up front:

- _Self-selection_: review writers are not representative buyers (extreme satisfaction tends to be over-represented).
- _Consideration set assumption_: you must assume each customer compared all cards, even though you only observe their final choice.

### Stack the data

For revealed-preference logistic conjoint, expand each customer's single observation into one row per card in the consideration set:

```
N customers × M cards = N×M stacked observations
```

The chosen card gets `y=1`; the others `y=0`. Each row carries the full attribute encoding of _that card_, not the customer's choice. The case study: 20 customers × 8 cards = 160 rows.

Stacking template and code: `scripts/build_stacked_data.py`.

---

## Phase IV — Model estimation

### Decide: single model or split models?

This is the most common decision point. Default rule:

```
IF (cards generated by orthogonal design) AND (N > 10 × num_predictors):
    → single full model
ELSE IF (realistic cards) OR (small N):
    → split into sub-models per attribute group
```

**Why splitting works.** When attributes are correlated (e.g., MORKSUKY brand always ships with 145mm frames in the case study), throwing them all into one logistic regression produces unstable coefficients, inflated standard errors, and sometimes sign reversals. Splitting estimates each attribute's effect _averaged over the joint distribution of the others_, which is less precise but more stable.

**The cost of splitting.** You lose the ability to detect interaction effects. Note this limitation in the report.

The case study used 5 sub-models: brand / color / size / features (anti-scratch + UV) / price. Use the price sub-model's coefficient as the "price sensitivity" reference for WTP calculations later.

### Fit the model(s)

For binary outcomes (choice, purchase, click): logistic regression via MLE.

```python
import statsmodels.api as sm

X = df[['UKNOW', 'MORKSUKY']]      # one sub-model at a time
X = sm.add_constant(X)
y = df['purchased']
model = sm.Logit(y, X).fit()
```

The β coefficients become **part-worth utilities** for each attribute level. Reference levels have utility = 0 by construction.

Full fitting code with diagnostics, p-value handling, and robustness checks: `scripts/fit_logistic_conjoint.py`.

### Statistical significance — set expectations

With small samples (case study had N=160 stacked = 20 unique customers), p-values often fail to reach 0.05 even when effect sizes are large. **State this up front.** Conjoint with revealed-preference data is usually directional, not inferential. If the user needs proper hypothesis testing, they need a larger sample or a designed survey.

---

## Phase V — Insight translation

Coefficients are abstract. This phase converts them into four decision-grade outputs. Always produce all four — they answer different questions.

### 1. Attribute importance

Measures relative influence of each attribute on the choice.

```
For each attribute:
    range_i = max(part-worth) - min(part-worth)
    # For PRICE specifically: range = |β_price| × (max_price - min_price)
importance_i = range_i / sum(all ranges) × 100%
```

**Why price is special.** Categorical coefficients are already on a "relative-to-reference" scale; price is a marginal-per-dollar coefficient. Without multiplying by the actual price range, you'll dramatically under-state price importance. Always do this rescaling.

### 2. Willingness to pay (WTP)

Translates abstract utility back into dollars:

```
WTP(level) = part-worth(level) / |β_price|
```

A WTP of $8.90 means "the consumer would pay up to $8.90 extra for this level versus the reference."

**When WTP is unreliable** — flag any of these:

- Price coefficient is positive (violates economic theory; usually means the price range is too narrow).
- Price coefficient has very high p-value (>0.5).
- Some attribute's WTP exceeds the max market price.

In any of these cases, report WTP as "directional only" with a caveat. The case study had β_price = +0.052, which made WTP estimates technically computable but economically unstable.

### 3. Choice probability via logistic transform

For each candidate product configuration, compute total utility and convert to a 0–1 probability:

```
U = β₀ + Σ β_i × X_i
P = exp(U) / (1 + exp(U))
```

The card with the highest P is the **predicted optimal product** under current market preferences. Rank all cards by P and present a top-3.

For multi-product scenarios (share-of-preference rather than single-card P), use the multinomial form — see `references/insight_translation.md`.

### 4. Cost-benefit (ROI) per attribute level

For product development resource allocation, combine demand-side utility with supply-side cost:

```
ROI(upgrade) = part-worth gain / unit cost increase
```

An ROI of 1.54 means each $1 of additional cost produces 1.54 utility units. Rank upgrades by ROI to prioritize R&D investment.

The cost figures are usually estimates from the user — ask them. If they don't have data, use a Δcost = 1 placeholder and let the user fill in real numbers later.

Full insight calculation code: `scripts/compute_insights.py`.

---

## Output: the standard report structure

When you produce the final deliverable for the user, follow this structure. The case study's report is included as `examples/case_study_safety_glasses.md` — read it before writing your first conjoint report.

```
1. Research scope & data sources
   - Category, sample size, time window
   - Supply track + demand track summary
2. Attribute design
   - Final attributes table (attribute / levels / reference)
   - Encoding scheme
   - Justification for what was excluded and why
3. Experimental design
   - Card list (all combinations tested)
   - Response variable definition
   - Stacked data structure (N × M)
4. Model results
   - Coefficient table with p-values
   - Note on splitting strategy
5. Insights
   - Attribute importance ranking
   - WTP table (with caveats if unreliable)
   - Choice probability ranking → optimal product
   - Cost-benefit ROI
6. Strategic recommendations
   - Product configuration
   - Pricing
   - R&D priorities
7. Limitations & future research
```

Default output format is **a Word document** for academic/business reports, or **a one-page HTML flow + markdown report pair** for executive summaries. Always offer both.

---

## Common pitfalls

These come up almost every time. Watch for them:

1. **User skips the universality filter** and includes a feature that's on every product. Coefficient ends up unidentifiable. → Always run the filter.
2. **User picks the wrong reference level** (e.g., the most premium brand as reference). All other brands then have negative coefficients, which reads strangely. → Pick the baseline / lowest-tier as reference.
3. **User reports raw price coefficient as "importance"** without rescaling by price range. → Underestimates price by 5–10×.
4. **User tries to interpret WTP when β_price is positive.** → Flag as unreliable; recommend wider price range.
5. **User runs one big regression on correlated realistic cards** and gets sign flips. → Switch to split models.
6. **User claims statistical significance with N<200 stacked observations.** → Report as directional, not inferential.

---

## Workflow at a glance

When a user brings a conjoint task, work through this checklist out loud:

1. ☐ What kind of data? (rating / choice / observed) → determines model type
2. ☐ How was the data collected? → drives Phase I two-track check
3. ☐ Pull out attribute candidates, run universality filter
4. ☐ Triangulate against demand signal, finalize attributes
5. ☐ Choose reference levels deliberately, encode with dummies
6. ☐ Decide: orthogonal design or realistic cards?
7. ☐ Build stacked data structure, define response variable
8. ☐ Decide: single model or split models? (default: split when realistic cards)
9. ☐ Fit logistic regression(s), pull part-worth utilities
10. ☐ Compute the 4 insights: importance, WTP, choice probability, ROI
11. ☐ Write structured report with limitations section

If at any step you're unsure, the relevant `references/*.md` file has the deeper reasoning. The `scripts/` folder has working Python code for the heavy lifting.

---

## Files in this skill

- `SKILL.md` (this file) — main workflow + decision logic
- `references/encoding.md` — dummy coding rules, edge cases, multi-level handling
- `references/model_estimation.md` — single vs split models, OLS variant for ratings, diagnostics
- `references/insight_translation.md` — formulas for importance / WTP / probability / ROI with full derivations
- `references/review_mining.md` — text mining recipe for the demand-side track
- `references/orthogonal_design.md` — generating fractional factorial designs when survey is possible
- `scripts/build_stacked_data.py` — turn raw purchase records into N×M stacked format
- `scripts/fit_logistic_conjoint.py` — split-model logistic regression with diagnostics
- `scripts/compute_insights.py` — the 4 standard insight transforms
- `assets/report_template.md` — markdown skeleton for the final report
- `assets/attribute_design_worksheet.md` — fillable worksheet for Phase II
- `examples/case_study_safety_glasses.md` — the original case study, fully worked
