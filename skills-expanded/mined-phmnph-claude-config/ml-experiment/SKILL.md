---
name: ml-experiment
description: Plan, run, or assess an ML model comparison with a reproducible baseline, valid split, and bounded compute budget.
---

# Answer an ML hypothesis

Use this for an experiment decision, not an ordinary model API bug or a general
literature survey. Establish which stage the user requested: protocol, execution,
or analysis. Reuse an existing protocol and run artifacts rather than restarting
the process. Read [PROTOCOL.md](PROTOCOL.md) for the checks relevant to that stage.

Define the hypothesis and decision rule before interpreting candidate results.
Choose a credible baseline, data split, metric, and cheapest informative run from
project evidence. Explain material tradeoffs and ask only for missing goals,
permissions, or resource limits that affect the experiment. A local smoke check
within existing authorization does not require another approval round.

For execution, first check data and calculations on a small sample. Use $tdd for
changes to preprocessing, metrics, or other code behavior; numerical assertions
need independent expected values. Tests of code do not establish model quality.
Record dataset/split identity, code revision and uncommitted changes, parameters,
environment, seeds, commands, run IDs, failures, metrics, and resource use.

Follow the existing platform's run procedure. Use separately installed ml-dev
skills only for projects on that platform. Honor the agreed compute budget and
stop on invalid comparison, exhausted budget, or missing required authorization.
Do not infer permission for deployment from permission to run an experiment.

For analysis, check comparability before ranking models. Report the effect,
uncertainty, important slices, cost, and limitations. Distinguish feasibility,
predictive improvement, and production readiness. Inconclusive or negative
results are valid outcomes. Recommend retaining the baseline, one bounded next
experiment, or implementation preparation according to the decision rule.
Save a concise protocol or report with artifact links and reproduction steps.
