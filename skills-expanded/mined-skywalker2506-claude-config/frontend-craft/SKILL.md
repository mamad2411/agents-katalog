---
name: frontend-craft
description: "ANF frontend pipeline — high-end site/app build. Triggers: frontend craft, frontend pipeline, ANF, high-end site, web craft, premium frontend, build me a site, build a landing page, add a page, fix the design"
argument-hint: "[start|setup|assemble|normalize|fill|polish|add|fix]"
user-invocable: true
---

# /frontend-craft — High-End Frontend Pipeline

Builds $5-10K quality websites and applications. Works on **new or existing** projects. Handles anything from a single section to a full product site.

---

## Entry Point

```
/frontend-craft           → Interview + build (new or existing project)
/frontend-craft redesign  → Existing project: keep logic, replace all visual layer
/frontend-craft polish    → Existing project: improve current design (no structure change)
/frontend-craft help      → Show command reference
```

---

## redesign

**Existing project: keep all logic, data, and routing — replace the entire visual layer.**

Use this when the project works but looks bad, outdated, or inconsistent.

### Step 1: Audit the project silently

Read the codebase (Glob, Read, Grep):
- List all pages/routes
- Identify all components/sections
- Extract existing CSS — note what's hard-coded (colors, spacing, fonts)
- Find any existing design tokens or CSS variables
- Note what JS/logic to preserve (forms, API calls, auth, routing)

### Step 2: Interview (4 questions, one by one)

Q1:
```
Projeyi inceledim. Şu sayfalar/bileşenler var:
[listele]

Hepsini mi yeniden tasarlayalım, yoksa belirli sayfalar mı?
  a) Hepsini
  b) Sadece şunlar → hangilerini?
```

Q2:
```
Stil yönü?
  a) Minimal & clean
  b) Bold & güçlü
  c) Editorial & magazine
  d) Kurumsal & güven veren
  e) Dark mode ağırlıklı
  f) Oyuncu & enerjik
  g) Diğer → yaz
```

Q3:
```
Renkler?
  a) Mevcut renkleri koru
  b) Marka rengim var → hex yaz
  c) Sen seç (stilden çıkar)
```

Q4:
```
Animasyon / motion?
  a) Sade — sadece hover ve geçişler
  b) Orta — scroll animasyonları ekle
  c) Premium — hero video, parallax, frame sequence
  d) Yok — statik kal
```

### Step 3: Show redesign plan

```
Redesign planı:

📋 Scope: [X sayfa / Y bileşen]
🎨 Stil: [seçilen]
🔒 Korunacaklar: [JS logic, form handlers, API calls, routing]
🔄 Değişecekler: CSS tamamen, HTML yapısı (semantic düzeltmeler), görseller

Dosya planı:
  src/styles.css     → sıfırdan yazılır (design tokens + global)
  components/*.html  → semantic HTML ile yeniden yapılandırılır
  assets/images/     → gen-assets.sh ile otomatik üretilir
  [korunanlar]       → dokunulmaz

Başlayayım mı? (y / değiştir)
```

### Step 4: Execute (after "y")

For each page/component:
1. Read existing HTML — extract all text content and data attributes
2. Rewrite HTML with semantic structure (keep text, replace markup)
3. Write new CSS using design token system
4. Preserve all JS event handlers, form actions, API endpoints verbatim
5. Run `bash scripts/gen-assets.sh` for automatic image generation
6. Apply Normalize pass across all files
7. Apply Polish if motion ≥ "Orta"

**Never touch:**
- JavaScript business logic
- Form `action` and `method` attributes
- API endpoint URLs
- Authentication flows
- Database queries or ORM calls
- Environment variables

---

## polish

**Existing project: improve the current design without changing structure or logic.**

Use this when the project looks mostly okay but needs refinement — better spacing, animations, typography, color consistency, or performance.

### Step 1: Audit visually

Read CSS, HTML, JS silently. Build a diff list:

