---
name: cma-issue-to-pr-pipeline
description: Autonomous end-to-end issue resolution pipeline using Claude Managed Agents. Multi-turn reproduction, test-driven fixing, CI failure recovery, and automated pull request generation.
---

# Autonomous Issue-to-PR Pipeline Architecture

## Pipeline Stages
1. **Issue Analysis & Grounding:** Agent parses the issue description and reproduces the failure with an automated test case.
2. **TDD Fix Execution:** Modifies minimal code lines to satisfy the failing test while preserving existing test passes.
3. **CI Simulation & Recovery:** Simulates local build and test pipelines, iteratively resolving compilation or lint errors.
4. **PR Synthesis:** Formulates structured PR title, intent summary, diff explanation, and verification proof.
