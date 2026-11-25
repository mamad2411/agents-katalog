---
name: data-cleaning
description: Use when profiling, cleaning, transforming, standardizing, deduplicating, or validating data with Excel, Google Sheets, Oracle SQL, Python/Pandas, Informatica IDMC, or similar tools. Context-aware rules for missing values, format standardization, sentinel values, and edge cases with before-and-after summaries.
---

# Data Cleaning

Data cleaning identifies, corrects, and manages inaccurate, incomplete, duplicated, or inconsistent data so it is reliable, consistent, and suitable for analysis and reporting. Preserve data integrity, prevent silent data loss, and avoid unnecessary information loss.

## Core tasks

- **Missing values:** Profile nulls and blanks by column and row with counts and percentages; apply context-based remediation (evaluating 5%, 10%, and 50% missingness scenarios) rather than fixed automatic thresholds.
- **Sentinel values & placeholders:** Detect and normalize sentinel values (`N/A`, `NA`, `-`, `unknown`, `null`, `None`, `?`, `999`, `-1`) before profiling and transformations.
- **Inconsistent & invalid formats:** Detect and standardize date representations, numeric strings, currency, whitespace, casing, category labels, and mixed data types.
- **Edge cases without silent data loss:** Handle all-null columns, malformed dates, and failed type conversions using explicit quarantine/error flagging rather than silent drops.
- **Duplicates:** Detect exact duplicate rows vs duplicate business keys or entities; distinguish genuine repeats from records that need consolidation.
- **Data types:** Coerce types accurately while preserving leading zeros (e.g., postal codes, account IDs).
- **Outliers:** Detect anomalous values; distinguish valid extreme observations from data-entry errors before altering or excluding them.
- **Validation & Reconciliation:** Verify row grain, key uniqueness, allowed values, referential integrity, and reconcile totals against untouched raw data.
- **Documentation:** Maintain an audit trail of cleaning steps, exclusions, assumptions, and reversible changes.

## Profiling and handling missing values

### 1. Missingness profiling
- Always calculate and report missing-value counts and percentages for every column:
  $$\text{Missing \%} = \frac{\text{Null count}}{\text{Total rows}} \times 100\%$$
- Profile row-level missingness patterns (e.g., records missing multiple mandatory business fields).
- Identify missingness mechanisms where possible:
  - **Missing Completely at Random (MCAR):** Missingness is independent of both observed and unobserved data.
  - **Missing at Random (MAR):** Missingness is related to other observed fields (e.g., missing income is correlated with age or employment status).
  - **Missing Not at Random (MNAR):** Missingness is directly related to the unobserved value itself (e.g., high earners withholding income).

### 2. Context-aware evaluation by missingness tier
Do not apply fixed thresholds as unconditional drop or impute rules. Evaluate the business context and analytical objectives:

- **~5% Missingness (Low):**
  - Verify whether missingness is random (MCAR) or concentrated in a specific segment.
  - **Options:** Retain as null if downstream models/tools support nulls; impute using central tendency (median for skewed numeric data, mean for symmetric numeric data, mode for categorical data) or forward/backward fill for ordered time series.
  - Listwise row exclusion may be considered only if the data is confirmed MCAR, sample size is sufficient, and removal will not introduce bias into downstream cohorts.
- **~10% Missingness (Moderate):**
  - Investigate relationships with other columns (MAR).
  - Avoid unconditional row deletion, which risks significant selection bias, reduced sample representation, and loss of statistical power.
  - **Options:** Domain-guided business-rule imputation; add a companion binary missingness indicator column (`<col>_is_missing`) alongside imputed values; or assign a distinct categorical bucket (e.g., `"Unknown"` or `"Unspecified"`).
- **~50% Missingness (High):**
  - **Never apply an unconditional column drop rule.** High missingness does not automatically make a column useless.
  - Assess business context: determine whether the column is **sparse by design** (e.g., secondary phone number, referral/discount code, apartment/suite number, cancellation reason, optional customer feedback).
  - If sparse by design, dropping the column destroys meaningful business information. Instead, retain the field, create a binary indicator flag (e.g., `has_referral_code`), bucket missing records into an explicit category (e.g., `"No Promo Used"`, `"Active / Not Cancelled"`), or analyze the population as a separate sub-cohort.
  - Only propose dropping a column if it has confirmed low analytical value, is not required for any business rule or downstream reporting, and domain stakeholders explicitly confirm removal.

### 3. Rules on imputation methods

