---
name: agent-evals
description: |
  Design and implement evaluation frameworks for AI agents.
  This skill should be used when testing agent reasoning quality, building
  graders, performing error analysis, establishing regression protection,
  debating whether a prompt change improved things, or deciding which agent
  component to improve next.
---

# Agent Evaluations

Guide for building systematic evaluation frameworks that measure and improve AI agent quality.

## What This Skill Does

- Design evaluation datasets (Typical/Edge/Error categories)
- Classify eval criteria using the Four Quadrants framework
- Build graders (code-based, LLM-judged, combined)
- Perform systematic error analysis to find failure patterns
- Set up regression protection with per-criterion tracking
- Guide the complete quality loop from prototype to production
- Optimize agent cost/latency after quality is established

## What This Skill Does NOT Do

- Execute evaluations at runtime or benchmark specific models
- Integrate with specific observability platforms (Datadog, LangSmith, etc.)
- Handle data privacy/compliance for eval datasets
- Provide SDK-specific code (OpenAI, Anthropic, Google ADK adapters)
- Deploy or host evaluation infrastructure

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing agent code, test infrastructure, CI/CD setup |
| **Conversation** | User's agent type, framework, quality goals |
| **Skill References** | Domain patterns from `references/` (graders, error analysis, datasets) |
| **User Guidelines** | Project conventions, team standards, deployment environment |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

---

## Required Clarifications

Ask about the USER'S context (not eval methodology):

1. **Agent type**: "What does your agent do?" (customer support, code generation, research, etc.)
2. **Current state**: "Do you have existing test data or production logs?"
   - Yes, production logs available -> Mine real data for dataset
   - Yes, some test cases exist -> Build on existing cases
   - No, starting from scratch -> Create synthetic dataset first

## Optional Clarifications

Ask if relevant, otherwise use defaults:

3. **Framework**: "What agent framework/SDK are you using?" (Default: framework-agnostic Python)
4. **Domain stakes**: "Is this high-stakes, standard, or experimental?" (Default: standard, 5% threshold)

### If User Skips Clarifications

- **Agent type**: Proceed with general-purpose agent patterns
- **Current state**: Assume starting from scratch, create synthetic dataset
- **Framework**: Use framework-agnostic Python examples
- **Domain stakes**: Default to Standard (5% drop threshold)

---

## Workflow

Follow this sequence when implementing an eval framework:

```
1. Classify Criteria (Four Quadrants)
2. Design Dataset (Typical/Edge/Error)
3. Build Graders (matched to quadrant)
4. Establish Baseline
5. Analyze Errors (systematic counting)
6. Fix Lowest Component (one change at a time)
7. Re-run Evals + Check Regressions
8. Ship Decision
```

For the full 10-step production workflow including deployment and monitoring, see `references/quality-loop.md`.

---

## Key Concepts

### Evals vs TDD

| Aspect | TDD (Code Testing) | Evals (Agent Evaluation) |
|--------|-------------------|-------------------------|
| Core Question | "Does it work?" | "Did it decide correctly?" |
| Outcome | PASS or FAIL (deterministic) | Scores (probabilistic) |
| Correct Answers | Exactly one | Range of acceptable responses |

**Decision**: "Is there exactly one correct answer?" Yes -> TDD. No (range of acceptable answers requiring judgment) -> Evals.

Gray area: "Did the agent call the right API?" might have one correct answer in simple cases, but when multiple APIs could work, you need evals.

### The Four Quadrants

Every eval criterion exists along two axes: **Scoring Method** (Objective vs Subjective) and **Reference Data** (Ground Truth vs No Ground Truth).

```
                    | Ground Truth Available | No Ground Truth |
--------------------+-----------------------+-----------------+
Objective           |        Q1 [preferred] |       Q3        |
(Code-checkable)    |   Fastest, Cheapest   |   Fast, Cheap   |
--------------------+-----------------------+-----------------+
Subjective          |        Q2             |       Q4        |
(LLM-judged)        |      Moderate         | Most Expensive  |
--------------------+-----------------------+-----------------+
```

**Q1: Objective + Ground Truth** - Code verifies outputs match expected answers. Examples: date extraction, JSON schema validation, exact tool call verification.

