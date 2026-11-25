---
title: Commercial Variation Order Analysis
description: Analyze, quantify, and assess variation orders for scope changes, pricing validation, contractual entitlement, and approval routing
version: 1.0
frequency_percent: 65.0
success_rate_percent: 90.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/00250-commercial/commercial-variation-order-analysis
gigabrain_tags: disciplines, 00250-commercial, commercial-variation-order-analysis, change-management
openstinger_context: variation-orders, scope-change, cost-impact-analysis
last_updated: 2026-04-01
related_docs:
  - docs_construct_ai/disciplines/00250-commercial/agent-data/domain-knowledge/00250_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/00250-commercial/agent-data/prompts/00250_AI-NATIVE-COMMERCIAL-PROMPT.md
related_skills:
  - commercial-claim-quantification
  - commercial-contract-amendment
---

# Commercial Variation Order Analysis

## Overview
Analyze and quantify variation orders — rate application, cost impact, time impact, and precedent analysis.
**Announce at start:** "I'm using the commercial-variation-order-analysis skill to analyze a variation order."

## When to Use This Skill
**Trigger Conditions:** Variation event directed by engineer/owner, scope change encountered, unforeseen conditions encountered, design modification required
**Prerequisites:** Variation event documented, contract rates available, scope change identified

## Step-by-Step Procedure
### Step 1: Identify Variation Event
1. Identify the event triggering the variation
2. Verify written instruction received
3. Document the circumstances (date, cause, impact description)
### Step 2: Verify Contractual Entitlement
1. Identify the contract clause providing for variations
2. Check if notice requirements met
3. Verify the variation is within the scope of allowable changes
### Step 3: Identify Applicable Rates
1. Check if contract contains applicable rates for the varied work
2. If no applicable rate, identify analogous rates for similar work
3. If no analogous rate, calculate new rates from first principles
### Step 4: Calculate Cost Impact
1. Direct costs: Additional labor, materials, equipment
2. Time-related costs: Extended preliminaries, site overhead
3. Overheads and profit: Apply contract percentage or reasonable rate
### Step 5: Calculate Time Impact
1. Determine if variation is on the critical path
2. Calculate additional days required
3. Assess concurrency with other delays
### Step 6: Assess Precedent
1. Identify similar variations and their settlement
2. Ensure consistency with previous variation assessments
3. Document precedent for future reference
### Step 7: Prepare VO Submission
1. Compile variation description
2. Attach entitlement clause reference
3. Include detailed cost breakdown
4. Include time impact assessment
5. Submit for approval and routing

## Success Criteria
- [ ] Variation event documented with written instruction
- [ ] Contractual entitlement verified and documented
- [ ] Applicable rates identified and applied correctly
- [ ] Cost impact calculated with detailed breakdown
- [ ] Time impact assessed with critical path analysis
- [ ] Precedent reviewed for consistency
- [ ] VO submission prepared with all elements

## Common Pitfalls
1. **No Written Instruction** — Never proceed with varied work without written instruction. Oral instructions must be confirmed in writing.
2. **Wrong Rate Application** — Applying inappropriate rates leads to disputes. Follow contract rate hierarchy: applicable → analogous → new.
3. **Missing Time Impact** — Time impact is often under-assessed. Always check critical path.

## Cross-References
### Related Skills
- `commercial-claim-quantification` — Cost quantification methodology
- `commercial-contract-amendment` — Contract amendment process
### Related Agents
- `COM-009` Commercial Variation & Claims Agent — Primary agent
- `COM-002` Commercial Contract Administrator Agent — Supporting agent