---
name: knowledge-base-gap-finder
description: Identify what documentation is missing by comparing support issues, product behavior, and existing docs. Use when the knowledge base is incomplete or stale.
---

# Knowledge Base Gap Finder

## Overview

Identify what documentation is missing by comparing support issues, product behavior, and existing docs.

## Core Workflow

1. Inspect the relevant diffs, configs, source files, or artifacts before forming a conclusion.
2. Compare the current state against repo conventions, expected guarantees, and known risk areas.
3. Prioritize the highest-impact gaps, regressions, or improvement opportunities instead of surface-level noise.
4. Recommend the smallest high-leverage changes and the checks that would validate them.

## Deliver

- Ranked findings or improvement opportunities with clear evidence.
- The main risks, tradeoffs, or regressions that matter most.
- Validation steps or follow-up edits that would reduce risk.

## Guardrails

- Lead with findings, not generic praise or low-value commentary.
- Use repo evidence and surrounding context instead of reviewing in isolation.
- Flag missing validation when a recommendation depends on behavior you could not confirm.
- Do not invent metrics, policy decisions, customer commitments, or ownership that the inputs do not support.
