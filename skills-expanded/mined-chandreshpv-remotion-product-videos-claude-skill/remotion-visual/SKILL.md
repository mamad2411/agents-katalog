---
name: remotion-visual
title: Remotion Visual Production Skill
author: Chandresh Vaghanani
version: 1.2
description: Use this skill when creating Remotion promo videos. Covers canvas sizing, scene structure, mockup 3D entry, cursor animations, micro-animations, transitions, audio, and production best practices.
---

# Remotion Visual Production Skill

> Built from real production experience creating the SureCart 4.2 launch video.
> Author: **Chandresh Vaghanani**

---

## Before You Start — 2 Questions (Non-Negotiable)

Ask these **2 questions** before writing any code. Keep it casual — one message, two questions. Do not skip them even if the user says "just go" or "start now." These 10 seconds prevent hours of rework.

```
Before I start — two quick things:
1. Light or dark background? (or share your website/screenshot and I'll pull it from there)
2. Do you have a product screenshot or mockup? (totally optional — I can build without one)
```

That's it. No more questions unless the user volunteers more.

**What to do with the answers:**

- **If they share a mockup/screenshot** — extract background color, accent color, font style, UI copy. Use it.
- **If they share a website URL** — fetch it, extract the same. Do not guess.
- **If they answer light/dark only** — proceed with the No-Info Fallback Defaults below.
- **If they skip both questions** — proceed with the No-Info Fallback Defaults below. Do not ask again.

Other assets (logo, music, extra colors) — accept if offered, but never block on them.

---

## No-Info Fallback Defaults

**When brand info is unavailable, the AI's instinct is to shrink fonts and add padding. That instinct is wrong for video. Apply these instead:**

These kick in automatically when no mockup, screenshot, or website is provided. They ensure a professional result even with zero brand info.

### Layout
- `justifyContent: "center"` + `alignItems: "center"` on every scene's AbsoluteFill — no exceptions
- `marginTop: -50` to pull content slightly above true center
- Mockup/card width: **1200px** (use the upper end — fill the frame)
- Container padding: **max 40px** — never more
- Content must occupy at least **75% of the 1080px height**. If it doesn't, increase font sizes or reduce gaps.

### Font sizes (fallback — upper end of range)
| Element | Fallback size |
|---------|--------------|
| Main headline | 140px |
| Sub-headline | 56px |
| Body / description | 36px |
| Label / pill | 22px |
| Card content text | 28px |

### Colors (fallback palette — safe and professional)
- Background: `#0a0a0f` (near-black, neutral)
- Accent: `#6366f1` (indigo — readable, modern, not product-specific)
- Text: `#ffffff`
- Muted text: `rgba(255,255,255,0.55)`
- Card bg: `rgba(255,255,255,0.06)`

> These are STARTING POINTS only. The moment the user shares brand colors, replace them entirely.

### What NOT to do without brand info
- Do NOT use neon/cyber colors — that's a personal aesthetic, not a brand match
- Do NOT use `paddingTop: 120` and call it "centered" — it's top-aligned with dead space
- Do NOT pick `fontSize: 32` for a headline because it "looks clean" — it's illegible on video

---

## Rule #1 — Canvas is NOT a Website

**This is the single most common mistake in AI-generated Remotion videos.**

Remotion canvas is **1920×1080px**. Design to fill it — not like a webpage.

> ⚠️ **These are MINIMUMS. Writing `fontSize: 18` for body text is a BUG, not a style choice.**
> Anything below the minimum column means the text is unreadable on a 1080p screen.
> Treat these numbers like type errors — they must be fixed before moving on.

| Element | MINIMUM (hard floor) | Recommended Range |
|---------|---------------------|-------------------|
| Main headline | 80px | 100–160px |
| Sub-headline | 40px | 48–72px |
| Body / description | 28px | 32–40px |
| Label / pill / badge | 18px | 20–24px |
| Card content text | 22px | 24–32px |

