---
name: apply-rubric
description: >
  Apply an EAROS rubric to an architecture artifact using the three-pass agent
  evaluation pattern (Extractor, Evaluator, Challenger). Use this skill whenever
  the user wants to "evaluate an architecture artifact", "apply a rubric",
  "review an architecture document", "score an architecture artifact",
  "run an EAROS evaluation", "assess architecture quality", "apply the
  solution architecture rubric", "evaluate this ADR", "review this capability
  map", "check this against the rubric", "run the architecture review",
  or mentions "evaluate", "score", "assess", "review", or "apply rubric"
  in the context of applying an EAROS rubric to a specific artifact.
  Also triggers when the user says "how does this artifact score",
  "is this architecture document good enough", "run the three-pass evaluation",
  "extract evidence from this document", or any request to systematically
  evaluate a specific architecture work product against defined criteria.
  Does NOT trigger for creating rubrics (use earos-rubric for that), general
  architecture modeling, or diagram creation.
---

# EAROS Rubric Evaluator

You are applying an EAROS rubric to an architecture artifact using the three-pass agent evaluation pattern. This pattern exists because architecture review is vulnerable to confident but weak inference — a single reviewer (human or agent) can score an artifact favorably because the prose *sounds* comprehensive, without noticing thin evidence or internal contradictions. The three-pass model catches this.

## The three passes

| Pass | Agent role | Purpose | Why it's separate |
|------|-----------|---------|-------------------|
| **1. Extractor** | Evidence finder | Read the artifact and extract candidate evidence for each criterion | Separating extraction from judgment prevents confirmation bias — the extractor finds what's there (and what's not) without the pressure of assigning a score |
| **2. Evaluator** | Scorer | Apply rubric criteria to the extracted evidence, assign scores, rationale, confidence | Scoring with pre-extracted evidence is more disciplined than scoring while reading — the evaluator can focus on judgment rather than hunting |
| **3. Challenger** | Adversarial reviewer | Challenge the evaluation for unsupported claims, over-scoring, missed gaps, rubric misuse | The challenger catches the evaluator's blind spots — disagreements surface the ambiguous cases that need human attention |

Read `references/agent-prompts.md` for the full prompt templates for each agent. Read `references/evaluation-schema.md` for the exact output format.

## How to interact with the user

This skill requires input from the user before evaluation can begin. You must **stop and wait for the user's response** after each question — use whatever mechanism your agent platform provides for soliciting user input (e.g., a question tool, a prompt, a form). Do not just print questions as text and continue generating; that skips the user's answer entirely.

## How to run this skill

### Step 0: Gather inputs

You need two things from the user. Stop and ask for each one, waiting for a response before proceeding.

**First, stop and ask the user for the rubric:**

> Which EAROS rubric should I apply? Please provide the file path to the rubric YAML file (profile or overlay).
>
> If you're not sure, tell me the artifact type (e.g., solution architecture, ADR, capability map) and I'll check for a matching rubric in the repository.

If the user mentions an artifact type but no rubric, check the `tmp/profiles/` and `tmp/overlays/` directories for a matching EAROS rubric. If none exists, suggest they create one first using the `earos-rubric` skill.

**Then, stop and ask the user for the artifact:**

> Which architecture artifact should I evaluate? Please provide the file path(s). This could be a markdown file, a PDF, a Word document, or a collection of files.

**Then, stop and ask for metadata:**

> A few more details for the evaluation record:
> - **Artifact ID and title** — a short identifier and human-readable name
> - **Artifact owner** — who is responsible for this artifact
> - **Additional overlays** — should I apply any cross-cutting overlays (security, data, regulatory) in addition to the profile?
>
> (If you're unsure about any of these, just say so and I'll use reasonable defaults.)

### Step 1: Load and compose the rubric

Read the rubric YAML file. If it has `inherits: [EAROS-CORE-001@1.0.0]`, also load the core meta-rubric from `tmp/profiles/core-meta-rubric.v1.yaml`. Compose the full criterion set by merging:

1. All criteria from the core meta-rubric
2. All criteria from the artifact profile
3. All criteria from any attached overlays

Build a complete criterion list with all fields: id, question, required_evidence, scoring_guide, gate configuration, anti_patterns.

### Step 2: Assess artifact scope and plan agent strategy

Read the artifact to estimate its scope. Consider:

- **Number of sections/chapters** — more sections means more evidence to extract
- **Number of diagrams or views** — each needs separate analysis
- **Number of criteria to evaluate** — core (9-10) + profile-specific + overlay criteria
- **Artifact length** — longer artifacts benefit from parallel extraction

Based on this assessment, decide the agent strategy:

**Standard strategy** (artifact < ~50 pages, < 15 total criteria):
- 1 extractor agent
- 1 evaluator agent
- 1 challenger agent

**Parallel strategy** (artifact is comprehensive — many sections, many criteria, or > ~50 pages):
Split the criteria into groups and run multiple evaluator agents in parallel. Each evaluator handles a subset of dimensions. This reduces the risk of evaluator fatigue (where later criteria get less attention) and speeds up the evaluation.

Partition criteria by dimension for the parallel split — keep all criteria within the same dimension together so the evaluator can assess coherence within the dimension.

Tell the user which strategy you're using and why.

### Step 3: Run Pass 1 — Extractor

Spawn an extractor agent with the following task. The extractor must NOT score — it only extracts evidence.

Use the Agent tool to spawn a subagent with the prompt from `references/agent-prompts.md` Section "Extractor prompt". Provide:
- The full artifact content (read all artifact files)
- The complete criterion list with required_evidence fields
- Instructions to produce a structured evidence map

The extractor returns a JSON/YAML evidence map:
```yaml
evidence_map:
  - criterion_id: STK-01
    evidence_found:
      - location: "Section 1.2 Audience"
        excerpt: "This document is intended for the architecture board and engineering leads."
        evidence_class: observed
      - location: "Section 1.3 Purpose"
        excerpt: "The purpose is to gain approval for the proposed integration approach."
        evidence_class: observed
    evidence_gaps:
      - "No stakeholder-concern mapping found"
      - "Decision context not explicitly stated"
    evidence_sufficiency: partial
```

Wait for the extractor to complete before proceeding.

### Step 4: Run Pass 2 — Evaluator(s)

Spawn one or more evaluator agents using the prompt from `references/agent-prompts.md` Section "Evaluator prompt". Provide each evaluator with:
- The rubric criteria assigned to it (all criteria if single evaluator, a dimension-group if parallel)
- The evidence map from the extractor (filtered to relevant criteria)
- The scoring guidance from the rubric

**If using parallel strategy:** Spawn all evaluator agents simultaneously using the Agent tool. Each evaluator handles a distinct set of dimensions, so there are no dependencies between them.

Each evaluator returns criterion results:
```yaml
criterion_results:
  - criterion_id: STK-01
    score: 3
    judgment_type: observed
    confidence: high
    evidence_sufficiency: sufficient
    evidence_refs:
      - location: "Section 1.2 Audience"
        excerpt: "Architecture board and engineering leads are named."
    rationale: >
      Stakeholders are explicitly named and the decision purpose is clear.
      Minor gap: concerns are not systematically mapped to views.
    missing_information:
      - "Concern-to-view matrix"
    recommended_actions:
      - "Add stakeholder-concern-view table"
```

Collect results from all evaluators. If parallel, merge the criterion_results arrays.

### Step 5: Run Pass 3 — Challenger

Spawn a challenger agent using the prompt from `references/agent-prompts.md` Section "Challenger prompt". Provide:
- The original artifact content
- The evidence map from the extractor
- The complete evaluation results from the evaluator(s)
- The rubric criteria and scoring guidance

The challenger reviews each criterion result and produces challenges:
```yaml
challenges:
  - criterion_id: STK-01
    original_score: 3
    challenge_type: potential_over_score
    argument: >
      The evaluator scored 3 based on named stakeholders, but the
      scoring guide requires "explicit and mostly complete" for a 3.
      No concern mapping exists, which is a significant gap for
      the "mostly complete" threshold.
    suggested_score: 2
    confidence: medium

  - criterion_id: SOL-02
    original_score: 2
    challenge_type: agreement
    argument: >
      Score of 2 is appropriate. NFRs are stated but architectural
      mechanisms are not described. The critical gate status is
      correctly applied.
    suggested_score: 2
    confidence: high
```

### Step 6: Reconcile and compute final results

After the challenger completes, reconcile the evaluation:

1. **Review each challenge.** Where the challenger disagrees with the evaluator:
   - If the challenger's argument is well-reasoned and evidence-based, adopt the challenger's suggested score
   - If the challenge is weak or speculative, keep the original score
   - Note all material disagreements in the evaluation record — these signal areas where human review is especially valuable

