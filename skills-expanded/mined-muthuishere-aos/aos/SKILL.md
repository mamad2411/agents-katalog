---
name: aos
description: >
  Drive the machine you are on — macOS, Windows or Linux — through one CLI:
  windows, mouse and keyboard, screenshots, files, processes, shell commands, packages, network,
  audio, clipboard, services, on-screen captions, and a LAN screen-share you can
  watch from a phone. Trigger on: move/resize/focus a window, list windows or
  monitors, take a screenshot, screenshot an app, click, type, press a key
  combination, launch an app, open a URL, read/write/delete a file, run a command
  and capture its output, install a package, check wifi or battery or volume,
  lock or sleep the machine, list or kill a process, watch a file or the clipboard,
  run something as a service,
  show a caption on screen, share my screen on the LAN, what can this machine do,
  snap a window to a half / quarter / third, N-way split, put an app on monitor 2,
  apply / save a window layout, which monitor is active, read all the text of a window, find a button / menu /
  text on screen, where is the Allow button, point at it, draw an arrow, show me
  where to click, highlight / circle / box this, hide / black out / cover something
  private on screen, open a terminal and run a command,
  is this machine set up correctly, expose this machine to an agent over MCP,
  record my screen, capture video, record a demo, screen recording with zoom,
  list tabs, find tab, switch tab, open tab, close tab, which terminal tab is in
  this folder, type into a terminal tab, watch a tab, wait for text in a tab,
  read a page, type into a page, click a button in a tab,
  add my own aos command, extend aos, write an aos plugin or adapter,
  wait until / tell me when: a build or process finishes, the network is back,
  a monitor is plugged in, a USB drive or headset connects, the battery is low
  or full, the person is idle or locked the screen, a call starts (camera or
  mic busy), text appears in a tab, a window or a URL, a page changes,
  what is eating my disk, is there a captive portal, a QR code to read or to
  join wifi, serve this folder over HTTP, launch the app or focus it if open,
  dark mode, brightness, bluetooth, now playing, do not disturb, notify.
  For mail, Teams, WhatsApp or calendar events use apl, not aos.
---

# aos

> **Supersedes `window-ctl-skill`.** aos runs windowctl as its engine library,
> so everything that skill did (window layout, zones, pointing, find, draw, the
> visual loop) is here as `aos …` commands. If both skills are installed, use
> this one; `windowctl` remains only as the library aos is built on.

One command surface over the machine, identical on macOS, Windows and Linux.
You already have a shell, so just run these commands — there is nothing to start
and nothing to connect to. (The same commands are also available over MCP for
agents that want typed tools; either way it is one code path.)

## Principles

- **aos is primitives.** Small, composable commands. It never decides for you.
- **A watch is a condition.** `aos watch ...` exits **0** when its condition is
  met and **3** on `--timeout`. It does not alert and has no `--then`: you do the
  alerting and the next step (`watch ... && <next>`, `|| <timeout path>`).
- **Cross-platform or not shipped.** A feature ships only if it works on macOS
  and Windows (Linux is optional); `commands --all` marks the exceptions.
- **Mail, Teams, WhatsApp and calendar events are apl's job**, not aos's. aos
  watches the machine (windows, tabs, URLs, processes, network, power, devices).

## The one rule

**Ask the binary, do not guess.** The catalogue is machine-readable and always
current:

```bash
aos commands            # what this machine can run right now
aos commands --json     # the same, parseable, with needs_display + platforms
aos <group> --help      # a group's commands
aos <group> <cmd> --help
```

If a command is not in `commands`, it does not exist here. Do not invent flags —
`--help` lists the real ones, and an unknown flag is rejected rather than ignored.

## Never take the person's focus

Someone is usually working at this machine while you drive it. **Always target
a window by name and act through accessibility; never through focus or bare
coordinates, unless the owner asked for exactly that.**

- Type: `key type --app=Notepad "text"` / `key press enter --title=T`. That puts
  the text into that window without focusing it (macOS posts to the process;
  Windows uses EM_REPLACESEL or UIA SetValue). Never use a bare `key type`, which
  types into whatever has focus (it warns on stderr).
- Click: `mouse click --app=X --find=Save` (AXPress / UIA Invoke, Toggle,
  Select, ExpandCollapse; no pointer move, and it works when the window is
  covered). Never use `mouse click X Y`.
- Read: `window text --app=X`, `find --app=X --text=T`. Neither raises the
  window; `--raise` (needed only to OCR a covered window) opts in.
- Focus-free first, then the foreground: when a window has no focus-free
  route (Paint, a WinUI app with no editable field, Chrome keystrokes on macOS),
  `key type --app` / `mouse click --find` take the foreground for the moment
  they need it and hand the front window and the pointer back afterwards.