**Rules:**
- Content must feel like it fills the screen
- Mockup cards: `width: 1100–1200px`, centered
- Container padding: max 48px — NOT 80–120px like a webpage
- If text feels "too big for comfort" — it's probably right for video

---

## Rule #2 — All Animations MUST Use `useCurrentFrame()`

```tsx
// CORRECT
const frame = useCurrentFrame();
const opacity = interpolate(frame, [0, 20], [0, 1], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});

// FORBIDDEN — will NOT render correctly
// CSS: transition: opacity 1s ease
// Tailwind: animate-fade-in
// CSS @keyframes
```

**Always include `extrapolateLeft: "clamp"` and `extrapolateRight: "clamp"`** on every `interpolate()` call unless you explicitly need unbounded values. Forgetting this causes values to bleed outside their range and creates subtle bugs.

---

## Rule #3 — Determinism

```tsx
// FORBIDDEN — different value on every render pass
const x = Math.random() * 100;

// CORRECT — same value every time, every frame
import { random } from "remotion";
const x = random("particle-x-1") * 100; // string seed = deterministic
```

---

## Rule #4 — Assets

```tsx
import { staticFile } from "remotion";
import { Img } from "remotion";        // NOT native <img>
import { Audio } from "@remotion/media";

// Always use staticFile() for anything in public/ folder
<Audio src={staticFile("bg-music.mp3")} />
<Img src={staticFile("logo.png")} />   // <Img> ensures asset loads before frame renders

// Remote URLs don't need staticFile() but require CORS
```

---

## Rule #5 — Smooth Preview Playback

Add `premountFor={30}` on `<Sequence>` components so heavy components preload 30 frames before their time:

```tsx
<Sequence from={90} durationInFrames={120} premountFor={30}>
  <HeavyScene />
</Sequence>
```

---

## Easing Recipes

```tsx
import { Easing } from "remotion";

// Crisp UI entrance (strong ease-out, no overshoot) — most enter animations
Easing.bezier(0.16, 1, 0.3, 1)

// Slow editorial fade (balanced ease-in-out) — mood transitions
Easing.bezier(0.45, 0, 0.55, 1)

// Playful overshoot — bouncy/fun elements
Easing.bezier(0.34, 1.56, 0.64, 1)

// Spring — no bounce (mockup entries, cards, UI)
spring({ frame, fps, config: { damping: 200 } })

// Spring — snappy with slight bounce (punchy elements)
spring({ frame, fps, config: { damping: 20, stiffness: 200 } })

// Spring — bouncy/playful
spring({ frame, fps, config: { damping: 8 } })
```

---

## Pre-Layout Gates — Run BEFORE Writing Any Scene Layout

**These are not suggestions. Run all three gates before writing the first `<div>` of any scene. If any gate fails, change the layout — never patch with fixed dimensions or extra content.**

---

### Gate 1 — Canvas Fill (both axes, mandatory)

```
Width axis:
  dead_side = (1920 − content_width) / 2
  MUST be ≤ 300px. If > 300px → content is too narrow. Widen it or change layout.

Height axis:
  fill_h = content_height / 1080
  MUST be ≥ 0.80. If < 0.80 → content is too short. Change the layout shape.
```

> ⚠️ **If height fails, do NOT fix it by setting a fixed height on cards or containers.**
> A fixed height creates an empty void inside the card — the dead space moves inside the element instead of being eliminated. The only real fix is changing the layout shape (Gate 2).

Real failure example — 3 short feature cards:

| Version | content_width | dead_side | content_height | fill_h | Verdict |
|---------|--------------|-----------|----------------|--------|---------|
| v1: 3-col cards (365px) | 1151px | **384px** | 416px | **38%** | ❌ both axes fail |
| v2: forced `height: 720px` | 1542px | 189px | 864px | 80% | ✅ width, ❌ visual (empty void in card) |
| v3: horizontal rows (1400px) | 1400px | 260px | 916px | **85%** | ✅ both axes pass |

