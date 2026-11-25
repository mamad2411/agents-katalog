---
name: remotion-beautiful-videos
description: |
  Generate premium 40s product launch videos using Remotion. Scrapes the brand's real landing page
  for colors/fonts/assets. Builds ANIMATED PRODUCT UI MOCKUPS — full dashboards, code editors,
  conversation UIs, data charts — not floating text on backgrounds. Uses lucide-react icons (never emoji),
  spring physics, SVG chart animations, TransitionSeries with fade/light-leak transitions.
  Follows the Stripe/Linear/Vercel 5-act structure. Integrates remotion-best-practices patterns.
---

# Remotion Beautiful Videos

Create 40-second product launch videos that look like a $50k agency produced them. The secret: build **animated product UI mockups** — real dashboards, conversation interfaces, code editors, data visualizations — all constructed in code and spring-animated.

## When to Use

User names a brand or gives a URL and wants a product launch / marketing / demo video.

## Tech Stack

Remotion 4.x + React 19 + TypeScript + Zod + lucide-react + @remotion/transitions + @remotion/google-fonts + @remotion/paths + @remotion/light-leaks + @remotion/media

## Core Philosophy

1. **Build product UI mockups, not abstract graphics.** The UI IS the animation.
2. **Scrape first, design second.** Every color, font, logo comes from the real brand site.
3. **Pacing is luxury.** 40 seconds lets content breathe. Never rush features.
4. **Taste over templates.** If it looks like "AI made this," redesign.
5. **One font family, weight hierarchy.** 300-600 range only, never bold (700+).

## Rules

Read individual rule files for detailed explanations and code examples:

### Design System
- [rules/typography.md](rules/typography.md) - Font weights (max 600), size hierarchy (min 24px), text safety
- [rules/color.md](rules/color.md) - Brand polarity, neutral tinting, 60-30-10 rule, accent opacity levels
- [rules/layout.md](rules/layout.md) - Grid system, 4px spacing scale, safe zones, border-radius hierarchy, anti-overlap

### Visual Content
- [rules/ui-mockups.md](rules/ui-mockups.md) - Product UI construction, density, title bars, syntax coloring, cursor simulation
- [rules/cards.md](rules/cards.md) - Staggered card grids, interior fill techniques, animated card bodies, no duplicates
- [rules/data-viz.md](rules/data-viz.md) - SVG charts, animated metrics, tabular-nums, status badges, anti-hero-metric

### Motion & Production
- [rules/motion.md](rules/motion.md) - Springs, easeOutExpo, per-character stagger, timing standards, hold-then-snap
- [rules/transitions.md](rules/transitions.md) - TransitionSeries, light leaks, fluid backgrounds, noise textures, parallax
- [rules/cinematic.md](rules/cinematic.md) - Film grain, vignette, shimmer sweep, color grading, glassmorphism, render settings

### Strategy & Quality
- [rules/taste.md](rules/taste.md) - AI slop blacklist, design principles, UX laws, self-review checklist, pacing
- [rules/narrative.md](rules/narrative.md) - 5-act structure, headline/UI rhythm, story arc, logo constellation
- [rules/narrative-templates.md](rules/narrative-templates.md) - Industry-specific narrative templates (AI SaaS, FinTech, DevTool, E-Commerce, Healthcare, Cybersecurity, Collaboration)
- [rules/workflow.md](rules/workflow.md) - Brand scraping, icon system, asset strategy, video embedding, file organization

## Reference Files (Code Patterns)

- [references/animations.md](references/animations.md) - FadeIn, ScaleIn, SplitText, Typewriter, CountUp, AnimatedPath
- [references/audio.md](references/audio.md) - Audio sync, beat detection, voiceover ducking
- [references/components.md](references/components.md) - GradientMesh, GlassPanel, FilmGrain, ProductFrame, BrandIcon
- [references/lottie.md](references/lottie.md) - @remotion/lottie integration, recommended sources
- [references/visual-effects.md](references/visual-effects.md) - Tiered visual effects library reference (lottie, motion-blur, confetti, flubber, three.js)

