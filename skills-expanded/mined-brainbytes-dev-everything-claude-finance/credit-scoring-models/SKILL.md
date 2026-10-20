# credit-scoring-models

Credit scoring models — Altman Z-score, Merton, scorecards.

## When to Activate

- Assessing the creditworthiness of a corporate borrower or counterparty
- Building or validating a credit scorecard for lending decisions
- Estimating probability of default (PD) for a portfolio
- Evaluating a structural model approach to credit risk
- Analyzing rating migration and transition probabilities
- Calibrating internal rating systems for regulatory capital (IRB approach)
- Back-testing model performance against realized defaults

## Core Concepts

### Altman Z-Score

Edward Altman's discriminant analysis model predicts corporate bankruptcy using five financial ratios. Originally developed for publicly traded manufacturers (1968).

**Original Z-Score (public manufacturing):**
```
Z = 1.2 * X1 + 1.4 * X2 + 3.3 * X3 + 0.6 * X4 + 1.0 * X5

X1 = Working Capital / Total Assets          (liquidity)
X2 = Retained Earnings / Total Assets        (cumulative profitability)
X3 = EBIT / Total Assets                     (operating efficiency)
X4 = Market Value Equity / Book Value Debt   (solvency)
X5 = Sales / Total Assets                    (asset turnover)
```

- Z > 2.99 — Safe zone (low default probability)
- 1.81 < Z < 2.99 — Grey zone (caution)
- Z < 1.81 — Distress zone (high default probability)

**Z'-Score (private firms):** Replaces market value of equity with book value. Revised coefficients and cutoffs (Z' < 1.23 = distress).

**Z''-Score (non-manufacturing / emerging markets):** Drops X5 (Sales/Total Assets) to remove industry bias from asset turnover. Suitable for service firms and emerging market companies.

- Apply the correct variant based on the entity type
- Z-score is a point-in-time indicator — supplement with trend analysis over 3-5 years
- Does not capture industry-specific risk factors or qualitative considerations

### Merton Structural Model

Based on the Black-Scholes option pricing framework. Equity is modeled as a call option on the firm's assets with a strike price equal to the face value of debt.

- **Asset value (V)**: Unobservable — inferred from equity market value and equity volatility using iterative methods
- **Asset volatility (sigma_V)**: Also unobservable — estimated simultaneously with V
- **Default point**: Firm defaults when asset value falls below the debt obligation at maturity
- **Distance to Default (DD)**: Number of standard deviations the asset value is above the default point
  ```
  DD = (ln(V/D) + (mu - 0.5 * sigma_V^2) * T) / (sigma_V * sqrt(T))
  ```
