<!-- owner: shared | audience: all-pms | last-updated: 2026-04 -->
<!-- purpose: One-command structured investigation: quant data + qual evidence + counter-evidence + hypothesis -->

# Investigate

You have been given a signal or question to investigate: **$ARGUMENTS**

Run a structured investigation combining quantitative data, qualitative evidence, and counter-evidence. Produce a hypothesis and recommended next steps.

**Important: Do NOT ask any clarifying questions. Do NOT pause for user input. Run the entire investigation in one pass.**

## Step 1: Parse the signal

Extract from the user's input:
- **Metric**: What is being measured (e.g. step completion rate, sign-up-to-activation, churn rate)
- **Segment**: Any filters (e.g. Android, new users, enterprise accounts)
- **Timeframe**: When (e.g. this week, since app release, Q1). Default to "recent" if not specified
- **Direction**: What changed (e.g. dropped, increased, anomaly)

State these clearly before proceeding.

## Step 2: Quantitative investigation

Run these searches in parallel:

### 2a. Metric definitions and baselines
- Read `data/funnel-context.md` for metric definitions, baselines, and how to interpret the metric (leading vs lagging)
- Read `context/current-priorities.md` to check if this metric relates to a current goal or target

### 2b. Data warehouse query (if MCP available)
- Use dbt Semantic Layer tools to search for relevant metrics (`list_metrics`, `query_metrics`)
- Use `get_all_models` or `get_mart_models` to find relevant dbt models
- Query BigQuery directly if the right table is identified
- Follow the conventions in your data warehouse conventions

### 2c. Saved data files (always — as fallback or supplement)
- Search `data/` folder for CSV files, saved reports, and metric files matching the signal keywords
- Search for any weekly business review (WBR) data or funnel detail files
- Grep across the repo for the specific metric values or trend references

Record: what the data says, the source, the time period, and confidence level (High / Medium / Low).

### 2d. Programmatic analysis (if quant data is available)

If the investigation involves quantitative data (metric trends, comparisons, distributions, or correlations) and CSV or BigQuery data is available:

1. Check that `data/notebooks/.venv/bin/papermill` exists
2. Run the investigation notebook with appropriate analysis type:
   ```
   data/notebooks/.venv/bin/papermill \
     data/notebooks/templates/investigation-template.ipynb \
     data/notebooks/outputs/investigation-{title}-{date}.ipynb \
     -k pm-analyst \
     -p investigation_title "{title}" \
     -p csv_paths "{comma-separated paths}" \
     -p analysis_type "{trend|comparison|distribution|correlation}" \
     -p metric_columns "{comma-separated}" \
     -p report_date "{date}"
   ```
3. Read the output JSON from `data/reports/charts/investigation-{title}-{date}.json`
4. Reference any generated chart PNGs in the investigation output
5. Use computed values (z-scores, correlations, distribution stats) as the quantitative foundation — more reliable than mental arithmetic

If the notebook fails, proceed with manual analysis as before. The notebook is a supplement, not a requirement.

## Step 3: Qualitative evidence search

Run these searches in parallel with Step 2:

### 3a. Internal knowledge base
- Grep all repo files for keywords related to the signal (metric name, feature area, platform)
- Search `insights/` for user research findings, interview summaries, and analysis
- Search `projects/` for related experiment docs or project files
- Check `context/personas/` for persona-specific context on the affected area

### 3b. Recent signals (if MCP available)
- Search Slack for recent mentions of the signal keywords (use `slack_search_public` if available)
- Check relevant channels: #product, #data, #engineering, {your-reviews-channel}, {your-suggestions-channel}

### 3c. Review data
- Search for recent customer review digests (`insights/qual/`)
- Search for app review digests (`insights/app-reviews/`)
- Grep for Trustpilot or App Store quotes related to the signal

Record: what was found, the source file or channel, when it was captured, and sample size where applicable.

## Step 4: Counter-evidence

Explicitly search for evidence that **contradicts or complicates** the emerging picture:

