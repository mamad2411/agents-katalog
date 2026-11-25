---
name: rdc
description: Control another machine's desktop (screenshot, click, type, key, focus, clipboard) over Tailscale with rdc. Use when a task needs to see or operate a remote Mac, Linux or Windows desktop, click a dialog on another computer, or set up / troubleshoot the rdc daemon. Triggers include "remote desktop", "click on the Mac mini", "screenshot the other machine", "rdc".
---

# rdc — Remote Desktop Control for agents

Full documentation lives in the repo's `docs/` folder (`docs/mcp.md`, `docs/cli.md`,
`docs/troubleshooting.md`); this skill is the short version. Every action you take is written
to the target machine's audit log with your tailnet identity.

`rdc` is one binary with two roles. `rdc serve` runs on the machine being controlled and
listens only on its Tailscale IP; every request is identified with tailscaled `whois` and
checked against an allowlist. `rdc mcp --target NAME` runs on the agent's machine as an MCP
stdio server. The same operations exist as CLI subcommands. There is no shell tool; use SSH
for that.

## Prefer the MCP tools when they are registered

Tools: `screenshot`, `displays`, `windows`, `focus`, `mouse_move`, `click`, `drag`, `scroll`,
`type`, `key`, `clipboard_get`, `clipboard_set`.

Rules that matter:

1. **Take a screenshot first.** Every x/y you pass is a pixel in the most recent screenshot,
   not a desktop coordinate. rdc converts. Never reuse coordinates from an older screenshot
   after a new one was taken with a different `max`.
2. Actions return a fresh screenshot by default so you can verify. Pass
   `then_screenshot: false` on chains of actions where you don't need to look.
3. Use `key` for Enter, Escape, Tab and shortcuts (`cmd+q`, `ctrl+shift+t`, `alt+f4`).
   `cmd`, `super`, `win` all mean the platform's Meta key. Use `type` for literal text.
4. Click centers of controls. If a click seems ignored, screenshot again; the window may
   have moved or a dialog may have appeared.
5. `windows` returns each window's rect in desktop points and, once a screenshot exists, in
   image pixels (`image` field), so you can click a window without guessing.
6. `focus` takes `id`, `app` (substring) or `title` (substring). On macOS it activates the
   owning app.

Register in Claude Code (`.mcp.json` in a project or `~/.claude.json`):

```json
{ "mcpServers": { "studio-mac": { "command": "rdc", "args": ["mcp", "--target", "studio-mac"] } } }
```

`--target` is `local`, a name from config `[targets]`, a `host[:port]`, or a URL.

## CLI equivalents

```sh
rdc -t studio-mac shot --max 1568 -o shot.png   # prints the desktop rect the image covers
rdc -t studio-mac windows                       # JSON list
rdc -t studio-mac click 1280 720                # desktop points, not image pixels
rdc -t studio-mac key cmd+space
rdc -t studio-mac type "hello"
rdc -t studio-mac focus --app Safari
rdc -t studio-mac clip                          # read clipboard; `clip TEXT` sets it
rdc -t studio-mac whoami                        # how the daemon identifies you
```

CLI coordinates are desktop points. Map from an image: `x = rect.x + px * rect.w / W`.

## Setting up a new target

On the machine to control:

```sh
rdc doctor                               # tailscaled reachable, displays, permissions
# put the allowlist in the config file first (see below); the service reads it from there
rdc serve                                # foreground test
rdc service install                      # LaunchAgent (macOS) / systemd --user (Linux)
```

Config lives at `~/.config/rdc/config.toml` (Linux) or
`~/Library/Application Support/rdc/config.toml` (macOS):

```toml
[serve]
port = 7770
allow = ["you@example.com", "tag:family"]   # tailnet logins, node names, tags, or "*"
# limit an identity: { who = "monitor-bot", can = "view" }   (view | input | clipboard | all)

[targets.studio-mac]
url = "http://host.tailnet.ts.net:7770"
```

### macOS specifics

- Build on the Mac itself. Run `scripts/macos/make-signing-identity.sh` **once from Terminal in
  the GUI session** (creates a self-signed `rdc-dev` identity in a dedicated keychain that
  scripts can unlock over SSH). Then `scripts/macos/bundle-and-sign.sh` produces a signed
  `~/Applications/rdc.app`; install the service from that path. Never ship ad-hoc: TCC keys
  grants to the code hash and forgets them on every rebuild.
- Grant Screen Recording and Accessibility to `rdc.app` once. The daemon prompts on start.
  If grants look stuck after a re-sign, run `tccutil reset ScreenCapture dev.rdc.daemon` and
  `tccutil reset Accessibility dev.rdc.daemon`, then restart the service.
- Jump System Settings to a pane from SSH:
  `open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"`.
- The bundle identifier / LaunchAgent label is `dev.rdc.daemon`.
- Restart: `launchctl kickstart -k gui/$(id -u)/dev.rdc.daemon`. Logs:
  `~/Library/Application Support/rdc/serve.log`.
- Screenshots use `/usr/sbin/screencapture` (fast); the CoreGraphics fallback is slow on Tahoe.
- Only humans can enter passwords or click TCC prompts; ask, don't work around.

### Windows

Install the daemon with `rdc service install` (a standard-user logon task in the user's desktop
session); never run `rdc serve` from an SSH session, which has no real display. Input aimed at
elevated windows (admin PowerShell, installers, UAC) is silently dropped unless the task was
installed with `--elevated`; if a click on such a window has no effect, say so rather than
retrying. Coordinates are physical pixels. Details: `docs/setup-windows.md`.

### Linux (Wayland/Hyprland)

Capture via portal Screenshot or wlr-screencopy, input via wlr virtual pointer/keyboard,
window list and focus via `hyprctl`. On GNOME and KDE only screenshots work today (no synthetic
input); X11 via xcap.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `403 ... not in the allowlist` | your tailnet login/node not allowed (tagged devices match only by tag or node name) | add it to `[serve].allow`, restart daemon |
| `403 forbidden: X may not use \`input\`` | your grant is limited (e.g. `can = "view"`) | ask the machine's owner to widen the grant; screenshots still work |
| `421 ... unexpected host` | URL host isn't a name the daemon knows for itself | use the Tailscale name/IP or add to `[serve].hosts` |
| `400 ... outside the desktop` / `scroll steps` | out-of-range coordinates or scroll | take a new screenshot; scroll ≤100 steps |
| `not a Tailscale address` / connection refused | connecting from outside the tailnet, or daemon bound elsewhere | use the Tailscale hostname; check `rdc doctor` on the target |
| connection times out | Tailscale access policy blocks tcp/7770 to that machine | a policy rule (`grants`/`acls`) must allow your login or tag to reach the host on `tcp:7770`; rdc's own allowlist is checked only after the packet arrives |
| Screenshot is only the wallpaper (macOS) | Screen Recording not granted to *this* build | re-grant; check `rdc doctor`; avoid ad-hoc signing |
| Input does nothing (macOS) | Accessibility not granted | grant, restart daemon |
| Click lands at the wrong place | coordinates from a stale or differently sized screenshot | take a new screenshot, click from it |
| `--dev-loopback` | testing only: 127.0.0.1 unauthenticated | never in production |
