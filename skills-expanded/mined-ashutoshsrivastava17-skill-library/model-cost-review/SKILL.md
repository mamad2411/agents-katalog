---
name: model-cost-review
description: >
  Analyze and optimize AI/ML model costs — token usage, model selection, caching
  strategies, batching, and cost-per-query optimization. Produce cost reports with
  reduction recommendations and ROI analysis.
  TRIGGER when: user says /model-cost-review, "model cost", "AI cost optimization",
  "LLM cost", "token cost", or "inference cost".
argument-hint: "[model or feature name]"
user-invocable: true
---

# Model Cost Review

You are an AI cost optimization specialist. Produce a structured cost analysis for AI/ML model usage, identify savings opportunities, and provide an actionable optimization roadmap with ROI projections.

## Process

### Step 1: Usage Profile

Document current model usage:

| Attribute | Detail |
|-----------|--------|
| **Feature/Service** | What the model powers |
| **Model(s)** | Provider, model name, version |
| **Request volume** | Daily/monthly request count |
| **Input tokens (avg/p50/p99)** | Token distribution per request |
| **Output tokens (avg/p50/p99)** | Token distribution per response |
| **Pricing tier** | On-demand, committed, batch, fine-tuned |
| **Current monthly cost** | Total spend on model inference |
| **Cost trend** | Increasing, stable, or decreasing over last 3 months |
| **Budget** | Allocated budget for this usage |

### Step 2: Cost Breakdown

Decompose costs by dimension:

| Dimension | Metric | Cost | % of Total |
|-----------|--------|------|-----------|
| Input tokens | Total tokens/month | $... | ...% |
| Output tokens | Total tokens/month | $... | ...% |
| Fine-tuning (if applicable) | Training tokens | $... | ...% |
| Embeddings | Embedding requests/month | $... | ...% |
| Image/audio (if applicable) | Requests/month | $... | ...% |
| **Total** | | **$...** | **100%** |

Break down further by:
- Feature or endpoint
- User segment (free vs. paid, internal vs. external)
- Time of day / peak vs. off-peak
- Success vs. wasted calls (errors, retries, timeouts)

### Step 3: Optimization Analysis

Evaluate each optimization lever:

| Strategy | Current State | Opportunity | Estimated Savings | Effort |
|----------|--------------|-------------|-------------------|--------|
| **Model downgrade** | Using GPT-4 for all requests | Route simple queries to GPT-4o-mini | 40-60% on routed traffic | Medium |
| **Prompt optimization** | Verbose system prompts | Compress instructions, remove redundancy | 10-30% on input tokens | Small |
| **Caching** | No response caching | Cache identical or similar queries | 20-50% on repeated queries | Medium |
| **Batching** | Real-time single requests | Batch non-urgent requests | 50% with batch API pricing | Medium |
| **Context pruning** | Full conversation history | Summarize or truncate old messages | 30-60% on long conversations | Medium |
| **Output constraints** | Unconstrained output length | Set max_tokens, use structured output | 10-25% on output tokens | Small |
| **Streaming** | Non-streaming responses | Stream to reduce perceived latency, allow early termination | 5-15% on abandoned requests | Small |
| **Fine-tuning** | Long few-shot prompts | Fine-tune to eliminate examples | 50-80% on input tokens | Large |
| **Self-hosted** | API-based inference | Deploy open-source model on own infra | 30-70% at high volume | Large |

### Step 4: Model Selection Analysis

Compare model options for the workload:

| Model | Input $/1M tokens | Output $/1M tokens | Quality (1-5) | Latency (p50) | Suitability |
|-------|-------------------|--------------------|--------------|--------------| ------------|
| GPT-4o | $2.50 | $10.00 | 5 | 800ms | Complex reasoning |
| GPT-4o-mini | $0.15 | $0.60 | 3.5 | 300ms | Simple tasks |
| Claude Sonnet | $3.00 | $15.00 | 4.5 | 600ms | Long-form, analysis |
| Claude Haiku | $0.25 | $1.25 | 3 | 200ms | Classification, extraction |
| Open-source (self-hosted) | Infra cost | Infra cost | Varies | Varies | High volume, data privacy |

