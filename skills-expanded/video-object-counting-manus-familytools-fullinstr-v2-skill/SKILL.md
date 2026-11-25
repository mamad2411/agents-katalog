---
name: video-object-counting-manus-familytools-fullinstr-v2-skill
description: Family-scoped SkillLearnBench skill for video-object-counting using latest full-instruction v2 family injection.
allowed-tools:
  - image_grayscale_inplace
  - image_metadata
  - list_dir
  - read_file
  - run_python
  - run_shell
  - template_match_count
  - video_extract_keyframes
  - write_file
  - write_table
metadata:
  benchmark: SkillLearnBench
  generator: Manus
  baseline: manus_familytools_fullinstr_v2
  generation_constraints: slb_no_instance_memory_familytools_v2
  allowed_gold_input: familytools_full_instruction_v2
  skill_injection_scope: family_scoped
  date: "2026-05-23"
---

# Skill: video-object-counting

## 1. When to use this skill
Use this skill when tasked with analyzing a video (e.g., a screen recording of a game like Super Mario) to count the occurrences of specific objects (e.g., coins, enemies, turtles) across extracted keyframes, and outputting the results into a structured format like a CSV file.

## 2. Visible input and artifact inventory
- **Input Video**: Typically an MP4 file (e.g., `/root/super-mario.mp4`).
- **Template Images**: PNG files representing the objects to be counted (e.g., `/root/coin.png`, `/root/enemy.png`, `/root/turtle.png`). Note that there might be multiple templates for a single object class (e.g., `coin1.png`, `coin2.png`).
- **Instruction File**: `instruction.md` containing the specific requirements, including the output path and schema.
- **Output Artifact**: A CSV file (e.g., `/root/counting_results.csv`) with columns for frame ID and counts for each object class.

## 3. Execution procedure for the current task
1. **Read Instructions**: Carefully read the `instruction.md` to identify the input video path, template image paths, required object classes, and the exact output CSV path and schema.
2. **Extract Keyframes**: Use the `video_extract_keyframes` tool to extract frames from the input video into the specified directory (usually `/root`).
3. **Convert to Grayscale**: For each extracted keyframe, use the `image_grayscale_inplace` tool to convert the RGB image to grayscale, overwriting the original file.
4. **Template Matching**: For each object class, use the `template_match_count` tool to count occurrences in each grayscale keyframe using the provided template images. If multiple templates exist for a class, ensure all are used and results are properly aggregated or deduplicated.
5. **Compile Results**: Gather the counts for all object classes across all keyframes.
6. **Generate Output**: Use the `write_table` tool to create the final CSV file with the required columns (e.g., `frame_id`, `coins`, `enemies`, `turtles`) and rows corresponding to each keyframe in timeline order.

## 4. Family tool routing and useful placeholder snippets
- **video_extract_keyframes**: Use to extract frames from the video.
- **image_grayscale_inplace**: Use to convert extracted frames to grayscale.
- **template_match_count**: Use to count objects in frames based on templates.
- **list_dir**: Use to verify extracted frames and available templates.
- **write_table**: Use to write the final CSV output.

*Snippet for writing CSV:*
```python
# Example using run_python or write_table conceptually
import csv
data = [
    {"frame_id": "/root/keyframes_001.png", "coins": 5, "enemies": 2, "turtles": 0},
    # ...
]
# Write to /root/counting_results.csv
```

## 5. Validation checks before final submission
- Verify that the output CSV file exists at the exact path specified in the instructions.
- Check that the CSV has the correct headers as requested (e.g., `frame_id`, `coins`, `enemies`, `turtles`).
- Ensure the `frame_id` format matches the requirement (e.g., `/root/keyframes_001.png`).
- Confirm that the number of rows in the CSV matches the number of extracted keyframes.

## 6. Common failure modes and repair actions
- **Missing Templates**: If a template is not found, use `list_dir` to check the available files in the environment directory and adjust the template paths accordingly.
- **Incorrect Frame ID Format**: If the validation fails due to frame ID format, ensure the zero-padding matches the instruction (e.g., `%03d`).
- **Grayscale Conversion Failure**: Ensure `image_grayscale_inplace` is called on the correct extracted frame paths before attempting template matching.

## 7. Finalizer capsule
If the task is nearing the maximum step limit and full processing is incomplete, prioritize creating the output CSV file at the requested path with the correct headers and at least one row of data (even if counts are partial or zero) to satisfy the minimum artifact shape requirement. Use `write_table` or `run_python` to quickly generate this fallback artifact.