## Remotion API Reference (Bundled)

This skill bundles the full `remotion-best-practices` reference for Remotion API patterns. Load these when you need Remotion-specific API knowledge:

- [remotion-best-practices/rules/videos.md](remotion-best-practices/rules/videos.md) - Video embedding, trimming, volume, speed, looping
- [remotion-best-practices/rules/audio.md](remotion-best-practices/rules/audio.md) - Audio importing, trimming, volume, speed, pitch
- [remotion-best-practices/rules/timing.md](remotion-best-practices/rules/timing.md) - Interpolation curves, linear, easing, spring
- [remotion-best-practices/rules/transitions.md](remotion-best-practices/rules/transitions.md) - Scene transition patterns
- [remotion-best-practices/rules/compositions.md](remotion-best-practices/rules/compositions.md) - Compositions, stills, folders, default props
- [remotion-best-practices/rules/sequencing.md](remotion-best-practices/rules/sequencing.md) - Sequence delay, trim, duration limiting
- [remotion-best-practices/rules/fonts.md](remotion-best-practices/rules/fonts.md) - Google Fonts and local font loading
- [remotion-best-practices/rules/images.md](remotion-best-practices/rules/images.md) - Img component usage
- [remotion-best-practices/rules/charts.md](remotion-best-practices/rules/charts.md) - Bar, pie, line, stock chart patterns
- [remotion-best-practices/rules/light-leaks.md](remotion-best-practices/rules/light-leaks.md) - @remotion/light-leaks overlay effects
- [remotion-best-practices/rules/lottie.md](remotion-best-practices/rules/lottie.md) - @remotion/lottie integration
- [remotion-best-practices/rules/text-animations.md](remotion-best-practices/rules/text-animations.md) - Typography animation patterns
- [remotion-best-practices/rules/calculate-metadata.md](remotion-best-practices/rules/calculate-metadata.md) - Dynamic composition metadata
- [remotion-best-practices/rules/voiceover.md](remotion-best-practices/rules/voiceover.md) - AI voiceover with ElevenLabs TTS
- [remotion-best-practices/rules/parameters.md](remotion-best-practices/rules/parameters.md) - Zod schema parametrization
- [remotion-best-practices/rules/ffmpeg.md](remotion-best-practices/rules/ffmpeg.md) - FFmpeg operations for video trimming

## Workflow (MUST follow in order)

### Step 0: Scaffold Project (30 seconds, not 30 minutes)

Copy the built-in scaffold to create a ready-to-run Remotion project:

```bash
# Copy scaffold to new project directory
cp -r /path/to/skills/remotion-video/scaffold/ <brand-name>-launch-video/

# Replace project name in package.json
sed -i '' 's/{{PROJECT_NAME}}/<brand-name>-launch-video/' <brand-name>-launch-video/package.json

# Create required directories
mkdir -p <brand-name>-launch-video/public/brand
mkdir -p <brand-name>-launch-video/scripts

# Install dependencies
cd <brand-name>-launch-video && npm install
```

**Scaffold provides:** Remotion 4.x + Tailwind v4 + TransitionSeries + light-leaks + noise + paths + Google Fonts + lucide-react + Zod. Plus pre-built: `MainVideo.tsx` (5-act TransitionSeries), `Animations.tsx` (FadeIn/ScaleIn/SplitText/Typewriter/CountUp), `Background.tsx` (GradientMesh/FilmGrain/Vignette/ColorGrade), `UI.tsx` (GlassPanel/BrandIcon/GradientText), `theme.ts` (token 占位).

**Pre-requisites (install if missing):**

```bash
# yt-dlp — video downloader (REQUIRED for brand video assets)
brew install yt-dlp   # macOS
# or: pip install yt-dlp   # any OS with Python

# ffmpeg — video/audio processing (REQUIRED for trimming + BGM)
brew install ffmpeg   # macOS
# or: sudo apt install ffmpeg   # Linux

# Verify both are available
yt-dlp --version && ffmpeg -version
```

