---
name: coloring-book-generator
description: Create printable coloring book pages from a theme prompt and style. Generate black and white line art with thick lines suitable for coloring. Use when the user wants themed coloring pages, transparent PNG output, JPG export, reproducible prompt logs, or a series of connected pictures with consistent style.
---

# Coloring Book Generator

Use this skill to generate a printable coloring book with multiple pages, black and white line art with thick lines, transparent backgrounds, and a Markdown file that records the prompts and picture plan used for reproduction.

You can also provide a sample image as a style reference during generation.

## When To Use It

Use this skill when the user asks for any of the following:

- a themed coloring book
- coloring pages with a transparent background
- printable coloring pages
- a specific number of pages in a coloring book
- black and white line art suitable for coloring
- a reproducible prompt log for image generation
- OpenAI or Gemini / Nano Banana image generation
- consistent style across multiple coloring pages

## Workflow

1. Collect the required inputs:
   - `theme`: may be a short theme or a long prompt string
   - `style`: may be a short style or a long prompt string (optional, defaults to "simple line art")
   - `pages`: number of pages to generate (default to 5)
   - `reference_image`: optional reference picture for style consistency
   - `constraints`: optional hard requirements to apply across all pages; pass multiple `--constraint` flags
2. If needed, install local prerequisites:

```bash
bash skills/coloring-book-generator/scripts/install.sh
```

3. Run the bundled script:

```bash
python3 skills/coloring-book-generator/scripts/generate_coloring_book.py \
  --theme 'Underwater adventure with friendly sea creatures' \
  --style "simple line art, thick black outlines, minimal detail" \
  --constraint "square composition" \
  --constraint "all characters are smiling" \
  --pages 5 \
  --output-dir tmp
```

4. Confirm the outputs:
   - `<theme-slug>-<timestamp>-page-001.jpg` through `<theme-slug>-<timestamp>-page-XXX.jpg`
   - `<theme-slug>-<timestamp>-plan.md`

To use a local style reference image:

```bash
python3 skills/coloring-book-generator/scripts/generate_coloring_book.py \
  --theme 'Underwater adventure with friendly sea creatures' \
  --style "simple line art, thick black outlines, minimal detail" \
  --reference-image /absolute/path/to/reference.png \
  --constraint "square composition" \
  --constraint "submarine windows are round" \
  --pages 5 \
  --output-dir tmp
```

Example with multiple structural constraints:

```bash
python3 skills/coloring-book-generator/scripts/generate_coloring_book.py \
  --theme 'Happy Sukkot family scenes for young kids' \
  --reference-image /absolute/path/to/sukkah-reference.png \
  --constraint "square pictures" \
  --constraint "the sukkah roof is flat with a horizontal top edge" \
  --constraint "kids are smiling" \
  --pages 5 \
  --output-dir tmp
```

To use Gemini / Nano Banana instead of OpenAI:

```bash
python3 skills/coloring-book-generator/scripts/generate_coloring_book.py \
  --provider gemini \
  --theme 'Underwater adventure with friendly sea creatures' \
  --style "simple line art, thick black outlines, minimal detail" \
  --pages 5 \
  --output-dir tmp
```

Gemini also supports the same `--reference-image` option.

## Replay From Markdown

If you want to iterate from a previous run, edit the generated Markdown file and rerun with:

```bash
python3 skills/coloring-book-generator/scripts/generate_coloring_book.py \
  --replay-from-md tmp/your-theme-20260317-120000-plan.md \
  --output-dir tmp
```

Editable sections that affect the rerun:

- `Theme`
- `Style`
- `Constraints`
- `Reference image`
- `Number of pages`
- `Provider`
- `Picture Descriptions`
- `Generated Image Prompts`
- `Planner model`
- `Image model`

If `Generated Image Prompts` are present, the script uses them directly. If you remove those blocks, the script rebuilds the image prompts from the edited theme, style, and picture descriptions.

## Character Consistency for Storylines

**Enhanced Planning**: The script now specifically identifies and tracks main characters across pages:

```bash
python3 skills/coloring-book-generator/scripts/generate_coloring_book.py \
  --theme "Princess Luna (golden braided hair, blue star dress, silver crown) and Spark the dragon (small, purple, orange wings) explore a magical castle" \
  --pages 4 \
  --output-dir tmp
```

**Character-Focused Themes**: For best results, include detailed character descriptions in your theme:
- **Physical features**: hair color/style, clothing, distinctive accessories
- **Character names**: helps maintain identity across pages
- **Relationships**: how characters interact (friends, pets, siblings)

**What The Script Does

- **Character extraction**: Automatically identifies main characters from the theme and creates detailed descriptions for consistency
- Uses a text model to turn the theme and style inputs into:
  - an exact picture list for each page that advances a cohesive storyline
  - detailed character descriptions that get included in all image prompts
  - detailed image-generation prompts for each page
- Uses the image model to generate the first picture as a style and character reference
- **Enhanced character consistency**: All subsequent pages include character descriptions and use the first page as visual reference
- **Parallel generation**: After the first page, generates remaining pages in parallel for faster completion
- **Pure black and white**: Generates images with only pure black lines on white background, no gray colors or shading
- **Robust error handling**: If a page fails to generate (e.g., content policy violation), the script:
  - Skips that page and continues with remaining pages
  - Reports failed pages at the end with specific error messages
  - Documents failures in the markdown plan for future reference
- Exports each successful page as a separate JPEG file
- Writes a Markdown log with the user inputs, generated picture descriptions, model names, prompts used, and any failures
- Supports `--provider openai` and `--provider gemini`
- Defaults to OpenAI for maximum reliability

## Requirements

- **For OpenAI runs**: `OPENAI_API_KEY` or `OPEN_AI_TOKEN` must be set
- **For Gemini runs**: `GEMINI_API_KEY` or `GOOGLE_API_KEY` must be set
- This skill currently targets macOS because it relies on `sips`
- `scripts/install.sh` bootstraps Homebrew and Python 3 if needed, then verifies the Apple toolchain

## Notes

- **Performance**: After generating the first page for reference, remaining pages are generated in parallel (up to 3 concurrent requests) for faster completion
- **Pure black and white**: All images use only pure black lines on white background with absolutely no gray colors, shading, or gradients
- **Complete framing**: All coloring pages ensure that characters, objects, and scene elements are fully contained within page boundaries with no cropped or cut-off elements
- The first generated image is used as a style reference for all subsequent pages to maintain consistency
- **Error resilience**: The script gracefully handles content policy violations and API errors by skipping problematic pages while continuing to generate the rest
- Failed pages are clearly reported at the end with specific error messages and documented in the plan file
- **Default**: The script uses OpenAI for both planning and image generation by default (most reliable)
- **Gemini option**: Use `--provider gemini` to use Gemini for both planning and image generation
- If the user wants revisions, rerun the script with adjusted `theme`, `style`, or `pages`
- Each page is saved as a separate file to allow for individual printing or use
