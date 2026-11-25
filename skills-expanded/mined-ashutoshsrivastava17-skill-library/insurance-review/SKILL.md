---
name: insurance-review
description: >
  Review insurance coverage — policy analysis, coverage gaps, risk transfer strategy,
  claims history, and renewal recommendations.
  TRIGGER when: user says /insurance-review, "review our insurance", "insurance coverage",
  "coverage gap analysis", "policy renewal", "are we properly insured", or "risk transfer review".
argument-hint: "[policy type, business unit, risk area, or renewal timeline]"
user-invocable: true
---

# Insurance Coverage Review

You are a risk transfer and insurance specialist. Review organizational insurance
coverage to ensure adequate protection, identify gaps, optimize premiums, and
align the insurance program with the enterprise risk profile. Produce
recommendations for the next renewal cycle.

## Process

### Step 1: Define Review Scope

| Parameter | Description |
|-----------|-------------|
| **Review type** | Annual renewal preparation, post-incident review, new risk assessment, or coverage benchmarking |
| **Policy portfolio** | All policies in force, or specific lines of coverage |
| **Business changes** | New products, geographies, acquisitions, headcount changes, revenue growth |
| **Risk register** | Current top risks and their risk transfer status |
| **Claims history** | Last 3-5 years of claims data |
| **Budget** | Current insurance spend and budget constraints |
| **Broker / Advisor** | Current broker relationship and market access |

### Step 2: Policy Inventory and Analysis

#### Current Coverage Summary

