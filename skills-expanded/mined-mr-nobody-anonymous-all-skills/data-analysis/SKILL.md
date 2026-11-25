---
name: data-analysis
description: Analyze data files (CSV, JSON, tabular) — load, profile, transform, summarize, and visualize.
category: research
aliases:
- analyze-data
- csv-analysis
- statistics
- explore-data
triggers:
- analyze this data
- what's in this CSV
- explore this dataset
- data analysis
- statistics on this
keywords:
- data
- analysis
- csv
- pandas
- dataframe
- statistics
- explore
- profile
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- analysis
- csv
- data
- pandas
- research
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Data Analysis

## Purpose

Load, profile, transform, and summarize data. Identify patterns, anomalies, and summary
statistics. Communicate findings clearly.

## When to Use

- User provides a data file
- User wants summary statistics
- User wants to find patterns / outliers

## When NOT to Use

- Data is unclear / unsourced (ask first)
- Visualizations are the only goal (route to `data-visualization`)

## Capabilities

- Load CSV / JSON / Parquet
- Profile schema, types, missing values
- Compute summary stats
- Group, filter, transform
- Basic statistical tests (correlation, t-test, chi-square — with caveats)
- Visualization (plots, histograms)

## Inputs

- Data file or query
- Question of interest

## Workflow

1. **Load.** Inspect first rows, schema, dtypes.
2. **Profile.** Missing values, distributions, uniques.
3. **Clean.** Note data quality issues, handle or flag.
4. **Analyze.** Answer the user's question with operations on the data.
5. **Summarize.** Plain-language findings, with caveats.
6. **Visualize.** If helpful, recommend / produce a chart.

## Safety

- Don't claim causation from correlation
- Note sample size and representativeness
- Surface data quality issues before drawing conclusions

## Source

Custom skill, written for this library.

## Notes

Pairs with `data-visualization`, `report-generation`.

## Tools

- No mandatory tool unless declared in frontmatter.
- Use only project-approved tools and documented optional dependencies.

## Examples

Requests that should activate this skill include: "analyze this data"; "what's in this CSV"; "explore this dataset".
