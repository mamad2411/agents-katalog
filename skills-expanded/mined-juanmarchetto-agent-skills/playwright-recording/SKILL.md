---
name: playwright-recording
description: "Record browser interactions as video using Playwright. Capture demo videos, app walkthroughs, and UI flows. Includes cursor highlighting, click ripple effects, cookie banner dismissal, and window scaling patterns. Use when: record demo, capture browser video, screen recording, walkthrough footage."
license: MIT
metadata:
  version: 1.0.0
  category: toolchain
  tags: [playwright, recording, video, demo, browser, walkthrough, screen-capture]
---

# Playwright Video Recording

Record browser interactions as video using Playwright — quick capture of demos, walkthroughs, and UI flows during development.

## When to Use This vs Other Recording Skills

| Need | Use |
|------|-----|
| Scripted demos with cursor animation, overlays, themes | webreel |
| Quick browser capture during development | **playwright-recording** (this skill) |
| Natural language -> automated recording pipeline | demo-pipeline |
| Live browser interaction with element refs | agent-browser |

Use this skill when you need a fast, scriptable way to capture browser video without the overhead of a full production pipeline. Write a TypeScript script, run it, get a `.webm` file.

## Workflow

### Step 1: Setup
```bash
npm init -y
npm install -D playwright @playwright/test
npx playwright install chromium
```

### Step 2: Write Recording Script
Create a TypeScript file that launches a browser context with video recording enabled:

```typescript
import { chromium } from 'playwright';

async function record() {
  const browser = await chromium.launch({ slowMo: 50 });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    recordVideo: {
      dir: './recordings',
      size: { width: 1920, height: 1080 }
    }
  });

  const page = await context.newPage();

  // Recording actions
  await page.goto('https://example.com');
  await page.waitForTimeout(2000);
  await page.click('button.demo');
  await page.waitForTimeout(3000);

  // Close to save video
  await context.close();
  await browser.close();
  console.log('Recording saved to ./recordings/');
}

record();
```

### Step 3: Run
```bash
npx tsx scripts/record-demo.ts
```

### Step 4: Convert (optional)
Playwright outputs WebM. Convert to MP4 if needed:
```bash
ffmpeg -i recording.webm -c:v libx264 -crf 20 -preset medium -movflags faststart output.mp4
```

## Recording Patterns

### Viewport Sizes
```typescript
// Standard 1080p (recommended)
viewport: { width: 1920, height: 1080 }

// 720p (smaller files)
viewport: { width: 1280, height: 720 }

// Square (social media)
viewport: { width: 1080, height: 1080 }

// Mobile
viewport: { width: 390, height: 844 } // iPhone 14
```

### Cursor Highlighting
Playwright does not show a cursor by default. Inject one:

```typescript
await page.addStyleTag({
  content: `
    * { cursor: none !important; }
    .playwright-cursor {
      position: fixed;
      width: 24px; height: 24px;
      background: rgba(255, 100, 100, 0.5);
      border: 2px solid rgba(255, 50, 50, 0.8);
      border-radius: 50%;
      pointer-events: none;
      z-index: 999999;
      transform: translate(-50%, -50%);
      transition: transform 0.1s ease;
    }
    .playwright-cursor.clicking {
      transform: translate(-50%, -50%) scale(0.8);
      background: rgba(255, 50, 50, 0.8);
    }
  `
});

await page.evaluate(() => {
  const cursor = document.createElement('div');
  cursor.className = 'playwright-cursor';
  document.body.appendChild(cursor);
  document.addEventListener('mousemove', (e) => {
    cursor.style.left = e.clientX + 'px';
    cursor.style.top = e.clientY + 'px';
  });
  document.addEventListener('mousedown', () => cursor.classList.add('clicking'));
  document.addEventListener('mouseup', () => cursor.classList.remove('clicking'));
});
```

**Note:** Injected DOM elements appear in the video. Re-inject after navigation since they reset on page load.

### Cookie Banner Dismissal
```typescript
const COOKIE_SELECTORS = [
  '#onetrust-accept-btn-handler',
  '#CybotCookiebotDialogBodyButtonAccept',
  '.cc-btn.cc-dismiss',
  '[class*="cookie"] button[class*="accept"]',
  'button:has-text("Accept all")',
  'button:has-text("Got it")',
];

async function dismissCookieBanners(page) {
  await page.waitForTimeout(500);
  for (const selector of COOKIE_SELECTORS) {
    try {
      const btn = page.locator(selector).first();
      if (await btn.isVisible({ timeout: 100 })) {
        await btn.click({ timeout: 500 });
        return;
      }
    } catch { /* try next */ }
  }
}
```

### Window Scaling for Laptops
Record at full 1080p while showing a smaller window:
```typescript
const scale = 0.75;
const context = await browser.newContext({
  viewport: { width: 1920 * scale, height: 1080 * scale },
  deviceScaleFactor: 1 / scale,
  recordVideo: { dir: './recordings', size: { width: 1920, height: 1080 } },
});
```

## Example Output

Running a recording script produces:
```
$ npx tsx scripts/record-homepage.ts
Starting recording: homepage-walkthrough
Navigating to https://myapp.com ...
Clicking "Get Started" ...
Filling demo form ...
Submitting ...
Recording saved: ./recordings/abc123def456.webm (14.2s, 1920x1080, 8.3MB)

Convert to MP4:
ffmpeg -i ./recordings/abc123def456.webm -c:v libx264 -crf 20 -movflags faststart ./recordings/homepage-walkthrough.mp4
```

The output is a `.webm` video file in the configured directory. The filename is auto-generated by Playwright — rename or move it in your script using `page.video()?.saveAs('desired-name.webm')`.

## Tips
1. **Use slowMo** — 50-100ms makes actions visible to viewers
2. **Add waitForTimeout** — pause between actions for comprehension
3. **Wait for animations** — use `waitForLoadState('networkidle')`
4. **Test without recording first** — debug before final capture
5. **Clear browser state** — use fresh context for clean demos
6. **Use headless: false** for debugging, headless: true for final capture

## Error Handling
- **Chromium not installed:** Run `npx playwright install chromium`. If on CI, add to setup step.
- **Video codec issues:** Playwright outputs VP8 in WebM. If your player can't handle it, convert with `ffmpeg -i input.webm -c:v libx264 output.mp4`.
- **Black/empty video:** Ensure `context.close()` is called before `browser.close()` — the video is finalized on context close.
- **Recording too large:** Reduce viewport size or use shorter `waitForTimeout` durations.
- **Injected elements lost after navigation:** Re-inject cursor/overlays in a `page.on('load')` handler.
- **Permission denied on Linux:** Playwright may need `--no-sandbox` flag: `chromium.launch({ args: ['--no-sandbox'] })`.

## Structure

```
playwright-recording/
├── SKILL.md           # This file
└── reference.md       # Full API reference, selectors, timing utilities
```
