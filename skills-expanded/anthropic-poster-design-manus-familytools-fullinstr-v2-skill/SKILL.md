---
name: anthropic-poster-design-manus-familytools-fullinstr-v2-skill
description: Family-scoped SkillLearnBench skill for anthropic-poster-design using latest full-instruction v2 family injection.
allowed-tools:
  - brand_token_lookup
  - image_canvas_draw
  - image_metadata
  - list_dir
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

# Skill: anthropic-poster-design

## When to use this skill
Use this skill when generating a branded visual artifact (e.g., technical poster, launch card, packaging visual) for an Anthropic product. The task requires applying Anthropic's official brand colors and typography, maintaining a minimalist, low-saturation aesthetic, and outputting an image file and a JSON file with applied design parameters.

## Visible input and artifact inventory
- **Visible Inputs:** Task instructions (`instruction.md`) and environment configuration (`Dockerfile`, `task.toml`). These define the product, visual elements, color strategy, and output paths.
- **Artifact Inventory:** An image file (e.g., `/root/nova_technical_poster.png`) and a JSON file (e.g., `/root/design_parameters.json`) containing applied HEX color values and heading font name.

## Execution procedure for the current task
1. **Read Instructions:** Read the visible instruction file to understand the product, visual elements, and color strategy.
2. **Extract Parameters:** Extract output paths, JSON schema, and brand tokens (e.g., Corporate Dark, Identity Light, Primary Accent).
3. **Lookup Brand Tokens:** Use `brand_token_lookup` to retrieve exact HEX values and font names for required Anthropic brand tokens.
4. **Generate Image:** Use `image_canvas_draw` (or a Python script via `run_python`) to create the visual artifact. Adhere to minimalist, low-saturation constraints; avoid neon or "AI gradient" styling.
5. **Generate JSON:** Create the JSON file with applied HEX color values and heading font name, strictly following the provided schema. Use `write_json`.
6. **Validate Outputs:** Verify both files exist at specified paths and contents match requirements.

## Family tool routing and useful placeholder snippets
- **`brand_token_lookup`:** Find exact HEX values for Anthropic brand colors and the official heading font.
- **`image_canvas_draw`:** For straightforward image generation tasks described via parameters.
- **`run_python`:** If `image_canvas_draw` is insufficient for complex layouts, use a Python script with `Pillow` or `matplotlib`.
- **`write_json`:** Safely write the `design_parameters.json` file, ensuring correct formatting.

## Validation checks before final submission
- **File Existence:** Check that the final image and JSON files exist at exact paths specified in instructions.
- **JSON Schema:** Verify the JSON file strictly follows the required structure and contains only requested keys.
- **Image Content:** Ensure image dimensions are reasonable and dominant colors match requested brand tokens using `image_metadata`.
- **Aesthetic Constraints:** Confirm the design is minimalist and low-saturation, avoiding neon or high-intensity gradients.

## Common failure modes and repair actions
- **Incorrect Brand Tokens:** Re-run `brand_token_lookup` to ensure correct values are applied.
- **JSON Schema Mismatch:** Rewrite using `write_json` to strictly match the requested schema.
- **Image Generation Failure:** Check parameters passed to `image_canvas_draw` or debug the Python script. Ensure all required layers are included.
- **Incorrect Output Paths:** Move files to exact paths specified in instructions.

## Finalizer capsule
Before concluding, perform a final check to ensure minimum required artifacts exist and match the expected shape. If image generation is too complex near the maximum step limit, generate a simplified version applying correct brand colors and typography. Ensure the JSON file is perfectly formatted and contains correct brand token values. The final state must have requested files at exact paths specified in instructions.
