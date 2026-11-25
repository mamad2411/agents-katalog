---
name: marey
description: >-
  Use Marey to inspect visual behavior that changes over time by capturing the
  screen or a specific window as timestamped frames and a contact sheet. Use for
  animations, transitions, dragging, hover states, menus opening or closing,
  flashes, rendering glitches, visual reordering, stutter, and other UI behavior
  that cannot be understood reliably from a single screenshot. Also use when
  setting up, connecting, configuring, testing, or troubleshooting Marey.
---

# Marey

Marey is an MCP server in this repository for inspecting **temporal visual
behavior**.

It captures a screen or window as timestamped still frames and combines the
frames into a contact sheet that can be inspected as a single image.

Use Marey when understanding **what changes between frames** matters.

## Decide whether to use Marey

Use:

- `capture` when one static screenshot is sufficient.
- `record` when the behavior involves motion, timing, transitions, interaction,
  or a state change.
- `list_windows` before targeting a specific application window.

Typical reasons to use `record` include:

- dragging or resizing
- animations and transitions
- hover behavior
- menus or popovers opening and closing
- flicker or flashes
- canvas or DOM elements moving or reordering
- rendering glitches that appear briefly
- stutter or inconsistent frame-to-frame behavior
- UI state changes caused by an interaction

Do **not** record several seconds of the screen when a single screenshot can
answer the question.

Prefer the smallest relevant capture scope. A specific window is usually better
than the entire desktop.

# Normal workflow

When Marey is already connected, do not repeat installation or backend checks.

## Static visual inspection

Call:

```text
capture
```

Prefer a specific window when possible.

## Temporal visual inspection

1. If the relevant window is not known, call `list_windows`.
2. Select a visible, non-minimized window by its stable `windowId`. A title is a fallback and must be unambiguous.
3. Call `record`; use `rect: {x,y,w,h}` to restrict recording to the relevant area if possible.
4. Inspect the returned contact sheet.
5. Check the quality summary first: achieved FPS, capture gaps, warnings, errors, and completion reason. A partial/failed recording can still contain useful evidence. Compare frames in chronological order.
6. Refer to both **frame numbers and timestamps** when describing a change.
7. If one transition needs closer inspection, inspect the corresponding
   neighborhood with `get_frames {dir,startMs,endMs,maxFrames}` and fetch a cropped full-resolution raw frame with `get_frame` before making another recording.

Do not infer exact timing from frame numbers or requested FPS. Use the timestamp
shown on each frame because FPS is only a target.

# Recording defaults

Start with the smallest recording likely to reveal the behavior.

Choose `detail` by what must be read, not by habit. If the behavior involves UI
text, labels, or fine detail, start at `detail: "high"`; the default
`"overview"` packs the whole screen into small cells and is often unreadable.

### Normal UI interaction

```text
seconds: 4
fps: 3
detail: "high"
```

### Slow animation or transition

```text
seconds: 6
fps: 2
detail: "high"
```

### Short or fast visual event

```text
seconds: 2
fps: 20
```

### Many frames at a glance (coarse motion, no fine detail)

```text
detail: "overview"
```

Higher requested FPS does not guarantee higher effective FPS. Screen capture and
PNG encoding take time.

If frames are being missed:

1. Prefer `region: "window"` over full-screen capture.
2. Reduce the captured area if possible.
3. Shorten the recording.
4. Increase `fps` only when the event genuinely requires it.

If the contact sheet is difficult to read, raise the `detail` preset before
anything else:

```text
detail: "overview"   # default: 4 cols @ 480px, many frames at a glance
detail: "high"       # 2 cols @ 760px, UI text usually readable
detail: "max"        # 1 col @ 1280px, closest to the raw frame
```

A returned image has a fixed resolution budget split across columns, so
legibility comes from fewer, wider cells — not from `thumbWidth` alone. `detail`
sets both at once; explicit `cols`/`thumbWidth` still override it.

When even `detail: "max"` is not enough, read the full-resolution raw frame
directly (see **Interpreting a recording**) instead of re-recording.

# Targeting a window

Call `list_windows` first when the target title is uncertain.

Then record using:

```text
region: "window"
windowId: "<visible window ID from list_windows>"
```

Example:

