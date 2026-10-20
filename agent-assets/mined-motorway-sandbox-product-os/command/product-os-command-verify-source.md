<!-- owner: shared | audience: all-pms | last-updated: 2026-02 -->
<!-- purpose: Audit evidence accuracy, confidence, and bias after pulling insights or data -->

# Verify Source

Review the evidence and insights presented earlier in this conversation for accuracy, confidence, and potential bias.

Run this command after asking for insights, evidence, or data analysis — it acts as a structured second pass to catch issues before you build on the findings.

## Instructions

Before starting, read `pm-playbook/evidence-standards/audit-criteria.md` for the detailed evaluation criteria and `pm-playbook/evidence-standards/output-template.md` for the output format. If either file is missing, proceed using the audit steps below and the Key Principles section as your guide — the command still works without the reference files.

### Step 1: Identify what to audit

Look back through the current conversation and identify all claims, insights, data points, and conclusions that were presented. List them as a numbered set of statements.

### Step 2: Audit each statement

For each statement, evaluate against the criteria in `pm-playbook/evidence-standards/audit-criteria.md`:

- **2a. Source verification** — check the cited source is correct, current, and accurately represented
- **2b. Confidence assessment** — rate High / Medium / Low using the defined criteria
- **2c. Bias check** — test for confirmation, survivorship, selection, anchoring, and correlation/causation biases
- **2d. dbt layer verification** — for any quantitative claim, verify the underlying dbt model definition, health, and lineage
- **2e. Gaps and assumptions** — identify missing evidence, unstated assumptions, and counter-evidence

### Step 3: Search for counter-evidence

For any hypothesis or conclusion presented in the conversation:

1. Identify the core claim
2. Search relevant data files, research documents, and insight files for evidence that contradicts or complicates the claim
3. Report what you find — even if the counter-evidence is weak, it's worth noting

If you find no counter-evidence, say so explicitly and note whether that's because the claim is well-supported or because we simply don't have data that would test it.

### Step 2f: Computational verification

For quantitative claims identified in Step 1 (claims with specific numbers, percentages, or metrics):

1. Check that `data/notebooks/.venv/bin/papermill` exists
2. Prepare a JSON array of claims to verify, each with: `statement`, `cited_value`, `cited_source`, `metric_name`
3. Identify relevant CSV data sources from `data/reports/` that contain the cited metrics
4. Run the verify-claim notebook:
   ```
   data/notebooks/.venv/bin/papermill \
     data/notebooks/templates/verify-claim.ipynb \
     data/notebooks/outputs/verify-claim-{date}.ipynb \
     -k pm-analyst \
     -p claims_json '{json_string}' \
     -p data_sources "{comma-separated paths}" \
     -p report_date "{date}"
   ```
5. Read outputs from `data/reports/charts/`:
   - `verification-{date}.json` — per-claim verification status and computed values
   - `verification-summary-{date}.md` — formatted verification table
6. Add a **Computationally verified** column to the audit table in Step 5, showing: Verified / Discrepancy / Unverifiable for each quantitative claim
7. For any discrepancies, note the computed value alongside the cited value and flag for investigation

If the notebook fails or claims are purely qualitative, skip this step and note "Computational verification not applicable" in the output.

### Step 4: Pattern check — should we fix the source?

If the audit reveals a significant number of low-confidence, corrected, or misleading statements (roughly a third or more), diagnose *why* using the root cause checklist in `pm-playbook/evidence-standards/audit-criteria.md` and recommend upstream fixes.

### Step 5: Output

Present the audit using the template in `pm-playbook/evidence-standards/output-template.md`.

## Key Principles

- **Be adversarial, not confirmatory.** Your job here is to find problems, not validate the work
- **Re-read actual sources.** Don't rely on what was claimed about a source — go back and check
- **"We don't know" is a valid finding.** Flagging a gap is more useful than papering over it
- **Distinguish between "wrong" and "uncertain".** A low-confidence insight isn't necessarily wrong — it just needs to be treated differently
- **Don't fabricate counter-evidence.** If you can't find contradictory data, say so honestly. Don't invent concerns for the sake of balance
- **UK English** throughout
