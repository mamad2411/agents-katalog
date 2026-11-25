---
name: schedule-planning-manus-familytools-fullinstr-v2-skill
description: Family-scoped SkillLearnBench skill for schedule-planning using latest full-instruction v2 family injection.
allowed-tools:
  - calendar_block_detect
  - date_normalize
  - list_dir
  - pdf_extract_text
  - pdf_render_pages
  - read_file
  - read_json
  - run_python
  - run_shell
  - schedule_slot_search
  - write_file
  - write_json
  - write_text_artifact
metadata:
  benchmark: SkillLearnBench
  generator: Manus
  baseline: manus_familytools_fullinstr_v2
  generation_constraints: slb_no_instance_memory_familytools_v2
  allowed_gold_input: familytools_full_instruction_v2
  skill_injection_scope: family_scoped
  date: "2026-05-23"
---

# Skill: Schedule Planning

## 1. When to use this skill
Use this skill when tasked with parsing meeting schedule requests from an input file and proposing meeting times based on an internal calendar. The task involves extracting busy blocks, constraints, participants, and duration from visible inputs, normalizing dates, searching for valid slots, and writing the requested schedule artifacts.

## 2. Visible input and artifact inventory
The input files typically include a meeting requests JSON file containing email requests with meeting duration and specific time/date constraints, and a calendar PDF containing existing appointments where the time between two adjacent horizontal lines is typically 15 minutes. The output artifacts include reply text files generated based on a specific template, and a results JSON file that logs the filenames of all generated text files and their recipients.

## 3. Execution procedure for the current task
First, read the visible instruction and inventory visible files before creating artifacts. Read the meeting requests JSON file to extract the meeting duration and any specific time/date constraints mentioned in the message body for each email. Access and read the calendar PDF to extract existing appointments, determining start and end times by measuring position and span relative to the timeline axis. Specifically identify blue-colored blocks, which represent low-priority or flexible tasks, and treat these as available time that can be overwritten. If a meeting request overlaps with a blue-colored entry, prioritize the meeting. Ensure that the earliest compatible time is selected for each request, provided that all requests can be accommodated. For each email, generate the reply content based on the provided template and save it as an individual text file, ensuring strict adherence to the required date and time formats. Finally, log the filenames of all generated text files and their recipients in the results JSON file using the required format.

## 4. Family tool routing and useful placeholder snippets
Use `read_json` to read the meeting requests file. Use `calendar_block_detect` and `pdf_extract_text` or `pdf_render_pages` to parse the calendar PDF and extract appointment blocks and their colors. Use `date_normalize` to handle date and time formats. Use `schedule_slot_search` to find the earliest compatible time slots based on constraints and calendar availability. Use `write_text_artifact` or `write_file` to generate the reply text files. Use `write_json` to create the final results JSON file.

## 5. Validation checks before final submission
Verify that all required reply text files have been generated with the correct naming convention. Check that the content of each reply file strictly follows the provided template and formatting rules. Ensure that the results JSON file exists, is properly formatted, and contains the correct filenames and recipients for all processed requests. Confirm that the selected meeting times do not conflict with non-flexible calendar appointments and satisfy all constraints mentioned in the requests.

## 6. Common failure modes and repair actions
If the generated reply files have the wrong date or time format, review the template requirements and use `date_normalize` or custom Python scripts to format them correctly. If a proposed time conflicts with a non-flexible appointment, re-evaluate the calendar blocks and use `schedule_slot_search` to find the next available slot. If some reply files are missing, check the extraction logic for the meeting requests JSON to ensure all emails are processed. If the results JSON is invalid, verify the structure against the required format and use `write_json` to recreate it.

## 7. Finalizer capsule
Before completing the task, ensure that the minimum required artifacts exist at the visible paths and their shapes match the instruction. If the full process fails near the maximum step limit, attempt to generate the reply files and results JSON with the best available time slots, even if some constraints are partially met, to provide a structured output. Ensure the results JSON is valid and points to the generated text files.
