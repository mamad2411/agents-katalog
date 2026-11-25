---
name: webreel
description: "Create and record scripted browser demo videos with webreel. Generates MP4, GIF, or WebM recordings with cursor animation, keystroke overlays, and sound effects from a JSON config. Use when: record a demo, create a browser video, edit a webreel config, generate a screen recording, preview a demo, product video, marketing video, record website, work with webreel in any way."
license: MIT
metadata:
  version: 1.0.0
  category: video
  tags: [demo, recording, video, browser, mp4, gif, cursor-animation]
---

# webreel

webreel records scripted browser demos as MP4, GIF, or WebM with cursor animation, keystroke overlays, and sound effects. You define steps in a JSON config, and webreel drives headless Chrome, captures frames, and encodes with ffmpeg.

## Installation

Install webreel as a project dependency so the version is pinned in the lockfile. This ensures deterministic recordings across machines and CI.

```bash
npm install webreel
```

If the project already has webreel in its dependencies, skip this step.

## Prerequisites

webreel requires Chrome and ffmpeg, but you do NOT need to install them manually. Both are automatically downloaded to `~/.webreel` on first run if not already present. Do not install Chrome or Chromium via puppeteer, playwright, or any other tool. webreel manages its own browser.

To download dependencies explicitly, or to fix corrupted/broken binaries:

```bash
npx webreel install
npx webreel install --force   # delete cached binaries and re-download
```

To override the auto-downloaded binaries, set these environment variables:

- `CHROME_PATH` - path to a Chrome or Chromium binary (used for preview)
- `CHROME_HEADLESS_PATH` - path to a chrome-headless-shell binary (used for recording)
- `FFMPEG_PATH` - path to an ffmpeg binary

If a recording fails with "No inspectable targets" or similar browser errors, the issue is almost certainly in the webreel config (wrong `waitFor`, missing element, timing), not a missing browser. Check the config and use `--verbose` to debug.

## .gitignore

The `.webreel` directory is created at the project root during recording (frames, intermediate files). Add it to `.gitignore`:

```
.webreel
```

## Quick start

```bash
# Scaffold a config
npx webreel init --name my-demo --url https://example.com

# Edit webreel.config.json with your steps

# Preview in a visible browser (no recording)
npx webreel preview my-demo

# Record the video
npx webreel record my-demo
```

`npx` resolves to the locally installed version when webreel is in `devDependencies`. Output lands in `videos/` by default (configurable via `outDir`).

## Agent Workflow

When the user asks to record a demo, follow these steps:

1. **Check for config** — look for `webreel.config.json` (or `.ts`/`.js` variants) in the project root
2. **Initialize if missing** — if no config exists, run `npx webreel init --name <name> --url <url>` to scaffold one
3. **Edit config with steps** — add steps to the `videos` map based on what the user wants to demonstrate (clicks, typing, navigation, etc.)
4. **Preview first** — run `npx webreel preview <name>` to verify steps work in a visible browser before recording
5. **Record** — run `npx webreel record <name>` to produce the final video
6. **Iterate** — if the user wants to adjust timing, theme, or overlays, edit the config and use `npx webreel composite <name>` to re-apply overlays without re-recording

If the user provides a URL but no specific steps, suggest a sensible default flow: navigate to the page, wait for load, scroll down slowly, highlight key UI elements with clicks or hovers.

## When to Use webreel vs Other Tools

| Tool | Best For | Key Difference |
|------|----------|----------------|
| **webreel** | Scripted demos with polish (cursor animation, keystroke overlays, sound effects) | Deterministic, config-driven, produces production-quality video |
| **Playwright recording** | Quick screen captures for bug reports or docs | Fast but no cursor animation, no overlays, no post-processing |
| **demo-pipeline** | Natural language to automated demo | Higher-level abstraction, less control over individual steps |
| **Agent browser (Playwright MCP)** | Live interaction and testing | Real-time browsing, not optimized for video output |

**Choose webreel when:** the output needs to look polished (marketing, onboarding, product demos, social media), steps are known in advance, and you want repeatable recordings.

## CLI commands

### init

Scaffold a new `webreel.config.json`.

```bash
webreel init
webreel init --name login-flow --url https://myapp.com
webreel init --name hero -o hero.config.json
```

Flags: `--name` (video name), `--url` (starting URL), `-o, --output` (output file path).

### record

Record one or more videos.

```bash
webreel record                        # all videos in config
webreel record hero login             # specific videos by name
webreel record -c custom.config.json  # custom config path
webreel record --watch                # re-record on config change
webreel record --verbose              # log each step
webreel record --dry-run              # print resolved config only
webreel record --frames               # save raw JPEGs to .webreel/frames/
```

