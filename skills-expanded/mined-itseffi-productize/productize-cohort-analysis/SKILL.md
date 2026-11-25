---
name: productize-cohort-analysis
description: >-
  Cohort Analysis. Use when analyzing retention by signup, activation, usage, plan, feature
  adoption, or customer segment, especially when churn, engagement, or product health needs
  cohort evidence.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Cohort Analysis

## Productize Preamble

Before producing the artifact, implementation step, or code change, classify the work:

- **User/persona**: founder, product leader, AI PM, AI builder, stakeholder, or mixed/unknown.
- **Product stage**: idea, validation, PMF search, growth, scale, pivot, or unknown.
- **Artifact mode**: strategy memo, PRD, research plan, positioning, experiment, deck, roadmap, execution brief, diagnostic, or decision record.
- **Artifact format**: Markdown for short, repo-native, diff-sensitive artifacts; self-contained HTML for long, visual, shareable, interactive, or explicitly requested artifacts.
- **Evidence standard**: what is known, assumed, missing, and risky.
- **Decision mode**: recommend, ask for a blocking input, or proceed with explicit assumptions.

Operating rules:

1. Do not produce generic product strategy filler. Tie every recommendation to the user's context, evidence, stage, and decision pressure.
2. Separate facts from assumptions. Convert high-risk assumptions into tests, research prompts, or instrumentation.
3. Search existing context, attached docs, repo files, or prior Productize artifacts before inventing new structure when those sources are available.
4. Ask only for inputs that materially change the output. If the next step is obvious, proceed and state assumptions.
5. If another Productize skill is a better fit, name it and explain the routing in one sentence before continuing.
6. Enforce the output contract for this skill. Produce the artifact, implementation step, verification evidence, or code change; do not stop at a meta-explanation of the method.
7. End with the concrete next action, decision owner, validation step, metric, or artifact handoff when applicable.
8. Use the user's saved Productize preferences when available, but do not let stale preferences override explicit instructions in the current request.
9. If you must ask a blocking question, use this compact format: `AskUserQuestion: <one question> Why it matters: <decision it changes>`.
10. Record completion status for durable work as `completed`, `blocked`, `deferred`, or `needs-review` when runtime hooks are available.

Artifact format policy:

- Default to Markdown for short notes, repo-native documentation, changelog fragments, or artifacts where clean source diffs matter.
- Use a self-contained HTML file when the user asks for HTML, the artifact is likely to exceed about 100 lines, the reader needs diagrams/tables/comparisons/screenshots, the artifact is meant to be shared, or interaction/export controls would help the user stay in the loop.
- Route by product job first, then choose the format. Do not create a generic HTML workflow when a Productize playbook, gate, or routed skill owns the work.
- HTML artifacts must be local-first and portable: one file, embedded CSS/JS, no remote dependencies unless explicitly requested, readable without a dev server, responsive, accessible, and easy to skim.
- Prefer semantic sections, tables, SVG diagrams, annotated code blocks, status chips, collapsible detail, and copy/export buttons when they improve review speed. Avoid decorative complexity that hides the decision.
- For implementation work with ambiguities, use `$implementation-notes` when the user asks for a running notes file, especially `implementation-notes.html` or `implementation-notes.md`.

Runtime hooks, if available:

- Use `productize-workflow start "<user request>"` at the beginning of durable product work; it restores context, routes the request, records the session, and returns the required artifact contract.
- Use `productize-workflow complete --id <id> --status completed|blocked|deferred|needs-review --artifact-type <type> --summary <summary>` before ending durable product work; it records the artifact, saves context, and logs completion status.
- Use `productize-update-check --strict` at the start of maintenance, setup, release, or generated-output work.
- Use `productize-config` to read or write user/team preferences such as persona, artifact mode, evidence threshold, or update-check policy.
- Use `productize-session-log` to record important workflow decisions.
- Use `productize-artifact-log` when a durable artifact is produced.
- Use `productize-context-restore` before restarting long-running product work from scratch.
- Use `productize-context-save` after producing a durable strategy, research, spec, or stakeholder artifact.
- Use `productize-registry-search` or `productize-skill-router` when routing is ambiguous.
- Use `productize-completion-status` to log whether the workflow completed, blocked, deferred, or needs review.

Telemetry standard:

- Keep telemetry local by default in `.productize/` or `PRODUCTIZE_STATE_DIR`.
- Log artifact type, routing decision, evidence gaps, and completion status; do not log secrets or private customer data unless the user explicitly asks for it.

Current skill metadata:

- **Skill**: `cohort-analysis`
- **Lifecycle**: Measure
- **Category**: Analytics
- **Primary artifact**: Cohort retention and engagement diagnosis with segment-level actions

Use when analyzing retention by signup, activation, usage, plan, feature adoption, or customer segment, especially when churn, engagement, or product health needs cohort evidence.

## Productize Contract

