# U11-CLEAN Skill: Anthropic poster-design artifact

## Output contract
- Extract the exact contract first:
  - final image path and type: one PNG
  - final metadata path and type: one JSON object
  - exact JSON keys, with no extras
  - required title text, required visual elements, any count/cap rules, and any canvas hint
- JSON values are only visible HEX strings for requested color roles, plus a heading font name only when the schema asks for it.
- If no size is specified, choose one deterministic canvas appropriate to the visible artifact type and keep that choice consistent through validation.

## Ledger
Keep a small internal ledger, not a file, with one row per:
- output path
- JSON field
- title / heading text
- composition type
- required module, layer, icon, or annotation element
- each named brand color role
- heading font, if requested
- any measurable cap or count rule

Each row must be backed by one visible prompt/file anchor, one `brand_token_lookup` result, one deterministic layout/count, or one concrete draw operation.

## Route
1. Use `list_dir` and `read_file` only enough to capture the artifact contract from visible files and the prompt.
2. Reserve the outputs immediately:
   - `write_json` the exact JSON schema with empty strings
   - create a minimal valid PNG at the final path with the correct background and a simple title/block so the artifact exists early
3. Use `brand_token_lookup` for every named Anthropic token actually required by the contract. Fill the JSON as soon as each value is known.
4. Infer the smallest visual route from the contract:
   - technical poster route: separated or exploded modules, clear spacing, thin leader lines, readable hierarchy
   - branded card / packaging-front route: strong heading, generous whitespace, one simple device silhouette or icon, restrained accent use
5. Render with `image_canvas_draw` in a few deterministic passes:
   - background
   - main structural forms
   - title typography
   - restrained accents and annotations
6. Keep the look muted and minimal: flat fills or subtle tonal variation, no neon, no glow, no loud gradient styling unless the visible brief explicitly asks for it.
7. After each meaningful fill, rewrite the PNG and keep the JSON synchronized.
8. If a slot lacks support, leave the most conservative schema-valid value rather than inventing content.

## Public readback / spot-check
- Use `image_metadata` to confirm the image exists and to inspect size, format, and basic color summary.
- Then spot-check one fragile requirement against its source:
  - minimum distinct layers/modules for technical posters
  - restrained highlight share if the brief caps highlight area
  - low-saturation / muted palette if style compliance is the main risk
- Use `run_python` only for a simple measurable check such as accent-area share or coarse saturation sampling.
- Read back the JSON and confirm:
  - exact requested keys only
  - all requested fields are populated
  - each value matches a looked-up token or the actual heading font used

## Last-write rule
Near the step cap, make one final write so the required PNG and JSON paths contain the most complete schema-valid artifact available.

## RL1C Public Contract Pin Delta
Before any long tool action, pin the prompt-visible artifact path, required schema or fields, and one public acceptance check in a tiny ledger. After writing the artifact, reread only the produced artifact and verify the pinned public contract before finalizing.