```text
record {
  seconds: 4,
  fps: 3,
  region: "window",
  title: "Visual Studio Code"
}
```

Prefer window capture because it:

- removes unrelated visual noise
- reduces privacy exposure
- reduces capture cost
- can improve effective frame rate
- produces easier-to-read contact sheets

# Coordinating an interaction

When the user wants to demonstrate a bug, prefer `observe`; for an intermittent glitch, prefer `replay`. Announce the interaction and Finish/Mark controls before calling these blocking tools. For agent-controlled timing, use the following alternatives:

## Fixed duration (`record` + `delay`)

Use when the interaction is short and its duration is predictable. Set `delay`
so the user can get ready, tell them exactly when to act, and `record` captures
for a fixed `seconds`.

```text
record { seconds: 5, fps: 4, delay: 3, detail: "high" }
```

Do not use long delays when they are unnecessary.

## Open-ended (`start_recording` / `stop_recording`)

Use when the **user** controls the timing and the duration is unpredictable
(dragging until something happens, waiting for a load, exploring a menu).

1. Call `start_recording` (same options as `record` except `seconds`).
2. Tell the user to perform the interaction now.
3. When the user says they are done, call `stop_recording`. It returns a contact
   sheet exactly like `record`.

Only one recording can be active at a time. If `start_recording` reports one
already in progress, call `stop_recording` first. Prefer this pair over a long
fixed `record` when you would otherwise be guessing the duration.

Keep the interaction simple enough to reproduce reliably.

# Interpreting a recording

Treat the recording as a sequence, not as independent screenshots.

When analyzing the result:

1. Establish the initial state.
2. Find the first frame where a visible change occurs.
3. Follow the change through subsequent frames.
4. Identify the final stable state.
5. Reference relevant frames and timestamps.
6. Distinguish what is directly visible from what is inferred.

Prefer statements such as:

```text
The menu is closed at #003 (0.84 s), begins appearing at #004 (1.17 s), and is
fully visible by #005 (1.51 s).
```

Avoid unsupported timing claims based only on the requested FPS.

If the contact sheet does not contain enough detail, fetch the relevant frames
at full resolution with `get_frame` instead of re-recording. Pass the recording
directory and the frame number (both are listed in the `record` /
`stop_recording` response):

```text
get_frame { dir: "<recording dir from the response>", index: 4 }
```

`get_frame` returns the original full-resolution frame as an image over MCP, so
it works even without filesystem access. The raw frames are also on disk under
`captures/<timestamp>/` for clients that prefer to read them directly.

Do this before re-recording unless the event itself was missed.

# Available MCP tools

Marey exposes ten tools.

| Tool | Use |
| --- | --- |
| `record` | Capture temporal behavior for a fixed duration and return a contact sheet |
| `start_recording` | Begin an open-ended recording the user controls |
| `stop_recording` | Stop the open-ended recording and return the contact sheet |
| `capture` | Capture one screenshot |
| `get_frame` | Fetch one frame from a recording at full resolution |
| `list_windows` | Discover IDs, bounds, and hidden state; prefer exact IDs |
| `observe` | Record until the user clicks Finish |
| `replay` | Keep a rolling buffer; user marks glitches then finishes |
| `status` | Inspect recording state |
| `get_frames` | Inspect a time range as a contact sheet, optionally cropped |

## `record`

Parameters:

| Parameter | Default | Meaning |
| --- | ---: | --- |
| `seconds` | `5` | Recording duration, 0.1–120 seconds |
| `fps` | `15` | Target frames per second, 0.1–60 |
| `region` | `primary` | `primary`, `virtual`, or `window` |
| `title` | — | Unambiguous title substring, an alternative to `windowId` |
| `windowId` | — | Stable native ID from `list_windows` |
| `rect` | — | Integer `{x,y,w,h}` in target-relative pixels, applied during recording |
| `delay` | `0` | Delay before recording starts |
| `detail` | `overview` | Legibility preset: `overview`, `high`, or `max` |
| `cols` | `4` | Contact-sheet columns (overrides `detail`) |
| `thumbWidth` | `480` | Thumbnail width in pixels (overrides `detail`) |

## `start_recording`

Takes the same parameters as `record` **except `seconds`** (the recording runs
until `stop_recording`): `fps`, `region`, `title`/`windowId`, `rect`, `delay`, `detail`, `cols`,
`thumbWidth`. Only one recording can be active at a time.

