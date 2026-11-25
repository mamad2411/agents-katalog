---
name: lazy-load-backgrounds-videos
description: Implement and debug lazy loading for CSS background images and videos with the Image Prioritizer plugin.
---

# Lazy Load Backgrounds & Videos

## Overview
This skill guides the debugging of advanced lazy loading features applied to inline CSS background images and video tags.

## Guidelines
1. Ensure inline `style="background-image: ..."` elements outside the initial viewport are correctly deferred.
2. For videos outside the initial viewport, verify they are set to `preload="none"`.
3. Check that initial viewport videos retain their `preload="metadata"` default.
4. Ensure occluded initial-viewport images (e.g., subsequent carousel slides) correctly receive `fetchpriority="low"`.
5. Verify that lazily loaded videos restore their `autoplay` and `poster` attributes just before entering the viewport.
