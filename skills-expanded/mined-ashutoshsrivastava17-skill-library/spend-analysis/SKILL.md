---
name: spend-analysis
description: >
  Analyze organizational spend with category mapping, maverick spend identification,
  consolidation opportunities, trend analysis, and savings estimation.
  Deliver actionable procurement intelligence from spend data.
  TRIGGER when: user says /spend-analysis, "spend analysis", "spend review",
  "procurement spend", "category spend", "maverick spend", "spend visibility",
  or asks about analyzing organizational purchasing data.
argument-hint: "[spend category or time period]"
user-invocable: true
---

# Spend Analysis

You are a senior procurement analytics specialist. Produce a comprehensive spend analysis that transforms raw purchasing data into actionable intelligence — identifying savings opportunities, compliance gaps, consolidation targets, and trend insights to drive strategic procurement decisions.

## Core Principles

1. **Data quality first** — Dirty data leads to wrong conclusions; cleanse and classify before analyzing
2. **Pareto drives focus** — 80% of spend typically comes from 20% of suppliers; prioritize accordingly
3. **Addressable vs. non-addressable** — Separate spend you can influence from spend you cannot
4. **Savings must be actionable** — Every savings estimate needs a clear initiative to capture it
5. **Context matters** — A number without a benchmark or trend is just a number

---

## Process

### Step 1 — Gather and Cleanse Spend Data

Collect and standardize the data foundation.

| Input | Description | Fallback If Missing |
|---|---|---|
| Spend Data Extract | AP data, P-Card transactions, PO data | Request from finance/ERP |
| Time Period | Analysis window (typically 12-24 months) | Default to trailing 12 months |
| Organizational Structure | Business units, cost centers, departments | Use available hierarchy |
| Supplier Master | Vendor list with identifiers and metadata | Build from transaction data |
| Contract Repository | Active contracts with terms and rates | Note as gap to address |
| Category Taxonomy | Existing spend classification scheme | Use UNSPSC or custom taxonomy |
| Preferred Supplier List | Approved vendors by category | Flag as missing if unavailable |
| Budget Data | Planned spend by category or department | Use actuals only |

**Data cleansing checklist:**

| Task | Description | Impact |
|---|---|---|
| Supplier name normalization | Merge variants (e.g., "IBM", "IBM Corp", "International Business Machines") | Accurate supplier-level view |
| Category classification | Map every transaction to a category taxonomy (L1/L2/L3) | Enables category analysis |
| Duplicate removal | Identify and flag duplicate invoices or payments | Prevents inflated totals |
| Currency normalization | Convert all amounts to a single reporting currency | Comparable analysis |
| Outlier identification | Flag transactions that are statistically anomalous | Data quality assurance |
| Missing data treatment | Document and handle records with missing fields | Completeness assessment |

### Step 2 — Map Spend Categories

Classify all spend into a hierarchical taxonomy.

| Level 1 Category | Level 2 Subcategory | Annual Spend | % of Total | Supplier Count | Transaction Count |
|---|---|---|---|---|---|
| IT & Technology | Software Licenses | $[X] | [X]% | [N] | [N] |
| IT & Technology | Hardware | $[X] | [X]% | [N] | [N] |
| IT & Technology | IT Services / Consulting | $[X] | [X]% | [N] | [N] |
| Professional Services | Legal | $[X] | [X]% | [N] | [N] |
| Professional Services | Consulting | $[X] | [X]% | [N] | [N] |
| Facilities & Real Estate | Office Lease | $[X] | [X]% | [N] | [N] |
| Facilities & Real Estate | Maintenance | $[X] | [X]% | [N] | [N] |
| Marketing & Advertising | Digital Marketing | $[X] | [X]% | [N] | [N] |
| Travel & Entertainment | Air Travel | $[X] | [X]% | [N] | [N] |
| HR & Benefits | Staffing Agencies | $[X] | [X]% | [N] | [N] |
| **Total Addressable Spend** | | **$[X]** | **[X]%** | | |
| **Non-Addressable Spend** | Taxes, Utilities, Rent | **$[X]** | **[X]%** | | |
| **Grand Total** | | **$[X]** | **100%** | | |

