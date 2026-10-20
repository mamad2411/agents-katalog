---
name: five-whys-root-cause-analyzer
description: "Apply Five Whys rigorously to trace issues to root causes and define durable corrective actions. USE WHEN a task matches the Craft workspace workflow for five-whys-root-cause-analyzer."
cluster: quality-eval
version: 1.0.0
origin: "craft-agent workspace"
---

# Five Whys Root Cause Analyzer

Use this skill for structured root-cause analysis when users report recurring problems or unclear failures.

## Trigger Conditions
- User asks for root cause analysis
- User mentions recurring issue or repeated failure
- User asks to apply Five Whys

## Required Inputs
1. Problem statement
2. Symptoms and evidence
3. Timeline/context of occurrence
4. Stakeholders/systems involved

## Workflow
1. **Problem definition**: state issue in observable, measurable terms.
2. **Five Whys chain**: ask successive why questions with evidence checks.
3. **Root cause validation**: test if cause explains repeated symptoms.
4. **Corrective actions**: design fixes at system/process level.
5. **Prevention plan**: define controls and monitoring.

## Output Format
- Problem statement
- Five Whys chain
- Confirmed root cause(s)
- Corrective + preventive actions (CAPA)
- Verification checklist

## Guardrails
- Don’t stop at superficial or person-blame causes.
- Require evidence at each why step.
- Include system-level prevention measures.
