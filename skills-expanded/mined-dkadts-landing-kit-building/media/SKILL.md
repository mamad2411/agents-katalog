---
name: media
description: Media pipeline. Takes files from inbox/media/, converts photos to WebP/AVIF with size variants (srcset), videos to WebM+MP4 with posters. Lands them in site/media/.
---

# /media

Solves the assets-optimization bottleneck (usually done twice in a naive workflow).

## When to use

- After `/inbox` (materials validated).
- Every time a new batch of media arrives.

## Requirements

- Tools available: `ffmpeg` (for video + posters), `cwebp` / `avifenc` / `sharp` (for photos).
- On Windows the simplest path: node.js + `sharp` (`npm install -g sharp-cli`) + `ffmpeg`.
- If tools are missing — inform the user, provide install commands.

## Process

**Step 1. Read config**
- `brief/00-priority.md` — desktop-first or mobile-first (affects priority sizes).
- `brief/06-technical.md` — media hosting decision (local / Vercel / R2).
- `brief/blocks/video-embed.md` — hero-loop needed? formats?

**Step 2. Walk inbox/media/photos/**

For each photo:

**A. Determine purpose**
- From filename / `brief/04-content.md`.
- Hero — priority, LCP-critical.
- Portrait / case — standard.
- Icon-size (small) — optimize differently.

**B. Generate size variants**

For desktop-first:
- 480w, 768w, 1200w, 1920w, 2400w.

For mobile-first:
- 320w, 480w, 768w, 1200w, 1920w.

**C. Convert to formats**
- `.webp` (required, quality ~80-85).
- `.avif` (optional, quality ~60-70 — better compression).
- Original `.jpg` fallback — only if old-browser support needed (usually not).

**D. Save in `site/media/`**
Naming: `<name>-<width>.webp`

Example:
```
site/media/
├── hero-480.webp
├── hero-768.webp
├── hero-1200.webp
├── hero-1920.webp
└── hero-2400.webp
```

**E. Generate `srcset`-snippet for this file**
Save to `site/media/_srcset-snippets.md` for use in `/build`:
```html
<img src="/media/hero-1200.webp"
     srcset="/media/hero-480.webp 480w,
             /media/hero-768.webp 768w,
             /media/hero-1200.webp 1200w,
             /media/hero-1920.webp 1920w,
             /media/hero-2400.webp 2400w"
     sizes="(max-width: 768px) 100vw, 60vw"
     alt="TBD"
     loading="lazy" decoding="async">
```

**Step 3. Walk inbox/media/videos/**

For each video:

**A. Format**
- `.webm` (VP9, main) — required.
- `.mp4` (H.264, fallback) — required.

**B. Optimization**
- Bitrate: 2-4 Mbps for 1080p hero-loop (no more).
- Muted, no audio track for hero-loop (rule).
- Cut to 30s if longer (except case videos).

**C. Poster (first frame in WebP)**
```
ffmpeg -i video.mp4 -vframes 1 -f image2 - | cwebp - -o video-poster.webp
```

**D. Naming**
```
site/media/videos/
├── hero-loop.webm
├── hero-loop.mp4
└── hero-loop-poster.webp
```

**Step 4. Walk brand/logo/**

Copy SVGs into `site/media/`:
- `logo.svg`
- `logo-white.svg`
- `logo-mark.svg` (for mobile-header and favicon fallback).

Verify: SVGs are clean (no embedded raster, text outlined).

**Step 5. Favicon**

From `brand/logo/logo-mark.svg`:
- `site/media/favicon.svg` (main, SVG).
- `site/media/apple-touch-icon.png` (180×180, PNG for iOS).
- `site/media/favicon-32.png` (fallback for old browsers).

**Step 6. OG-image**

Check for `inbox/media/og-image.png` (1200×630).
If missing — warn the user, needed for social preview. Offer to generate from hero + logo overlay.

**Step 7. Report**

`site/media/_media-report.md`:
```markdown
# Media pipeline report — 2026-08-08

## Photos
- hero: 5 sizes × webp + avif = 10 files (total 480 KB)
- founder: 3 sizes × webp = 3 files (180 KB)
...

## Videos
- hero-loop: webm 1.2 MB, mp4 1.8 MB, poster 40 KB

## Total
- Before: 45 MB (raw)
- After: 3.2 MB (-93%)

## Next
- srcset-snippets ready in _srcset-snippets.md — use in /build
- OG-image missing — 1200×630 required
```

## Rules

- **Do not redo what's already done.** If a file is already in site/media/ and the inbox-file hash is unchanged — skip. (Hashes in `site/media/_hashes.json`.)
- **Verify after each conversion.** `identify hero-1200.webp` — matches size?
- **Do not crop beyond need.** Preserve alpha in PNG for logo. Do not change aspect.
- **No backup needed.** Originals stay in inbox/, we do not write there.

## What NOT to do

- Do not delete files from inbox/.
- Do not pull in anything not in brief (e.g. default stock icons).
- Do not change colors/crop/retouch — that's not `/media`, that's a designer's task.

## Next

- `/icons` — hybrid icon set.
- `/build` — uses size variants via srcset.
- `/audit` — verifies all photos use optimized formats.