---

### Gate 2 — Layout Selection Decision Table

**Content volume determines layout shape. Choose layout from this table BEFORE writing code.**

| Items | Content per item | Correct layout | Why |
|-------|-----------------|----------------|-----|
| 3–5 items | icon + name + 1 line | **Horizontal rows** (1400px wide) | Short content stacks vertically → fills height naturally |
| 3 items | icon + name + 2–3 lines | **3-column cards** (min 1100px wide) | Enough content to fill card height without void |
| 2 items | substantial | **Side-by-side large cards** or split-screen | |
| 1 item | anything | **Full-screen hero** | |

> If the natural layout for your content leaves either axis below threshold after Gate 1 — that layout is wrong. Pick a different row in this table.
>
> Never choose layout by aesthetics or default instinct. Content fit first. Aesthetics second.

---

### Gate 3 — Content Density Limit

> **Per item maximum: icon + name + 1 short line. Hard stop.**
> No bullets. No sub-sections. No paragraphs. No second description lines.

A viewer has ~5 seconds per scene. They read 1 line. They do not read 4 bullets.

**If content feels thin and you want to add more to fill space — that is Gate 2 telling you the layout shape is wrong, not that content is missing.**

Fill empty space with **SIZE** (bigger fonts, bigger icons, larger gaps between items) — never with more content.

---

## Universal Scene Rules

1. **Vertical alignment** — `justifyContent: "center"` + `marginTop: -40` to `-60` (slightly above true center = modern, premium feel. NOT top-aligned with padding.)

   ❌ **WRONG** — top-aligned, leaves empty space at bottom:
   ```tsx
   <AbsoluteFill style={{ display: "flex", flexDirection: "column", paddingTop: 110 }}>
     <h1>Headline</h1>
     <p>Subtext</p>
     {/* large empty void at bottom */}
   </AbsoluteFill>
   ```
   ✅ **RIGHT** — vertically centered, slightly above midpoint:
   ```tsx
   <AbsoluteFill style={{ display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", marginTop: -50 }}>
     <h1>Headline</h1>
     <p>Subtext</p>
     {/* content fills the frame — no dead space */}
   </AbsoluteFill>
   ```
2. **Canvas fill — run Pre-Layout Gates before writing this scene.** Gate 1 checks both width (`dead_side ≤ 300px`) and height (`fill_h ≥ 0.80`) together. Gate 2 selects the layout shape from the decision table. Gate 3 caps content per item. All three gates live in the Pre-Layout Gates section above — they supersede the old width-only check that was here.

3. **Headline z-index** — always `zIndex: 20` on headline container so mockup never overlaps text
4. **Headline overflow** — always `whiteSpace: "nowrap"` on headline text (prevents wrap behind mockup)
5. **No `overflow: hidden` on AbsoluteFill** — clips cursor and SVG elements. Remove it or place cursor outside.
6. **15 frame hold** — every scene must have at least 15 frames of fully-visible hold at the END before transition fires. Never start a transition while an animation is still playing in the outgoing scene.
7. **Font** — use one consistent font throughout. Recommended: **Plus Jakarta Sans** via `@remotion/google-fonts`. Max available weight: **800** (writing `fontWeight: 900` renders as 800).
8. **Color** — 2–3 brand colors max. One dark background, one primary accent, white/muted white for text. Consistent across all scenes.

### Typography Hierarchy

```tsx
// Supertitle / Label pill
{ fontSize: 20, letterSpacing: "4px", textTransform: "uppercase", fontWeight: 600 }

// Main headline
{ fontSize: 112, fontWeight: 800 }  // range: 100–160px

// Sub-text / description
{ fontSize: 36, opacity: 0.7 }  // range: 32–40px

// Trust line / small badges
{ fontSize: 26, opacity: 0.5 }  // range: 24–28px
```

### Font Setup

