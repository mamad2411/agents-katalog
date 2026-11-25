---
name: ebook
description: "Generate professional, sell-ready PDF ebooks from any topic, YouTube channel, or website. Researches content via web scraping, YouTube analysis, and /last30days skill. Uses Gemini Pro for content writing and image generation. Produces premium PDF with cover art, professional typography, and custom design matching the creator's branding. Use when the user says 'ebook', 'e-book', 'create an ebook', 'generate a PDF book', 'digital product from YouTube', 'ebook from topic', or wants to create a sellable digital product (PDF guide, mini-course book, lead magnet)."
allowed-tools: Bash(python3 *), Bash(pip3 install *), Bash(curl *), Bash(yt-dlp *), Bash(ls *), Bash(mkdir *), Bash(open *), Bash(base64 *), Bash(cat *), Bash(wc *)
---

# Professional E-book Generator

Generate sell-ready PDF ebooks from a topic, YouTube channel, or website. Uses Gemini Pro for content + images, WeasyPrint for PDF rendering.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/ebook [topic]` | Create ebook from a topic |
| `/ebook [youtube-url]` | Create ebook from YouTube channel content |
| `/ebook [website-url]` | Create ebook from website/blog content |
| `/ebook [topic] --pages 50` | Specify page count |
| `/ebook [topic] --lang en` | Specify language (default: fr) |

## Workflow Overview

```
GATHER INFO → RESEARCH → BRAND ANALYSIS → OUTLINE → WRITE CHAPTERS → GENERATE IMAGES → ASSEMBLE HTML → RENDER PDF
```

## Step 1: Gather Information

Ask the user for:
1. **Source** — Topic, YouTube channel URL, or website URL
2. **Pages** — Target page count (default: 30-40)
3. **Language** — fr (default) or en
4. **Author name** — For the cover and about page
5. **Author photo** — Path (optional, for about page)
6. **CTA** — What to promote at the end (next product, community, coaching...)

If the user provides only a topic or URL, infer reasonable defaults and proceed.

## Step 2: Deep Research

Run research in parallel using multiple sources:

### 2a. If YouTube channel provided
Scrape the channel to understand the creator's content, voice, and expertise:

```bash
# Get channel video list with titles and descriptions
yt-dlp --flat-playlist --print "%(id)s|%(title)s|%(view_count)s|%(description).200s" \
  "[CHANNEL_URL]/videos" 2>/dev/null | sort -t'|' -k3 -nr | head -20
```

Download and read thumbnails to understand visual branding:
```bash
# Get channel banner/avatar for brand colors
yt-dlp --write-thumbnail --skip-download --convert-thumbnails png \
  -o "/tmp/ebook_yt_%(id)s" "[TOP_VIDEO_URL]" 2>/dev/null
```

Transcribe 2-3 top videos (use WebFetch on auto-generated transcript URLs or summarize descriptions) to capture the creator's voice, frameworks, and key teachings.

### 2b. If website provided
Use WebFetch to scrape:
- Homepage (brand, positioning, value prop)
- About page (author bio, credibility)
- Blog/content pages (topics, writing style, expertise)
- Extract colors, fonts, and design patterns from CSS/meta tags

### 2c. Topic research (always)
Use the `/last30days` skill to research the topic:
- What people are discussing on Reddit
- Latest trends and debates
- Common questions and pain points
- What's working vs. what's outdated

Also use WebSearch for:
- Top-performing content on the topic
- Statistics and data points to include
- Competitor ebooks (to differentiate)

### 2d. Synthesize Research
Compile all research into a structured brief:
- Creator profile (name, niche, voice, expertise)
- Topic landscape (trends, pain points, opportunities)
- Target reader persona
- Unique angle for the ebook
- Key data points and examples to include

## Step 3: Brand & Design Analysis

### Extract Creator's Visual Identity
From YouTube/website, identify:
- **Primary color** (dominant brand color)
- **Secondary color** (supporting color)
- **Accent color** (CTAs, highlights)
- **Font style** (modern, editorial, tech, etc.)
- **Visual mood** (dark/light, minimal/rich, playful/serious)

If no source to analyze, ask the user or use a fallback palette.
See [references/design-system.md](references/design-system.md) for palette options and font pairings.

### Choose Design Configuration
Based on brand analysis, set:
```
PALETTE: {primary, secondary, accent, text, background}
FONTS: {heading_font, body_font, accent_font}
STYLE: {dark|light}
FORMAT: {trade|a4} (trade = 6x9in for ebooks, a4 for guides)
```

## Step 4: Create Outline with Gemini Pro

Select the appropriate structure template from [references/ebook-structures.md](references/ebook-structures.md) based on page count and content type.

Call Gemini 2.5 Pro to generate a detailed outline. See [references/prompts.md](references/prompts.md) — Phase 1 prompt.

```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "OUTLINE_PROMPT_HERE"}]}],
    "generationConfig": {"temperature": 0.8, "maxOutputTokens": 8192}
  }' > /tmp/ebook_outline.json
