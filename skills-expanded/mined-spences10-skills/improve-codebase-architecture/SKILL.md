---
name: improve-codebase-architecture
# prettier-ignore
description: "Find AI-readiness architecture issues and module-deepening refactors. Use when improving codebase architecture, testability, agent navigation, seams, or refactor tickets."
metadata:
  last_updated: "2026-04-29"
  verified_against: "current local skill refresh"
---

<!-- Sources: https://www.youtube.com/watch?v=uC44zFz7JSM and https://www.youtube.com/watch?v=3MP8D-mdheA -->

# Improve Codebase Architecture

Your codebase is the real prompt. Use this skill to find places where agents will get lost, make scattered changes, or accelerate entropy, then turn them into human-approved module-deepening refactors.

Core stance: **agents are tactical programmers; the human is the strategic programmer**. Do not AFK-rewrite architecture.

## Quick Start

1. Explore the codebase like a new starter with no memory.
2. Return a numbered shortlist of deepening candidates; do not design solutions yet.
3. Ask: “Which candidate should we grill?”
4. Ground the chosen candidate in code, ask boundary questions, then sketch a deep/gray-box module.
5. If requested, create a focused RFC/issue for an implementation agent.

## Process

Explore for AI friction. Build the mental map exposed by the filesystem: product/domain areas, obvious public interfaces, tests/feedback loops, and places requiring too much hidden context. The friction you experience is signal.

Find deepening opportunities. Prioritize candidates that improve **locality** and **leverage**: duplicated domain rules, parallel implementations with no seam, shallow modules, arbitrary imports, missing boundary tests, and hard-to-discover public APIs.

Present candidates, not solutions. For each candidate include: modules involved, why this is AI friction, proposed deepening move, locality gain, leverage gain, seam/test impact, confidence, and risk. Then ask which candidate to grill.

Grill the chosen candidate. Ground it in concrete files, call sites, invariants, dependencies, and test gaps. Ask what the module owns, what interface callers should learn, what invariants tests must lock down, which dependencies need adapters, and how to migrate safely.

Sketch the module shape. Propose a deep/gray-box module: public interface/types, common usage example, hidden implementation details, seams/adapters, boundary tests, and migration steps. Optimize for progressive disclosure: agents should understand the module from interface/docs before reading internals.

Produce the handoff artifact. If the user wants follow-through, create a focused refactor RFC/issue. Do not implement broad architectural rewrites unless explicitly asked; if implementing, do one narrow module-deepening slice with tests.

## Reference

Read [REFERENCE.md](references/REFERENCE.md) for the glossary, candidate rubric, design prompts, dependency categories, and RFC template.
