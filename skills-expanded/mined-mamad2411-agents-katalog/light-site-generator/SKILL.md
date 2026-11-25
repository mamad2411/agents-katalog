---
name: light-site-generator
description: >-
  Build and deploy clean, professional single-page sites for home-service
  leads (plumber, HVAC, electrician). Uses a template-variable system to
  populate business info from lead CSV/DB. Generates images via Higgsfield
  Nano Banana Pro (unlimited on Ultra plan).
version: 1.1.0
metadata:
  hermes:
    tags: [light-site, generator, template, lead, deploy, higgsfield]
    triggers: [light site, build site, generate site, template site, lead site, business site, deploy site, professional site]
    related_skills: [scroll-world-pipeline, site-factory]
---

# Light Site Generator

Builds clean, professional single-page business sites for home-service leads.
Outputs a 5-section site (Home, Services, About, Gallery, Contact) with
business-specific info swapped in via template variables.

## Template System

**Canonical template:** `assets/templates/light-site/index.html`
**Generator script:** `scripts/generate_site.py`

The template uses HTML comment variables:

| Variable | Source | Example |
|----------|--------|---------|
| `<!-- BUSINESS_NAME -->` | Lead data | "Linear Plumbing & Drain Cleaning" |
| `<!-- NICHE -->` | Generated | "Plumber" |
| `<!-- TAGLINE -->` | Generated | "Trusted Plumbing Service in Albany, NY" |
| `<!-- DESCRIPTION -->` | Generated | "Family-owned for over 10 years..." |
| `<!-- PHONE -->` | Lead data | "(518) 320-6158" |
| `<!-- ADDRESS -->` | Lead data | "372 Delaware Ave, Albany, NY 12209" |
| `<!-- SERVICES_INTRO -->` | Generated | Section intro text |
| `<!-- SERVICES_INJECTED -->` | Generated | 6 service cards as HTML with SVG icons |
| `<!-- ABOUT_HEADING -->` | Generated | "Serving Albany for Over 10 Years" |
| `<!-- ABOUT_P1 -->` | Generated | About paragraph 1 |
| `<!-- ABOUT_P2 -->` | Generated | About paragraph 2 |
| `<!-- CONTACT_INTRO -->` | Generated | Contact section intro |
| `<!-- HOURS -->` | Lead data | "Mon-Fri: 7am-7pm..." |

### Generation command

```bash
python3 scripts/generate_site.py \
  --name "Business Name" \
  --phone "(518) 555-1234" \
  --address "123 Main St, City, NY" \
  --city "Albany" \
  --region "Capital Region" \
  --niche plumber
```

Output: `astro-sites/generated/_gh_pages_deploy/{niche}/{slug}/index.html`

## Template Features

### Dark/Light Theme Toggle
- Built into template via `[data-theme="dark"]` CSS custom properties
- Toggle button in nav (last element, right of "Call Now" CTA)
- Persists choice in `localStorage` — survives page reloads
- All colors (backgrounds, borders, text, cards) defined as CSS vars on `:root` and `[data-theme="dark"]`
- Theme toggle icon: ☯ (U+25C1) — clean, no words, no emoji

### SVG Icon System
- Service card icons are inline `<svg>` elements (18×18px, stroke-based) with path data from a Python dict called `SVG_ICONS` in `scripts/generate_site.py`
- 6 distinct SVG paths (hand-picked matching Heroicons-style paths):
  1. Clock/timer — circle with vertical line (emergency response)
  2. Grid of 4 squares — general work/service variety
  3. Chat bubble — communication (water heater consultation)
  4. Speech bubble with lightning — solutions (pipe repair)
  5. Lightning bolt — fast/efficient (fixture install)
  6. Exclamation in circle — caution/critical (sewer & drain)
- SVG icons inherit `currentColor`, styled via CSS class `.service-card .icon`
- Icon container: 40×40px circle with `var(--bg-alt)` background
- **NO emoji** in service cards — SVG icons or nothing

### Full-Bleed Hero
- Hero image spans full viewport width as background
- **Subtle 10% overlay** via CSS `::after` pseudo-element (`background: rgba(0,0,0,0.1)`) — just enough to keep white text readable without obscuring the photo
- Text readability via `text-shadow: 0 2px 12px rgba(0,0,0,0.4)` on h1
- Fallback to `--primary` color while image loads
- Dark mode: hero image drops to 0.8 opacity for comfortable reading
- Positioned at full 80vh minimum height