```tsx
import { loadFont } from "@remotion/google-fonts/PlusJakartaSans";

// Call at top level — must load before render
const { fontFamily } = loadFont("normal", {
  weights: ["400", "600", "800"],
  subsets: ["latin"],
});
```

For other fonts: install via `@remotion/google-fonts/FontName` or drop `.woff2` in `public/` and use `loadFont` from `@remotion/fonts`.

---

## Scene Structure Template

Every scene follows this fixed layer order (bottom → top):

```tsx
<AbsoluteFill style={{ background: brandBg }}>

  {/* Layer 1 — Background glow */}
  <div style={{
    position: "absolute",
    inset: 0,
    background: "radial-gradient(ellipse at center, rgba(ACCENT, 0.15) 0%, transparent 70%)",
  }} />

  {/* Layer 2 — Headline (zIndex: 20 always) */}
  <div style={{
    position: "absolute",
    zIndex: 20,
    top: 110,
    width: "100%",
    textAlign: "center",
  }}>
    {/* Supertitle pill */}
    {/* Main headline — whiteSpace: "nowrap" */}
  </div>

  {/* Layer 3 — Mockup / Card */}
  <div style={{
    position: "absolute",
    top: 375,
    left: "50%",
    transform: `translateX(-50%) perspective(1400px) ...`,
    transformOrigin: "center top",
    width: 1150,
  }} />

  {/* Layer 4 — Cursor (ALWAYS last, direct child of AbsoluteFill) */}
  {/* NEVER inside mockup div or any transformed/overflow:hidden parent */}
  <CursorSVG />

</AbsoluteFill>
```

**Layer order is non-negotiable.** Cursor last. Always.

---

## Per-Scene Self-Verification Checklist

**Before moving to the next scene, verify ALL of these:**

- [ ] **Gate 1 passed** — calculated `dead_side = (1920 − content_width) / 2 ≤ 300px` AND `fill_h = content_height / 1080 ≥ 0.80` before writing layout
- [ ] **Gate 2 passed** — layout shape chosen from the decision table (not default instinct or aesthetics)
- [ ] **Gate 3 passed** — per item content is icon + name + 1 short line max; no bullets, no paragraphs
- [ ] No font below `32px` anywhere in this scene (card text, labels, descriptions)
- [ ] Sub-headline / description is `≥ 48px`
- [ ] Background color matches the actual brand (NOT a default dark/cinematic theme)
- [ ] Cursor is a direct child of `AbsoluteFill` — not inside a mockup or transformed div
- [ ] Every `interpolate()` call has `extrapolateLeft: "clamp"` and `extrapolateRight: "clamp"`
- [ ] Scene ends with `≥ 15 frames` of fully-visible hold before transition fires

**If any box is unchecked — fix it before writing the next scene.**

---

## Mockup 3D Entry Animation

**Always fixed regardless of style chosen:**
- `perspective(1400px)` in the transform string
- `transformOrigin: "center top"` on mockup wrapper
- Opacity fade-in over 20 frames
- Starting scale always ≤ 1.0 (max 1.05 for Slam only)

### Option A — Tilt Drop *(Recommended — SureCart style)*

```tsx
const ENTER = 0; // frame offset when mockup starts entering

const mScale = spring({
  frame: frame - ENTER, fps,
  config: { damping: 18, stiffness: 110 },
  from: 0.72, to: 1,
});
const mOpacity = interpolate(frame, [ENTER, ENTER + 20], [0, 1], {
  extrapolateLeft: "clamp", extrapolateRight: "clamp",
});
const rotX = interpolate(frame, [ENTER, ENTER + 55], [10, 2], {
  extrapolateLeft: "clamp", extrapolateRight: "clamp",
});
const rotY = interpolate(frame, [ENTER, ENTER + 55], [14, 2], {
  extrapolateLeft: "clamp", extrapolateRight: "clamp",
});

// Apply to wrapper div:
// transform: `translateX(-50%) perspective(1400px) rotateX(${rotX}deg) rotateY(${rotY}deg) scale(${mScale})`
// opacity: mOpacity
// transformOrigin: "center top"
```

