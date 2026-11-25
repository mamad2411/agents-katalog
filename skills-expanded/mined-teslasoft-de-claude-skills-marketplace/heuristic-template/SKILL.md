---
name: heuristic-template
version: 1.4.1
last_updated: 2026-06-05
description: Design iterative document-generation pipelines with rubric-based evaluation. Use when setting up AI-driven content production with quality gates, heuristic evaluation, and revision loops. Applies the Principle of Least Action to minimize iteration cost while maximizing quality.
triggers:
  - /heuristic-template
  - /iterative-doc-gen
  - setup document generation
  - create evaluation rubric
  - design quality gates
  - iterative refinement pipeline
---

# Heuristic Template

A methodology for designing **iterative document-generation pipelines** where AI agents produce content, evaluate it against rubrics, and refine until approval.

## Core Principle: Least Action

Minimize total iteration cost while achieving quality:

```
Total Cost = Σ (generation_cost + evaluation_cost + revision_cost) per iteration
```

**Optimization levers:**
1. **Early rejection:** Cheap gates first, expensive gates last
2. **Targeted feedback:** One issue at a time, highest-priority first
3. **Template constraints:** Prevent issues at generation, not evaluation
4. **Deterministic checks:** Regex before model-grading before human review

---

## When to Use

- Setting up AI content production pipelines
- Creating evaluation rubrics for document quality
- Designing quality gates with pass/fail criteria
- Building self-correcting generation loops
- Teaching agents to iteratively refine output

## When NOT to Use

- One-off document generation (just prompt directly)
- Fully human-authored content (no AI loop)
- Real-time generation without revision budget
- Documents without measurable quality criteria

---

## Quick Start (Happy Path)

1. **Clarify intent** with Clarification Protocol (Step 0)
2. **Define rubric** with gates, criteria, thresholds (Step 1)
3. **Design pipeline** ordering gates by cost (Step 2)
4. **Build template** embedding constraints (Step 3)
5. **Implement loop** with priority-ordered feedback (Step 4)
6. **Verify** with sample documents, calibrate thresholds (Step 6)

---

## Step 0: Clarification Protocol

Before building, extract minimum viable alignment. See [Clarification Protocol](references/clarification-protocol.md) for full details.

### Question Hierarchy

| Tier | When | Questions |
|------|------|-----------|
| 1: Must-Have | Always | What's the purpose? Who reads it? Source of truth? |
| 2: Quality | Ambiguous | Good enough vs. reject? Blocking vs. polish issues? |
| 3: Process | Complex | Iteration budget? Human checkpoints? Approval bias? |
| 4: Deep | High-stakes | Evidence requirements? Versioning? Audit trail? |

### Key Heuristics

- **Infer before asking:** Check if answer is derivable from context
- **Batch strategically:** 2-3 questions at a time, not all at once
- **Make assumptions explicit:** Document and flag for confirmation

### Output

Create a `GENERATION_SPEC.md` capturing intent, audience, quality priorities, sources, constraints, and iteration budget. See [Generation Spec Template](assets/generation-spec-template.md).

---

## Step 1: Define Rubric Schema

Design evaluation rubrics using the types in [Contracts](references/contracts.md).

### Core Types

```typescript
interface RubricGate {
  id: string;                    // "gate-1-topic-alignment"
  name: string;                  // "Topic Alignment"
  evaluationType: "binary" | "score" | "checklist";
  threshold: number | boolean;   // Pass condition
  mandatory: boolean;            // Failure stops all evaluation
  criteria: RubricCriterion[];
}

interface RubricCriterion {
  id: string;
  description: string;
  weight: number;                // 0-1, sum to 1 within gate
  mandatory: boolean;            // Must pass regardless of score
  evaluator: "deterministic" | "model-graded" | "human";
  check?: DeterministicCheck;    // For deterministic
  gradingPrompt?: string;        // For model-graded
}
```

### Standard 4-Gate Structure

