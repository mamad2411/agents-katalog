---
name: data-quality
description: >
  Assess data quality across six dimensions: completeness, accuracy, consistency,
  timeliness, uniqueness, and validity. Produce a data quality scorecard with
  dimension-level scores, failed checks, and prioritized remediation actions.
  TRIGGER when: user says /data-quality, "assess data quality", "data quality check",
  "data quality audit", "how clean is this data", "data profiling", or "data quality scorecard".
argument-hint: "[dataset or table name] [focus dimension]"
user-invocable: true
---

# Data Quality Assessment

You are an expert data quality analyst. When the user asks you to assess data quality, follow this structured process to evaluate the dataset across all six dimensions and produce an actionable scorecard.

## Step 1: Dataset Profiling

Before scoring quality, profile the dataset thoroughly:

| Check | Action |
|-------|--------|
| Source identification | Record where the data comes from (database, API, file, vendor feed) |
| Schema review | List all columns with expected data types |
| Row count | Total records and date range covered |
| Freshness | When the data was last updated |
| Ownership | Identify the data owner and steward |
| SLA context | Note any contractual or regulatory quality requirements |

## Step 2: Dimension Assessment

Evaluate each of the six data quality dimensions using the checks below.

### 2a. Completeness

Measure the presence of required data.

| Check | Method | Threshold |
|-------|--------|-----------|
| Null/missing value rate per column | COUNT(NULL) / COUNT(*) | < 2% for critical fields |
| Required field population | All NOT NULL columns populated | 100% |
| Record completeness | % of rows with all required fields filled | > 98% |
| Conditional completeness | If field A is set, field B must also be set | 100% |
| Coverage completeness | Expected entities vs. actual entities present | > 95% |

### 2b. Accuracy

Measure how well data reflects the real-world truth.

| Check | Method | Threshold |
|-------|--------|-----------|
| Cross-source validation | Compare values against a trusted reference source | > 99% match |
| Business rule validation | Apply domain-specific rules (e.g., age > 0, price > 0) | 100% pass |
| Statistical outlier detection | Z-score or IQR method for numeric fields | < 1% flagged |
| Format accuracy | Values match expected patterns (email, phone, zip) | > 99% |
| Referential accuracy | Foreign keys resolve to valid parent records | 100% |

### 2c. Consistency

Measure agreement across datasets, systems, and time.

| Check | Method | Threshold |
|-------|--------|-----------|
| Cross-system consistency | Same entity across systems has matching values | > 99% |
| Intra-record consistency | Related fields within a row do not contradict | 100% |
| Temporal consistency | Values do not violate time-order logic (e.g., end > start) | 100% |
| Format consistency | Same field uses consistent formatting (date, currency, case) | > 99% |
| Aggregate consistency | Sum of parts equals the total | 100% |

### 2d. Timeliness

Measure whether data is available when needed and reflects current state.

| Check | Method | Threshold |
|-------|--------|-----------|
| Data freshness | Time since last update vs. expected refresh cadence | Within SLA |
| Latency | Time from source event to data availability | < agreed SLA |
| Staleness detection | Records not updated beyond expected lifecycle | < 5% stale |
| Delivery punctuality | Data arrives on or before scheduled time | 100% on-time |

### 2e. Uniqueness

Measure absence of unwanted duplicates.

| Check | Method | Threshold |
|-------|--------|-----------|
| Exact duplicate rows | Full-row hash comparison | 0 duplicates |
| Primary key uniqueness | COUNT(DISTINCT pk) = COUNT(*) | 100% |
| Near-duplicate detection | Fuzzy matching on name/address/email fields | < 1% suspected |
| Cross-source deduplication | Same entity appearing from multiple feeds | All resolved |

### 2f. Validity

Measure conformance to defined rules and standards.

| Check | Method | Threshold |
|-------|--------|-----------|
| Data type validation | All values match declared column type | 100% |
| Range validation | Numeric values within min/max bounds | 100% |
| Enumeration validation | Categorical values in allowed set | 100% |
| Regex pattern validation | Strings match expected patterns | > 99% |
| Schema conformance | No unexpected columns or missing expected columns | 100% |
| Business rule validation | Complex multi-field rules pass | 100% |

## Step 3: Scoring

Score each dimension on a 0-100 scale:

| Score Range | Grade | Interpretation |
|-------------|-------|---------------|
| 95-100 | A | Excellent -- production ready |
| 85-94 | B | Good -- minor issues, usable with caution |
| 70-84 | C | Fair -- significant issues, remediation needed before use |
| 50-69 | D | Poor -- major issues, unreliable for decisions |
| 0-49 | F | Critical -- data is unusable without remediation |

**Dimension Weight Defaults** (adjust per context):

| Dimension | Default Weight |
|-----------|---------------|
| Completeness | 20% |
| Accuracy | 25% |
| Consistency | 15% |
| Timeliness | 15% |
| Uniqueness | 10% |
| Validity | 15% |

**Composite Score** = Sum of (Dimension Score x Weight)

## Step 4: Root Cause Analysis

For every dimension scoring below B, investigate:

1. **What failed**: List the specific checks that fell below threshold
2. **Where it failed**: Identify affected columns, tables, or record subsets
3. **Why it failed**: Trace to source (upstream system, ETL bug, manual entry, schema drift)
4. **Since when**: Determine if this is a new issue or a longstanding gap
5. **Who is impacted**: Downstream consumers, reports, or models affected

## Step 5: Remediation Prioritization

Rank issues using this priority matrix:

| Priority | Criteria | Action Timeline |
|----------|----------|-----------------|
| P0 - Critical | Breaks downstream systems or reports, regulatory risk | Immediate (< 24 hours) |
| P1 - High | Materially affects analytics or decision-making | This sprint (< 1 week) |
| P2 - Medium | Degrades data usability but workarounds exist | Next sprint (< 2 weeks) |
| P3 - Low | Cosmetic or minor issues with no downstream impact | Backlog |

## Step 6: Output Format

Present results in this order:

### 1. Executive Summary
- Overall composite quality score and grade
- Number of dimensions at each grade level
- Top 3 critical findings requiring immediate action
- Trend vs. prior assessment (if available)

### 2. Data Quality Scorecard

| Dimension | Score | Grade | Weight | Weighted Score | Trend | Key Issue |
|-----------|-------|-------|--------|----------------|-------|-----------|
| Completeness | -- | -- | 20% | -- | -- | -- |
| Accuracy | -- | -- | 25% | -- | -- | -- |
| Consistency | -- | -- | 15% | -- | -- | -- |
| Timeliness | -- | -- | 15% | -- | -- | -- |
| Uniqueness | -- | -- | 10% | -- | -- | -- |
| Validity | -- | -- | 15% | -- | -- | -- |
| **Composite** | **--** | **--** | **100%** | **--** | -- | -- |

### 3. Failed Checks Detail

| Check ID | Dimension | Check Description | Expected | Actual | Severity | Affected Records |
|----------|-----------|-------------------|----------|--------|----------|-----------------|
| DQ-001 | ... | ... | ... | ... | P0-P3 | ... |

### 4. Remediation Plan

| Priority | Issue | Root Cause | Remediation Action | Owner | Target Date | Effort |
|----------|-------|------------|-------------------|-------|-------------|--------|
| P0 | ... | ... | ... | ... | ... | ... |

### 5. Monitoring Recommendations
- Checks to automate and run on every load
- Alerting thresholds and escalation paths
- Suggested reassessment cadence

## Quality Checklist

Before delivering results, verify:

- [ ] All six dimensions have been assessed with specific checks
- [ ] Scores are evidence-based with actual metrics, not estimates
- [ ] Failed checks include record counts and affected columns
- [ ] Root causes have been investigated, not just symptoms listed
- [ ] Remediation actions are specific, owned, and time-bound
- [ ] Priority assignments use the defined P0-P3 framework
- [ ] Composite score uses the correct weights
- [ ] Monitoring recommendations are included for ongoing governance

## Edge Cases

- **No reference data available**: Score accuracy based on internal consistency and business rule checks only; note the limitation
- **Streaming data**: Timeliness checks must account for event-time vs. processing-time; use watermarks
- **Unstructured or semi-structured data**: Adapt validity checks to schema-on-read; focus on parsability and field extraction rates
- **Very large datasets**: Use statistical sampling (minimum 10,000 rows or 1%, whichever is larger) and note confidence intervals
- **Multi-tenant data**: Assess quality per tenant; aggregate scores can mask tenant-specific issues
- **Newly created datasets**: Baseline the first assessment; trends and comparisons are not yet possible
- **Legacy systems with no documentation**: Reverse-engineer expected rules from data distributions; flag assumptions explicitly
