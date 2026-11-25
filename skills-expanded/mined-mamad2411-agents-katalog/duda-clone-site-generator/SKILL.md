---
name: duda-clone-site-generator
version: 1.0.0
description: >
  Generate high-quality standalone HTML websites for local service
  businesses using the Duda-clone single-file generator
  (scripts/generate_duda_site.py + template.html). Covers the
  critical JS quoting bug, dark mode CSS trap, city-cycle SEO,
  image sourcing with Nano Banana Pro, hyperframes video integration,
  and GitHub Pages deployment with cache busting.
category: web-development
metadata:
  hermes:
    triggers:
      - duda clone
      - generate duda site
      - generate_duda_site.py
      - single file html site
      - html template generator
      - city cycle seo
      - surrounding cities rotation
      - dark mode toggle website
      - hero overlay image
      - service modal website
      - formspree contact
      - plumbing template
      - local service html site
      - quick turn around site
      - light plan site
      - 497 site
      - no build step site
      - hyperframes promo video
      - html to mp4 video
    related_skills:
      - local-service-websites
      - astro-site-rebuild
      - website-landlord-astro-builder
      - hyperframes
      - scroll-world
---

# Duda-Clone Single-File HTML Site Generator

## When to Use
Generate a standalone `index.html` (~43KB) for a local service business. No build step, no Node.js — instant deploy. Preferred for quick demos, the $497 Light plan ($197/mo recurring), or when the operator wants immediate visual feedback.

Use the Astro pipeline (`local-service-websites`) instead when you need multi-page sites, SEO schema JSON-LD, layout variants, or mass generation (200+ sites).

## Files
- `scripts/generate_duda_site.py` — Python generator with template variables
- `assets/templates/duda-clone/template.html` — Master HTML template
- `assets/hyperframes-project/` — HeyGen HyperFrames video composition project
- CloudFront CDN base: `https://d8j0ntlcm91z4.cloudfront.net/user_3Go22NtA815gb2uzpXzDXwmZyAy/`

## Pipeline
```
template.html (master HTML with <!-- PLACEHOLDER --> vars)
  + generator fills via build_site(name, phone, city, region, niche, ...)
  → index.html (self-contained, ~43KB, all CSS+JS embedded)
  → cp to gh-pages repo → git commit + push → live in 1-2 min
```

## CRITICAL BUG #1: JS Array Quoting in Template Variables

**This will silently kill ALL JavaScript on the entire page.**

The template has:
```javascript
var cities = [<!-- CITY_LIST -->];
```

If the generator outputs `Dallas","Plano","Carrollton` (missing opening quote on first item) or `"Dallas","Plano","Carrollton` (missing closing quote on last item before `]`), the entire `<script>` block hits a SyntaxError.

**Fix both ends of every array:**
```python
# Generator code — EACH entry gets opening AND closing quotes
DALLAS_LIST = '"Dallas","Plano","Frisco","Garland","Irving","Arlington","Richardson","Carrollton"'

# Fallback — both ends quoted
city_list = SURROUNDING_CITIES.get(primary_city, f'"{primary_city}","Serving All of {region}"')
```

**Verification after every change:**
```bash
grep "var cities" output.html
# PASS:  ["Dallas","Plano","Carrollton"];
# FAIL:  [Dallas","Plano","Carrollton];   (first missing opening quote)
# FAIL:  ["Dallas","Plano","Carrollton];  (last missing closing quote before ])
```

## CRITICAL BUG #2: Dark Mode CSS Specificity

```css
:root{--c3:#fff;--c4:#272727;--c5:#144b76}                     /* specificity 0,1,0 */
html[data-theme="dark"]{--c3:#111318;--c4:#e2e4ea;--c5:#1a3050}  /* specificity 0,1,1 — must be AFTER :root */
```

1. `:root` must come FIRST (sets defaults)
2. `html[data-theme="dark"]` must come SECOND (overrides in dark mode)
3. The `html` prefix gives it higher specificity than `:root` — required
4. The button uses `onclick="toggleTheme()"` with `id="themeToggle"`

## RULE: All JS Must Be try/catch Wrapped

Every independent feature gets its own try/catch. One JS error must never kill another feature:

```javascript
try{
  // City rotation
  var cities = [<!-- CITY_LIST -->];
  setInterval(rotateCity, 4000);
}catch(e){console.log('city:',e)}

try{
  // Dark/light theme toggle — localStorage guarded
  (function(){
    var t, b=document.getElementById('themeToggle');
    try{ t = localStorage.getItem('theme'); }catch(e){}
    if(t==='dark'){ document.documentElement.setAttribute('data-theme','dark'); if(b)b.innerHTML='&#9728;'; }
  })();
  function toggleTheme(){
    var h=document.documentElement, hD=h.getAttribute('data-theme')==='dark', b=document.getElementById('themeToggle');
    if(hD){ h.removeAttribute('data-theme'); try{localStorage.setItem('theme','light');}catch(e){} if(b)b.innerHTML='&#9681;'; }
    else{ h.setAttribute('data-theme','dark'); try{localStorage.setItem('theme','dark');}catch(e){} if(b)b.innerHTML='&#9728;'; }
  }
}catch(e){console.log('theme:',e)}
```

## Hero Image Architecture

The hero uses the photorealistic image as a FULL background, NOT a dim overlay on top of a gradient:

