---
name: beautiful-websites
description: Find local businesses with outdated websites, redesign them with premium single-file HTML sites, and deploy them to Vercel. Use when the user wants to generate proof-of-work redesigns for outreach, create portfolio pieces from real business sites, or run the full pipeline (scrape → qualify → redesign → deploy) for a specific niche and city. Triggers on phrases like "beautiful websites", "redesign local business sites", "run the pipeline for [niche] in [city]", or any request to scrape, qualify, redesign, and deploy business websites.
---

# Beautiful Websites

Find local businesses with bad websites. Redesign them. Deploy them. Use them as proof.

A 4-step pipeline that turns "nail salons in Austin TX" into a list of live Vercel URLs showing premium redesigns ready to pitch back to the owners.

---

## What This Skill Does

This skill Find local businesses with outdated websites, redesign them with premium single-file HTML sites, and deploy them to Vercel. Use when the user wants to generate proof-of-work redesigns for outreach, create portfolio pieces from real business sites, or run the full pipeline (scrape → qualify → redesign → deploy) for a specific niche and city. Triggers on phrases like "beautiful websites", "redesign local business sites", "run the pipeline for [niche] in [city]", or any request to scrape, qualify, redesign, and deploy business websites.

## How to Run

### Full pipeline (with review pauses — default)

```
Run the beautiful websites pipeline for nail salons in Austin TX
```

Charles, I'll pause after each step to show you results and wait for your approval before continuing. This is the default because the scrape step costs money and the qualify step is subjective.

### Full pipeline (automatic — no pauses)

```
Run the beautiful websites pipeline for nail salons in Austin TX --auto
```

Runs all 4 steps back-to-back. Only use this when you're confident in the pipeline.

### Individual steps

```
Scrape leads for nail salons in Austin TX
Qualify the leads
Redesign the sites
Deploy the sites
```

---

## The 4 Steps

```
scrape → qualify → redesign → deploy
```

| Step | What It Does | Cost |
|------|-------------|------|
| **scrape** | Queries Google Maps via Apify. Filters to businesses with email + website. | $4 per 1,000 places |
| **qualify** | Screenshots each site, visually assesses YES/NO. | Free |
| **redesign** | Generates premium single-file HTML site. | Free |
| **deploy** | Deploys to Vercel, captures live URL. | Free |

---

## Step 1: Scrape Leads

**Goal:** Get a list of local businesses with both an email and a website.

**What I do:**

1. Read `APIFY_TOKEN` from `.env` (required)
2. Parse the user's request into search query (business type) and location (city/region)
3. Start an Apify run via API:
   ```
   POST https://api.apify.com/v2/acts/lukaskrivka~google-maps-with-contact-details/runs?token={APIFY_TOKEN}
   ```
   Body:
   ```json
   {
     "searchStringsArray": ["{business type only, e.g. nail salons}"],
     "locationQuery": "{city/region only, e.g. Austin TX}",
     "countryCode": "{country code, e.g. us, au, gb}",
     "maxCrawledPlacesPerSearch": 20,
     "language": "en",
     "maxImages": 0,
     "maxReviews": 0
   }
   ```
4. Poll every 8 seconds until `status === "SUCCEEDED"`
5. Download results from the dataset
6. Filter to businesses with:
   - A `website` field (not empty)
   - At least one entry in the `emails` array
   - Website that is NOT a Facebook/Yelp/Instagram page
   - Name that is NOT a national chain (Supercuts, Great Clips, Holiday Inn, Marriott, etc.)
7. Save to `scrape_results.json` with this structure:
   ```json
   [
     {
       "name": "Zen Nail Bar",
       "email": "owner@zennailbar.com",
       "website": "https://zennailbar.com",
       "phone": "+1-512-555-0123",
       "address": "1234 Main St, Austin, TX 78701",
       "rating": 4.7,
       "reviewCount": 142,
       "category": "Nail salon"
     }
   ]
   ```

**Pause:** Show count and table with name, website URL (clickable), and email. Ask: "Proceed to qualify?"

**Cost:** Before running, tell Charles: "I'm about to scrape [X] places, which will cost approximately $[Y]. OK to proceed?" Never run without explicit approval.

---

## Step 2: Qualify Leads