| Method | Potential use | Cautions & considerations |
| --- | --- | --- |
| **Retain nulls** | Natural sparsity, non-mandatory attributes, or when downstream algorithms natively handle missingness. | Ensure reporting tools do not miscalculate denominators or omit categories. |
| **Flag as indicator** | Moderate or non-random missingness (MAR/MNAR). Create `<col>_is_missing` (1/0). | Preserves information about the missingness mechanism for analysis and modeling. |
| **Category bucket** | Categorical attributes with missing entries. Map to `"Unknown"`, `"Unspecified"`, or `"Not Applicable"`. | Avoid conflating "unknown" with "not applicable" when they have different business meanings. |
| **Median imputation** | Skewed numerical data or distributions with outliers. | Preserves median but artificially reduces distribution variance; flag imputed rows. |
| **Mean imputation** | Symmetrically distributed continuous data without heavy tails or outliers. | Distorts variance and correlations; avoid when data is skewed. |
| **Mode imputation** | Categorical data with a clear dominant category. | Can artificially inflate the frequency of the modal class; use cautiously. |
| **Forward/backward fill** | Ordered time-series data with short missing intervals. | Validate that observations do not cross entity boundaries or long time gaps. |
| **Business-rule imputation** | Domain logic explicitly defines default states (e.g., no end date = `"Active"`). | Must be documented with the business rule and approved by stakeholders. |
| **Remove rows** | Negligible missingness, confirmed MCAR, low analytical value. | Validate that row loss does not bias required segment coverage. |
| **Remove columns** | Extreme missingness with confirmed zero business or analytical utility. | Requires explicit confirmation; never drop columns automatically. |

> **Strict rule on zero substitution:**
> Never replace missing values with zero by default. Zero is a specific quantitative measurement (e.g., \$0 revenue, 0 visits, 0°C temperature) and is not equivalent to unknown, uncollected, or not applicable. Replacing nulls with zero corrupts sums, averages, ratios, and distributions. If a business rule explicitly justifies zero substitution (e.g., null discount amount means \$0 discount), document the exact business rule.

## Format detection and standardization

Detect and standardize invalid, inconsistent, and mixed formats across all fields:

- **Dates:**
  - **Ambiguous date formats:** For dates formatted as `DD/MM/YYYY` vs `MM/DD/YYYY`, inspect day components greater than 12 across the dataset to determine the source locale before parsing.
  - **Standardization:** Standardize all valid dates to ISO 8601 format (`YYYY-MM-DD` or `YYYY-MM-DD HH:MM:SS`).
  - **Malformed dates:** For invalid calendar dates (e.g., `2023-02-30`, `0000-00-00`), do not silently convert them to null or drop rows. Log the record, preserve the raw value, and place it in a quarantine/remediation list.
- **Numeric strings & currency:**
  - Strip formatting artifacts: currency symbols (`$`, `€`, `£`, `¥`), thousand separators (`,`), percent signs (`%`), and leading/trailing whitespace.
  - Handle accounting negatives: convert parenthesized numbers such as `(1,250.00)` to `-1250.00`.
  - Preserve leading zeros for postal codes, phone numbers, identification numbers, and account codes by retaining them as string/text types.
- **Text, whitespace, and casing:**
  - Trim leading and trailing whitespace; collapse consecutive internal spaces; strip non-printable or control characters.
  - Standardize casing (`UPPERCASE`, `lowercase`, or `Title Case`) according to data dictionary standards.
  - Standardize abbreviation variations (e.g., `"CA"`, `"Calif."`, `"California"`) only when mapping tables or business rules are definitive.
- **Category labels and mixed data types:**
  - Harmonize boolean representations (`Y`/`N`, `Yes`/`No`, `True`/`False`, `1`/`0`) into a single uniform representation.
  - In columns with mixed types (e.g., numeric values mixed with text notes like `"approx 50"` or `"N/A"`), extract the clean numeric component into a numeric field and preserve qualifying notes in a separate attribute.

## Sentinel values and edge cases (Preventing silent data loss)

- **Sentinel values:**
  - Actively detect placeholder strings and sentinel codes across datasets:
    - **Text sentinels:** `"N/A"`, `"NA"`, `"-"`, `"--"`, `"None"`, `"NULL"`, `"null"`, `"unknown"`, `"Unknown"`, `"?"`, `"#N/A"`, `""` (blank/empty strings).
    - **Numeric sentinels:** `-1`, `999`, `9999`, `-999`, `0` (when used as a placeholder rather than a valid measured quantity).
    - **Date sentinels:** `"1900-01-01"`, `"9999-12-31"`, `"0000-00-00"`.
  - Normalize recognized sentinels into true `NULL` values prior to computing statistics, distributions, or applying imputation.
  - Document all detected sentinel values and their mapped conversions in the change log.
- **All-null columns:**
  - Distinguish between attributes that are unpopulated due to upstream pipeline extraction bugs vs attributes that are expected empty placeholders for future collection.
  - Do not silently delete all-null columns. Report them explicitly, state the potential pipeline impact, and request stakeholder confirmation before dropping.
- **Failed type conversions:**
  - When parsing dates, integers, or floats, avoid silent coercion that turns invalid entries into nulls without tracking (e.g., untracked `errors='coerce'`).
  - Quarantine records that fail conversion into an audit table or log with the row ID, column name, raw value, and error description.

## Step-by-step cleaning workflow

1. **Clarify requirements:** Confirm the analytical goal, row grain, columns and expected types, business keys, business rules, and target tool/environment.
2. **Profile raw data:**
   - Report row and column counts.
   - Report missing-value counts and percentages for each column.
   - Detect sentinel values, format inconsistencies, duplicate rows/keys, and extreme outliers.
