---
name: temperature-simulation-manus-familytools-fullinstr-v2-skill
description: Family-scoped SkillLearnBench skill for temperature-simulation using latest full-instruction v2 family injection.
allowed-tools:
  - glm_compute_public_metrics
  - glm_parameter_sweep
  - glm_run
  - list_dir
  - netcdf_summary
  - nml_edit_params
  - nml_read_params
  - read_file
  - run_python
  - run_shell
  - write_file
  - write_json
metadata:
  benchmark: SkillLearnBench
  generator: Manus
  baseline: manus_familytools_fullinstr_v2
  generation_constraints: slb_no_instance_memory_familytools_v2
  allowed_gold_input: familytools_full_instruction_v2
  skill_injection_scope: family_scoped
  date: "2026-05-23"
---

# Skill: Temperature Simulation

## When to use this skill
Use this skill for `temperature-simulation` tasks to run the General Lake Model (GLM), calibrate allowed parameters within published ranges, and evaluate vertical water temperature simulations using exact RMSE metrics.

## Visible input and artifact inventory
**Inputs:**
- Forcing data in `/root/bcs/`
- Observations at `/root/field_temp_oxy.csv`
- Initial config at `/root/glm3.nml`
- Executable at `/root/glm`

**Artifacts:**
- Simulation output at `/root/output/output.nc`
- Evaluation metrics at `/root/metrics.json`

## Execution procedure for the current task
1. **Assess**: Read instructions to identify allowed calibration parameters, their ranges, and target RMSE thresholds.
2. **Baseline**: Use `nml_read_params` to check initial parameters. Run `glm_run` and compute baseline metrics with `glm_compute_public_metrics`.
3. **Calibrate**: Adjust allowed parameters using `nml_edit_params` or `glm_parameter_sweep`. Ensure changes stay within published ranges.
4. **Evaluate**: After adjustments, use `glm_compute_public_metrics` to calculate exact RMSE metrics based on matched observation/simulation pairs. Do not use interpolation.
5. **Finalize**: Once RMSE thresholds are met, ensure parameters are saved in `/root/glm3.nml`. Run `glm_run` to generate the final `/root/output/output.nc`.
6. **Report**: Save final metrics to `/root/metrics.json` using `write_json`, ensuring all required keys are present.

## Family tool routing and useful placeholder snippets
- **Read Params**: `nml_read_params` extracts current values safely.
- **Edit Params**: `nml_edit_params` modifies parameters. Example: `nml_edit_params(nml_path="/root/glm3.nml", params={"Kw": 0.3})`.
- **Run Model**: `glm_run` executes the simulation.
- **Compute Metrics**: `glm_compute_public_metrics` calculates required RMSE values directly, handling exact datetime and rounded-depth merging.
- **Sweep Params**: `glm_parameter_sweep` systematically explores the parameter space.

## Validation checks before final submission
- `/root/glm3.nml` contains modifications ONLY to explicitly allowed parameters.
- Final parameter values are strictly within published ranges.
- `/root/output/output.nc` exists and matches the final parameter set.
- `/root/metrics.json` exists, contains all required keys, and satisfies RMSE thresholds.

## Common failure modes and repair actions
- **Out of Bounds**: Parameter outside allowed range. *Repair*: Use `nml_edit_params` to correct the value.
- **Unauthorized Changes**: Modifying unlisted parameters. *Repair*: Revert unauthorized changes in `/root/glm3.nml`.
- **Incorrect Metrics**: Using custom scripts instead of exact matching. *Repair*: Rely exclusively on `glm_compute_public_metrics`.
- **Missing Output**: Failing to run the model after final adjustment. *Repair*: Execute `glm_run` before writing metrics.

## Finalizer capsule
If nearing the maximum step limit without finding optimal parameters, restore the environment to a valid state. Ensure `/root/glm3.nml` contains parameters within allowed ranges. Run `glm_run` to generate `/root/output/output.nc` and use `glm_compute_public_metrics` to generate `/root/metrics.json`. Submitting a valid, complete set of artifacts with suboptimal performance is better than an invalid state.
