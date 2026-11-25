---
name: html-video
description: Render frame-accurate deterministic MP4 videos from HTML/CSS/SVG compositions using headless Chrome and FFmpeg, with strict network isolation, local asset pinning, seek-order determinism, contact-sheet evidence, and ffprobe validation.
---

# HTML Video

Render deterministic, frame-addressed MP4 videos from HTML/CSS/SVG compositions using headless Google Chrome and FFmpeg.

Read [references/timeline-contract.md](references/timeline-contract.md) before authoring compositions.
Read [references/security-and-isolation.md](references/security-and-isolation.md) for isolation boundaries, asset pinning, and Windows execution policies.

**Optional, only when a mechanism illustration is requested**: read [references/mechanism-explainers.md](references/mechanism-explainers.md) for bounded explainer patterns (single state model, geometry invariants, contact-sheet checkpoints, accessible alternatives, visible simplifications). Normal sessions add no reference reads, model calls, or work steps; this link adds a small static prompt-token cost. The existing isolation policy remains authoritative.

## Runtime Prerequisites

- **Python**: 3.10+ with `playwright` and `Pillow`.
- **Browser**: Google Chrome at `C:\Program Files\Google\Chrome\Application\chrome.exe` (or `CHROME_BIN`). Runs with native Chromium OS sandboxing explicitly enabled (`chromium_sandbox=True`), strictly omitting `--no-sandbox`.
- **Encoders**: `ffmpeg` and `ffprobe` accessible on PATH.
- **Process Policy**: Windows children execute with `CREATE_NO_WINDOW` (`0x08000000`) without opening terminal windows.
- **Bytecode**: `PYTHONDONTWRITEBYTECODE=1` is enforced across all runners.

## Resolving Skill Root

```powershell
if (-not $env:SKILL_ROOT) { throw 'Set SKILL_ROOT to the directory containing this SKILL.md.' }
$SkillRoot = (Resolve-Path -LiteralPath $env:SKILL_ROOT).Path
if (-not (Test-Path -LiteralPath (Join-Path $SkillRoot 'scripts\render_video.py'))) { throw 'Invalid html-video SKILL_ROOT.' }
```

## Key Capabilities

1. **Deterministic Time Stepping**: Compositions expose `window.seek(t)` and `window.renderTimeline`. Wall-clock timers (`Date.now()`, `setInterval`, autonomous `requestAnimationFrame`) are prohibited.
2. **Network & Asset Isolation**: All remote requests (`http:`, `https:`, `ws:`, `wss:`, `ftp:`) are aborted at the Playwright route layer with `blockedbyclient`. Service workers and WebSockets are disabled via Chromium feature flags (`--disable-features=ServiceWorker,SharedWorker`), context-level blocking (`service_workers="block"`), pre-network WebSocket routing (`context.route_web_socket` immediately closing routes with code 1008 without server connection), and DOM-level prototype overrides. Both context HTTP routing and pre-network WebSocket routing strictly fail closed before any navigation if unavailable or on registration failure, never downgrading to page-only routing. Local file access is strictly confined to the composition root and explicitly admitted/pinned assets.
3. **Seek-Order & Cross-Browser Determinism**: The engine tests forward stepping against backward seeking (MAE $\le 0.001$) and tests fresh-browser repeated-frame captures across independent Chrome processes to rule out in-memory cache pollution.
4. **Safety Gates**: Refuses overwrite of existing files unless `--force` is specified. Requires an explicit output directory. In selftests, fresh unique retained run subdirectories allow repeated checks without overwrite conflicts.
5. **Technical Audio Validation**: Optional WAV audio is validated for RIFF headers, PCM format code, channels, sample rate, and duration before FFmpeg muxing.
6. **Auditable Evidence**: Generates keyframe contact sheets, `ffprobe` stream metadata (verifying duration, FPS, dimensions, frame count), FontFaceSet fingerprint, and SHA-256 manifests. Compositions declare local font files and assets in `renderTimeline.assets`, and their binary file SHA-256 hashes are pinned and verified in `manifest.json`. Selftest privately copies a local Windows font into its retained output package, declares `@font-face` and admitted asset bytes, and proves the actual binary SHA-256 without redistributing OS fonts in the skill origin. Each run retains evidence under its explicitly selected local output directory without automated deletion. Historical private UAT evidence is not distributed with this source edition.

---

## Workflow

1. **Select or Author Composition**: Create an HTML file adhering to the timeline contract. See `compositions/typography_chart.html` for a production reference supporting both 16:9 (`1920x1080`) and 9:16 (`1080x1920`).
   - *Conditional*: when the task calls for an animated architecture/data-flow diagram (nodes, edges, packet motion) rather than the telemetry chart, build a composition from a strict JSON config via `scripts/build_architecture_flow.py` — opt-in only; see [references/architecture-flow.md](references/architecture-flow.md) and `compositions/architecture_flow.example.json`.
