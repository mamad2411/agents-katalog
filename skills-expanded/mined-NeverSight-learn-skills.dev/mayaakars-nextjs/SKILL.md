---
name: mayaakars-nextjs
description: >
  Build, edit, or extend the Mayaakars interior design studio website in Next.js (App Router).
  Use this skill whenever working on any page, component, animation, or config for the Mayaakars
  project — including converting HTML prototypes to Next.js components, wiring up brand tokens,
  adding new pages, updating content, or integrating APIs/ERP. Trigger on any mention of
  "Mayaakars", "the website", "the Next.js project", "the studio site", or any named page/section
  (hero, gallery, projects, about, team, navbar, loading screen, testimonials, etc).
---
# Mayaakars — Next.js Website

Full-stack luxury interior design studio website. Architecture & Interiors brand.
Built with **Next.js 14 App Router**, **Tailwind CSS**, **GSAP**, **Lenis smooth scroll**.

---

## Brand Identity (ALWAYS follow these)

### Colors

```css
--bg:         #050505      /* near-black — primary background */
--bg-light:   #E3E4E0      /* warm off-white — light sections */
--gold:       #C49A3A      /* primary accent */
--gold-light: #C8A95C      /* lighter gold variant */
--text:       #E3E4E0      /* primary text on dark */
--text-dark:  #0A0A0A      /* text on light backgrounds */
--muted:      rgba(227,228,224,0.45)   /* secondary text */
--border:     rgba(196,154,58,0.15)    /* subtle gold borders */
```

### Gradients (from brandbook)

- **Light Gold Flow**: champagne → classic gold (hero/header sections)
- **Rich Gold Flow**: classic → rich gold (CTAs, accent elements)
- **Deep Gold Flow**: rich → antique gold (warm/vintage sections)
- **Soft Neutral**: soft white → pearl grey (card backgrounds)
- **Sophisticated Fade**: pearl grey → charcoal (transition sections)
- **Premium Dark**: charcoal → deep black (footer, premium content)

### Typography

```
Primary:   	 — headings, display, hero text
           Use italic variant for gold emphasis words
Secondary: Geist — body copy, UI, nav, labels
Tertiary:  M PLUS Rounded 1C — tags, badges, supporting text
```

### Logo

- 3D gold knot mark (triangular, three interlocking forms)
- Wordmark: "MAYAAKARS" in Cormorant Garamond, wide tracking
- On dark bg: white wordmark + gold knot
- On light bg: dark wordmark + gold knot
- Never recolor the knot mark; never stretch or rotate wordmark

---

## Project Structure

```
mayaakars/
├── app/
│   ├── layout.tsx              # Root layout — fonts, loading screen, navbar
│   ├── page.tsx                # Home page
│   ├── about/page.tsx
│   ├── projects/
│   │   ├── page.tsx            # All projects (3D carousel, category filter)
│   │   └── [slug]/page.tsx     # Individual project
│   ├── gallery/
│   │   ├── page.tsx            # Drag canvas gallery
│   │   └── [slug]/page.tsx     # Parallax photo detail
│   ├── services/
│   │   ├── page.tsx            # 5-strip accordion
│   │   └── [slug]/page.tsx     # 3D slider service detail
│   ├── blog/
│   │   ├── page.tsx                # All posts — 3-col scroll, image expand
│   │   └── [slug]/page.tsx         # Individual post (MDX)
│   ├── contact/page.tsx
│   ├── careers/page.tsx
│   ├── privacy/page.tsx
│   └── not-found.tsx           # 404 torch effect
├── components/
│   ├── layout/
│   │   ├── Navbar.tsx          # Fixed navbar (logo center, hamburger right)
│   │   ├── Menu.tsx            # Full-screen overlay menu (split panel)
│   │   └── Footer.tsx          # MAYAAKARS large text + contact + form
│   ├── loading/
│   │   └── LoadingScreen.tsx   # Logo spin → text reveal → glide to nav
│   ├── home/
│   │   ├── Hero.tsx            # Door SVG scroll animation
│   │   ├── Services.tsx        # 5-strip accordion section
│   │   ├── Projects.tsx        # 3D carousel preview
│   │   ├── Stats.tsx           # Animated numbers
│   │   ├── Testimonials.tsx    # Marquee + cards
│   │   └── CTA.tsx             # Bottom contact CTA
│   ├── about/
│   │   ├── AboutHero.tsx
│   │   ├── AboutContent.tsx
│   │   └── Team.tsx            # GSAP spotlight scroll
│   ├── gallery/
│   │   ├── GalleryCanvas.tsx   # Infinite drag 3D grid
│   │   └── GalleryDetail.tsx   # Parallax scroll sections
│   ├── projects/
│   │   ├── ProjectCarousel.tsx
│   │   └── ProjectFilter.tsx   # Category tabs
│   └── ui/
│       ├── GrainOverlay.tsx    # Fixed noise texture
│       ├── ScrollCue.tsx       # Animated scroll indicator
│       ├── RevealBlock.tsx     # IntersectionObserver fade-up wrapper
│       ├── CustomCursor.tsx    # Dot + ring cursor, mix-blend-mode diff
│       └── textures/
│           ├── DotField.tsx    # Animated dot grid (texture_1)
│           ├── MeshGrid.tsx    # Mouse-interactive mesh (texture_2)
│           └── LiquidGrid.tsx  # Step-reveal liquid lines (texture_4)
├── content/
│   └── blog/                   # .mdx files for blog posts
├── lib/
│   ├── gsap.ts                 # GSAP + ScrollTrigger registration
│   └── lenis.ts                # Lenis smooth scroll setup
├── styles/
│   └── globals.css             # CSS variables + base styles
└── public/
    └── images/                 # Real client photos (replace Unsplash)
```