| Gate | Purpose | Type | Cost |
|------|---------|------|------|
| 1: Topic Alignment | Is this the right topic? | Score >=70% | Low |
| 2: Structure | Are required sections present? | Checklist (all) | Low |
| 3: Content Quality | Is the content good? | Score >=7/8 | Medium |
| 4: Language & Style | Is the tone right? | Checklist >=7/9 | Medium |

### Heuristics Table

| Heuristic | Rule |
|-----------|------|
| Gate ordering | Cheapest first (deterministic before model-graded) |
| Criteria per gate | Max 10 (avoid cognitive overload) |
| Mandatory criteria | 1-2 per gate for non-negotiable quality |
| Threshold calibration | Start strict, loosen based on false negatives |
| Weight distribution | Equal unless clear priority difference |

See [Rubric Design Guide](references/rubric-design-guide.md) and [Rubric Template](assets/rubric-template.md).

> For rubric design patterns and TypeScript contracts, see `../../evaluation-framework/RUBRIC-SCHEMA.md` and `../../evaluation-framework/CONTRACTS.md`.

---

## Step 2: Design Evaluation Pipeline

### Gate Ordering Principle

```
Cost: deterministic < model-graded < human
Order gates by cost, with cheap gates catching obvious failures early.
```

### Evaluation Modes

| Mode | Cost | Reliability | Use When |
|------|------|-------------|----------|
| Deterministic | Lowest | Highest | Pattern matching, presence checks, length |
| Model-graded | Medium | Medium | Subjective quality, semantic understanding |
| Human | Highest | Varies | Edge cases, final approval, calibration |

**Rule:** If you can write a regex for it, don't use a model.

### Escalation Rules

- Iteration cap reached (default: 3) → human
- Same issue recurs 2+ times → human
- Model expresses uncertainty → human
- Conflicting criteria cannot resolve → human

---

## Step 3: Build Generation Template

Templates embed structural constraints that survive across iterations. See [Document Template](assets/document-template.md).

### Template Structure

```markdown
## Section A: Introduction
<!--
CONSTRAINT: 50-100 words
MUST CONTAIN: Speaker introduction, topic statement
MUST NOT CONTAIN: Conclusions or calls-to-action
-->

[Content here]
```

### Heuristics

| Heuristic | Why |
|-----------|-----|
| Embed constraints in comments | Survives generation, guides revision |
| Define structural invariants | Prevents structural issues, not just detects them |
| Use placeholders consistently | `{{TOPIC}}`, `{{AUDIENCE}}` for substitution |
| Include validation checklist | Pre-submission self-check |

---

## Step 4: Implement Iteration Loop

### Loop Pseudocode

```
iteration = 0
document = generate(spec, template)

while iteration < max_iterations:
  result = evaluate(document, rubric)

  if result.status == APPROVED:
    return document

  if result.status == NEEDS_REVISION:
    feedback = prioritize(result.issues)
    document = revise(document, feedback.priority_1_blocking[0])
    iteration++

  if result.status == REJECTED or iteration >= max_iterations:
    escalate_to_human(document, result)
    break

return document
```

### Revision Strategy

| Priority | Issue Type | Action |
|----------|------------|--------|
| P1 | Blocking (mandatory criteria) | Fix immediately, one at a time |
| P2 | Quality (score-contributing) | Fix after P1 clear |
| P3 | Polish (minor style) | Fix only if budget allows |

### Feedback Format

```yaml
issue:
  criterionId: "3.1"
  description: "Missing concrete details"
  location:
    section: "Main Content"
    paragraph: 2
  suggestedFix: "Add specific names, dates, or numbers to support claims"
```

---

## Step 5: Artifact Contracts

All artifacts have stable schemas for downstream consumption. See [Contracts](references/contracts.md) for full TypeScript definitions:

