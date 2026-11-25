---
name: ferrisgrid-use
description: Use FerrisGrid as an agent-facing visual control tool. Use when an agent needs to observe screens, read screenshot paths, choose normalized coordinates, execute one action, and continue by alternating observe and act calls.
---

# FerrisGrid Use

FerrisGrid is single-step. Do one observe or one action per call, then stop and inspect the Markdown result.

When a task says to use FerrisGrid only, do not use browser automation, page-source fetches, scraping, external search, or host GUI control to inspect or drive the target. Use FerrisGrid observations/actions and inspect the screenshot files returned by FerrisGrid.

If `ferrisgrid` is not installed on the host, install the published CLI first:

```bash
cargo install ferrisgrid-cli
```

## Container Workspace

For the Linux Docker/noVNC workspace, keep the agent terminal on the host and run FerrisGrid inside the container:

```bash
docker ps --filter name=ferrisgrid-workspace --format '{{.Names}}:{{.Status}}:{{.Ports}}'
docker exec ferrisgrid-workspace ferrisgrid doctor
docker exec ferrisgrid-workspace ferrisgrid observe --max-image-edge 1280
```

If the container is not running:

```bash
docker run --rm -d --name ferrisgrid-workspace -p 6080:6080 -v "$PWD:/workspace" ferrisgrid-linux-workspace
```

The human can view the same background desktop at:

```text
http://127.0.0.1:6080/vnc.html?autoconnect=1&resize=scale
```

Container-specific checks:

- Run `ferrisgrid doctor` inside the container before task work; expected backend is `native-linux-x11`.
- If `.ferrisgrid/` was deleted, the next `observe` recreates it automatically.
- Use `docker exec ferrisgrid-workspace ferrisgrid ...`; do not run host `cargo run` when the target is the container desktop.
- If host `curl` to noVNC fails from the sandbox but `docker ps` shows `6080` mapped, retry with approved local network access before assuming noVNC is down.
- Leave the container running when the user wants to inspect the workspace; stop it only when cleanup is requested.

## Observe

Capture all screens by default:

```bash
ferrisgrid observe
```

Capture one screen only:

```bash
ferrisgrid observe --screen-id screen-1
```

Use smaller images for faster LLM vision:

```bash
ferrisgrid observe --max-image-edge 1280
```

## Coordinates

- Use `coordinate_mode: normalized-1000`.
- `x=0 y=0` is the top-left of the target screen.
- `x=1000 y=1000` is the bottom-right.
- Coordinates are screen-local, not virtual-desktop coordinates.
- If multiple screens are listed, include `screen_id`.
- Read the returned `screenshot=` path and optional `metadata=` path after every call.

## Act

Write compact Markdown to an action file, not JSON or prose:

```bash
# Update .ferrisgrid/action.md with one compact Markdown action, then run:
ferrisgrid act --file .ferrisgrid/action.md
```

For the container workspace:

```bash
docker exec ferrisgrid-workspace ferrisgrid act --file .ferrisgrid/action.md --max-image-edge 1280
```

Before each action, replace the whole action block. Do not patch only one field if that can leave duplicate keys such as two `x:` lines. If in doubt, read the file first:

```bash
sed -n '1,80p' .ferrisgrid/action.md
```

Example `.ferrisgrid/action.md`:

```markdown
status: action
action: click
screen_id: screen-1
x: 500
y: 500
button: left
wait_after_ms: 500
```

Use `wait_after_ms` on UI-changing actions so FerrisGrid captures the updated UI after the action settles. It waits after executing the action and before taking the returned screenshot. Omit it for pointer moves or actions where an immediate capture is useful. Maximum: `30000`.

Suggested `wait_after_ms` values:

- `150-300`: simple desktop focus changes, opening menus, toggles, hover-triggered UI.
- `300-700`: local app tab switches, list selection, expanding rows, lightweight modals.
- `700-1200`: browser SPA route changes, message/thread switches, filtered lists, autocomplete results.
- `1200-2500`: form submissions, sign-in transitions, search results, uploads that start background work.
- `2500-5000`: full page loads, slow web dashboards, OAuth redirects, network-heavy state changes.
- `5000-15000`: installers, app launches, downloads, operations that visibly show a progress state.

Useful actions:

```markdown
status: action
action: click
screen_id: screen-1
x: 742
y: 611
button: left
wait_after_ms: 700
```

```markdown
status: action
action: scroll
screen_id: screen-1
x: 500
y: 500
delta_y: -720
wait_after_ms: 300
```

```markdown
status: action
action: type
text: hello
```

```markdown
status: action
action: press_key
key: enter
wait_after_ms: 1200
```

## Browser Tips

- If a page does not scroll, first click inside the page content, then retry scroll from that area.
- Browser overlays, galleries, and find boxes can capture input; close them before continuing.
- For product pages, `cmd+f` with a price symbol or keyword can jump to hidden details faster than repeated scrolling. Close find with `escape` before reading the final view.
- On Linux/X11 use ordinary web shortcuts such as `ctrl+l`, not macOS `cmd` shortcuts.
- If the address bar is already focused, type the URL directly, then `press_key enter`.
- On retail sites, dismiss cookie banners before country or location modals if clicks appear to do nothing.
- If a campaign/category feed hides product names or prices, use site search for a broad term to get a normal product grid.
- When grid product names are truncated, open the product detail page to confirm the full name and price.
- FerrisGrid overlays can obscure small text; rely on several screenshots, scroll slightly, or open detail pages rather than guessing.

## Troubleshooting

- If `observe` works but `act` through stdin returns `CoreGraphics returned no displays`, use the default `--file .ferrisgrid/action.md` path.
- If `docker exec ... ferrisgrid observe` works but noVNC is not visible from the host, check `docker logs ferrisgrid-workspace` for the WebSockify line and confirm port `6080` is mapped in `docker ps`.
- If Chromium opens smaller than the Xvfb display, check the container entrypoint `--window-size` values and verify with `xdotool search --onlyvisible --class chromium getwindowgeometry %@`.
- If input lands in the wrong place, run `xdotool getmouselocation` inside the container after a `move_mouse` smoke test to confirm coordinate mapping.

## Loop

1. Run `observe`.
2. Inspect returned screenshots.
3. Write exactly one action to `.ferrisgrid/action.md` and run `act --file`, adding `wait_after_ms` when the action should change visible UI.
4. Inspect the post-action screenshot path.
5. Repeat until done.

Finish with:

```markdown
status: done
reason: task complete
```