- Polite: anything that takes focus or moves the pointer first **waits** while
  the person is typing or moving the mouse (idle 5 s), up to 60 s
  (`AOS_POLITE_WAIT`), and only then gives up with **exit 5**. `--force` /
  `AOS_FOCUS=allow` skip the wait; use them only when the owner asked.
- `aos obs focus` lists every focus-taking call and the agent behind it.

## Read the exit code

- **0** — worked.
- **1** — ran and failed, or a deliberate "no": `battery present` on a desktop,
  `network wifi` on ethernet, `remote url` with nothing running. Often not an error.
- **2** — refused before doing anything: the command needs a display this machine
  lacks, or is not supported on this platform. The message says which.
- **3** — not found, or a watch timed out: `find` / `draw --find` could not find
  the window or the text; `tab focus` / `tab close` found no matching tab;
  `watch ... --timeout` ran out before its condition was met.
  The message lists the closest labels it did see; retry with one of them.
- **5** — gave up politely: the command needed focus or the pointer and the
  person kept using the machine for the whole wait (60 s). Use the targeted form,
  or retry later.

Exit 2 on Linux is fixable: `aos headless start --wm` provides a virtual
display, and later commands adopt it automatically. On macOS and Windows it means
there is no logged-in session and the desktop commands cannot work at all.

## By intent

