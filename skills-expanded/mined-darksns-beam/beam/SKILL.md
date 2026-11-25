---
name: beam
description: Drive Chrome as text through the `beam` CLI — read a page's structure, fill forms, click, navigate. Use it for data entry in admin panels (WordPress/ACF), filling forms, checking pages, structured scraping, UI QA. No screenshots: all text, one round trip per operation.
---

# Beam

CLI: `beam` (on the PATH: from the `beam-chrome` plugin, or linked into
`~/.local/bin` by `install.sh`). It talks to a local hub on
127.0.0.1:8777 that relays commands to the user's Chrome extension — so it works
**inside the session they are already logged into**, with no credentials and no
separate profile.

The hub starts by itself on the first command. If the extension does not answer,
the error is `extension not connected`: ask the user to open the Beam panel from
the Chrome toolbar icon (it shows `!` when disconnected) and press
**Reconnect**. If Beam is not in Chrome at all, run `beam extension`: it copies
the extension to `~/.beam/extension` and prints the three steps to load it,
which the user does by hand. If a command prints `note: the running hub is …`,
run `beam server --stop` once. `beam ping` returns the id, the version and the panel url.

## How to work

Do not use `beam shot` by default. Screenshots are for when the user wants a
visual check or a widget is undecipherable from the DOM (canvas, charts,
builder layouts) — and then `beam shot --marks`, so the picture carries refs.
See **Visual pages**. The normal flow is:

1. `beam open <url>` once. It uses a Chrome window of its own that stays
   unfocused, and every later `open` reuses that same tab. Do not pass `--new`.
   Do not pass `--focus` unless the person asked to look at it. Do not
   `beam close` when the task is done: Beam closes the window by itself after
   10 minutes without commands, and when the Claude Code chat ends.
   Two Claude Code chats already get two windows: the CLI names the session
   from `CLAUDE_CODE_SESSION_ID` (a Cursor chat uses `CURSOR_CONVERSATION_ID`).
   Do not export `BEAM_SESSION` unless you want a stable name, or one window
   shared across chats. The same name shares a window. A terminal with none
   of these set shares `default`.
2. `beam snap` (or `beam fields`) to read the page **once**
3. act with `set` / `do`, which do everything in a single round trip
4. re-read only what matters (`beam snap --sel ...`) to verify

`beam use <id>` is only for a tab the person already has open, and it does not
bring that tab forward. `beam focus` does, and only when they ask. A command
with nothing bound fails instead of attaching to whatever they are looking at.

## Reading

```
beam snap    [--sel CSS] [--max N] [--hidden] [--boxes]   # interactive elements, with @n refs
beam outline [--sel CSS] [--depth N]            # the HTML structure tree
beam fields  [--sel CSS] [--hidden] [--vlen N]  # every form field, as JSON
beam text    [--sel CSS] [--max N] [--from N]   # readable text
beam html    [--sel CSS] [--max N]              # raw HTML (use it last)
beam info | tabs | frames | sessions | profiles
beam network [filter] [--type xhr,doc,js,css,img] [--method M] [--failed] [--last N] [--clear]
```

`snap` returns lines like:

```
h2 Hero
@4 input:text "Kicker" = "New collection 2026"
@5 input:text "Title" = "Woven roots" *
@6 textarea "Description" = "There is a moment…"
@7 select "Status" = "Draft" {Draft|Published}
@8 button "Update" #publish
```

`*` = required, `(hidden)` = present but not visible (fill it anyway: handy for
closed ACF tabs), `{…}` = a select's options. A password field reads
`<hidden, N chars>`: Beam can fill it but never reads the value back, in
`snap`, `fields`, `html` or a `--dry` diff.

`@n` refs last until the next `snap` or a page change; after navigating, snap
again. For stable references use `name=` or `css=`.

`beam fields` returns **whole** values; on screen they are cut at 200 characters
with the real length shown, and `--json` gives them in full. Never conclude a
field is empty or short from a shortened output.

### Iframes

`beam frames` lists the injectable frames, including the ones that do not show
up in the navigation history (such as the WordPress editor canvas).

```
beam snap --frame all      # reads every frame, refs become @<frame>:<n>
beam click @583:12         # the frame comes from the ref, no extra flag
beam set --frame 583 @payload.json
```

`--frame all` is for reading only: to act, name one frame. Frame ids change when
the application recreates them — re-read them, do not reuse them.

A frame that does not answer within 8 s is left out: `--frame all` lists it under
`skipped`, and `beam frames` shows it as `(not injectable: timeout)` with its id
and url. A command that hangs for more than 45 s (or `--timeout` + 15 s) answers
with an error and frees the session, so no `reloadext` is needed.

