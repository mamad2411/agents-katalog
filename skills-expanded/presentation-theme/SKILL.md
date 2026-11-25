---
name: presentation-theme
description: "Apply a consistent light-and-dark PowerPoint theme, including title slides, section dividers, closing slides, and optional miniature diorama artwork. Use for deck-wide restyling or section backgrounds. 明暗デザイン、表紙、区切り、箱庭背景の統一に使用。"
license: MIT
---

# Presentation Theme

## Scope and priorities

Use the user's brand, template, language, and explicit choices before these defaults.
Confirm the target slides; do not restyle the whole deck for a single-slide request.
Preserve facts, citations, presenter spelling, notes, and accessibility information.
Do not invent personal details or insert an organization, customer, or internal URL.
Only remove information the user explicitly marks for exclusion, including matching
occurrences in notes, alternative text, and shape names. Retain required attribution.

## Procedure

1. Inspect the selected deck's slide size, theme, content, fonts, and available
   editing capabilities. Keep a recoverable original before a broad restyle.
2. Select one consistent dark-page recipe:
   - **Black miniature:** background `000000`, white text, accent `7FD1D8`.
     Optional title-text gradient: `4FC3F7` to `8B7CF6` to `F06CC8`.
     Use miniature/isometric artwork on a matching black background, with no overlay.
   - **Navy diorama:** background `101E4B`, white text, cyan emphasis.
     Use a matching navy miniature scene on the right. If needed, blend only the
     image boundary with a background-colored gradient, not a band behind the title.
   Default to black when no existing theme or user preference decides. Never apply
   the black-background and navy-blending instructions simultaneously.
3. Use dark pages for the cover, section dividers, and closing slide. Reserve about
   60% of their width for left-aligned text and 40% for artwork. Adapt to content
   rather than forcing those proportions. Do not add a cover unless requested.
4. Use light content pages: background `F5F7FB`, white rounded cards, navy
   `1E2761` headings, and blue `0F6CBD` accents. Use subtle shadows without
   decorative outlines. Use editable native charts for actual numerical data.
5. Follow existing fonts. If no font is prescribed, use Yu Gothic UI for Japanese
   when available and a supported sans-serif for English. Suggested title sizes
   are 36-48 pt on covers and 28-36 pt on content slides; aim for body text at
   least 14 pt. Split dense content before shrinking text.
6. If artwork is requested and image generation is available, create a distinct
   subject for each divider while keeping a shared miniature/isometric style.
   Preserve aspect ratio, leave title space clear, and add meaningful alt text.
   Do not generate logos, embedded words, or factual diagrams as decoration.
   Do not send confidential source text to an image service; use an approved,
   non-sensitive scene description. If unavailable, explain this and keep the
   layout usable without an image; do not claim an image was generated.
7. Check every changed slide for clipping, contrast, readable title gradients,
   consistent typography, and image boundaries. Preserve numerical values and
   required citations. Report what changed and any checks not possible.

## Optional image prompt

Use only after an artwork request, adapting the subject and approved palette:

> Isometric miniature diorama, soft handcrafted model textures, [non-sensitive
> scene], tiny figures and contextual props, subject on the right, plain [black or
> deep navy] background matching the slide, generous empty space on the left,
> no words, letters, numbers, logos, or watermarks.

## Boundaries

Do not add animations as part of theming. Existing animations stay unchanged.
Do not claim pixel-perfect rendering, font availability, or complete information
removal without checking the corresponding surfaces.
