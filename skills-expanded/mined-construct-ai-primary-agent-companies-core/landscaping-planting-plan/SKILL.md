---
title: Landscaping Planting Plan
description: Automated generation of planting plans including climate-appropriate plant selection, quantities, spacing, and soil preparation requirements
frequency: Per zone or landscape area
success_rate: 95%
tags:
  - domainforge_ai
  - landscaping
  - planting-plan
  - 03000_landscaping
docs:
  - docs_construct_ai/disciplines/03000_landscaping/agent-data/domain-knowledge/03000_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/03000_landscaping/agent-data/prompts/03000_AI-NATIVE-LANDSCAPING-PROMPT.md
---

# Landscaping Planting Plan

## Overview
Automated generation of planting plans including climate-appropriate plant selection, quantities, spacing, soil preparation requirements, and installation notes. Primary agent: 03000-001 Planting Plan Agent.

## Triggers
- Landscape design brief received
- Planting plan requested for zone
- Plant palette change requested
- Soil conditions identified for zone

## Prerequisites
- Design brief with landscape intent
- Climate zone and soil analysis data available
- Plant database with climate, soil, and water requirements
- Area measurements and site constraints

## Steps

### Step 1: Site Analysis
Gather site data for the zone:
- Climate zone, exposure, aspect, wind patterns
- Soil type, pH, drainage, compaction
- Sun/shade patterns throughout the day
- Existing vegetation and removal requirements
- Space constraints including utilities, structures

### Step 2: Plant Selection
Select plants appropriate for the zone:
- Filter database for climate and soil appropriate species
- Consider design intent: screening, groundcover, feature planting
- Calculate mature size and spacing requirements
- Check biodiversity and native species requirements
- Verify availability and establishment requirements

### Step 3: Layout and Quantities
Generate plant layout and schedule:
- Calculate quantities from area and spacing
- Define layers (canopy, understory, shrub, groundcover)
- Specify sizes (CAL, H, container size)
- Generate plant list with quantities, sizes, spacing
- Include planting method notes for each type

### Step 4: Soil Preparation Requirements
Specify soil preparation for the zone:
- Topsoil testing results and required amendments
- pH adjustment requirements
- Organic matter or fertiliser application rates
- Drainage improvement if required
- Grading requirements for planting

### Step 5: Establishment and Maintenance Requirements
Document establishment needs:
- Watering requirements during establishment period
- Protection from wind, sun, traffic
- Maintenance schedule during establishment
- Plant health monitoring requirements
- Expected establishment timeline

## Success Criteria
- All plants appropriate for climate and zone conditions
- Layout provides layered planting for visual effect
- Quantities accurately calculated from area and spacing
- Soil preparation recommendations based on test results
- Establishment requirements documented for handover

## Common Pitfalls
1. Inappropriate species for climate → Verify climate zone and hardiness
2. Spacing not accounting for mature size → Consider mature size at installation
3. No soil preparation specified → All zones require soil improvement
4. Establishment period underestimated → Native species may establish in 12-24 months

## Cross-References
- `landscaping-irrigation-design/SKILL.md` — Plant water requirements for irrigation
- `landscaping-maintenance-programme/SKILL.md` — Maintenance from planting plan