---

## Key Pages & Their Source HTML

| Page / Component     | Source HTML file            | Key tech                        |
| -------------------- | --------------------------- | ------------------------------- |
| Loading screen       | `logo.html`               | GSAP timeline, letter stagger   |
| Home Hero            | `hero.html`               | SVG door, GSAP ScrollTrigger    |
| Home Services        | `service.html`            | CSS flex accordion, hover       |
| Home Projects        | `projects.html`           | 3D carousel, drag physics       |
| Home Footer/CTA      | `bottom.html`             | Scroll reveal, enquiry form     |
| Navbar + Menu        | `navbar.html`             | GSAP CustomEase "hop", split bg |
| About Hero + Content | `about.html`              | Parallax, grid layout           |
| About Team           | `team.html`               | GSAP + Lenis, spotlight scroll  |
| Gallery (main)       | `gallery.html`            | 3D drag canvas, fly-in          |
| Gallery (detail)     | `gallery_inside.html`     | GSAP ScrollTrigger parallax     |
| Service detail       | `service_per_page.html`   | 3D z-depth card slider          |
| 404                  | `error_3.html`            | Torch/flashlight cursor effect  |
| Custom cursor        | `mouse.html`              | Lerp ring, mix-blend-mode diff  |
| Texture: dot field   | `texture_1.html`          | Canvas, animated dots           |
| Texture: mesh grid   | `texture_2.html`          | Canvas, mouse-interactive       |
| Texture: liquid grid | `texture_4.html`          | Canvas, step-reveal lines       |
| Testimonials         | *(to build)*              | Marquee scroll + cards          |
| Blog (listing)       | `blog.html`               | 3-col scroll, image expand      |
| Blog (data)          | `blog_data.js`            | Content → MDX files            |
| Contact              | `bottom.html`             | Form + ERP integration stub     |
| Careers              | *(to build from scratch)* | Job listings + apply form       |
| Privacy              | *(to build from scratch)* | Static content page             |

---

## Shared Animations & Conventions

### GSAP Setup (always register in lib/gsap.ts)

```ts
import gsap from 'gsap'
import ScrollTrigger from 'gsap/ScrollTrigger'
import CustomEase from 'gsap/CustomEase'

gsap.registerPlugin(ScrollTrigger, CustomEase)
CustomEase.create('hop', '0.85, 0, 0.15, 1')  // Menu open/close
```

### Lenis Smooth Scroll

```ts
// lib/lenis.ts
import Lenis from 'lenis'
const lenis = new Lenis()
lenis.on('scroll', ScrollTrigger.update)
gsap.ticker.add((time) => lenis.raf(time * 1000))
```

### Grain Overlay (fixed, z-index 100, pointer-events none)

```css
opacity: 0.032;
background-image: url("data:image/svg+xml, ...fractalNoise...");
background-size: 180px 180px;
```

### Scroll Reveal Pattern

```tsx
// Use RevealBlock component or IntersectionObserver
// opacity: 0 → 1, translateY: 40px → 0
// threshold: 0.12, transition: 0.9s cubic-bezier(0.2,0.8,0.2,1)
```

### Section Overline Pattern

```tsx
<span className="overline">  {/* Cormorant Garamond, 0.7rem, 0.42em tracking, gold, uppercase */}
<h2>Headline with <em>italic gold</em> word</h2>
```

---

## Next.js Specific Notes

