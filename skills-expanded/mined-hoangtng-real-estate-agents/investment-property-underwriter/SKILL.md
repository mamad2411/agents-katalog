---
name: investment-property-underwriter
description: Underwrite any residential investment property with a full financial model including NOI, cap rate, cash-on-cash return, DSCR, and 5-year projection. Use this skill whenever a user asks if a property is a good investment, what the cap rate is, how to analyze a rental property, whether a BRRRR deal pencils, what the cash flow would be, or "does this deal work." Also use when evaluating short-term rental (STR/Airbnb) feasibility or comparing LTR vs. STR returns. Produces a complete underwriting summary with a clear deal verdict.
---

# Investment Property Underwriter

Produces a complete investment property financial model — conservative underwriting, honest verdict, no wishful thinking. This is Rajan's work: cap rates before feelings.

## What You Need From the User

- **Property:** address or description, purchase price, property type (SFR / duplex / triplex / 4-plex / STR)
- **Financials:** asking rent or market rent estimate, current occupancy if tenant-occupied
- **Financing:** down payment %, expected rate, loan term (or cash purchase)
- **Expenses known:** property tax, HOA, insurance (use estimates if unknown)
- **Use case:** long-term rental / BRRRR / short-term rental / flip (affects model)

If purchase price is the only input, generate a full model with clearly marked assumptions and note what data would sharpen the analysis.

## Underwriting Rules (always applied)

- **Vacancy:** minimum 8% even in tight markets; 10% for STR/seasonal
- **Management fee:** always model 8–10% even if self-managing — this shows true economics
- **Maintenance:** 1% of value/year for properties under 15 years old; 1.5% for older
- **CapEx reserve:** 0.5–1% of value/year depending on age and systems
- **Never underwrite to optimistic rent growth** — use today's rents for Year 1
- **DSCR minimum:** flag any deal below 1.20x as financing risk

## Output: Standard Long-Term Rental

```markdown
## Investment Property Underwriting
**Property:** [Address] | [Asset Type]
**Prepared by:** Rajan, Investment Advisor | [Date]
**Recommendation:** [Strong Buy / Buy / Pass / Negotiate to $X]

---

### Acquisition
| Item                         | Amount      |
|------------------------------|-------------|
| Purchase Price               | $[X]         |
| Down Payment ([X]%)          | $[X]         |
| Loan Amount                  | $[X]         |
| Rate / Term                  | [X]% / [X]yr |
| Monthly P&I                  | $[X]         |
| Closing Costs (est. [X]%)    | $[X]         |
| Immediate Repairs / Updates  | $[X]         |
| **Total Cash-In at Close**   | **$[X]**     |

---

### Income (Annual)
| Item                              | Amount  |
|-----------------------------------|---------|
| Gross Rental Income               | $[X]     |
| Vacancy Allowance ([X]%)          | -$[X]    |
| **Effective Gross Income (EGI)**  | **$[X]** |

---

### Operating Expenses (Annual)
| Expense                        | Amount  | Basis              |
|--------------------------------|---------|--------------------|
| Property Tax                   | $[X]     | [X]% of value      |
| Insurance                      | $[X]     | Quote / estimate   |
| Property Management ([X]%)     | $[X]     | % of EGI           |
| Maintenance & Repairs          | $[X]     | [X]% of value      |
| CapEx Reserve                  | $[X]     | [X]% of value      |
| HOA (if applicable)            | $[X]     |                    |
| Utilities (landlord-paid)      | $[X]     |                    |
| **Total OpEx**                 | **$[X]** |                    |
| **Expense Ratio**              | **[X]%** | (healthy: 35–50%)  |

---

### Returns
| Metric                              | Value   | Benchmark        |
|-------------------------------------|---------|------------------|
| Net Operating Income (NOI)          | $[X]/yr  |                  |
| **Cap Rate**                        | **[X]%** | Market: ~[X]%    |
| Annual Debt Service                 | $[X]/yr  |                  |
| **DSCR** (NOI ÷ Debt Service)       | **[X]x** | Lenders want 1.2x+|
| **Annual Cash Flow**                | **$[X]** |                  |
| Monthly Cash Flow                   | $[X]/mo  |                  |
| **Cash-on-Cash Return**             | **[X]%** | Target: 6–8%+    |
| Gross Rent Multiplier               | [X]x     |                  |

---

### 5-Year Projection
*Assumes [X]% annual appreciation, [X]% annual rent growth*

| Year | Property Value | Equity  | Annual Cash Flow | Cumulative CF | Total Return |
|------|---------------|---------|-----------------|---------------|--------------|
| 1    | $[X]           | $[X]     | $[X]             | $[X]           | [X]%         |
| 2    | $[X]           | $[X]     | $[X]             | $[X]           | [X]%         |
| 3    | $[X]           | $[X]     | $[X]             | $[X]           | [X]%         |
| 5    | $[X]           | $[X]     | $[X]             | $[X]           | [X]%         |
| **Exit (Yr 5)** | | Net proceeds after 6% sale costs: **$[X]** | | **IRR: [X]%** | |

---

### Deal Verdict

**Recommendation:** ✅ Strong Buy / ✅ Buy / ⚠️ Marginal / ❌ Pass

**The case for this deal:**
[2–3 sentences: what makes this work — cash flow, equity upside, value-add potential]

**Key risks:**
1. [Risk + mitigation]
2. [Risk + mitigation]

**If the price were $[X] instead:** [How returns change — show the buyer their negotiating target]
```