### Option B — Flip Forward
`rotateX: 45→0`, `scale: 0.88→1`, spring `{ damping: 200, stiffness: 120 }`. Bold reveal feel.

### Option C — Drift Up
`translateY: 60→0`, `scale: 0.92→1`, `opacity: 0→1` over 30f, `Easing.bezier(0.16, 1, 0.3, 1)`. Clean and minimal.

### Option D — Rotate In
`rotateY: 25→0`, `scale: 0.85→1`, spring `{ damping: 200 }`. Side-reveal, modern.

### Option E — Slam
`scale: 1.05→1`, spring `{ stiffness: 180, damping: 12 }` + opacity. Punchy, energetic. Starting scale max 1.05 — higher will overflow.

---

## Mouse Cursor

### Positioning Rules
- **Direct child of AbsoluteFill** — never inside mockup, card, or any transformed parent
- **Canvas-space coordinates** (1920×1080)
- Cursor tip lands just to the RIGHT of click target (keeps target word readable)
- Entry: glide from a nearby position — NOT from a screen corner
- Canvas coordinate reference: mockup (1150px wide, centered) → left edge at x≈385, right at x≈1535. Inner padding ~44px: content starts at x≈429.
- Recalculate cursor coords whenever mockup `top` changes

### Cursor Style Options

**Option A — Arrow Pointer (SureCart style)**
```tsx
<svg
  width="26" height="30" viewBox="0 0 13 15"
  style={{
    position: "absolute",
    left: cursorX,
    top: cursorY,
    zIndex: 100,
    filter: "drop-shadow(1px 2px 6px rgba(0,0,0,0.6))",
    transform: `scale(${cursorScale})`,
    transformOrigin: "2px 2px",
  }}
>
  <path
    d="M1.5 1.5 L1.5 13 L4.5 10 L7 15.5 L9 14.5 L6.5 9 L11.5 9 Z"
    fill="white" stroke="#111" strokeWidth="1.1" strokeLinejoin="round"
  />
</svg>
```

**Option B — Hand Pointer**
Use an SVG hand icon with the same absolute positioning, `zIndex: 100`, press scale animation.

### Press Scale Animation (Universal — use with any cursor style)

```tsx
const CLICK = 45; // frame when click happens

const press = interpolate(
  frame,
  [CLICK, CLICK + 4, CLICK + 10],
  [0, 1, 0],
  { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
);
const cursorScale = 1 - 0.30 * press;
```

### Click Effect Options

**Option A — Ripple Ring (SureCart style)**
```tsx
// TX, TY = click target canvas coordinates
const t = interpolate(frame, [CLICK, CLICK + 20], [0, 1], {
  extrapolateLeft: "clamp", extrapolateRight: "clamp",
});
// Render as absolute div centered on click point:
// left: TX - t*40, top: TY - t*40
// width: t*80, height: t*80
// borderRadius: "50%"
// border: `3px solid rgba(ACCENT_COLOR, ${1 - t})`
// pointerEvents: "none"
```

**Option B — Flash**
Quick white radial flash at click point: `opacity: 0 → 0.4 → 0` over 10 frames.

**Option C — Pulse**
Click target element scales `1 → 1.08 → 1` over 20 frames.

---

## Mockup Micro-Animations

### Typing Cursor

When mouse pointer clicks into an input field, show a blinking text cursor:

```tsx
const blink = Math.floor((frame - TYPE_START) / 15) % 2 === 0 ? 1 : 0;
const charsTyped = Math.floor(
  interpolate(frame, [TYPE_START, TYPE_END], [0, fullText.length], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  })
);
const displayText = fullText.slice(0, charsTyped);

// Render:
// <span>{displayText}</span><span style={{ opacity: blink }}>|</span>
```

### Contextual Icon Animations