## `stop_recording`

Takes no arguments. Stops the active recording and returns a contact sheet with
the same shape as `record`.

## `get_frame`

Returns one frame at full resolution. Supply either the recording directory plus
a frame number, or a direct frame path.

| Parameter | Default | Meaning |
| --- | ---: | --- |
| `dir` | — | Recording directory from a `record` / `stop_recording` response |
| `index` | — | 1-based frame number (required with `dir`) |
| `path` | — | Direct path to a frame PNG (alternative to `dir` + `index`) |

`capture` supports `region`, `title`/`windowId`, `rect`, and `delay`.

`get_frames` requires `dir`; `startMs`/`endMs` specify inclusive acquisition milliseconds, `maxFrames` is 2–36 (default 12), and `crop` uses the same format as `get_frame`. It retains before/changed/following context and reports absent/unreadable frames.

Read `quality`, `actual`, `warnings`, `errors`, `completionReason`, and `target` from structured results when available. Older clients receive a text fallback. Never claim that an event did not happen inside a capture gap. A degraded result is useful partial evidence, not a clean reproduction.

`list_windows` takes no arguments.

# Setup

Only perform these steps when Marey is being installed, connected, or
troubleshot.

## Requirements

- Node.js 18+

Capture backends are auto-detected:

- **Windows 10/11:** PowerShell + `System.Drawing`
- **Linux X11:** `scrot`, ImageMagick `import`, or `ffmpeg`
- **Linux Wayland:** `grim`
- **macOS:** built-in `screencapture`

Continuous X11 capture requires FFmpeg and xdotool; window listing/validation also requires xwininfo. macOS continuous capture requires FFmpeg AVFoundation and Screen Recording permission. Wayland uses a slower native-command fallback; use region:"virtual" or a rect. macOS virtual-desktop/window capture is unsupported.

## Verify the capture backend

The server speaks MCP over stdio and has no standalone subcommands. To probe
the capture backend outside an MCP client, clone the repo and run the bundled
CLI:

```bash
node src/cli.mjs backend             # report the detected capture backend
node src/cli.mjs windows             # list targetable windows
node src/cli.mjs capture --region primary
```

If the backend reports `*:none` or capture fails, fix the capture backend
(install `scrot`/`grim`/`ffmpeg` on Linux; PowerShell and `screencapture` are
built in on Windows/macOS) before debugging MCP configuration.

# Connect Claude Code

The recommended install is the published npm package via `npx` — no clone, no
absolute path:

```bash
claude mcp add marey -- npx -y @anilyesilkaya/marey
```

Verify using:

```bash
claude mcp list
```

or `/mcp` inside Claude Code.

The following tools should be available:

```text
record
start_recording
stop_recording
capture
get_frame
get_frames
list_windows
observe
replay
status
```

Alternatively, install the Claude Code plugin, which bundles this skill and the
MCP server together:

```text
/plugin marketplace add anilyesilkaya/marey
/plugin install marey@marey
```

# Connect another MCP client

Add Marey to the client's MCP configuration using `npx`:

```json
{
  "mcpServers": {
    "marey": {
      "command": "npx",
      "args": ["-y", "@anilyesilkaya/marey"]
    }
  }
}
```

Restart the MCP client after modifying its configuration.

# Troubleshooting

### No capture backend

```text
linux:none
```

Install a supported capture backend.

### Window cannot be found

Run `list_windows` again and select a visible window ID. An ambiguous title requires an ID; hidden/minimized targets are rejected.

The window must be visible and non-minimized.

### MCP connects but capture hangs

Test:

```bash
node src/cli.mjs capture
```

If this also fails, troubleshoot the capture backend rather than MCP.

### MCP output cannot be parsed

The server uses:

- stdout for JSON-RPC
- stderr for diagnostic logging

Do not add arbitrary stdout logging to the MCP server.

# Verification

Run the test suite:

```bash
npm test
```

To test the MCP protocol directly:

```bash
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"t","version":"0"}}}' \
  '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
  | node src/server.mjs
```

The response should identify the server as `marey` and list:

```text
record
start_recording
stop_recording
capture
get_frame
get_frames
list_windows
observe
replay
status
```
