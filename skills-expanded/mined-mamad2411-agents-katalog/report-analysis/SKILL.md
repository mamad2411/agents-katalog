---
name: deep-analyze-report-analysis
description: Generate an analysis report — structure overview, root cause chains, evidence, recommendations
argument-hint: "[scope]"
related:
  - report
  - create-report-in-dot-devin
---

## Goal

Turn the result of `/deep-analyze` into an analysis report — structure, findings, and root cause chains with evidence

## Scope

- Use when `/deep-analyze` dispatches to `report`, or invoke standalone against existing analysis results
- Covers: codebase structure, findings per area, root cause chains, tool/CLI analysis
- Output: tables in chat, or a persistent artifact via `/create-report-in-dot-devin` if the user asks

## Execute

### 1. Organize Analysis

> Goal: arrange the analysis into categories that support decisions

1. Group findings by area: structure, dependencies, data flow, error paths
2. Build root cause chains: symptom → cause → origin for key findings
3. Attach evidence (file:line, command output) to every finding

### 2. Build Report

> Goal: a report that directly answers the analysis question

1. Summary — always lead with the answer to the analysis question
2. Tables: `No.`, `Area`, `Finding`, `Evidence`, `Impact`
3. Root cause chains as numbered steps for complex findings
4. Diagram/visualization references if the analysis produced any

### 3. Recommendations

> Goal: actionable output, not just narration

1. Recommendations list ordered by impact/effort
2. Distinguish quick wins vs structural changes
3. If archiving is needed → run `/create-report-in-dot-devin`

## Rules

- The main answer must be at the top — the report supports, it doesn't lead
- Every claim has evidence — without one, label it a hypothesis
- Clearly separate "actually found" from "likely"

## Expected Outcome

- An analysis report that answers the question directly, with evidence and recommendations
