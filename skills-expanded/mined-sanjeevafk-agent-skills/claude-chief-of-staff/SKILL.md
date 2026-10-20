---
name: claude-chief-of-staff
description: Architectural blueprint for an executive Chief of Staff agent powered by Claude Agent SDK. Handles cross-stream information synthesis, priority triage, talent scoring, financial forecasting, and multi-criteria decision matrices.
---

# Claude Chief of Staff Agent Architecture

## Overview
The Chief of Staff pattern establishes an executive agent that synthesizes fragmented organizational inputs (communications, talent pipelines, financial forecasts) and translates them into structured decision matrices.

## Core Capabilities
1. **Communication & Priority Triage:** Ingests unorganized updates, ranks urgency vs. impact, and identifies critical path blockers.
2. **Financial Forecast Modeling:** Calls deterministic financial projection scripts to stress-test budget assumptions without arithmetic errors.
3. **Talent Scorer:** Evaluates candidate profiles against structured competency rubrics.
4. **Decision Matrix Synthesis:** Formulates weighted multi-criteria trade-off tables for executive reviews.

## Architecture Workflow
```
User Ingestion / Webhooks
         |
         v
+---------------------------------+
|   Chief of Staff Agent Core     |
|   (Claude 3.5 Sonnet / Opus)    |
+----------------+----------------+
                 |
  +--------------+--------------+
  |              |              |
  v              v              v
Financial      Talent        Decision
Forecast       Scorer        Matrix
(Scripts)     (Rubric)      (Weights)
```
