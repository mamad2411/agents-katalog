---
name: adesk-pro
description: Drive desktop apps for the user through the accessibility tree — snapshot windows into JSON trees with refs, then click, type, set values, press shortcuts and scroll on those refs. Works on Windows and macOS. Use when the user asks to open, click, fill, read, close, resize or automate a desktop app, needs UI state or a window screenshot, or wants window management. Triggers on "open app", "click the button", "fill the form", "read the window", "close the app", "take a window screenshot", "desktop automation", "adesk".
---

# adesk-pro

adesk-pro reads apps through the OS accessibility tree (Windows UIA, macOS AX) and returns JSON with refs. You act on refs, then verify by reading again — the observe-act-verify loop lives in you; the tool has no model inside.

Install steps live in [INSTALL.md](INSTALL.md) shipped with this skill. Run `adesk-pro doctor` once before letting an agent use it.

## First run

1. `adesk-pro doctor` — permissions, platform readiness and visible windows. **Run this before anything else**; an empty `list-apps` is almost always a missing permission, not a missing app.
2. `adesk-pro list-apps` — the windows you can address. Note the `name` (window title) and `process` (process name); `--app` matches either.
3. `adesk-pro skills --name desktop` — this guide, straight from the binary you are running.
4. `adesk-pro <command> --help` — flags for one command. This guide does not repeat flag lists.

## The loop

```
adesk-pro snapshot --app Notepad -i              # JSON tree, interactive elements carry refs
adesk-pro click @s8f3k2p9:e12                    # act on a ref
adesk-pro snapshot --app Notepad -i              # read again to verify
```

Every ref command also accepts the explicit flag form (`--ref @s8f3k2p9:e12`); both are the same.

- `-i` keeps interactive elements only. For a dense app take `--skeleton` (subtrees summarized with `children_count`), then `snapshot --root @s8f3k2p9:e3 -i` to drill one region.
- `find --app X --name "Save"` locates elements by name/role without walking the whole tree yourself.
- An action that opens a dialog lists it in the result; snapshot again to see it.
- After an async step, `wait` for the window or ref state instead of a fixed sleep. A `wait` timeout comes back as `ok:false` with `TIMEOUT` — do not treat it as success.
- Can't match a window by title? `list-apps --process <name>` and retry with `--pid`, or pass the numeric id from `list-apps`.

## Refs

- Refs are qualified `@<snapshotId>:e<N>` and bind to their snapshot. After the UI changes, re-snapshot.
- Before any action the element is re-identified live: scope-path descent → RuntimeId pinning (Windows) → identity match. Zero matches: `STALE_REF`. Several: `AMBIGUOUS_TARGET` — take a fresh snapshot and pick a unique element.
- Identity uses the stable role id, not a localised label, so refs survive a UI-language change. A text field's name *is* its content, so editing it does not invalidate the ref.
- `find` can address repeated controls (twin buttons): it issues refs with RuntimeId pinning.

## Delivery and retry

Results and errors carry `disposition`. Retry an action only when `disposition.retry` is `safe` (nothing was delivered). Otherwise the action may have landed — read live state (`get`, `snapshot`) and decide. Never repeat a click or type because an error looked odd.

## Headed input

`press`, `mouse-click`, `hover` and `drag` move the real cursor or synthesize keys. Use them deliberately: `mouse-click` targets screen coordinates (the fallback for controls without patterns), `press --app X` scopes a shortcut to one app without focusing it manually.

## When the tree is empty

If `snapshot` returns `refCount: 0` or fails on an app that is clearly on screen, the app may draw its
own UI without exposing accessibility nodes (some games, remote-desktop canvases, badly-behaved
Electron/Flutter builds). Fall back to `screenshot` (`--out shot.png` or inline base64) and reason
from the image; treat that as the exception, not the default.

## Limits

- Windows and macOS. Sequential MCP dispatch.
- A walk that hits its budget returns `complete: false` — drill with `--root` or raise `--timeout-ms` instead of trusting a partial tree.
- `STALE_REF` errors include a diagnostic comparing live vs. saved identity fields; read it before re-snapshotting blindly.
