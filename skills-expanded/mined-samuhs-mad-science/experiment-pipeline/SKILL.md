---
name: experiment-pipeline
description: "Break an experiment doc into small vertical slices (stages, phases, experiments) with goals, metrics, status and dependencies, tracked in docs/experiments-pipeline. Use when the experiment contract is settled and the user wants a run plan, wants to know which experiments can run in parallel, or wants to update experiment status."
disable-model-invocation: true
mode: true
icon: crown
color: yellow
---

## Experiments Workflow

Based on the experiment doc, create the experiment pipeline. To do this, analyze the Experiment Stories to see which experiments will run and in what order, and check whether any of them can run in parallel with another.

The main idea is to break the experiments into small slices and create a file to help track the pipeline workflow.

Then show the workflow order to the user, broken down as a numbered list in this pattern:

<vertical-slice-rules>
### Experiment Stage <number> 
<description of the main idea of the stage>

#### Phase <number>

<description of the main idea of the phase>

#### Experiment <number>
**title**: short descriptive name
**Goals**: Experiment goals and the metric that will be checked.
**Status**: Control tag for the experiment; tell the user whether it is **not-implemented**, **waiting-to-run**, **running**, or **completed**.
**Blocked by**: Which other experiments (if any) must complete first.
**Result**: When status is **completed**, write here a short text about the result of experiment. 

</vertical-slice-rules>

When the workflow order is completed, ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct: does each experiment depend only on experiments that genuinely gate it?
- Should any experiments be merged or split further?

Then, if the user approves, write this document to `docs/experiments-pipeline/<name.md>`