### Fonts (app/layout.tsx)

```tsx
import { Cormorant_Garamond, Geist } from 'next/font/google'
// M PLUS Rounded 1C also from google fonts
// Pass as CSS variables: --font-cormorant, --font-geist, --font-mplus
```

### GSAP in Next.js

- Always wrap GSAP animations in `useEffect` with cleanup (`return () => ctx.revert()`)
- Use `gsap.context()` scoped to a ref for proper cleanup
- For ScrollTrigger: call `ScrollTrigger.refresh()` after font load

### Client Components

- Any component using GSAP, mouse events, window, or refs → `'use client'`
- Static content (blog posts, about text) → Server Components

### Image Handling

- Use `next/image` with `fill` prop for all project/gallery images
- Placeholder: `placeholder="blur"` with `blurDataURL`
- Client images go in `/public/images/projects/[slug]/`

### ERP Integration (future)

- Keep all form submissions in `/app/api/` route handlers
- Use environment variables for ERP endpoints: `NEXT_PUBLIC_ERP_URL`
- Contact + Careers forms → POST to `/api/contact` and `/api/careers`
- Stub with `console.log` until ERP is confirmed

---

## Component Patterns

### Blog Listing (blog/page.tsx)

- Fixed vertical center line (`position: fixed, left: 50%, width: 1px`)
- Per-post: 3-column grid — `1fr | min(600px,85vw) | 1fr`
- Center image: starts at `width: 30%` → expands to `width: 100%` when row is "active"
- Active = row closest to `window.innerHeight / 2` (updated on scroll via rAF)
- Text columns: `opacity: 0, visibility: hidden` → reveal with per-character span animation (`animationDelay: i * 0.018s`) when active
- "Read More" overlay: `opacity: 0` → 1 on hover, gold text with expanding letter-spacing
- Bottom CTA: page bg transitions `#050505` → `#ffffff` via CSS variable swap when white section hits 40% visibility (IntersectionObserver)
- Mobile: single column stack, image first, text below

### Pages to Build from Scratch

**Contact** — brand-consistent form:

- Large "Let's Talk" or "Begin a Conversation" hero heading (Cormorant Garamond)
- Form fields: Name, Email, Phone, Project Type (dropdown), Message
- Subtle DotField or LiquidGrid texture background
- POST to `/api/contact` → ERP stub
- Studio address + phone + email (from bottom.html: +91 88844 96888, info@mayaakars.com, Near Gayatri Lakefront, Bridge 3, Outer Ring Road, Subramani Nagar, Guddadahalli, Hebbal Kempapura, Bengaluru, Karnataka 560024)

**Careers** — minimal job listings:

- Hero: "Join the Studio"
- Job cards: role, type (full-time/intern), location
- Apply CTA → form or mailto
- LiquidGrid texture background

**Privacy** — static legal content:

- Clean typography, Geist body text
- Sections: Data collected, How used, Contact for queries
- No animations needed — keep it simple
- Two-panel split background: left `#e8dfdf`, right `#e5e3d9`
- Panels rotate open from `rotate(±180deg)` → `rotate(0deg)` via GSAP "hop" ease
- Nav links slide up from `translateY(110%)` with stagger 0.05s
- Mobile: single panel, column layout, links left-aligned
- Nav color inverts when menu is open (dark text on light bg)

### Hero Door (Hero.tsx)

- 400vh spacer drives ScrollTrigger
- Doors SVG: left panel slides `x: -520px`, right `x: +520px`
- Door handles rotate ±90deg during open
- 3 text steps fade in/blur sequence after doors open
- At 98% scroll progress: hero fades out, page content takes over

### Loading Screen (LoadingScreen.tsx)

- Shows on first visit (sessionStorage flag to skip on navigation)
- Logo: opacity 0→1, rotates -360deg left, text reveals letter by letter
- Text disappears, logo rotates back 0deg, pause, glides to navbar position
- Loading screen fades out

### Gallery Canvas (GalleryCanvas.tsx)

- `useRef` on drag container, zoom wrapper
- Images: scattered grid with random size presets
- Intro: `gsap.fromTo` z: -5000 → 0 (fly-in from deep space)
- Physics loop: `requestAnimationFrame`, lerp factor 0.05 for butter

---

## Content Data Structure

### Projects

```ts
type Project = {
  slug: string
  title: string
  category: 'residential' | 'commercial' | 'hospitality'
  year: number
  location: string
  coverImage: string
  images: string[]
  description: string
  area?: string
  duration?: string
}
```

### Blog (MDX frontmatter)

