---
name: cpk-analyze
description: Analyze CPK capability history, evaluate alert rules, and generate HTML reports. Use when reviewing process capability status, checking for degrading CPK trends, generating quality reports for stakeholders, or identifying stations and parameters that need attention. Requires cpk-track to have been run first.
compatibility: Python 3.10+, pandas, numpy, scipy, plotly. Requires cpk-track to have been run first.
---

# CPK Analyze - Rule Evaluation & Report Generation

Evaluate capability history against alert rules and generate HTML reports.

## When to Use

- Reviewing overall process capability status across all tracked targets
- Checking for degrading CPK trends that need attention
- Generating quality reports for stakeholders or audits
- Identifying specific stations, channels, or parameters with poor capability
- After `cpk-track` has been run to import new data

## Prerequisites

1. **Project initialized** — `cpk-init` has created config and database
2. **Data tracked** — `cpk-track` has been run to compute capability results
3. **Sufficient history** — At least one tracking period of data

## How to Invoke

```python
from auto_cpk.skills.cpk_analyze import run_analyze

result = run_analyze(
    config_path=".auto_cpk/config.json",
)
```

## Output

Returns an `AnalyzeResult` with:

| Field | Description |
|-------|-------------|
| `report_path` | Path to generated HTML report (e.g., `reports/cpk-report-YYYYMMDD.html`) |
| `alerts` | List of `AlertEvent` objects triggered by rule evaluation |
| `diagnostics` | Error/info messages if analysis could not complete |

## Alert Rule Evaluation

### Threshold Rules

| Rule | Threshold | Level | Meaning |
|------|-----------|-------|---------|
| `ppk_above_1_33` | Ppk >= 1.33 | **ok** | Process is capable |
| `ppk_warning` | Ppk < 1.33 | **warning** | Process is marginal — monitor closely |
| `ppk_fail` | Ppk < 1.0 | **fail** | Process cannot consistently meet specs |
| `ppk_critical` | Ppk < 0.67 | **critical** | Immediate corrective action required |

### Trend Rules

Detects consecutive Ppk decline across time periods:
- **Declining trend**: Ppk decreases for N consecutive periods
- **Amplitude check**: Total decline exceeds a minimum threshold
- Triggers **warning** level alert when both conditions are met

## HTML Report

The generated report includes:

1. **Summary cards** — Overall capability status with color coding
2. **Per-target breakdown** — Each tracked measurement item
3. **Per-group details** — Results by Station ID + Channel ID
4. **Trend sparklines** — Ppk trend over time periods
5. **Rule alerts** — Highlighted items that triggered warnings or failures
6. **Color coding**:
   - Green: Ppk >= 1.33 (capable)
   - Yellow: 1.0 <= Ppk < 1.33 (marginal)
   - Red: Ppk < 1.0 (incapable)

The report is self-contained HTML with embedded CSS — no external dependencies.

## Alert Events

Each alert contains:

```python
AlertEvent(
    rule_id="ppk_fail",           # Which rule triggered
    target_id="Item42",           # Measurement item
    group_key="FCT2|1",          # Station|Channel group
    severity="fail",             # warning / fail / critical
    message="Ppk=0.002 is below 1.0",
    observed_value=0.002,        # Actual Ppk value
    threshold=1.0,               # Rule threshold
)
```

Alerts are saved to the database for historical tracking.

## Interpretation Guide

### Ppk Values

| Ppk Range | Rating | Action |
|-----------|--------|--------|
| >= 1.67 | Excellent | No action needed |
| 1.33 - 1.67 | Good | Routine monitoring |
| 1.00 - 1.33 | Marginal | Investigate — process may be drifting |
| 0.67 - 1.00 | Poor | Corrective action required |
| < 0.67 | Critical | Stop and fix immediately |

### Cp vs Cpk Difference

- **Cp >> Cpk**: Process is capable but off-center — adjust mean toward target
- **Cp ≈ Cpk**: Process is well-centered
- **Both low**: Process variation is too large — reduce spread

### Worse Side

The `worse_side` field tells you which spec limit is closer:
- `"upper"`: Mean is closer to USL — risk of exceeding upper limit
- `"lower"`: Mean is closer to LSL — risk of falling below lower limit

## Edge Cases

- **No tracked targets**: Returns diagnostic "No tracked targets configured"
- **No capability results**: Returns diagnostic "No capability results found. Run track first."
- **Empty history**: Analysis completes but no alerts triggered
- **Single period**: No trend analysis possible (needs 2+ periods)

## Configuration

Analysis behavior is controlled by the project config (`.auto_cpk/config.json`):

| Setting | Default | Description |
|---------|---------|-------------|
| `output_dir` | `"reports"` | Where HTML reports are saved |
| `database_path` | `".auto_cpk/auto_cpk.sqlite"` | Capability data source |
| `rule_file` | `"ruler.md"` | Custom rule definitions (optional) |

## Workflow

The complete 3-step CPK analysis workflow:

```
1. cpk-init  →  Configure project, select items to track
2. cpk-track  →  Import data, compute Pp/Ppk/Cp/Cpk
3. cpk-analyze →  Evaluate rules, generate reports, trigger alerts
```

Repeat steps 2-3 as new data becomes available for ongoing monitoring.
