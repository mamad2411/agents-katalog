---
name: puda-workflows
description: Discover PUDA experiment workflows and choose the right experiment for the task. Use when you need to run, set up, or understand a PUDA experiment such as colour mixing optimization.
---

# PUDA workflows

## Goal

Provide experiment-selection and workflow guidance for PUDA workflows, then load the correct experiment reference before execution.

## Critical Rule

If you are unsure which experiment matches the user's task, **ask the user** before proceeding.  
Do **not** assume.

## Experiment Capabilities and When to Use

### Colour Mixing Optimization (`colour-mixing-opt`)

Use for **iterative RGB colour mixing to match a target colour via RMSE minimization**.

Capabilities:
- Automated liquid handling on Opentrons OT-2 to mix R, G, B dye volumes
- Camera capture of mixed colour after each dispensing step
- VLM-based image processing and ROI extraction for per-well RGB measurement
- RMSE calculation between mixed and target colour
- Bayesian Optimization (BO) or LLM-driven suggestion of next volume ratios
- Iterative protocol generation and execution until stop condition is reached
- Per-iteration report generation (volumes, RGB, RMSE, next suggestion)

Use this experiment when:
- The user wants to mix colours to match a target RGB
- The task involves optimizing volume ratios of dyes to minimize colour error
- The user mentions colour mixing, RMSE, BO, or LLM-guided liquid handling

Runner script: [`scripts/run_colour_mixing.py`](scripts/run_colour_mixing.py)
- End-to-end experiment runner; edit the config block at the top to change parameters
- Set `ROBOT_IP` to the OT-2 IP address for fully automated protocol execution via HTTP API
- Set `OPENROUTER_API_KEY` environment variable before running
- Outputs: generated protocols in `protocols/`, corrected images in `images/`, live report in `reports/report.md`

Before running:
- Refer to: [colour-mixing-opt](references/colour-mixing-opt.md)
- See optimization details: [optimization.md](references/optimization.md)
- See image processing details: [image-processing.md](references/image-processing.md)
- Optimizer classes: [scripts/optimizers.py](scripts/optimizers.py)
- RMSE utility: [scripts/rmse.py](scripts/rmse.py)
- Image processing pipeline: [scripts/image_processing.py](scripts/image_processing.py)

### Viscosity Optimization (`viscosity-optimization`)

Use for **iterative tuning of Opentrons OT-2 liquid handling parameters for viscous fluids using gravimetric feedback**.

Capabilities:
- Automated protocol generation and execution on Opentrons OT-2
- Concurrent gravimetric data collection from a mass balance (4 Hz) during each run
- Automatic data processing: outlier removal, phase slicing, normalisation
- Transfer error calculation (signed and absolute, in µL)
- Bayesian Optimization (LCB or EI) or LLM-driven suggestion of next protocol parameters
- Optimizable parameters: flow rates, delays, aspirate/dispense offsets
- Per-iteration report generation (params, signed error, absolute error)

Use this experiment when:
- The user wants to improve pipetting accuracy for viscous or non-water liquids
- The task involves tuning flow rate, delay, or offset parameters to minimize transfer error
- The user mentions gravimetric calibration, balance feedback, or viscosity optimization
- The user mentions BO, LCB, EI, or LLM-guided pipetting parameter optimization

Before running:
- Refer to: [viscosity-optimization](references/viscosity-optimization.md)

---

## Selection Workflow

1. Parse user intent and identify the experiment type.
2. Match intent to the experiment capabilities above.
3. If experiment selection is unclear or ambiguous, **ask the user** and wait for confirmation.
4. Load the corresponding reference file.
5. Proceed with the experiment workflow only after the experiment is confirmed.

## Output Guidance

When answering experiment-selection questions:
- State the recommended experiment and a one-line reason tied to its capability.
- If uncertain, ask a direct clarification question instead of guessing.

## Critical Rules

1. Always ask for all required inputs (target colour, thresholds, limits, deck layout) **before** starting any experiment.
2. Ask the user for the **OT-2 robot IP address** before running — set it as `ROBOT_IP` in the runner script.
3. Ask the user for the **OpenRouter API key** if not already set in the environment.
4. Invoke **puda-memory** after every protocol creation and run to keep `experiment.md` current.
5. Opentrons protocols must always end with no tip attached to any pipette.
6. Ask user if unsure — do not assume.
