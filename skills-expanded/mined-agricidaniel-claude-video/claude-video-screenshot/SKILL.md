---
name: claude-video-screenshot
description: >
  Web screenshot capture for video production using Playwright. Takes full-page, viewport,
  or element-specific screenshots at video-native dimensions (1920x1080, 1080x1920).
  Device emulation (100+ presets), CSS injection to hide ads/banners, authentication
  persistence, Ken Burns zoom/pan animation from screenshots, browser session recording,
  and batch URL capture. Use when user says "screenshot", "web capture", "capture website",
  "screenshot for video", "web to image", "record browser", "ken burns", "web recording",
  "page capture", or "capture URL".
allowed-tools:
  - Bash
  - Read
  - Write
---

# claude-video-screenshot — Web Capture for Video Production

## Pre-Flight

Check Playwright is installed:
```bash
source ~/.video-skill/bin/activate
python3 -c "from playwright.sync_api import sync_playwright; print('Playwright ready')"
```

If not installed:
```bash
source ~/.video-skill/bin/activate
pip install playwright && playwright install --with-deps chromium
```

## Single Screenshot

Capture a web page at video-native dimensions:

```bash
source ~/.video-skill/bin/activate
python3 scripts/web_capture.py \
  --url "https://example.com" \
  --output capture.png \
  --viewport 1920x1080
```

**Options:**
- `--url "..."` — URL to capture
- `--output capture.png` — Output file path
- `--viewport WxH` — Browser viewport size (default: 1920x1080)
- `--full-page` — Capture entire scrollable page (not just viewport)
- `--element ".css-selector"` — Capture a specific element only
- `--transparent` — Transparent background (omit page background)
- `--hide ".ads,.cookie-banner,.popup"` — CSS selectors to hide via `display:none`
- `--wait N` — Wait N seconds after page load before capture
- `--wait-for ".selector"` — Wait for a specific element to appear
- `--device "iPhone 15 Pro"` — Emulate a device (100+ presets)
- `--dark-mode` — Emulate dark color scheme preference
- `--locale en-US` — Set browser locale
- `--timezone "America/New_York"` — Set browser timezone

## Video-Native Presets

Use `--preset` for common video dimensions:

| Preset | Viewport | Use Case |
|--------|----------|----------|
| `--preset landscape` | 1920x1080 | 16:9 YouTube/LinkedIn |
| `--preset portrait` | 1080x1920 | 9:16 TikTok/Reels/Shorts |
| `--preset square` | 1080x1080 | 1:1 Instagram |
| `--preset instagram` | 1080x1350 | 4:5 Instagram portrait |
| `--preset 4k` | 3840x2160 | 4K landscape |

## Batch Capture

Capture multiple URLs at once:

```bash
source ~/.video-skill/bin/activate
python3 scripts/web_capture.py \
  --urls urls.txt \
  --output-dir ./captures/ \
  --viewport 1920x1080 \
  --hide ".cookie-banner"
```

The `urls.txt` file contains one URL per line. Output files are named after the URL slug.

## Browser Recording

Record a browser session as video:

```bash
source ~/.video-skill/bin/activate
python3 scripts/web_capture.py \
  --record \
  --url "https://example.com" \
  --output recording.mp4 \
  --viewport 1920x1080 \
  --duration 10
```

Uses Playwright's `record_video_dir` to capture the browser session. Useful for tutorial videos or documenting web interactions.

**Options:**
- `--record` — Enable video recording mode
- `--duration N` — Recording duration in seconds
- `--scroll` — Auto-scroll the page during recording
- `--scroll-speed N` — Pixels per second for auto-scroll (default: 200)

## Ken Burns Animation

Convert a screenshot into a zoom/pan video:

```bash
source ~/.video-skill/bin/activate
python3 scripts/web_capture.py \
  --url "https://example.com" \
  --output capture.png \
  --viewport 1920x1080 \
  --ken-burns \
  --ken-burns-duration 5
```

Or apply Ken Burns to an existing image:

```bash
python3 scripts/web_capture.py \
  --ken-burns-image existing.png \
  --ken-burns-duration 5 \
  --ken-burns-direction zoom-in \
  --output kenburns.mp4
```

**Ken Burns options:**
- `--ken-burns` — Auto-create Ken Burns video after screenshot
- `--ken-burns-image FILE` — Apply Ken Burns to existing image
- `--ken-burns-duration N` — Animation duration in seconds (default: 5)
- `--ken-burns-direction zoom-in|zoom-out|pan-left|pan-right` — Animation direction

**FFmpeg command used internally:**
```bash
ffmpeg -loop 1 -framerate 60 -i capture.png \
  -vf "scale=8000:-1,zoompan=z='zoom+0.001':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=DURATION*60:s=1920x1080:fps=60" \
  -t DURATION -c:v libx264 -pix_fmt yuv420p kenburns.mp4
```

## Device Emulation

Common device presets (Playwright has 100+):

| Device | Resolution | User Agent |
|--------|-----------|------------|
| iPhone 15 Pro | 393x852 | Mobile Safari |
| iPhone 15 Pro Max | 430x932 | Mobile Safari |
| Pixel 7 | 412x915 | Mobile Chrome |
| iPad Pro 11 | 834x1194 | Mobile Safari |
| Galaxy S21 | 360x800 | Mobile Chrome |

```bash
python3 scripts/web_capture.py --url "..." --device "iPhone 15 Pro" --output mobile.png
```

## CSS Injection

Hide unwanted elements before capture:

```bash
python3 scripts/web_capture.py --url "..." --hide ".ads,.cookie-banner,.popup,.newsletter-modal" --output clean.png
```

For custom CSS injection:
```bash
python3 scripts/web_capture.py --url "..." --inject-css "body { font-size: 24px !important; }" --output styled.png
```

## Integration with Video Workflow

Screenshots can be used as:
- **Overlay** on video via edit sub-skill PiP overlay
- **Slideshow** source — capture multiple URLs, concatenate as slideshow with transitions
- **Ken Burns** source — zoom/pan animation from static capture
- **Tutorial B-roll** — browser recording for product demos
- **Thumbnail** background — screenshot + text overlay

## Safety Rules

1. Run `bash scripts/preflight.sh` for output path validation
2. Respect robots.txt and site terms of service
3. Do not capture login pages or authenticated content without user consent
4. Clean up temporary browser recording files

## Reference

Load `references/web-capture.md` for Playwright API details, device presets, and FFmpeg Ken Burns formulas.
