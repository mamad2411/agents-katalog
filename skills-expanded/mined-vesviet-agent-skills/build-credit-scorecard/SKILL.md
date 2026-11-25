---
name: build-credit-scorecard
description: Use when building regulatory credit risk scorecards, performing monotonic WOE binning, evaluating IV thresholds, calibrating PDO point scales, and tracking PSI drift.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, query_db, read_database]
---

# Build Credit Scorecard

Engineer, calibrate, and validate regulatory-compliant retail credit risk scorecards using monotonic Weight of Evidence (WOE) transformations, Information Value (IV) filtering, and Points to Double Odds (PDO) scaling.

## When to Use

- Developing retail loan origination, credit card, or SME default risk scorecards
- Transforming continuous and categorical predictors into strictly monotonic WOE bins
- Filtering candidate risk drivers using regulatory IV thresholds and VIF collinearity checks
- Calibrating logistic regression model log-odds into integer score scales via PDO parameters
- Monitoring post-deployment score distribution drift using Population Stability Index (PSI)

## Core Rules

- **Strict Monotonicity Invariant**: Continuous and ordinal variables must exhibit strictly monotonic (strictly increasing or decreasing) WOE curves. If a variable demonstrates non-monotonic trends across bins, merge adjacent bins via Chi-Square ($\chi^2$) pooling or reject the feature from the candidate pool.
- **Minimum Bin Volume**: Every bin must account for at least $5\%$ of the total sample population. Bins with zero defaults or zero goods are prohibited (apply Laplace smoothing or pool bins).
- **IV Filtering Bands**: Screen predictors against regulatory Information Value criteria:
  - $\text{IV} < 0.02$: Exclude (unpredictive)
  - $0.02 \le \text{IV} < 0.10$: Weak (use only if economically vital)
  - $0.10 \le \text{IV} < 0.30$: Medium (standard core predictor)
  - $0.30 \le \text{IV} \le 0.50$: Strong (high-value predictor)
  - $\text{IV} > 0.50$: Suspicious (audit for target leakage or overfitting)
- **Multi-Collinearity Ceiling**: Reject any candidate feature having Variance Inflation Factor $\text{VIF} \ge 3.0$ or pairwise correlation $|\rho| \ge 0.60$ against another higher-IV predictor.
- **PDO Score Scaling**: Calibrate integer scores using:
  $$\text{Factor} = \frac{\text{PDO}}{\ln(2)}, \quad \text{Offset} = \text{TargetScore} - \text{Factor} \cdot \ln(\text{TargetOdds})$$
  Default baseline: Target Score = 600 at Odds = 50:1 with PDO = 20 points.
- **PSI Drift Governance**: Compute $\text{PSI} = \sum (A_j - E_j) \ln(A_j / E_j)$. Trigger moderate alert at $\text{PSI} \ge 0.10$; trigger mandatory retrain/recalibration at $\text{PSI} > 0.25$.
- **Fair Lending Prohibition**: Strictly exclude protected demographic attributes (race, gender, religion, marital status, national origin) from feature candidate pools.

## Suggested Process

### 1. Define Population and Clean Observation Window
- Define default target variable $Y$ ($Y=0$ Good, $Y=1$ Bad, e.g. 90+ days past due within 12 months).
- Partition historical data into Development ($60\%$), Out-of-Time Test ($20\%$), and Holdout Validation ($20\%$) windows.
- Isolate missing and exceptional value codes into separate category bins.

### 2. Perform Monotonic WOE Binning
- Apply initial quantile binning (5 to 10 bins per variable).
- Calculate $\text{WOE}_i = \ln((G_i / G_{\text{total}}) / (B_i / B_{\text{total}}))$ for each bin.
- Inspect slope monotonicity; run automated adjacent-bin Chi-Square pooling for non-monotonic segments.
- Verify all final bins exceed the $5\%$ sample volume floor.

### 3. Screen Features via Information Value and Collinearity
- Compute total $\text{IV} = \sum (G_i/G_{\text{total}} - B_i/B_{\text{total}}) \cdot \text{WOE}_i$ for all candidate features.
- Retain variables with $0.10 \le \text{IV} \le 0.50$; thoroughly audit variables with $\text{IV} > 0.50$ for target leakage.
- Run correlation matrix and VIF analysis to eliminate collinear redundant variables.

### 4. Fit Logistic Regression and Scale Points
- Fit multivariate logistic regression on WOE-transformed features: $\ln(\text{Odds}) = \beta_0 + \sum \beta_j \text{WOE}_j$.
- Verify all coefficients $\beta_j$ are statistically significant ($p < 0.05$) and maintain positive alignment with risk.
- Convert logistic coefficients into integer points using Factor and Offset derived from PDO calibration parameters.
- Verify that total applicant score equals the sum of assigned bin points rounded to integer.