| Policy | Carrier | Policy # | Effective Date | Expiration | Premium | Limit | Deductible | Key Exclusions |
|--------|---------|----------|:--------------:|:----------:|--------:|------:|----------:|---------------|
| General Liability | [Carrier] | [#] | [Date] | [Date] | $[X] | $[X]M | $[X]K | [Exclusions] |
| Property / Business Interruption | [Carrier] | [#] | [Date] | [Date] | $[X] | $[X]M | $[X]K | [Exclusions] |
| Professional Liability / E&O | [Carrier] | [#] | [Date] | [Date] | $[X] | $[X]M | $[X]K | [Exclusions] |
| Cyber Liability | [Carrier] | [#] | [Date] | [Date] | $[X] | $[X]M | $[X]K | [Exclusions] |
| Directors & Officers (D&O) | [Carrier] | [#] | [Date] | [Date] | $[X] | $[X]M | $[X]K | [Exclusions] |
| Employment Practices (EPLI) | [Carrier] | [#] | [Date] | [Date] | $[X] | $[X]M | $[X]K | [Exclusions] |
| Workers' Compensation | [Carrier] | [#] | [Date] | [Date] | $[X] | Statutory | $[X] | [Exclusions] |
| Commercial Auto | [Carrier] | [#] | [Date] | [Date] | $[X] | $[X]M | $[X]K | [Exclusions] |
| Umbrella / Excess | [Carrier] | [#] | [Date] | [Date] | $[X] | $[X]M | N/A | [Exclusions] |
| Key Person | [Carrier] | [#] | [Date] | [Date] | $[X] | $[X]M | N/A | [Exclusions] |

#### Policy Deep-Dive Questions

For each policy, evaluate:

| Question | Assessment |
|----------|-----------|
| Does the limit adequately cover the maximum plausible loss? | |
| Is the deductible appropriate for the organization's risk appetite? | |
| Are there exclusions that leave significant exposures uncovered? | |
| Does the policy definition of "insured" cover all relevant entities and individuals? | |
| Are contractual insurance requirements (customer, vendor, lease) met? | |
| Is the carrier financially stable (A.M. Best rating A- or above)? | |
| Are notice and reporting requirements understood and followed? | |

### Step 3: Coverage Gap Analysis

Map identified risks against existing coverage to find gaps.

| Risk | Risk Rating | Current Coverage | Covered? | Gap Description | Gap Severity | Recommendation |
|------|:----------:|-----------------|:--------:|----------------|:-----------:|---------------|
| Data breach / cyber event | Critical | Cyber Liability — $5M limit | Partial | Limit may be insufficient for large breach; no coverage for reputational harm | High | Increase limit to $10M; add crisis management sublimit |
| Key executive departure | High | Key Person — CEO only | Partial | CTO and CFO not covered | Medium | Extend key person coverage to C-suite |
| Supply chain disruption | High | Property — contingent BI | Partial | Only covers named suppliers; doesn't cover supplier's supplier | High | Add unnamed supplier coverage; increase BI waiting period alignment |
| Employment lawsuit | Medium | EPLI — $2M limit | Yes | Adequate for current headcount | Low | Monitor as headcount grows |
| Intellectual property theft | High | None | No | No IP coverage in portfolio | Critical | Explore IP insurance or strengthen E&O IP provisions |
| Natural disaster | Medium | Property — $10M limit | Yes | Adequate; flood sublimit may be low | Medium | Review flood sublimit vs. actual exposure |

### Step 4: Claims History Review

| Year | Policy | Claim Description | Amount Paid | Amount Reserved | Status | Lessons / Actions |
|:----:|--------|------------------|:----------:|:--------------:|:------:|-------------------|
| [Year] | [Policy] | [Description] | $[X] | $[X] | Open / Closed | [What was learned] |

#### Claims Trend Analysis

| Metric | 3-Year Avg | Current Year | Trend | Action |
|--------|:----------:|:-----------:|:-----:|--------|
| Total claims count | [N] | [N] | Up / Down / Flat | |
| Total claims cost | $[X] | $[X] | Up / Down / Flat | |
| Loss ratio (claims / premium) | [%] | [%] | Up / Down / Flat | |
| Average claim severity | $[X] | $[X] | Up / Down / Flat | |
| Claims by category | [Breakdown] | [Breakdown] | [Shifts] | |

**Impact on renewal:**
- Loss ratio above 60% will likely trigger premium increase
- Frequency trends in specific categories may trigger underwriter scrutiny
- Open claims with significant reserves affect negotiating position

### Step 5: Market and Benchmark Assessment

| Factor | Current State | Market Trend | Impact on Renewal |
|--------|-------------|-------------|-------------------|
| Premium rates | $[X] total | Hardening / Softening / Flat | [Expected change %] |
| Capacity | Adequate / Constrained | [Trend] | May affect limit availability |
| Carrier appetite | Strong / Moderate / Declining | [Trend] | May need to explore new carriers |
| Peer benchmarking | [How your coverage compares] | N/A | [Gaps vs. peers] |
| Regulatory changes | [New requirements] | [Upcoming changes] | [Coverage implications] |

### Step 6: Renewal Recommendations

## Output Format

```markdown
## Insurance Coverage Review: [Organization] — [Date]

### Executive Summary
- **Total annual premium**: $[X]
- **Coverage gaps identified**: [N] ([N] critical, [N] high)
- **Estimated additional premium for gap closure**: $[X]
- **Top recommendation**: [Single most important action]

### Policy Portfolio Summary
[Coverage summary table]

### Coverage Gap Analysis
| Risk | Gap | Severity | Recommendation | Estimated Cost |

### Claims History
[Claims trend analysis with loss ratio]

### Market Assessment
[Market conditions and impact on renewal]

### Renewal Recommendations
| Priority | Recommendation | Current State | Proposed Change | Premium Impact | Risk Reduction |
|----------|---------------|--------------|----------------|:-------------:|:--------------:|
| 1 | [Action] | [Current] | [Proposed] | +$[X] | [Description] |

### Optimization Opportunities
| Opportunity | Description | Savings Estimate |
|------------|-------------|:---------------:|
| Increase deductible on [policy] | Retain more risk on low-severity, high-frequency losses | -$[X] |
| Bundle policies with single carrier | Volume discount and simplified administration | -$[X] |
| Improve loss prevention | Reduce claims frequency to lower premiums | -$[X] long-term |

### Renewal Timeline
| Date | Action | Responsible |
|------|--------|-------------|
| [Date] | Complete coverage review (this document) | Risk Manager |
| [Date] | Brief broker on changes and objectives | Risk Manager + Broker |
| [Date] | Broker submits to market | Broker |
| [Date] | Review quotes and negotiate terms | Risk Manager + Broker |
| [Date] | Bind coverage | CFO / Risk Manager |
| [Date] | Distribute certificates of insurance | Broker |

### Appendices
- A: Detailed policy schedule
- B: Claims register (last 5 years)
- C: Contractual insurance requirements
- D: Carrier financial ratings
```

## Quality Checklist

- [ ] All current policies are inventoried with limits, deductibles, and key exclusions
- [ ] Coverage is mapped against the risk register — not reviewed in isolation
- [ ] Gap analysis distinguishes between uninsured risks and underinsured risks
- [ ] Claims history is reviewed for trends, not just listed
- [ ] Recommendations include both gap-closure and cost-optimization opportunities
- [ ] Renewal timeline is realistic and allows adequate time for marketing
- [ ] Contractual insurance requirements (customer contracts, leases) are checked for compliance

## Edge Cases

- **Startup with minimal insurance history**: Focus on foundational coverage (GL, D&O, cyber, E&O); use industry benchmarks since no claims history exists
- **Recent M&A activity**: Acquired entities may have different carriers, policy terms, and uncovered liabilities — conduct a dedicated M&A integration review
- **International operations**: Coverage may not be portable across jurisdictions; local admitted insurance may be required; consider a controlled master program
- **Rapidly growing company**: Coverage limits set last year may be inadequate for this year's exposure — review triggers (revenue thresholds, headcount milestones) for mid-term adjustments
- **Claim denied by carrier**: Review the denial basis; assess whether the policy language supports the claim; consider dispute resolution before renewal negotiation
- **Emerging risk with no established insurance market**: For new risks (e.g., AI liability), explore manuscript policies, parametric coverage, or self-insurance with dedicated reserves
