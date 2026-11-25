---
name: debug-responsive-image-sizes
description: Troubleshoot and optimize the accuracy of the sizes attribute using the Enhanced Responsive Images (auto-sizes) WordPress plugin.
---

# Debug Responsive Image Sizes

## Overview
This skill addresses how to debug the generation of the `sizes` attribute on images in block themes, leveraging the Enhanced Responsive Images plugin.

## Guidelines
1. Verify the site is using a block theme, as layout constraint calculations rely on block context (e.g., column counts, parent alignment). This is not available for classic themes.
2. Check if the parent blocks (like `core/columns`, `core/post-featured-image`, `core/cover`) pass the correct layout context.
3. Ensure relative alignment widths are correctly translating to the calculated `sizes` attribute.
4. Review image blocks with left/right/center alignments to ensure `sizes` reflect their respective layout constraints.
