---
name: use-thuenv-presentation-style
description: Use the bundled structured THUENV Deck template when a user explicitly asks for the Tsinghua University School of Environment presentation style, 清华环境学院 PPT 风格, or the THUENV presentation template. Apply it to new or redesigned presentations through a presentation workflow that supports SVG Deck workspaces.
metadata:
  short-description: 使用结构化清华环境学院 SVG Deck 模板制作演示文稿
---

# Use THUENV Presentation Style

Use the host presentation workflow to create, render, and validate the presentation.

Resolve paths relative to this Skill directory. Treat
`assets/thuenv_presentation/` as the exact reusable Deck workspace. Preserve its
directory structure and select it as the presentation template instead of
recreating the visual style.

Read and follow:

- `assets/thuenv_presentation/templates/design_spec.md`
- the applicable SVG layouts in `assets/thuenv_presentation/templates/`
- their linked image assets in `assets/thuenv_presentation/images/`

Adapt the user's content to the available layouts while preserving the fixed
identity layers, relative asset references, and editable template structure.
