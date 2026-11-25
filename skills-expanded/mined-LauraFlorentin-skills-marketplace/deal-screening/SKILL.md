---
name: deal-screening
description: >
  Rapid target evaluation through CIM extraction and IOI drafting. Strips
  sell-side marketing rhetoric from Confidential Information Memorandums to
  isolate core financials (EBITDA, margins, churn, CAC/LTV). Enables buy-side
  teams to screen dozens of targets daily and generate customized Indications
  of Interest.
  Use when user asks to "screen a deal", "evaluate acquisition target", "deal pipeline", or mentions target screening, deal criteria, or preliminary assessment.
---

# Deal Screening

Use only authorized deal materials. Cite each extracted figure to the source document and page, preserve confidentiality, label management claims and assumptions, and treat every IOI as a draft requiring investment, financing, and legal approval before submission.

This skill separates source-backed facts, management adjustments, and marketing claims so the deal team can perform preliminary screening and draft an IOI for review.

## The /cim-extract Protocol

### How It Works

Deliberately bypasses CIM formatting entirely. Instructs the AI to ignore narrative prose and extract only:
- **Quantitative assertions**: Revenue, EBITDA, margins, growth rates, customer metrics
- **Explicit strategic claims**: Market position, competitive moats, expansion vectors
- **Management adjustments**: Proposed EBITDA add-backs with stated rationale
- **Key risk indicators**: Customer concentration, churn rates, capex requirements

### Output Format

```
## CIM Extraction Summary — [Target Name]

### Financial Snapshot
| Metric | FY-2 | FY-1 | LTM | Mgmt Projection |
|--------|------|------|-----|-----------------|
| Revenue | | | | |
| Gross Margin | | | | |
| Adj. EBITDA | | | | |
| EBITDA Margin | | | | |
| Free Cash Flow | | | | |

### Proposed EBITDA Adjustments
| Add-Back | Amount | Rationale | Defensibility |
|----------|--------|-----------|---------------|
| | | | High / Medium / Low |

### Key Metrics
- **Customer concentration**: Top 10 = [X]% of revenue
- **Churn rate**: [X]%
- **CAC / LTV ratio**: [X]
- **Organic growth rate**: [X]%

### Investment Highlights (seller's claims)
1. [Claim] — [Supporting data point or "UNSUBSTANTIATED"]

### Red Flags
- [Identified concerns from the data]

### Verdict
[Quick BUY-SIDE assessment: Advance / Further Diligence / Pass]
```

## IOI Memorandum Generation

### Key Sections

| Section | Focus |
|---------|-------|
| Purchase Price Range | Enterprise valuation estimate, expressed as EBITDA multiple |
| Transaction Structure | Asset vs. stock, cash/equity/rollover/earn-out mix |
| Sources of Financing | Proof of funds, committed equity, anticipated leverage |
| Key Assumptions | Metrics the valuation relies upon |
| Due Diligence Scope | Remaining access required to reach definitive agreement |
| Timing & Approvals | Timeline to LOI and investment committee requirements |

### AI-Assisted IOI Workflow

1. Ingest the target's CIM and the buyer's investment committee memos
2. Map buyer's strategic rationale to seller's growth pillars
3. Generate bespoke IOI that feels tailored (not a form letter)
4. Align the offer structure directly with CIM's identified opportunities

## Operating Guidelines

- Never trust sell-side EBITDA at face value — always flag adjustments for validation
- Distinguish between organic and inorganic (M&A-driven) revenue growth
- Flag customer concentration above 20% for any single customer
- For IOIs, ensure the valuation range is defensible with stated methodology
- Record the time spent, evidence gaps, and review status rather than promising a fixed productivity gain


## Examples

**Input**: "Screen this CIM. Key criteria: >$20M EBITDA, >70% gross margin, <12x EV/EBITDA."

**Screening output**:
| Criterion | Target | Finding | Pass/Fail |
|---|---|---|---|
| EBITDA | >$20M | $23.4M (adj.) | ✅ Pass |
| Gross margin | >70% | 68% | ❌ Fail |
| EV/EBITDA (ask) | <12x | 14.5x implied | ❌ Fail |
| Customer concentration | <20% top customer | Top customer = 31% | ⚠️ Flag |

**Recommendation**: Pass. Gross margin and valuation both miss. Note concentration risk for future reference.


## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| CIM doesn't disclose key metrics | Sell-side omission | Flag gaps in screening report; request data room access or submit IOI with conditions |
| Adjusted EBITDA looks inflated | Aggressive add-backs | Challenge non-recurring items; apply QoE discount pending diligence |
| Too many deals passing screening | Criteria too loose | Tighten thresholds or add negative criteria (e.g., "no government revenue >30%") |
