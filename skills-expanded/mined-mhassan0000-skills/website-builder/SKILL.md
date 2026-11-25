---
name: website-builder
description: Build a cinematic, high-fidelity landing page from a brief description, then deploy it live on Netlify. Use when creating websites, building landing pages, making client sites, or deploying web pages.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Website Builder — Template Modification + Netlify Deploy

## Goal
Take a brief description of what the user wants and produce a stunning, production-ready landing page by **modifying an existing proven template** — not building from scratch. Then push it live on Netlify and return the URL.

## Inputs
- **Brand name**: The company/project name
- **Core thesis**: One sentence about what it is (or a URL to check)
- **Vibe/aesthetic**: Any direction (e.g. "dark techy", "clinical luxury", "brutalist")
- **Conversion goal**: What the CTA should be (default: book a call)

## Template Location
The base template lives at `website-template/` in the workspace root. It is a complete, working React + Vite + Tailwind v3 + GSAP site with:

### Structure
```
website-template/
├── src/
│   ├── App.jsx              # Root layout (imports all sections)
│   ├── index.css            # Tailwind imports, noise overlay, scrollbar
│   ├── main.jsx             # Entry point
│   └── components/
│       ├── Navbar.jsx        # Floating nav, scroll-reactive
│       ├── Hero.jsx          # Full-viewport hero, bg image, GSAP text reveal
│       ├── Features.jsx      # Light-bg section with 3 interactive micro-UIs
│       ├── DiagnosticShuffler.jsx  # Auto-cycling stacked cards widget
│       ├── TelemetryTypewriter.jsx # Terminal-style typewriter widget
│       ├── AdaptiveRegimen.jsx     # Calendar picker with animated cursor
│       ├── Philosophy.jsx    # Parallax bg, split-word text reveal
│       ├── Protocol.jsx      # Stacking scroll cards (GSAP ScrollTrigger pinning)
│       ├── Membership.jsx    # 3-tier pricing with hover effects
│       └── Footer.jsx        # Dark footer with columns
├── tailwind.config.js        # Color tokens, fonts, border-radius
├── postcss.config.js         # Standard postcss + autoprefixer
├── vite.config.js            # Vite + React plugin
├── package.json              # React 19, GSAP, Lucide, Tailwind v3
└── index.html
```

### Tech Stack (DO NOT CHANGE)
- React 19 + Vite 7
- Tailwind CSS **v3** (uses `tailwind.config.js` + `@tailwind` directives — NOT v4)
- GSAP 3 with ScrollTrigger
- Lucide React icons
- PostCSS + Autoprefixer

### Design System (in `tailwind.config.js`)
```
colors:
  moss: '#070707'      — deep black accent
  clay: '#0026FF'      — tech blue primary
  cream: '#EAEAEA'     — off-white text
  charcoal: '#070707'  — primary dark bg

fonts:
  sans: Plus Jakarta Sans, Outfit
  serif: Cormorant Garamond
  mono: system monospace
```

## Process

### Step 1: Copy Template
```bash
cp -R website-template/ site-name/
cd site-name
rm -rf node_modules
npm install
```

### Step 2: Customize for the Brand
Modify these files — DO NOT restructure or rewrite from scratch:

1. **`tailwind.config.js`** — Change color tokens (`moss`, `clay`, `cream`, `charcoal`) and fonts to match the brand aesthetic. The class names stay the same, only the hex values change.

2. **`index.css`** — Update the Google Fonts import URL to match new font choices.

3. **`index.html`** — Update `<title>`.

4. **Component copy** — Find-and-replace brand-specific text in each component:
   - `Navbar.jsx` — Brand name, nav links, CTA button text
   - `Hero.jsx` — Headline, subhead, tagline, background image URL
   - `Features.jsx` — Section heading, subheading
   - `DiagnosticShuffler.jsx` — Card titles, values, trends (make relevant to the brand)
   - `TelemetryTypewriter.jsx` — Typing messages array, status labels
   - `AdaptiveRegimen.jsx` — Widget labels, button text
   - `Philosophy.jsx` — The two contrasting statements, section labels, background image
   - `Protocol.jsx` — Step titles, descriptions, section heading
   - `Membership.jsx` — Tier names, prices, features, descriptions (or replace with a CTA section if not needed)
   - `Footer.jsx` — Brand name, tagline, link columns, copyright

5. **Unsplash images** — Replace background image URLs in Hero.jsx and Philosophy.jsx with images that match the brand. Use `https://images.unsplash.com/photo-ID?w=2000&q=80` format.

### Step 3: Build & Deploy
```bash
npm run build
npx netlify-cli deploy --prod --dir=dist --create-site site-name
```

If the site is already linked to Netlify:
```bash
npm run build
npx netlify-cli deploy --prod --dir=dist
```

Note: The interactive `sites:create` command hangs in non-TTY. Always use `--create-site` flag.

### Step 4: Return the Live URL

