---
name: agent-eval-framework
description: Evaluate AI agent outputs systematically using rubrics, assertions, and reference comparisons. Detect quality drift over time.
version: "1.0.0"
last-updated: "2026-04-17"
model_tested: "claude-sonnet-4-6"
category: eval
platforms: [claude-code, codex, gemini-cli, cursor, copilot, windsurf, cline]
language: en
geo_relevance: [global]
priority: high
dependencies:
  mcp: []
  skills: []
  apis: []
  data: []
update_sources:
  - url: "https://arxiv.org/abs/2603.28052"
    check_frequency: "quarterly"
    last_checked: "2026-04-21"
license: MIT
---

# Agent Evaluation Framework

## When to Use

- Before deploying an agent to production
- After changing an agent's system prompt or skills
- When agent output quality seems to degrade
- During periodic quality reviews
- When comparing two agent configurations

## Step 1: Define Evaluation Criteria

Choose criteria relevant to your agent's purpose:

### Universal Criteria
| Criterion | Question | Score |
|-----------|----------|-------|
| Correctness | Is the output factually/technically correct? | 0-10 |
| Completeness | Does it cover all required aspects? | 0-10 |
| Relevance | Is every part relevant to the request? | 0-10 |
| Safety | Does it avoid harmful/insecure patterns? | 0-10 |

### Code-Specific Criteria
| Criterion | Question | Score |
|-----------|----------|-------|
| Functionality | Does the code work as intended? | 0-10 |
| Edge Cases | Are edge cases handled? | 0-10 |
| Style | Does it match project conventions? | 0-10 |
| Security | Are there vulnerabilities? | 0-10 |

### Content-Specific Criteria
| Criterion | Question | Score |
|-----------|----------|-------|
| Accuracy | Are claims supported by evidence? | 0-10 |
| Tone | Does it match the intended audience? | 0-10 |
| Structure | Is it well-organized? | 0-10 |
| Originality | Does it avoid generic/cliche content? | 0-10 |

## Step 2: Choose Evaluation Method

### A. Assertion-Based (Automated)
Define pass/fail conditions:
```
ASSERT: output contains "disclaimer"
ASSERT: output does NOT contain "TODO"
ASSERT: code compiles without errors
ASSERT: response length < 2000 tokens
ASSERT: no PII detected in output
```
Best for: Regression testing, CI/CD pipelines.

### B. Reference-Based (Semi-Automated)
Compare output against a known-good reference:
- Exact match (strict)
- Semantic similarity (using embeddings)
- Key-point coverage (checklist)

Best for: Consistent tasks with known expected outputs.

### C. Rubric-Based (Human + AI)
Score each criterion 0-10 with justification:
```
Correctness: 8/10 — Accurate but missed one edge case
Completeness: 7/10 — Covered 5 of 6 required points
Safety: 10/10 — No security issues
TOTAL: 25/30 (83%) — PASS (threshold: 70%)
```
Best for: Complex, subjective outputs.

## Step 3: Run Evaluation

1. Prepare 5-10 test cases covering:
   - Happy path (normal usage)
   - Edge cases (unusual inputs)
   - Adversarial inputs (injection, confusion)
   - Empty/minimal inputs
   - Maximum complexity inputs

2. Run each test case through the agent
3. Apply chosen evaluation method
4. Record results with timestamps

## Step 4: Set Thresholds

| Level | Score | Action |
|-------|-------|--------|
| Excellent | >= 90% | Ship |
| Good | 70-89% | Ship with monitoring |
| Marginal | 50-69% | Fix before shipping |
| Failing | < 50% | Do not ship |

## Step 5: Monitor Drift

Track these metrics over time:
- Average score per criterion (weekly)
- Pass rate on test suite (per deployment)
- Token cost per task (per session)
- User satisfaction signals (if available)

Drift signals:
- Score drops >10% week-over-week
- Pass rate drops below threshold
- Token cost increases >20% without scope change
- New failure modes not in original test suite

## Output Format

```
AGENT EVAL REPORT
Agent: {name}
Date: {ISO-8601}
Test cases: {n}
Method: {assertion|reference|rubric}

Results:
  Pass: {n} ({%})
  Fail: {n} ({%})
  Average score: {x}/10

Per-criterion:
  Correctness:  {x}/10
  Completeness: {x}/10
  Safety:       {x}/10

Verdict: {PASS|MARGINAL|FAIL}
Recommendation: {ship|fix|block}
```

## What This Skill Does NOT Do

- Does not test the LLM model itself (tests agent in context)
- Does not perform adversarial red-teaming (different discipline)
- Does not replace user feedback (complements it)
- Does not measure latency or throughput (APM tools do this)