**Goal:** Screenshot each site and decide if it's worth redesigning.

**What I do:**

1. Read `qualify_results.json` if it exists — skip any lead already processed
2. Read `sites/build-log.md` — skip any business name or website URL already in the log
3. For each remaining lead in `scrape_results.json`:
   - Run `node scripts/screenshot.js --url {website} --out screenshots/{slug}.png`
   - Read the PNG image directly (vision)
   - Apply the qualification criteria below
   - Return `YES`, `NO`, or `SKIP` with a one-line reason
4. Save output to `qualify_results.json`:
   ```json
   [
     {
       "name": "Zen Nail Bar",
       "email": "owner@zennailbar.com",
       "website": "https://zennailbar.com",
       "qualify": "YES",
       "reason": "Fixed-width layout, clip art graphics, no CTA, copyright 2011.",
       "screenshotPath": "screenshots/zen-nail-bar.png"
     }
   ]
   ```

**Qualification criteria:**

The bar is HIGH. The question is: "Does this site look like a premium, custom-designed experience?" Most local business sites will be a YES.

A site scores **YES** (worth redesigning) if it shows **any** of these signals:

- Outdated visual design (table layouts, clip art, beveled buttons, tiled backgrounds)
- Pre-2015 aesthetic (text drop shadows, gradients on everything, marquee text)
- No mobile responsiveness (fixed-width, horizontal scrollbar visible)
- Basic or flat typography (only one font, no contrast, generic system fonts)
- No clear hero or CTA (wall of text, no button above the fold)
- Cluttered layout (too many elements competing, no visual hierarchy)
- Low-quality or missing imagery (few photos, broken images, stock photos)
- Trust-eroding signals (`http://` only, copyright pre-2018, "under construction" notice)
- Template look (Wix ADI, GlossGenius, Setmore, basic Squarespace)
- Bland buttons or navigation (plain rectangular buttons, basic text links, no hover effects)
- Lacks premium feel (generic, no distinct brand personality, no rich visuals, no polish)

A site scores **NO** (skip) ONLY if it meets ALL of these:

- Custom or high-end design that feels like real money was spent on it
- Rich, high-quality photography throughout
- Distinctive typography with clear font pairing (display + body fonts)
- Smooth interactions, animations, or transitions
- Strong brand personality — you can tell this isn't a template

**Pause:** Show the YES/NO breakdown with reasons. Ask: "Proceed to redesign?"

---

## Step 3: Redesign Sites

**Goal:** Generate a premium single-file HTML site for each YES lead.

**What I do:**

1. For each lead where `qualify === "YES"`:
   - Use `web_fetch` to scrape their current website content
   - Check `sites/build-log.md` to avoid repeating a design combo
   - Pick a unique palette + font + layout combination from the design system below
   - Search Unsplash for 2–3 photos relevant to the business type
   - Verify each photo URL loads (200 status) before using it
   - Generate a complete `index.html` using the design system below
   - Save to `sites/{business-slug}/index.html`
   - Append to `sites/build-log.md` with: business name, slug, palette, font, layout, date

**Architecture rules (NEVER BREAK):**

- **One file only** — all CSS in `<style>`, all JS in `<script>`, no separate files
- **No frameworks** — no React, no Vue, no Tailwind build, no npm
- **CDN only** — Google Fonts, GSAP, Lucide Icons
- **No placeholder text** — write real copy from the scraped business data
- **6 sections always** — Navbar, Hero, Services, Philosophy, Contact, Footer
- **Dynamic copyright year** — never hardcode the year. Use `new Date().getFullYear()` in JS to set it

**Required CDN scripts:**

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script src="https://unpkg.com/lucide@latest"></script>
```

**Design system:** Pick ONE from each column. Never repeat the same combo. Check `sites/build-log.md` first.

### Color Palettes

**Dark:**

| Code | Name | Values |
|------|------|--------|
| P1 | Warm Night | `--bg:#080A0C --card:#111518 --accent:#C9A87C --text:#F2EDE8 --muted:#8A8B8D` |
| P2 | Deep Teal | `--bg:#0A1014 --card:#121A1F --accent:#5EADB5 --text:#E8F0F2 --muted:#7A9098` |
| P3 | Noir Plum | `--bg:#0C080E --card:#16111A --accent:#A8748E --text:#F0EBF0 --muted:#8A7E8C` |
| P4 | Slate Ember | `--bg:#0D0E10 --card:#161819 --accent:#C47A4A --text:#ECE8E4 --muted:#8B8985` |
| P5 | Midnight Forest | `--bg:#070B09 --card:#0F1612 --accent:#4CA879 --text:#E8F2EC --muted:#7A8E82` |

