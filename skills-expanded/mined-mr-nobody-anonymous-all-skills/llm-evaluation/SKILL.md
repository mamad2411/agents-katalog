---
name: llm-evaluation
description: "Evaluating Large Language Models: benchmark datasets (MMLU, GSM8k), LLM-as-a-judge, reference-based vs. reference-free metrics"
category: ai-evaluation
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/ai-evaluation/llm-evaluation/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# LLM Evaluation Methodology

## Scope
LLM evaluation provides quantitative and qualitative assessment of Large Language Model outputs across capabilities, reasoning, factuality, and domain expertise.

## Evaluation Frameworks
- **Automated Standard Benchmarks**:
  - MMLU (Massive Multitask Language Understanding): Multi-choice knowledge.
  - GSM8k / MATH: Multi-step mathematical reasoning.
  - HumanEval / MBPP: Code generation functional correctness (pass@k metric).
- **LLM-as-a-Judge**: Using high-capability models (Claude 3.5 Sonnet, GPT-4o) with structured rubrics to score complex open-ended responses on clarity, helpfulness, and correctness.
- **Position & Verbosity Bias Mitigation**: Swapping response order in pairwise comparisons; normalizing length penalties.

## Tools & Platforms
- **Software**: DeepEval, Ragas, Promptfoo, lm-evaluation-harness (EleutherAI).
