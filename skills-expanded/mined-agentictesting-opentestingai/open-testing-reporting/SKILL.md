---
name: open-testing-reporting
description:       Test reporting, progress dashboards, release advice, and final test reports using the REPORTS agent pipeline. Use this skill whenever the user mentions test report, progress report, test dashboard, release advice, go/no-go decision, test metrics, defect trends, test execution summary, quality assessment, final test report, lessons learned, RAG status, or wants to generate any kind of testing status or quality report. Also trigger for executive summaries, sprint test reports, release readiness, or stakeholder communication about testing. MANDATORY TRIGGERS: test report, progress, dashboard, release advice, go/no-go, test metrics, defect trend, RAG status, quality report, test summary
---

<!-- Tip: Use /open-testing-reporting in chat to generate content with agent assistance -->

# Open Testing Reporting (REPORTS)

Generate comprehensive test reports, progress dashboards, release advice, and quality assessments. The REPORTS pipeline transforms raw test execution data into actionable reporting for stakeholders at all levels.

## Agent Pipeline

### Agent 1: R_realtime — Progress Reporter

Generate real-time test progress reports with RAG (Red/Amber/Green) status indicators.

**Procedure:**
1. Read test execution data (planned, executed, passed, failed, blocked, not-run)
2. Calculate progress metrics: execution progress, pass rate, defect discovery rate, blocked rate
3. Apply RAG thresholds:
   - **GREEN**: Execution ≥90%, Pass Rate ≥95%, Blocked ≤5%
   - **AMBER**: Execution 70-89%, Pass Rate 85-94%, Blocked 5-15%
   - **RED**: Execution <70%, Pass Rate <85%, Blocked >15%
4. Generate dashboard with sparkline trends

**Output (xlsx):**

| Metric | Target | Actual | RAG | Trend |
|---|---|---|---|---|
| Execution Progress | 90% | 82% | AMBER | +5% from yesterday |
| Pass Rate | 95% | 91% | AMBER | -2% from yesterday |
| Open Critical Defects | 0 | 3 | RED | Same as yesterday |
| Blocked Tests | <5% | 2% | GREEN | -3% from yesterday |

### Agent 2: E_execution_status — Execution Status Reporter

Detailed test execution breakdown across all dimensions.

**Breakdowns:**
- By Test Level: Unit / Integration / System / Acceptance
- By Test Type: Functional / Non-functional / Regression / Smoke
- By Priority: Critical / High / Medium / Low
- By Feature/Module: Per-feature execution and pass rates
- By Sprint/Iteration: Sprint-over-sprint comparison

**Defect Summary:**

| Severity | New | Open | In Progress | Resolved | Closed | Reopened |
|---|---|---|---|---|---|---|
| Critical | 1 | 3 | 2 | 5 | 12 | 0 |
| Major | 4 | 8 | 5 | 15 | 28 | 2 |
| Minor | 2 | 5 | 3 | 22 | 45 | 1 |

### Agent 3: P_product_quality — Quality Assessor

Assess product quality against exit criteria and ISO 25010 quality characteristics.

**Assessment Dimensions:**
1. Functional Suitability — Are all specified functions working correctly?
2. Performance Efficiency — Do response times meet NFR targets?
3. Compatibility — Works in all target environments?
4. Usability — Usability test results satisfactory?
5. Reliability — Defect density acceptable? MTBF projections?
6. Security — All security tests passed? Pen test results?
7. Maintainability — Code coverage metrics, static analysis clean?
8. Portability — Installation/migration tests passed?

For each exit criterion from the test plan, evaluate pass/fail with evidence.

**KB Files:** `terminology.json`, `ieee-standards.json` (IEEE 829 MTR/LTR), `quality-to-technique.json`

### Agent 4: O_outcome — Release Advisor

Generate release advice with go/no-go/conditional recommendation.

