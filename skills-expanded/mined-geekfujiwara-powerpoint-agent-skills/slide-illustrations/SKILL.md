---
name: slide-illustrations
description: "Create consistent flat illustrations and fit them inside PowerPoint cards or empty illustration slots without distortion or accidental cropping. Use for card artwork, spot illustrations, or flat modern visuals. カード内の挿絵、フラットイラストの生成・配置に使用。"
license: MIT
---

# Slide Illustrations

## Procedure

1. Confirm the selected cards or slides, intended scene, and requested artwork.
   Use available image-generation features only when the user requests artwork.
   Do not pass confidential text, internal diagrams, or personal data to an
   external image service. Use an approved, non-sensitive scene description.
   If generation or measurement is unavailable, state the limitation and request
   an asset or the missing dimensions instead of inventing a result.
2. Measure the actual available slot using supported editing tools; use slide XML
   only if accessible and necessary. Account for text, padding, and existing art.
   Measure in a consistent unit: 914400 EMU = 1 inch; 12700 EMU = 1 point.
3. For an empty card, use these optional starting measurements, then check fit:
   - Padding `P = 0.20 in`, gap `G = 0.15 in`.
   - Wide card (`width >= 1.5 * height`): image left, text right.
     Slot width `min(height - 2*P, width*0.28)`; height `height - 2*P`.
   - Other cards: image above text. Slot width `width - 2*P`;
     initial image height `height*0.45`. Reserve the remaining area for text.
   - If a dimension is non-positive or text cannot fit, adjust the layout or
     ask to split the content. Do not continue with invalid dimensions.
4. Select one style for the deck:
   - **Business line art:** navy `1E2761`, blue `2F6FD0`, light blue `8FB3E0`,
     thin outlines, simple rounded figures, white or very light background.
   - **Flat modern:** no outlines or gradients, simplified faceless figures,
     purple, periwinkle, steel blue, navy, and white, with a subtle ellipse
     floor shadow and light background.
   Match the existing palette first. These are alternatives, not simultaneous rules.
5. Request the measured aspect ratio or the closest supported ratio with generous
   safe margins. Do not assume a portrait slot should use a square image.
6. Fit the image proportionally:
   `scale = min(slot_width/image_width, slot_height/image_height)`.
   Center it within the slot; preserve the full image without stretching or
   cropping. Use a user-approved crop only if explicitly requested.
7. Reflow adjacent text without changing its meaning. Preserve template fonts;
   aim for at least 14 pt body text. Ask before materially shortening content.
   Add concise alt text describing the scene's meaning, not decorative details.
8. Inspect the changed slides for overlap, aspect ratio, empty space, readable
   text, and consistent style. Report generated or reused assets and limitations.

## Prompt patterns

Business line art:

> Flat vector business illustration of [scene], thin clean outlines, rounded
> figures, navy and blue palette matching the slide, light background,
> generous safe margins, [slot aspect ratio], no words, letters, numbers, or logos.

Flat modern:

> Flat modern spot illustration of [scene], simplified faceless person,
> rounded periwinkle panel, purple ellipse floor shadow, steel blue props,
> navy accents, light background, no outlines, no gradients, [slot aspect ratio],
> no words, letters, numbers, or logos.

## Independence

This skill can be used on its own. If a journey card or another layout provides
an explicit slot, use that slot rather than recalculating it from the whole card.
