---
name: bi-powerbi-dax-optimization
description: "Profile, debug, and optimize DAX queries and calculated measures using DAX Studio and Tabular Editor to eliminate expensive row-context transitions."
category: business-intelligence
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - business-intelligence
  - powerbi
  - dax
  - tabular-editor
  - performance
---

# Power BI DAX Performance Optimization

## Overview & Core Principles
Profile, debug, and optimize DAX queries and calculated measures using DAX Studio and Tabular Editor to eliminate expensive row-context transitions.

### Profiling Workflow & Invariants
1. **Filter Context vs. Row Context**: Replace nested `CALCULATE` inside `FILTER` iterators (`SUMX`, `AVERAGEX`) with pre-filtered scalar variables.
2. **Columnar Compression & VertiPaq**: Ensure high-cardinality columns (e.g. timestamps, GUIDs) are separated into date and time integer keys to maximize Run-Length Encoding (RLE) and bit-packing ratios.
3. **Evaluation Tracing**:
   - Capture Server Timings (SE CPU vs FE CPU). Keep FE CPU below 20% of total query execution time.
   - Look for xmSQL callback operations (`CallbackDataID`); rewrite DAX expressions to push computation down into the VertiPaq storage engine.
4. **Implementation Example**:
```dax
// Optimized Revenue Prior Year Measure
Revenue PY :=
VAR CurrentYear = SELECTEDVALUE('Date'[CalendarYear])
RETURN
    IF(
        NOT ISBLANK(CurrentYear),
        CALCULATE(
            [Total Revenue],
            SAMEPERIODLASTYEAR('Date'[Date])
        )
    )
```
5. **Quality Checklist**:
   - Zero synthetic bidirectional cross-filtering relationships in the star schema.
   - Star schema dimension tables have integer surrogate primary keys and 1-to-many single-directional relationships.
