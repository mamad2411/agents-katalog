---
name: clarity-promptforge-performance-optimization
description: >
  Use when optimizing prompt performance, reducing token costs, improving response
  speed, and enhancing prompt clarity without sacrificing output quality. This skill
  provides systematic optimization procedures for prompt efficiency.
---

# Clarity - Prompt Optimization & Performance Analytics

## Overview
Clarity optimizes prompt performance for PromptForge AI. Good prompts aren't just correct—they're efficient, clear, and cost-effective. Clarity ensures every prompt delivers maximum quality at minimum cost.

## When to Use
- When a prompt is too expensive (high token usage, excessive API costs)
- When a prompt is too slow (long response times, excessive reasoning)
- When a prompt produces verbose or unfocused outputs
- When optimizing prompts for production scale
- When balancing quality vs. cost trade-offs
- **Don't use when:** Designing new prompts from scratch (use blueprint-promptforge-template-designer)

## Core Procedures

### Step 1: Profile Current Performance
Measure the prompt's current state:
- **Token Usage:** Input tokens, output tokens, total tokens
- **Cost:** API cost per invocation, cost per month at current volume
- **Latency:** Average response time, p95, p99
- **Quality:** Current quality score (from analyzer metrics)
- **Verbosity:** Output length vs. information density

### Step 2: Identify Optimization Opportunities
Common optimization targets:
- **Redundant Instructions:** Repeated or overlapping instructions
- **Unnecessary Context:** Information the model already knows
- **Verbose Examples:** Examples that are longer than needed
- **Over-Specification:** Constraints that don't improve output quality
- **Inefficient Structure:** Instructions ordered suboptimally

### Step 3: Apply Optimizations
Optimization techniques:
- **Trim:** Remove words, sentences, sections that don't affect output quality
- **Consolidate:** Merge overlapping instructions
- **Prioritize:** Put most important instructions first (model attention decays)
- **Structure:** Use clear headings, bullet points, numbered lists
- **Constrain:** Add output length limits where appropriate

### Step 4: Validate Optimization
After each optimization:
- [ ] Output quality is maintained or improved (compare to baseline)
- [ ] Token usage decreased (measure the improvement)
- [ ] No regression on edge cases
- [ ] Cost savings calculated and documented

### Step 5: Document Optimization
```
OPTIMIZATION REPORT
===================
Prompt: [name and version]
Before: [tokens, cost, latency, quality]
After: [tokens, cost, latency, quality]
Changes Made: [specific optimizations applied]
Savings: [token reduction %, cost reduction %]
Quality Impact: [maintained/improved/degraded]
Recommendation: [deploy/revert/further optimize]
```

## Success Metrics
- Token reduction: >=20% average reduction without quality loss
- Cost savings: >=15% average cost reduction per prompt
- Optimization cycle time: <2 hours per prompt optimization
- Quality maintenance: 0% quality regression after optimization

## Error Handling
- **Error:** Optimization degrades output quality
  **Response:** Revert the specific change, investigate why it caused degradation, try alternative optimization
- **Error:** Optimization saves tokens but increases latency
  **Response:** Measure net impact, if latency increase is significant, reconsider the optimization
- **Error:** Prompt is already well-optimized (<5% further savings possible)
  **Response:** Document as optimized, focus effort on higher-impact prompts

## Cross-Team Integration
**Related Skills:** analyzer-promptforge-prompt-analytics, tuner-promptforge-ab-testing, quantifier-promptforge-benchmarking, cost-optimization
**Used By:** Analyzer, Tuner, Quantifier, Sage, ALL agents creating production prompts