---
name: create-social-cover-image
description: Create social media cover images sized and branded per platform
argument-hint: "[platform] [topic]"
related:
  - gen-media
  - draw-svg-image
  - follow-design-system
  - report
  - create-video-story
  - enhance-prompt

---

## Goal

Create a social media cover image that matches the platform dimensions, brand identity, and the intended content

## Scope

- Primarily supports Twitter/X, Facebook, LinkedIn, YouTube, Instagram
- Determines dimensions per platform
- Uses AI image generation or SVG drawing
- Supports text, logo, and brand color placement
- Exports an image file

## Execute

### 1. Identify Platform And Topic

> Goal: Identify the platform and content

1. Take `platform` from the argument (twitter, facebook, linkedin, youtube, instagram)
2. Take the `topic` or headline to show on the cover
3. If no platform is given → default to `twitter`
4. If the topic is ambiguous → use `/enhance-prompt` or `/ask-me`

### 2. Select Dimensions

> Goal: Pick the cover image size for the platform

1. Use `/report` to show the platform options:
   - `twitter`: 1500 x 500 px (header)
   - `facebook`: 820 x 312 px (cover)
   - `linkedin`: 1584 x 396 px (cover)
   - `youtube`: 2560 x 1440 px (banner)
   - `instagram`: 1080 x 1080 px (post)
2. Select the size for the specified platform
3. Keep width, height, and the safe zone for text

### 3. Design Concept

> Goal: Lay out the cover image concept

1. Use `/follow-design-system` to pull brand colors, typography, and logo if available
2. Define the layout: background, foreground, text position
3. Choose a style: minimal, gradient, illustration, photo, abstract
4. Specify the primary text, secondary text, and CTA (if any)

### 4. Generate Background Image

> Goal: Create the background image

1. If using AI generation → use `/gen-media-ai-images` with a dedicated prompt
2. If using vector → use `/draw-svg-image`
3. If using geometric → use `/draw-tldraw` or `/draw-excalidraw`
4. The prompt should state aspect ratio, style, and mood

### 5. Add Text And Branding

> Goal: Add text and brand elements

1. Use `/draw-svg-image` or an image editing tool to place text
2. Position the headline within the safe zone
3. Add the logo or watermark if available
4. Check contrast and readability
5. If no image editor is available → use Python (Pillow) or ImageMagick via `use-scripts`

### 6. Export And Verify

> Goal: Export the image file and verify it

1. Save the file as `<platform>-cover-<topic>.png` or `.jpg`
2. Check the file size and dimensions
3. Use `/deep-review-codebase` to look at file size
4. Show a preview if possible

### 7. Report

> Goal: Summarize the result

1. Use `/report` to show platform, dimensions, file path, file size
2. Advise on usage on each platform
3. If resizing is needed → use `/draw-svg-image` or `use-scripts`

## Rules

### 1. Platform Dimensions

- Must match the platform dimensions
- Define a safe zone for text (so it is not cropped)
- Keep the file under 5 MB for social upload

### 2. Brand Consistency

- Use `/follow-design-system` if a brand guide exists
- Use brand colors, fonts, and logo
- Do not include content that conflicts with the brand

### 3. Text Readability

- Use a font size readable on mobile
- No more than 2-3 lines of primary text
- Sufficient contrast (light text on dark bg or vice versa)

### 4. Copyright

- Do not use copyrighted images or fonts without permission
- If using AI generation, state the source
- Do not create content that infringes others' trademarks or copyright

### 5. File Format

- Export `png` if transparency is needed
- Export `jpg` if a small file size is needed
- `webp` is fine for web use

- Use /create-video-story if needed
- Use /gen-media-image-character if needed

## Expected Outcome

- A cover image matching the platform dimensions
- Includes the headline and brand elements
- Exported file with its path
- Report of dimensions, file size, platform
- Ready to upload to social media
