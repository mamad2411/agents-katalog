---
name: model-selection-and-routing
description: Pick models on the accuracy-vs-cost frontier and route easy queries to cheaper models — the most expensive model is rarely the right default.
---

# Model selection and routing

The biggest model is not the default-correct choice. Evaluate on the **accuracy-vs-cost Pareto frontier**, and for mixed workloads, **route by difficulty** instead of sending everything to one tier.

## Select on the cost/accuracy frontier

- When choosing a model for a task, plot candidates on accuracy *and* cost and pick from the Pareto frontier — the set where you can't get more accuracy without paying more. The priciest models are **rarely Pareto-optimal**; a cheaper model often matches them on your task at a fraction of the cost.
- Re-run this comparison per task type. Frontier position is workload-specific — a model that's optimal for extraction may be dominated for multi-step reasoning.

## Route by difficulty

- For a stream of mixed-difficulty requests, a **learned router** that sends easy queries to a small/cheap model and hard ones to a strong model can cut cost **more than 2×** while retaining roughly **95%** of the strong model's quality.
- Route on predicted difficulty, with a confidence threshold and a fallback/escalation path to the strong model when the cheap model is uncertain or fails validation.
- Measure the router itself: track the escalation rate and the quality delta on routed-cheap traffic so a drift in either doesn't silently erode quality or savings.

## Examples

```ts
// BAD — always routing every request to the most expensive model
const response = await client.messages.create({
  model: 'claude-opus-4-8',  // overkill for simple extraction tasks
  messages: [{ role: 'user', content: 'Extract the date from: "Meeting on June 15"' }],
})

// GOOD — route by difficulty; reserve strong model for complex tasks
const difficulty = await router.predict(prompt)  // learned router
const model = difficulty === 'easy'
  ? 'claude-haiku-4-5-20251001'   // fast and cheap for simple tasks
  : 'claude-sonnet-4-6'           // stronger model for complex reasoning
const response = await client.messages.create({ model, messages })
```

## Sources

Kapoor et al., "Holistic Agent Leaderboard (HAL)," 2025-10 — <https://arxiv.org/abs/2510.11977>: agents should be compared on the accuracy–cost Pareto frontier; the most expensive models are rarely Pareto-optimal. Ong et al., "RouteLLM," ICLR 2025 — <https://openreview.net/forum?id=8sSqNntaMr>: a learned strong/weak router achieves >2× cost reduction at ~95% of GPT-4 quality. (Per-benchmark routing figures beyond the >2×/~95% headline are project self-reported; cite only the peer-reviewed headline as fact.)
