---
name: telemetry-analyst
description: Analyzes and summarizes SDD token costs and usage metrics from telemetry logs. Use when the user wants to see total project costs, phase-specific expenses, or detailed breakdowns of prompt, reasoning, and output tokens.
---

**Triggers**: "/update-telemetry"

# Telemetry Analyst

This skill provides tools and workflows to monitor the financial impact of the Agentic Code Supply Chain.

## Workflows

### 1. Generate Summary
To update the `telemetry_summary.json` file with the latest metrics:
- Run the analysis script: `python3 .gemini/skills/telemetry-analyst/scripts/analyze_telemetry.py`

### 2. View Costs
You can view the costs by phase or total:
- **Total Cost**: Aggregated across all logged interactions including **Prompt**, **Reasoning**, and **Output** tokens.
- **Phase Cost**: Breakdown by Foundations, Specs, Planning, Implementation, and Validation.

## Resources
- **Summary Backend**: `.factory/telemetry_summary.json`
- **Source Data**: `.factory/telemetry.json`
