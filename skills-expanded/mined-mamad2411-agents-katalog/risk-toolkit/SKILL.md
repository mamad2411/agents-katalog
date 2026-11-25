---
name: risk-toolkit
description: Consolidated toolkit for risk. Covers risk-metrics-calculation, risk-manager
---
# Risk Toolkit

## Use this skill when
- Building risk dashboards
- Calculating risk-adjusted returns
- Implementing risk limits
- Measuring portfolio risk
- Needing guidance, best practices, or checklists for risk manager
- Regulatory reporting
- Setting position sizes
- Working on risk manager tasks or workflows

## Do not use this skill when
- The task is unrelated to risk manager
- The task is unrelated to risk metrics calculation
- You need a different domain or tool outside this scope

## Core Capabilities
# Risk Toolkit

# Risk Metrics Calculation

Comprehensive risk measurement toolkit for portfolio management, including Value at Risk, Expected Shortfall, and drawdown analysis.

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.

---

## Focus Areas

- Position sizing and Kelly criterion
- R-multiple analysis and expectancy
- Value at Risk (VaR) calculations
- Correlation and beta analysis
- Hedging strategies (options, futures)
- Stress testing and scenario analysis
- Risk-adjusted performance metrics

## Approach

1. Define risk per trade in R terms (1R = max loss)
2. Track all trades in R-multiples for consistency
3. Calculate expectancy: (Win% × Avg Win) - (Loss% × Avg Loss)
4. Size positions based on account risk percentage
5. Monitor correlations to avoid concentration
6. Use stops and hedges systematically
7. Document risk limits and stick to them

## Output

- Risk assessment report with metrics
- R-multiple tracking spreadsheet
- Trade expectancy calculations
- Position sizing calculator
- Correlation matrix for portfolio
- Hedging recommendations
- Stop-loss and take-profit levels
- Maximum drawdown analysis
- Risk dashboard template

Use monte carlo simulations for stress testing. Track performance in R-multiples for objective analysis.

---