## Output: BRRRR Analysis (when user mentions BRRRR or rehab/refinance)

Add this section to the standard model:

```markdown
## BRRRR Analysis

### Rehab Budget
| Item              | Cost   | Notes        |
|-------------------|--------|--------------|
| Roof              | $[X]    |              |
| Kitchen           | $[X]    |              |
| Bath(s)           | $[X]    |              |
| Flooring          | $[X]    |              |
| Paint             | $[X]    |              |
| HVAC / Mechanical | $[X]    |              |
| Contingency (15%) | $[X]    | Always include|
| **Total Rehab**   | **$[X]**|              |

### BRRRR Math
| Item                          | Amount  |
|-------------------------------|---------|
| Purchase Price                | $[X]     |
| Total Rehab                   | $[X]     |
| Holding Costs ([X] months)    | $[X]     |
| **All-In Cost**               | **$[X]** |
| After-Repair Value (ARV)      | $[X]     |
| Refi at [X]% of ARV           | $[X]     |
| **Cash Returned**             | **$[X]** |
| **Cash Left in Deal**         | **$[X]** |
| **% of Cash Recovered**       | **[X]%** |

**BRRRR Score:** [Full / Partial / Not a BRRRR] — [1-line explanation]
```

## Output: STR Feasibility (when user mentions Airbnb / short-term / vacation rental)

```markdown
## STR Feasibility Check

### Regulatory Gate (check first)
- STR permitted: [Yes / No / Check local ordinance]
- License required: [Yes ($[X]) / No]
- Owner-occupancy requirement: [Yes / No]
- HOA restriction: [Yes — blocks STR / No]
- **Proceed:** [Yes / No / Verify first]

### STR Projections
| Metric                        | Conservative | Market Avg |
|-------------------------------|-------------|------------|
| Occupancy Rate                | [X]%         | [X]%        |
| Average Daily Rate (ADR)      | $[X]         | $[X]        |
| Gross Annual Revenue          | $[X]         | $[X]        |
| Platform Fees (3%)            | -$[X]        | -$[X]       |
| Cleaning / Supplies           | -$[X]        | -$[X]       |
| STR Management ([X]%)         | -$[X]        | -$[X]       |
| **STR Net Income**            | **$[X]**     | **$[X]**    |

### LTR vs STR
| Metric         | LTR     | STR (conservative) | STR (market avg) |
|----------------|---------|--------------------|------------------|
| Annual Income  | $[X]     | $[X]                | $[X]              |
| Annual OpEx    | $[X]     | $[X]                | $[X]              |
| NOI            | $[X]     | $[X]                | $[X]              |
| Management load| Low      | High                | High              |
| **Verdict**    | Stable   | [X]% better/worse  | [X]% better/worse |
```

## Behavior Notes

- Always show the "what if I negotiate to $X" scenario — it gives the buyer their target.
- If cash flow is negative in Year 1: say so clearly. Don't bury it. "This deal does not cash flow at this price — here's what changes that."
- Cap rate below 4% in a non-appreciating market: flag as speculative.
- DSCR below 1.0: flag as "this deal cannot service its own debt."
- If user seems emotionally attached to a bad deal: present the numbers plainly, give the pass recommendation, and offer a counter — "here's what you'd need to make this work."
