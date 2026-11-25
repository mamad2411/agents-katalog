---
name: image-edit
description: Edit or retouch an existing image with a connector - background removal, generative fill/expand, cleanup, recolor, or compositing. Use when modifying a photo or asset rather than generating from scratch.
---

# image-edit

Non-destructive, disclosed, and licensed editing via the right connector.

## Pick the connector
- **Adobe Express / Firefly:** background removal, generative fill/expand, object cleanup, colour adjustments.
- **Nano Banana (Gemini):** prompt-based edits and multi-image compositing (blend references).
(See `mcp/CONNECTORS.md`.)

## Process
1. **State the edit precisely** (remove background, extend canvas to 16:9, remove the trash can, warm the tone).
2. **Run it through the connector**; confirm the result returned.
3. **Check it didn't misrepresent** a real subject (for product/real-estate/editorial, don't alter material facts).
4. **Disclose AI editing** where required (the `ai`/license rules), and keep the original.
5. Export at the right format/size/colour profile (hand to `asset-export`).

## Output
- The edited image (confirmed from the connector), what changed, and a disclosure/license note.

## Guardrails
- Don't claim an edit happened if the connector didn't run it.
- Disclose AI alteration when it matters; don't edit away material truth in documentary/product imagery.