**Rule: icon = semantic choice first, animation = logical behavior second.**

Choose the icon that actually represents the feature. Then animate it based on what that icon naturally does:

| Icon type | Natural animation |
|-----------|------------------|
| Gear ⚙️ | `rotate(${frame * 2}deg)` — continuous spin |
| Location Pin 📍 | Spring drop: `translateY(-20→0)` + small bounce |
| Download ⬇️ | `translateY: 0→8→0` repeating every 20f (waterfall) |
| Check ✓ | Scale `0→1` spring on appear, then hold |
| Bell 🔔 | `rotate(${Math.sin(frame/5) * 15}deg)` — swing |
| Star ⭐ | Scale `1→1.2→1` pulse every 40f |

---

## Scene Transitions

### Duration Calculation (Most Common Bug)

```
durationInFrames = sum of ALL scene durations − sum of ALL transition durations

Example:
Scene durations:       130 + 165 + 265 + 250 + 450 + 140 + 110 = 1510
6 transitions × 20f:  120
Net total:             1510 − 120 = 1390

Root.tsx durationInFrames MUST exactly match this number.
Too small → video cuts off early.
Too large → blank frames at end.
```

### Option A — SureCart Setup *(Copy-paste ready)*

```tsx
import { TransitionSeries, linearTiming, springTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={130}>
    <SceneHook />
  </TransitionSeries.Sequence>

  {/* Mood shift → fade */}
  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 20 })}
  />

  <TransitionSeries.Sequence durationInFrames={165}>
    <SceneFeatureList />
  </TransitionSeries.Sequence>

  {/* Feature → feature → slide */}
  <TransitionSeries.Transition
    presentation={slide({ direction: "from-right" })}
    timing={springTiming({ config: { damping: 200 }, durationInFrames: 20 })}
  />

  <TransitionSeries.Sequence durationInFrames={265}>
    <SceneFeature1 />
  </TransitionSeries.Sequence>

  {/* Continue pattern... */}
</TransitionSeries>
```

### Transition Decision Rules

| Use | When |
|-----|------|
| `fade()` + `linearTiming` | Mood or energy shift (hook→content, features→recap, recap→CTA) |
| `slide(from-right)` | Forward progression (feature → next feature) |
| `slide(from-bottom)` | Going deeper into detail |
| `slide(from-left)` | Closing a loop / coming back around |
| Avoid `slide(from-top)` | Feels like something falling — unnatural |

**Critical rules:**
- Always `damping: 200` on slide springs — prevents overshoot and peek of previous scene
- Max transition duration: **20 frames**
- Always **15f hold** at end of outgoing scene before transition fires

---

## Audio Setup *(Optional — skip entirely if no music)*

```tsx
import { Audio } from "@remotion/media";
import { staticFile, interpolate } from "remotion";

const TOTAL_FRAMES = 1385; // must match your durationInFrames

<Audio
  src={staticFile("bg-music.mp3")}
  volume={(f) =>
    interpolate(
      f,
      [0, 30, TOTAL_FRAMES - 45, TOTAL_FRAMES],
      [0, 0.55, 0.55, 0],
      { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
    )
  }
  endAt={TOTAL_FRAMES}
/>
```

**Rules:**
- `volume` MUST be a callback `(f) => number` — a static `volume={0.5}` cannot fade in/out
- `endAt={TOTAL_FRAMES}` — always set this — prevents music bleeding past the last frame
- Peak volume sweet spot: `0.4–0.6` (won't drown voiceover or SFX)
- Fade in: 30f (1s). Fade out start: `TOTAL_FRAMES - 45` (1.5s before end)

---

## Credits

Skill built by **Chandresh Vaghanani**
Born from building the SureCart 4.2 launch video with Claude Code + Remotion 4.x
v1.2 — Pre-Layout Gates added (Canvas Fill Gate, Layout Selection Decision Table, Content Density Limit) from Power Coupons video production failures