**Q2: Subjective + Ground Truth** - LLM judges assess semantic coverage against reference. Examples: summaries covering key points, reports including required findings.

**Q3: Objective + No Ground Truth** - Code checks constraints without correct answers. Examples: "response under 500 tokens", "no PII detected", "valid JSON".

**Q4: Subjective + No Ground Truth** - LLM judges evaluate quality via rubrics. Examples: response helpfulness, explanation clarity, appropriate tone.

### Quadrant Decision Tree

```
1. Can you obtain ground truth for test cases?
   |
   +-- YES --> 2a. Can code verify success deterministically?
   |                |
   |                +-- YES --> Q1 (Use code grader with expected outputs)
   |                +-- NO ---> Q2 (Use LLM judge with reference comparison)
   |
   +-- NO ---> 2b. Can code check the constraint?
                    |
                    +-- YES --> Q3 (Use code grader with constraint check)
                    +-- NO ---> Q4 (Use LLM judge with rubric)
```

**Priority**: Q1 > Q3 > Q2 > Q4. The cheapest reliable eval is the best eval.

### Good Example

"Did the agent return valid JSON?" -> Q1 (code grader). Deterministic, zero cost, instant.

### Bad Example (Avoid)

"Did the agent return valid JSON?" -> Q4 (LLM judge with rubric). Wastes LLM calls on a code-checkable criterion, introduces noise where none is needed.

---

## Graders (Quick Reference)

Graders are functions that score agent outputs. Match grader type to quadrant.

**Code-Based (Q1, Q3)** - Dictionary of boolean checks, sum-based scoring:
```python
checks = {
    "has_required_fields": all(f in output for f in expected["fields"]),
    "valid_json": is_valid_json(output),
    "within_length": len(output) <= expected.get("max_length", 1000),
}
score = sum(checks.values()) / len(checks)
```

**LLM-Based (Q2, Q4)** - 5-7 binary YES/NO questions, count affirmatives:
```python
# Decompose quality into specific yes/no questions:
# 1. Does the response directly address the user's request?
# 2. Is the information factually consistent with the reference?
# ... (5-7 total)
# Score = count(YES) / total_questions
```

**Combined** - Code checks first (fail fast), then LLM only if structural checks pass.

For full grader patterns, templates, validation, and pairwise comparison guidance, see `references/graders.md`.

---

## Dataset Design (Quick Reference)

Start with 10-20 cases using the three-category framework:

| Category | Count | Purpose | Pass Rate Target |
|----------|-------|---------|------------------|
| Typical | 10 | Common use cases (80% of real usage) | 90%+ |
| Edge | 5 | Unusual but valid scenarios | 70-80% |
| Error | 5 | Out-of-scope or impossible requests | Fail gracefully |

Each case: `{"input": "...", "expected": "...", "rationale": "why this case exists"}`

Prefer real production data over synthetic. Grow dataset organically from production failures.

For full dataset design, mining real data, and growth strategy, see `references/dataset-design.md`.

---

## Error Analysis (Quick Reference)

Systematic counting beats intuition. Thirty minutes tabulating errors outperforms thirty hours fixing the wrong component.

1. Tabulate failures by component using the spreadsheet method
2. Count occurrences - let percentages emerge from data
3. Prioritize: **Priority = Frequency x Feasibility**
4. Fix the single highest-priority component
5. Re-run evals to verify improvement

Trace errors to root cause. A component might fail because it receives degraded input upstream, not because it's broken.

For full methodology, failure modes, and implementation code, see `references/error-analysis.md`.

---

## Regression Protection (Quick Reference)

Aggregate improvements can mask critical per-criterion regressions.

1. **Baseline before changes** - Capture performance before any modification
2. **Compare per-criterion** - Track every criterion independently, not just aggregate
3. **Apply domain thresholds** - High-stakes: any drop. Standard: 5%. Experimental: 10%
4. **Decide explicitly** - Accept tradeoff, revert, or iterate further

```python
# Always compare to captured baseline, never to memory
regression_report = detect_regressions(
    baseline=baseline_results["by_criterion"],
    current=current_results["by_criterion"],
    threshold_config={"drop_threshold": 0.05}
)
```

