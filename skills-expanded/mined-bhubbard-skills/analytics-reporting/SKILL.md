---
name: analytics-reporting
description: Generates reports from Google Analytics using the Data API, including custom and funnel reports.
---

# Google Analytics Reporting Skill

Use this skill when the user asks to generate or run a report from Google Analytics.

## Tools to use
You have access to the Google Analytics MCP server which provides the following tools for reporting:
- `run_report`: Runs a standard Google Analytics report.
- `run_funnel_report`: Runs a funnel report.
- `get_custom_dimensions_and_metrics`: Retrieves custom dimensions and metrics for a specific property to assist with building reports.

## Instructions
1. Determine if the user needs a standard report or a funnel report.
2. If necessary, use `get_custom_dimensions_and_metrics` to ensure you are requesting valid dimensions/metrics.
3. Call `run_report` or `run_funnel_report` with the necessary parameters (property ID, dimensions, metrics, date ranges, etc.).
4. Present the results clearly to the user, typically formatting the data in a markdown table or artifact for readability.