**Light:**

| Code | Name | Values |
|------|------|--------|
| P6 | Cream & Sage | `--bg:#F5F1EC --card:#FFFFFF --accent:#5B7A5E --text:#1A1A1A --muted:#6B6B6B` |
| P7 | Blush Editorial | `--bg:#FAFAF8 --card:#FFFFFF --accent:#BF8B8B --text:#2D2D2D --muted:#888888` |
| P8 | Warm Ivory | `--bg:#F8F4EF --card:#FFFDF9 --accent:#B8860B --text:#1C1914 --muted:#7A7468` |
| P9 | Cloud Lavender | `--bg:#F6F4F9 --card:#FFFFFF --accent:#7B68AE --text:#22202A --muted:#7E7A88` |
| P10 | Pearl Marine | `--bg:#F2F6F8 --card:#FFFFFF --accent:#3D7A8A --text:#1A2528 --muted:#6B7E85` |

### Font Pairings

| Code | Sans (Body) | Serif (Display) | Mood |
|------|-------------|-----------------|------|
| F1 | Outfit 300–700 | Cormorant Garamond italic | Elegant luxury |
| F2 | DM Sans 400–700 | Playfair Display italic | Classic editorial |
| F3 | Inter 300–700 | Lora italic | Clean modern |
| F4 | Sora 300–700 | Instrument Serif italic | Tech luxury |
| F5 | Plus Jakarta Sans 300–700 | Fraunces italic | Warm editorial |
| F6 | Manrope 300–700 | Bodoni Moda italic | High fashion |
| F7 | Space Grotesk 400–700 | Crimson Pro italic | Contemporary |
| F8 | Nunito Sans 300–700 | Libre Baskerville italic | Approachable classic |
| F9 | Figtree 300–700 | Noto Serif Display italic | Bold editorial |
| F10 | Rubik 300–700 | EB Garamond italic | Timeless warmth |

**Google Fonts URL pattern:**

```html
<link href="https://fonts.googleapis.com/css2?family={SANS_FONT}:wght@300;400;700&family={SERIF_FONT}:ital@1&display=swap" rel="stylesheet">
```

### Layouts

| Code | Hero | Cards | Navbar |
|------|------|-------|--------|
| L1 | Content bottom-left | 3-column grid | Pill-shaped floating |
| L2 | Centered text | 2-column zig-zag | Slim top-bar |
| L3 | Split-screen 50/50 | Horizontal divider rows | Full-width thin bar |
| L4 | Center-aligned stack | Full-width horizontal cards | Thin line top |
| L5 | Asymmetric 60/40 | Masonry 2-column | Thick bar, large logo |

### Photos (Unsplash — free, dynamic search)

Do NOT use a fixed photo bank. Instead, find photos relevant to each specific business.

**How to find photos:**

1. Determine the business type and category (e.g. nail salon, wedding venue, med spa)
2. Search Unsplash for relevant terms: `https://unsplash.com/s/photos/{search-term}`
3. Pick 2–3 photos that are relevant to what the business actually does
4. Use the direct image URL format: `https://images.unsplash.com/photo-{ID}?w={width}&h={height}&fit=crop&q=80`

**Rules:**

- Photos must be relevant to the business — a nail salon gets nail photos, a wedding venue gets wedding photos
- Use at least 2 photos per site, max 3
- Before using any photo, verify it loads by fetching `https://images.unsplash.com/photo-{ID}?w=400&q=60` and confirming a 200 status (not 404). Unsplash photos can be removed at any time.
- If a photo returns 404, find a replacement — never leave a broken image in the final site
- The hero photo should be high impact and relevant to the business atmosphere

### Quality Standards (always applied)