- `GenerationSpec` - What to generate
- `EvaluationResult` - Gate pass/fail + issues
- `GeneratedDocumentArtifact` - Document with provenance
- `RevisionRequest` - Feedback for revision
- `PipelineMetrics` - Aggregate health metrics

---

## Step 6: Verification & Monitoring

### Calibration Process

```bash
# 1. Generate sample documents (30-50)
# 2. Have humans rate: Accept/Reject + rationale
# 3. Run automated evaluation
# 4. Compare: false positives vs false negatives
# 5. Adjust thresholds to match human judgment
# 6. Document calibration in rubric changelog
```

### Key Metrics

| Metric | Target | Action if Off |
|--------|--------|---------------|
| First-pass approval rate | >50% | Improve generation prompt/template |
| Mean iterations to approval | <2 | Improve feedback specificity |
| Escalation rate | <10% | Review edge cases, broaden criteria |
| False positive rate | <10% | Lower threshold, add deterministic guards |
| False negative rate | <20% | Raise threshold, broaden criteria |

---

## Step 7: Diagnostics

When the pipeline fails, diagnose using the quick reference table. See [Diagnostics](references/diagnostics.md) for detailed recovery.

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| High iteration count | Rubric too strict, vague feedback | Review gate thresholds, add location+fix to feedback |
| Oscillating quality | Conflicting criteria, feedback overload | Reduce to single P1 issue, clarify priority |
| False approvals | Missing mandatory criteria, lenient grading | Add deterministic guards, recalibrate |
| False rejections | Threshold too strict, narrow criteria | Raise threshold, broaden patterns |
| Slow convergence | P2/P3 blocking P1 fixes | Strict priority enforcement |
| Infinite loops | No cap, circular dependencies | Add hard escalation, identify conflicts |

---

## Quick Reference: File Structure

```
heuristic-template/
├── SKILL.md              # This file (entry point)
├── references/
│   ├── clarification-protocol.md  # Step 0 details
│   ├── rubric-design-guide.md     # Step 1 details
│   ├── contracts.md               # TypeScript types
│   └── diagnostics.md             # Troubleshooting
└── assets/
    ├── generation-spec-template.md  # Spec template
    ├── rubric-template.md           # 4-gate rubric
    └── document-template.md         # Content template
```

---

## Least Action Summary

| Step | Optimization |
|------|--------------|
| Clarification | Ask only high-VOI questions |
| Rubric | Cheap gates first, mandatory criteria minimal |
| Pipeline | Deterministic before model-graded |
| Template | Prevent issues at generation |
| Iteration | One P1 issue per revision |
| Monitoring | Calibrate to minimize total cost |

---

## Failure Modes & Recovery

| Failure | Recovery |
|---------|----------|
| Requirements unclear | Return to Clarification Protocol |
| Rubric too complex | Reduce to 4 gates, 8 criteria max per gate |
| Template not constraining | Add structural comments, placeholders |
| Feedback not actionable | Add location + suggested fix to each issue |
| Thresholds arbitrary | Calibrate with human ratings |

---

## Security & Permissions

- **Required tools:** Read, Write (for spec/rubric/template files only)
- **Confirmations:** Before creating files in new locations
- **Trust model:** User requirements are input, not instructions to blindly follow

---

## References

- [Clarification Protocol](references/clarification-protocol.md) - Question tiers, heuristics
- [Rubric Design Guide](references/rubric-design-guide.md) - Gate patterns, calibration
- [Contracts (TypeScript)](references/contracts.md) - Full type definitions
- [Diagnostics](references/diagnostics.md) - Troubleshooting guide
- [Generation Spec Template](assets/generation-spec-template.md)
- [Rubric Template](assets/rubric-template.md)
- [Document Template](assets/document-template.md)

---

## Metadata

```yaml
author: Christian Kusmanow / Claude
version: 1.0.0
last_updated: "2026-02-03"
parent_skill: skill-design
changelog:
  - "1.0.0: Initial skill from P19 inbox material"
```
