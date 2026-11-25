---
name: performance-optimization
description: Find and fix performance bottlenecks — profiling, measurement, and targeted optimization.
category: development
aliases:
- perf
- profiling
- bottleneck
- speed-up
triggers:
- this is slow
- profile this
- find the bottleneck
- speed this up
- performance optimization
keywords:
- performance
- slow
- profile
- bottleneck
- latency
- throughput
- optimize
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- bottleneck
- development
- optimization
- performance
- profile
- slow
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: write
credential_access: false
destructive_operations: false
---

# Performance Optimization

## Purpose

Identify performance bottlenecks via measurement and fix them with targeted changes.

## When to Use

- Code is too slow or uses too much memory
- User reports latency issues
- Scaling concerns

## Workflow

1. **Measure.** Always profile first. Don't optimize blind.
2. **Identify hotspot.** Where does time / memory actually go?
3. **Hypothesize.** Why is this slow?
4. **Fix.** Change one thing at a time.
5. **Re-measure.** Confirm improvement, check for regressions.
6. **Stop when good enough.** Don't optimize beyond the requirement.

## Safety

- Don't optimize prematurely
- Don't sacrifice readability for negligible wins

## Source

Custom skill, written for this library.

## Notes

Pairs with `debugging`, `architecture`.

## When NOT to Use

Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.

## Capabilities

- Apply the performance-optimization workflow consistently.
- Produce a clear, reviewable result.
- Surface assumptions, constraints, and unresolved risks.

## Inputs

- The user's goal and desired output.
- Relevant source material, constraints, and environment details.
- Acceptance criteria when available.

## Tools

- No mandatory tool unless declared in frontmatter.
- Use only project-approved tools and documented optional dependencies.

## Examples

Requests that should activate this skill include: "this is slow"; "profile this"; "find the bottleneck".
