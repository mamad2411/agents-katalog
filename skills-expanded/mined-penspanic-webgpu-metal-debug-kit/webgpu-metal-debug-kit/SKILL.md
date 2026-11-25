---
name: webgpu-metal-debug-kit
description: "Debug Chrome WebGPU applications on macOS — browser-level via Chrome DevTools MCP, GPU-driver-level via Xcode xctrace Metal System Trace. Use when: WebGPU rendering bugs, GPU performance issues, shader debugging, frame timing analysis, Metal command buffer profiling."
license: MIT
compatibility: "Requires macOS, Chrome 113+, Xcode (for Metal tracing). Chrome DevTools MCP for AI integration."
metadata:
  author: penspanic
  version: "2.2"
  platform: macOS
allowed-tools: Bash Read Grep Glob mcp__chrome-devtools__evaluate_script mcp__chrome-devtools__take_screenshot mcp__chrome-devtools__navigate_page mcp__chrome-devtools__list_console_messages
---

# WebGPU Metal Debug Kit

Debug Chrome WebGPU applications on macOS at two levels:

1. **Browser level** — Chrome DevTools MCP
2. **GPU driver level** — Xcode `xctrace` Metal System Trace

## Environment

Metal Toolchain: !`/usr/bin/xcrun xctrace list templates 2>/dev/null | grep -q "Metal System Trace" && echo "installed" || echo "NOT INSTALLED — run: xcodebuild -downloadComponent MetalToolchain"`

## Rules

1. **ONE Chrome only.** MCP manages Chrome. Never launch Chrome manually. Never run `setup-metal-debug.sh`.
2. **Wait after navigate.** After `navigate_page`, wait 2-3 seconds before calling `evaluate_script`.
3. **`evaluate_script` over `take_screenshot`.** Stats = few tokens. Screenshot = ~1MB tokens.
4. **Metal trace: direct command only.** Always use `/usr/bin/xcrun xctrace` directly. Never use `bash scripts/capture-metal-trace.sh` (PATH issues in Claude Code).

## Workflow

The user provides a URL to their running WebGPU app. If they say "demo", run `bash ${CLAUDE_SKILL_DIR}/../../demo/start.sh --no-open` in the background. The script finds an available port automatically and prints `Server ready: http://localhost:<port>/demo/`. Parse the URL from the output and use it. The `--no-open` flag prevents opening a system browser (MCP Chrome will be used instead).

### Step 1: Open the app

```
navigate_page → <user's URL>
```

Wait, then verify the debug helpers are loaded:

```javascript
// evaluate_script
() => window.__gpu ? window.__gpu.stats() : 'not loaded'
```

If `window.__gpu` is not available, the app may not include `webgpu-debug-helpers.js`. Guide the user to add it.

### Step 2: Browser-level debugging

```javascript
window.__gpu.stats()          // { fps, avgMs, maxMs, frameGapMs }
window.__gpu.setDebugMode(0)  // normal
window.__gpu.setDebugMode(1)  // render path (blue=hit, dark=miss)
window.__gpu.setDebugMode(2)  // step heatmap (green=few, red=many)
window.__gpu.setDebugMode(3)  // depth (dark=near, bright=far)
window.__gpu.setDebugMode(4)  // normals (RGB)
window.__gpu.textures()       // tracked texture info
window.__gpu.timings()        // GPU timing records
```

Check `list_console_messages` for WGSL shader errors or WebGPU warnings.

### Step 3: Metal-level profiling (when needed)

When `frameGapMs` >> `avgMs`, there may be a driver-level bottleneck.

```bash
GPU_PID=$(pgrep -f "Google Chrome.*--type=gpu-process" | head -1)
echo "GPU PID: $GPU_PID"
rm -rf /tmp/webgpu-metal-trace.trace
/usr/bin/xcrun xctrace record \
  --template 'Metal System Trace' \
  --attach "$GPU_PID" \
  --time-limit 5s \
  --output /tmp/webgpu-metal-trace.trace
```

Export and analyze:

```bash
/usr/bin/xcrun xctrace export --input /tmp/webgpu-metal-trace.trace --toc | grep schema

/usr/bin/xcrun xctrace export --input /tmp/webgpu-metal-trace.trace \
  --xpath '/trace-toc/run/data/table[@schema="metal-gpu-intervals"]'
```

Look for:
- Command buffer count per frame (high = Dawn overhead)
- Encoder durations (long = GPU bottleneck)
- Gaps between GPU executions (stalls)

Note: For full Metal encoder/command buffer detail, the user should configure MCP with `--browser-url` to connect to a Chrome launched with `--disable-gpu-sandbox`. See `assets/mcp-settings-metal.json`.

### Diagnostic Reference

| Symptom | Action |
|---------|--------|
| Artifacts | `setDebugMode(1)` — which path is wrong? |
| Shader error | `list_console_messages` |
| Data missing on GPU | `__gpu.stats()` — check uploadCount |
| Slow, GPU time fine | Metal trace — command buffer count |
| Hot pixels | `setDebugMode(2)` — red = expensive |
