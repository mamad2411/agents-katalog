---
name: cma-outcome-grader-loop
description: Iterative grade-and-revise evaluation architecture for autonomous agents. A primary generator agent drafts artifacts while an independent outcome grader validates claims against a strict rubric until verification gates pass.
---

# Outcome Grader Iteration Architecture

## Overview
A dual-agent loop that guarantees artifact rigor by separating generation from verification.

## Pipeline
1. **Generator Turn:** Agent produces initial artifact (report, code, plan).
2. **Stateless Outcome Grader:** An independent evaluation agent fetches references, runs tests, and scores the output against an immutable rubric.
3. **Feedback Loop:** If the score is below the acceptance threshold, concrete defect feedback is returned to the generator.
4. **Convergence Gate:** The loop terminates when the rubric passes or max iterations are reached.