### 5. Validate Discrimination and Population Stability
- Evaluate discrimination metrics on Out-of-Time dataset: Kolmogorov-Smirnov ($\text{KS} \ge 0.30$) and ROC $\text{AUC} \ge 0.70$.
- Generate production baseline score deciles for ongoing PSI monitoring.
- Configure Adverse Action reason code engine mapping the 4 largest point deficits per rejected application.

## Output Format

Outputs should include the scorecard specification table, validation metrics, and governance brief:

```markdown
# <Scorecard Name> - Regulatory Calibration Brief

## Scorecard Parameters
- Target Score: 600 points | Target Odds: 50:1 | PDO: 20 points
- Scaling Factor: 28.8539 | Offset: 487.1229
- Feature Count: <count> variables selected

## Discrimination Metrics (Out-of-Time Validation)
- Kolmogorov-Smirnov (KS): <e.g. 0.42> (Pass >= 0.30)
- ROC Area Under Curve (AUC): <e.g. 0.78> (Pass >= 0.70)
- Gini Index: <e.g. 0.56>

## Selected Predictor Summary
| Variable | IV Value | Bin Count | Monotonicity | VIF |
| :--- | :--- | :--- | :--- | :--- |
| <var_1> | 0.284 | 5 | Strictly Increasing | 1.18 |
| <var_2> | 0.192 | 4 | Strictly Decreasing | 1.34 |

## PSI Monitoring Baseline
- 10-decile reference distribution established
- Re-calibration threshold: PSI > 0.25
```

## Failure Modes

- **Non-monotonic WOE curves accepted**: Unpooled erratic bins create unexplainable credit decisions that fail regulatory audits. **Mitigation**: Enforce automated bin pooling or variable exclusion during step 2.
- **Target leakage features**: Features capturing post-default actions (e.g. collections outreach) inflate IV ($> 0.50$) but fail in production. **Mitigation**: Discard any feature with $\text{IV} > 0.50$ unless proven strictly pre-origination.
- **Data drift unmonitored**: Economic shifts change applicant demographics without notice. **Mitigation**: Establish automated monthly PSI calculations with alerts triggered at $\text{PSI} \ge 0.10$.
- **Protected attribute proxy leakage**: Zip code or non-protected variables acting as racial or gender proxies. **Mitigation**: Run adverse impact disparate analysis before finalizing scorecard variables.

## Output Contracts

When producing scorecard deliverables or risk validation briefs, emit:

- Comprehensive scorecard points lookup table and adverse action reason code definitions.
- If producing analytics validation reports, adhere to `contracts/schemas/validation-result.json`.

## Security Guardrails (OWASP ASI)

- **ASI02 Data Ingestion Guard**: Sanitize all SQL queries and data extraction scripts; never execute dynamic unsanitized SQL against customer credit bureaus.
- **ASI07 PII Privacy Guard**: Do not write unmasked Social Security Numbers, national identity IDs, or sensitive customer names to scorecard logs or artifacts.

## Checklist

- [ ] Binary default target $Y$ cleanly defined with unambiguous performance window.
- [ ] Data partitioned into Development, Validation, and Out-of-Time temporal holdouts.
- [ ] Strictly monotonic WOE binning verified for all continuous and ordinal predictors.
- [ ] Every bin validated to contain at least $5\%$ of total sample volume.
- [ ] IV thresholds applied ($0.10 \le \text{IV} \le 0.50$ preferred; $\text{IV} > 0.50$ audited).
- [ ] Multi-collinearity evaluated (VIF $< 3.0$ and pairwise $|\rho| < 0.60$).
- [ ] Logistic regression coefficients verified for statistical significance ($p < 0.05$).
- [ ] Score scaling correctly applied using PDO formula ($\text{Factor} = \text{PDO}/\ln(2)$).
- [ ] KS statistic ($\ge 0.30$) and ROC AUC ($\ge 0.70$) confirmed on holdout data.
- [ ] Baseline score deciles and PSI drift monitoring thresholds ($0.10 / 0.25$) documented.
- [ ] Adverse action reason code engine verified for rejected applicant disclosures.
- [ ] Zero protected demographic attributes included in final scorecard specification.

## Related Skills

- **analyze-data**: Perform exploratory data analysis, distribution profiling, and summary statistics
- **build-data-pipeline**: Construct reproducible feature extraction and scoring data pipelines
- **ai-risk-assessment**: Evaluate regulatory compliance, algorithmic fairness, and governance risks
- **write-tests**: Author automated unit and property-based tests for score calculation logic
- **systematic-debugging**: Isolate data discrepancies, missing values, and scoring calculation anomalies
