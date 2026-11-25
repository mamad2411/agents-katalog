---
name: are-dashboard
description: Show telemetry dashboard (costs, tokens, traces) (experimental)
disable-model-invocation: true
---

Show the ARE telemetry dashboard with cost analysis, token usage, and trace timelines.

<execution>
## STRICT RULES - VIOLATION IS FORBIDDEN

1. Run ONLY the exact command shown: `npx agents-reverse-engineer@$VERSION dashboard $ARGUMENTS`
2. DO NOT add ANY flags the user did not explicitly type
3. If user typed nothing after `/are-dashboard`, run with ZERO flags

## Steps

1. **Read version**: Read `.claude/ARE-VERSION` → store as `$VERSION`. Show the user: `agents-reverse-engineer v$VERSION`

2. **Run the dashboard command**:
   ```bash
   npx agents-reverse-engineer@$VERSION dashboard $ARGUMENTS
   ```

3. **Present the output** to the user. The dashboard has several modes:

   - **Default (no flags)**: Shows a summary table of all runs with costs, tokens, duration, and errors
   - **`--run <id>`**: Drill-down into a specific run showing per-entry details (latency, tokens, cost per file)
   - **`--trace <id>`**: ASCII Gantt timeline showing concurrent phase execution and worker utilization
   - **`--trends`**: Cost and usage trends across all runs (daily aggregation, cache savings, error rates)
   - **`--format html`**: Generate a self-contained HTML report with Chart.js visualizations — pipe to a file: `npx agents-reverse-engineer dashboard --format html > report.html`
   - **`--format json`**: Output raw run log data as JSON

4. **If no runs found**, suggest the user run `/are-generate` or `/are-update` first to create telemetry data.

**Options:**
- `--run <id>`: Show per-entry detail for a specific run (partial timestamp match)
- `--trace <id>`: Show ASCII timeline from a trace file (partial timestamp match)
- `--trends`: Show cost & usage trends across all runs
- `--format html`: Generate self-contained HTML report with charts
- `--format json`: Output raw data as JSON
</execution>
