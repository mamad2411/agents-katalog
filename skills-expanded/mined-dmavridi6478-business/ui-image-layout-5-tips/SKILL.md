---
name: ui-image-layout-5-tips
description: Five UI layout tips for placing images with text - split images into columns, put images outside the layout for an immersive feel, wrap text smartly, make some images lead the pack, and add dynamic sizes to a grid - each with the do and the don't. Use when designing article pages, galleries, cards or landing sections that mix images and text. Source @iqonicdesign / @ux_dose "5 Tips To Help You In UI Design" carousel (Batch 103). Cover slide plus 5 tip slides; all 6 were in the upload.
---

# 5 tips for images in UI layouts

| # | Tip | Do not | Do |
|---|---|---|---|
| 1 | Split images into columns | Wrap text around a single image so the text column gets narrow | Split the view into separate columns: image in one, text in the other |
| 2 | Put images outside the layout | Keep every image inside the text column | Let an image break out of the column (full bleed or beside it) for a more immersive page or article |
| 3 | Use text wrapping smartly | Interrupt the reading flow with the image mid-paragraph | Align images inside a paragraph to the top or right, so the eye keeps its line |
| 4 | Make images stand out | Show a screen of equal-sized images | With multiple images, make some lead the pack: one large hero, smaller supporting images |
| 5 | Add dynamic to the layout | Repeat a uniform grid (3 x 4 equal tiles) | Employ multiple columns and image sizes so scrolling is more interactive |

## Applying them
- Use CSS grid with named areas for tips 1 and 4, `float` or `shape-outside` only for tip 3, and a negative inline margin or `grid-column: 1 / -1` for tip 2.
- Keep one focal image per viewport; a "bento" or masonry grid (tip 5) is only worth it with at least 6 images.
- Check each layout at 400 px wide: columns should stack and the lead image should stay first.
- Template: `design-templates/templates/ui-tip-do-dont.html` reproduces the do/don't card format. Related skills: `responsive-design`, `visual-design-foundations`, `better-layout`.
