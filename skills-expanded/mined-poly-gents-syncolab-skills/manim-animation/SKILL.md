---
name: manim-animation
description: "Community Manim workflow: Scene/Construct pattern, Tex/MathTex, render qualities, export and embed."
---

# Manim animation (Community)

- Author scenes under `/agent-filesystem/manim/<slug>/scene.py`. One `Scene` subclass per file is fine; `construct(self)` holds the animation.
- Use **`MathTex`** for inline math and **`Tex`** for prose; both compile through the sandbox's LaTeX install.
- Iterate at low quality first: `manim_render` with `quality="l"` (480p). Bump to `m` or `h` only when David approves the storyboard.
- Standard primitives: `Create`, `Write`, `Transform`, `FadeIn`/`FadeOut`, `MoveAlongPath`, `play(..., run_time=2)`.
- After render, upload the MP4 via the `manim_render` tool's built-in upload (returns an initiative-file id) so David can play it in chat.
- Keep scenes < 30s each — David can stitch in Cal-Culus post-production if needed.