Check for:
- Hard-coded colors (not in variables) → flag each
- Inconsistent spacing (mixed px values) → flag
- Missing font-display, preconnect → flag
- Missing width/height on images → flag
- Missing prefers-reduced-motion → flag
- WCAG contrast failures → flag
- No ARIA landmarks → flag
- Hard-coded font sizes (not using scale) → flag
- No hover/focus states on interactive elements → flag

### Step 2: Show polish menu (one question)

```
Projeyi inceledim. Şu sorunları buldum:

[sorun listesi — etki ve efor ile]

Ne yapalım?
  a) Hepsini düzelt (önerilen)
  b) Seç → hangilerini? (numaraları yaz)
  c) Sadece animasyon / motion ekle
  d) Sadece renk & tipografi düzelt
  e) Sadece erişilebilirlik (WCAG) düzelt
  f) Sadece performans (LCP, CLS, font loading)
```

Wait for answer. Then execute selected items automatically.

### Step 3: Execute (no more questions)

**Always run in this order:**

1. **Token extraction** — if no CSS variables exist, extract all repeated values and create `--color-*`, `--space-*`, `--text-*` tokens
2. **Normalize pass** — replace hard-coded values with tokens
3. **WCAG fixes** — adjust colors to 4.5:1 minimum contrast
4. **Performance fixes** — add font-display, preconnect, fetchpriority, width/height
5. **Accessibility fixes** — add ARIA landmarks, alt text, focus states
6. **Motion additions** — add scroll animations, hover transitions, wrapped in prefers-reduced-motion
7. **Asset refresh** — if images are placeholders or missing, run gen-assets.sh

**Never touch:**
- HTML structure (unless adding ARIA)
- JavaScript logic
- Routing or server config
- Any working functionality

---

## help

When `/frontend-craft help` is called, print this exactly:

```
╔══════════════════════════════════════════════════╗
║          /frontend-craft — Quick Reference       ║
╠══════════════════════════════════════════════════╣
║  /frontend-craft          Start interview + build ║
║  /frontend-craft help     Show this reference     ║
╠══════════════════════════════════════════════════╣
║  PLATFORMS                                       ║
║  Web  → Vanilla / Next.js / Astro                ║
║  Mobile → Flutter / React Native / Expo          ║
╠══════════════════════════════════════════════════╣
║  PHASES (run manually if needed)                 ║
║  /frontend-craft setup    Scaffold + tokens       ║
║  /frontend-craft assemble Build sections          ║
║  /frontend-craft normalize Unify design system    ║
║  /frontend-craft fill     Real copy + assets      ║
║  /frontend-craft polish   Animations + deploy     ║
╠══════════════════════════════════════════════════╣
║  EXISTING PROJECT                                ║
║  /frontend-craft redesign Sıfırdan yeniden yaz   ║
║  /frontend-craft polish   Mevcut tasarımı geliştir║
╠══════════════════════════════════════════════════╣
║  SHORTCUTS                                       ║
║  /frontend-craft add      Add page/section/feature║
║  /frontend-craft fix      Fix/redesign something  ║
╠══════════════════════════════════════════════════╣
║  FILE LAYOUT (after setup)                       ║
║  index.html               Main entry             ║
║  src/styles.css           Design tokens + global  ║
║  src/main.js              JS interactions         ║
║  components/              Section HTML files      ║
║  assets/                  Images, video, research ║
║  craft-brief.md           Project brief           ║
╚══════════════════════════════════════════════════╝
```

---

## Phase 0 — Interview (ALWAYS FIRST)

Before touching any file, ask ALL questions in a single message. Never ask one at a time.

### Step 1: Detect context silently

Scan the current directory (Glob, Read):
- Existing project? (package.json, index.html, src/, app/, pubspec.yaml)
- Stack? (React, Next.js, vanilla, Astro, Flutter)
- Existing design system? (CSS variables, Tailwind config)
- Existing copy / brand info?

