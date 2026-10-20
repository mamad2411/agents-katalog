<!-- owner: shared | audience: all-pms | last-updated: 2026-04 -->
<!-- purpose: Estimate experiment parameters: past experiment lookup, success metric, sample size, run time, ROTI score, confidence intervals -->

# Experiment Setup

Generate a complete experiment setup recommendation for a proposed experiment. This command cross-references past experiments, estimates the right success metric, calculates sample size and run time, scores revenue potential (ROTI), and produces a ready-to-use experiment parameters section for the project doc.

## Arguments

The user should provide one of:
- A description of the proposed experiment (what they want to test and where)
- A path to an existing project/experiment doc that needs setup parameters
- A hypothesis in "If X, then Y, because Z" format

If insufficient context is provided, ask for: the intervention point (which funnel step), the hypothesised mechanism, and the engineering estimate (days).

## Instructions

### Phase 1: Past experiment lookup

Before calculating anything, search for similar past experiments to ground the analysis in evidence.

1. **Search the Notion Experimentation Tracker** using `mcp__claude_ai_Notion__notion-search` against the data source `{your-experiment-tracker-collection-id}`. Search by:
   - **Location of test** — find experiments at the same funnel step (e.g. {your funnel steps, e.g. Sign-up page, Onboarding, Activation, Checkout})
   - **Lever** — find experiments using the same psychological/UX mechanism (e.g. Credibility, Effort, Trust, Urgency, User flow, Social Proof)
   - **Pillar/Squad** — find experiments from the same team area

2. **Fetch the top 3-5 most relevant** completed experiments using `mcp__claude_ai_Notion__notion-fetch` and read their content for detailed metrics (funnel uplift, ARR impact, learnings).

3. **Search Hex** using `mcp__claude_ai_Hex__search_projects` for experiment result dashboards with detailed analysis.

4. **Check local experiment docs** in `projects/` for full writeups with statistical analysis.

5. **Check the experiment results log** at `data/experiment-results-log.md` — the Concluded section has historical results with authoritative source, actual uplift, and decisions. This is the fastest source for calibration data.

6. **Search Optimizely for concluded experiments** at the same funnel step using `python3 your experiment platform API list --status concluded --ab-only --limit 20` (via Bash). Use `python3 your experiment platform API lookup "{name}"` to get detailed results for promising matches.

7. **Present findings** in this format:

```markdown
## Relevant past experiments

| Experiment | Location | Lever | Result | Key metric uplift | ARR impact | Relevance |
|------------|----------|-------|--------|-------------------|------------|-----------|
| [Name] | [Location] | [Lever] | Winner/Loser | +X% [metric] | £Xk | [Why relevant] |

**Calibration note:** [What past experiments suggest about the expected uplift range. E.g. "Past experiments at this funnel step have seen X-Y% uplift. Check whether the proposed target is within or above historical precedent."]
```

Use findings to calibrate the uplift estimate, identify known risks, suggest the right primary metric, and refine the hypothesis.

### Phase 2: Success metric recommendation

Recommend the primary metric based on:

**By funnel position (workspace convention):**
- Experiments targeting steps **before {mid-funnel metric}** (sign-up, onboarding, activation, checkout): use **{mid-funnel metric}** as primary metric
- Experiments targeting steps **after {mid-funnel metric}** (post-purchase, retention, expansion): use **{end-funnel metric}** as primary metric

**Why this matters:**
- {mid-funnel metric} matures in ~2 weeks; {end-funnel metric} takes ~4 weeks. Choosing the closer metric reduces run time and noise
- {mid-funnel metric} captures the full user journey without being confounded by downstream factors outside the experiment
- {end-funnel metric} is the true revenue proxy but introduces more noise from factors outside the experiment's control

**Also recommend:**
- 2-3 **secondary metrics** that diagnose the mechanism (e.g. step completion rate, time on step)
- 2-3 **guardrail metrics** that must not degrade (e.g. {your guardrail metrics, e.g. churn rate, error rate, support tickets}). Pull current baselines from WBR data or BigQuery

If past experiments at the same location used a different primary metric, flag it and explain the trade-off.

### Phase 3: Revenue potential and ROTI

#### Revenue estimation

Walk through the funnel impact step by step using baseline data from `data/funnel-context.md` and WBR reports in `data/reports/`:

1. **Identify the intervention point** — which funnel step does this experiment target?
2. **Estimate the uplift** — what's the hypothesised improvement at that step? Calibrate against past experiment findings from Phase 1. Flag if speculative
3. **Convert through downstream funnel** — apply known conversion rates at each subsequent step
4. **Calculate weekly revenue impact** — additional {end-funnel metric} × ARPU (use your latest figure from data/funnel-context.md)
5. **Annualise** — weekly impact × 52

