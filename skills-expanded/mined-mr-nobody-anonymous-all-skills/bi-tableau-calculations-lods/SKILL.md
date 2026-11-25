---
name: bi-tableau-calculations-lods
description: "Design enterprise Tableau data models utilizing FIXED, INCLUDE, and EXCLUDE Level of Detail expressions for complex cohort, market basket, and benchmark analytics."
category: business-intelligence
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - business-intelligence
  - tableau
  - lod
  - analytics
  - sql
---

# Tableau Advanced Calculations and Level of Detail (LOD) Expressions

## Overview & Core Principles
Design enterprise Tableau data models utilizing FIXED, INCLUDE, and EXCLUDE Level of Detail expressions for complex cohort, market basket, and benchmark analytics.

### LOD Evaluation Hierarchy & Context Filters
1. **Order of Operations**:
   - Extract Filters -> Data Source Filters -> Context Filters -> FIXED LOD Expressions -> Dimension Filters -> INCLUDE/EXCLUDE LOD Expressions -> Measure Filters -> Table Calculations.
2. **Archetypal LOD Use Cases**:
   - Customer First Purchase Cohort: `{FIXED [Customer ID] : MIN([Order Date])}`
   - Total Category Sales for Market Share: `[Sales] / {EXCLUDE [Sub-Category] : SUM([Sales])}`
   - Customer Order Frequency Benchmark: `{FIXED [Region] : AVG({INCLUDE [Customer ID] : COUNTD([Order ID])})}`
3. **Performance Invariants**:
   - Promote dimensional filters to Context Filters when FIXED expressions must respect user slicers.
   - Avoid nesting LODs across unindexed blended data sources.
