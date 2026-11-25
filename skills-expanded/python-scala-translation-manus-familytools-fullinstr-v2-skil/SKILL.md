---
name: python-scala-translation-manus-familytools-fullinstr-v2-skill
description: Family-scoped SkillLearnBench skill for python-scala-translation using latest full-instruction v2 family injection.
allowed-tools:
  - diff_summary
  - list_dir
  - read_file
  - repo_search
  - run_shell
  - scala_compile
  - scala_format_check
  - scala_run_public_tests
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

# Skill: Python to Scala Translation

## 1. When to use this skill
Use this skill for `python-scala-translation` tasks in SkillLearnBench. It applies when translating a Python script into a high-quality Scala implementation. The task requires reading a source Python file, understanding its semantics, and writing a Scala file that follows Scala best practices, compiles, and passes public test specifications.

## 2. Visible input and artifact inventory
The task involves several key files. The source Python file contains the logic to be translated. The target Scala file is the destination path for the translated code. A Scala test specification defines the expected API signatures and behavior. The instruction file details specific requirements, classes, and functions. Environment files include build configurations and directory structures.

## 3. Execution procedure for the current task
Begin by reading the visible instruction file to understand the goal and required components. Read the source Python file to grasp the logic, and examine the Scala test specification to identify exact API signatures and expected return types. Translate the Python semantics into Scala, utilizing proper abstractions and idiomatic error handling rather than a word-for-word translation. Write the translated code to the target path. Use the provided tools to compile and test the implementation against the public specifications. If errors occur, analyze them, adjust the code, and repeat the process until successful.

## 4. Family tool routing and useful placeholder snippets
Use `read_file` to inspect the Python source and Scala test specs, and `write_file` to save the translated code. Utilize `search_text` and `repo_search` to find class definitions, and `diff_summary` to review changes. For Scala-specific tasks, use `scala_compile` to check for syntax errors, `scala_run_public_tests` to validate logic, and `scala_format_check` to ensure formatting conventions. Use `run_shell` for ad-hoc commands.

## 5. Validation checks before final submission
Verify that all requested classes and functions are present in the Scala implementation. Ensure the code compiles successfully with Scala 2.13 and that all public tests pass. Check that the final file is saved exactly at the requested target path and follows idiomatic Scala conventions.

## 6. Common failure modes and repair actions
Compilation errors often result from incorrect translation of Python's dynamic typing to Scala's static typing; repair this by reviewing the test specification for expected types. Missing methods or classes can occur; cross-reference the Python file and instructions to ensure all elements are implemented. Test failures indicate logic errors; compare data transformations and debug failing cases. For formatting issues, run `scala_format_check` and apply corrections.

## 7. Finalizer capsule
Before concluding, perform a final verification to ensure the minimum required artifact exists at the correct path. If nearing the maximum step limit with failing tests, prioritize ensuring the Scala file is present, contains all required signatures (even if incomplete), and compiles successfully. This guarantees the output shape matches the instruction.
