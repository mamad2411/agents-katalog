---
name: wp-classic-theme-assets-and-editor
description: Implements and reviews WordPress classic theme CSS, JavaScript, fonts, images, editor styles, block styles, and optional theme.json integration. Use when loading assets or aligning editor and frontend presentation.
license: MIT
compatibility: "General guidance; verify API availability against the project's WordPress version."
---

# WordPress Classic Theme Assets and Editor

## Use this skill when

- Enqueueing CSS or JavaScript.
- Adding editor styles or block-specific styles.
- Choosing parent-aware or child-aware asset helpers.
- Adding `theme.json` to a classic theme.
- Debugging editor/frontend visual mismatch.
- Reviewing script dependencies, strategies, and cache busting.

## Approach

1. Inventory every asset and where it is needed.
2. Use WordPress enqueue APIs and prefixed handles.
3. Declare dependencies and versions.
4. Choose parent-only or child-overridable path helpers deliberately.
5. Avoid globally loading assets needed only on one template or block.
6. Verify editor and frontend parity.
7. Test with caching, concatenation, and optimization plugins where relevant.

## Workflow

Use [asset-and-editor-parity-workflow.md](workflows/asset-and-editor-parity-workflow.md).

## Resources

- [asset-loading-checklist.md](resources/asset-loading-checklist.md)
- [hybrid-theme-json-guidance.md](resources/hybrid-theme-json-guidance.md)
- [enqueue-and-editor-style-patterns.md](examples/enqueue-and-editor-style-patterns.md)
