---
name: leeway-candidate-search-repair
description: Candidate-generation and repair behavior for exploring alternative plans/states, diagnosing constraint failures and iterating before real execution.
license: MIT
---
# LeeWay Candidate Search & Repair

Generate candidates that differ in meaningful mechanism/provider/sequence, not superficial wording. Evaluate hard gates first. On failure isolate violated constraints and repair only affected dimensions. Maintain rejected candidates/reasons to avoid cycling. Stop only at ACCEPTED candidate or VERIFIED_BLOCKER.
