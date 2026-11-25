---
name: competitive-site-cloning
version: 1.0.0
description: "Clone a competitor's CMS-built site (Duda, Wix, Squarespace), rebrand it as a demo business, and set up template variables for per-lead regeneration."
metadata:
  hermes:
    tags: [clone, duda, template, rebrand, site-generation, local-service]
    triggers:
      - clone competitor website
      - rebrand website as demo
      - duda site template
      - copy every page of website
      - set up site for regeneration
      - rebuild competitor site as template
    related_skills: [local-service-websites, astro-site-rebuild]
---

# Competitive Site Cloning & Template System

When the operator says "copy every page and set it up to just regenerate the wording
for everything" — this is the workflow.

## Workflow

### 1. Capture the Original Site

```bash
# Save full HTML
curl -sL "https://competitor.com" > assets/clones/competitor-raw.html

# Find all pages via sitemap
curl -sL "https://competitor.com/sitemap.xml" | grep -oP '<loc>[^<]+</loc>'

# Download CSS assets linked in HTML
# grep for href="*.css" and curl each one
```

### 2. Analyze Structure

Examine: sections, color scheme, fonts, navigation, image URLs, form targets,
JS behavior. Duda sites ship runtime.css, theme.css, page.css, widget.css
(~470KB total). The self-contained rebuild inlines only what's needed.

### 3. Rebuild as Self-Contained HTML

Single-file HTML with inline CSS and JS. No external dependencies
(except hosted images and Google Fonts CDN URLs). Match the layout quality
exactly — the operator compares against the original.

**Key UI rules the operator enforces:**
- No emoji anywhere (replaced with SVG icons)
- No badges/pills/chips
- No "Learn More" buttons on service cards
- No "coming soon" or "under construction" text
- All images must be photorealistic (Nano Banana Pro), not isometric/clay
- Hero overlay at 10% opacity
- Every nav link, button, and map must work — no broken functionality

### 4. Rebrand All Content

Replace every page's text with demo business data:
- Business name, phone, email, address
- City and region (use a DIFFERENT market than the original)
- Services reworded for the new niche
- All image URLs replaced with Nano Banana Pro CloudFront URLs
- Meta descriptions, OG tags, testimonials — everything

### 5. Add Template Variables

Replace every business-specific value with HTML comment placeholders:

```
<!-- BUSINESS_NAME -->  <!-- PHONE -->  <!-- CITY -->  <!-- REGION -->
<!-- NICHE -->  <!-- ADDRESS -->  <!-- EMAIL -->  <!-- HOURS -->
<!-- HERO_IMAGE -->  <!-- GALLERY_1 --> through <!-- GALLERY_6 -->
<!-- SERVICES_INJECTED -->  <!-- FAQ_INJECTED -->  <!-- WHY_INJECTED -->
<!-- CITY_LIST -->  <!-- MAP_QUERY -->  <!-- FORM_ID -->
<!-- ABOUT_HEADING -->  <!-- ABOUT_P1 -->  <!-- ABOUT_P2 -->
```

### 6. Build the Generator

A Python script at `scripts/generate_duda_site.py` fills the template for any lead.
The generator should handle:

- **Per-niche services** (plumber/hvac/electrician — 6 cards each with SVG icons)
- **Per-niche FAQs** (6 Q&A pairs)
- **Per-niche why-choose items** (6 bullet points)
- **Per-niche color schemes** (green accent for plumber, blue for HVAC, etc.)
- **City-cycle SEO rotation** — hero cycles through surrounding cities every 4s
- **Surrounding city lookup** for 16+ major metro areas (Dallas→Plano,Frisco,Garland...)
- **Auto-generated testimonials** with city references
- **Auto-generated meta descriptions** from name + city + niche
- **Working map embed** (Google Maps iframe, no API key needed)
- **Working contact form** (Formspree POST endpoint)

### 7. Deploy & Verify

```bash
# Generate
python3 scripts/generate_duda_site.py \
  --name "Demo Business" --phone "(555) 123-4567" \
  --city "City" --region "Region" --niche plumber

# Copy to demo path
cp output/{niche}/{slug}/index.html demo/{slug}/index.html

# Verify all features work
```

Checklist before pushing:
- [ ] Google Maps embed loads (`maps.google.com/maps?q=`)
- [ ] Contact form reaches Formspree (`formspree.io/f/`)
- [ ] City rotation JS enabled (`rotateCity`)
- [ ] All nav links scroll to sections
- [ ] FAQ accordion works
- [ ] Testimonial carousel auto-rotates
- [ ] Phone numbers are `tel:` clickable
- [ ] Hours displayed in contact section
- [ ] All 6 gallery images load
- [ ] No "Learn More" buttons

## Images: Nano Banana Pro Strategy

- Use Nano Banana Pro 2K (unlimited on Ultra plan) for ALL site photos
- Prompt for photorealistic scenes ("Photorealistic photograph of...")
- Images hosted on CloudFront — use URLs directly, no local storage
- Generate hero (16:9) + 6 gallery (4:3) images
- If credits exhausted for G6, use existing mass-gen image as fallback
- Previous van-isometric-diorama style was explicitly rejected — go photorealistic

**Example gallery shot types:**
- Hero: van/truck on residential street with plumber
- Under-sink pipe repair with tools
- Tankless water heater installation
- Drain snake machine in bathroom
- Handshake with happy customer
- Copper pipe soldering close-up

## Surrounding City Lookup Table

Built into the generator. Covers 16 metros: Dallas, Albany, Los Angeles, Houston,
Austin, San Antonio, Phoenix, Atlanta, Chicago, New York, Boston, Seattle, Miami,
Denver, Philadelphia, San Francisco. Add new entries to the `SURROUNDING_CITIES`
dict. Unlisted cities fall back to `"<city>","Serving All of <region>"`.

## Pitfalls

- **Duda sites are JS-heavy:** The captured HTML may embed most content in
  `window.Parameters` or JSON objects rather than visible DOM. Look for
  `window.APP_INITIALIZATION_STATE`, `window.Parameters`, and JSON-LD scripts.
- **Google Static Maps requires API key:** Use the embed iframe format instead
  (`maps.google.com/maps?q=QUERY&output=embed&z=12`) which needs no key.
- **Nano Banana Pro credit exhaustion:** The "unlimited stills" on Ultra plan
  has a per-billing-period cap on the standard generation pool. If generation
  fails with "not_enough_credits", fall back to earlier batch images.
- **Section comment markers are not template vars:** `<!-- HEADER -->`,
  `<!-- HERO -->`, `<!-- SERVICES -->`, etc. are developer section markers,
  not unfilled template variables. Don't report them as missing.
- **CLI image generation on Windows:** Use background processes for each image
  (they take ~30-60s each). Download via Python urllib, not curl (MSYS path issues).
  Check job status with `hf generate get <job_id>` to get the CloudFront URL.
