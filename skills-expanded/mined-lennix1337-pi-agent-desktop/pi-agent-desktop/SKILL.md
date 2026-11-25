---
name: pi-agent-desktop
description: Operate native desktop apps (Windows, macOS, Linux) from Pi through the `desktop` tool, backed by vercel-labs/agent-desktop and the OS accessibility tree. Use to open, read, click, type into or screenshot a desktop program (Notepad, Explorer, Slack, Office, GeneXus IDE, settings dialogs), read notifications or the clipboard, or when a task needs something no API or browser reaches. Web pages go to browser_harness instead.
---

# pi-agent-desktop

The `desktop` tool takes either `command: "exec"` with `code` (a cell: several steps in one call) or one `agent-desktop` subcommand, run without a shell, returning its JSON.

## Cells (default for more than one step)

`code` is the body of an async JavaScript function. Helpers:

- `win(app, title?)` picks a visible window by app-name prefix and title substring and sets `W`; the other helpers target `W`, and `press`/`keys` refuse until it is set.
- `ad("launch", app, "--activate")` waits up to 30 s for a window, as long as the default cell: give that cell `timeout: 60`.
- `snap(...args)` (`snapshot -i` of `W`), `find(...args)`, `click(ref)`, `type(ref, text)`, `press(combo)`, `keys(text)` (one press per character, for fields without a ref).
- `at(x, y)` clicks and `wheel(dy, x?, y?)` scrolls at window-screenshot pixels (focus and offset handled); both need `headed: true`.
- `shot(opts?)`, `sleep(ms)`, `print(...)`, `ad(command, ...args)` for any other subcommand. `shot()` accepts opt-in `{ ref, padding, rect, maxWidth, scale, format, quality }`; `noScreenshot: true` (default `false`) skips the automatic post-action screenshot of `W`.

Values assigned without `let`/`const` persist to the next cell; `return` a value to see it. The cell stops at the first refused or failed step and reports every step it ran (`steps:`); calls made after it reported are refused, and calls it forgot to await are waited for. A cell that times out while its code still runs loses its variables, so that code cannot act later. An acting cell returns a screenshot of `W`, so check it before the next cell. Example: `await win("notepad"); await keys("hello"); await press("ctrl+s")`.

A long output is cut (default 12000 characters, `limit`), with `steps:` and `error:` right after the cut. An `exec` call with `offset` reads on in the stored output of the last cell and runs nothing, so nothing is clicked or typed twice; `code` may be left out. With no stored output, or with other code, it is refused, not run.

## Loop (single commands)

1. Find the target: `list-apps`, then `list-windows` with `["--app","<name>"]`. Several windows of one app give `AMBIGUOUS_TARGET`: pass `--window-id <id>`.
2. Observe: `snapshot` with `["--app","<name>","-i"]` (interactive elements with `@e` refs). Large trees: add `--skeleton`, or page with `offset` (a single command runs again for each page, so page only commands that observe).
3. Act on a ref: `click ["@e5"]`, `type ["@e7","text"]`, `set-value`, `press ["ctrl+s"]`, `select`, `check`.
4. Verify: snapshot again, or `wait` with `--text`/`--element`. A successful act result is not proof the app did what you wanted.

Refs expire when the UI changes: snapshot again before reusing one.

Chromium/Electron apps (Slack, VS Code, Teams) return `TIMEOUT` on a full `snapshot -i`, and raising `--timeout-ms` does not help (measured on Slack: 10 s, 30 s and 60 s all timed out). Use `snapshot -i --max-depth 3` (129 ms on Slack); depths 4-6 also timed out. If the shallow tree lacks the element, use `screenshot` plus `headed` physical input, or the app's API. Native apps (Notepad, Explorer, Office dialogs) snapshot in about 0.2 s at default depth.

## Safety

- The desktop is the user's live session. Act only on the apps and windows the task names; observing commands are always fine.
- Default delivery is semantic (accessibility actions, no cursor movement). `headed: true` moves the real mouse and keyboard and steals focus; use it only when a semantic action failed or the command is physical (`mouse-*`, `drag`, `hover`, `double-click`, `key-down/up`).
- `close-app --force`, typing into password fields, notification actions and clipboard writes are effects: they need the task's authority like any other write.
- `screenshot` returns an image; prefer `snapshot` text for reading. All screenshot optimizations are opt-in (defaults off): pass `screenshot: { ref, padding, rect: { x, y, w, h }, maxWidth, scale, format: "jpeg", quality }` on `screenshot`, `verify`, or `exec` (or `shot(opts)` in a cell) to crop to an element/rect, downscale, or encode as JPEG.
- `nonIntrusive: true` (default `false`): guarantees the user's screen is not touched by refusing `headed: true`, `focus-window`, `focus`, `minimize`, `maximize`, `restore`, `open-system-surface`, and `launch --activate`. Occluded (behind) windows are captured via `--window-id`; minimized windows cannot be captured without restoring them.
- Fewer turns: pass `verify: "<window id>"` on an action to get the after-screenshot in the same result instead of a separate `screenshot` call. Batch several presses or clicks only when no step depends on what the previous one showed.
- Physical coordinates are virtual-desktop pixels: add the window's `bounds.x/y` from `list-windows` to a point inside the window screenshot. Run `focus-window` first. Every pointer command takes the point as `--xy X,Y` (or `--x X --y Y`); the tool converts to the form the binary parses.
- Web pages inside a browser window usually expose nothing to `find`; use browser_harness, or screenshot + headed input when the session lives only in that window. `type` needs a snapshot ref, so without refs use `keys(text)` in a cell.

## More

`desktop` with `command: "skills"` and `args: ["get","desktop"]` (or `"platform"`) returns the upstream guide that matches the bundled binary version. `status` and `permissions` diagnose accessibility permissions (macOS needs Accessibility and Screen Recording for the host terminal).

Binary override: `PI_AGENT_DESKTOP_BIN`.
