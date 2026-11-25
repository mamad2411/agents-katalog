---
name: huashu-image-upload
description: One-click generation and upload of article illustrations to an image host, with automatic Markdown link insertion. Use when the user mentions "illustrations", "article images", "upload images", or "image for the article".
---

# Image Generation & Upload

A professional capability for automatically generating illustrations for WeChat articles, uploading them to an image host, and inserting Markdown links.

## When to Use This Skill

This skill is automatically loaded when the following scenarios are detected:

- The user says "add illustrations now", "help me with illustrations", or "add images"
- After article proofreading is complete and illustrations are needed
- When the article content is complete but images are missing

## Core Features

1. **Analyse illustration requirements**: Determine 5–8 illustrations needed based on article content
2. **Source images from**:
   - Public domain works (Wikimedia Commons, Google Arts & Culture)
   - AI-generated images (Volcano Engine doubao-seedream API)
   - Free stock libraries (Unsplash, Pexels)
3. **Auto-upload to image host**: Call ImgBB to obtain permanent links
4. **Insert Markdown**: Insert image links at the appropriate positions in the article
5. **Verify display**: Ensure all image links are valid

## Illustration Quantity Guidelines

- **Recommended**: 5–8 images
- **Minimum**: 3 images (cover + 2 body images)
- **Maximum**: No more than 10 (to avoid excessive interruption to reading flow)

## Illustration Placement Strategy

**Mandatory placement**:

- ✅ Cover image (hero image): Below the title — always required
- ✅ Core sections: 1 image per key section

**Optional placement**:

- Theory support (e.g., referencing a classic work)
- Data visualisation (comparison charts, graphs)
- Case supplements (product screenshots, examples)

## Image Source Priority

### 1️⃣ Public Domain Works (Highest Priority)

- **Sources**: Wikimedia Commons, Google Arts & Culture
- **Suitable for**: Classic artwork, historical portraits, ancient book covers
- **Advantages**: Free, no copyright issues, high quality
- **Examples**: Van Gogh's Starry Night, Kant portrait
- **Method**: Use WebFetch to obtain Wikimedia Commons image links

### 2️⃣ AI-Generated (Recommended)

- **Source**: Volcano Engine doubao-seedream-4-0-250828
- **Suitable for**: Cover images, concept art, abstract themes
- **Advantages**: Original, customisable, fast
- **Method**: Call API to generate image, returns a temporary URL

### 3️⃣ Free Stock Libraries

- **Sources**: Unsplash, Pexels, Pixabay
- **Suitable for**: Cover images, concept art, background images
- **Advantages**: Free, high quality, commercially usable (CC0)
- **Method**: WebFetch search + download

### 4️⃣ Screenshots / Official Assets (Citation required)

- **Sources**: YouTube, Bilibili, product websites, film posters
- **Suitable for**: Case images (product screenshots, video stills)
- **Note**: Cite the source; use under fair use principles
- **Method**: Remind user to take their own screenshot, or generate an AI concept image as a substitute

## Image Host Upload Workflow

### Core Script

Use the project's existing `/tools/upload_image.py` script

### Upload Method

```python
# Call upload script (via Bash)
python3 /Users/alchain/Documents/writing/tools/upload_image.py <image URL or local path>

# Handle web images (e.g., AI-generated temporary links)
python3 /Users/alchain/Documents/writing/tools/upload_image.py "https://example.com/ai-generated.jpg"

# Handle local images
python3 /Users/alchain/Documents/writing/tools/upload_image.py "/Users/alchain/Pictures/image.png"

# Script automatically returns ImgBB permanent link
```

### Fallback Mechanism

- ✅ Prefer uploading to ImgBB image host (permanent links)
- ⚠️ If upload fails, automatically use the original URL as a fallback
- 📌 See `/tools/README.md` for image upload script documentation

## Markdown Insert Format

```markdown
![Image description](https://i.ibb.co/xxxxx/image.jpg)
```

