---
name: make-video
description: Create, validate, preview, and render a local video with the Instavar Remotion templates and VideoSpec.
---

# Make a video

1. If the `instavar-remotion` MCP server is connected, call `get_capabilities`, `list_templates`, and `get_template`. Otherwise use the template list in the README.
2. Ask for any missing brief details that materially affect the result: audience, goal, platform, aspect ratio, duration, source media, call to action, and audio intent. Audio intent must be narration, music, or explicitly silent.
3. Create or scaffold a `*.video.json` VideoSpec. Use only published template and scene identifiers. Write the creative copy from the user's brief. Do not treat placeholder copy as finished content. Never show `scene.kind` as audience copy. Avoid all-caps headings and decorative labels above headings.
4. If narration is approved, preserve the exact script in `audio.narrationText`. For private Supertonic narration, write one paragraph per scene at `https://instavar.com/voice`, download the WAV and timing manifest, then run `npm run video:timing -- <spec> --audio <wav> --manifest <timing.json>`. The beat count must equal the scene count. Otherwise add an existing local `audio.narrationSrc`, or run `npm run video:narrate -- <spec>` for no-key system TTS. Never leave approved narration only in the conversation.
5. Run `npm run video:validate -- <spec>` and fix every blocking error. Treat hierarchy, scene differentiation, text density, and audio diagnostics as product requirements.
6. Run `npm run video:preview -- <spec>`. It renders a midpoint frame for every scene. Inspect every output in `out/previews/<id>/`, not only the opening, middle, and ending. Correct clipping, weak hierarchy, unreadable copy, repeated layouts, poor visual balance, or timing problems. Use `--studio` only when an interactive review is useful.
7. Run `npm run video:render -- <spec>` only after validation and every-scene preview are satisfactory. The render command performs post-render audio QA and fails if expected audio is absent or effectively silent.
8. Report the exact spec, preview directory, MP4 path, audio mode, and unresolved warnings. Do not claim a render succeeded unless the output exists and the expected-audio QA passes.

Keep all creative assets local unless the user explicitly approves an upload. Ask before using paid services or publishing to an external platform.
