---
title: Landscaping Plant Health Analysis
description: Assessment of plant health from photos including disease identification, pest damage, water stress, and growth tracking
frequency: Per photo assessment or monitoring request
success_rate: 90%
tags:
  - domainforge_ai
  - landscaping
  - plant-health-analysis
  - 03000_landscaping
docs:
  - docs_construct_ai/disciplines/03000_landscaping/agent-data/domain-knowledge/03000_DOMAIN-KNOWLEDGE.MD
---

# Landscaping Plant Health Analysis

## Overview
Computer vision-based assessment of plant health from photos including disease identification, pest damage, water stress detection, and growth tracking. Primary agent: 03000-006 Plant Health Analysis Agent.

## Steps
1. **Image Preprocessing** → Prepare photo for analysis (crop, resize, normalise)
2. **Plant Detection** → Identify all plants in the image
3. **Health Assessment** → Analyse each plant for: colour (chlorosis), leaf condition (wilting, spotting), growth rate, pest damage, disease symptoms
4. **Classification** → Classify health status: Healthy, Stressed, Diseased, Pest-affected
5. **Recommendation** → Generate treatment recommendation based on diagnosis
6. **Documentation** → Log health assessment with evidence, location, and date

## Cross-References
- `landscaping-establishment-monitoring/SKILL.md` — Health data for establishment tracking