- Use permanent network links (not local paths)
- Write a meaningful image description (alt text)
- Keep descriptions concise and focused on the image content

## Image Specifications

### Size Specifications

- Cover image: 1200 x 600px (16:9)
- Body images: 800–1200px wide
- Person/product: 800 x 800px (1:1)

### File Specifications

- Format: JPG (photos) / PNG (illustrations)
- Size: < 500KB
- Naming: lowercase, semantic, in English (e.g., `mrbeast.jpg`, `starry-night.jpg`)

### Path Specifications

- ✅ Network link: `https://i.ibb.co/xxxxx/image.jpg` (recommended, permanent)
- ❌ Local path: No longer used (breaks when pasted into the WeChat editor)

## Copyright Notes

- ✅ Public domain works (author deceased 70+ years)
- ✅ CC0-licensed images (Unsplash, etc.)
- ✅ AI-generated images (confirm tool licence)
- ⚠️ Screenshots/official assets require source attribution

## Illustration Checklist

Before executing an illustration task, confirm:

- [ ] Article has been proofread and content is finalised
- [ ] Number of illustrations determined (5–8)
- [ ] Illustration positions confirmed (cover + core sections)
- [ ] All images obtained (AI-generated / public domain / stock)
- [ ] All images uploaded to ImgBB image host
- [ ] Image links are permanent network links (starting with https://)
- [ ] Images inserted in Markdown (using network links)
- [ ] Image descriptions (alt text) have been filled in
- [ ] All image links verified as valid (accessible)

## Execution Steps (5-Step Standard Workflow)

### Step 1: Analyse article and determine illustration requirements

- Read the full article, mark key sections
- List illustration requirements (6–8 items)
- Determine the position and purpose of each image

### Step 2: Source / generate images

Based on source priority order:

1. Public domain works → WebFetch to retrieve
2. AI-generated → Call API
3. Free stock → WebFetch search
4. Screenshot assets → Remind user to provide

### Step 3: Upload to image host, obtain permanent links

```bash
# Call upload script for each image
python3 /Users/alchain/Documents/writing/tools/upload_image.py <image URL>
```

### Step 4: Insert images into article

```markdown
![Image description](https://i.ibb.co/xxxxx/image.jpg)
```

### Step 5: Verify display

```bash
# Check all image references
grep -n "!\[" "article-path.md"
# All image links should start with https://
```

## Reference Resources

- `/tools/README.md` — Image upload script documentation
- `/tools/upload_image.py` — Image upload script
- `/writing/AI-image-generation-API.md` — AI image generation API documentation
- `/writing/images/illustration-best-practices.md` — Illustration best practices

## Frequently Asked Questions

### Q1: Will AI-generated image temporary links expire?

**A**: Yes. That's why you must call `upload_image.py` to upload to ImgBB and get a permanent link.

### Q2: What if the image host upload fails?

**A**: The script has a fallback mechanism and will automatically use the original URL. However, it's recommended to check your ImgBB API configuration.

### Q3: Does every article need illustrations?

**A**: Illustrations are strongly recommended, especially for long articles (3,000+ words). Short articles (under 1,000 words) may only need a cover image.

### Q4: Can local image paths be used?

**A**: Not recommended. Local paths break when pasted into the WeChat editor — always use network links.

## Technical Dependencies

- **Python script**: `/tools/upload_image.py` (already in place)
- **API configuration**: ImgBB API key (configured in `~/.zshrc`)
- **AI generation API**: Volcano Engine doubao-seedream (optional)
- **Tools**: WebFetch (for retrieving public domain images)

## Success Examples

- **"Why the Best Content Is Useless"**: 6 illustrations (2 public domain + 4 AI-generated)
- **"DeepSeek-OCR In-Depth Review"**: 5 illustrations, all uploaded to ImgBB, copy-pasted to WeChat without issue

---

**Last Updated**: 2025-11-07
**Applicable Projects**: WeChat article writing
**Maintained by**: Huashu

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