```

Extract the text response:
```python
python3 -c "
import json
with open('/tmp/ebook_outline.json') as f:
    data = json.load(f)
print(data['candidates'][0]['content']['parts'][0]['text'])
"
```

**Show the outline to the user for approval before proceeding.**

## Step 5: Generate Content Chapter by Chapter

For each chapter, call Gemini 2.5 Pro with the chapter writing prompt from [references/prompts.md](references/prompts.md) — Phase 2.

**Critical rules:**
- Generate chapters sequentially (each needs context from previous)
- Pass the previous chapter summary to maintain flow
- Each chapter outputs clean HTML with semantic classes
- Target ~250 words per page for comfortable reading
- Save each chapter to `/tmp/ebook_ch_N.html`

Generate the introduction first (Phase 3 prompt), then chapters, then conclusion (Phase 6 prompt).

### Content Quality Checks
After generating each chapter, verify:
- [ ] Opens with a hook (not "In this chapter...")
- [ ] Contains at least 1 example or story
- [ ] Has a tip-box or pull-quote
- [ ] Ends with key takeaways
- [ ] Matches the creator's voice/tone
- [ ] All HTML tags are properly closed

## Step 6: Generate Images with Gemini

### 6a. Cover Art
Generate the cover illustration using Gemini 3 Pro Image. See [references/prompts.md](references/prompts.md) — Phase 4.

```bash
curl -s -o /tmp/ebook_cover_raw.json \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "COVER_PROMPT_HERE"}]}],
    "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]}
  }'

python3 scripts/extract_gemini_image.py /tmp/ebook_cover_raw.json /tmp/ebook_cover.png
```

### 6b. Chapter Illustrations (optional, for premium feel)
Generate 1 illustration per chapter using Phase 5 prompt. Run in parallel for speed.

### 6c. Cover Composition
The cover image has NO text. Composite title + author name using HTML/CSS in the final assembly (WeasyPrint handles this perfectly with the cover page styling).

## Step 7: Assemble HTML

Build a single HTML file that WeasyPrint will convert to PDF.

### HTML Structure
```html
<!DOCTYPE html>
<html lang="{LANG}">
<head>
  <meta charset="UTF-8">
  <style>
    :root {
      --primary: {PRIMARY};
      --secondary: {SECONDARY};
      --accent: {ACCENT};
      --text: {TEXT_COLOR};
      --bg: {BG_COLOR};
      --accent-5: {ACCENT}0D;
      --accent-20: {ACCENT}33;
    }
    @import url('https://fonts.googleapis.com/css2?family={HEADING_FONT}:wght@700;800&family={BODY_FONT}:wght@400;500;600&display=swap');
    body { font-family: '{BODY_FONT}', sans-serif; }
    h1, h2, h3 { font-family: '{HEADING_FONT}', sans-serif; }
  </style>
