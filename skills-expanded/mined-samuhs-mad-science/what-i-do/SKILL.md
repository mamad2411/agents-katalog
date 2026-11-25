---
name: what-i-do
description: "Orientation map and canonical catalogue of the mad-science data science skills. Use when the user asks how the skills fit together, which command to run next, where to start an experiment, or needs a quick overview of the hypothesis-to-notebook flow."
mode: true
icon: crown
color: purple
---

# What I Do

This skill is the orientation map for the experiment-driven workflow — and the **canonical catalog** of every skill in this repo. It explains how the data-science commands fit together, tells you which one to invoke next, and lists every skill with its role. It does not implement anything itself — it routes.

> **Catalog governance:** every skill in this repo must be registered here, below,
> before it is considered final. If a skill changes the experiment flow, the
> *Main Flow* and/or *Flow Checks* sections must be updated to reflect it. The
> `README.md` of the repo mirrors this file; this file wins on divergence.

## Main Flow: Hypothesis → Notebook Experiment

You have a hypothesis and want to test it. The flow has four steps, in order:

1. **`/hypothesys`** — Understand and sharpen the user's hypothesis through a short interview. This is the first step: it clarifies the hypothesis, the premises, and the goal metrics of the experiment before anything is built.
2. **`/to-doc`** — Write the experiment doc for the idea to be developed. This fixes and consolidates the ideas, giving the next step a stable contract to implement against.
3. **`/experiment-pipeline`** — Transform the doc into a pipeline workflow, breaking it into small slices to run and tracking the experiment rounds.
4. **`/let-it-rip`** — Implement the hypothesis safely in a notebook.
   - Follows the rules of `/expectation-driven-science` so the science code stays rigorous (expectation before trust, vertical slices, deviation-as-information).
   - Every implementation is reviewed by `/exp-review` to ensure the code state is correct before moving on.

## Standalone

Skills used on their own — independent from the main experiment flow, not a step in the hypothesis → notebook pipeline.

| Skill | Role | When to use |
|---|---|---|
| `/literature-research` | Deep research on high-trust primary sources; saves findings as Markdown | State of the art check, next to/after step 1 |
| `/to-article` | Turns experiment results/docs into a scientific-technical article | When results are ready to publish |
| `/mad-science-setup` | Configures repo layout and documents | Once, before first use of other skills |
| `/notify-gchat-human-wait` | Sends Google Chat card when agent waits for a human | Automation/operations (outside science flow) |
| `/critic-review` | Reviews the whole project — docs, experiments, results — against the state of the art and flags gaps, weak evidence, wrong assumptions | At the end of the project, or when you want a critical second look |
| `/experiment-graph` | Renders a read-only interactive graph of the pipeline doc — status, dependencies, critical path | Any time you need a visual overview of `docs/experiments-pipeline/*.md` |
| `/what-i-do` | This orientation map and canonical skill catalog | Whenever you don't know which skill to invoke next |

## Principles

Development principles — reference material that guides **how** to develop, not steps of the flow.

| Skill | Role | When to use |
|---|---|---|
| `/expectation-driven-science` | Hypothesis → prediction → verification discipline | Any analysis/model driven by explicit expectations |
| `/developing-data-science-notebooks` | Production-grade notebook practices (structure, modularization, reproducibility) | Creating/refactoring/reviewing notebooks |


## Flow Checks

| Phase | Goal | Output | Prevents |
|---|---|---|---|
| `/hypothesys` | Clarity of the question | Hypothesis + premises + goal metrics | Undefined falsifiability (hindsight) |
| `/to-doc` | Experiment contract | Doc with baseline, metrics, validation | Trust before expectation |
| `/experiment-pipeline` | Slice-based execution | Sliced pipeline + tracked rounds | Untracked experiment rounds |
| `/let-it-rip` | Rigorous implementation | Notebook + expectation-driven rules | Ad-hoc science code |
| `/exp-review` | Final verification | Approved code state | Unreviewed error / bias |