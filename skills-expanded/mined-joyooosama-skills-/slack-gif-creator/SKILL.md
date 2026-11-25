---
name: slack-gif-creator
description: Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation concepts. Use when users request animated GIFs for Slack like "make me a GIF of X doing Y for Slack.
license: Complete terms in LICENSE.txt
---

# slack gif creator

Use this skill when the task matches the description above.
Keep the initial response concise and only open bundled references or scripts when they are clearly needed.

## Quick cues

- Emoji GIFs: 128x128 (recommended)
- Message GIFs: 480x480
- FPS: 10-30 (lower is smaller file size)
- Colors: 48-128 (fewer = smaller file size)
- Duration: Keep under 3 seconds for emoji GIFs
- **Use it directly** (e.g., "animate this", "split this into frames")
- **Use it as inspiration** (e.g., "make something like this")
- Use gradients for backgrounds (`create_gradient_background`)

## Available sections

- Slack GIF Creator
- Slack Requirements
- Core Workflow
- 1. Create builder
- 2. Generate frames
- 3. Save with optimization
- Drawing Graphics
- Working with User-Uploaded Images
- Use directly, or just as reference for colors/style
- Drawing from Scratch
- Circles/ovals
- Stars, triangles, any polygon

## Bundled resources

- core
- requirements.txt

Open these resources only if the current task needs deeper detail or executable helpers.