### Step 2: One question at a time — with lettered options

Ask questions **one by one**. Each question is a separate message. Wait for the answer, then ask the next automatically. Do NOT ask multiple questions in one message. Skip questions already answered by context.

**Question sequence:**

Q1:
```
Bu ne? (bir cümle — ürün, servis veya amaç)
```
→ Wait for answer. Then:

Q2:
```
Kime yönelik?
  a) B2C — bireysel kullanıcı
  b) B2B — şirketler
  c) Geliştirici / teknik kitle
  d) Genel / karma
  e) Diğer → yaz
```
→ Wait. Then:

Q3:
```
Ne lazım?
  a) Tam site (landing + birden fazla sayfa)
  b) Sadece landing page
  c) Belirli bir sayfa → hangisi?
  d) Mevcut siteye ekleme → ne?
  e) Küçük bir şeyi düzelt → ne?
```
→ Wait. Then:

Q4:
```
Stil?
  a) Minimal & clean
  b) Bold & güçlü
  c) Editorial & magazine
  d) Kurumsal & güven veren
  e) Dark mode ağırlıklı
  f) Oyuncu & enerjik
  g) Diğer → yaz
```
→ Wait. Then:

Q5:
```
Renkler?
  a) Marka rengim var → hex yaz
  b) Sen seç (stilden çıkar)
```
→ Wait. Then:

Q6:
```
Özellik lazım mı?
  a) Contact form
  b) Pricing tablosu
  c) Newsletter kaydı
  d) Blog / içerik alanı
  e) Auth UI (login/signup)
  f) Dashboard shell
  g) Yok, sadece statik
  (birden fazla seçebilirsin, örn: a c)
```
→ Wait. Then:

Q7:
```
Platform / Stack?
  a) Web — Vanilla HTML/CSS/JS
  b) Web — Next.js
  c) Web — Astro
  d) Mobile — Flutter
  e) Mobile — React Native / Expo
  f) Ne önerirsen
  g) Diğer → yaz
```
→ Wait for final answer.

**If d) Flutter or e) React Native selected:** skip web-specific questions and route to the relevant mobile platform section below.

### Step 3: Build brief

After answers, write `craft-brief.md` in project root. Then show a **file plan** before creating anything:

```
Anlıyorum. İşte yapacaklarım:

📁 Dosya yapısı:
├── index.html              → Ana sayfa (hero + features + CTA + footer)
├── src/
│   ├── styles.css          → Design tokens + global styles
│   └── main.js             → Scroll animasyonları, form handling
├── components/
│   ├── hero.html           → Hero section
│   ├── features.html       → Özellikler grid
│   └── footer.html         → Footer
├── assets/
│   ├── research.json       → Ürün araştırması (Fill fazında)
│   └── demo/               → Görseller buraya
└── craft-brief.md          → Proje brief'i

🎨 Stil: [seçilen stil]
🎯 Scope: [ne yapılacak]
⚡ Stack: [seçilen stack]

Başlayayım mı? (y / değiştir)
```

Show plan. Wait for ONE final confirmation ("y" or "değiştir").

**If "y":** Execute the entire pipeline to completion. No more questions. No pauses. No "shall I continue?" between phases. Run straight through to the end.

**If "değiştir":** User edits specific parts inline → update plan → re-confirm → then execute fully.

### Step 3: Build a brief

After the user answers, write `craft-brief.md` in the project root:

```markdown
# [Project Name] — Craft Brief
> Created: [date]

## What
[One sentence]

## Who
[Target audience]

## Scope
[Exact deliverables — pages, sections, features]

## Style
[Direction + colors]

## Stack
[Chosen tech]

## Must-haves
[Feature list]

## Existing project
[What was found, what to keep, what to replace]
```

Show the brief to the user. Ask: **"Good to go? (y / adjust)"**

If adjust: let them correct inline, update the brief, re-confirm.

If yes: proceed to execution.