1. Search for positive signals in the same area (e.g. if completion dropped, look for segments where it improved)
2. Search for alternative explanations (e.g. seasonality, tracking changes, unrelated releases)
3. Check if any prior research or experiment results conflict with the hypothesis forming
4. Look for user quotes that express satisfaction with the area under investigation

If no counter-evidence is found, state this explicitly and note whether that's because:
- The signal is well-supported across sources, or
- We simply don't have data that would test the counter-hypothesis

## Step 5: Synthesis

Present the investigation results in this format:

---

# Investigation: [Signal description]

**Parsed signal**: [Metric] | [Segment] | [Timeframe] | [Direction]

---

## Quantitative findings

| Finding | Value | Source | Period | Confidence |
|---------|-------|--------|--------|------------|
| [What the data shows] | [Number] | [dbt model / CSV / report] | [When] | High / Med / Low |

**Summary**: [2-3 sentences on what the numbers tell us]

---

## Qualitative findings

| Finding | Source | Detail |
|---------|--------|--------|
| [Theme or insight] | [File path / Slack channel / review digest] | [Key quote or data point] |

**Key quotes**:
> "[Most relevant user/stakeholder quote]" -- [Source]

> "[Second most relevant quote]" -- [Source]

**Summary**: [2-3 sentences on what qual evidence tells us]

---

## Counter-evidence

| Evidence | Source | Implication |
|----------|--------|-------------|
| [What contradicts the main signal] | [Source] | [Why this matters] |

_If none found: "No counter-evidence identified. Note: [reason — well-supported OR insufficient data to test]"_

---

## Hypothesis

**IF** [we do / change X]
**THEN** [Y will happen — specific, measurable outcome]
**BECAUSE** [Z — the mechanism, grounded in evidence above]

**Strength**: Strong / Moderate / Weak
**Rationale**: [Why this strength rating — what evidence supports it, what's missing]

---

## Recommended next steps

1. [Most important action] — _[why this first]_
2. [Second action]
3. [Third action]

**Evidence gaps to fill**: [What we still don't know that would strengthen or invalidate the hypothesis]

---

_Investigation completed. Sources: [count] quantitative, [count] qualitative, [count] counter-evidence. [count] repo files searched._

## Step 6: Save discovery doc and create canonical

Save the investigation output to `projects/{signal-slug}/discovery.md`. Use the signal description, slugified (lowercase, hyphens, no special characters) as the folder name. Create the folder if it doesn't exist.

The saved file should contain the full synthesis from Step 5 above, plus a header block:

```markdown
**Date:** [today's date]
**Status:** Discovery complete
**Evidence strength:** [Strong / Moderate / Weak]
```

### Create or update canonical doc

Follow the canonical document convention in `pm-playbook/conventions/canonical-documents.md`. Use the **initiative canonical template**.

- If this is a new initiative folder, create `projects/{signal-slug}/canonical.md` with current stage set to "Discovery", the summary from the investigation, and the discovery.md linked in the stage artifacts table
- If a canonical doc already exists (from a prior stage), update the stage artifacts table and current status rather than overwriting
- Add a Key decisions entry: "{date}: Investigation initiated — {signal description}"

If a discovery doc already exists at the same path (from a prior investigation of the same signal), update it rather than creating a new one — add a dated section at the top noting the re-investigation and what changed. Also update the canonical doc's current status and Key decisions.

## Principles

- **State facts, not interpretations.** Label hypotheses and inferences explicitly
- **Cite sources precisely.** Every claim must reference a specific file, data source, or channel
- **Don't cherry-pick.** Actively search for contradictory evidence
- **Distinguish correlation from causation.** If two metrics move together, say so — don't imply causation without evidence
- **Qual is not quant.** Note sample sizes. User quotes illustrate themes, they don't prove prevalence
- **Don't fill gaps with assumptions.** "We don't have evidence for this" is a valid and useful answer
- **UK English** throughout