**Only proceed to Step 1 after `npm run dev` works AND `yt-dlp` + `ffmpeg` are installed.**

### Step 1: Scrape Brand + Download ALL Assets (BLOCKING — nothing starts before this)

**This step has THREE mandatory outputs. Do NOT proceed until ALL THREE exist in `public/brand/`.**

#### 1A. Scrape Design DNA

Use whichever browser tool is available. Try in order:

```bash
# Option 1: bb-browser (if installed)
bb-browser open https://brand-site.com
bb-browser snapshot -i
bb-browser eval "getComputedStyle(document.documentElement).cssText"
bb-browser eval "document.querySelector('h1')?.textContent"
bb-browser eval "document.querySelector('link[rel*=icon]')?.href"
bb-browser screenshot public/brand/homepage.png
bb-browser close

# Option 2: MCP chrome-devtools (if available)
# Use navigate_page, evaluate_script, take_screenshot MCP tools

# Option 3: curl + manual inspection (always works)
curl -s https://brand-site.com -o /tmp/brand-page.html
# Extract CSS: grep for font-family, --color-, background in the HTML
# Extract hero: grep for <h1, og:title, og:image in the HTML
# Screenshot: open the URL in your browser, take screenshot manually
```

**Any method works — the OUTPUT matters, not the tool.** You need: hex colors, font names, logo URL, hero copy, product type.

#### 1B. Download Logo SVG (MANDATORY — NEVER hand-write)

```bash
curl -o public/brand/logo.svg <favicon-or-header-svg-url>
# Verify it renders: open public/brand/logo.svg in browser
```

#### 1C. Download Video OR Product Screenshots (MANDATORY — at least ONE)

**Try video first (ALWAYS preferred over static images):**

```bash
# Option A: Found YouTube/Vimeo embed on brand site
yt-dlp -f "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" \
  -o public/brand/demo-full.mp4 "<video-url>"
ffmpeg -i public/brand/demo-full.mp4 -ss 0 -t 8 -c copy public/brand/demo.mp4

# Option B: No embed found — search YouTube
yt-dlp "ytsearch1:<BrandName> official product demo 2024" \
  -f "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" \
  -o public/brand/demo-full.mp4
ffmpeg -i public/brand/demo-full.mp4 -ss 0 -t 8 -c copy public/brand/demo.mp4

# Option C: Direct CDN video found on page
curl -o public/brand/demo-full.mp4 "<cdn-video-url>"
ffmpeg -i public/brand/demo-full.mp4 -ss 0 -t 8 -c copy public/brand/demo.mp4
```

**After downloading, WATCH the clip. Does it show the product's core experience?** If it's a random promo with talking heads or unrelated footage, search for a better one. The video must show the actual product UI in action — dashboards, editors, conversations, the thing users interact with.

**If video truly impossible, download product screenshots:**

```bash
# Download hero image, product screenshots, og:image
curl -o public/brand/hero.png "<hero-image-url>"
curl -o public/brand/product-ui.png "<product-screenshot-url>"

# Full-page screenshot (use whichever tool is available)
bb-browser screenshot public/brand/homepage-full.png --full-page  # bb-browser
# or: use MCP chrome-devtools take_screenshot
# or: manually screenshot in browser and save to public/brand/
```

#### 1D. Download BGM Track (MANDATORY — NEVER ask user for music)

**Try sources in order until one works. All are royalty-free, no attribution required:**