For full detection code, CI/CD integration, and threshold configuration, see `references/regression-protection.md`.

---

## Cost Optimization (Quick Reference)

Optimize in strict order: **Quality -> Latency -> Cost**. Never reverse.

1. Achieve quality threshold with most capable model (e.g., claude-opus-4)
2. Reduce latency while maintaining quality (shorter prompts, parallel calls, caching)
3. Reduce cost while maintaining quality + latency (smaller models, reduced context)

Starting with cheap models wastes effort engineering around capability gaps. Establish quality ceiling first, then trade down.

For full optimization phases and implementation, see `references/cost-optimization.md`.

---

## Varies vs Constant

| Varies (ask user) | Constant (encode in skill) |
|--------------------|----------------------------|
| Agent framework/SDK | Eval methodology (quadrants, graders, analysis) |
| Specific eval criteria | Grader design principles |
| Quality thresholds | Error analysis approach (counting, prioritization) |
| Tech stack (Python, TS) | Regression detection logic |
| CI/CD platform | Dataset design framework (Typical/Edge/Error) |
| Domain (medical, support) | Cost optimization sequence (Quality > Latency > Cost) |

---

## Output Checklist

Before delivering an eval framework, verify:

### Dataset
- [ ] 10-20 cases covering Typical/Edge/Error categories
- [ ] Cases include input, expected criteria, and rationale
- [ ] Real production data used where available

### Graders
- [ ] Each criterion classified into correct quadrant (Q1-Q4)
- [ ] Grader type matches quadrant (code-based for Q1/Q3, LLM for Q2/Q4)
- [ ] Graders tested against real agent responses (not mock data)
- [ ] Standardized output format (passed, score, checks, failed_checks)

### Baseline and Regression
- [ ] Baseline captured before any changes
- [ ] Per-criterion tracking configured (not just aggregate)
- [ ] Domain-appropriate thresholds set
- [ ] CI/CD integration outlined (if applicable)

### Error Analysis
- [ ] Failure tabulation method in place
- [ ] Prioritization formula defined (frequency x feasibility)
- [ ] Root cause attribution traces to component level

---

## Official Documentation

| Resource | URL | Use For |
|----------|-----|---------|
| Anthropic - Demystifying Evals | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | Agent eval concepts, graders, harnesses |
| OpenAI - Evaluation Best Practices | https://platform.openai.com/docs/guides/evaluation-best-practices | Eval design patterns, data sources, graders |
| OpenAI - Agent Evals | https://platform.openai.com/docs/guides/agent-evals | Agent-specific evaluation guidance |
| OpenAI Evals API | https://platform.openai.com/docs/api-reference/evals | Programmatic eval configuration |
| Hamel Husain - LLM Evals FAQ | https://hamel.dev/blog/posts/evals-faq/ | Practical eval methodology, error analysis |
| Hamel Husain - LLM-as-Judge | https://hamel.dev/blog/posts/llm-judge/ | LLM judge design, validation against humans |
| Braintrust Docs | https://www.braintrust.dev/docs | Eval platform, CI/CD integration, scoring |
| DeepLearning.AI - Agentic AI | https://www.deeplearning.ai/courses/agentic-ai/ | Andrew Ng's course on agent design patterns and evals |

For patterns not covered in this skill, fetch from the official sources above.

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/graders.md` | Building graders, LLM judge prompts, grader validation, pairwise comparison |
| `references/error-analysis.md` | Analyzing failures, prioritizing fixes, failure mode categorization |
| `references/dataset-design.md` | Designing eval datasets, mining real data, growth strategy |
| `references/regression-protection.md` | Baseline comparison, per-criterion detection, CI/CD, thresholds |
| `references/quality-loop.md` | Full 10-step workflow, ship decisions, deployment safeguards, monitoring |
| `references/cost-optimization.md` | Quality -> Latency -> Cost optimization phases |

---

*Methodology last verified: 2026-02. Based on Andrew Ng's evaluation-driven development framework, Anthropic's agent eval patterns, and Hamel Husain's practical eval methodology.*