### Network

`beam network` lists the requests made by the bound tab (and Beam's own tab)
since it was bound: status, method, type, time, url. Bodies and headers are not
captured. `--type xhr` keeps fetch/XHR calls only, `--failed` keeps errors and
status >= 400, `--clear` empties the log after printing it. To see what one
action calls: `beam network --clear`, act, then `beam network --type xhr`.
Recording starts when a tab is bound: the very first `open` of a new Beam
window misses its initial load, so `beam reload` if that matters.
The log is off until the person turns it on: if `network` answers `the network
log is off`, ask them to open the Beam panel and press **Enable network log**
(Chrome asks once). Do not work around it.

## Acting

```
beam open <url> [--new] [--focus]   its own window, unfocused; reuses that session's tab
beam open <url> --incognito         the same, in an Incognito window (no logins); sticky until `beam end`
beam end                            close this session's window and forget the session
beam focus                          bring the Beam window forward
beam nav <url> | reload | back | forward | close | use <tab> [--focus]
beam click <target>
beam hover <target>
beam fill <target> <value>
beam select <target> <value>         # by value or by visible label
beam check <target> [on|off]
beam press <Key>
beam wait [--sel CSS] [--text T] [--timeout ms]
beam scroll [--sel CSS] [--by N]
beam upload <target> <url|file>      # a file into an input[type=file]
beam drop <target> <url|file>... [--text T] [--at x,y]   # onto a dropzone
beam drag <target> <to> [--at x,y] [--from x,y] [--mode auto|html5|mouse]
beam shot [<target>] [--marks] [--hires] [--out file.jpg]  # only when truly needed
beam viewport [375 | 375x812 | mobile | tablet | desktop]   # resize for responsive checks
beam reloadext                       # reload the extension after editing it
beam extension                       # copy the extension to ~/.beam/extension, to load unpacked
```

**Targets**: `@12` · `css=.my-class` · `text=Update` · `label=Kicker` ·
`name=acf[field_abc]` · `title=Heading Settings` · `xy=120,40` (viewport point). A bare string is tried as CSS,
then as text, then as a label.

## Batch — the fast path

Filling many fields in one round trip:

```bash
beam set '{"label=Kicker":"New collection 2026","name=acf[field_bb]":"Woven roots"}'
beam set @hero-copy.json        # the same object, from a file
beam set --dry @hero-copy.json  # preview: shows the diff, writes nothing
```

Always go through `--dry` before a bulk write.

Mixed sequences (tab clicks, waits, fills):

```bash
beam do '[
  {"op":"click","target":"text=Identity"},
  {"op":"wait","sel":".acf-field[data-name=identity_title]"},
  {"op":"fill","target":"label=Title","value":"Made by nature."},
  {"op":"snap","sel":".acf-fields"}
]'
```

A failing step stops the sequence and reports the steps already done; put
`"optional": true` on steps that may be missing.

## Drag & drop

```bash
beam drag "css=#list li:nth-child(4)" "css=#list li:nth-child(1)"
beam drag "css=#r1 .handle" "css=#r3" --at 40,28     # drop near the bottom of r3
beam drop "css=.uploader" ./hero.jpg https://example.com/b.pdf
```

`auto` presses the source, then uses HTML5 drag events if it is (or became)
`draggable`, pointer moves otherwise. If the result does not move, retry with
the other `--mode`. `--at x,y` picks where on the target to let go — the top
or bottom of a row decides before/after. `drag … accepted: false` / `drop …
did not accept it` means no handler took it: target the zone itself, or the
list container. Check the outcome by reading the list back (`beam text --sel`).
Reordering and dropping are writes like any other: in a CMS, the new order is
only kept after a save, which you ask about first.

## Visual pages

```bash
beam snap --boxes            # every line gets [x,y wxh]; canvas/svg/img/video listed
beam shot --marks            # screenshot with @n labels drawn, plus the legend as text
beam shot css=#chart         # crop to one element
beam click css=#chart --at 167,102   # a point inside it, from its top-left corner
beam click xy=640,380        # whatever is drawn at that viewport point
```

The refs drawn by `--marks` are live: `beam click @12` right after works. To
pick a point inside a canvas, `shot <target>` it (the crop has 8 px of margin
around the element) and pass the point with `--at`.

## WordPress / ACF

- Fields in inactive ACF tabs are already in the DOM: fill them without clicking the tab.
- The sturdiest identifier is `name=acf[field_xxx]`, which `beam fields` shows for every field.
- TinyMCE wysiwyg fields are handled (plain text → `<p>` paragraphs).
- Repeater rows are added with a click: `{"op":"click","target":"css=[data-name=stops] a[data-event=add-row]"}`.
- Images and files can **not** be set from here: they go through the media library.
- Do not click "Update"/"Publish" on your own initiative: ask first — saving is visible to the outside world.

### Beaver Builder / VamTam

The wrench is not in the page until the pointer is over the module. Beaver
Builder builds the overlay on `mousemove` (it checks `clientX`/`clientY`), and
the control is a `<span title="Heading Settings">`, not a button — `snap` never
lists it. The layout usually lives in the builder iframe.

```bash
beam frames
beam hover --frame ID "css=.fl-module"          # first module; narrow the selector to pick one
# @ID:n span "Heading Settings" .fl-block-settings
beam click --frame ID "title=Heading Settings"  # or click the @ID:n from hover
beam snap                                       # the settings form opens in the parent frame
```

`hover` also forces `:hover` styles (a synthetic event does not). One hover
replaces the previous one. The Beam window's tab is already the active tab of
that window, so it has layout without being focused. `beam focus` only if the
person wants to watch. If hover says there is no layout, the bound tab is one
of theirs and it is not the tab on screen: do not switch to it.

In one round trip, inside the iframe:

```bash
beam do --frame ID '[
  {"op":"hover","target":"css=.fl-node-abc.fl-module"},
  {"op":"click","target":"title=Heading Settings"}
]'
```

## Parallel sessions

Each `BEAM_SESSION` (or `beam --session <name>`) owns one unfocused window and
reuses one tab inside it. With no name, a Claude Code or Cursor chat is already
its own session, taken from the chat id. Set a name when the window should
outlive that chat, or when two chats should share it. Commands in one session
never navigate, activate, or `use` a tab that belongs to another session
(`--force` is the override, same as the tab guard). Names are `[A-Za-z0-9._-]`,
up to 40 characters.

```bash
export BEAM_SESSION=pages
beam open https://example.com/wp-admin
```

`beam sessions` lists them. `beam tabs` marks each owned tab with `beam:<name>`
and `*` for the tab this session is bound to. Do not close the tab when the
task is done: a session with no command for 10 minutes loses its window, and
the next `beam open` makes a new one. `beam end` closes it now.

Chrome profiles: run `beam profiles` before the first `beam open` of a task.
- The person named one ("in my work profile"): pass `--profile <name>` on that
  `open`. If the name is not listed, ask them to open Chrome on that profile
  and name it in its Beam panel (the **profile** field): Beam cannot open a
  profile itself.
- One profile listed, or `BEAM_PROFILE` is set: no flag, no question.
- Two or more listed and none named: ask the person which one to use, listing
  the names (`#id` for an unnamed one), and wait for the answer before
  opening anything. Do not guess from the site: a profile without the login
  shows a login page, not an error.

The session's later commands follow the profile of that `open` until
`beam end`, so ask once per task, not per command.

`beam open --incognito <url>` only when the person asks for Incognito (a
logged-out check, a clean cart, no cookies). The session stays Incognito until
`beam end`; later `open`s need no flag. If it answers `Beam is not allowed in
Incognito`, ask the person to turn on **Allow in Incognito** for Beam in
`chrome://extensions`: do not fall back to a normal window. All Incognito
windows share one cookie jar.

## The tab guard

Beam stays bound to the tab named by `use`/`open`/`nav` for this session.
`open` keeps that tab in the session's own unfocused window and reuses it. If
the person moves that tab elsewhere, every **write** command is refused and the
new url is reported: re-bind with `beam use <id>` after looking at `beam tabs`.
`--force` exists but is only for after you have checked where you are writing.
A second session does not touch this one. Do not close the Beam tab at the end
of a task.

## Limits

- Does not work on `chrome://` pages, the Web Store, or built-in PDFs.
- No virtualized lists (React recycling nodes).
- `drag` and `drop` send synthetic events (`isTrusted` is false): a page that
  checks it, or drags inside a cross-origin iframe, will not follow.
- `shot <target>` and `--marks` work in the main frame only.
- A tab that is not the selected tab of its window has no layout. Beam's own
  window keeps its tab selected, so hover works there without focusing the
  window. `beam focus` is how a person asks to see it.
- `viewport` resizes this session's own window, so media queries see a real
  width. Below Chrome's narrowest window (about 500px) it zooms the tab
  instead, so `innerWidth` is still the width asked for. No device emulation:
  no touch events and no mobile user agent. Snap again after a resize: the
  layout, and so the refs, may have changed.
- If a click causes a full navigation, wait with `beam wait` and snap again: the
  previous refs are gone.