- **PD from DD**: Map DD to PD using the normal distribution (theoretical) or empirical mapping (Moody's KMV / EDF approach uses historical default frequency for each DD bucket)

**Strengths**: Market-based, forward-looking, continuous updating. **Weaknesses**: Requires liquid equity market, assumes single debt maturity, sensitive to equity volatility estimation.

### Credit Scorecards

Statistical models (typically logistic regression) that assign points to borrower characteristics to produce a credit score.

**Development process:**
1. **Data collection**: Gather historical loan-level data with default outcomes (12-month observation window typical)
2. **Variable selection**: Financial ratios, behavioral data, industry, age of firm, management quality proxies
3. **Weight of Evidence (WoE) transformation**: Bin continuous variables; calculate WoE = ln(% of goods / % of bads) for each bin
4. **Information Value (IV)**: Measures predictive power of each variable. IV > 0.3 = strong; 0.1-0.3 = medium; < 0.1 = weak
5. **Logistic regression**: Fit model using selected WoE-transformed variables
6. **Scaling**: Convert log-odds to a score. Common convention: Score = Offset + Factor * ln(odds), where Factor = PDO / ln(2), PDO = points to double the odds
7. **Scorecard format**: Each attribute level gets a partial score; total score maps to PD

### Probability of Default (PD) Estimation

- **Through-the-cycle (TTC)**: Long-run average PD over a full economic cycle — used for regulatory capital
- **Point-in-time (PIT)**: Current PD reflecting prevailing economic conditions — used for IFRS 9 / CECL provisioning
- **PD calibration**: Ensure model-predicted PDs align with observed default rates. Central tendency adjustment to match long-run average
- **Low-default portfolios**: Where defaults are rare (e.g., investment-grade corporates, sovereigns), use external data, expert judgment, or Bayesian techniques to estimate PD

### Rating Migration Matrices

Transition matrices show the probability of moving from one rating grade to another over a defined horizon (typically one year).

```
From \ To    AAA    AA     A      BBB    BB     B     CCC/D
AAA          90.0   8.5    1.0    0.3    0.1    0.0   0.1
AA           1.0    88.0   8.5    1.5    0.5    0.3   0.2
A            0.1    2.0    87.0   7.5    2.0    0.8   0.6
BBB          0.0    0.3    4.0    84.0   7.0    3.0   1.7
BB           0.0    0.1    0.5    5.0    78.0   10.0  6.4
```

- **Upgrade/downgrade ratios**: Track the health of a portfolio over time
- **Absorbing state**: Default is absorbing — once an entity defaults, it cannot migrate back
- **Multi-year PDs**: Derived by raising the one-year transition matrix to the power of n

### Model Validation

- **Discriminatory power**: AUROC (area under ROC curve), Gini coefficient (= 2 * AUROC - 1), Kolmogorov-Smirnov statistic
- **Calibration accuracy**: Binomial test, Hosmer-Lemeshow test, traffic light approach (compare predicted PD to observed default rate by grade)
- **Stability**: Population Stability Index (PSI) measures drift in score distributions over time. PSI > 0.25 signals significant shift
- **Backtesting**: Compare predicted defaults to actual defaults; analyze by segment, time period, and rating grade

## Methodology

1. **Define scope**: Identify the portfolio segment, default definition (e.g., 90 days past due, bankruptcy), and observation period
2. **Data preparation**: Collect financial statements, market data, behavioral data. Clean and validate. Apply exclusions (e.g., newly formed entities, data errors)
3. **Model development**: Choose model type (scorecard, structural, hybrid). Develop candidate variables, test statistical significance, build the model
4. **Calibration**: Map model output to PD. Validate central tendency against long-run default rates. Adjust for economic cycle if TTC PD required
5. **Validation**: Test discriminatory power, calibration accuracy, and stability. Compare against benchmark models
6. **Implementation**: Integrate into credit approval workflow, pricing, and portfolio monitoring. Define override policy
7. **Ongoing monitoring**: Track model performance quarterly. Re-estimate or recalibrate when PSI exceeds thresholds or discriminatory power degrades

## Templates

### Altman Z-Score Calculation

```
Company: [Name]                     Year: [Year]

                                    Value       Ratio
Working Capital                     $12.5M
Total Assets                        $85.0M      X1 = 0.147
Retained Earnings                   $28.0M      X2 = 0.329
EBIT                                $10.2M      X3 = 0.120
Market Value of Equity              $45.0M
Book Value of Total Debt            $35.0M      X4 = 1.286
Sales                               $92.0M      X5 = 1.082

Z-Score = 1.2(0.147) + 1.4(0.329) + 3.3(0.120) + 0.6(1.286) + 1.0(1.082)
        = 0.176 + 0.461 + 0.396 + 0.772 + 1.082
        = 2.887

Assessment: Grey zone — monitor closely. Declining from 3.15 prior year.
Key concern: Working capital deterioration (X1 dropped from 0.210 to 0.147)
```

### Scorecard Output Summary

```
Borrower: [Name]            Application Date: [Date]

Attribute                    Value           WoE Bin      Points
Debt/EBITDA                  3.2x            2.5-4.0x     +35
Interest Coverage            4.5x            3.0-5.0x     +28
Current Ratio                1.4x            1.2-1.6x     +22
Revenue Growth (3yr)         8%              5-10%        +18
Years in Business            12              10-20        +15
Industry Risk                Medium          B            +10
Management Quality           Strong          A            +20

Total Score: 148 + Base Score (200) = 348
Mapped PD: 0.85%
Internal Rating: BB+
```

### Model Validation Dashboard

```
Metric                    Current Period   Prior Period   Threshold   Status
AUROC                     0.82             0.84           > 0.70      Pass
Gini Coefficient          0.64             0.68           > 0.40      Pass
KS Statistic              0.52             0.55           > 0.30      Pass
PSI (score distribution)  0.12             0.08           < 0.25      Pass
Hosmer-Lemeshow (p-value) 0.35             0.42           > 0.05      Pass
Predicted vs Actual DR    1.2% vs 1.4%    1.1% vs 1.0%  Within 20%  Pass
```

## Quality Gate

- [ ] Correct Z-score variant applied for the entity type (public, private, non-manufacturing, emerging market)
- [ ] Merton model inputs validated: equity value, equity volatility, debt structure, risk-free rate
- [ ] Scorecard developed on representative data with adequate default observations
- [ ] Variable selection justified statistically (IV, p-values) and economically (business logic)
- [ ] PD calibration aligned with chosen philosophy (TTC or PIT) and long-run default rates
- [ ] Model validation completed: AUROC, Gini, KS, calibration tests all within thresholds
- [ ] Population Stability Index monitored; recalibration triggered if PSI > 0.25
- [ ] Rating migration matrix computed and compared to external benchmarks
- [ ] Model documentation meets regulatory standards (IRB, IFRS 9, CECL)
- [ ] Override rate tracked and within policy limits (typically < 10-15% of decisions)
- [ ] Independent model validation function has signed off
