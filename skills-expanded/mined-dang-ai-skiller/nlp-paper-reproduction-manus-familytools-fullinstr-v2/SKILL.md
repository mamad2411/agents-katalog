---
name: nlp-paper-reproduction-manus-familytools-fullinstr-v2-skill
description: Family-scoped SkillLearnBench skill for nlp-paper-reproduction using latest full-instruction v2 family injection.
allowed-tools:
  - list_dir
  - read_file
  - simpo_loss_prepare
metadata:
  benchmark: SkillLearnBench
  generator: Manus
  baseline: manus_familytools_fullinstr_v2
  generation_constraints: slb_no_instance_memory_familytools_v2
  allowed_gold_input: familytools_full_instruction_v2
  skill_injection_scope: family_scoped
  date: "2026-05-23"
---

# Skill: nlp-paper-reproduction

## 1. When to use this skill
Use this skill when tasked with reproducing code repositories for NLP papers, specifically focusing on implementing loss functions (like SimPO loss) and computing deterministic reproduction artifacts. This skill is applicable when the task requires patching minimal paths, inspecting visible tensors/scripts, and recording Python/package metadata without heavy retraining.

## 2. Visible input and artifact inventory
- **Visible Inputs:**
  - Task instructions detailing the required implementation (e.g., `simpo_loss` function in `SimPOTrainer`).
  - Source code files (e.g., `/root/SimPO/scripts/simpo_trainer.py`).
  - Reference papers (e.g., `/root/SimPO/paper.pdf`).
  - Unit test files (e.g., `/root/SimPO/unit_test/unit_test_1.py`).
  - Environment configuration files (e.g., `Dockerfile`, `environment.yml`).
- **Artifact Inventory:**
  - Computed loss values saved in a specific format (e.g., `/root/loss.npz` with key `losses`).
  - Python version and package metadata logs (e.g., `/root/python_info.txt`).

## 3. Execution procedure for the current task
1. **Inventory and Read:** Begin by reading the visible instruction and inventorying visible files before creating any artifacts. Extract required output paths, schemas, constraints, and source data exclusively from prompt-visible files.
2. **Environment Setup:** Ensure the correct environment is set up for the project. Resolve or replace any existing components that conflict with the project requirements.
3. **Implementation:** Implement the required function (e.g., `simpo_loss`) based on the provided reference paper. Patch the minimal path necessary for the loss computation.
4. **Testing and Generation:** Run the provided testing code (e.g., `unit_test_1.py`) to generate the loss for evaluation using fixed input tensors. Ensure the output is deterministic.
5. **Artifact Creation:** Save the computed values to the specified output path (e.g., `/root/loss.npz`) using the required key (e.g., `losses`).
6. **Metadata Logging:** Log the Python version and installed packages using commands like `python -VV` and `python -m pip freeze` to the specified file (e.g., `/root/python_info.txt`).

## 4. Family tool routing and useful placeholder snippets
- **`list_dir`**: Use to explore the directory structure and locate necessary files (e.g., scripts, unit tests, environment files).
- **`read_file`**: Use to read the contents of source code, configuration files, and reference papers to understand the implementation requirements.
- **`simpo_loss_prepare`**: Prefer this family-specific operation tool over ad hoc shell code when preparing the environment or data for SimPO loss computation.

*Placeholder Snippet for Metadata Logging:*
```bash
python -VV > /root/python_info.txt
python -m pip freeze >> /root/python_info.txt
```

## 5. Validation checks before final submission
- Verify that the implemented function correctly computes the loss based on the reference paper.
- Ensure the output artifact (e.g., `/root/loss.npz`) exists at the correct path and contains the required key (e.g., `losses`).
- Check that the metadata log (e.g., `/root/python_info.txt`) contains both the Python version and the package list.
- Confirm that no unit test files were modified if prohibited by the instructions.

## 6. Common failure modes and repair actions
- **Failure:** Environment conflicts prevent the code from running.
  - **Repair:** Inspect the `Dockerfile` or `environment.yml` and resolve conflicts by replacing or updating packages as needed.
- **Failure:** The output artifact is missing or has the wrong key.
  - **Repair:** Review the saving logic in the implementation and ensure it matches the requested schema (e.g., `np.savez('/root/loss.npz', losses=...)`).
- **Failure:** The computed loss is incorrect or non-deterministic.
  - **Repair:** Re-read the reference paper and verify the mathematical implementation of the loss function. Ensure fixed input tensors are used correctly.

## 7. Finalizer capsule
Before finalizing the task, ensure the minimum required artifacts exist at their visible paths and their shapes match the instruction. Run lightweight public sanity checks using visible files or tool summaries. Repair the first concrete mismatch found. Finalize only after confirming the presence and correctness of the output artifacts (e.g., `/root/loss.npz` and `/root/python_info.txt`).
