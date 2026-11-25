---
name: webapp-testing
description: Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
requires: playwright, npm
---
# Web Application Testing

To test local web applications, write native Python Playwright scripts.

**Run them with `python3`.** Playwright and a headless Chromium are already installed for the shell's
`python3` (`PLAYWRIGHT_BROWSERS_PATH` points at the browser), so a script runs as it is:
`python3 qa/shoot.py`. Do not `uv add playwright`, `uv run` it or `playwright install`: `uv` picks
another interpreter without Playwright, and the install downloads a second browser into the workspace.
Write screenshots into the workspace (`qa/shots/…`), not `/tmp`, which is gone when the command ends,
then look at them with `ImageView`.

**Helper Scripts Available**:
- `scripts/with_server.py` - Manages server lifecycle (supports multiple servers)

They live in this skill's directory, at the absolute path the Skill tool printed with the skill: run
them by that path, since a command starts in the workspace. **Always run scripts with `--help` first** to see usage. DO NOT read the source until you try running the script first and find that a customized solution is abslutely necessary. These scripts can be very large and thus pollute your context window. They exist to be called directly as black-box scripts rather than ingested into your context window.

## Decision Tree: Choosing Your Approach

```
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         ├─ Success → Write Playwright script using selectors
    │         └─ Fails/Incomplete → Treat as dynamic (below)
    │
    └─ No (dynamic webapp) → Is the server already running?
        ├─ No → Run: python scripts/with_server.py --help
        │        Then use the helper + write simplified Playwright script
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

## Example: Using with_server.py

To start a server, run `--help` first, then use the helper:

**Single server:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**Multiple servers (e.g., backend + frontend):**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

To create an automation script, include only Playwright logic (servers are managed automatically):
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # Always launch chromium in headless mode
    page = browser.new_page()
    page.goto('http://localhost:5173') # Server already running and ready
    page.wait_for_load_state('networkidle') # CRITICAL: Wait for JS to execute
    # ... your automation logic
    browser.close()
```

## WebGL, three.js and other 3D pages

When the operator passed a GPU into the agent's container, a plain `p.chromium.launch()` draws WebGL on
it: the image's Chromium adds the switches itself (`--use-angle=vulkan --ignore-gpu-blocklist`). Check what
draws before you judge a frame rate, once per script:

```python
renderer = page.evaluate("""() => {
  const gl = document.createElement('canvas').getContext('webgl2') || document.createElement('canvas').getContext('webgl');
  if (!gl) return 'no WebGL';
  const info = gl.getExtension('WEBGL_debug_renderer_info');
  return info ? gl.getParameter(info.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER);
}""")
print('renderer:', renderer)   # the GPU: "ANGLE (NVIDIA, Vulkan … NVK …)"; the CPU: "SwiftShader" or "llvmpipe"
```

**SwiftShader or llvmpipe means the browser fell back to the processor, not that the machine has no GPU.**
Never tell the operator there is no video card from that. Find out why instead:
- `ls -l /dev/dri` in Exec: no `renderD…` node means the GPU is not passed into the agent's commands
  (`AGENT_GPU_DEVICE` in the installation's `.env`). Say exactly that, and test with what you have.
- `echo $DAEDALUS_CHROMIUM_GPU` is not `1`, or you launched a Chromium the image did not install (one you downloaded,
  `executable_path=…`, another `PLAYWRIGHT_BROWSERS_PATH`): pass the switches yourself,
  `p.chromium.launch(args=["--use-angle=vulkan", "--ignore-gpu-blocklist"])`.
- Your own `args` put `--use-angle=swiftshader` or `--disable-gpu`: take them out.

The card is modest, and its frame rate is not what a visitor's laptop gets: a frame rate here proves a scene
runs and finds the frames that stall, not that it is fast enough. Heavy fill (large points, many full-screen
passes, a high `devicePixelRatio`) is slow on it too.

**Test a heavy animation in two passes**, or every check waits on the scene:
1. One real WebGL check: load the page, wait for a couple of `requestAnimationFrame`s, read the renderer,
   check the canvas is not blank (a screenshot of the canvas, or `gl.readPixels` on a few points), and if it
   matters measure frames over three to five seconds. Once, not per check.
2. Everything else (layout, text, clicks, forms, responsive shots) with the animation skipped:
   `browser.new_context(reduced_motion="reduce")` when the page honours `prefers-reduced-motion` (build it
   to, a static frame is also what those visitors should get), or a switch of the page's own (`?static=1`
   that renders one frame and stops the loop). A screenshot of a still frame takes a moment; one of a
   running 40 000-point scene on the processor took minutes.

## Reconnaissance-Then-Action Pattern

1. **Inspect rendered DOM**:
   ```python
   page.screenshot(path='qa/shots/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **Identify selectors** from inspection results

3. **Execute actions** using discovered selectors

## Common Pitfall

❌ **Don't** inspect the DOM before waiting for `networkidle` on dynamic apps
✅ **Do** wait for `page.wait_for_load_state('networkidle')` before inspection

## Best Practices

- **Use bundled scripts as black boxes** - To accomplish a task, consider whether one of the scripts available in `scripts/` can help. These scripts handle common, complex workflows reliably without cluttering the context window. Use `--help` to see usage, then invoke directly. 
- Use `sync_playwright()` for synchronous scripts
- Picture one section with `page.locator('#pricing').screenshot(path=...)` or the whole page with
  `full_page=True`: a viewport shot cuts the section at the fold, and the review of it asks for the rest
- Always close the browser when done
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
- Add appropriate waits: `page.wait_for_selector()` or `page.wait_for_timeout()`

## Reference Files

- **examples/** - Examples showing common patterns:
  - `element_discovery.py` - Discovering buttons, links, and inputs on a page
  - `static_html_automation.py` - Using file:// URLs for local HTML
  - `console_logging.py` - Capturing console logs during automation