## Design Rules (from user preferences)

ALL of these are HARD RULES enforced by `reference/the operator-rules.md` in the `service-site-generation` umbrella:

1. **NO emoji** in site content — professional, clean, ordinary
2. **NO badges/pills** — no rating badges, trust badges, "Niche — City" pills
3. **NO objection busters** — "Worried about cost? Free estimate!" strips
4. **NO backend upsells** — "Don't pay until you get a call", "First month free"
5. **NO em dashes (—)** in rendered output — use commas or periods
6. **NO star ratings (★)** — use review count instead
7. **NO middle dot (·)** separators — use pipes `|` or commas
8. Looks like a **real, legitimate local business website** — not AI-generated

## Image Pipeline

Generate images via Higgsfield Nano Banana Pro 2K (unlimited on Ultra plan).

### Scene Types
1. **Hero** (hero.jpg) — Photorealistic: service van/plumber, residential street, warm light
2. **Service** (service.jpg) — Isometric clay close-up of hands-on work
3. **Result** (result.jpg) — BEFORE/AFTER split or completed work
4. **Lifestyle** (lifestyle.jpg) — Isometric clay: home, safety, resolution

### Workflow
1. Generate 5 variations per scene (total 20 images)
2. Run full batch via `assets/mass-gen/run_all.sh` or individual `hf.exe generate create` commands
3. Download to `assets/mass-gen-variations/{job_id}.png`
4. Pick best variation per scene and copy to `assets/plumber-light-template/assets/`
5. Mass-gen is serial (one image at a time, nano_banana_pro queue)
6. Zero credit cost on Ultra plan for 2K images

### Prompt Patterns
- Hero: "Photorealistic photograph of a professional [vehicle] with [business] lettering parked on a quiet residential street in [city]. Golden hour. A [worker] in uniform beside it. Professional, local business feel."
- Service: "Isometric clay diorama close-up of [trade] work. Tools laid out on a clean towel. Warm [material] tones."
- Result: "Isometric clay diorama split view. LEFT: before [damaged/old]. RIGHT: after [new/repaired]. Dramatic transformation."
- Lifestyle: "Isometric clay diorama looking through a warm-lit window at a cozy [room]. Evening. The feeling of safety."

## Lead Sources
- Ranked call list: `docs/plumber-call-list.md`
- Nationwide CSV: `data/leads/nationwide/`
- Lead DB: `data/leads/leads.db`

## Hero Overlay Preferences
See `references/hero-overlay-guide.md` for the exact CSS technique (10% `::after` overlay) and the iterative refinement process that led to it.

## Deployment Path
- Built sites go to: `astro-sites/generated/_gh_pages_deploy/<niche>/<slug>/`
- Live at: `https://your-username.github.io/project-sites/<niche>/<slug>/`
- Repo: `pmb2/project-sites` (gh-pages)
- Source repo: `website-landlord` on `feature/lead-capture-workflow`

## Generator Pipeline Steps
1. Read lead CSV row (business_name, niche, location, phone, address, rating)
2. Map niche to service generation rules (plumber → 6 plumbing services)
3. Generate 6 service cards as HTML with SVG icons
4. Generate about section copy (location + years + niche)
5. Replace all 12 template variables
6. Copy 4 images from image bank or generate new ones
7. Write to deploy directory
8. Git commit + push to gh-pages

## Niche Service Rules

See `references/service-generation-rules.md` for full per-niche service definitions.

### Plumber
1. Emergency Repair — 24/7 for burst pipes, sewage backups
2. Drain Cleaning — Clogged drains, slow sinks
3. Water Heater — Installation, repair, replacement
4. Pipe Repair — Leaks, frozen pipes, repiping
5. Fixture Installation — Toilets, faucets, disposals
6. Sewer & Drain — Sewer scope, main line cleaning

### HVAC
1. AC Repair — Central air, ductless mini-splits
2. Furnace Service — Gas, oil, electric
3. Heating Repair — Boilers, radiators
4. Thermostat — Smart thermostats, zoning
5. Ductwork — Cleaning, sealing, installation
6. Indoor Air Quality — Humidifiers, purifiers