---

## Phase 1 — Scope Router

Based on the brief, choose the execution path:

| Scope | Path |
|-------|------|
| Single section or fix | → [Targeted Mode](#targeted-mode) |
| Single page | → Setup + Assemble + Normalize + Fill |
| Full site | → Full ANF + Polish |
| Add to existing | → [Addon Mode](#addon-mode) |
| Feature (form, auth, etc.) | → [Feature Mode](#feature-mode) |

---

## Targeted Mode

For small requests ("fix the hero", "add a pricing section", "redesign the nav"):

1. Read the existing file(s)
2. Understand the current design system (extract variables if any)
3. Make the targeted change — nothing else
4. Apply Normalize rules to the changed section only
5. Fill with real copy if placeholder text is present

---

## Addon Mode

For adding to an existing project:

1. Read the project structure
2. Identify: routing system, component pattern, CSS approach
3. Create the new page/section following existing conventions
4. Do not change files that weren't asked about
5. Apply Fill phase only to new content

---

## Feature Mode

For functional additions (contact form, pricing, newsletter, auth UI, dashboard, etc.):

1. Build the UI component with real functionality
2. **Contact form:** HTML form + Netlify Forms (`netlify` attribute) or Formspree endpoint
3. **Pricing table:** tier comparison, CTA per tier, annual/monthly toggle
4. **Newsletter:** input + submit + success state (integrate Buttondown or Mailchimp embed)
5. **Auth UI:** login + signup forms, forgot password flow (UI only unless stack supports it)
6. **Dashboard shell:** sidebar nav, header, main content area, responsive
7. Wire up interactions in vanilla JS or the project's framework
8. Apply all accessibility rules (ARIA, keyboard nav, labels)

---

## Full ANF Pipeline

### Setup

**Only for new projects or when explicitly asked to scaffold.**

- Create folder structure: `src/`, `assets/`, `components/`, `public/`
- Install dependencies based on chosen stack
- Define CSS custom properties:

**Spacing (8px grid):**
```css
--space-xs: 4px;
--space-sm: 8px;
--space-md: 16px;
--space-lg: 24px;
--space-xl: 40px;
--space-2xl: 64px;
```

**Typography:**
```css
--text-sm: 0.875rem;    /* 14px */
--text-md: 1rem;        /* 16px */
--text-lg: 1.125rem;    /* 18px */
--text-xl: 1.25rem;     /* 20px */
--text-2xl: 1.5rem;     /* 24px */
--text-display: 2.5rem; /* 40px */
--leading-tight: 1.2;
--leading-normal: 1.5;
--leading-relaxed: 1.75;
--font-regular: 400;
--font-medium: 500;
--font-bold: 700;
```

**Colors (4-role system):**
```css
--color-primary: [from brief];
--color-surface: [from brief];
--color-muted: [from brief];
--color-accent: [from brief];
```

**Semantic tokens (dark mode ready):**
```css
:root {
  --color-bg: var(--color-surface);
  --color-text: oklch(15% 0 0);
  --color-text-muted: oklch(45% 0 0);
  --color-border: oklch(88% 0 0);
}
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: oklch(12% 0 0);
    --color-text: oklch(92% 0 0);
    --color-text-muted: oklch(65% 0 0);
    --color-border: oklch(25% 0 0);
  }
}
```

**Other tokens:**
```css
--radius-sm: 4px;
--radius-md: 8px;
--radius-lg: 16px;
--shadow-soft: 0 2px 8px rgba(0,0,0,.06);
--shadow-medium: 0 4px 24px rgba(0,0,0,.10);
--shadow-strong: 0 8px 48px rgba(0,0,0,.18);
--ease-default: cubic-bezier(.4,0,.2,1);
--duration-fast: 150ms;
--duration-normal: 250ms;
--duration-slow: 400ms;
```

**Font loading:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
```
```css
@font-face {
  font-display: swap;
  /* define fallback stack */
}
```

**taste-skill:** Reference https://github.com/Leonxlnx/taste-skill/tree/main for design principles. Pin to a specific commit SHA before use.

---

### Assemble (ANF: A)

- Read component prompts from `components/*.txt` if they exist
- Otherwise generate sections from the brief: hero, features, social proof, CTA, footer
- Every section is a semantic `<section id="...">` element

**ARIA Landmarks (required):**
```html
<header>...</header>
<nav aria-label="Main navigation">...</nav>
<main>
  <section aria-labelledby="hero-heading">...</section>
  <section aria-labelledby="features-heading">...</section>
</main>
<footer>...</footer>
```
Every section without a visible heading gets `role="region" aria-label="..."`.

**Image & Video (required for CLS):**
- Always set `width` and `height` on `<img>` and `<video>`
- Use `aspect-ratio` CSS
- Hero image preload:
```html
<link rel="preload" as="image" href="hero.webp" fetchpriority="high">
<img src="hero.webp" width="1440" height="800" fetchpriority="high" alt="...">
```

**21st.dev workflow (optional):**
1. Browse https://21st.dev
2. "Copy Prompt" → "Claude Code"
3. Save as `components/01.txt`, `02.txt`, etc.

---

### Normalize (ANF: N)

Replace all hard-coded values with CSS custom properties:
- Spacing → `--space-*`
- Typography → `--text-*`, `--leading-*`, `--font-*`
- Colors → `--color-*` (4-role system)
- Buttons → single border-radius, single hover pattern
- Shadows → `--shadow-soft/medium/strong`
- Motion → `--ease-default`, `--duration-*`
- Purge purple defaults (#6366f1, indigo-500) if present

**WCAG 2.1 AA (required):**
- Text on background: minimum 4.5:1 ratio
- Large text (18px+): minimum 3:1 ratio
- Check: https://webaim.org/resources/contrastchecker/
- Use `oklch()` for perceptually uniform color tweaks

---

### Fill (ANF: F)

1. Read `craft-brief.md` for product context
2. Research (WebSearch): value props, target audience pain points, competitor positioning
3. Write `assets/research.json`
4. Replace all placeholder copy:
   - Headlines: max 8 words
   - Sublines: max 20 words
   - CTAs: max 4 words
   - Banned words: "leverage", "seamless", "revolutionary", "transformative", "cutting-edge"
5. SEO: set `<title>`, `<meta description>`, `<h1>` hierarchy

**Alt text (required):**
- Informative: descriptive, max 125 chars (`alt="Dashboard showing revenue up 23%"`)
- Decorative: `alt=""` (empty, not missing)
- Logo: `alt="[Company name] logo"`
- AI-generated: describe subject + mood — never write "AI generated image"

**Asset generation — AUTOMATIC:**

After writing `assets/research.json`, run:
```bash
bash scripts/gen-assets.sh assets/research.json
```

This script runs automatically and:
1. Generates hero, features, social-proof, cta-bg images
2. Fetches or generates hero video
3. Compresses video to H.264 + WebM with ffmpeg

**Fallback chain (automatic, no manual steps):**
| Priority | Source | Requires | Quality |
|----------|--------|----------|---------|
| 1 | Together AI FLUX.1-schnell | `TOGETHER_API_KEY` + credits | AI generated |
| 2 | HuggingFace FLUX.1-schnell | `HF_TOKEN` | AI generated |
| 3 | Unsplash stock photo | Nothing | Stock photo |
| 4 | CSS gradient placeholder | Nothing | Fallback |

**Video fallback chain:**
| Priority | Source | Requires |
|----------|--------|----------|
| 1 | Pexels stock video | `PEXELS_API_KEY` (free to get) |
| 2 | Pixabay stock video | `PIXABAY_API_KEY` (free to get) |
| 3 | ffmpeg gradient video | ffmpeg only |

**To enable AI image generation:** add credits to Together AI account.
**To enable stock video:** get free API key at pexels.com/api and add `PEXELS_API_KEY` to `~/.claude/secrets/secrets.env`.

**Manual generation tools (if needed):**
| Tool | URL | Free | Best for |
|------|-----|------|----------|
| Playground AI | playgroundai.com | 500/day | Custom hero |
| Ideogram | ideogram.ai | ~25/day | Text-in-image, logos |
| Higgsfield | higgsfield.ai | 66 credits/day | AI video |

---

### Polish

**Motion safety (required — always wrap animations):**
```css
@media (prefers-reduced-motion: no-preference) {
  /* all animations here */
}
```
Or add globally:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

**Hero video:**
```html
<video autoplay loop muted playsinline style="object-fit:cover">
  <source src="hero.webm" type="video/webm">
  <source src="hero.mp4" type="video/mp4">
</video>
```

**Video compress:**
```bash
ffmpeg -i input.mp4 -vcodec libx264 -crf 28 -movflags +faststart output.mp4
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 35 -b:v 0 output.webm
```

**Scroll animation:** IntersectionObserver + requestAnimationFrame, or `animation-timeline: scroll()`

**Deploy workflow:**
```bash
# 1. Preview
npx netlify-cli deploy --dir=.
# 2. Review preview URL
# 3. Confirm prod deploy with user
npx netlify-cli deploy --prod --dir=.
```

**Verify:** Lighthouse audit, target 90+ on all metrics.

---

## Design Rules

**Anti-patterns (never do):**
- Hard-coded `indigo-500` or purple as default brand color
- Generic card grid for every section
- Inter on everything
- Symmetric, template-looking layouts
- Gradient blob + floating mockup hero

**Principles (always follow):**
- Asymmetric layouts with editorial spacing
- Strong typographic hierarchy (2 font families max)
- Intentional whitespace — let content breathe
- Each section feels uniquely composed
- Consistent rhythm, not monotonous repetition

---

## Execution Rules

- **Never ask mid-task.** All questions happen in Phase 0. After confirmation, execute to completion.
- **Existing projects:** Read first, adapt to what's there. Don't overwrite working code.
- **Small requests:** Don't run the full pipeline. Targeted Mode only.
- **Copy:** Never lorem ipsum in the final output. Research and write real copy.
- **Code:** All values via CSS custom properties — zero hard-coded colors, sizes, or spacing.

---

## Flutter Platform

Triggered when `pubspec.yaml` is detected or user selects Flutter in Q7.

### Platform detection

```
pubspec.yaml present → Flutter
lib/ + main.dart → Flutter confirmed
android/ + ios/ → Flutter confirmed
```

### Flutter Design Tokens

Instead of CSS variables, create `lib/core/theme/app_theme.dart`:

```dart
import 'package:flutter/material.dart';

class AppColors {
  // Primary palette (from brief)
  static const primary     = Color(0xFF[HEX]);
  static const surface     = Color(0xFF[HEX]);
  static const muted       = Color(0xFF[HEX]);
  static const accent      = Color(0xFF[HEX]);

  // Semantic
  static const background  = Color(0xFFF8F8F8);
  static const onBackground= Color(0xFF111111);
  static const onSurface   = Color(0xFF333333);
  static const border      = Color(0xFFE0E0E0);
}

class AppSpacing {
  static const xs  = 4.0;
  static const sm  = 8.0;
  static const md  = 16.0;
  static const lg  = 24.0;
  static const xl  = 40.0;
  static const x2l = 64.0;
}

class AppRadius {
  static const sm = Radius.circular(4);
  static const md = Radius.circular(8);
  static const lg = Radius.circular(16);
}

class AppTheme {
  static ThemeData light() => ThemeData(
    colorScheme: ColorScheme.fromSeed(
      seedColor: AppColors.primary,
      surface: AppColors.surface,
    ),
    textTheme: const TextTheme(
      displayLarge: TextStyle(fontSize: 40, fontWeight: FontWeight.bold, height: 1.2),
      headlineMedium: TextStyle(fontSize: 24, fontWeight: FontWeight.w600, height: 1.3),
      bodyLarge: TextStyle(fontSize: 18, height: 1.5),
      bodyMedium: TextStyle(fontSize: 16, height: 1.5),
      bodySmall: TextStyle(fontSize: 14, height: 1.5),
    ),
    useMaterial3: true,
  );

  static ThemeData dark() => ThemeData(
    colorScheme: ColorScheme.fromSeed(
      seedColor: AppColors.primary,
      brightness: Brightness.dark,
    ),
    useMaterial3: true,
  );
}
```

### Flutter Assemble

Each "section" is a `StatelessWidget` in `lib/features/[screen]/widgets/`:

```dart
class HeroSection extends StatelessWidget {
  const HeroSection({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(
        vertical: AppSpacing.x2l,
        horizontal: AppSpacing.lg,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Headline', style: Theme.of(context).textTheme.displayLarge),
          const SizedBox(height: AppSpacing.md),
          Text('Subline', style: Theme.of(context).textTheme.bodyLarge),
          const SizedBox(height: AppSpacing.lg),
          FilledButton(onPressed: () {}, child: const Text('CTA')),
        ],
      ),
    );
  }
}
```

**File structure for new Flutter project:**
```
lib/
  core/
    theme/
      app_theme.dart     → tokens + ThemeData
      app_colors.dart    → color constants
  features/
    home/
      screens/home_screen.dart
      widgets/
        hero_section.dart
        features_section.dart
        cta_section.dart
  main.dart
assets/
  images/                → gen-image.sh output
  research.json
craft-brief.md
```

### Flutter Normalize

Scan all `.dart` files for:
- Hard-coded `Color(0xFF...)` not in AppColors → move to AppColors
- Hard-coded `double` spacing not using AppSpacing → replace
- Hard-coded `TextStyle` not in TextTheme → replace
- `BorderRadius.circular(N)` not using AppRadius → replace

### Flutter Fill

Same copy rules as web. For assets:
- Run `bash scripts/gen-image.sh` for each section image
- Add images to `pubspec.yaml` assets section automatically
- Use `AssetImage` or `Image.asset` with `semanticsLabel` (= alt text equivalent)

### Flutter Polish

**Motion:**
```dart
// Implicit animation (preferred)
AnimatedOpacity(
  opacity: _visible ? 1.0 : 0.0,
  duration: const Duration(milliseconds: 250),
  child: child,
)

// Scroll-driven reveal
class RevealOnScroll extends StatefulWidget { ... }
// Uses VisibilityDetector or custom ScrollController
```

Respect `MediaQuery.of(context).disableAnimations` — equivalent of prefers-reduced-motion:
```dart
final reduceMotion = MediaQuery.of(context).disableAnimations;
final duration = reduceMotion ? Duration.zero : const Duration(milliseconds: 250);
```

**Deploy:**
- Web: `flutter build web --release` → `build/web/` → Netlify or Firebase Hosting
- iOS: `flutter build ipa`
- Android: `flutter build appbundle`

### Flutter redesign & polish

`/frontend-craft redesign` on Flutter project:
- Reads all existing screens and widgets
- Rewrites theme system (app_theme.dart)
- Rewrites widget visual layer (padding, colors, typography)
- Keeps all business logic, state management, navigation verbatim

`/frontend-craft polish` on Flutter project:
- Checks for: hard-coded Colors, missing AppSpacing usage, missing disableAnimations checks, no semanticsLabel on images
- Shows diff list → user selects → auto-fix

---

## React Native / Expo Platform

Triggered when `package.json` contains `react-native` or `expo`, or user selects RN in Q7.

### Platform detection

```
package.json → "react-native" or "expo" in dependencies → React Native
app.json or app.config.js → Expo confirmed
app/(tabs)/ or app/(expo-router)/ → Expo Router
```

### React Native Design Tokens

Create `src/theme/tokens.ts`:

```typescript
export const colors = {
  primary:    '[HEX from brief]',
  surface:    '[HEX]',
  muted:      '[HEX]',
  accent:     '[HEX]',
  background: '#F8F8F8',
  text:       '#111111',
  textMuted:  '#666666',
  border:     '#E0E0E0',
} as const;

export const spacing = {
  xs:  4,
  sm:  8,
  md:  16,
  lg:  24,
  xl:  40,
  x2l: 64,
} as const;

export const radius = {
  sm: 4,
  md: 8,
  lg: 16,
} as const;

export const typography = {
  display: { fontSize: 40, lineHeight: 48, fontWeight: '700' as const },
  h1:      { fontSize: 24, lineHeight: 32, fontWeight: '600' as const },
  body:    { fontSize: 16, lineHeight: 24, fontWeight: '400' as const },
  small:   { fontSize: 14, lineHeight: 20, fontWeight: '400' as const },
} as const;
```

### React Native Assemble

Each screen section as a component in `src/components/`:

```typescript
import React from 'react';
import { View, Text, StyleSheet, Pressable } from 'react-native';
import { colors, spacing, typography, radius } from '@/theme/tokens';

export function HeroSection() {
  return (
    <View style={styles.container}>
      <Text style={styles.headline}>Headline</Text>
      <Text style={styles.subline}>Subline text here</Text>
      <Pressable style={styles.cta}>
        <Text style={styles.ctaText}>CTA</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container:  { padding: spacing.lg, gap: spacing.md },
  headline:   { ...typography.display, color: colors.text },
  subline:    { ...typography.body, color: colors.textMuted },
  cta:        { backgroundColor: colors.primary, borderRadius: radius.md, padding: spacing.md },
  ctaText:    { ...typography.body, color: '#fff', fontWeight: '600', textAlign: 'center' },
});
```

**File structure:**
```
src/
  theme/
    tokens.ts          → design tokens
  components/
    HeroSection.tsx
    FeaturesSection.tsx
    CTASection.tsx
  screens/
    HomeScreen.tsx
assets/
  images/              → gen-image.sh output
  research.json
craft-brief.md
```

### React Native Normalize

Scan all `.tsx/.ts` files for:
- Inline `color:` strings not using `colors.*` → move to tokens
- Hard-coded numeric spacing → replace with `spacing.*`
- Hard-coded `fontSize` → replace with `typography.*`
- `borderRadius` numbers → replace with `radius.*`

### React Native Polish

**Motion — use `react-native-reanimated` if installed, else `Animated` API:**

```typescript
// Fade in on mount
const opacity = useSharedValue(0);
useEffect(() => {
  opacity.value = withTiming(1, { duration: 250 });
}, []);

// Respect reduce motion
import { AccessibilityInfo } from 'react-native';
const [reduceMotion, setReduceMotion] = useState(false);
useEffect(() => {
  AccessibilityInfo.isReduceMotionEnabled().then(setReduceMotion);
}, []);
```

Always check `reduceMotion` before animating — equivalent of `prefers-reduced-motion`.

**Images:**
```typescript
<Image
  source={require('@/assets/images/hero.jpg')}
  style={{ width: '100%', aspectRatio: 16/9 }}
  accessibilityLabel="Description of image"  // = alt text
/>
```

**Deploy:**
- Expo: `eas build` + `eas submit`
- Web: `npx expo export` → Netlify

### React Native redesign & polish

`/frontend-craft redesign` on RN project:
- Reads all screens and components
- Rewrites `tokens.ts` + all StyleSheet definitions
- Keeps navigation, state, API calls verbatim

`/frontend-craft polish` on RN project:
- Checks: inline colors/spacing, missing accessibilityLabel, no reduceMotion checks
- Shows diff list → user selects → auto-fix
