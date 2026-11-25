---
name: ui-validation
description: Compare generated UI against Figma designs — screenshot, diff, iterate until 85%+ match
category: general
triggers:
  - "use ui-validation"
---

Compare generated UI against Figma designs.

## How it works
1. Takes screenshot of generated UI
2. Fetches Figma design via MCP
3. Pixel-compares (similarity percentage)
4. Reports differences: spacing, colors, typography
5. Iterates until 85%+ match

For full instructions, read `agents/ui-validation.md`.
