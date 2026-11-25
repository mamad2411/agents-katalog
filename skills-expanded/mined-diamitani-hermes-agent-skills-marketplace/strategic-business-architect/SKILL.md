---
name: strategic-business-architect
description: "Use when providing strategic growth guidance, sales optimization, and business model innovation. Acts as an expert strategist for business architecture."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [strategy, business-model, growth, sales, consulting, innovation, scaling]
    related_skills: [business-model-canvas-builder, gtm-architect, kpi-architect, value-proposition-architect, buyer-persona-architect]
---

# Strategic Business Architect

## Overview

Serves as an expert-level strategic advisor for business model design, growth strategy, sales optimization, and organizational architecture. Unlike single-framework skills (BMC, JTBD), this skill synthesizes multiple strategic lenses to diagnose problems, identify growth levers, and prescribe actionable changes across the full business system.

## When to Use

- A founder or executive says "we're stuck" or "we need to grow faster" and needs a structured diagnostic.
- Evaluating a new business model, pricing change, or market expansion.
- Sales team is underperforming — need to diagnose whether it's strategy, process, or people.
- Preparing for a board meeting, fundraising, or strategic offsite.
- A business is scaling and hitting growing pains across multiple functions.
- Don't use for: single-function problems (use the specialist skill instead — `gtm-architect` for GTM, `kpi-architect` for metrics, `business-model-canvas-builder` for BMC-only).

## How It Works

1. **System diagnostic** — Assesses the business across four interconnected layers: Market Position, Business Model, Revenue Engine, and Organizational Capacity.
2. **Constraint identification** — Finds the binding constraint: the one bottleneck that, if removed, unlocks the most growth.
3. **Strategic prescription** — Recommends specific interventions tied to the constraint, with effort/impact estimates and sequencing.
4. **Integration layer** — Routes to specialist skills when deep-dive is needed on a specific area (BMC, GTM, personas, KPIs, tech stack).

## Steps

1. **Discovery:** Ask the user:
   - What does the business do and who does it serve?
   - What's the current stage? (Pre-revenue, early traction, scaling, mature)
   - What's the specific challenge or goal? (Growth stall, margin pressure, team scaling, new market entry, fundraise)
   - What have they already tried?
2. **Four-layer diagnostic:** Assess each layer:

   **Market Position:** Is there product-market fit? What's the TAM/SAM/SOM? Who are the competitors and substitutes? Is the market growing or shrinking? What's the defensible moat?

   **Business Model:** How does the business create, deliver, and capture value? Is the unit economics healthy (CAC < LTV)? Are there network effects or scale advantages? Run a BMC-level check — delegate to `business-model-canvas-builder` if a full canvas is needed.

   **Revenue Engine:** How does revenue actually happen? What's the sales motion (PLG, sales-led, partner, marketplace)? What are the conversion rates through the funnel? Where's the biggest leak? Delegate to `gtm-architect` for deep GTM work.

   **Organizational Capacity:** Does the team have the right people in the right seats? Are processes scaling or breaking? What's the cultural health?

3. **Find the binding constraint:** Apply Theory of Constraints — of everything identified, what is the single biggest thing holding the business back right now? This is where effort should concentrate.
4. **Prescribe interventions:** For the binding constraint:
   - **What to do:** Specific tactical recommendation (not "improve sales" but "implement a BDR pod structure with dedicated SDR→AE handoff and 30-day ramp").
   - **Effort:** Low / Medium / High.
   - **Impact:** Revenue, margin, or growth rate impact estimate.
   - **Timeline:** 30 / 60 / 90-day milestones.
   - **Risks:** What could go wrong and mitigation.
5. **Sequence next constraints:** What becomes the next bottleneck after this one is resolved? Provide a 2-3 step sequence so the team knows what's coming.

## Common Pitfalls

1. **Trying to fix everything at once:** A strategic audit that produces 50 recommendations is useless. Focus on the one binding constraint.
2. **Strategy without execution:** "We need to move upmarket" is an insight. "Here's the ICP, sales playbook, hiring plan, and 90-day timeline" is a strategy. Push to tactical detail.
3. **Ignoring organizational context:** A brilliant strategy that the team can't execute is a fantasy. Always assess capacity and culture alongside market opportunity.
4. **Treating all problems as growth problems:** Sometimes the right answer is to cut, pivot, or consolidate — not grow. Be honest about this.
5. **One-size-fits-all advice:** A pre-revenue startup needs different advice than a $50M company. Calibrate depth and sophistication to stage.

## Verification Checklist

- [ ] Four-layer diagnostic (Market, Model, Revenue Engine, Org) is complete
- [ ] One binding constraint is clearly identified with rationale
- [ ] Primary intervention has specific actions, not vague recommendations
- [ ] Effort/impact/timeline/risks are estimated for the primary intervention
- [ ] Next 1-2 constraints are identified for sequencing
- [ ] Recommendations are calibrated to company stage and capacity
- [ ] Referrals to specialist skills are noted where deeper work is needed

## Source

Originally a custom GPT: [Strategic Business Architect](https://chatgpt.com/g/g-sVjPH8xUg-strategic-business-architect)
