---
name: growth-mcp-connect
description: >
  Connect to growth-mcp MCP server for real campaign data, retention metrics,
  churn predictions, and A/B test analysis. Use when the user says "check
  our real data", "pull live metrics", "what does growth-mcp say", or before
  running any analysis that needs current numbers. Requires growth-mcp running.
metadata:
  author: thaolst
  version: "1.0"
  license: MIT
  related_skills:
    - campaign-brief
    - ab-test-analyzer
    - meu-planning
    - retention-analyzer
    - churn-intervention
    - voucher-mechanic-designer
---

# Growth MCP Connector

Kết nối Agent Skills với real growth metrics qua MCP server.

> Check `.agents/growth-metrics-context.md` first. If growth-mcp credentials
> are configured, you MUST pull live data before running any analysis.

## How to Connect

Ask the user:
1. "Do you have growth-mcp running? If yes, I'll pull real data."
2. If yes → call `get_growth_metrics` tool on the MCP server
3. If no → use values from `.agents/growth-metrics-context.md` or expert defaults

## Available Data

| Tool | Returns |
|------|---------|
| `design_campaign` | Campaign brief suggestions by level |
| `suggest_voucher` | Voucher design recommendations |
| `analyze_retention` | Cohort retention analysis |
| `predict_churn_risk` | Churn prediction + intervention |
| `analyze_experiment` | A/B test with statistical analysis |
| `estimate_sample_size` | Required sample size for experiments |

## When to Connect

- Before running `campaign-brief`: pull past campaign performance
- Before `ab-test-analyzer`: pull current experiment data
- Before `meu-planning`: pull current retention + churn
- Before `retention-analyzer`: pull real cohort data
- Before `churn-intervention`: pull current churn trends

## Related Skills

- [campaign-brief](../campaign-brief/) — writes briefs using real campaign data
- [ab-test-analyzer](../ab-test-analyzer/) — uses real experiment data
- [retention-analyzer](../retention-analyzer/) — uses real cohort data
- [churn-intervention](../churn-intervention/) — uses real churn metrics
