---
name: business-card-image-design
description: "Generate professional UK business card front and back image designs from the correct client/project folder using codex-imagen. Use this whenever the user asks for a business card design, print-ready card artwork, UK 85mm x 55mm cards, celebrant/APC cards, or asks to turn current-folder client details into front/back business card images. This is a multi-stage workflow: first resolve the source folder, gather evidence-backed business/person/brand details, fill gaps, then generate separate raster card faces. Prefer this skill over HTML mockups when the user wants generated image artwork."
---

# Business Card Image Design

Create two separate generated image files for a UK business card:

- Front of card
- Back of card

Use `codex-imagen` for the actual artwork generation. Do not substitute an HTML/CSS mockup unless the user explicitly asks for HTML; this skill is for generated raster artwork.

## Bundled Resources

Read these only when needed:

- `references/business-card-prompt-template.md` - prompt skeleton for front and back card generation.
- `assets/APC-seal.png` - bundled Academy of Professional Celebrants seal. Use this as the fallback APC/accreditation reference when a client/project folder does not already include a better approved APC badge.

## Requirements

- CLI: `codex-imagen`
- Optional but preferred: ImageMagick `magick`
- Bundled APC seal:
  `/Users/jack/.agents/skills/business-card-image-design/assets/APC-seal.png`

The artwork size is 91mm x 61mm, which is the standard UK 85mm x 55mm card plus 3mm bleed on every side. Important content must sit comfortably inside the trimmed 85mm x 55mm area; backgrounds and decoration may extend to the edge.

Use a 91:61 aspect ratio for the delivered images. A practical print raster target is `2150x1441` pixels, which is roughly 600 DPI for 91mm x 61mm. If the image generator returns a different size, use ImageMagick to resize and crop/pad to `2150x1441` while preserving the design.

## Operating Principle

Treat the current project folder as the source of truth. The quality of the card depends on using the right client's real site, assets, copy, and contact details. Do not skip straight to image generation from a generic prompt.

If the user says "current folder", "this repo", "the client in here", or similar, first prove the working directory is the intended client/project folder. If the current directory is only a Codex scratch folder or does not contain client/site evidence, locate the actual project folder before generating. Use an explicit user-provided path when available. If the user only gives a client name and the folder is unclear, use `pj-browse` to find candidate client folders, then choose the obvious match or ask a short question.

Good evidence that you are in the right folder includes:

- client/business name in `package.json`, `README`, site metadata, content files, or visible copy
- contact details, website URL, or service pages
- logo and brand assets in `public/`, `assets/`, `src/assets/`, `static/`, or media folders
- existing print/collateral folders such as `print-output/`, `brochure-materials/`, `output/`, `docs/`, or `assets/`

## Multi-Stage Workflow

### Stage 1: Resolve The Source Folder

1. Run `pwd` and inspect the immediate directory shape.
2. If the user provided a folder path, use that path as the project root.
3. If the current folder looks like the client/project repo, continue there.
4. If the current folder is a Codex temporary workspace or otherwise not the client repo, find the client folder:
   - use `pj-browse` when a client name or project hint is available
   - otherwise search under `/Users/jack/Documents/GitHub` with `rg --files` and targeted folder names
5. In the final response, state the source folder used. Do not generate from an uncertain folder.

### Stage 2: Gather A Card Brief

Create a short working note before generation, usually at `work/business-card-brief.md` or the project repo's `print-output/business-card-brief.md`. Record both the value and where it came from.

Gather:

- business name
- tagline or short description
- person name
- role/title
- phone
- email
- website URL
- services, preferably 3-5 short service labels
- brand colours and design cues
- website or local page used for inspiration
- logo asset path
- person/photo asset path, if present
- badge/accreditation asset paths
- any existing cards, brochures, flyers, or print assets that should influence the design

Search likely source locations:

- `AGENTS.md`, `README*`, `docs/`, notes, handover docs, and project setup files
- `package.json`, framework config, `src/`, `app/`, `pages/`, `components/`, `content/`, `data/`, `lib/`, and `config/`
- `public/`, `assets/`, `src/assets/`, `static/`, `media/`, image folders, favicons, and logo folders
- constants, metadata, SEO, schema, contact, navigation, footer, homepage, about, services, and location pages
- existing `print-output/`, `brochure-materials/`, `output/`, PDFs, cards, brochures, and flyers

Use `rg` for contact details and business facts. Useful searches:

```bash
rg -n "phone|tel:|email|mailto:|website|www\\.|https?://|services|about|role|title|tagline|APC|Academy|Professional Celebrants" .
rg --files | rg -i "logo|brand|headshot|portrait|photo|badge|seal|apc|card|brochure|flyer|print"
```

### Stage 3: Fill Gaps Before Generation

Do not silently invent missing contact details. Separate facts into:

- `confirmed` - found in the user prompt or project files
- `inferred` - reasonable from surrounding copy, but not explicit
- `missing` - needed for the requested card but not found

If a key field is missing, handle it before generation:

