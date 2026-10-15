---
name: vision-click
description: "Vision-based coordinate click: screenshot → Codex CLI (NDJSON) → DPR correction → mouse click. Codex CLI only. Triggers: vision click, 비전 클릭, coordinate click, 좌표 클릭, screenshot click, non-DOM click, agbrowse-vision-click. NOT for: regular DOM clicks (use browser skill), desktop app clicks (use computer-use)."
---

# Vision Click (Codex CLI)

Click non-DOM elements by screenshot analysis using Codex CLI.

## Quick Start

```bash
agbrowse-vision-click "Submit button"
agbrowse-vision-click "Play icon" --double
agbrowse-vision-click "first result row" --prepare-stable --region left-panel --verify-before-click
agbrowse-vision-click "Menu" --viewport 1280x800
```

## Prerequisites

- **agbrowse** running Chrome (`agbrowse start`)
- **Codex CLI** installed (`npm install -g @openai/codex`)

## When to Use

Use when `agbrowse snapshot` returns **NO ref** for target:
- Canvas elements, cross-origin iframes, Shadow DOM
- Dynamically rendered content (WebGL, SVG)
- Elements behind overlays or custom web components

> **Always try `snapshot --interactive` first.** Only fall back to vision-click if no usable ref exists.

## Pipeline

```
1. agbrowse snapshot --interactive  → Check if target has a ref ID
2. If ref exists → agbrowse click <ref>  (normal path, preferred)
3. If NO ref → vision-click fallback:
   a. agbrowse screenshot --json     → { path, dpr, viewport }
   b. optional --prepare-stable resize (default 1440x900) or --clip / --region crop
   c. codex exec -i <path> --json       → NDJSON events → vision bbox candidate
   d. optional verify crop (--verify-before-click or auto for low-confidence/point-only)
   e. DPR correction + clip origin      → CSS pixels
   f. agbrowse mouse-click <x> <y>   → click
   g. agbrowse snapshot --interactive → verify
```

## How It Works

`codex exec --json` emits NDJSON (newline-delimited JSON) events:

```jsonl
{"type":"thread.started","thread_id":"..."}
{"type":"turn.started"}
{"type":"item.completed","item":{"type":"agent_message","text":"{\"found\":true,\"bbox\":{\"x\":500,\"y\":70,\"width\":44,\"height\":24},\"point\":{\"x\":522,\"y\":82},\"confidence\":0.88,\"description\":\"search button\"}"}}
{"type":"turn.completed","usage":{"input_tokens":16964,"output_tokens":542}}
```

The vision candidate JSON is extracted from the `item.completed` event's `item.text` (or `item.aggregated_output`) field. Legacy `{found,x,y}` point-only JSON is still parsed, but it is normalized to `kind: "coordinate"` with a `point_only` risk flag and default confidence 0.5, requiring verification before click.

## Flags

| Flag | Description |
| --- | --- |
| `--double` | Double-click instead of single click |
| `--port <N>` | CDP port (default: 9222) |
| `--browser-script <path>` | Path to browser.mjs |
| `--prepare-stable` | Resize to a stable desktop viewport (default 1440x900) before capture |
| `--viewport <WxH>` | Custom viewport size, e.g. `1280x800` (resizes before capture) |
| `--region <name>` | Named crop region: `left-panel`, `center-map`, `top-bar` |
| `--clip <x y w h>` | Manual crop rectangle in CSS pixels |
| `--bundle <path>` | ObservationBundle JSON from `observe-bundle --json` for ref reconciliation |
| `--verify-before-click` | Re-check with a zoomed verification crop before clicking |
| `--help`, `-h` | Print usage and exit |

## Examples

```bash
# Basic click
agbrowse-vision-click "Login button"

# Double-click
agbrowse-vision-click "Canvas play icon" --double

# Custom CDP port
agbrowse-vision-click "Submit" --port 9333

# Custom browser.mjs path
agbrowse-vision-click "Menu" --browser-script /path/to/browser.mjs

# Resize to stable desktop viewport (default 1440x900) before capture
agbrowse-vision-click "first result row" --prepare-stable --region left-panel --verify-before-click

# Custom viewport size
agbrowse-vision-click "first result row" --viewport 1280x800

# Reconcile a vision bbox against refs from observe-bundle
agbrowse observe-bundle --screenshot --boxes --json > /tmp/bundle.json
agbrowse-vision-click "Submit button" --bundle /tmp/bundle.json --verify-before-click

# Manual clip when you know the rough area
agbrowse-vision-click "zoom button" --clip 980 120 220 220
```

## Environment Variables

| Variable           | Default                  | Description          |
| ------------------ | ------------------------ | -------------------- |
| `BROWSER_SCRIPT`   | `../browser/browser.mjs` | Path to browser.mjs  |
| `CDP_PORT`         | `9222`                   | Chrome CDP port      |

## Exit Codes

| Code | Meaning |
| --- | --- |
| `0` | Click succeeded (or `--help` printed) |
| `1` | Target not found, low-confidence rejection, verification failure, or any thrown error |

## Accuracy Tips

- Start with `--prepare-stable` to normalize the viewport before capture.
- Use `--region left-panel` for search result panels and `--region center-map` for map canvas targets.
- Use `--verify-before-click` on dense UIs where a wrong click is expensive.
- If you already know the rough target area, `--clip x y w h` is more reliable than full-screen analysis.
- Candidates below confidence `0.75` fail closed unless `--verify-before-click` is passed. Point-only candidates (no bbox) and low-confidence candidates with confidence >= 0.5 are auto-verified when `--verify-before-click` is set.
- When `--bundle` is provided, reconciliation may upgrade to a ref click or fail with `COMPUTER_TARGET_AMBIGUOUS` if the candidate is ambiguous.
- Prefer `agbrowse click <ref>` whenever `snapshot --interactive` exposes a usable ref; coordinate click remains the last fallback.

## DPR (Device Pixel Ratio) Correction

Retina displays (DPR=2) produce screenshots at 2x resolution.
Codex returns coordinates in image pixel space.
`vision-click` auto-divides by DPR before passing to `mouse-click`.

```
raw: (600, 200)  DPR=2  →  css: (300, 100)  →  mouse-click 300 100
```

When a clip region is used, clip origin is added back after DPR division:
```
raw: (100, 50)  DPR=2  clip=(400, 200, ...)  →  css: (450, 225)
```

## Limitations

- Requires codex CLI (GPT vision) — no other providers
- Latency: 3-10 seconds per call (model inference)
- English target descriptions work best; Korean can fail on some elements
- Complex dense UIs may need `--region`, `--clip`, or `--verify-before-click`
- Known `--region` names are `left-panel`, `center-map`, `top-bar`; unknown names throw an error during clip resolution