```bash
# Source 1: Pixabay Music API (no login needed for direct MP3 links)
# Search: https://pixabay.com/music/search/?q=corporate+ambient&duration=30-60
# Find a track page, look for the download button's direct URL
curl -L -o public/brand/bgm-raw.mp3 "<pixabay-direct-mp3-url>"

# Source 2: Mixkit (direct download, no login)
# Browse: https://mixkit.co/free-stock-music/
# Each track has a direct download link — right-click "Download" → copy URL
curl -L -o public/brand/bgm-raw.mp3 "https://assets.mixkit.co/music/download/mixkit-<track-name>.mp3"

# Source 3: Uppbeat (direct download for free tier)
# Browse: https://uppbeat.io/browse/music
# Free tracks have direct download URLs after browsing

# Source 4: YouTube royalty-free music (always works as last resort)
yt-dlp -x --audio-format mp3 -o public/brand/bgm-raw.mp3 \
  "ytsearch1:royalty free corporate ambient background music 30 seconds"

# After downloading from ANY source, trim + fade:
ffmpeg -i public/brand/bgm-raw.mp3 -t 45 -af "afade=in:0:d=2,afade=out:st=42:d=3" public/brand/bgm.mp3
```

**Tone matching guide:**
| Brand Tone | Search Keywords |
|------------|----------------|
| Tech/SaaS | "corporate ambient", "tech minimal", "digital innovation" |
| Creative/Design | "inspiring cinematic", "modern elegant" |
| Startup/Hype | "upbeat technology", "energetic corporate" |
| Enterprise/Serious | "ambient corporate", "calm business" |
| Playful/Consumer | "happy upbeat", "positive modern" |

**If one source fails (login wall, CAPTCHA, region block), move to the next. `yt-dlp` YouTube search (Source 4) ALWAYS works as ultimate fallback.** See [rules/workflow.md](rules/workflow.md) for full BGM sourcing protocol.

#### ⛔ BLOCKING GATE — Verify Before Proceeding

```bash
ls -la public/brand/
# MUST contain ALL of these:
# ✅ logo.svg (or logo.png)          — brand logo, downloaded verbatim
# ✅ demo.mp4 OR hero.png            — real product visual (video preferred)
# ✅ bgm.mp3                         — background music track
# ✅ homepage.png                     — reference screenshot
```

**🚫 DO NOT PROCEED TO STEP 2 IF ANY OF THESE ARE MISSING:**
- No `logo.svg`? → Go back and download it. NEVER hand-write SVG paths.
- No `demo.mp4` AND no `hero.png`? → Go back and download product visuals. NEVER build a video with zero real assets.
- No `bgm.mp3`? → Go back and download from Pixabay. NEVER ship a silent video.

**Extract from scrape:** exact hex colors, font families, hero copy, product features, visual style.

### Step 1.5: Ask User for Storyline (BLOCKING — never assume narrative)

After scraping, STOP and ask the user:

> I've scraped [brand] and extracted: [colors, fonts, product type, features list].
> 
> Before I build scenes, I need your storyline:
> 1. **What story do you want to tell?** (product launch? feature highlight? brand intro? problem→solution?)
> 2. **Which features to showcase?** (I found: [list from scrape]. Pick 2-4, or tell me others)
> 3. **What's the key message / tagline?** (or I can use: "[hero copy from scrape]")
> 4. **Any proof points?** (metrics, benchmarks, user count, testimonials — or skip Act 4)
> 5. **Tone?** (hype launch? calm authority? playful? technical?)

**Why this step exists:** Every user's video must be DIFFERENT. The 5-act structure is a FRAMEWORK, not a script. ACT 1 (Hook) is always a product UI — but WHICH UI, showing WHAT interaction, depends on the user's story. ACT 3 (Showcase) could be 2 features or 4. ACT 4 could be data or testimonials or cut entirely for a longer showcase.

**Match industry template:** After identifying the brand's industry, load [rules/narrative-templates.md](rules/narrative-templates.md) for pre-built narrative patterns (AI SaaS, FinTech, DevTool, E-Commerce, Healthcare, Cybersecurity, Collaboration). Use the matching template as a STARTING POINT, then adapt to the user's answers.

**NEVER auto-generate storyline.** "It reasons. It codes. It creates." is lazy template output. Ask, listen, then build.

### Step 2: Build Theme from Scraped Data

Update `theme.ts` using ONLY scraped values. Replace all `#REPLACE_ME` tokens. Update `lib/fonts.ts` to load the brand's actual fonts. Update `index.css` @theme vars to match.