- Ask the user for critical missing details such as person name, phone, email, or website.
- If the user wants you to proceed anyway, omit missing fields cleanly rather than fabricating them.
- For services, infer short labels from the site's actual service pages or homepage sections when available.
- For brand colours, sample from CSS variables, logo colours, existing design tokens, or visible website assets. If no formal palette exists, describe cues rather than pretending exact brand guidelines exist.

Only move to image generation once the prompt fields are either confirmed, responsibly inferred, or intentionally omitted.

### Stage 4: Build The Reference Set

Identify a small set of high-signal references. Too many references can confuse the generator.

Prefer:

- actual logo file
- person/headshot photo when the back design should include it
- existing brochure/card/flyer assets if they show approved brand treatment
- website screenshot or hero imagery only when it adds useful visual direction
- bundled APC seal when relevant:
  `/Users/jack/.agents/skills/business-card-image-design/assets/APC-seal.png`

If the project folder already contains an approved APC seal or badge, prefer the project asset. Use the bundled `assets/APC-seal.png` when the project lacks one.

For traceability, record reference asset paths in the working brief and pass them to `codex-imagen` with repeated `--input-ref` flags.

### Stage 5: Assemble The Generation Prompts

Write two prompt files:

- `work/business-card-front-prompt.txt`
- `work/business-card-back-prompt.txt`

Use `references/business-card-prompt-template.md` and replace every placeholder. If a field is intentionally omitted, remove that line from the prompt rather than leaving placeholders like `[PHONE NUMBER]`.

The prompt should include the gathered card brief in direct plain language. It should also state:

- generate flat, straight-on card artwork, not a lifestyle mockup
- use full-bleed 91mm x 61mm ratio
- do not show crop, bleed, trim, or safe-margin marks
- keep important content well inside the safe area
- use the supplied reference assets for brand feel, not as random collage elements

### Stage 6: Generate Front And Back With `codex-imagen`

Generate the two sides separately. Use deterministic output paths when practical.

Example command shape:

```bash
codex-imagen --json --timeout 300 \
  --output ./print-output/business-card-front.png \
  --input-ref /path/to/logo.png \
  --input-ref /Users/jack/.agents/skills/business-card-image-design/assets/APC-seal.png \
  --prompt-file ./work/business-card-front-prompt.txt

codex-imagen --json --timeout 300 \
  --output ./print-output/business-card-back.png \
  --input-ref /path/to/logo.png \
  --input-ref /Users/jack/.agents/skills/business-card-image-design/assets/APC-seal.png \
  --prompt-file ./work/business-card-back-prompt.txt
```

Only include the APC seal `--input-ref` when APC/accreditation is relevant. Omit unavailable `/path/to/logo.png` examples in real commands; do not pass fake paths.

### Stage 7: Verify And Normalize The Output

Check dimensions:

```bash
magick identify -format '%w %h %[fx:w/h]\n' ./print-output/business-card-front.png
magick identify -format '%w %h %[fx:w/h]\n' ./print-output/business-card-back.png
```

Target ratio: `91 / 61 = 1.4918032787`.

If the file is not already close to 91:61, normalize to `2150x1441`.

ImageMagick normalization:

```bash
magick input.png -resize 2150x1441^ -gravity center -extent 2150x1441 output-91x61.png
```

Use this carefully: if cropping would cut off important content, regenerate with a stronger safe-space prompt instead of accepting a bad crop.

### Stage 8: Inspect Before Delivery

Inspect the final images visually. Confirm:

- front and back are separate files
- no visible crop marks, bleed lines, trim lines, or safe-margin guides
- important text, logos, badges, QR codes, and photos have generous internal spacing
- business/person/contact details are legible and not misspelled
- the card reads as a premium printed business card, not a poster, flyer, or social post

If text is misspelled or unreadable, regenerate. Image models often struggle with text, so be strict.

## Prompt Content

Each prompt should include:

- Full artwork size: 91mm x 61mm
- Trimmed UK card size: 85mm x 55mm
- 3mm bleed on all sides
- No visible bleed, crop, trim, or margin marks
- Generous safe space for important content
- Clean, modern, professional layout
- Separate side-specific content
- Brand cues from local assets, website, and user-provided details
- Flat front-on artwork, not a mockup on a desk
- Source folder and reference assets used

Front side content:

- Business logo
- Business name
- Tagline or short description
- Clean visual branding
- Minimal confident layout

Back side content:

- Person name
- Role or title
- Phone
- Email
- Website
- Key services
- Professional person image if supplied
- Trust/certification/partner/accreditation badge if supplied

## Output Contract

Return:

- Source folder used
- Brief/gap summary
- Front image path
- Back image path
- Any normalized image paths if different from the raw generations
- Source prompt files used
- Reference assets used
- Verification summary with dimensions and known caveats

If exact print-ready production is required, say whether the output is generated raster artwork only or whether a designer/printer still needs a vector/PDF prepress pass. Do not overclaim colour accuracy, embedded fonts, CMYK conversion, or guaranteed printer acceptance unless those checks were actually performed.
