---
name: social-card-composer
description: A universal social media card and layout generator with automatic AI background removal. Use this when a user wants to remove backgrounds from subjects (images) and composite them into customizable, aesthetic posters for social media (e.g., comparison cards, lookbooks, product showcases). Supports fully customizable titles, subtitles, background images, and text boxes. Now natively supports twin engines satori (default for text-heavy layouts) and pillow (for shadow-heavy 1:1 image comparisons).
---

# Social Card Composer (social-card-composer)

A general-purpose CLI workflow to remove backgrounds from uploaded images and automatically layout and render them into a high-aesthetic social media poster.

It provides a dual-engine rendering system:
- **[Default] Satori Engine (`--engine satori`)**: Powered by Vercel Satori. Essentially writes HTML/CSS flexbox code and converts it to SVG/PNG. The absolute best choice for text-heavy notes, single image polaroid style, long paragraphs, and structured bullet points since it handles auto text-wrapping perfectly.
- **Pillow Engine (`--engine pillow`)**: Powered by Python's PIL. Best choice when dealing with 2+ images side-by-side, advanced Gaussian shadow effects, and complex layered transparency (Glassmorphism), where text length is fixed/short.

## Workflow & Usage

1. **Background Removal (Optional but recommended)**
   `scripts/remove_bg.sh <image_path_1> [image_path_2] ...`
   Extracts subjects from the given images and outputs `*_transparent.png` files in `/tmp/openclaw/`.

2. **Generate Layout**
   `scripts/generate.sh [--engine satori|pillow] --img1 <path> [--img2 <path>] [options...]`
   Creates the final composed image.
   
   **Supported Options:**
   - `--engine`: 'satori' (default) or 'pillow'
   - `--img1`: Path to the first image (transparent or original)
   - `--img2`: (Optional) Path to the second transparent image (triggers comparison layout in pillow engine)
   - `--maintitle`: Main poster title (e.g., "风格双生图鉴" or "Product Showcase")
   - `--subtitle`: Sub poster title
   - `--bg-url`: Background image URL from Unsplash/web (fallback provided if omitted, used by Pillow)
   - `--box1-title`, `--box1-desc1`, `--box1-desc2`, `--box1-desc3`: Custom text for the first item's info box.
   - `--box2-title`, `--box2-desc1`, `--box2-desc2`, `--box2-desc3`: Custom text for the second item's info box.
   - `--output`: Resulting image path (default `/tmp/openclaw/final_social_card.jpg`)

## Guidelines for the AI Agent

1. When a user provides images and text for a poster, default to `--engine satori` if they are providing lots of descriptive text or a single image. Switch to `--engine pillow` if they explicitly want a two-image side-by-side comparison with heavy shadows and glass UI.
2. Download user images.
3. Run `scripts/remove_bg.sh` on the images.
4. Construct the `generate.sh` command using the extracted transparent PNGs and passing in the user's custom text.
5. Provide the resulting image back to the user in the chat.
