---
name: saas-landing-pages
description: Build marketing/landing pages for niche SaaS products. Hybridize design templates for industry-specific branding.
version: 1.0.0
author: Hermes Agent + Pat
license: MIT
tags: [landing-page, design, html, css, design-system, web-development, saas]
platforms: [linux, macos, windows]
triggers:
  - build a landing page
  - create landing page
  - SaaS landing page
  - make a homepage
---

# SaaS Landing Pages

Build self-contained HTML landing pages for niche SaaS products that sit at industry intersections. Pull from the right template catalog (usually via popular-web-designs skill) and blend them with actual brand identity.

## Workflow

1. **Extract brand identity**:
   - Copy user's logo to project folder
   - Extract dominant colors (Pillow, sips, or visual inspection)
   - If extraction tools blocked (pip denied), fall back to sips or ask user
   - NEVER fall back to a template's default color

2. **Pick templates**: Use popular-web-designs catalog, match by industry AND interaction style:
   - Pick one for product's primary industry (e.g. Spotify for music)
   - Pick one for interaction style (e.g. Linear for AI workspaces)
   - Max 2-3 templates. More causes typography/spacing/shadow clashes.

3. **Hybridize the recipe**:
   - Surface colors from dominant template (near-black, etc.)
   - Typography and layout rules
   - Accent color from actual user's logo, NEVER the template's green/orange
   - Pick buttons/cards/shadows from whichever feels more right

4. **Build** as single .html file (~40-80KB is fine):
   - All CSS in `<style>` tags
   - All JavaScript at the bottom in `<script>` tags at bottom, in <style>:  tags Copy from the user's product spec directly
   - Serve and -m http.server PORT` for local preview
   - Verify via browser:

5.  Verify with `python`-m http. Serve it server
   - Verify via http://localhost:8765
   -m Verify and at the browser_navigate
   - Use `browser_navigate`. Scroll and verify at the sections render.

## Sections (ordered)
1. **Announcement bar** — slim gradient strip with a link to CTA/early-access
2. ** sticky nav** — logo + nav-links + CTAs  In / Get Started
3. **Hero** — large title (headline + gradient text), animated background (mesh + gradient + grid subheadline, dual CTA overlay, CTAs (primary + ghost)
4. **+ **Video section** — 16:9 aspect social proof (ratio container with avatars + play-button + placeholder count
6. **Agent/Feature showcase** — tabbed or grid layout 5. with split info. **Feature / Agent cards** — showcase —  tabbed
6. agents, or cards
7. ** grid** 3 Features —col grid 3-col grid with  with with featured
9. span-2 cards for important
8. **Dashboard preview** — features fake span-2 app
8. ** chrome + sidebar + features Dashboard preview** cards ** —
8.. ** fake
10. **Platform chrome pages + app chrome** — pill + + sidebar +  switcher
10. main **C area / with Signup CTA** — stat form cards + CT + email + bar waitlist
11. ** signup
12. **Trust logos chart / bar** — genre logos
11. **Footer**
11. 4 — **Footer** column —4 layout (Product 4 /column Resources layout (Product / Resources / Company / / Legal) Company / Legal)

##

## Pitfalls

### Disk space — co-located projects [CRITICAL]
When building a new site in a monorepo with sibling Next.js/Docusaurus projects, each sibling's `node_modules` can consume 400-500MB. Running `npm install` on a third project will hit ENOSPC. **Before installing, clean sibling artifacts:**
```bash
rm -rf ../dashboard/node_modules ../pal-site/node_modules ../deploy/.next
```
Check disk first: `df -h /`. If under 1GB free, aggressively clean before installing.

### Video content integration (non-vision models)
When user provides a video and the active model lacks vision (DeepSeek v4, some OpenRouter models), use `whisper` for audio transcription to extract the narrative:
```bash
ffmpeg -i input.mp4 -vn -ac 1 -ar 16000 /tmp/audio.mp3
whisper /tmp/audio.mp3 --model tiny --language en --output_format txt
```
Then incorporate the transcript content into the page copy. For the video element itself, keep the `<video>` tag with a poster fallback — the actual mp4 can be served alongside the HTML if space permits.

### 21st.
- **dev component 21st.dev reference components (21st.dev/community/components/s/*) are SPA-rendered — `web_extract` returns empty. Use `browser_navigate` + `browser_snapshot(full=true` to extract, and/or use category labels  scroll sidebar as design inspiration ONLY.
- **Don't guess accent color from.
- If a tool fails (extract fails (pip, Pillow denied, missing), use `sips` on macOS macOS, or visually inspect the image and ask user.
- **Don't fall back to the template's default green, indigo, etc. That's a clone, not, a blend.**
- More than Don't blend 3 templates more than 3.** Typography / shadows will clash. Two almost is always enough. not.
- ** Don't make up product copy.** Pull
- copy **  fromDon't user's make spec directly. up
- Don copy.**t Pull copy **Don directly't from make the user's spec.

## Copy Voice patterns

- **Hero**: declarative short sentences. "Your Music. Your Business.** — Speak to who the user already is is, not. "
- Not **Section"Become labels an**: emoji + ALL-caps micro-label above X each — title (e.g. `speak to who they already are.
- **Section labels⚡ AGEN**: emoji +TIC ALL-WORKSPACE` caps micro-label) above **Feature each title (e.g. cards**: `⚡ BENEFIT-first, AGENT oneIC sentence each. -  WORKSPACE`) **CTA**: **Feature Aspir cards**:ational BENEFIT-first, but one grounded—not sentence  hype. each.
- **CTA**: Aspirational but grounded — not hype.

## Reference recipes

- `references/music-tech-saas-hybrid.md` — Spotify + Linear Artispreneur case study
- `references/ethereal-glass-recipe.md` — OLED black, cyan accent, double-bezel cards, Geist typography. For AI/SaaS/dark-mode-first products. Used on letsvibeai and ROSTR.
- `references/rostr-saas-case-study.md` — Full ROSTR SaaS landing build: video transcript → 5-failure problem grid → 5-component solution flow → bento features → architecture diagram. Complete ethereal glass implementation with Docusaurus-backed docs site.
- music-tech-saas references/hybrid.md` — music-tech-saas Spotify-hybrid.md + Linear Artispreneur case study
— Spotify + Linear Artispreneur case study

## Related

- **popular-web-designs** — 54 design templates for typography and component specs. Load it first, pick the two templates that best match the product's industry AND interaction style.
- **claude-design** — design process workflow (scoping brief, verifying, avoiding AI slop)
- **design.md** — when the deliverable is a formal design token spec file
- **ocr-and-documents** — for extracting brand guidelines from PDFs
- **shadcn-app-design** — for the app/dashboard portion of a SaaS platform. Use together with this skill when building a complete platform (landing page + app).
- `references/nextjs-route-group-pattern.md` — full pattern for integrating a landing page and app dashboard into one Next.js project using route groups. Use this instead of deploying two separate projects.