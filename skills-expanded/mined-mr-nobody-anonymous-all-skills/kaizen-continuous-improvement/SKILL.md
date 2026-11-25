---
name: kaizen-continuous-improvement
description: Apply Toyota Kaizen principles and Plan-Do-Check-Act (PDCA) cycles to systematically eliminate waste (Muda) in daily workflows.
category: productivity
aliases:
- kaizen
- continuous-improvement
- pdca-cycle
- muda-elimination
triggers:
- apply Kaizen to my workflow
- continuous improvement PDCA
- eliminate waste in development process
- run a Kaizen workflow review
- identify Muda in my routine
keywords:
- kaizen
- pdca
- continuous-improvement
- toyota
- muda
- waste
- efficiency
- workflow
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
lifecycle: enabled
capabilities:
- waste-elimination
- pdca-cycle-execution
- workflow-streamlining
inputs:
- workflow_description
- recurring_friction
- cycle_time
outputs:
- kaizen_event_plan
- muda_audit
- standard_work_update
permissions:
  filesystem: none
  network: none
  shell: none
  secrets: none
author: Mr-Nobody-Anonymous
tags:
- continuous
- continuous-improvement
- improvement
- kaizen
- pdca
- productivity
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

# Kaizen Continuous Improvement

## Purpose
Applies Toyota Production System Kaizen methodologies and Plan-Do-Check-Act (PDCA) cycles to technical workflows. Systematically identifies and eliminates the 8 types of waste (Muda) to achieve compound micro-improvements.

## When to Use
- Development or operational processes feel sluggish, repetitive, or prone to recurring friction.
- Conducting sprint retrospectives, process post-mortems, or onboarding audits.
- Establishing standard work baselines to reduce variance across team operations.
- Engineering teams seeking small, continuous, sustainable daily workflow refinements.

## When NOT to Use
- Greenfield innovation where the core problem and workflow are not yet understood.
- One-time black-swan incident responses that require immediate triage rather than process refinement.

## Capabilities
- **Muda Waste Audit**: Classify waste across 8 dimensions (Waiting, Overproduction, Rework/Defects, Motion, Overprocessing, Inventory, Transport, Underutilized Talent).
- **PDCA Cycle Framework**: Guide iterative experiments (Plan -> Do -> Check -> Act) with measurable baselines.
- **Root-Cause Simplification**: Eliminate unnecessary steps rather than automating inefficient complexity.
- **Standard Work Documentation**: Codify proven optimizations into repeatable, living documentation.

## Inputs
- `process_description` (required) — Current workflow, ceremony, or technical routine.
- `known_friction` (optional) — Specific pain points, delays, or quality defects observed.
- `cycle_time` (optional) — Current elapsed time required to complete the process.

## Workflow
1. Map the current value stream: list every step required from start to finish.
2. Classify each step as value-add, necessary non-value-add, or pure waste (Muda).
3. Target the single largest source of delay or rework for a rapid PDCA experiment.
4. Formulate an actionable, low-cost intervention (Plan) and define success metrics.
5. Document standardized operating guidelines to lock in gains and prevent regression.

## Tools
- Value stream mapping and process audit checklists.

## Examples
- "Apply Kaizen to our code-review and deployment handoff process."
- "Identify Muda and waste in our daily standup and task tracking."
- "Run a PDCA cycle to reduce our PR review turnaround time."

## Safety
- Never eliminate safety checks, security gates, or testing stages under the guise of waste reduction.
- Focus on process ergonomics and friction removal rather than unsustainable pace increases.

## Source
Custom skill maintained in this library based on Lean and Toyota Kaizen operational models.

## Notes
Composes effectively with `productivity.first-principles-reasoning` and `development.git-workflow`.