</head>
<body>
  <!-- COVER PAGE -->
  <div class="cover">
    <img class="cover-bg" src="/tmp/ebook_cover.png" alt="">
    <div class="cover-content" style="color: white; text-shadow: 0 2px 20px rgba(0,0,0,0.8);">
      <h1>{TITLE}</h1>
      <div class="subtitle">{SUBTITLE}</div>
      <div class="author">{AUTHOR_NAME}</div>
    </div>
  </div>

  <!-- TABLE OF CONTENTS -->
  <div class="toc">
    <h2>Table des matieres</h2>
    <!-- Generate TOC entries from chapters -->
  </div>

  <!-- CHAPTERS -->
  <!-- Insert each chapter HTML here -->
  <div class="chapter-opener">
    <div class="chapter-number">01</div>
    <h1>{Chapter Title}</h1>
    <p class="chapter-intro">{Chapter summary quote}</p>
    <img class="chapter-illustration" src="/tmp/ebook_ch1_img.png" alt="">
  </div>
  <!-- Chapter content -->
  <div class="page-break"></div>

  <!-- ABOUT AUTHOR -->
  <div class="about-author">
    <img class="author-photo" src="{AUTHOR_PHOTO}" alt="{AUTHOR_NAME}">
    <h2>A propos de l'auteur</h2>
    <p>{AUTHOR_BIO}</p>
  </div>

  <!-- CTA PAGE -->
  <div class="cta-page">
    <h2>{CTA_HEADLINE}</h2>
    <p class="cta-text">{CTA_TEXT}</p>
    <div class="cta-box">{CTA_BUTTON_TEXT}</div>
    <p>{CTA_URL}</p>
  </div>
</body>
</html>
```

Save the assembled HTML to `{OUTPUT_DIR}/ebook.html`.

## Step 8: Render PDF

```bash
pip3 install weasyprint 2>/dev/null
python3 scripts/generate_pdf.py {OUTPUT_DIR}/ebook.html {OUTPUT_DIR}/{SLUG}.pdf --format trade
```

Verify the PDF:
```bash
# Check file size and page count
python3 -c "
from weasyprint import HTML
doc = HTML(filename='{OUTPUT_DIR}/ebook.html').render()
print(f'Pages: {len(doc.pages)}')
"
ls -lh {OUTPUT_DIR}/{SLUG}.pdf
```

Open the PDF for the user:
```bash
open {OUTPUT_DIR}/{SLUG}.pdf
```

## Step 9: Present & Iterate

Show the user:
- PDF file path and size
- Page count
- Cover preview (read the cover image)
- Table of contents

Offer iterations:
- "Adjust the design/colors?"
- "Rewrite a specific chapter?"
- "Add more pages/content?"
- "Change the cover style?"
- "Export in A4 format?"

## Output

Default directory: `~/Documents/ebook/`
Files produced:
- `{slug}.pdf` — The final ebook (main deliverable)
- `ebook.html` — Source HTML (for future edits)
- `cover.png` — Cover artwork
- `ch_N_img.png` — Chapter illustrations

## Technical Notes

- **Gemini text model**: `gemini-2.5-pro` (best quality for long-form writing)
- **Gemini image model**: `gemini-3-pro-image-preview` (best for illustrations)
- **PDF engine**: WeasyPrint (HTML/CSS to PDF, supports @page, fonts, images)
- **API key**: `$GEMINI_API_KEY` (must be exported in environment)
- **Dependencies**: `pip3 install weasyprint` (auto-installed if missing)
- **Font loading**: Google Fonts via @import in HTML (WeasyPrint fetches them)

## Quality Gates

- [ ] Cover looks professional (no AI text artifacts, clean composition)
- [ ] All pages render correctly (no overflow, no cut text)
- [ ] Typography is consistent (headings, body, quotes)
- [ ] Colors match creator's brand
- [ ] Content reads naturally (not robotic/AI-sounding)
- [ ] Every chapter has actionable value
- [ ] CTA page is compelling
- [ ] PDF file size under 20MB
- [ ] Page count matches target (+/- 5 pages)
