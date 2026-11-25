---
name: skillx-python-scala-translation-skill
description: skillx family-level skill for SkillLearnBench task family python-scala-translation.
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
  family: python-scala-translation
  tool_profile: qs_no_tests
  disclosure: family_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  functional_skill_count: 0
  generated_at: '2026-05-22T16:07:55Z'
---

## SkillLearnBench Family Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Task family: `python-scala-translation`

Use this skill only for this task family. Read the current instruction and visible local files before acting.
Treat every rule below as a reusable procedure with placeholders tied to the current instance.

## Family Plan

# step 1: Read the prompt, the Python source, and the visible Scala spec or scaffold to extract the required classes, functions, method signatures, output file location, and language/version constraints before writing code.
# step 2: Map the Python module’s behavior into Scala constructs with the same public API, preserving semantics while using idiomatic Scala types and standard-library abstractions for optional values, collections, and error handling.
# step 3: Implement the Scala file with the minimum complete set of requested data types and tokenization components, keeping naming and structure aligned with the visible spec so local checks can discover the expected symbols.
# step 4: Save the implementation to the requested path and use the Scala compile tool first to catch signature, import, inheritance, and type mismatches early.
# step 5: Run the public Scala local checks after compilation succeeds to validate behavioral equivalence, then fix the first concrete failing mismatch by comparing the test expectation with the translated Python logic.
# step 6: Run formatting or style checks if available, apply small direct patches for remaining type or formatting issues, and stop only once the file exists at the target path and public checks pass.

## Extracted Functional Procedures

No functional SkillX procedure was recovered for this family. Follow the family plan and visible verifier contract directly.

## Completion Contract

Create the artifact requested by the current instance using the visible instruction and local files.
Do a lightweight local sanity check when useful. Finish with the exact completion marker required by the task.
