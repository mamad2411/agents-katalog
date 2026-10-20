---
name: use-fast-models-for-quick-checks
description: "Assign bounded routine checks to suitable smaller models and escalate tasks that require stronger reasoning or verification."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["model-routing", "token-economics", "haiku-vs-sonnet", "latency-optimization", "cost-efficiency", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Use Fast Models for Quick Checks (Model Routing Economics) (AI Skill)

## Overview
Using a heavyweight reasoning model (like OpenAI o1 or Claude 3.5 Sonnet) to fix a spelling mistake, extract a date, or format a Markdown table is like hiring a senior structural engineer to screw in a lightbulb.

Heavy models are **10x to 50x more expensive** and have significantly higher latency (5-15 seconds vs. 400ms).

The **Model Routing Economics Protocol** matches task cognitive difficulty to the optimal model tier, slashing AI API costs and accelerating daily workflow velocity.

---

## The 3-Tier Model Routing Matrix

```
┌─────────────────────────────────────────────────────────────┐
│                 3-Tier Model Routing Matrix                 │
│                                                             │
│  [ TIER 1: LIGHTWEIGHT / SPEED TIER ]                       │
│  • Models: GPT-4o-mini, Claude 3.5 Haiku, Gemini 1.5 Flash  │
│  • Cost: ~$0.15 - $0.80 per Million Tokens (Sub-second)     │
│  • Tasks: Proofreading, classification, JSON ETL, summaries │
│                                                             │
│  [ TIER 2: GENERAL FRONTIER WORKHORSE ]                     │
│  • Models: Claude 3.5 Sonnet, GPT-4o                        │
│  • Cost: ~$3.00 - $15.00 per Million Tokens (2-4 seconds)   │
│  • Tasks: Full-stack coding, persuasive copywriting, RFCs   │
│                                                             │
│  [ TIER 3: DEEP REASONING & MATH ]                          │
│  • Models: OpenAI o1 / o3-mini                              │
│  • Cost: ~$15.00 - $60.00 per Million Tokens (10-30 seconds)│
│  • Tasks: Complex distributed systems, formal math, proofs │
└─────────────────────────────────────────────────────────────┘
```

---

## Task-to-Model Decision Guide

| Daily Task | Recommended Tier | Example Model | Why |
| :--- | :--- | :--- | :--- |
| **Fix Grammar & Typos** | Tier 1 (Lightweight) | Claude Haiku / 4o-mini | Perfect accuracy, 200ms latency, zero waste. |
| **Convert Unstructured Text to TSV**| Tier 1 (Lightweight) | Gemini Flash / 4o-mini | Deterministic parsing, 90% cheaper than Sonnet. |
| **Write a Full React Component** | Tier 2 (Frontier) | Claude 3.5 Sonnet | Requires nuanced architectural & styling awareness. |
| **Debug Race Condition / Deadlock**| Tier 3 (Reasoning) | OpenAI o1 / o3-mini | Requires multi-step chain-of-thought search. |

---

## Real-World Cost Analysis

### Scenario: Processing 10,000 Customer Support Tickets per Month

- **Using Tier 2 (Claude 3.5 Sonnet / GPT-4o)**:  
  $10,000 \text{ tickets} \times 1,500 \text{ tokens} = 15\text{M tokens} \rightarrow \mathbf{\$45.00 - \$75.00}$
- **Using Tier 1 (Claude 3.5 Haiku / GPT-4o-mini)**:  
  $10,000 \text{ tickets} \times 1,500 \text{ tokens} = 15\text{M tokens} \rightarrow \mathbf{\$2.25 - \$4.50}$

**Result**: **94% Cost Reduction** with 4x faster response times and zero measurable degradation in classification accuracy.

---

## Summary Best Practices
- **Default to the fast model first**: In web chat interfaces, keep your default set to the fast/mini model for everyday queries; switch to the heavy model only when writing code or complex strategy.
- **Use Two-Stage Cascades**: In API pipelines, use a fast model to classify and filter incoming data, only routing the complex 5% of edge cases to the heavy frontier model.