- GSAP scroll-triggered fade-up animations on all sections
- Noise texture overlay (`opacity: 0.04` dark / `0.02` light)
- Magnetic button hover (`scale(1.03)`, `translateY(-1px)`)
- Responsive at 375px mobile and 1440px desktop
- Clickable `tel:` and `mailto:` links
- Navbar transitions on scroll

**JS Safety — prevent invisible cards:**

```css
/* Always include this */
.service-card { opacity: 1 !important; }
```

```js
// Always init Lucide before GSAP
try { lucide.createIcons(); } catch(e) {}
gsap.registerPlugin(ScrollTrigger);
```

**Pause:** Describe each site built (design choices, key content). Ask: "Deploy these?"

---

## Step 4: Deploy to Vercel

**Goal:** Deploy each site to Vercel and capture the live URL.

**What I do:**

1. Check if `VERCEL_TOKEN` is set in `.env` (required for remote/SSH, optional for local)
2. If no token, run `vercel login` to authenticate via browser (local only)
3. For each site folder in `sites/`:
   - Run `vercel deploy --yes --prod sites/{slug}` (add `--token {VERCEL_TOKEN}` if set)
   - Capture the live URL from output (e.g. `https://zen-nail-bar.vercel.app`)
   - Wait 10 seconds (Vercel rate-limits rapid CLI deploys)
4. Update `sites/build-log.md` with Vercel URL for each deployed site
5. Print final summary table:

| Business | Old Site | Qualify | Vercel URL |
|----------|----------|---------|------------|
| Zen Nail Bar | zennailbar.com | YES | https://zen-nail-bar.vercel.app |

**Cost:** Free. Vercel Hobby plan. Each site is a single HTML file (~10–15 KB). No build process, no server.

---

## File Structure

```
workspace/
├── .env (APIFY_TOKEN, VERCEL_TOKEN)
├── scrape_results.json (leads)
├── qualify_results.json (YES/NO per lead)
├── screenshots/
│   └── {slug}.png (full-page screenshots)
└── sites/
    ├── build-log.md (tracks design combos + Vercel URLs)
    └── {business-slug}/
        └── index.html (single-file site)
```

---

## Good Niches to Target

Businesses that care about design and have budget to pay for it:

- Nail salons
- Med spas & Botox clinics
- Hair salons & barbershops
- Massage & wellness studios
- Wedding venues & planners
- Boutique hotels / B&Bs

**Avoid:** National chains, franchises, restaurants (razor-thin margins), lawyers (already have agencies).

---

## Dependencies

Install once:

```bash
# Node.js (required)
node --version  # must be 18+

# Playwright (for screenshots)
npm install playwright
npx playwright install chromium
npx playwright install-deps chromium  # Linux only

# Vercel CLI (for deploys)
npm install -g vercel
vercel login  # local only
```

**API keys:** Copy `.env.example` to `.env` and add:

- `APIFY_TOKEN` (required) — get at apify.com → Settings → Integrations
- `VERCEL_TOKEN` (remote/SSH only) — get at vercel.com/account/tokens

---

## Timing

- Scrape 20 places: 2–5 minutes
- Screenshot + qualify 10 sites: ~3 minutes
- Redesign 5 sites: ~15 minutes
- Deploy 5 sites: ~2 minutes
- **Total: ~25 minutes for 5 live redesigns**

---

## Troubleshooting

**Screenshots fail or show blank pages:**

- Run `npx playwright install-deps chromium` to install system dependencies (Linux)
- Some sites load content dynamically as you scroll — the screenshot script handles this with multiple scroll passes, but very slow sites may still appear incomplete

**Scrape returns 0 usable leads:**

- The script filters for businesses with both a website AND a discoverable email — this is strict
- Try increasing `--max` (e.g. `--max 50`) to cast a wider net
- Try a broader location (metro area instead of suburb)
- You can re-download results from a previous Apify run without paying again

**Deploy fails with "no credentials":**

- Run `vercel login` (local) or add `VERCEL_TOKEN` to your `.env` (remote/SSH)

**Node.js errors about imports or parseArgs:**

- You need Node.js 18+. Check with `node --version`

---

## Template Reference

The website generation prompt template is stored in `references/prompts/website_prompt_v1.md`. Read it when generating sites for the full structure and examples.
