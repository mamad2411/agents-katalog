# Optional recreation prompt

Use for an explicitly requested faithful recreation, not automatically for a different brand. The source SOP targets Seedance 2.5; verify the chosen provider's current model schema rather than treating its historical duration/pixel limits as permanent.

Build the prompt from reconciled evidence:

1. Preserve authorized source dialogue exactly when faithful dialogue is requested; label speakers and delivery. Keep any requested rewrite in a separate adapted version.
2. Exclude added captions, subtitles, handles, watermarks and graphics by default. Specify intended physical label/screen text and its source. Final requested captions belong in the editing stage.
3. Describe named background objects and their positions, not vague aesthetic adjectives.
4. Match the actual visual style. Apply the SOP's phone realism language only to phone/UGC references; do not strip cinematic lighting or grading from a cinematic perfume reference.
5. Specify observed tripod/handheld behavior and camera moves by dialogue/action beat; use precise timing where synchronization requires it.
6. Give separate setup blocks for wardrobe/room changes and the beat that connects them.
7. For a real UI on screen, use supplied or authorized screen footage rather than asking the model to invent text. Check current reference constraints, preserve aspect ratio and mute only clips serving as visual-only references. Keep intentional voice/motion/audio references intact.
8. Prefer clean authorized source assets for generation so overlays are not reproduced accidentally. Log reference preprocessing. Preserve original footage and attribution in the analysis evidence.

Return a prompt and attachment list, not a claim that the generation will perfectly match the source.
