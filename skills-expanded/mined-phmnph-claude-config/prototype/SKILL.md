---
name: prototype
description: Build a small disposable artifact to answer a specific UI, logic, data, or feasibility question.
---

# Prototype a question

State the question, what observation would answer it, and the available budget.
Choose the cheapest format that exposes the uncertainty. Read only the matching
reference; the formats below are options, not a mandatory sequence.

- **UI alternatives:** [UI.md](UI.md) when comparing visual arrangements.
- **Interactive state transitions:** [LOGIC.md](LOGIC.md) when someone needs to
  drive a state model by hand. HTML is useful here, not required for all logic.
- **Data, numerical logic, model feasibility:** [EXPERIMENT.md](EXPERIMENT.md)
  for a script, notebook, benchmark, or small data sample. Use $ml-experiment
  when the question is a model-quality comparison requiring a valid protocol.

Keep the artifact isolated and clearly provisional. Use the project's existing
runtime and conventions. Restrict persistence and external mutations to what the
question actually requires and the user authorized. Verify that the artifact
runs and that its output can answer the question; numerical checks are warranted
when an incorrect calculation would invalidate the result.

Stop when the question is answered, the budget is exhausted, or a named blocker
prevents the observation. Report the answer, its evidence and limits, and the
artifact path or reproduction command. Retain it according to the caller's
request and repository conventions; do not create a branch or commit by default.
Promotion into production is a separate implementation task with appropriate
TDD and review, not an automatic consequence of a successful prototype.
