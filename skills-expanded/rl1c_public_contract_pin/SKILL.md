# anthropic-poster-design — RL1C_PUBLIC_CONTRACT_PIN

## Contract pin first
- Use `read_tests` first; use `read_file` on `/tests/test_outputs.py` only if truncation hides details.
- Before any long render/write, pin a tiny scratch ledger with:
  - `OUTPUT_IMAGE`
  - `OUTPUT_META`
  - exact `REQUIRED_KEYS`
  - exact `EXPECTED_HEX_VALUES`
  - `EXPECTED_HEADING_FONT_SUBSTRING` if present
  - one public image check to guard first:
    - technical posters: background detected and every declared hex visibly appears
    - branded cards: background detected and accent remains restrained / under any visible cap
- Trust only prompt-visible instructions and public tests.

## Reserve final artifacts early
- Create `/root/design_parameters.json` immediately with the exact key set only, lowercase hex values exactly as in tests, and `applied_heading_font` containing `Poppins` only when that field is required.
- Create the PNG directly at `OUTPUT_IMAGE`; no draft path.
- Prefer Pillow via `run_python` for deterministic flat fills.
- First draw must be an explicit full-canvas solid background in the required hex; leave all 4 corners untouched background.

## Branch rules
- `/root/anthropic_branded_artifact.png`
  - Background `#faf9f5`
  - Large heading + simple device/icon in `#141413`
  - 1–3 small solid `#d97757` highlights only
  - Quiet, premium, no gradients/glow/neon
- `/root/nova_technical_poster.png`
  - Background `#faf9f5`
  - At least 5 clearly separated layers/modules
  - Casing `#141413`, thermal `#6a9bcc`, PCB `#788c5d`, connector accents `#d97757`, annotation lines `#b0aea5`
- `/root/orion_technical_poster.png`
  - Background `#141413`
  - Multiple clearly separated modules
  - Casing `#faf9f5`, thermal `#6a9bcc`, PCB `#788c5d`, connector accents `#d97757`, annotation lines `#b0aea5`

## Anti-failure rules
- Metadata-only is not enough: every hex declared in JSON must have a solid visible patch/line in the PNG.
- Background must be dominant; do not let primary accent dominate.
- Keep style low-saturation and minimalist with flat fills and simple geometry.
- For technical posters, use thin muted-gray leader lines and small solid color chips if needed to guarantee exact-color presence.
- Do not rely on antialiased text alone to prove a color exists.

## Pinned readback before finalize
After the last write, reread only the produced artifacts:
- `OUTPUT_IMAGE` via `image_metadata` or Pillow
- `/root/design_parameters.json`

Verify the pinned public contract:
- paths match
- JSON keys are exact, no extras
- pinned hex values match exactly
- background hex is present at corners and visually dominant
- every declared hex has nontrivial pixel presence
- `applied_heading_font` contains `Poppins` when required

Then run `/tests/test.sh` once if needed, repair only the first public failure, reread the produced artifacts again, and finalize.

## Execution hygiene
- Emit exactly one tool call or one final answer per turn.
- Finalize only after both final-path artifacts exist and pass the pinned readback.