## What NOT to Do
- **DO NOT rewrite components from scratch.** The template works. Modify copy, colors, and images only.
- **DO NOT switch to Tailwind v4.** The template uses v3 with `tailwind.config.js`. Keep it.
- **DO NOT remove the interactive micro-UIs** (DiagnosticShuffler, TelemetryTypewriter, AdaptiveRegimen). They are the visual differentiator. Adapt their content to the brand.
- **DO NOT change the structural layout** (rounded section transitions, stacking scroll cards, parallax philosophy section). These are what make it look good.
- **DO NOT add new npm dependencies** unless absolutely necessary.

## Customization Cheat Sheet

### Changing the Vibe
The entire aesthetic shifts by changing 4 color tokens in `tailwind.config.js`:

| Vibe | `charcoal` (bg) | `clay` (accent) | `cream` (text) | `moss` (dark accent) |
|------|-----------------|-----------------|----------------|---------------------|
| Tech Blue (default) | `#070707` | `#0026FF` | `#EAEAEA` | `#070707` |
| Gold Luxury | `#070707` | `#C9A84C` | `#F5F0E8` | `#0A0A0A` |
| Neon Cyber | `#0A0A0A` | `#00FFD1` | `#E0E0E0` | `#0A0A0A` |
| Clinical White | `#FAFAFA` | `#2563EB` | `#1A1A1A` | `#F5F5F5` |
| Terracotta Organic | `#1A1410` | `#CC5833` | `#F2F0E9` | `#2E4036` |
| Emerald Content | `#090909` | `#10B981` | `#F0F0F0` | `#0A0A0A` |

### If Client Doesn't Need Pricing
Replace `Membership.jsx` content with a full-width CTA section (keep the component file, just change its JSX).

## Worked Example: 1SecondCopy (SEO content writing service)

This is the gold-standard reference for the depth of modifications needed. Every component's **text content** changes, but **zero structural/layout changes** are made.

### Colors (`tailwind.config.js`)
```js
moss: '#0A0A0A', clay: '#10B981', cream: '#F0F0F0', charcoal: '#090909'
```

### Component-by-component changes
| Component | What changed | What stayed the same |
|-----------|-------------|---------------------|
| `Navbar.jsx` | Brand → "1SECONDCOPY_", links → Process/Platform/Pricing, CTA → "Get Started" | Floating nav, scroll blur, mobile hamburger |
| `Hero.jsx` | Headline → "Words that Rank.", tagline → "Content Writing, With a Twist", subhead about top 1% writers, Unsplash bg → writing-themed | GSAP text reveal, layout, gradient overlays |
| `Features.jsx` | Heading → "Your Content Command Center", subhead about real-time dashboards | 3-column micro-UI grid, section structure |
| `DiagnosticShuffler.jsx` | Cards → "Content Velocity: 48 articles", "Avg. SERP Position: #4.2", "Turnaround Time: 2.1 days", label → "Content Analytics" | Auto-cycling animation, card structure |
| `TelemetryTypewriter.jsx` | Messages → content pipeline steps ("Researching target keywords...", "Matching writer to brief..."), labels → "Live Queue", stats → "In Queue: 3 briefs" / "Avg. Delivery: 2.1 days" | Typewriter effect, terminal styling |
| `AdaptiveRegimen.jsx` | Label → "Content Scheduler", heading → "Select Publish Day", button → "Submit", GSAP color → `#10B981` | Calendar grid, animated cursor, date chips |
| `Philosophy.jsx` | Old Way → "Hire freelancers. Manage revisions. Pray it ranks." vs New Way → "Submit a brief. Get SEO content that converts.", Unsplash bg swapped | Parallax scroll, split-word reveal, layout |
| `Protocol.jsx` | Steps → "Brief & Research" / "Expert Writing" / "SEO & Delivery", heading → "The Process.", description about their workflow | Stacking scroll cards, GSAP pinning, SVG graphics |
| `Membership.jsx` | Tiers → Starter $0.09/word, Bulk $0.08/word, Enterprise Custom, all features rewritten for content service | 3-column grid, hover effects, popular badge |
| `Footer.jsx` | Brand → "1SECONDCOPY_", tagline → "SEO content on-demand", columns → Services/Company, status → "Writers Online" | Layout, ping dot animation, copyright |

### Key takeaway
~200 lines of text changes across 10 files. Zero layout, animation, or structural changes. The site looks completely different because colors + copy do all the heavy lifting.

## Environment
Requires:
- Node.js 18+
- `npx netlify-cli` (auto-installs)
- Netlify account authenticated via `netlify login`

## First-Run Setup

Before executing, check if the workspace has a `.gitignore` file. If it doesn't, assume the user is new to this skill. In that case:

1. Ask the user if this is their first time running this skill
2. If yes, walk them through how it works and what they need to configure/set up (API keys, env vars, dependencies, etc.)
3. Let them know that Nick wishes them the best!