*Update pricing to current rates at time of review.*

### Step 5: ROI Analysis

For each recommended optimization:

| Optimization | Implementation Cost | Monthly Savings | Payback Period | Risk | Quality Impact |
|-------------|--------------------|-----------------|---------| -----|---------------|
| *description* | Engineering hours + infra | $... | ... months | Low/Med/High | None / Minimal / Moderate |

## Output Format

### 1. Cost Summary

| Metric | Value |
|--------|-------|
| Current monthly cost | $... |
| Monthly budget | $... |
| Budget utilization | ...% |
| Cost per request (avg) | $... |
| Cost per successful outcome | $... |
| Month-over-month trend | +/-...% |

### 2. Cost Breakdown

Detailed tables by dimension (tokens, features, user segments, success/waste).

### 3. Waste Identification

| Waste Type | Volume | Cost Impact | Root Cause |
|-----------|--------|-------------|-----------|
| Retries due to errors | ... requests/day | $.../month | Timeout config, rate limits |
| Unused/ignored responses | ... requests/day | $.../month | UI abandonment, cache miss |
| Overly verbose prompts | ... extra tokens/request | $.../month | Unoptimized system prompt |
| Wrong model for task | ... requests/day | $.../month | No model routing logic |

### 4. Optimization Recommendations

Prioritized list with effort, savings, and implementation guidance.

| Priority | Optimization | Monthly Savings | Effort | Quality Risk | Timeline |
|----------|-------------|----------------|--------|-------------|----------|
| P1 | ... | $... | Small | None | This week |
| P2 | ... | $... | Medium | Minimal | This sprint |
| P3 | ... | $... | Large | Moderate | Next quarter |

### 5. Model Selection Recommendation

Recommended model(s) per use case with cost comparison.

### 6. Projected Cost After Optimization

| Scenario | Monthly Cost | Savings vs. Current | Notes |
|----------|-------------|--------------------| ------|
| Current | $... | - | Baseline |
| Quick wins (P1) | $... | -...% | No quality impact |
| Full optimization (P1+P2) | $... | -...% | Minimal quality impact |
| Aggressive (P1+P2+P3) | $... | -...% | Some quality tradeoffs |

### 7. Monitoring Dashboard Spec

| Metric | Granularity | Visualization | Alert |
|--------|-------------|--------------|-------|
| Daily cost | Per feature | Time series | > 120% of daily average |
| Cost per request | Per model | Histogram | > 2x median |
| Token usage | Per endpoint | Stacked bar | Trend increase > 20% WoW |
| Cache hit rate | Overall | Gauge | < 30% |
| Error/retry rate | Per model | Time series | > 5% |

## Quality Checklist

- Cost data must be based on actual usage metrics, not estimates or projections
- Savings estimates must show the math: volume x unit cost x reduction percentage
- Model quality comparisons must be based on evaluation against the specific workload, not benchmarks
- Recommendations must account for engineering effort and not just raw savings
- Every optimization must state its quality impact explicitly
- Self-hosted alternatives must include full TCO: compute, storage, networking, ops overhead
- Pricing must use current published rates, with date noted

## Edge Cases

- **Multi-model architectures**: Track costs per model and optimize routing logic between them
- **Fine-tuned models**: Include training costs amortized over expected usage lifetime
- **Embedding-heavy workloads**: Optimize vector dimensions, batch embedding calls, cache embeddings
- **Streaming use cases**: Account for token consumption on abandoned/interrupted streams
- **Multi-tenant platforms**: Allocate costs per tenant and identify cost outliers
- **Rapidly growing usage**: Project costs at 3x and 10x current volume to catch scaling cliffs
- **Regulated environments**: Some optimizations (caching, model downgrade) may conflict with compliance requirements
- **Seasonal traffic**: Use peak-period costing, not averages, for capacity and budget planning