2. **Check gates.** For each criterion with a gate:
   - `critical` gate: if score < threshold specified in failure_effect → status cannot be better than `reject`
   - `major` gate: if score < threshold → status cannot be better than `conditional_pass`
   - Collect all gate failures

3. **Compute dimension scores.** For each dimension, compute the weighted average of its criteria (excluding N/A criteria from the denominator).

4. **Compute overall score.** Weighted average of all dimension scores.

5. **Determine status** using the EAROS thresholds:
   - **Pass**: no critical gate failures, overall >= 3.2, no dimension < 2.0
   - **Conditional pass**: no critical gate failures, overall 2.4-3.19 or one weak dimension
   - **Rework required**: overall < 2.4 or repeated weak dimensions
   - **Reject**: critical gate failure or mandatory control breach
   - **Not reviewable**: evidence insufficient for core gate criteria

6. **Flag for human review** when:
   - Any critical gate fails
   - Confidence is low on a gated criterion
   - Status changes due to challenger disagreement
   - Overall confidence is low
   - The artifact is marked as high-risk or customer-facing

### Step 7: Produce the evaluation record

Generate a YAML evaluation record conforming to the schema in `references/evaluation-schema.md`. The record must include:

- `evaluation_id`: Generate as `EVAL-{RUBRIC_PREFIX}-{NNNN}` (e.g., EVAL-SOL-0001)
- `rubric_id` and `rubric_version`: from the rubric file
- `artifact_ref`: id, title, type, owner, uri from user input
- `evaluation_date`: today's date
- `evaluators`: list all agents used (extractor, evaluator(s), challenger)
- `status`: the final determination
- `overall_score`: the computed weighted average
- `gate_failures`: list of failed gate criterion IDs
- `criterion_results`: the reconciled results for every criterion
- `dimension_results`: dimension-level scores and summaries
- `summary`: strengths, weaknesses, risks, next_actions, decision_narrative

Stop and ask the user where to save the evaluation:

> Where should I save the evaluation record? I'll produce both a YAML file (machine-readable) and a markdown report (human-readable). If you don't have a preference, I'll save them next to the artifact or in `tmp/calibration/results/`.

### Step 8: Generate the narrative report

In addition to the machine-readable YAML, produce a human-readable markdown report. Structure it as:

```markdown
# Architecture Evaluation Report

## Artifact
- **Title:** ...
- **Type:** ...
- **Rubric:** ...
- **Date:** ...
- **Status:** ... (with color-coded indicator)

## Executive Summary
[2-3 sentence decision narrative]

## Gate Results
[Table of all gates, pass/fail, with severity]

## Dimension Scores
[Table of dimension scores with traffic-light indicators]

## Criterion Details
[For each criterion: score, confidence, evidence, rationale, gaps, actions]

## Challenger Findings
[Summary of material disagreements and their resolution]

## Recommended Actions
[Prioritized list of improvements]

## Human Review Required
[Flag if any escalation triggers were hit, with reasons]
```

Present this report to the user directly in the conversation, and also save it as a markdown file alongside the YAML record.

### Step 9: Offer next steps

After presenting the results, stop and ask the user what they'd like to do next:

> The evaluation is complete. Here are some options:
> - **Re-evaluate** — if the author addresses the recommended actions, I can re-run the evaluation
> - **Apply additional overlays** — if the evaluation revealed cross-cutting concerns not yet covered (security, data, regulatory)
> - **Calibrate** — have a human reviewer score the same artifact independently so you can compare results and tighten scoring guidance
>
> Would you like to do any of these, or is the evaluation complete?

## Handling edge cases

**Artifact is too short or incomplete to evaluate:**
If the extractor finds evidence is insufficient for more than half the gated criteria, set status to `not_reviewable` and explain why. Don't force scores on thin evidence — that creates false precision.

**Rubric has no profile-specific criteria (core only):**
This is valid — the core meta-rubric alone can evaluate any architecture artifact. Proceed normally with just the 9 core dimensions.

**Multiple overlays requested:**
Apply all overlays. Criteria from different overlays are independent — evaluate them separately and include all in the final record.

**User provides the artifact as multiple files:**
Concatenate or read all files. Tell the extractor agent which content came from which file so evidence references include file names.

**Challenger disagrees on a gate criterion:**
Always flag this for human review regardless of how you reconcile. Gate disagreements are high-stakes and should not be resolved by agents alone.