### Step 3: Build 6-Act Scenes (from user's storyline) — MUST USE REAL ASSETS

The structure is a framework. Adapt content to the user's story. **ACT 0 (Logo) is MANDATORY.**

| Act | Structure (fixed) | Content (from user) | **Required Real Asset** |
|-----|-------------------|---------------------|------------------------|
| **ACT 0 Logo** | **MANDATORY. Brand logo spring entrance + shimmer sweep. 4s.** | Real SVG logo | `<Img src={staticFile("brand/logo.svg")} />` |
| ACT 1 Hook | Product UI mockup, spring entrance | Which product screen? | **`<OffthreadVideo src={staticFile("brand/demo.mp4")} />` or `<Img src={staticFile("brand/hero.png")} />`** |
| ACT 2 Reveal | Capability icons + tagline | Which capabilities? | Icons from lucide-react |
| ACT 3 Showcase | Headline → UI alternating rhythm | Which features? | **At least 1 scene: real screenshot/video inside UI chrome** |
| ACT 4 Proof | Data visualization / social proof (optional) | What metrics? | Code-built data viz OK |
| ACT 5 Close | CTA lockup + brand logo again | What tagline? | `<Img src={staticFile("brand/logo.svg")} />` again |

**⚠️ CRITICAL: ACT 0/5 logo usage does NOT count. Among ACT 1-4, at least 2 acts MUST use a real downloaded video or screenshot via `staticFile()`.** This means `<OffthreadVideo src={staticFile("brand/demo.mp4")} />` or `<Img src={staticFile("brand/hero.png")} />` showing actual product visuals — not just the logo SVG. Pure code-built UIs are SUPPLEMENTS, not replacements. If ACT 1-4 contain zero `staticFile("brand/...")` references for video/images, you are doing it wrong.

**How to use assets in scenes:**

```tsx
// Video inside browser chrome (product UI recordings)
<div style={{ borderRadius: 16, overflow: "hidden", border: "1px solid rgba(255,255,255,0.1)" }}>
  <OffthreadVideo src={staticFile("brand/demo.mp4")} style={{ width: 1200 }} />
</div>

// Full-screen video (cinematic/lifestyle footage)
<AbsoluteFill>
  <OffthreadVideo src={staticFile("brand/demo.mp4")} style={{ width: "100%", height: "100%" }} />
</AbsoluteFill>

// Product screenshot inside UI mockup
<Img src={staticFile("brand/product-ui.png")} style={{ width: "100%", objectFit: "contain" }} />
```

**ACT 0 Logo Animation Requirements:**
- Real brand SVG wordmark/logo — downloaded, NEVER hand-written
- Spring scale entrance (0→1, damping 16, stiffness 50)
- Shimmer sweep across logo (frame 40-80)
- **NO text under the logo** — logo stands alone, pure and confident
- **Premium background required** — NEVER plain white/black. Add: GradientMesh (brand colors, low opacity 0.05-0.08), center glow pulse (radial-gradient breathing), subtle conic-gradient radial lines. The background sells luxury.
- Logo appears ONLY in ACT 0 and ACT 5 — NOT in middle acts

See [rules/workflow.md](rules/workflow.md) for Asset Strategy details.

### ⛔ Step 3 BLOCKING GATE: Asset Relevance Check (MANDATORY — every asset must make sense)

**Before moving to Step 3.5, review EVERY real asset you placed in a scene. Each one MUST pass ALL 4 checks:**

| Check | Question | FAIL Example |
|-------|----------|-------------|
| **Context Match** | Does this asset show what this scene is ABOUT? | Login page video in a "speed & performance" scene |
| **Narrative Flow** | Does the asset support the headline above/below it? | "Collaborate in real-time" headline over a solo-user screenshot |
| **Visual Quality** | Is it high-res, no watermarks, no OS chrome/cursors? | 480p YouTube rip with mouse cursor visible |
| **Brand Alignment** | Does it look like official brand marketing material? | Third-party review video used as if it's the brand's own |

