---
name: skillx-schedule-planning-skill
description: skillx family-level skill for SkillLearnBench task family schedule-planning.
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
  family: schedule-planning
  tool_profile: qs_no_tests
  disclosure: family_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  functional_skill_count: 0
  generated_at: '2026-05-22T16:07:55Z'
---

## SkillLearnBench Family Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Task family: `schedule-planning`

Use this skill only for this task family. Read the current instruction and visible local files before acting.
Treat every rule below as a reusable procedure with placeholders tied to the current instance.

## Family Plan

# step 1: Read the visible instruction and inspect the available input files first, so you know the required outputs, file names, formatting rules, and any calendar-specific assumptions.
# step 2: Parse the meeting-request JSON and extract, for each message, the recipient, message identifier, meeting duration, and any date or time constraints, because these drive slot feasibility and output naming.
# step 3: Parse the calendar PDF with the calendar-specific tools to recover dated time blocks, time zone, and visual block properties; treat normal occupied blocks as busy and mark the designated flexible color as overwriteable availability.
# step 4: Normalize all request constraints into concrete candidate windows using the calendar’s time zone and the stated grid resolution, so later slot search is consistent and deterministic.
# step 5: Search the calendar for the earliest slot that satisfies each request’s duration and constraints while allowing overlap with flexible blocks, because the task prioritizes earliest compatible scheduling.
# step 6: Write one reply text file per request using the exact template and required date/time formatting, so the artifact matches the expected communication style and schema.
# step 7: Write the summary JSON listing each generated reply filename and recipient, then do a lightweight sanity check that every requested artifact exists and matches the specified structure.

## Extracted Functional Procedures

No functional SkillX procedure was recovered for this family. Follow the family plan and visible verifier contract directly.

## Completion Contract

Create the artifact requested by the current instance using the visible instruction and local files.
Do a lightweight local sanity check when useful. Finish with the exact completion marker required by the task.
