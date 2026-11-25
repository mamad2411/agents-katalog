---
name: ai-prompt-design
version: 1.0.0
description: Design and iterate a production LLM prompt with clear structure, few-shot examples, a strict output contract, and failure handling.
author: matrixx0070
tags: [prompting, llm, output-contract, few-shot, reliability]
---

## When to use

Use this when you are turning a fuzzy task ("summarize tickets", "extract fields", "classify intent") into a prompt that ships behind an API and must behave the same way on the 10,000th call as the first.

**Not for:** one-off exploratory chats, or picking a model/price (see `ai-cost-latency`), or evaluating quality at scale (see `ai-eval-harness`).

## Method

1. Write the task as one sentence: input → transformation → output. If you cannot, the prompt is not the problem yet.
2. Choose an output contract FIRST: JSON schema, enum, or delimited text. Decision point: if a downstream system parses it, use JSON and forbid prose.
3. Draft the skeleton in fixed order: role → task → rules → input → output spec. Keep instructions imperative and deduplicated.
4. Add 2-5 few-shot examples ONLY if zero-shot fails on your hard cases. Decision point: if examples exceed ~30% of context, switch to fine-tuning candidacy (see `ai-fine-tune-plan`).
5. Handle failure explicitly: define the exact output for "unknown", "input too long", and "policy violation". Never leave these implicit.
6. Iterate against 10-20 saved hard cases, not vibes. Change one variable per round; keep a changelog.
7. Freeze the prompt with a version string and hand the hard cases to `ai-eval-harness`.

## Example

Task: classify support message urgency.

```
You are a support triage classifier. Output ONLY JSON.
Rules:
- urgency ∈ {"low","normal","high","critical"}
- If the message is unreadable or empty, use "unknown" and set reason.
Message: """{{message}}"""
Output: {"urgency": "...", "reason": "<12 words"}
```

Zero-shot mislabels outages as "high". Add one few-shot example pinning "service down for all users" → "critical". Re-run the 15 saved cases: 13/15 → 15/15.

## Pitfalls

- **Politeness padding.** "Please try your best" adds tokens and nothing else. Cut it.
- **Contradictory rules.** "Be concise" plus "explain thoroughly" makes output nondeterministic. Rank rules; resolve conflicts.
- **No unknown path.** Models hallucinate a confident answer when the honest output is "cannot tell". Always give an escape value.
- **Tuning on the demo case.** Improving one example while silently regressing others. Always re-run the full hard-case set.

## Output format

```
# Prompt: <name> v<n>
ROLE: <who the model is>
TASK: <one sentence>
RULES:
- <imperative rule>
INPUT: <delimited, named variables>
OUTPUT CONTRACT: <schema or enum; forbid extra text>
FAILURE CASES:
- unknown -> <exact output>
- oversized/invalid -> <exact output>
CHANGELOG: v<n> <what changed, which cases moved>
```