### preview

Run steps in a visible browser without recording.

```bash
webreel preview
webreel preview hero --verbose
```

### composite

Re-apply overlays (cursor, HUD, sfx) to existing raw video without re-recording. Useful for tweaking theme settings.

```bash
webreel composite
webreel composite hero
```

### install

Download Chrome and ffmpeg to `~/.webreel`. Also use this to fix corrupted or broken binaries.

```bash
webreel install
webreel install --force  # delete cached binaries and re-download
```

### validate

Check config for errors without running anything.

```bash
webreel validate
webreel validate -c custom.config.json
```

## Config structure

Config files are auto-discovered as `webreel.config.json` (or `.ts`, `.mts`, `.js`, `.mjs`). Use `-c` to specify a custom path.

### Top-level fields

| Field          | Default     | Description                                      |
| -------------- | ----------- | ------------------------------------------------ |
| `$schema`      | -           | `"https://webreel.dev/schema/v1.json"`           |
| `outDir`       | `"videos/"` | Output directory for rendered videos             |
| `baseUrl`      | `""`        | Base URL prepended to relative video URLs        |
| `viewport`     | `1080x1080` | Default viewport `{ width, height }`             |
| `theme`        | -           | Cursor and HUD overlay theme                     |
| `sfx`          | -           | Sound effect settings                            |
| `include`      | -           | Array of step file paths prepended to all videos |
| `defaultDelay` | -           | Default delay (ms) appended after each step      |
| `clickDwell`   | -           | Cursor dwell time (ms) before a click            |

### Per-video fields

Each entry in the `videos` map supports:

| Field          | Default        | Description                                        |
| -------------- | -------------- | -------------------------------------------------- |
| `url`          | required       | URL to open (absolute or relative to `baseUrl`)    |
| `viewport`     | inherited      | Override viewport `{ width, height }`              |
| `zoom`         | -              | CSS zoom factor                                    |
| `waitFor`      | -              | Selector or text to wait for before starting steps |
| `output`       | `"<name>.mp4"` | Output path (`.mp4`, `.gif`, `.webm`)              |
| `thumbnail`    | `{ time: 0 }`  | Thumbnail config, or `{ enabled: false }`          |
| `include`      | inherited      | Step files to prepend                              |
| `theme`        | inherited      | Override theme                                     |
| `sfx`          | inherited      | Override sound effects                             |
| `defaultDelay` | inherited      | Override default delay                             |
| `clickDwell`   | inherited      | Override click dwell                               |
| `fps`          | `60`           | Frame rate                                         |
| `quality`      | `80`           | Encoding quality (1-100)                           |
| `steps`        | required       | Array of step objects                              |

### Videos map

Videos are keyed by name in the config:

```json
{
  "videos": {
    "hero": { "url": "...", "steps": [...] },
    "login": { "url": "...", "steps": [...] }
  }
}
```

Record specific videos by name: `webreel record hero login`.

## Step types

Each step has an `action` field. Most steps accept optional `label`, `delay` (ms after step), and `description` fields.

| Action       | Key fields                                  | Purpose                            |
| ------------ | ------------------------------------------- | ---------------------------------- |
| `pause`      | `ms`                                        | Wait for a duration                |
| `click`      | `text` or `selector`, `within`, `modifiers` | Click an element                   |
| `type`       | `text`, `selector`, `within`, `charDelay`   | Type text into an input            |
| `key`        | `key`, `target`                             | Press a key combo (e.g. `"cmd+s"`) |
| `drag`       | `from`, `to` (element targets)              | Drag between two elements          |
| `scroll`     | `x`, `y`, `selector`                        | Scroll the page or an element      |
| `wait`       | `selector` or `text`, `timeout`             | Wait for an element to appear      |
| `moveTo`     | `text` or `selector`, `within`              | Move cursor to an element          |
| `navigate`   | `url`                                       | Navigate to a new URL              |
| `hover`      | `text` or `selector`, `within`              | Hover over an element              |
| `select`     | `selector`, `value`                         | Select a dropdown value            |
| `screenshot` | `output`                                    | Capture a PNG screenshot           |

For full field details on every step type, see [steps-reference.md](steps-reference.md).

## Element targeting

Many steps target elements using these fields:

- `text` - match by visible text content
- `selector` - match by CSS selector
- `within` - narrow the search to a parent matching this CSS selector

You can use `text` or `selector` (not both). `within` is optional and scopes the search.

```json
{ "action": "click", "text": "Submit" }
{ "action": "click", "selector": "#submit-btn" }
{ "action": "click", "text": "Submit", "within": ".modal" }
```

## Viewport presets

Use preset names as string values for `viewport`, or specify `{ width, height }`:

`desktop` (1920x1080), `desktop-hd` (2560x1440), `laptop` (1366x768), `macbook-air` (1440x900), `macbook-pro` (1512x982), `ipad` (1024x1366), `ipad-pro` (834x1194), `ipad-mini` (768x1024), `iphone-15` (393x852), `iphone-15-pro-max` (430x932), `iphone-se` (375x667), `pixel-8` (412x915), `galaxy-s24` (360x780).

## Theme

Customize cursor appearance and keystroke HUD:

```json
{
  "theme": {
    "cursor": {
      "image": "./cursor.svg",
      "size": 32,
      "hotspot": "center"
    },
    "hud": {
      "background": "rgba(30, 41, 59, 0.85)",
      "color": "#e2e8f0",
      "fontSize": 48,
      "fontFamily": "\"SF Mono\", monospace",
      "borderRadius": 12,
      "position": "top"
    }
  }
}
```

- `cursor.image` - path to a custom cursor SVG or PNG
- `cursor.size` - cursor size in pixels
- `cursor.hotspot` - `"top-left"` (default) or `"center"`
- `hud.position` - `"top"` or `"bottom"`

## Common patterns

### Shared steps via include

Factor out reusable step sequences (e.g. dismissing a cookie banner) into JSON files:

```json
// steps/dismiss-banner.json
{
  "steps": [
    { "action": "wait", "selector": ".cookie-banner", "timeout": 5000 },
    { "action": "click", "selector": ".accept-btn", "delay": 300 }
  ]
}
```

Reference them in the config:

```json
{
  "include": ["./steps/dismiss-banner.json"],
  "videos": { ... }
}
```

### Multiple videos in one config

Define several videos in the `videos` map. Shared settings (`viewport`, `theme`, `defaultDelay`) are inherited from the top level.

### Environment variables

Config values support `$VAR` and `${VAR}` substitution from the environment.

### Output formats

Set the `output` extension to control format: `.mp4` (default), `.gif`, `.webm`.

```json
{ "output": "demo.gif" }
```

## Tips

- Always set `waitFor` on a video to ensure the page is ready before steps run.
- Use `delay` on individual steps to control pacing between actions.
- Use `--watch` during development for automatic re-recording on config changes.
- Use `composite` to iterate on theme/overlay settings without re-recording.
- Use `--verbose` to debug step execution.
- Use `--dry-run` to inspect the fully resolved config (includes, env vars, defaults).
- Use `zoom` to scale up small UIs for readability in the recording.
- Start with `preview` to verify steps work before committing to a full recording.

## Troubleshooting

### Browser Errors

```
Error: No inspectable targets
Error: Browser closed unexpectedly
```

**Cause:** Almost always a config issue, not a missing browser. webreel auto-downloads Chrome to `~/.webreel`.

**Fix:**
1. Run `npx webreel record --verbose` to see which step fails
2. Check `waitFor` — if the selector doesn't exist on the page, the browser times out
3. Run `npx webreel install --force` to re-download binaries if they're corrupted
4. If using a custom `CHROME_PATH`, verify the binary exists and is executable

### Missing Elements

```
Error: Element not found: "Submit Button"
Error: Timeout waiting for selector ".hero-section"
```

**Cause:** The element hasn't loaded yet, the selector is wrong, or the page layout changed.

**Fix:**
1. Add a `wait` step before interacting: `{ "action": "wait", "selector": ".hero-section", "timeout": 10000 }`
2. Use `npx webreel preview --verbose` to watch the browser and see what's on screen
3. Verify selectors with browser DevTools on the target URL
4. If the page has lazy-loaded content, add a `scroll` step to trigger loading first

### Timing Issues

**Symptoms:** Actions happen too fast, elements are clicked before animations complete, typed text is cut off.

**Fix:**
- Add `delay` to individual steps: `{ "action": "click", "text": "Submit", "delay": 500 }`
- Set `defaultDelay` at the top level for consistent pacing across all steps
- Use `clickDwell` to add a pause before clicks (makes cursor movement feel natural)
- For typing, use `charDelay` to control speed: `{ "action": "type", "text": "hello", "charDelay": 80 }`

### Recording Produces Black/Empty Video

**Cause:** ffmpeg encoding issue or the page didn't render.

**Fix:**
1. Run `npx webreel record --frames` to save raw JPEGs — check if frames are captured
2. Verify the URL is accessible (not behind auth, VPN, or localhost that isn't running)
3. Try a simpler config with just a `pause` step to isolate the issue

## Reference files

- [steps-reference.md](steps-reference.md) - detailed docs for all 12 step types
- [examples.md](examples.md) - annotated config examples for common use cases
