---
name: let-it-rip
description: "Implement or fix an experiment in a Jupyter notebook from its experiment doc and pipeline, expectation-first: run every cell, review the result with /exp-review, then commit. Use when the experiment is planned and it is time to write the code."
disable-model-invocation: true
mode: true
icon: crown
color: yellow
---

Run this implementation or fix in a sub-agent. 

Implement the work described by the user in the docs at `docs/experiments-doc/<related_name.md>`, with the pipeline workflow in `docs/experiments-pipeline/<related_name.md>`. The code must satisfy the requirements described in both documents, when both exist.

If you are using the experiment pipeline, update the doc at the end of each experiment.

## Workflow

1. Load the development-principle skills below if needed:
  - **expectation-driven-science**: Development guide for the data-science process.
  - **developing-data-science-notebooks**: Development rules for writing usable, higher-quality notebooks in a data-science context.

2. Create the .env with uv if it does not exist, and use it to run.

3. For each cell you write, run it to make sure it works.

4. Once finished, before returning to the main agent, call the Skill tool with "exp-review" to review the work, and fix everything that is needed.

5. Commit your work to the current branch.