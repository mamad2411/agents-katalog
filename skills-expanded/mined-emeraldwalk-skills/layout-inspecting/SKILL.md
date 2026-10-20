---
name: layout-inspecting
description: Inspects the visual layout of a web page and returns a JSON tree of layout-relevant boxes — sections that stand out via background color or border color changes. Use when an agent needs to understand page structure, identify UI regions, verify layout, or describe what a page looks like without processing screenshots. Triggers on requests like "inspect the layout", "what does the page look like", "get the page structure", "analyze the UI layout", or "show me the visual regions of the page".
---

# Layout Inspecting

Runs a headless Playwright browser against a URL and walks the DOM to produce a compact JSON tree that mirrors what the human eye sees as distinct visual "boxes" — regions differentiated by background or border color changes.

## How It Works

- **Document** is the root node; its color is the page canvas background.
- A child node is included if its `background-color` or visible `border-*-color` differs from its parent's effective background.
- Nodes that are not visually distinct are skipped; their interesting descendants bubble up.
- Each node includes: `label`, `tag`, `rect` (x/y/width/height in px), `background`, optional `border`, optional `text` snippet, and nested `children`.

## Usage

Run `inspect_layout.js` using the skill's absolute path. No manual install needed — playwright and Chromium are downloaded automatically into the skill's own directory on first run.

```bash
node <path-to-skill>/scripts/inspect_layout.js <url> [options]
```

**Common options:**

| Flag | Default | Description |
|---|---|---|
| `--width <px>` | 1280 | Viewport width |
| `--height <px>` | 800 | Viewport height |
| `--full-page` | false | Capture full scrollable page, not just viewport |
| `--max-depth <n>` | 12 | Max DOM depth to recurse |
| `--min-size <px>` | 4 | Ignore elements smaller than this in both axes |
| `--timeout <ms>` | 30000 | Navigation timeout |
| `--output <file>` | stdout | Write JSON to a file |
| `--wait-for <sel>` | — | Wait for a CSS selector before inspecting |
| `--tui` | false | Launch interactive terminal UI showing a spatial wireframe |
| `--save-image <path>` | — | Save wireframe PNG/JPG image of the layout (e.g. `out.png`) |
| `--image-scale <factor>` | 0.25 | Scale factor relative to viewport size (e.g. 0.5 = 50%) |
| `--image-max-width <px>` | 1200 | Max image width; clamps output after scale is applied |
| `--image-max-height <px>` | 900 | Max image height; clamps output after scale is applied |

**Examples:**

```bash
# Inspect the viewport of a page
node <path-to-skill>/scripts/inspect_layout.js https://example.com

# Full-page capture, write to file
node <path-to-skill>/scripts/inspect_layout.js https://example.com --full-page --output layout.json

# Wait for app to render before inspecting
node <path-to-skill>/scripts/inspect_layout.js http://localhost:3000 --wait-for "#app"

# Narrow viewport (mobile simulation)
node <path-to-skill>/scripts/inspect_layout.js https://example.com --width 375 --height 812

# Launch interactive terminal wireframe UI (press q to quit)
node <path-to-skill>/scripts/inspect_layout.js https://example.com --tui

# Save a wireframe PNG image of the layout (default: 25% of viewport size)
node <path-to-skill>/scripts/inspect_layout.js https://example.com --save-image layout.png

# Save at 50% of viewport size
node <path-to-skill>/scripts/inspect_layout.js https://example.com --save-image layout.png --image-scale 0.5

# Save at 100% but capped at 800x600
node <path-to-skill>/scripts/inspect_layout.js https://example.com --save-image layout.png --image-scale 1.0 --image-max-width 800 --image-max-height 600

# Combine: write JSON, save image, and launch TUI in one run
node <path-to-skill>/scripts/inspect_layout.js https://example.com --output layout.json --save-image layout.png --tui
```

## Output Format

```json
{
  "url": "https://example.com",
  "viewport": { "width": 1280, "height": 800 },
  "fullPage": false,
  "capturedAt": "2025-01-01T00:00:00.000Z",
  "layout": {
    "label": "document",
    "tag": "document",
    "rect": { "x": 0, "y": 0, "width": 1280, "height": 800 },
    "background": "rgb(255,255,255)",
    "children": [
      {
        "label": "header#site-header",
        "tag": "header",
        "rect": { "x": 0, "y": 0, "width": 1280, "height": 64 },
        "background": "rgb(30,30,30)",
        "text": "My App  Home  About  Contact",
        "children": [...]
      },
      {
        "label": "main.content",
        "tag": "main",
        "rect": { "x": 0, "y": 64, "width": 1280, "height": 600 },
        "background": "rgb(245,245,245)",
        "border": "rgb(200,200,200)",
        "children": [...]
      }
    ]
  }
}
```

## Interpreting the Output

- **`rect`** gives position and size in CSS pixels, relative to the viewport top-left (or document top-left with `--full-page`).
- **`background`** is the resolved background color of that box.
- **`border`** appears only when a visible border with a color distinct from the parent background is present.
- **`text`** is a trimmed snippet of the element's visible text (≤80 chars).
- **`children`** contains nested interesting descendants within this box.
- Absence of `children` means no visually distinct sub-regions were found (the box is a leaf in the layout tree).

## Troubleshooting

| Problem | Fix |
|---|---|
| `npm install failed` | Ensure `node` and `npm` are on PATH |
| `playwright install chromium failed` | Check disk space; re-run the script to retry |
| Empty or sparse output | Try `--full-page`, reduce `--min-size`, or increase `--max-depth` |
| Page not fully rendered | Use `--wait-for <selector>` to wait for a key element |
| Timeout on slow pages | Increase `--timeout 60000` |