### Electrician
1. Electrical Repair — Wiring, outlets, switches
2. Lighting — Installation, fixtures, outdoor
3. Panel Upgrade — 200 amp service, breaker panels
4. Safety Inspection — Home electrical audit
5. Generator — Standby generator installation
6. Smart Home — Smart switches, automation

## Batch Generation from CSV (mass deploy — proven 787 sites, 2026-08-04)

The CLI (`--niche`) restricts niches to `plumber|hvac|electrician`. For a whole leads
CSV (20+ niches), import the module **in-process** and call `gen_site()` directly,
monkeypatching the service bank so EVERY niche gets a full 6-card grid. Full recipe +
24-niche service bank: `references/batch-service-bank.md`.

```python
import sys; sys.path.insert(0, "<repo>/scripts")
import generate_site as gs
gs.SERVICES.update(EXTRA_SERVICES)      # 24 niches, see reference file
for row in csv_rows:
    html = gs.gen_site(name, phone, address, city, region, niche_kebab)
    # HONESTY FIX (the operator rule — no invented claims):
    html = html.replace("Family-owned and operated for over 10 years.",
                        "Family-owned and operated.")
    out = Path(gs.OUTPUT_DIR) / niche_kebab / slug / "index.html"
```

Key facts that cost time when missed:
- `gs.OUTPUT_DIR` = `<repo>/astro-sites/generated/_gh_pages_deploy` — that directory IS
  the `pmb2/project-sites` git repo (branch `main`). Generate into it, then
  `git add -A && git commit && git pull --rebase origin main && git push`. The remote
  moves frequently — **always pull --rebase before push** (non-fast-forward otherwise).
- **Niche dir names must be kebab-case** (`hvac contractor` → `hvac`, `cleaning service`
  → `cleaning-service`). July-era dirs used spaces — don't mix; URL =
  `https://your-username.github.io/project-sites/{niche}/{slug}/`.
- Slug: `re.sub(r'[^a-z0-9-]+', '-', name.lower()).strip('-')[:60]` (keeps `-`, so
  "LLC - X" → triple dashes — functional but ugly; acceptable for batch).
- Append a `deployed_url` column to the source CSVs after generation — the deliverable
  the operator wants is every lead row fulfilled WITH its live site URL.
- Regenerate `astro-sites/generated/_all_sites_deployed.json` from the deploy dir
  (829 entries after the 787 batch).

### QA checklist (run before and after push — all proven failures)

1. **Zero leftover template vars** (`<!-- BUSINESS_NAME -->` etc.) across generated files.
2. **Zero emoji / star / middle-dot chars** (`★ · • 🌟`) — the operator's hard rules.
3. **No invented tenure** — "over 10 years" stripped (honesty fix above).
4. **Live verification**: curl sample URLs → HTTP 200 AND business name in HTML (a bare
   200 can be the Pages 404 page). **GitHub Pages publish lag**: brand-new sites 404 for
   1–3 min after push — wait and re-verify; a previously-deployed site 200s immediately
   and misleads you into thinking the push landed.
5. Build test URLs FROM THE DISK (find the dir), never from guessing the slug —
   `KARNER Mechanical, Inc.` → `karner-mechanical-inc`, not `karn-er-...`.
6. Old space-named dirs (`auto repair shop/...`) break urllib verification with
   "URL can't contain control characters" — that's the OLD format, not your new files.

## Higgsfield Notes
- Current plan: Ultra ($99-129/mo)
- **Nano Banana Pro 2K: UNLIMITED** (365-day unlimited image model access)
- Nano Banana Pro 4K: 4cr per image
- Seedance 2.0 1080p: 45cr per 5s clip
- Balance: 2,193 credits remaining (as of Jul 24)
- Account: <your-email>@gmail.com
- Workspace: 97cd87e1-56d6-4031-be0e-e5364f130c11
- CLI: `~/bin/hf.exe`
- CLI config dir: `~/.higgsfield/` (OAuth token managed via `hf auth login`)
- Token: `hf auth token` to print current access token

## Video Implementation Notes
Key takeaways from watched videos (see `docs/video-implementation-notes.md`):
1. Be human, not corporate — real people, real story
2. Don't assume customers know anything — spell it out
3. Objection busters belong in the **CALL**, not on the site
4. Build microsites, not monuments — 30 sites beats 1 perfect one
5. Speed over perfection — deploy first, optimize later