- **Primary lifecycle**: Measure
- **Supporting lifecycle**: Growth
- **Primary artifact**: Cohort retention and engagement diagnosis with segment-level actions
- **Source method**: pm-skills-main/pm-data-analytics/skills/cohort-analysis/SKILL.md

## Method

## Purpose
Analyze user engagement and retention patterns by cohort to identify trends in user behavior, feature adoption, and long-term engagement. Combine quantitative insights with qualitative research recommendations.

## How It Works

### Step 1: Read and Validate Your Data
- Accept CSV, Excel, or JSON data files with user cohort information
- Verify data structure: cohort identifier, time periods, engagement metrics
- Check for missing values and data quality issues
- Summarize key statistics (cohort sizes, date ranges, metrics available)

### Step 2: Generate Quantitative Analysis
- Calculate cohort retention rates and engagement trends
- Identify retention curves, drop-off patterns, and anomalies
- Compute feature adoption rates across cohorts
- Calculate month-over-month or period-over-period changes
- Generate Python analysis scripts using pandas and numpy if requested

### Step 3: Create Visualizations
- Generate retention heatmaps (cohorts vs. time periods)
- Create line charts showing cohort progression
- Build comparison charts for feature adoption
- Visualize drop-off points and engagement trends
- Output as interactive charts or static images

### Step 4: Identify Insights & Patterns
- Spot one or more significant patterns:
  - Early churn in specific cohorts
  - Late-stage engagement changes
  - Feature adoption clusters
  - Seasonal or temporal trends
- Highlight surprising findings and deviations
- Compare cohort performance to establish baselines

### Step 5: Suggest Follow-Up Research
- Recommend qualitative research methods:
  - Targeted user interviews with churning users
  - Feature usage surveys with engaged cohorts
  - Session replays of key interaction patterns
  - Win/loss analysis for high vs. low retention cohorts
- Design follow-up quantitative studies
- Suggest A/B tests or feature experiments

## Usage Examples

**Example 1: Upload CSV Data**
```
Upload cohort_engagement.csv with columns: cohort_month, weeks_active,
user_id, feature_x_usage, engagement_score

Request: "Analyze retention patterns and identify why Q4 2025 cohorts
underperform compared to Q3"
```

**Example 2: Describe Data Format**
```
"I have monthly user cohorts from Jan-Dec 2025. Each row shows:
cohort date, user ID, purchase frequency, and support tickets.
Analyze which cohorts show best long-term retention."
```

**Example 3: Feature Adoption Analysis**
```
Upload feature_usage.xlsx with cohort adoption data.

Request: "Compare adoption curves for our new feature across cohorts.
Which cohorts adopted fastest? Any patterns?"
```

## Key Capabilities

- **Data Reading**: Import CSV, Excel, JSON, SQL query results
- **Retention Analysis**: Calculate and visualize retention rates over time
- **Cohort Comparison**: Compare metrics across cohort groups
- **Anomaly Detection**: Flag unusual patterns or drop-offs
- **Python Scripts**: Generate reusable analysis code for ongoing analysis
- **Visualizations**: Create heatmaps, charts, and interactive dashboards
- **Research Design**: Suggest targeted follow-up studies and interview approaches
- **Statistical Summary**: Provide quantitative metrics and correlation analysis

## Tips for Best Results

1. **Include time dimension**: Provide data across multiple time periods
2. **Define cohort clearly**: Make cohort grouping explicit (signup month, feature launch date, etc.)
3. **Provide context**: Explain product changes, launches, or events during the period
4. **Multiple metrics**: Include retention, engagement, feature usage, revenue, etc.
5. **Sufficient data**: At least 3-4 cohorts for meaningful pattern identification
6. **Request specific output**: Ask for visualizations, Python scripts, or research recommendations

## Output Format

You'll receive:
- **Data Summary**: Cohort overview and data quality assessment
- **Quantitative Findings**: Key metrics, retention rates, and trend analysis
- **Visualizations**: Charts showing retention curves, adoption patterns
- **Pattern Identification**: 2-3 significant insights from the data
- **Research Recommendations**: Specific qualitative and quantitative follow-ups
- **Analysis Scripts** (if requested): Python code for reproducible analysis
- **Next Steps**: Prioritized actions based on findings

---

### Further Reading

- [Cohort Analysis 101: How to Reduce Churn and Make Better Product Decisions](https://www.productcompass.pm/p/cohort-analysis)
- [The Product Analytics Playbook: AARRR, HEART, Cohorts & Funnels for PMs](https://www.productcompass.pm/p/the-product-analytics-playbook-aarrr)
- [Are You Tracking the Right Metrics?](https://www.productcompass.pm/p/are-you-tracking-the-right-metrics)

## Productize Output Rules

- Produce the artifact named in the Productize contract, not a generic framework summary.
- Separate known facts, assumptions, missing evidence, and risky leaps before recommending.
- Convert uncertain claims into validation steps, metrics, owner decisions, or launch/readout checks.
- If this reference method conflicts with Productize evidence standards, keep the Productize standard.
