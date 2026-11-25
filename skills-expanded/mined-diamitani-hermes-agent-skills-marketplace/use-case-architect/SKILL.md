---
name: use-case-architect
description: "Use when defining and structuring AI/automation use cases. Identifies high-value applications, scopes requirements, and prioritizes implementation order."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ai, automation, use-cases, scoping, prioritization, roi]
    related_skills: [tech-stack-architect, kpi-architect, sop-architect, gtm-architect]
---

# Use Case Architect

## Overview

Transforms vague ideas ("we should use AI for customer support") into structured, scoped, and prioritized use cases ready for implementation. For each use case, defines the problem, the AI/automation approach, data requirements, success criteria, estimated effort, and expected ROI. Prioritizes a portfolio of use cases so teams build the highest-impact items first.

## When to Use

- An organization wants to adopt AI or automation but doesn't know where to start.
- You have a list of potential AI applications and need to prioritize them.
- A stakeholder has a specific automation idea that needs scoping and feasibility assessment.
- Building an AI/automation roadmap for a quarter, year, or funding pitch.
- Don't use for: technical implementation details (defer to engineering skills), or purely creative AI exploration with no business outcome.

## How It Works

1. **Opportunity Discovery** — Facilitates a structured brainstorm against business functions (sales, marketing, support, ops, product, HR, finance).
2. **Use Case Structuring** — Each use case gets a consistent template: Problem, Current State, Proposed Solution, Data Requirements, Success Metrics, Effort (T-shirt size), and Expected Impact.
3. **Prioritization** — Scores and ranks use cases on an Impact vs. Feasibility matrix with clear rationale.
4. **Roadmap** — Produces a phased implementation plan: Quick Wins (low effort, high impact), Strategic Bets (high effort, high impact), Fill-Ins (low effort, low impact), and Moonshots (high effort, uncertain impact).

## Steps

1. **Discovery session:** Ask the user about their business: team size, current pain points, existing tools, and where they feel AI could help. If they don't know, walk through each business function and suggest common AI/automation patterns.
2. **Generate use cases:** Produce 5-12 structured use cases using the template:
   - **Problem:** What's broken or slow today?
   - **Current state:** How is it done now (manual process, no process, expensive)?
   - **AI approach:** What type of AI/automation applies? (RPA, LLM, classification, recommendation, agent, workflow)
   - **Data needed:** What data must exist or be collected?
   - **Success metric:** How do we know it worked? Tie to a KPI from `kpi-architect`.
   - **Effort:** Small / Medium / Large
   - **Impact:** $ saved, hours saved, revenue gained, or NPS improvement
3. **Prioritize:** Plot on an Impact vs. Feasibility 2x2. Label each quadrant. Recommend Phase 1 (2-3 quick wins), Phase 2 (1-2 strategic bets), and Phase 3+ (everything else).
4. **Validate:** For the top 2-3 use cases, do a pre-mortem: what's most likely to go wrong? What dependency are we assuming? Flag risks explicitly.
5. **Deliver roadmap:** Present the prioritized portfolio with a clear "start here" recommendation and the first 30-60-90 day plan.

## Common Pitfalls

1. **Solution-first thinking:** Jumping to "let's build a chatbot" without defining the problem leads to shelfware. Always start with the pain point.
2. **Ignoring data readiness:** The best AI use case fails if the data doesn't exist or is siloed. Make data requirements a hard gate in prioritization.
3. **Over-indexing on novelty:** Just because generative AI is cool doesn't mean it's the right solution. Sometimes a simple automation or rule-based system is better.
4. **No success metric:** "Better customer experience" is not measurable. Every use case needs a quantifiable outcome.
5. **Boiling the ocean:** A roadmap with 20 use cases paralyzes teams. Cap Phase 1 at 3 items max.

## Verification Checklist

- [ ] Each use case has problem, current state, AI approach, data needs, success metric
- [ ] Prioritization matrix is complete with clear rationale
- [ ] Phase 1 is limited to 2-3 quick wins
- [ ] Top use cases have pre-mortem risk flags
- [ ] Roadmap includes 30-60-90 day milestones
- [ ] Data dependencies are surfaced for every use case

## Source

Originally a custom GPT: [Use Case Architect](https://chatgpt.com/g/g-68ae4bf0b1a081919c0bac4113cf7334-use-case-architect)