2. **Execute Render Pipeline**: Run `render_video.py render` with the target composition, output directory, and aspect ratio.
3. **Inspect Output Video**: Verify stream codec, resolution, and duration with `render_video.py probe`.
4. **Review Visual Evidence**: Inspect `contact_sheet.png` to confirm margins, typographic hierarchy, and visual stability across both orientations.
5. **Verify Manifest**: Inspect `manifest.json` for determinism metrics, runtime versions, pinned assets, and blocked network requests.

---

## CLI Commands

### 1. Render Video (16:9 Landscape)

```powershell
python -B (Join-Path $SkillRoot 'scripts\render_video.py') render `
  --composition (Join-Path $SkillRoot 'compositions\typography_chart.html') `
  --out-dir "output\video_16_9" `
  --out-name "telemetry_16_9.mp4" `
  --aspect "16:9" `
  --width 1920 `
  --height 1080 `
  --fps 30 `
  --duration 5.0
```

### 2. Render Video (9:16 Portrait Mobile)

```powershell
python -B (Join-Path $SkillRoot 'scripts\render_video.py') render `
  --composition (Join-Path $SkillRoot 'compositions\typography_chart.html') `
  --out-dir "output\video_9_16" `
  --out-name "telemetry_9_16.mp4" `
  --aspect "9:16" `
  --width 1080 `
  --height 1920 `
  --fps 30 `
  --duration 5.0
```

### 3. Render Video (1:1 Square)

```powershell
python -B (Join-Path $SkillRoot 'scripts\render_video.py') render `
  --composition (Join-Path $SkillRoot 'compositions\typography_chart.html') `
  --out-dir "output\video_1_1" `
  --out-name "telemetry_1_1.mp4" `
  --aspect "1:1" `
  --width 1080 `
  --height 1080 `
  --fps 30 `
  --duration 5.0
```

### 4. Render with Validated Audio Track

```powershell
python -B (Join-Path $SkillRoot 'scripts\render_video.py') render `
  --composition (Join-Path $SkillRoot 'compositions\typography_chart.html') `
  --out-dir "output\video_with_audio" `
  --audio "assets\audio_bed.wav" `
  --force
```

### 5. Technical Probe

```powershell
python -B (Join-Path $SkillRoot 'scripts\render_video.py') probe `
  --input "output\video_16_9\telemetry_16_9.mp4"
```

### 6. Generate Contact Sheet

```powershell
python -B (Join-Path $SkillRoot 'scripts\render_video.py') contact-sheet `
  --frames-dir "output\video_16_9\frames" `
  --out "output\video_16_9\contact_sheet.png" `
  --cols 3 `
  --count 9
```

### 7. Automated Self-Test

Executes end-to-end rendering of 16:9 and 9:16 test videos (5.0s full timeline), audio-bearing MP4 with ffprobe validation, fresh-browser repeated-frame determinism, and retains all evidence without deletion:

```powershell
python -B (Join-Path $SkillRoot 'scripts\render_video.py') selftest `
  --output-dir "<owned-evidence-dir>"
```

### 8. Run Unit & Regression Tests

Accepts `--artifact-root` and retains all synthetic fixtures without cleanup:

```powershell
python -B (Join-Path $SkillRoot 'scripts\test_render_video.py') `
  --artifact-root "<owned-evidence-dir>"
```

---

## Output Manifest Schema

Each render produces an auditable `manifest.json`:

```json
{
  "manifest_version": "1.0",
  "composition": {
    "path": "<owned-evidence-dir>/compositions/typography_chart.html",
    "sha256": "..."
  },
  "output_video": {
    "path": "<owned-evidence-dir>/output.mp4",
    "sha256": "...",
    "duration_sec": 5.0,
    "width": 1920,
    "height": 1080,
    "r_frame_rate": "30/1"
  },
  "contact_sheet": {
    "path": "<owned-evidence-dir>/contact_sheet.png",
    "sha256": "..."
  },
  "pinned_assets": {
    "assets/font.woff2": {
      "path": "<owned-evidence-dir>/assets/font.woff2",
      "sha256": "..."
    }
  },
  "runtime": {
    "python": "3.10...",
    "platform": "win32",
    "playwright": "1.40...",
    "browser_binary": "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "browser_version": "128.0.6613.119",
    "ffmpeg": "ffmpeg version 6.1...",
    "ffprobe": "ffprobe version 6.1...",
    "pillow": "10.2...",
    "font_hash": "..."
  },
  "isolation_audit": {
    "blocked_requests_count": 0,
    "page_errors": [],
    "console_errors": []
  },
  "determinism": {
    "exact_byte_match": true,
    "mae": 0.0,
    "tolerance": 0.001,
    "tolerance_passed": true
  }
}
```