**How to check:**
1. For each scene file, find every `staticFile("brand/...")` usage
2. Open the actual asset file and WATCH/VIEW it fully
3. Read the scene's headline text — does the asset illustrate THAT specific point?
4. If the asset doesn't match the scene context → find a better asset or change the scene narrative to match

**Common violations:**
- Downloading one generic product demo and reusing it in 3 different scenes (lazy — each scene needs context-appropriate footage)
- Using a "getting started" tutorial clip in the "enterprise scale" proof scene
- Placing a dashboard screenshot in a scene about "beautiful design" when the dashboard isn't visually impressive
- Using ANY asset you haven't actually watched/viewed yourself

**If ANY asset fails relevance → replace it or re-download a better one BEFORE proceeding.**

### Step 3.5: Wire BGM into MainVideo (MANDATORY — already downloaded in Step 1D)

BGM was downloaded in Step 1D. Now wire it into `MainVideo.tsx`. **This is NOT optional.**

```tsx
// Add to MainVideo.tsx — FIRST thing inside <AbsoluteFill>
import { Audio, staticFile, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export const MainVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // BGM volume envelope: fade in 2s, sustain at 0.3, fade out 3s
  const bgmVolume = Math.min(
    interpolate(frame, [0, 2 * fps], [0, 0.3], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
    interpolate(frame, [durationInFrames - 3 * fps, durationInFrames], [0.3, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })
  );

  return (
    <AbsoluteFill>
      <Audio src={staticFile("brand/bgm.mp3")} volume={bgmVolume} />
      {/* ... TransitionSeries with scenes ... */}
    </AbsoluteFill>
  );
};
```

**⛔ BLOCKING: After writing MainVideo.tsx, grep for `<Audio` in the file. If not found, you forgot BGM. Add it NOW.**

### Step 3.6: Beat-Sync Scene Transitions (AUTOMATIC)

```bash
# Analyze BGM and generate beat map
cp /path/to/skills/remotion-video/scripts/beat-sync.ts scripts/
npx tsx scripts/beat-sync.ts public/brand/bgm.mp3
```

Use `suggestedCuts` from `public/brand/beat-map.json` to fine-tune TransitionSeries `durationInFrames` so scene cuts land on beats.

### Step 4: Polish

Film grain + vignette + color grade + shimmer sweeps. See [rules/cinematic.md](rules/cinematic.md).

### Step 4.5: Readability & Watchability Audit (MANDATORY)

Before rendering, automatically validate every scene's timing:
- Every text element must be on screen long enough to READ (word_count × 10 frames minimum)
- Headlines hold 60+ frames (2s), UI mockups hold 120+ frames (4s)
- Typing animations MUST complete before scene transitions
- No text smaller than 28px at 1920x1080
- If any scene fails → fix duration/speed BEFORE rendering

See [rules/taste.md](rules/taste.md) "Automatic Readability & Watchability Audit" for full checklist.

**MANDATORY: Print Timing Audit Table after writing EVERY scene.** Do NOT proceed to the next scene without outputting this:

```
TIMING AUDIT — [SceneName] (durationInFrames: XXXf)
| Element | Type | delay | chars/items | finish frame | breathing (scene end - finish) | PASS/FAIL |
|---------|------|-------|-------------|-------------|-------------------------------|-----------|
| "text"  | SplitText | 10 | 24 chars × 2f stagger | 58f | 92f | ✓ PASS |
```

If ANY row shows breathing < 45f → STOP and fix before continuing. This is not optional.

### Step 5: Open Remotion Studio for User Preview (BLOCKING — never skip)

**NEVER render directly. ALWAYS open Remotion Studio first and let the user preview.**

```bash
# Start studio on an available port
npx remotion studio --port <available-port>
# Then open in browser for the user
open http://localhost:<port>
```

Tell the user the URL and WAIT for their feedback. Only proceed to render after the user confirms the video looks good. The user may request changes — iterate until approved.