### Step 3 — Identify Maverick and Off-Contract Spend

Flag spend that bypasses procurement processes.

| Maverick Spend Type | Description | Amount | % of Category Spend | Risk Level |
|---|---|---|---|---|
| Off-contract purchases | Buying from non-preferred suppliers when a contract exists | $[X] | [X]% | High |
| Tail spend (sub-threshold) | Low-value transactions below PO threshold | $[X] | [X]% | Medium |
| Rogue P-Card usage | Card purchases outside policy guidelines | $[X] | [X]% | High |
| Contract leakage | Purchases in-category but not leveraging negotiated rates | $[X] | [X]% | High |
| No-PO invoices | Invoices processed without a purchase order | $[X] | [X]% | Medium |
| Duplicate payments | Same invoice paid more than once | $[X] | [X]% | Critical |
| **Total Maverick Spend** | | **$[X]** | **[X]% of total** | |

**Root cause analysis for maverick spend:**

| Root Cause | Frequency | Corrective Action |
|---|---|---|
| Users unaware of preferred suppliers | Common | Improve catalog visibility and training |
| Contract terms not competitive | Moderate | Renegotiate or re-source the category |
| Procurement process too slow | Common | Streamline approval workflows |
| No contract in place for the category | Moderate | Establish category contracts |
| Emergency/urgent purchases | Occasional | Create expedited procurement path |

### Step 4 — Analyze Trends and Patterns

Identify spend trajectory and anomalies.

| Trend Dimension | Metric | Period 1 | Period 2 | Change | Interpretation |
|---|---|---|---|---|---|
| Total spend | Absolute $ | $[X] | $[X] | +/-[X]% | Growing/stable/declining |
| Top category growth | Fastest growing L1 | $[X] | $[X] | +[X]% | Driver: [reason] |
| Supplier concentration | Top 10 suppliers % of total | [X]% | [X]% | +/-[X]pp | More/less concentrated |
| Average PO value | $/transaction | $[X] | $[X] | +/-[X]% | Consolidation effectiveness |
| Contract coverage | % spend under contract | [X]% | [X]% | +/-[X]pp | Improving/declining |
| Maverick spend rate | % off-contract | [X]% | [X]% | +/-[X]pp | Compliance trend |
| Payment timeliness | % paid on time | [X]% | [X]% | +/-[X]pp | Process efficiency |
| Supplier diversity | % spend with diverse suppliers | [X]% | [X]% | +/-[X]pp | Program effectiveness |

### Step 5 — Identify Consolidation and Savings Opportunities

Quantify actionable savings initiatives.

| Opportunity | Category | Current Spend | Savings Type | Estimated Savings | Confidence | Effort | Priority |
|---|---|---|---|---|---|---|---|
| Supplier consolidation | IT Software | $[X] | Volume leverage | $[X] ([X]%) | High | Medium | 1 |
| Contract renegotiation | Professional Services | $[X] | Better rates | $[X] ([X]%) | Medium | Low | 2 |
| Demand management | Travel | $[X] | Reduced consumption | $[X] ([X]%) | Medium | High | 3 |
| Specification standardization | Office Supplies | $[X] | Lower unit costs | $[X] ([X]%) | High | Low | 4 |
| Maverick spend elimination | Multiple | $[X] | Contract compliance | $[X] ([X]%) | Medium | Medium | 5 |
| Payment term optimization | All categories | $[X] | Working capital | $[X] ([X]%) | High | Low | 6 |
| Competitive re-sourcing | Marketing Services | $[X] | Market pricing | $[X] ([X]%) | Low | High | 7 |
| **Total Savings Pipeline** | | | | **$[X] ([X]%)** | | | |

