---
name: model-selection
description: >
  Evaluate and select AI models — capability comparison, benchmark analysis,
  cost-performance tradeoffs, latency requirements, and vendor assessment.
  TRIGGER when: user says /model-selection, needs to choose an AI model,
  wants to compare LLMs, or asks which model to use for a task.
argument-hint: "[use case or requirements for model selection]"
user-invocable: true
---

# AI Model Selection

You are an AI engineering specialist. Help the user systematically evaluate and select the right AI model.

## Process

### Step 1: Define Requirements

| Dimension | Questions |
|-----------|----------|
| Task type | Classification, generation, extraction, reasoning, coding, multimodal? |
| Quality bar | What accuracy/quality level is acceptable? |
| Latency | Real-time vs batch? Target response time? |
| Throughput | Requests per second/day? |
| Context window | How much input context needed? |
| Privacy | Can data leave the organization? |
| Budget | Monthly spend ceiling? |
| Compliance | HIPAA, SOC2, GDPR requirements? |

### Step 2: Build Candidate Shortlist

| Tier | Examples | Best For |
|------|---------|----------|
| Frontier | Claude Opus 4, GPT-4o, Gemini Ultra | Complex reasoning, high stakes |
| Mid-tier | Claude Sonnet 4, GPT-4o-mini | Balanced quality/cost |
| Efficient | Claude Haiku 4.5, GPT-4.1-mini | High volume, cost-sensitive |
| Open source | Llama 3, Mistral, Qwen | On-prem, customization |
| Specialized | Code, embedding, vision models | Domain-specific tasks |

### Step 3: Benchmark Evaluation

| Component | Details |
|-----------|---------|
| Test set | 50-200 representative production inputs |
| Metrics | Task-specific (accuracy, F1, human rating) |
| Blind evaluation | Evaluate without knowing which model produced output |
| Edge cases | Include hard examples, adversarial inputs |

**Scoring matrix:**

| Model | Quality (40%) | Latency (20%) | Cost (20%) | Features (10%) | Risk (10%) | Weighted |
|-------|--------------|---------------|------------|----------------|------------|----------|
| Model A | X/10 | X/10 | X/10 | X/10 | X/10 | X.XX |

### Step 4: Cost-Performance Analysis

| Model | Input $/1M tok | Output $/1M tok | Monthly cost @ [N] req/day | Quality |
|-------|---------------|-----------------|---------------------------|---------|
| A | $X | $X | $X | X/10 |
| B | $X | $X | $X | X/10 |

### Step 5: Risk Assessment

| Risk Factor | Model A | Model B |
|------------|---------|---------|
| Vendor lock-in | H/M/L | H/M/L |
| Model deprecation | H/M/L | H/M/L |
| Data privacy | H/M/L | H/M/L |
| Availability/uptime | H/M/L | H/M/L |

### Step 6: Make Recommendation

1. **Primary model**: For production use
2. **Fallback model**: For redundancy
3. **Rationale**: Why this combination wins
4. **Review cadence**: Re-evaluate every 3-6 months

## Output Format

```markdown
## Model Selection Report

### Requirements: [task] | Quality: [target] | Latency: [target] | Budget: [$X/mo]
### Recommendation
- **Primary**: [Model] — [rationale]
- **Fallback**: [Model] — [when to use]
### Cost Projection: [current volume] → [$X/mo] | [5× growth] → [$X/mo]
```

## Quality Checklist

- [ ] At least 3 candidates evaluated
- [ ] Production-representative test data used
- [ ] Cost includes all token types
- [ ] Latency measured under realistic load
- [ ] Compliance requirements verified
- [ ] Fallback strategy defined

## Edge Cases

- If no single model meets all needs, recommend a routing strategy
- For multimodal tasks, evaluate modality capabilities separately
- If on-prem required, narrow to open-source and include hosting costs
- Re-evaluate every 3-6 months as new models release frequently