3. **Formulate a context-aware cleaning plan:**
   - Categorize safe normalizations (whitespace trimming, casing, sentinel conversion) vs context-dependent decisions (5%/10%/50% handling, imputation, record removal).
   - Document trade-offs, state assumptions, and ask for stakeholder clarification when business rules are not established.
4. **Preserve raw data & maintain auditability:**
   - Keep the raw dataset untouched on a separate copy, staging table, or raw layer.
   - Document every modification, transformation rule, and exclusion in a reproducible changelog or script.
5. **Execute transformations reproducibly:**
   - Provide reviewable, executable transformation code (SQL, Python/Pandas, or spreadsheet formulas) rather than manual one-off edits.
6. **Validate with before-and-after checks:**
   - Reconcile post-cleaning metrics against the raw dataset: row count differences, key uniqueness, missingness rates, allowed value compliance, and financial/metric reconciliation sums.
7. **Produce Before-and-After Data Quality Summary:**
   - Present a structured before-and-after summary table.
   - Disclose all unresolved issues, quarantined records, assumptions, and remaining limitations.

## Before-and-After Data Quality Summary

Always provide a concise, structured Before-and-After Data Quality Summary table documenting the impact of cleaning:

| Metric / Dimension | Before Cleaning | After Cleaning | Change / Remediated | Notes & Method |
| :--- | :--- | :--- | :--- | :--- |
| **Total Row Count** | 10,000 | 9,950 | -50 rows (-0.5%) | 50 exact duplicate records removed |
| **Primary Key Uniqueness** | 9,950 unique (50 duplicates) | 9,950 unique (100%) | 0 duplicate keys | Verified unique at `customer_id` grain |
| **Column A (5% missing)** | 500 missing (5.0%) | 0 missing (0.0%) | 500 imputed | Imputed via median (MCAR confirmed, numeric) |
| **Column B (10% missing)** | 1,000 missing (10.0%) | 1,000 missing (10.0%) | Flagged & retained | Retained nulls; added `col_b_is_missing` indicator |
| **Column C (50% missing)** | 5,000 missing (50.0%) | 5,000 categorized (50.0%) | Bucketed as `"Unspecified"` | Retained; sparse by design (optional promo code) |
| **Sentinel Values** | 350 placeholder strings (`"N/A"`, `"-"`) | 0 sentinels | Converted to NULL | Mapped to true `NULL` before profiling |
| **Invalid Date Formats** | 120 strings (`DD/MM/YYYY`, malformed) | 0 invalid strings | 115 standardized, 5 quarantined | ISO 8601 standardized; 5 malformed quarantined |
| **Numeric String Formatting** | 450 formatted (`$`, `,`) | 0 formatted strings | 450 cast to numeric | Stripped currency symbols and commas |

## Common tools

- **Excel and Google Sheets:**
  - Use `TRIM`, `CLEAN`, `UPPER`/`PROPER`, `IFERROR`, `ISBLANK`, `COUNTBLANK`, and `XLOOKUP`.
  - Always work on a duplicated worksheet or table; preserve raw formulas and document filter/deduplication steps.
- **Oracle SQL:**
  - Use `TRIM()`, `UPPER()`, `COALESCE()`, `NVL()`, `CASE`, `TO_DATE()`, `TO_NUMBER()`, and `REGEXP_REPLACE()`.
  - Write validation queries with `COUNT(*)`, `COUNT(column)`, and `ROUND(AVG(CASE WHEN column IS NULL THEN 1.0 ELSE 0.0 END) * 100, 2) AS pct_missing`.
  - Do not claim to run queries or alter database tables unless a live execution tool is available.
- **Python / Pandas:**
  - Use `df.isna().sum()`, `(df.isna().mean() * 100).round(2)`, `df.replace(['N/A', '-', 'NA', '?'], np.nan)`, `pd.to_datetime()`, `pd.to_numeric()`.
  - When converting types, avoid untracked coercion: capture quarantined records using `errors='coerce'` with an audit filter before updating.
  - Preserve original DataFrames using `.copy()`.
- **Informatica IDMC:**
  - Implement Cleanse and Parser transformations, standardization dictionaries, and rule specifications.
  - Configure exception and quarantine tables for failed conversions and referential integrity errors.

## Correctness and privacy

- Use only supplied data, column names, and schema; never invent columns, relationships, values, or counts.
- Distinguish observed facts from assumptions and recommendations.
- Avoid repeating personal or confidential values; suggest masking sensitive fields before sharing.
- Do not solicit or process payment-card data subject to PCI DSS, protected health information, government identifiers, or authentication credentials and secrets. If supplied data contains these fields, ask the user to remove or mask them before analysis. Process other sensitive or special-category personal data only when strictly necessary for the task, legally adequate consent is confirmed, and the user was explicitly informed before providing it; otherwise ask for removal or masking.
- Do not claim to execute transformations or modify source data unless an execution tool is actually available.