**Decision Framework:**
- **GO**: All exit criteria met, no open critical/major defects, coverage targets achieved
- **CONDITIONAL GO**: Most criteria met, known issues documented with workarounds, residual risk accepted
- **NO GO**: Critical criteria not met, open critical defects, unacceptable risk

**Release Advice Structure:**
```
# Release Advice: [Release] [Date]
## Recommendation: [GO / CONDITIONAL GO / NO GO]
## Summary (tests planned/executed/passed/failed, defect counts, coverage %)
## Exit Criteria Assessment (table with PASS/FAIL)
## Residual Risks (ranked with impact and mitigation)
## Conditions (if Conditional GO)
## Stakeholder Sign-off
```

### Agent 5: R_risk_report — Risk Reporter

Report on quality risk mitigation progress through testing.

**Sections:**
1. Risk Mitigation Matrix — How testing mitigated each identified product risk
2. Outstanding Risks — Not yet adequately mitigated
3. New Risks Discovered — Found during testing, not in original QRA
4. Risk Exposure Trend — Chart showing risk decreasing over testing cycles
5. Risk-based Coverage — Coverage percentage per risk class (A/B/C)

### Agent 6: T_trend — Trend Analyzer

Generate trend charts and velocity metrics over time.

**Charts:**
1. **Defect Discovery vs. Resolution** (line): Convergence indicates stability
2. **Test Execution Velocity** (area): Tests/day with burndown
3. **Defect Arrival Rate** (line): Should decrease toward release
4. **Coverage Growth** (line): Coverage % over time per coverage group
5. **Defect Age Distribution** (histogram): How long defects stay open
6. **Defect Root Cause Pareto** (bar): Top defect categories

**Analysis:** Calculate moving averages, detect trend direction, project completion date, flag anomalies.

### Agent 7: S_summary — Final Report Generator

Generate comprehensive final test reports and lessons learned.

**Final Test Report (IEEE 829-2008 MTR aligned):**
1. Report Identifier and Executive Summary
2. Variances from Test Plan
3. Comprehensive Quality Assessment (per ISO 25010 characteristic)
4. Summary of Results (by test level and type)
5. Detailed Test Metrics
6. Evaluation and Recommendation
7. Residual Risks
8. Lessons Learned and Process Improvements
9. Appendices

**Lessons Learned:**

| Area | What Went Well | What Could Improve | Action | Owner |
|---|---|---|---|---|
| Test Planning | Early risk analysis saved time | Estimation 30% under | Use historical data | QA Lead |
| Test Design | BVA found 12 critical defects | Classification tree underused | CTM training | Test Lead |

## Knowledge Base

Located at `/sessions/trusting-pensive-ptolemy/mnt/Open-Testing/knowledge-base/`:
- `terminology.json` — 1105 testing terms with definitions
- `ieee-standards.json` — IEEE 829-2008 test report document structures
- `quality-to-technique.json` — Quality characteristics for quality assessment
- `template-analysis.json` — Report template structures

Read the xlsx skill at `/sessions/trusting-pensive-ptolemy/mnt/.claude/skills/xlsx/SKILL.md` before generating spreadsheets.
Read the docx skill at `/sessions/trusting-pensive-ptolemy/mnt/.claude/skills/docx/SKILL.md` before generating documents.

## Input Requirements

- **Test execution data**: Test results (pass/fail/blocked) with dates
- **Defect data**: Severity, priority, status, dates
- **Test plan**: Exit criteria (or provide directly)
- **Risk analysis**: QRA with risk classes (from open-testing-design)

## Example Invocations

**"Generate a sprint test report for Sprint 15"**
→ R_realtime → E_execution_status → T_trend → S_summary

**"Are we ready to release version 3.2?"**
→ P_product_quality → O_outcome → R_risk_report → Export release advice

**"Show me defect trends for the last 6 sprints"**
→ T_trend → V_visualize → Export dashboard

## Integration

- **open-testing-coverage**: Receives coverage metrics for quality assessment
- **open-testing-management**: Feeds into process improvement
- **open-testing-design**: Uses risk classes for risk reporting
