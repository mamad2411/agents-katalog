<!-- owner: shared | audience: all-pms | last-updated: 2026-04 -->
<!-- purpose: Structured experiment results analysis: pull data, validate hypothesis, check guardrails, assess segments, capture learnings, recommend decision -->

# Experiment Writeup

Analyse the results of an experiment and produce a structured writeup with learnings and a clear decision recommendation.

**Experiment:** $ARGUMENTS

**Important: Run the entire analysis in one pass. Do NOT pause for user input until the final step.**

## Step 0: Find the experiment doc

1. Search `projects/` for a file matching the experiment name or description
2. If no match, search `projects/` subdirectories and check file contents
3. If still no match, ask the user for the file path and stop

Read the experiment doc and extract:
- **Hypothesis** — what was being tested and why
- **Primary metric** — the success measure
- **Secondary metrics** — supporting measures
- **Guardrail metrics** — what must not get worse
- **Decision rules** — pre-committed criteria for ship / iterate / kill
- **Audience** — who was in the experiment, how traffic was split
- **Run time** — how long it ran, expected sample size
- **ROTI** — if calculated, the expected return on time invested

If any of these are missing from the doc, flag it: "The experiment doc is missing [X] — this makes rigorous analysis harder. Recommend adding this to future experiments."

## Step 1: Gather results data

Check for results in this order:
1. **Existing results doc** — look for a results file alongside the experiment doc (e.g. `*-results.md`, `*-analysis.md`)
2. **Project folder** — check for any data files, CSVs, or analysis docs in the same directory
3. **BigQuery** — if no pre-existing results, use `/dbt-data-source-researcher` to identify relevant tables and pull key metrics
4. **Ask the user** — if data isn't available in any of the above, state what data is needed and ask the user to provide it

Also check:
- `data/reports/` for relevant WBR data covering the experiment period
- `insights/quant/` for any related quantitative analysis
- Granola (via MCP) for post-experiment meeting transcripts that may contain analyst findings

### Step 1b: Run statistical analysis notebook (if data available)

If control and treatment data CSVs are available (from the experiment doc, project folder, or BigQuery export):

1. Check that `data/notebooks/.venv/bin/papermill` exists
2. Run the experiment analysis notebook:
   ```
   data/notebooks/.venv/bin/papermill \
     data/notebooks/templates/experiment-analysis.ipynb \
     data/notebooks/outputs/experiment-{name}-{date}.ipynb \
     -k pm-analyst \
     -p experiment_name "{name}" \
     -p control_data_path "{path}" \
     -p treatment_data_path "{path}" \
     -p primary_metric "{metric}" \
     -p guardrail_metrics "{comma-separated}" \
     -p significance_level 0.05
   ```
3. Read the notebook outputs from `data/reports/charts/`:
   - `experiment-results-{name}-{date}.json` — computed p-values, CIs, effect sizes
   - `experiment-summary-{name}-{date}.md` — formatted statistical summary
4. **Use the computed p-values and confidence intervals as the primary source** — do not compute statistical tests manually. The notebook uses scipy for proper Welch's t-tests, chi-squared tests, and power analysis.
5. Reference chart file paths in the writeup (distribution, forest plot, segment breakdown, novelty check)

If the notebook fails or data isn't in CSV format, proceed with manual analysis as before.

## Step 2: Analyse against hypothesis

For each metric category, assess:

### Primary metric
- **Result:** State the numbers (control vs treatment, delta, % change)
- **Statistical significance:** p-value if available, confidence interval, sample size
- **vs hypothesis:** Did it meet the threshold stated in the hypothesis?
- **Verdict:** Clear win / clear miss / ambiguous

### Secondary metrics
For each secondary metric:
- **Result:** Numbers and direction
- **What it tells us:** Does it explain the mechanism behind the primary result?
- **Surprises:** Anything that moved unexpectedly or didn't move when expected?

### Guardrail metrics
For each guardrail:
- **Result:** Numbers and direction
- **Verdict:** Safe / concerning / breached
- **If concerning:** Is it statistically significant? Is it directionally consistent across segments? What's the magnitude of the downside?

### Pre-committed decision rules
- Check each decision rule from the experiment doc
- State which rules are satisfied and which aren't
- If the result falls into an ambiguous zone not covered by decision rules, flag it

## Step 3: Segment analysis

Don't just report top-line. Break results down by available segments:
- **Device** (mobile vs desktop) — if applicable
- **Value band** (vehicle price brackets) — if applicable
- **User type** (new vs returning, cohort) — if applicable
- **User segment (if segment-specific experiment)
- **Any other relevant dimension** from the data

For each segment:
- Does the treatment effect differ meaningfully?
- Are there segments where the experiment works well but others where it doesn't?
- Are guardrail concerns concentrated in a specific segment?

Flag: "The biggest opportunity is in [segment] where [metric] improved by [X]. The biggest risk is in [segment] where [guardrail] worsened by [Y]."

## Step 4: Assess what we learned

Write 4–6 key learnings. Each learning must be:
- **Specific** — reference actual numbers, not vague trends
- **Actionable** — implies something we should do or stop doing
- **Honest** — include learnings about what didn't work or surprised us

Frame learnings as:
> **[Learning title]**
> [Evidence from the data] → [What this means for our understanding] → [Implication for next steps]

Also note:
- Did the hypothesis mechanism play out as expected, or did something else drive the result?
- Were there unintended consequences?
- What assumptions were validated or invalidated?

## Step 5: Decision recommendation

Based on the evidence, recommend one of:

| Decision | When to use |
|----------|-------------|
| **Ship** | Primary metric hit target, guardrails safe, no segment concerns |
| **Ship with mitigations** | Primary wins but guardrail signals need addressing — specify the mitigations |
| **Iterate and re-test** | Promising signal but concerns need resolving before full rollout — specify what changes |
| **Kill** | Primary metric missed or guardrails breached beyond acceptable levels |
| **Extend** | Insufficient data to decide — specify what sample size or duration is needed |

Structure the recommendation as:
- **Decision:** [Ship / Ship with mitigations / Iterate / Kill / Extend]
- **Rationale:** 2–3 sentences grounded in the data
- **If shipping:** What needs to happen for productionisation? Reference the playbook stage 3 (productionisation scoping)
- **If iterating:** What specifically would change in v2? What's the new hypothesis?
- **If killing:** What did we learn that redirects our effort?
- **Trade-offs acknowledged:** What are we accepting by making this decision?

## Step 6: Write the output

### Results doc

Save a structured results doc in the same initiative folder as the experiment file (e.g. `projects/{slug}/results.md`). If a results doc already exists, update it rather than creating a new one.

Also **update the canonical doc** (`projects/{slug}/canonical.md`) per the convention in `pm-playbook/conventions/canonical-documents.md`:
- Set current stage to "Analyse & Learn", update stage artifacts table, add decision to Key decisions
- If no canonical doc exists, create one using the initiative canonical template from the convention doc

Use this format:

```markdown
# [Experiment Name] — Results & Learnings

**Date:** YYYY-MM-DD
**Squad:** [Squad name]
**PM:** [From experiment doc]
**Analyst:** [If known]
**Status:** [Concluded — Ship / Iterate / Kill / Extend]
**Experiment doc:** [Relative path to experiment doc]

---

## Executive Summary

[3–4 sentences: what we tested, headline result, key trade-off, decision]

## Results

| Metric | Category | Control | Treatment | Delta | Stat sig? |
|--------|----------|---------|-----------|-------|-----------|
| ... | Primary | ... | ... | ... | ... |

## Segment Breakdown

[Key segment differences — table or narrative as appropriate]

## Key Learnings

1. **[Title]** — [Evidence → Meaning → Implication]
2. ...

## Decision

**Recommendation:** [Decision]
**Rationale:** [Evidence-based justification]
**Next steps:** [Specific actions]
**Trade-offs:** [What we're accepting]

## Process Notes

[Optional: anything about how the experiment was run that we'd do differently — sample size, duration, measurement approach, missing baselines]
```

### Insight summary

Append a one-paragraph learning to `insights/summaries/experiment-learnings.md` (create the file if it doesn't exist). Format:

```markdown
### [Experiment name] — [YYYY-MM-DD]
**Squad:** [Squad] | **Decision:** [Ship/Iterate/Kill/Extend]
[One paragraph: what was tested, what happened, what we learned that's useful beyond this specific experiment. Focus on the transferable insight.]
```

## Step 6b: Write to agent memory

After writing the results doc and insight summary, write the key transferable learning to agent memory files. This ensures the learning persists beyond the current quarter's state files.

1. **Identify transferable learnings** — from the Key Learnings in Step 4, select 1–3 entries that would be useful beyond this specific experiment. Focus on:
   - Data interpretation gotchas discovered (e.g. "Segment X behaves differently from aggregate — always check segment breakdown")
   - User behaviour patterns confirmed or invalidated
   - Methodology learnings (e.g. "This metric needs 4 weeks to stabilise — 2-week experiments aren't reliable")

2. **Write to analyst memory** — append entries to `team/{initials}/agents/memory/analyst.md` under the appropriate category (Data interpretation or Past investigations). Format: `- YYYY-MM-DD | {experiment name} | {one-line learning}`. Update the `Line count` and `Last updated` headers.

3. **Write to PM memory** — append entries to `team/{initials}/agents/memory/product-manager.md` under the appropriate category (Data interpretation, User behaviour, or Past investigations). Same format.

4. **Write to shared memory (if cross-cutting)** — if the learning is relevant to multiple agents (e.g. a seasonal pattern, a stakeholder preference revealed by experiment results), also append to `team/{initials}/agents/memory/shared.md`. Update headers.

5. **Enforce line budgets** — 150 for analyst and PM, 200 for shared. If at limit, replace the oldest superseded entry in the same category.

If the memory files don't exist, skip this step silently and continue.

## Step 7: Present and offer next steps

Display the full results doc to the user, then ask:

"Anything that doesn't match your read of the results? Any learnings to add or adjust?"

If the user identifies changes, update both the results doc and the insight summary.

Then offer:
- "Want me to draft the company-wide comms for this result?" (per playbook stage 2)
- "Want me to add productionisation actions to the todo list?" (if shipping)
- "Want me to draft the v2 experiment doc?" (if iterating)

## Important Notes

- **Don't cherry-pick.** If guardrails are concerning, say so clearly — even if the primary metric is a win. The decision section is where trade-offs get weighed, not the analysis section.
- **Segment analysis is not optional.** Top-line results hide important variation. A "clear win" that's driven entirely by one segment and neutral/negative in others is not a clear win.
- **Cite the pre-committed decision rules.** If the team defined criteria upfront, hold them to it. If the result doesn't fit the pre-committed rules, flag the gap rather than inventing a new interpretation.
- **Reference the playbook.** The post-experiment process is defined in `pm-playbook/process/6-analyse-and-learn.md` — the writeup should align with stages 1 and 2 (analysis and decision).
- **Be honest about confidence.** If sample size is small, the experiment was short, or the data has known issues, say so. "Directional but not conclusive" is a valid assessment.