```yaml
---
title: "Post title"
date: "2025-01-15"
category: "Design Insights"
coverImage: "/images/blog/post-slug.jpg"
excerpt: "Short description"
author: "Mayaakars Studio"
---
```

### Blog Data (from blog_data.js — migrate to MDX)

4 seed articles already written with full content:

- `spatial-harmony` — Design Theory — The Art of Spatial Harmony
- `natural-light` — Lighting — Natural Light as Material
- `texture-language` — Materials — Texture & Material Language
- `modern-indian-home` — Cultural Design — The Modern Indian Home

Each article has: `id, category, title, subtitle, summary, content (HTML), date`

### Team Members

```ts
type TeamMember = {
  name: string
  role: string
  image: string
  bio?: string
}
```

---

## Do's and Don'ts

### DO

- Always use CSS variables for colors, never hardcode hex in components
- Use Cormorant Garamond italic + gold color for emphasis words in headings
- Add grain overlay to every dark full-screen section
- Keep GSAP animations smooth: use `will-change: transform` on animated elements
- Mobile-first: test accordion, carousel, gallery on touch devices
- Use `next/image` for all images — never raw `<img>` tags
- Scope GSAP with `gsap.context(ref)` and clean up in `useEffect` return

### DON'T

- Don't use Inter, Roboto, or Arial — brand fonts only
- Don't hardcode Unsplash URLs in production — use `/public/images/`
- Don't use `localStorage` in components (SSR will break)
- Don't skip `'use client'` on components with GSAP/window/events
- Don't use `WidthType.PERCENTAGE` in any table (N/A here but general rule)
- Don't place GSAP outside `useEffect` — causes SSR errors
- Don't add `scroll-snap` to pages that use Lenis (conflicts)

---

## Custom Cursor (mouse.html → components/ui/CustomCursor.tsx)

Global cursor, active on all pages. Desktop only (`pointer: fine` media query).

- **Dot**: 6px white circle, instant tracking (`translate3d`, 0 lag)
- **Ring**: 36px circle with border, lerp trailing (`speed = 0.35`)
- **Blend mode**: `mix-blend-mode: difference` on both elements — inverts colors underneath
- **Hover state**: add `data-interactive` attribute to any interactive element
  - Dot disappears (`scale(0)`), ring expands to 110px solid white → text inverts to black
- **Click state**: ring shrinks to 25px
- Hide default cursor: `cursor: none !important` on all elements

```tsx
// Usage — add to any clickable/hoverable element:
<button data-interactive>Click me</button>
```

---

## Textures & Backgrounds

Three canvas-based ambient textures. Use as backgrounds for hero, loading, or transition sections.

### texture_1 — Dot Field (components/ui/textures/DotField.tsx)

- Grid of 0.7px dots, spacing 45px
- Slow sine/cosine drift (`time += 0.005`) — barely moves, premium feel
- Shimmer: opacity pulses per dot via `sin(time + (i+j)*0.3)`
- Color: white dots, every 7th = gold `rgba(212,175,55,α)`
- Canvas `filter: blur(0.4px)` for printed/soft look
- **Best for**: hero section background, loading screen

### texture_2 — Interactive Mesh Grid (components/ui/textures/MeshGrid.tsx)

- Canvas grid lines 0.4px white at 15% opacity
- Points wave (`sin/cos * 8px`) + bend toward mouse within 250px radius
- Gold nodes (`#D4AF37`, 1.5px) at every 4th intersection
- Mouse repulsion formula: `force = max(0, (250 - dist) / 250)`
- **Best for**: contact page, about hero, any section with mouse interaction

### texture_3 — Liquid Minimal Grid (components/ui/textures/LiquidGrid.tsx)

- Full-screen H+V lines, 150px spacing, 0.5px stroke
- Step-reveal on load (`reveal += 0.8`, `delay = (i+j)*10`)
- Liquid drift: `sin(time + y*0.01) * 15` per line
- Gold intersection dots, globalAlpha controlled
- **Best for**: careers page, privacy page, minimal content sections

### Texture Usage Pattern

```tsx
// Textures go behind content, absolute positioned, pointer-events: none
<section className="relative">
  <DotField className="absolute inset-0 z-0" />
  <div className="relative z-10">{/* content */}</div>
</section>
```

---

## Deployment Notes

- Target: Vercel
- Environment variables needed: `NEXT_PUBLIC_ERP_URL`, `NEXT_PUBLIC_SITE_URL`
- Blog: static MDX, no DB needed
- Images: Vercel image optimization via `next/image`
- Analytics: add later (Vercel Analytics or Plausible)