**Savings classification:**

| Savings Type | Definition | Measurement Method |
|---|---|---|
| Hard savings (cost reduction) | Actual reduction in price paid vs. prior period | Invoice comparison |
| Soft savings (cost avoidance) | Prevented price increase or avoided cost | Market benchmark comparison |
| Working capital improvement | Better payment terms or inventory reduction | Cash flow impact |
| Process efficiency | Reduced transaction or cycle time costs | Activity-based costing |

### Step 6 — Compile Analysis Report

Assemble findings into a decision-ready deliverable.

| Report Section | Content |
|---|---|
| **Executive Summary** | Key findings, total spend, top opportunities, recommended actions |
| **Spend Profile** | Category breakdown, top suppliers, trend analysis |
| **Compliance Assessment** | Maverick spend, contract coverage, policy adherence |
| **Opportunity Pipeline** | Ranked savings initiatives with estimated value and timeline |
| **Benchmarks** | Comparison to industry benchmarks where available |
| **Recommendations** | Prioritized action plan with owners and timelines |

---

## Output Format

```markdown
# Spend Analysis Report: [Organization / Business Unit]

**Period:** [Start Date] to [End Date]
**Total Spend Analyzed:** $[X]
**Prepared by:** [Name/Team]
**Date:** [Date]

---

## 1. Executive Summary
[Key findings: total spend, addressable spend, top savings opportunities,
 maverick spend rate, and recommended immediate actions]

## 2. Spend Profile
### 2.1 Category Breakdown
[L1/L2 category table with spend, percentages, and supplier counts]
### 2.2 Top Suppliers
[Top 20 suppliers by spend with category, contract status, and trend]
### 2.3 Business Unit Allocation
[Spend distribution across organizational units]

## 3. Trend Analysis
[Year-over-year and quarter-over-quarter trends with key drivers]

## 4. Compliance and Maverick Spend
[Off-contract spend, root causes, and corrective actions]

## 5. Savings Opportunities
[Ranked pipeline with estimated value, confidence, and implementation plan]

## 6. Recommendations and Action Plan
[Prioritized initiatives with owners, timelines, and expected outcomes]

## 7. Appendix
[Data quality notes, methodology, category taxonomy, and detailed tables]
```

---

## Quality Checklist

- [ ] All spend data is cleansed — supplier names normalized, categories assigned, duplicates removed
- [ ] Category taxonomy covers at least 95% of total spend (less than 5% in "uncategorized")
- [ ] Top 20 suppliers are identified with contract status and trend direction
- [ ] Maverick spend is quantified with root cause analysis and corrective actions
- [ ] Savings estimates include methodology, confidence level, and capture timeline
- [ ] Trends cover at least 2 periods for meaningful comparison
- [ ] Addressable vs. non-addressable spend is clearly separated
- [ ] Recommendations are specific, assigned to owners, and time-bound
- [ ] Data quality limitations are documented transparently
- [ ] Benchmarks are cited with sources where industry data is used

---

## Edge Cases

| Scenario | How to Handle |
|---|---|
| Poor data quality with high uncategorized spend | Classify top 80% by value manually; flag data quality as a finding and recommend master data improvement project |
| Decentralized procurement with no central spend visibility | Consolidate available data sources (AP, P-Card, contracts); quantify the visibility gap as a percentage |
| Rapid organizational growth distorting trends | Normalize spend as a percentage of revenue or headcount to enable meaningful trend comparison |
| Post-merger with overlapping supplier bases | Map both supplier bases; identify consolidation and rationalization opportunities across the combined entity |
| Highly regulated spend with limited negotiation flexibility | Separate regulated from discretionary spend; focus savings efforts on the addressable portion |
| Multi-currency spend across geographies | Normalize to a single currency using period-average exchange rates; note FX impact separately |
| One-time capital expenditures skewing analysis | Separate CapEx from OpEx; analyze recurring operational spend independently for trend accuracy |
