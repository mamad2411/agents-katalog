---
name: business-model-canvas-builder
description: "Use when generating a Business Model Canvas from an idea. Uses guided questions and NLP to produce structured BMC outputs."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [business-model, canvas, bmc, strategy, lean, entrepreneurship, startup]
    related_skills: [value-proposition-architect, buyer-persona-architect, strategic-business-architect, gtm-architect]
---

# Business Model Canvas Builder

## Overview

Takes a raw business idea, product concept, or venture description and produces a complete Business Model Canvas (BMC) using guided discovery. Covers all nine building blocks: Customer Segments, Value Propositions, Channels, Customer Relationships, Revenue Streams, Key Resources, Key Activities, Key Partnerships, and Cost Structure. Identifies gaps, tests internal consistency, and flags risky assumptions.

## When to Use

- Validating a startup idea or new business line.
- Preparing for a pitch, accelerator application, or investor meeting.
- A team has a product but hasn't mapped the full business model.
- Teaching or facilitating a business model workshop.
- Stress-testing an existing business model for weaknesses or pivot opportunities.
- Don't use for: detailed financial models or P&L forecasts (BMC is strategic, not financial), or operational business plans (BMC is a snapshot, not an execution plan).

## How It Works

1. **Guided interview** — Walks through each of the nine blocks with targeted questions, adapting based on whether the business is B2B, B2C, marketplace, SaaS, or service-based.
2. **BMC assembly** — Produces a structured canvas with concise entries for each block, ensuring internal consistency (e.g., value prop matches customer segment, revenue model matches channel).
3. **Gap and risk analysis** — Flags empty or weak blocks, narrative inconsistencies, and untested assumptions.
4. **Variant generation** — Optionally produces alternative BMC configurations (different segments, revenue models, or channels).

## Steps

1. **Idea intake:** Ask the user to describe their business idea in 2-3 sentences. What problem does it solve? For whom? How does it make money (if known)?
2. **Block-by-block discovery:** Walk through each of the nine blocks:

   **1. Customer Segments:** Who are the customers? Are there distinct groups with different needs? B2B or B2C? Use `buyer-persona-architect` for depth if needed.

   **2. Value Propositions:** What unique value does each segment get? What problem is solved or need satisfied? Use `value-proposition-architect` for depth.

   **3. Channels:** How do customers discover, buy, and receive the product? (Direct sales, self-serve, partners, marketplace, retail?)

   **4. Customer Relationships:** What type of relationship does each segment expect? (Personal assistance, self-service, automated, community?)

   **5. Revenue Streams:** What are customers paying for? One-time, subscription, usage-based, marketplace take rate, freemium?

   **6. Key Resources:** What assets are essential? (IP, platform, people, brand, capital, data?)

   **7. Key Activities:** What must the business do exceptionally well? (Product development, sales, content, platform management, supply chain?)

   **8. Key Partnerships:** Who are critical partners/suppliers? Why partner vs. build? (Cost reduction, risk reduction, resource acquisition?)

   **9. Cost Structure:** What are the major fixed and variable costs? Is the model cost-driven or value-driven?

3. **Consistency check:** Verify:
   - Value propositions align with customer segment needs.
   - Revenue streams are sufficient to cover cost structure at scale.
   - Channels match customer expectations and revenue model.
   - Key activities support the value proposition.
4. **Risk flags:** Highlight:
   - Customer segments with no clear value proposition.
   - Revenue models that depend on unvalidated willingness to pay.
   - Key activities the team doesn't have capacity/experience for.
   - Partnerships that are critical but not yet established.
5. **Deliver:** Present the full BMC in a clean table or visual format, with a summary of top 3 risks and recommended next actions.

## Common Pitfalls

1. **Vague entries:** "Everyone" is not a customer segment. "Great experience" is not a value proposition. Force specificity on every block.
2. **Revenue optimism:** Assuming people will pay without evidence. Flag all revenue assumptions as hypotheses until validated.
3. **Ignoring costs:** Early-stage founders focus on revenue and forget cost structure. A BMC without costs is half a canvas.
4. **One canvas fits all:** If you have fundamentally different customer segments, you likely need multiple canvases (one per segment).
5. **Treating the BMC as static:** The canvas is meant to be iterated. Include a version number and date. Recommend revisiting after every major customer discovery interview.

## Verification Checklist

- [ ] All nine building blocks are populated with specific, non-generic content
- [ ] Value propositions are clearly mapped to specific customer segments
- [ ] Revenue streams are listed with pricing model details
- [ ] Cost structure includes both fixed and variable costs
- [ ] Internal consistency check passed (VP ↔ segments, revenue ↔ channels, activities ↔ VP)
- [ ] Top 3 risks are identified with recommended next actions
- [ ] Assumptions that need validation are flagged

## Source

Originally a custom GPT: [Business Model Canvas Builder](https://chatgpt.com/g/g-6874039771988191bc02dc0ee5e2db86-business-model-canvas-builder)