Example:
```
+500 additional activations/week
× 70% downstream → +350 converted
× 85% → +298 retained
× £{ARPU} = £X/week
× 52 = £X/year
```
```

Always state assumptions. Flag when downstream conversion rates may not hold (e.g. if the experiment changes user quality, not just volume).

#### ROTI score

Apply the **40% revenue haircut** before calculating ROTI. This accounts for:
- 13% statistical exaggeration (winner's curse)
- 20–25% metric translation loss ({mid-funnel metric} → {end-funnel metric})
- Buffer for novelty effects and implementation differences

```
ROTI = (Annual revenue impact × 0.60 haircut × Audience %) / Engineering days
```

| Component | How to determine |
|-----------|-----------------|
| Annual revenue impact | From the revenue estimation above |
| Audience % | 100% if experiment applies to all users; lower for segment-specific |
| Engineering days | Ask the PM for the build estimate from their EM |

Present as **£X per engineering day**.

**Sensitivity table** — always include:

| Scenario | Uplift | Annual revenue | After haircut | ROTI/eng day |
|----------|--------|---------------|---------------|--------------|
| Conservative (half) | X% | £Xm | £Xm | £Xk |
| Base case | X% | £Xm | £Xm | £Xk |
| Optimistic (double) | X% | £Xm | £Xm | £Xk |

If engineering days are not yet known, present the table with a placeholder and note "awaiting EM estimate to finalise ROTI".

### Phase 4: Experiment setup parameters

#### Statistical parameters (recommended defaults)

- Confidence level: **80%** for low-risk product changes. Use **90%** for high-risk decisions (pricing changes, core flows)
- Significance level (α): **0.05**
- Statistical power: **80%**
- Traffic split: **50/50** (unless there's a reason for unequal splits, e.g. risk mitigation)
- **A/A test:** Recommend when using new testing infrastructure or a different traffic split — validates randomisation before real experiment

#### Sample size calculation

1. Get the **baseline rate** for the primary metric (from WBR data or BigQuery)
2. Get the **minimum detectable effect (MDE)** — the smallest uplift worth detecting (from the hypothesis, calibrated by past experiments)
3. Calculate required sample size per variant:
   - For proportions: `n = (Z_α/2 + Z_β)² × (p₁(1-p₁) + p₂(1-p₂)) / (p₂ - p₁)²`
   - For continuous metrics: `n = (Z_α/2 + Z_β)² × 2σ² / δ²`
   - Where Z_α/2 = 1.96 (for α=0.05), Z_β = 0.84 (for 80% power)

#### Run time estimation

1. Get **weekly traffic** at the intervention point (from WBR data or BigQuery)
2. Divide required sample size by weekly traffic per variant
3. Round up to whole weeks
4. Add minimum **1 full week** for day-of-week effects
5. Typical range: **2–4 weeks** — flag if calculation suggests longer
6. **Add metric maturity wait:** +2 weeks if primary metric is {mid-funnel metric}, +4 weeks if {end-funnel metric}. The experiment must reach its predetermined sample size, then pause and wait for metrics to mature before analysis

**Total experiment timeline** = run time + maturity wait + analysis time (~1 week)

### Phase 5: Output

Present the complete setup as a single block ready to paste into the experiment doc:

```markdown
## Experiment Setup

### Past experiments
[Table from Phase 1]
[Calibration note]

### Recommended metrics
- **Primary metric:** [metric name] (baseline: X%)
- **Secondary metrics:** [list with baselines]
- **Guardrail metrics:** [list with baselines]

### Revenue potential
[Funnel walk-through from Phase 3]
- **Annual revenue estimate:** £Xm (before haircut)
- **After 40% haircut:** £Xm
- **ROTI:** £Xk per engineering day (based on X engineering days)

[Sensitivity table]

### Experiment parameters
- **Experiment type:** [A/B test | Multi-variate | Pre-Post | etc.]
- **MDE:** [X% relative / Xpp absolute]
- **Required sample per variant:** ~X,000
- **Weekly traffic at intervention point:** ~X,000/week
- **Run time:** X weeks
- **Metric maturity wait:** X weeks
- **Total timeline:** X weeks (run) + X weeks (maturity) + 1 week (analysis) = X weeks
- **Traffic split:** 50/50
- **Confidence level:** 80% | α = 0.05 | Power = 80%
- **A/A test needed:** Yes/No [reason]

### Decision rules
- **Clear win:** [primary metric hits target, guardrails safe] → Ship
- **Clear miss:** [primary metric missed or guardrails breached] → Kill
- **Mixed:** [primary wins but guardrail concern] → Ship with mitigations (specify which)
- **Ambiguous:** [insufficient data] → Extend X weeks

### Caveats
- [Any pricing baseline distortion affecting this experiment]
- [Any forecast-to-actual-revenue risks specific to this experiment]
- [Any risks identified from past experiment lookup]
```

## Important caveats to always check

- **Low-traffic steps:** If reaching significance takes >4 weeks, suggest Pre-Post design instead
- **Large hypothesised uplifts (>30%):** Set MDE conservatively — detecting a smaller-than-expected effect is more useful than confirming a large one
- **Downstream metrics:** Primary metric should minimise lag time — {mid-funnel metric}, not {end-funnel metric}, for upper funnel
- **Pricing baseline distortion:** Check whether any external factors (pricing changes, seasonality, market shifts) are distorting the baseline conversion rate your experiment measures against
- **Forecast ≠ actual revenue:** Common reasons: audience not at 100% immediately, baseline declining from seasonality/market, experiment not fully productionised, different metric definitions between product and finance, lagging metric materialisation. The 40% haircut covers some but not all of these

## Data sources

| Source | Access | Purpose |
|--------|--------|---------|
| Notion Experimentation Tracker | `{your-experiment-tracker-collection-id}` | Past experiments: hypothesis, metrics, results, lever, location |
| Hex | `mcp__claude_ai_Hex__search_projects` | Experiment result dashboards |
| Local experiment docs | `projects/` | Full writeups with statistical analysis |
| Funnel context | `data/funnel-context.md` | Metric definitions, conversion rates, baselines |
| WBR reports | `data/reports/` | Current baseline metrics, weekly traffic volumes |
| Experiment template | `pm-playbook/templates/experiment-template.md` | Standard doc structure |
