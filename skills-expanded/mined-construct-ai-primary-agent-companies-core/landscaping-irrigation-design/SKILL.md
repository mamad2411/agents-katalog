---
title: Landscaping Irrigation Design
description: Water requirement calculation, sprinkler selection, zone design, and irrigation specification for landscape areas
frequency: Per landscape zone
success_rate: 95%
tags:
  - domainforge_ai
  - landscaping
  - irrigation-design
  - 03000_landscaping
docs:
  - docs_construct_ai/disciplines/03000_landscaping/agent-data/domain-knowledge/03000_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/03000_landscaping/agent-data/prompts/03000_AI-NATIVE-LANDSCAPING-PROMPT.md
---

# Landscaping Irrigation Design

## Overview
Water requirement calculation, sprinkler selection, zone design, and irrigation specification for landscape areas. Primary agent: 03000-002 Irrigation Design Agent.

## Triggers
- Planting plan complete
- Irrigation design requested for zone
- Irrigation system upgrade required
- Water efficiency review requested

## Prerequisites
- Planting plan with plant types and quantities
- Site topography and water pressure data
- Water availability and efficiency requirements
- Climate data (evapotranspiration, rainfall patterns)

## Steps

### Step 1: Water Requirement Calculation
Calculate water requirements for each zone:
- Reference evapotranspiration rates from climate data
- Plant factor calculation by plant type and growth stage
- Zone area and application rate calculation
- Seasonal water requirements
- Peak demand calculation

### Step 2: Irrigation Method Selection
Select appropriate irrigation methods for each area:
- Sprinkler type by plant type (trees, shrubs, groundcover, lawn)
- Drip irrigation for feature planting and sensitive areas
- Rotary sprinklers for large open areas
- Consider wind patterns, topography, and microclimates

### Step 3: Sprinkler Layout and Coverage
Design sprinkler head layout for complete coverage:
- Head spacing based on manufacturer specifications
- Coverage overlap for uniform distribution
- Zone division by water requirement and plant type
- Pipe routing and pressure calculations

### Step 4: Controller Programming
Develop irrigation controller program:
- Zone scheduling based on water requirements
- Seasonal adjustments for climate variation
- Rain sensor and weather-based adjustments
- Cycle and soak for sloped or slow-drain areas

### Step 5: Commissioning and Testing
Define commissioning requirements:
- Pressure testing and leak checking
- Coverage verification and uniformity testing
- Controller programming verification
- Water efficiency verification against design calculations

## Success Criteria
- Calculated water requirements match site needs
- Sprinkler coverage provides uniform distribution
- Zones are divided appropriately by water requirement
- Controller programming meets seasonal requirements
- Commissioning procedures verify system performance

## Common Pitfalls
1. Under-sizing water requirements → Verify plant factors and evapotranspiration rates
2. Poor overlap between sprinklers → Verify head-to-head coverage design
3. One zone for mixed plant types → Separate zones by water requirement
4. Seasonal adjustments not programmed → Ensure controller supports multiple programmes

## Cross-References
- `landscaping-planting-plan/SKILL.md` — Plant types for water requirement calculation
- `landscaping-maintenance-programme/SKILL.md` — Irrigation maintenance from design specs