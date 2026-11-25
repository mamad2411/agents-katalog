---
name: artifact-quality-audit
description: "Scores Leeward artifacts against rubric dimensions, compares quality across a set, and surfaces drift patterns. Produces a Quality Audit Report with per-artifact scores, trend observations, and targeted recommendations."
category: measurement
default_depth: standard
---

# Artifact Quality Audit

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Scores a set of Shipwright artifacts against the universal rubric dimensions (Clarity, Completeness, Actionability, Correctness), layers artifact-specific eval criteria when available, and compares scores across the set to detect quality drift. The output is a Quality Audit Report, a scoring artifact, not a review or rewrite.

This skill is distinct from adversarial review. Adversarial review pressure-tests a single artifact for weak reasoning. Quality audit scores multiple artifacts against a consistent rubric to find patterns over time.

## When to Use

- After producing several artifacts in a session or sprint, to check whether quality is holding
- When a PM suspects output quality has degraded but can't pinpoint where
- Before adopting a new workflow or agent configuration, to establish a quality baseline
- During a retrospective, to ground "the outputs felt weaker" in scored evidence
- When onboarding a new team member to Shipwright, to calibrate expectations

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick pulse on 2-3 artifacts | Scores Table + one-line trend summary |
| **Standard** | Typical audit of 3-5 artifacts from recent work | All sections |
| **Deep** | Comprehensive audit across a full quarter or project, or comparison across agent/workflow configurations | All sections + per-agent breakdown, cross-workflow comparison, historical baseline if available |

**Omit rules:** At Light depth, skip Trend Analysis narrative and Recommendations. Produce only the scores table and a one-line summary of the strongest and weakest dimension. At Deep depth, add per-agent and per-workflow breakdowns but do not re-run or rewrite any artifact.

## Framework

### Step 1: Define the Audit Set

Identify which artifacts to score:

```markdown
## Audit Set

| # | Artifact | Type | Date | Producing Workflow/Agent |
|---|---|---|---|---|
| 1 | [name] | [PRD / Strategy / Research / etc.] | [date] | [/write-prd, @strategy-planner, etc.] |
| 2 | ... | ... | ... | ... |
```

If the PM has not specified artifacts, offer to review the last 3-5 from the current project. Confirm the list before scoring.

### Step 1b: Run the Deterministic Pre-Pass

Before scoring manually, locate the nearest Shipwright installation root containing
`manifest.json` and run the postflight validator on each artifact file by its absolute installed path:

```bash
node "<absolute-shipwright-root>/scripts/validate-artifact.mjs" path/to/artifact.md
```

The validator produces machine-generated issue counts for unsupported claims and missing sections. Use these counts as a floor for the **Correctness** dimension, an artifact flagged for multiple unsupported dollar figures cannot score above 6 on Correctness without PM-reviewed justification. If the artifact has a `## Sources` / `## References` / `## Evidence` section, citation checks are skipped and that penalty does not apply. Record the validator output alongside each artifact in the audit set.

### Step 2: Score Each Artifact

Apply the universal 4 dimensions from `/evals/rubric.md`:

- **Clarity** (1-9): Can the reader understand the artifact without re-reading?
- **Completeness** (1-9): Are all required sections present and substantive?
- **Actionability** (1-9): Can someone act on this artifact without asking follow-up questions?
- **Correctness** (1-9): Are claims sourced, consistent, and free of logical errors?

Use the anchored scale:
- **3** = Weak, significant gaps, confusion, or unsupported claims
- **6** = Adequate, meets the bar, no major issues
- **9** = Strong, notably sharp, thorough, and ready to act on

If an artifact-specific eval exists in `/evals/` (e.g., `prd.md`, `strategy.md`, `adversarial-review.md`), layer those additional dimensions and note them separately.

For each artifact, record:
1. Score per dimension with a one-line rationale citing specific evidence
2. Total score (sum of 4 universal dimensions)
3. Quality band: **Below Bar** (<18), **At Bar** (18-27), **Above Bar** (28+)

### Step 3: Compare and Detect Patterns

Produce a comparison table:

```markdown
## Scores

| Artifact | Clarity | Completeness | Actionability | Correctness | Total | Band |
|---|---|---|---|---|---|---|
| [name] | [score] | [score] | [score] | [score] | [total] | [band] |
| ... | ... | ... | ... | ... | ... | ... |
```

Then analyze:
- Any dimension declining across artifacts (quality drift)
- Any dimension consistently weak regardless of artifact type
- Patterns tied to specific workflows or agents
- Dimensions that are improving or consistently strong

### Step 4: Recommend Actions

Based on findings, produce 3-5 targeted recommendations:

1. **Failure modes to watch**, reference specific patterns from `docs/failure-modes.md`
2. **Recovery playbooks**, suggest which playbooks to apply for Below Bar artifacts
3. **Instruction tightening**, if a specific agent or workflow consistently underperforms on a dimension, recommend what to change

Each recommendation must be specific (name the dimension, the agent/workflow, and the fix) rather than generic ("improve quality").

## Minimum Evidence Bar

**Required inputs:** One or more completed Shipwright artifacts. A single-artifact audit scores the artifact and records that it cannot support trend findings; a comparison needs enough comparable artifacts to support the trend claimed.

**Acceptable evidence:** The artifacts themselves, plus any source materials or context that informed them.

**Insufficient evidence:** If artifacts are drafts with placeholder sections, note "Scoring deferred, artifact incomplete" for those entries rather than scoring partial work as weak.

**Hypotheses vs. findings:**
- **Findings:** Scores grounded in specific evidence from the artifact (e.g., "Actionability 4, no owner named in Decision Frame")
- **Hypotheses:** Trend attributions with small sample sizes, label "Directional, N=2, confirm over next cycle" when the audit set is fewer than 4 artifacts

## Output Format

Produce a **Quality Audit Report** with:
1. **Audit Set**, artifacts reviewed, types, dates, producing workflows
2. **Scores Table**, per-artifact scores on each dimension with totals and bands
3. **Trend Observations**, declining, stable, or improving per dimension; strongest and weakest patterns
4. **Recommendations**, 3-5 specific actions tied to failure modes and recovery playbooks

**Shipwright Signature (required closing):**
5. **Decision Frame**, Primary quality finding, trade-off (invest in fixing weakest dimension vs. maintain current trajectory), confidence with sample size caveat, owner, decision date, revisit trigger (next audit cycle)
6. **Unknowns & Evidence Gaps**, Artifacts not included in the audit, dimensions not scored due to missing artifact-specific evals, sample size limitations
7. **Pass/Fail Readiness**, PASS if every reviewed artifact is scored on all 4 universal dimensions with evidence-backed rationales, and any trend claim is supported by comparable artifacts. A single-artifact audit may PASS without a trend claim when it states that limitation. FAIL if scores lack rationales or trends are asserted without cross-artifact comparison.
8. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Scoring without rationale**, A score of "Clarity: 7" means nothing without citing what made it a 7 and not a 6 or 8
- **Blaming the agent for PM input quality**, If an artifact is weak because the PM provided no evidence, note that as context rather than scoring the agent down
- **Treating one weak artifact as a trend**, Two data points is not a trend; label small-sample observations as directional
- **Averaging across artifact types**, A PRD and a competitive landscape have different quality profiles; compare like with like when possible
- **Recommending "try harder"**, Every recommendation must name the specific dimension, the specific failure mode, and a concrete fix

## Weak vs. Strong Output

**Weak:**
> "Overall quality is decent. Some artifacts could be stronger on completeness. Recommend continuing current approach with minor improvements."

No scores, no specific evidence, no trend data, no actionable recommendation.

**Strong:**
> "Actionability declined across the last 3 PRDs (7 → 5 → 4). Common pattern: Decision Frames name an owner but omit a decision date and revisit trigger, making it unclear when to act. This matches the 'missing kill criteria' failure mode in docs/failure-modes.md (Strategy Planner section). Recommendation: add explicit Decision Frame completeness check to /write-prd Step 5 review pass."

Specific dimension, quantified trend, root cause identified, failure mode referenced, and a concrete fix proposed.