| you want to | run |
|---|---|
| see the machine | `system info`, `doctor`, `display list`, `network status`, `battery status` |
| find a window | `window list`, `window list --app=Chrome`, `window list --json` |
| place a window | `window move Chrome --zone=1B` · `--at=x,y,w,h` · `--monitor=2` · `window resize Chrome --w=900 --h=500` |
| save / restore a layout | `window save P` captures every window · `window arrange P` (or `-` for stdin JSON) puts them back |
| tabs (browsers, terminals) | `tab list --json` (id, title, url, cwd) · `tab focus --url=github.com/x` · `tab open URL --app=Chrome` · `tab open --app=Ghostty --cwd=D --command=C` · `tab send --id=ID --text=T` · `tab close --id=ID` (exit 3 = no such tab) |
| the page in a browser tab | `tab read --id=ID` (markdown, refs like `[e8] Send (button)`) · `tab type --id=ID --element=e7 --text=T --enter` · `tab click --id=ID --find=Send` · `watch tab --id=ID --match=T --timeout=5m` (no focus taken; `--url=web.whatsapp.com` or `--title=T` instead of `--id`) |
| focus / wait | `window focus Chrome` · `launch Chrome --wait` · `window wait Chrome --timeout=5000` |
| capture | `capture screenshot` · `--monitor=2` · `--app=Chrome` · `--region=x,y,w,h` · `--out=path` · redact in the file: `--cover=x,y,w,h` · `--cover-app=Preview` · `--cover-find=ghp_` (fail closed: exit 3 / 1 and no file if a cover cannot be placed) |
| read all text of a window | `window text Chrome` · `window text --focused --max-chars=4000` · `--json` (role, value, bounds) · `--source=ocr` (AX/UIA/AT-SPI first, OCR fallback) |
| find a control by name | `find --app=X --text=Allow --role=button --json` → Bounds + Center (exit 3 = not there) |
| point the human at it | `draw --app=X --find=Allow --text="Click Allow"` · `draw --at=x,y` · `--rect` · `--mouse` · `--detach` + `draw stop` · `--preview=out.png` |
| hide something on screen | `draw cover --app=Preview --detach --id=scan` (whole window, follows it) · `--rect=0,0,40%,100%` inside it · `--find=ghp_` · `--color=#1e40af --text="Hidden"` · `--preset=private` · `--block-input` · `draw cover list` / `update --id` / `stop --id` |
| click and type | `mouse move X Y` · `mouse click X Y --double` · `key type "text" --app=TextEdit --verify` (focus-free; `--focus` to force focus) · `key press enter --app=TextEdit` · `mouse click --app=Calculator --find=7` |
| files | `file read P --lines=10:40` · `file write P text` · `file list D --json` · `file stat P` · `file delete P --recursive` |
| run something | `exec capture -- <cmd>` (JSON: stdout, stderr, exit) · `exec run` (streams) · `exec shell "a \| b"` |
| running processes | `process list --json` · `process find X` · `process kill <pid\|name>` — kill by name refuses when ambiguous |
| packages | `pkg install X` · `search` · `list` · `upgrade` — one verb set over brew, winget, scoop, choco, apt, pacman, yay, dnf |
| keep it running | `service create NAME --autostart --now -- <cmd>` · `start` · `status` · `stop` · `remove` · `list` |
| tell the human | `subtitle show "what I am doing" --seconds=10 [--app=Safari]` — a film-style caption that never steals focus; `draw text "..." --position=top` for a label |
| speak | `say "build finished"` speaks AND shows it as a subtitle while it plays (`--no-subtitle` for voice only; macOS `say`, Windows SAPI/OneCore voices over COM) · `say "text" -- key type --app=Notepad "hi"` speaks AND acts, waits for both (exit = the command's) · `say "..." --async` then `say wait` / `say stop` · `say voices` · `say "..." --out=x.mp3` · `subtitle show "..." --say` (caption that speaks) |
| many steps at once | `batch demo.yaml` (or inline: `batch '[launch: calc, parallel: [say: seven, click: Calculator Seven]]'`) — YAML steps in order, `parallel:` runs together; the whole file is checked first (`batch --check`); verbs: `batch verbs` |
| many steps with logic, results feeding the next call, or parallel reads | `code run prog.js --json` / `code run - --input '{...}' --json` — ONE JavaScript program calls many aos commands as `ops["window-list"]({})` (batch verb names); `Promise.all` for parallel; results are the parsed JSON (failures throw: try/catch); only the final value returns; `code check` first; no exec/shell; `references/code.md` |
| let them watch | `remote share --monitor=2` — prints a LAN URL; the person opens it on a phone |
| record a demo | ASK FIRST (monitor, audio), then `capture video start smart --monitor=N --audio=mic` … `capture video stop` → `<out>.final.mp4`; follow `references/recording-a-demo.md` |
| wait for a condition | `watch process --name=X --exit` · `watch network --until=online` · `watch tab --url=U --match=T --reload=30s` · `watch window --app=A --match=T` · `watch url U --match=T` · `watch idle --for=10m` · `watch lock --until=unlocked` · `watch battery --below=20` · `watch display --until=added` · `watch device --until=added` · `watch camera --until=free` (all exit 0 when met, 3 on `--timeout`; chain with `&&`; `references/watch-and-observe.md`) |
| react to changes | `watch clipboard --max=1` · `watch window --max=1` · `watch file P --recursive --max=1` — one JSON line per event |
| disk and network facts | `disk top` (what fills the disk) · `disk list` · `network captive-portal` · `network wifi-qr` · `network speed` · `network public-ip` |
| QR codes | `capture qr FILE` / `--monitor=N` to read · `network wifi-qr` to show one |
| share a folder | `serve files DIR [--lan] [--for=10m]` — read-only HTTP; `--lan` adds a token for a phone |
| open or raise an app | `launch Slack --or-focus` raises its open window, else launches |

`--app` and `--title` both select a window; a bare word is treated as an app name
and falls back to matching the title, so `window focus Chrome` works everywhere.

## Deeper references

`references/commands.md` is the complete, generated index of every public
command with usage and examples. Load the guide that matches the intent:

| task | read |
|---|---|
| windows, monitors, zones, layouts | `references/windows-and-layout.md` |
| visual loop, terminals, screen sharing rules | `references/automation.md` |
| find a control by its text; read all text of a window | `references/find.md` |
| browser and terminal tabs: list, switch, open, type into, close; read, type into and click a page, wait for text | `references/tabs.md` |
| point at / label things on screen, hide private things | `references/draw.md` |
| speak, with a subtitle in step | `references/speech.md` |
| run many steps from YAML (batch) | `references/batch.md` |
| one program that calls many aos commands, in parallel, with logic (code mode) | `references/code.md` |
| record a demo (the full playbook) | `references/recording-a-demo.md` |
| `capture video` flags, camera modes, events format | `references/capture-video.md` |
| files, clipboard, exec, processes, services, packages, audio, battery, network, system power (which need a yes) | `references/system-and-files.md` |
| wait for a tab, window text, URL, network, idle, lock, process, battery, monitor, device, camera or mic; clipboard / file changes; audit what ran | `references/watch-and-observe.md` |
| LAN share, headless Linux display, MCP server | `references/remote-headless-mcp.md` |
| add your own commands (adapters, plugins) | `references/extending.md` |
| WSL → Windows desktop, SSH → the person's laptop (the host) | `references/host-wsl-ssh.md` |
| macOS Accessibility + Screen Recording | `references/permissions.md` |

## Screenshots are for looking, not just saving

`capture screenshot --app=X --out=/tmp/x.png` prints the captured rect
(`900x500+100+100`). Read the PNG back to see what is on screen before clicking —
that rect is how image coordinates become click coordinates: global = origin + pixel.

## Things that will bite you

- **Destructive commands need a yes first**: `system restart` / `shutdown` /
  `logout`, `process kill`, `file delete`, `pkg remove`, `service remove`.
  See `references/system-and-files.md`.
- **`exec capture` runs a program, not a shell.** `echo` is a builtin on Windows;
  use `exec capture -- cmd /c echo hi`, or `exec shell` when you want pipes and
  globs. Put `--` before the child command so its flags are not read as ours.
- **`launch` passes unknown flags to the app**, on purpose. Only `--wait` is ours.
- **A blocking command may not return**: `watch`, `remote share`, `serve mcp`,
  `serve files`. Give a watch a condition and `--timeout`, or `--max=N`, or run
  it in the background. A watch with a condition returns by itself (0 or 3).
  They are deliberately absent from the MCP tool list.
- **Public screen sharing needs an explicit yes.** `remote share` is LAN-only.
  Anything that puts desktop control on a public URL (e.g. `windowctl remote
  --tunnel`) must be confirmed by the human every time, after saying plainly
  what it exposes.
- **`draw` blocks** for its `--duration` (default 8 s) unless `--detach`; clean
  up detached drawings with `draw stop`.
- **`file delete` refuses** a filesystem root, `$HOME`, and system directories like
  `/etc`. That is a guard, not a bug. Directories need `--recursive`.
- **Nothing is silently unavailable.** A command that cannot run here still appears
  in `commands --all`, marked, and explains itself when invoked.

## Checking the machine

```bash
aos doctor          # clipboard round trip, real screenshot, window backend,
                           # permissions, package manager — each with a fix
```

On macOS, denied permissions are the usual cause of blank screenshots or failing
input: `aos permission request`.

## Driving a different machine

Nothing here is tied to a connection, so any machine you can `ssh` to and that
has the binary works the same way — same commands, same exit codes:

```bash
ssh server aos system info
ssh server aos exec capture -- systemctl is-active nginx
ssh server 'curl -fsSL https://raw.githubusercontent.com/muthuishere/aos/main/install.sh | sh'
```

A server has no display, so the desktop commands there exit 2 with that reason.
On Linux, `ssh server aos headless start --wm` gives it one and later commands
adopt it. The audit trail lives on the machine that ran the command, so
`ssh server aos obs audit` is how you see what happened *there*.

## When the screen is on another machine (WSL, SSH)

Screen commands (`window`, `tab`, `display`, `mouse`, `key`, `find`, `draw`,
`subtitle`, `capture`/`screenshot`, `clipboard`, `launch`, `open`, `webapp`,
`audio`, `remote share`, `lock`/`sleep`, ...) run on the **host**: the machine
whose screen the person sees. Everything else (`exec`, `file`, `process`,
`pkg`, `system info`, ...) runs where you are. Output and exit codes are the
same either way; `aos doctor` shows a `host:` line. Full setup and
fixes: `references/host-wsl-ssh.md`.

- **WSL**: the host is Windows. aos runs `aos.exe` from `%LOCALAPPDATA%\aos`
  (install.sh inside WSL puts it there) and translates paths, so
  `aos screenshot --out=~/s.png` lands in WSL.
- **SSH**: on the person's machine run `aos serve mcp --socket=~/.aos/serve.sock`
  and add `RemoteForward /tmp/aos-%r.sock %d/.aos/serve.sock` to that host's
  entry in `~/.ssh/config` (`%d` = home; ssh does not expand `~` there). Files given with `--out` come back over the socket;
  streams (every `watch`, `serve files`, `remote share`) and local input files are refused with a reason.
- Override with `--host=local|windows-host|<socket>`, `AOS_HOST`, or
  `host = ...` in `~/.config/aos/config`. If the host cannot be reached the
  command fails with the fix; it never quietly acts on the wrong screen.

## Serving it to another agent

```bash
aos serve mcp        # prints the URL and a per-run token; both are needed
```

The server refuses any request without the token, as a bearer header or `?t=`.
Loopback is not a permission. `AOS_MCP_TOKEN` pins one across restarts.

GUI tools are exposed only when the machine has a display (`--gui=on|off|auto`),
because offering a tool that cannot run is worse than not offering it.

## Adding commands

Two ways, both discovered automatically and both exposed over MCP:

- **Adapter** — JSON in `~/.config/aos/adapters/`, wrapping a command line.
  `aos adapters example --write` writes a starter.
- **Plugin** — any executable named `aos-<group>-<name>` on PATH, describing
  itself in `# aos:summary=` comment headers.

Neither can shadow a built-in command. Full guide: `references/extending.md`.

## What was asked of this machine

```bash
aos obs audit --since=24h   # what was run, oldest first — the audit trail
aos obs focus               # who took (or was refused) focus / the pointer, and which agent
aos obs audit --source=mcp  # only what agents asked for
aos obs summary             # is this being used, and by what
aos obs stats               # p50/p95 and failure rate per route
aos obs export              # OTLP JSON
```

Spans record the route, exit code, duration and the *count* of arguments — never
their contents.

## The skill keeps itself current

Every aos command (except `skill install/uninstall` and help) checks that this
skill is installed and matches the binary, and refreshes it if not, saying so in
one stderr line. `AOS_NO_SKILL_AUTOINSTALL=1`, or `aos skill uninstall`, turns
that off; `aos skill install` turns it back on.
