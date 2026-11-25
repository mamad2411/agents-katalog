---
name: unbounce-to-astro
description: >
  Converts Unbounce and live landing pages into native Astro components with 1:1
  visual, structural, and functional fidelity. Use when migrating pages from Unbounce
  or external landing page builders to Astro, optimizing images (avif + webp fallback),
  mapping DOM flow and hero assets, auditing CTAs and internal form scrolling, and
  verifying technical SEO, analytics, and responsive behavior.
---

# Unbounce to Astro Landing Page Conversion & Parity Skill

This skill provides an end-to-end workflow, scripts, and verification checklist for converting legacy Unbounce or live landing pages into native Astro components with pixel-perfect visual fidelity, optimized media (`.avif` + `.webp`), proper CTA anchor behavior, and zero redirection regressions.

---

## 7-Step Conversion Playbook

### Step 1: Scrape & Capture Live DOM
Always fetch the raw HTML and CSS from the live page or Unbounce preview:
```javascript
// Scrape live HTML
const res = await fetch("https://www.calljacob.com/<page-slug>/", {
  headers: { "User-Agent": "Mozilla/5.0 ..." }
});
const html = await res.text();
fs.writeFileSync("scratch/live_page.html", html);
```

### Step 2: Extract & Convert All Media
Extract all images (regular `<img>`, `data-src-desktop-1x`, and CSS `background-image: url(...)`).
Convert each bitmap asset to `.avif` (quality 80) and create `.webp` fallback using `sharp`.
```javascript
await sharp(buffer).avif({ quality: 80 }).toFile(avifPath);
await sharp(buffer).webp({ quality: 80 }).toFile(webpPath);
```
Serve via `<PublicPicture>` or `<picture>` element with `<source srcset="...avif" type="image/avif">` and `<img src="...webp">`.

### Step 3: Map Section Coordinates & Visual Flow
Parse `#lp-pom-block-*` and elements ordered by `top` coordinates to detect:
1. **Header / Top Bar**: Wordmark, 24/7 call badge, quick evaluation button.
2. **Hero Section**: Background image, H1 headline, kicker, urgent subheadings, hero Jacob cutout, primary CTAs.
3. **Sponsorship & Social Proof**: Sports banners (Lakers/Rams/LAFC), badges, stats counter.
4. **Testimonials Grid / Slider**: 6-card client photo quotes, review ratings.
5. **Video & Feature Spotlights**: "The Real Deal" embedded YouTube video, 4 bullet benefit checklist.
6. **Billboard & Geographic Coverage**: Billboard artwork + SoCal counties checklist with checkmarks.
7. **About Law Firm / Authority Section**: 25+ years experience, home/office visits note, gold accents.
8. **Interactive Lead Form**: `#service-form` on-page anchor, Jacob cutout, SMS consent, qualification inputs.
9. **Location & Contact Card**: Office address, direct phone link.
10. **Footer**: Bar license #, copyright year, terms & privacy links.

### Step 4: Rule of No External Redirects
- All "Free Evaluation", "Free Case Review", "Contact Us", and "Get Started" CTAs **must scroll to `#service-form` on the same page** (never redirect off-page).
- All "Chat With Jacob" CTAs **must open the interactive chat drawer `#talk-to-jacob`** via class `open-calljacob-chat`.
- Phone links must use `tel:+18889522952` or project `PHONE.TEL`.

### Step 5: Data Structure & Template Pairing
- Determine whether the page uses `ModernInjuryPage` (dark hero with background crash photography, 3-step cards, why call, tactics) or `SocalInjuryPage` (bright yellow brand theme `#ffcd30`, sports sponsorship banner, 6-card testimonial grid, video section, billboard graphic).
- Populate the strongly typed page object in `apps/web/src/data/injuryPages.ts`.

### Step 6: Automated Verification & Type Check
Run Vite+ validation:
```bash
vp check --fix
vp run build
```
Ensure 0 lint errors, 0 type errors, 0 broken images, and SEO graph validations pass.

### Step 7: Staging & Production Deployment
Deploy to both environments:
```bash
node apps/web/scripts/deploy.mjs staging
node apps/web/scripts/deploy.mjs production --yes
```

---

## Visual Fidelity & Audit Checklist

- [ ] **Hero Background Match**: Verify background image matches live site (e.g. truck accident crash scene, bicycle road scene, yellow brand hero).
- [ ] **Jacob Cutout Match**: Correct Jacob pose (suit standing, arms crossed, or transparent headshot).
- [ ] **Typography & Colors**: Correct font sizes, letter spacing, bold weights, and brand colors (`#ffcd30` yellow, `#fd0d1b` red, `#000000` black).
- [ ] **Button Styling**: 4px black borders with `rounded-[15px]` or pill shape matching live design.
- [ ] **All Video Embeds Present**: Verify embedded YouTube videos (e.g., "The Real Deal") render responsively.
- [ ] **Checkmark Lists**: Check that all bullet points have correct checkmark or arrow icons.
- [ ] **Image Formats**: All images have `.avif` primary source with `.webp` fallback.
- [ ] **Form Submission**: Lead form sends data to `https://webhooks.calljacob.com/astro/` and displays clean in-place success status.