```css
.hero { color:#fff; padding:100px 0 80px; position:relative; overflow:hidden; }
.hero::before { /* background image at 100% opacity */ }
.hero::after  { /* 20% dark overlay for text contrast */ z-index:1; }
.hero .container { /* content above overlay */ z-index:2; }
```

NOT:
```css
/* OLD — do not use */
.hero { background: linear-gradient(135deg,#0a2a3f,...,#1a6ba0); }
.hero::before { opacity: 0.1; } /* Image barely visible on top of dark gradient */
```

## City Cycle for Geo-SEO

16 major metro areas covered (Dallas, NYC, LA, Chicago, Houston, Austin, SF, Seattle, Miami, Denver, Boston, Philly, Phoenix, Atlanta, San Antonio, Albany). Rotates every 4 seconds.

Unrecognized cities fall back to: `"CityName","Serving All of Region"`

## Map Loading

Google Maps iframe with `loading="eager"` (not `"lazy"`) for instant load. No API key needed:
```html
<iframe src="https://maps.google.com/maps?q=Dallas+TX&output=embed&z=12" allowfullscreen loading="easter">
```

## Gallery Images

6 photos per site. Generated via Nano Banana Pro 2K (Ultra plan, unlimited stills). Prompt format: "Photorealistic photograph of [scene description]. High detail, photorealistic." When Ultra credits are exhausted (monthly cap), reuse existing CloudFront-hosted images from the mass-gen queue.

## Page Animations

Three zero-dependency animation patterns for single-file HTML pages: IntersectionObserver scroll-reveal, particle canvas background, and timer tick-pop. See `references/animation-patterns.md` for full code and integration guide.

## Deployment (GitHub Pages Cache Bust)

GitHub Pages caches for 10 minutes (`Cache-Control: max-age=600`). When the operator needs to see changes immediately:
1. Deploy to a FRESH path: `mkdir -p demo/my-business-v2 && cp ... demo/my-business-v2/`
2. Or: `git commit --allow-empty -m "force rebuild" && git push`
3. Tell the operator to hard refresh: `Ctrl+Shift+R` or `Cmd+Shift+R`

## HyperFrames Video Promos

HeyGen HyperFrames generates HTML-to-MP4 promo videos. Installed at `assets/hyperframes-project/`.

Required composition structure (v0.7.x):
```html
<div id="stage" data-composition-id="my-id" data-start="0" data-width="1080" data-height="1920">
  <div id="slide1" class="clip" data-start="0" data-duration="5" data-track-index="0">Slide 1</div>
  <div id="slide2" class="clip" data-start="5" data-duration="5" data-track-index="1">Slide 2</div>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <script>
    var tl = gsap.timeline({ paused: true });
    window.__timelines = window.__timelines || {};
    window.__timelines['my-id'] = tl;
  </script>
</div>
```

Full 5-scene brand promo composition pattern: see `references/brand-promo-composition.md`.

Render: `cd assets/hyperframes-project && npx hyperframes render`

## Template Variables Reference

| Variable | Description | Generator Field |
|----------|-------------|-----------------|
| `<!-- BUSINESS_NAME -->` | Full business name | `--name` |
| `<!-- BUSINESS_SHORT -->` | Short name | Derived from name |
| `<!-- PHONE -->` | Phone number | `--phone` |
| `<!-- CITY -->` | Primary city | `--city` |
| `<!-- CITY_LIST -->` | JS array of surrounding cities | Auto from SURROUNDING_CITIES |
| `<!-- REGION -->` | Region/state | `--region` |
| `<!-- HOURS -->` | Business hours | `--hours` |
| `<!-- HERO_IMAGE -->` | Hero background URL | DEFAULT_IMAGES["hero"] |
| `<!-- GALLERY_1..6 -->` | Gallery image URLs | DEFAULT_IMAGES["g1"]..["g6"] |
| `<!-- MAP_QUERY -->` | URL-encoded location | Auto from city+region |
| `<!-- FORM_ID -->` | Formspree form ID | `xqkrgepq` (default) |
| `<!-- ADDRESS -->` | Street address | `--address` |
| `<!-- EMAIL -->` | Email | `--email` |

## Pitfalls

1. **JS array quoting** — The most expensive bug. Missing quotes kill ALL JavaScript silently. Verify after every generator change.
2. **Dark mode CSS order** — `:root` first, `html[data-theme="dark"]` second. No exceptions.
3. **localStorage in private browsing** — Always wrap in try/catch. Safari/iOS private mode throws SecurityError.
4. **GitHub Pages cache** — 10-minute cache. Fresh URL path or force push for immediate updates.
5. **Nano Banana Pro credits** — Monthly limit on Ultra plan (~3,010 cr). Have fallback images ready.
8. **HyperFrames attribute format** — v0.7.x uses `data-start` / `data-duration` / `data-track-index` / `class="clip"`. The old `data-hf-start` / `data-hf-duration` format is pre-v0.7 and won't work. See `references/brand-promo-composition.md` for the current contract.
9. **HyperFrames lint warnings** — `gsap_exit_missing_hard_kill` and `scene_layer_missing_visibility_kill` are informational; the renderer handles them and produces correct output. Can be silenced by wrapping scene content in inner non-clip divs.
7. **Learn More buttons** — the operator has explicitly removed these. Do not add them back.
