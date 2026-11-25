# Model Router 2026

Route tasks to the optimal LLM for speed, quality, and cost.

## Model Roles

| Model | Use For | Why |
|-------|---------|-----|
| **Fable 5.1** (`claude-fable-5-1`) | Plans, audits, code review, architecture decisions, complex reasoning | Highest reasoning quality |
| **GPT-6** (`gpt-6`) | Tool execution, function calling, multi-step agentic tasks | Best tool-use accuracy |
| **Gemini** (`gemini-2.5-pro`) | High-volume batch processing, long-context ingestion, cheap scale | Lowest cost at volume |

## Routing Formula

```
Task type?
  ├─ Design / plan / audit / review → Fable 5.1
  ├─ Execute tools / call APIs / agent loops → GPT-6
  └─ Batch / embed / summarize at scale → Gemini
```

## When to Use This Skill

Invoke `/model-router-2026` when:
- Deciding which model to assign to a subtask in a multi-agent pipeline
- Estimating cost before scaling a workflow
- Reviewing an agent architecture for model mismatches

## Routing Rules

1. **Never use Gemini for reasoning-heavy single tasks** — cheap but weaker on complex chains
2. **Never use Fable for tool-heavy loops** — great thinker, slower executor
3. **Default to Fable** when uncertain about task type
4. **Switch mid-pipeline** is fine — plan in Fable, execute in GPT-6, summarize in Gemini

## Prompt Templates

### Fable 5.1 — Plan
```
You are a strategic planner. Given the following goal, produce a step-by-step implementation plan with clear success criteria for each step. Be specific about dependencies and risks.

Goal: {GOAL}
```

### GPT-6 — Execute
```
Execute the following plan step by step. Call tools as needed. Report results after each step. Stop if you encounter an error and describe it.

Plan: {PLAN}
Tools available: {TOOL_LIST}
```

### Gemini — Batch
```
Process the following {N} items. Apply the transformation uniformly. Return structured JSON.

Transformation: {TRANSFORM}
Items: {ITEMS}
```
