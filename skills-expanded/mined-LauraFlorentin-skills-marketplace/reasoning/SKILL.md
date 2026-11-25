---
name: reasoning
description: Design prompts and agent workflows that improve complex logical, mathematical, planning, and decision tasks through decomposition, verification, alternative hypotheses, and concise rationale. Use when a user asks to improve reasoning reliability, reduce calculation or logic errors, compare approaches, or build a structured problem-solving loop; do not require disclosure of private chain-of-thought.
---

# Reasoning Techniques

Improve outcomes with explicit task structure and verification. Do not require a model to expose hidden chain-of-thought. Ask for concise conclusions, assumptions, calculations, evidence, and checks that a user can evaluate.

## Pattern

1. Define the question, constraints, units, and success criterion.
2. Split the problem into independently checkable subproblems.
3. Retrieve or calculate required facts instead of guessing.
4. Consider materially different hypotheses or solution paths when ambiguity warrants it.
5. Verify with deterministic tools, invariants, counterexamples, or an independent review pass.
6. Return the answer with a concise rationale, assumptions, uncertainty, and verification evidence.

## Choose a method

| Need | Method |
|---|---|
| Multi-step calculation | Decompose, calculate with a tool, check units and bounds |
| Ambiguous diagnosis | Generate competing hypotheses and discriminating tests |
| Planning | Identify dependencies, risks, checkpoints, and stop conditions |
| High variance | Generate independent candidate answers and verify rather than majority-voting blindly |
| Search problem | Explore branches with explicit pruning criteria and resource limits |
| High-stakes judgment | Use authoritative evidence and qualified human review |

## Output contract

```text
Answer
Key assumptions
Concise rationale or calculation
Verification performed
Uncertainty and what would change the answer
```

Do not treat verbalized reasoning as proof. Correctness comes from evidence and checks.