**Why this step exists:** Rendering takes time. If the video has visual bugs (cropped images, animations cut off, bad pacing), the user discovers them AFTER waiting for a render. Studio preview catches issues in seconds.

### Step 6: Run Asset + BGM + Visual Audit (BLOCKING — render will not proceed without this)

Before rendering, run THREE mandatory checks:

#### 6A. Asset Usage Check (MANUAL)

```bash
# Check: do scenes actually USE real assets?
grep -r "staticFile" src/scenes/ | grep -E "\.(mp4|png|jpg)" | head -20
# ⚠️ logo.svg references do NOT count for this check.
# MUST find at least 2 matches in ACT 1-4 scenes (Hook, Reveal, Showcase, Proof)
# using demo.mp4, hero.png, product-ui.png, or other downloaded visuals.
#
# ✅ PASS: HookScene.tsx:staticFile("brand/demo.mp4") + ShowcaseScene.tsx:staticFile("brand/product-ui.png")
# ❌ FAIL: only LogoScene.tsx:staticFile("brand/logo.svg") + CloseScene.tsx:staticFile("brand/logo.svg")

# If fewer than 2 video/image matches in ACT 1-4 → GO BACK TO STEP 3 and add real assets.
```

#### 6A-2. Asset Relevance Check (MANUAL)

For EVERY `staticFile("brand/...")` match from 6A, verify the asset makes sense for that scene:
- Open the asset, watch/view it
- Read the scene's headline — does the asset illustrate THAT point?
- If mismatched → swap asset or adjust scene narrative
- See Step 3 BLOCKING GATE above for the full 4-check relevance table

#### 6B. BGM Check (MANUAL)

```bash
# Check: does MainVideo have <Audio> with bgm.mp3?
grep -n "Audio" src/MainVideo.tsx
grep -n "bgm" src/MainVideo.tsx
# MUST find <Audio src={staticFile("brand/bgm.mp3")} with volume envelope
# If not found → ADD IT NOW. Copy the code from Step 3.5 above.

# Also verify no localhost URLs survived:
grep -r "localhost:8888" src/
# MUST return ZERO results. Fix any matches with staticFile().
```

#### 6C. Visual Audit Script

```bash
cp /path/to/skills/remotion-video/scripts/visual-audit.ts scripts/
cp /path/to/skills/remotion-video/scripts/beat-sync.ts scripts/
npx tsx scripts/visual-audit.ts
```

**The audit checks (9 categories):**
1. **TIMING** — animations complete with 45+ frames breathing room
2. **FONT-SIZE** — no text smaller than 28px
3. **FONT-WEIGHT** — no weight above 600 (semi-bold)
4. **SAFE-ZONE** — padding ≥ 60px from edges for content
5. **OBJECTFIT** — no `objectFit: "cover"` on screenshots
6. **CONTRAST** — basic WCAG AA contrast checks
7. **IMG-SAFETY** — all `<Img>` have objectFit or maxHeight
8. **REAL-ASSETS** — at least 2 scenes reference `staticFile("brand/...")` for real media
9. **BGM-WIRED** — MainVideo.tsx contains `<Audio src={staticFile("brand/bgm.mp3")}>`

If ANY FAIL → fix → re-run → only then render:

```bash
npx remotion render --codec h264 --crf 16 --image-format png
```

## Premium vs Template

| Premium ($50k) | Template (avoid) |
|---|---|
| Logo animation opens the video | No logo or text-only logo |
| BGM with beat-synced transitions | Silent or stock music slapped on |
| Full product UI mockups | Text on gradient background |
| Real brand assets inside UI chrome | Pure code mockups, no screenshots |
| Per-character text stagger | Entire text block fades in |
| SVG chart path-drawing | Big numbers with no visualization |
| Spring physics (overshoot + settle) | Linear or basic ease |
| easeOutExpo (Apple keynote feel) | Cubic or bounce easing |
| 40s with breathing room | 30s of rushing through features |
| Film grain + vignette + color grade | Perfectly clean digital |
| One typeface, weight contrast 300-600 | Multiple fonts or bold 700+ |
