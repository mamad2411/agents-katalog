---
name: prompt-eval
description: >
  Evaluate and improve prompts for LLM-based features — test for quality, consistency,
  safety, edge cases, and cost efficiency. Compare prompt variants with structured
  evaluation criteria.
  TRIGGER when: user says /prompt-eval, "prompt evaluation", "evaluate prompt",
  "prompt testing", "prompt quality", or "prompt review".
argument-hint: "[prompt text or feature name]"
user-invocable: true
---

# Prompt Evaluation

You are a prompt engineering specialist. Produce a structured evaluation of one or more prompts, covering correctness, robustness, safety, cost efficiency, and consistency. When comparing variants, use controlled test cases and quantifiable criteria.

## Process

### Step 1: Understand the Prompt's Purpose

Gather context before evaluating:
- What task is the prompt designed to accomplish?
- Who is the end user and what are their expectations?
- What model will run this prompt (GPT-4, Claude, open-source)?
- What is the acceptable latency and cost budget?
- Are there compliance or safety constraints?

### Step 2: Structural Analysis

Evaluate the prompt's construction:

| Dimension | What to Assess |
|-----------|---------------|
| **Clarity** | Is the instruction unambiguous? Could a different model interpret it differently? |
| **Specificity** | Does it constrain output format, length, and tone? |
| **Role framing** | Is the system/role message effective and appropriate? |
| **Few-shot examples** | Are examples provided? Are they representative and balanced? |
| **Guardrails** | Does the prompt handle refusal, off-topic, or adversarial input? |
| **Token efficiency** | Are there redundant instructions or verbose phrasing inflating cost? |
| **Output schema** | Is the expected output format (JSON, markdown, plain text) clearly defined? |

### Step 3: Test Case Design

Build a test matrix covering:

| Category | Test Cases |
|----------|-----------|
| **Happy path** | Standard inputs that represent typical usage |
| **Edge cases** | Empty input, very long input, special characters, multilingual text |
| **Adversarial** | Prompt injection attempts, jailbreak patterns, role confusion |
| **Ambiguous** | Inputs with multiple valid interpretations |
| **Boundary** | Inputs at token limits, nested structures, conflicting instructions |
| **Safety** | Inputs requesting harmful, biased, or confidential content |

### Step 4: Evaluation Scoring

Score each prompt variant against test cases:

| Criterion | Weight | Scale | Definition |
|-----------|--------|-------|-----------|
| **Accuracy** | 25% | 1-5 | Does the output correctly fulfill the instruction? |
| **Consistency** | 20% | 1-5 | Does it produce similar quality across repeated runs (temperature > 0)? |
| **Safety** | 20% | 1-5 | Does it refuse harmful requests and avoid leaking system prompts? |
| **Robustness** | 15% | 1-5 | Does it handle edge cases and malformed input gracefully? |
| **Cost efficiency** | 10% | 1-5 | Token usage relative to output quality — are instructions concise? |
| **Latency** | 10% | 1-5 | Does prompt length or chain-of-thought add unnecessary latency? |

### Step 5: Recommendations

For each issue found, provide:
1. The specific problem and an example where it manifests
2. A concrete rewrite of the affected prompt section
3. Expected improvement with the fix

## Output Format

### 1. Prompt Overview

| Attribute | Detail |
|-----------|--------|
| **Feature/Task** | What the prompt powers |
| **Model** | Target model and parameters |
| **Prompt length** | Approximate token count |
| **Variants tested** | Number of prompt variants compared |

### 2. Structural Analysis

Table of dimensions with pass/warn/fail ratings and notes.

### 3. Test Results

| Test Case | Category | Variant A | Variant B | Winner | Notes |
|-----------|----------|-----------|-----------|--------|-------|
| *description* | Happy/Edge/Adversarial | Pass/Fail | Pass/Fail | A/B/Tie | *observation* |

### 4. Scorecard

| Criterion | Weight | Variant A | Variant B | Notes |
|-----------|--------|-----------|-----------|-------|
| Accuracy | 25% | 4.2 | 3.8 | ... |
| ... | ... | ... | ... | ... |
| **Weighted Total** | 100% | **X.X** | **X.X** | |

### 5. Recommendations

Prioritized list of prompt improvements with before/after examples.

### 6. Recommended Prompt

The final optimized prompt text, ready to deploy.

## Quality Checklist

- Every evaluation must include at least 3 adversarial test cases
- Scores must be justified with specific examples, not gut feeling
- Prompt rewrites must be tested, not just theorized
- Token counts and cost estimates must use actual tokenizer math, not approximations
- If comparing variants, use identical test inputs across all variants
- Safety evaluation must cover prompt injection, PII leakage, and harmful content
- Note model-specific behaviors (e.g., Claude vs GPT differences) when relevant

## Edge Cases

- **Multi-turn prompts**: Evaluate conversation history handling and context window management
- **Tool-use / function-calling prompts**: Test tool selection accuracy and parameter extraction
- **RAG prompts**: Evaluate faithfulness to retrieved context vs. hallucinated answers
- **Multilingual prompts**: Test with non-English inputs even if not the primary use case
- **Chain-of-thought prompts**: Verify reasoning steps are correct, not just final answers
- **System prompt only (no user message yet)**: Evaluate the system prompt in isolation for leakage risk
- **Prompts with dynamic variables**: Test template rendering with missing, null, or malicious variable values
