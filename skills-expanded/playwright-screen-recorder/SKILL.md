---
name: playwright-screen-recorder
description: "Record browser UX flow and cinematic demos without vision model dependency"
version: 1.0.0
category: media
license: MIT
tags: [playwright, recording, browser, qa, demo]
requires:
  - "Node.js 18+"
  - "Playwright"
  - "ffmpeg"
tested: schema-only
tested_note: Frontmatter and docs validated; recorder not executed by this repo.
---

# Playwright Screen Recorder — No Vision Model Needed

Records browser interactions at 1440p/1280p with smooth cursor pacing. Two modes:
- **flow** — clicks through nav, tests every button/island (80ms slowMo)
- **cinema** — slow pans, hover pauses, theme toggles, hero shot (120ms slowMo)

Zero GPU vision requirement. Playwright drives Chromium internally.

## Dependencies

- `@playwright/test` installed in project
- Chromium browser (`npx playwright install chromium`)
- ffmpeg for format conversion

## Quick Start (Any Project)

```bash
cd <your-project>
npm install -D @playwright/test
npx playwright install chromium --with-deps
npm run dev &
sleep 5
RECORD_URL=http://localhost:3000 RECORD_OUTPUT=/tmp npx playwright test --project=flow
```

## Recording Spec File

Create `scripts/recording.spec.ts` and `playwright.config.ts` in the target project. Two modes:

**flow** — Clicks through sidebar nav, hovers cards, tests buttons, toggles theme:
- Viewport: 1280x800
- slowMo: 80ms
- Runtime: ~21s

**cinema** — Slow scrolls, dramatic pauses, hover linger:
- Viewport: 1440x900
- slowMo: 120ms
- Runtime: ~29s

## Output Conversion

```bash
# WebM to MP4 (for X/Twitter, WhatsApp)
ffmpeg -i /tmp/video.webm -vcodec libx264 -crf 20 -preset fast \
  -vf "scale=1280:-2" -movflags +faststart /tmp/demo.mp4

# WebM to GIF (for GitHub README, Discord inline)
ffmpeg -i /tmp/video.webm \
  -vf "fps=24,scale=1280:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer" \
  -loop 0 /tmp/demo.gif
```

## Wiki-LLM Vault Integration

All QA assets live in `labs/<project>/media/` inside the wiki-llm vault:

```
labs/<project>/
├── .md                     # Project brief (title, type, status, tags, tools)
├── QA-Visual-Assets.md     # Media inventory table + QA checklist results
└── media/
    ├── videos/             # MP4 recordings (flow + cinema)
    ├── screenshots/        # PNG captures at breakpoints
    └── gifs/               # Optimized GIFs for README/Discord
```

After recording, copy to wiki-llm and create the QA doc:

```bash
PROJECT="<name>"
BASE="$HOME/projects/wiki-llm/labs/$PROJECT"
mkdir -p "$BASE/media"/{videos,screenshots,gifs}
cp /tmp/qa-*.png "$BASE/media/screenshots/"
cp /tmp/*-flow.mp4 "$BASE/media/videos/"
cp /tmp/*-cinema.mp4 "$BASE/media/videos/"
cp /tmp/*.gif "$BASE/media/gifs/"
```

Then create `$BASE/QA-Visual-Assets.md` with:
- Media inventory table (file, size, description)
- QA checklist results per breakpoint
- Recording method summary

## Hybrid Manual Capture (Kap)

For quick non-automated captures, Kap is available:
```bash
brew install --cask kap
# Open Kap.app, select region, record, export as GIF/MP4/WebM
```

Use Kap when: ad-hoc bug capture, quick share, no automation needed.
Use Playwright when: full UX flow, CI pipeline, reproducible QA sequence.

## Configuration

- `RECORD_URL` — target URL (default: http://localhost:3000)
- `RECORD_OUTPUT` — save directory (default: /tmp)

## Pitfalls

- Dev server MUST be running before test starts
- `screencapture` needs Screen Recording permission; Playwright bypasses this entirely
- Flow script assumes standard button aria-labels — customize selectors per project
- Default timeout 120s; increase in playwright.config.ts for longer demos
- GitHub doesn't autoplay GIFs in README preview; use mp4 for social posts
- Wiki-llm media folder uses labs/ for experimental/creative projects per vault conventions
