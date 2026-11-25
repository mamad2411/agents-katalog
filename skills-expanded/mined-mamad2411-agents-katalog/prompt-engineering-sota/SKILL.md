---
name: prompt-engineering-sota
description: >
  Apply SOTA prompt engineering techniques to any task. USE when: improving AI responses,
  structuring complex instructions, debugging poor outputs, choosing between CoT/ToT/ReAct,
  writing system prompts, or any task needing optimal LLM interaction. Covers 40+ techniques
  from Zero-shot to Tree-of-Thought, ReAct, Reflexion, Self-Consistency. Optimized for fast
  models (Haiku 4.5, Llama 3.1 8B). Trigger: "improve this prompt", "the AI gives bad answers",
  "write a system prompt", "use chain of thought".
metadata:
  version: "1.0.0"
  category: "AI/Prompt Engineering"
  optimized_for: ["claude-haiku-4-5", "llama-3.1-8b", "gpt-oss-120b-free"]
  sources: ["arXiv:2402.07927", "Anthropic docs", "NeurIPS 2022-2023"]
---

# Skill: Prompt Engineering SOTA

## Decision Tree — Select Technique

```
Task type?
├── Simple factual → Zero-shot (direct question)
├── Needs reasoning steps → Chain-of-Thought (CoT)
│   ├── Single answer OK → Standard CoT ("think step by step")
│   └── Need reliable answer → Self-Consistency (CoT × 3-5, majority vote)
├── Complex multi-path problem → Tree-of-Thought (ToT)
│   └── Explore branches, backtrack, select best path
├── Needs tool use or web → ReAct (Reason + Act loop)
├── Needs self-correction → Reflexion (act → evaluate → reflect → retry)
├── Has examples to learn from → Few-shot (2-5 examples in prompt)
│   └── Need task decomposition → Least-to-Most Prompting
└── Classify/route inputs → Instruction Following + Role Prompting
```

## Core Techniques (Haiku-compatible — no deep reasoning required)

### 1. Zero-Shot Direct
```
[Task]: <clear instruction>
[Output format]: <specify exactly>
```

### 2. Chain-of-Thought (CoT)
Add one of these triggers:
- "Think step by step."
- "Let's reason through this carefully."
- "Before answering, work through the problem."

### 3. Few-Shot Examples
```
[Task]: <instruction>

Examples:
Input: <example_1_input>
Output: <example_1_output>

Input: <example_2_input>
Output: <example_2_output>

Input: <actual_input>
Output:
```

### 4. ReAct (for agentic tasks)
```
You have access to tools: [tool_list]

Thought: What do I need to do?
Action: <tool_name>(<args>)
Observation: <result>
Thought: What did I learn? What next?
...
Answer: <final_answer>
```

### 5. Self-Consistency (reliability boost)
Generate 3-5 independent answers → take majority. Use when accuracy > speed.

### 6. Role Prompting
```
You are an expert [role] with [N] years of experience in [domain].
Your task: [instruction]
```

### 7. Structured Output Forcing
```
Respond ONLY in this JSON format (no prose):
{
  "field1": "<value>",
  "field2": ["item1", "item2"],
  "confidence": 0.0-1.0
}
```

## System Prompt Template (SOTA)
```
## Role
You are [role]. You [key capability].

## Context
[Relevant background. Problem domain. Constraints.]

## Instructions
1. [Primary instruction]
2. [Secondary instruction]
3. [Quality gate: "If X, then Y"]

## Output Format
[Exact format. Examples if needed.]

## Guardrails
- Do: [allowed actions]
- Don't: [forbidden actions]
- If uncertain: [fallback behavior]
```

## Anti-Patterns to Avoid
- ❌ Vague instructions ("be helpful") → ✅ Specific outcomes ("return a 3-item list")
- ❌ Overloading a single prompt → ✅ Decompose into pipeline steps
- ❌ No output format specified → ✅ Always define format explicitly
- ❌ No examples for ambiguous tasks → ✅ Add 2-3 few-shot examples
- ❌ "Do X and Y and Z and..." → ✅ One primary objective per prompt

## Token Optimization (for cheap models)
- Front-load the most important instruction
- Remove filler words ("Please kindly", "I would like you to")
- Use XML tags for structure: `<context>`, `<task>`, `<format>`
- Compress examples: use minimal but representative ones
- Split complex tasks: orchestrator prompt → specialized worker prompts

## References
- Sahoo et al. arXiv:2402.07927 (40+ techniques survey, 2025)
- Anthropic "Claude Prompt Engineering" docs
- Wei et al. "Chain-of-Thought Prompting Elicits Reasoning" (NeurIPS 2022)
- Yao et al. "Tree of Thoughts" (NeurIPS 2023)
- Yao et al. "ReAct: Synergizing Reasoning and Acting" (ICLR 2023)
