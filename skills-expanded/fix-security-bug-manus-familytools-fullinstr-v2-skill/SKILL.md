---
name: fix-security-bug-manus-familytools-fullinstr-v2-skill
description: Family-scoped SkillLearnBench skill for fix-security-bug using latest full-instruction v2 family injection.
allowed-tools:
  - apply_patch_text
  - diff_summary
  - export_patch
  - java_source_inspect
  - list_dir
  - maven_build
  - read_file
  - repo_search
  - run_shell
  - search_text
  - write_file
metadata:
  benchmark: SkillLearnBench
  generator: Manus
  baseline: manus_familytools_fullinstr_v2
  generation_constraints: slb_no_instance_memory_familytools_v2
  allowed_gold_input: familytools_full_instruction_v2
  skill_injection_scope: family_scoped
  date: "2026-05-23"
---

# Skill: fix-security-bug

## 1. When to use this skill
Use this skill when tasked with fixing a security vulnerability in a codebase (e.g., Apache Druid). The task typically involves identifying the vulnerable code path, writing a targeted patch, applying the patch to the source code, and rebuilding the project to ensure the fix is effective without breaking legitimate functionality.

## 2. Visible input and artifact inventory
- **Visible Inputs:**
  - `instruction.md`: Contains the full text of the vulnerability description, the required deliverables, and the build command.
  - `environment/Dockerfile`: Details the environment setup.
  - `task.toml`: Task configuration.
- **Artifact Inventory:**
  - Patch files to be written in a specific directory (e.g., `/root/patches/`).
  - The target source code repository (e.g., `/root/druid/`).
  - The rebuilt project artifacts (e.g., patched JAR files).

## 3. Execution procedure for the current task
1. **Read Instructions:** Start by reading the visible instruction file (`instruction.md`) to understand the vulnerability, the required patch location, the source code location, and the specific build command.
2. **Inspect Repository:** Use `repo_search` and `java_source_inspect` to locate the vulnerable code path described in the instructions.
3. **Develop Patch:** Write the necessary patch files to address the vulnerability. Ensure the patch blocks the exploit while maintaining legitimate functionality.
4. **Apply Patch:** Use `apply_patch_text` or `run_shell` to apply the patch to the source code repository.
5. **Rebuild Project:** Execute the provided build command (e.g., using `maven_build` or `run_shell`) to compile the patched source code. Pay attention to any skipped tests or checks specified in the instructions.
6. **Verify:** Ensure the patch files are in the correct location and the build completes successfully.

## 4. Family tool routing and useful placeholder snippets
- **`repo_search` / `search_text`:** Use to find specific classes, methods, or keywords related to the vulnerability.
- **`java_source_inspect` / `read_file`:** Use to examine the context of the vulnerable code.
- **`write_file`:** Use to create the patch files in the designated directory.
- **`apply_patch_text`:** Use to apply the generated patch to the source code.
- **`maven_build` / `run_shell`:** Use to execute the build command provided in the instructions. Example: `mvn clean package -DskipTests ...`

## 5. Validation checks before final submission
- Verify that the patch files exist in the required directory (e.g., `/root/patches/`).
- Verify that the patch has been successfully applied to the source code.
- Verify that the build command completes without errors, producing the expected artifacts (e.g., patched JAR).
- Ensure the patch addresses the specific vulnerability described in the instructions without introducing syntax errors.

## 6. Common failure modes and repair actions
- **Patch Application Fails:** If the patch does not apply cleanly, re-examine the source code using `java_source_inspect` and adjust the patch file accordingly. Ensure correct line numbers and context.
- **Build Fails:** If the build fails, check the compilation errors. The patch might have introduced syntax errors or broken dependencies. Fix the code and rebuild.
- **Out of Memory (OOM) during Build:** Ensure you are using the exact build command provided in the instructions, which may include flags to skip certain modules (e.g., `-pl '!web-console'`).

## 7. Finalizer capsule
Before concluding the task, perform a final check to ensure the minimum required artifacts are present.
1. Check if the patch files are in the correct output directory.
2. Check if the build command was executed successfully.
If the build is failing near the maximum step limit, ensure at least the patch files are written to the correct location, as partial credit might be awarded for identifying the fix even if the build environment has issues.
