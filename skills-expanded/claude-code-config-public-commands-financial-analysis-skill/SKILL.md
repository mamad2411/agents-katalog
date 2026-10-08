---
name: financial-analysis
description: Comprehensive financial analysis suite including DCF modeling, ratio analysis, sensitivity testing, Monte Carlo simulations, and financial statement evaluation for companies and investment opportunities
---

# Financial Analysis Suite

A comprehensive financial analysis toolkit combining ratio analysis, valuation modeling, and risk assessment using industry-standard methodologies.

## Core Capabilities

### 1. Financial Ratio Analysis
Calculate and interpret key financial metrics:
- **Profitability**: ROE, ROA, Gross Margin, Operating Margin, Net Margin
- **Liquidity**: Current Ratio, Quick Ratio, Cash Ratio
- **Leverage**: Debt-to-Equity, Interest Coverage, Debt Service Coverage
- **Efficiency**: Asset Turnover, Inventory Turnover, Receivables Turnover
- **Valuation**: P/E, P/B, P/S, EV/EBITDA, PEG
- **Per-Share**: EPS, Book Value per Share, Dividend per Share

### 2. Valuation Models

#### Discounted Cash Flow (DCF)
- Build complete DCF models with multiple growth scenarios
- Calculate terminal values using perpetuity growth and exit multiple methods
- Determine weighted average cost of capital (WACC)
- Generate enterprise and equity valuations

#### Comparable Company Analysis
- Identify peer companies
- Analyze trading multiples (P/E, EV/EBITDA, P/S)
- Calculate valuation ranges

#### Precedent Transactions
- Review similar deals for valuation benchmarks
- Analyze transaction premiums

### 3. Sensitivity & Scenario Analysis
- One-way and two-way sensitivity testing
- Tornado charts for sensitivity ranking
- Best/Base/Worst case scenario planning
- Monte Carlo simulation with probability distributions
- Breakeven analysis

### 4. Risk Assessment
- Identify and quantify key risks
- Calculate confidence intervals
- Stress test extreme cases
- Consider correlation effects

## Methodology

### Data Collection
1. Gather historical financial statements (income statement, balance sheet, cash flow)
2. Verify data sources for accuracy and completeness
3. Identify anomalies or missing data points

### Analysis Workflow
1. Calculate financial ratios with industry benchmarking
2. Build appropriate valuation models
3. Perform sensitivity analysis on key assumptions
4. Generate comprehensive report with recommendations

## Input Formats
- CSV with financial line items
- JSON with structured financial statements
- Text description of key financial figures
- Excel files with financial statements

## Key Outputs
1. **Executive Summary**: High-level findings and recommendations
2. **Financial Model**: Detailed projections with documented assumptions
3. **Valuation Range**: Multiple methods with sensitivity analysis
4. **Risk Assessment**: Key risks and mitigation factors
5. **Visualizations**: Charts, tornado diagrams, scenario comparisons

## Scripts

Located in `scripts/` directory:
- `calculate_ratios.py`: Financial ratio calculation engine
- `interpret_ratios.py`: Industry benchmarking and interpretation
- `dcf_model.py`: Complete DCF valuation engine
- `sensitivity_analysis.py`: Sensitivity and scenario testing framework

## Example Usage

**Ratio Analysis:**
```
"Calculate key financial ratios for this company based on the attached financial statements"
"Analyze the liquidity position using the balance sheet data"
```

**Valuation:**
```
"Analyze Tesla's financials and provide a DCF valuation"
"Evaluate this startup's unit economics and runway"
```

**Sensitivity:**
```
"Run sensitivity analysis showing impact of growth rate and WACC on valuation"
"Create tornado chart ranking key value drivers"
```

**Scenario Planning:**
```
"Develop three scenarios for this expansion project with probability weights"
"Run Monte Carlo simulation with 5,000 iterations"
```

## Best Practices

### Modeling Standards
- Consistent formatting and structure
- Clear assumption documentation
- Separation of inputs, calculations, outputs
- Error checking and validation

### Valuation Principles
- Use multiple methods for triangulation
- Apply appropriate risk adjustments
- Validate against trading multiples
- Consider both quantitative and qualitative factors

### Risk Management
- Use conservative assumptions when uncertain
- Include probability-weighted scenarios
- Clearly document all assumptions and rationale
- Present results with appropriate caveats

## Limitations
- Models are only as good as their assumptions
- Past performance doesn't guarantee future results
- Industry benchmarks are general guidelines
- Not a substitute for professional financial advice
