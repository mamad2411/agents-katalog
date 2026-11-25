---
name: guardrail-designer
description: Design practical limits, thresholds, and operating constraints that keep a plan or system safe enough to proceed. Use when work should continue, but only inside clearly defined boundaries.
---

# Guardrail Designer

## Goal

Define the minimum constraints needed to keep a plan inside safe operating limits.

This skill does not stop work by default. It translates known risks into explicit boundaries, tripwires, and do-not-cross conditions.

## When To Use

- after failure modes are known
- before risky execution
- when a plan needs safe operating limits rather than broad caution

## Scope Boundaries

In scope:

- define red lines and thresholds
- name stop conditions and fallback conditions
- convert vague caution into explicit boundaries

Out of scope by default:

- broad policy writing
- full compliance frameworks

## Workflow

1. State the action or system.
2. Identify the risk areas that need control.
3. Define operating limits.
4. Define stop triggers.
5. Define fallback or escalation response.

## Output Contract

1. `protected_action`
2. `risk_areas`
3. `guardrails`
4. `stop_triggers`
5. `fallback_conditions`
6. `recommended_followup`
7. `next_step`

## Guardrails

- Do not write abstract "be careful" rules.
- Keep guardrails observable and actionable.
- Prefer a small set of hard constraints over a long soft checklist.
