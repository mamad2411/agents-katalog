---
name: skillx-fix-security-bug-skill
description: skillx family-level skill for SkillLearnBench task family fix-security-bug.
allowed-tools:
- list_dir
- read_file
- write_file
- python
- shell
metadata:
  benchmark: skilllearnbench
  source_method: skillx
  source_dir: <SOURCE_DIR>
  family: fix-security-bug
  tool_profile: qs_no_tests
  disclosure: family_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  functional_skill_count: 0
  generated_at: '2026-05-22T16:07:55Z'
---

## SkillLearnBench Family Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Task family: `fix-security-bug`

Use this skill only for this task family. Read the current instruction and visible local files before acting.
Treat every rule below as a reusable procedure with placeholders tied to the current instance.

## Family Plan

# step 1: Read the visible instruction and inspect the repository layout to identify the required patch output location, the target codebase, and the public build command, so you constrain the work to visible requirements only.
# step 2: Search the source for the request parsing and validation path that handles the vulnerable feature configuration, then inspect the smallest set of classes that deserialize or interpret that object, so you can patch the bypass at its entry point.
# step 3: Implement a minimal source change that rejects or ignores malformed configuration using an empty-field-name override while preserving normal JavaScript-related settings and other legitimate request shapes, so the exploit path is blocked without broad regressions.
# step 4: Save the change as a patch file in the required patch directory and apply it to the repository using the provided patch/edit tools, so both the deliverable artifact and the modified source tree are present.
# step 5: Review the diff to confirm the patch is narrowly scoped to the vulnerable code path and does not alter unrelated behavior, so the fix remains surgical and maintainable.
# step 6: Rebuild the specified module set with the public Maven command and skips from the instruction, so you verify the patched project still compiles in the expected environment.
# step 7: Finalize only after the patch file exists, the source tree contains the applied fix, and the build succeeds or reaches the first actionable mismatch you can repair, so the submission satisfies both artifact and functionality requirements.

## Extracted Functional Procedures

No functional SkillX procedure was recovered for this family. Follow the family plan and visible verifier contract directly.

## Completion Contract

Create the artifact requested by the current instance using the visible instruction and local files.
Do a lightweight local sanity check when useful. Finish with the exact completion marker required by the task.
