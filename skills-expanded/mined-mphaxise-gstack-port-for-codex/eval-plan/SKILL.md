---
name: eval-plan
description: Design a preregistered comparison of model, prompt, or skill variants with a baseline, blind scoring, a dry run and a bounded pilot.
---

# Plan a model or skill evaluation

Write the decision first. Name the baseline, the hypothesis, representative
held-out tasks, success threshold, failure conditions, and stop rule before
seeing results. For a skill evaluation include a plain-model arm. Keep the
model, effort, tools, and input fixed across a prompt comparison.

Pass the real input shapes through a stub and the actual grader. Include a
known failure to check that the grader rejects it. Withhold the arm label and
expected answers from the candidate. Record quality, time, usage and cost
separately. Keep the judge blind to the arm label when judgment is involved.

Price each arm before a paid pilot. Execute a pilot or full run only within
the user's authorized spend. Use measured pilot usage to estimate a range
for the full comparison. Report paired outcomes and uncertainty alongside
baseline performance. A pilot establishes feasibility and cost.

[Upstream evaluation protocol](https://github.com/garrytan/gstack/tree/76535826f5d50c721f95820f300037a3efe833a9/eval-plan)
