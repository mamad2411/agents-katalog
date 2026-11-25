---
name: bx
description: Drive the user's own running Chromium browser (Brave and others) from the shell, in a named profile. Use when a task needs a logged-in session in the user's browser - reading a dashboard, filling a form, checking a page, taking a screenshot - or when the user says "in my browser", "in my <name> profile", names their browser, or says "bx".
---

# bx

`bx` drives the user's real, running browser over the DevTools Protocol.
Tabs live in the user's profiles with their logins and cookies. Run
`bx list profiles` to see the profile names; never guess them. Treat every
action as something the user did with their own hands.

## Rules

- Pass `-o json` when you parse output. Every command supports it.
- Never prompts. Exit codes: 0 ok, 1 user error (bad tab ID, unknown
  profile), 2 bad flags, 3 browser failed or unreachable, 4 permission.
- Exit 4 needs the human: either the terminal app lacks Full Disk Access,
  or nobody clicked Allow in the browser. Tell the user which; don't retry in a loop.
- References are exact: profile display name or folder name, and the full
  tab ID from `bx list tabs`.
- The first command after the browser starts shows an Allow dialog in the
  browser. Tell the user to click it. Later commands reuse that connection.
- If remote debugging is off (exit 3 saying so), ask the user to quit the
  browser, then run `bx setup`. Never quit their browser yourself.
- If the user names a browser ("in Chrome"), pass `--browser chrome`. Check
  `bx list browsers` when unsure which one bx will drive.
- `--browser <name>-agent` (or `BX_BROWSER`) drives a separate agent browser
  started with `bx launch`: no Allow dialog, but its own logins. Use it only
  when the user set it up or asks for it.
- Ask before submitting forms, sending messages, buying, deleting or
  changing settings on the user's behalf. Reading is fine.
- When a page asks for something you don't have, such as an address, a tax
  ID, a phone number, a sign-in or a code, stop and ask the user for it.
  Never make up their details. Once they give them, fill them in and go on:
  giving them is their go-ahead for that form.
- `bx close tab` needs `--yes`. Close only tabs you opened.

## Commands

```
bx list profiles
bx list tabs [--profile <name>]
bx open <url> [--profile <name>]          # the new tab's ID and the page's interactive
                                          # elements; profile defaults to the one last used.
                                          # Name one when the task belongs to a particular account.
bx show tab <id>
bx snapshot <tab> [--out <file>]          # elements with refs: e12 button "Save"
          [--interactive] [--within <ref>]  # only controls and headings; one part of the page
bx read <tab> [--selector <el>] [--format text|html]
bx screenshot <tab> [--selector <el>] [--full] [--out <file.png>]
bx eval <tab> '<js expression or () => function>' | --file <script.js>
bx wait <tab> --text <text> | --selector <el> [--gone]
bx goto <tab> <url|back|forward|reload>
bx click <tab> <el> [--double]
bx hover <tab> <el>
bx drag <tab> <from-el> <to-el>
bx fill <tab> <el> <value> [<el> <value> ...]
bx type <tab> <text> [--into <el>] [--submit Enter]  # key by key
bx key <tab> <key>                        # Enter, Escape, Tab, ArrowDown, Meta+a
bx batch <tab> '<json steps>' | --file <f> # several actions in one call
bx start "<title>" [--mode watch] [--pace human] [--typing keys]  # begin a task; the pointer shows the title
bx done ["<summary>"]                     # once, when finished; lists the tabs the task opened
bx upload <tab> <el> <file> [<file> ...]
bx download <tab> <el> [--out <dir>] [--name <file>]  # click a download, wait for the
                                          # file; prints its path. Default ~/Downloads
bx pdf <tab> [--out <dir>] [--name <file>]  # save the page as a PDF (receipts with no download)
bx mouse <tab> click|double|right|move|wheel <x> <y> [<dx> <dy>]  # at a point, in
                                          # screenshot pixels: canvas, maps, grids
bx dialog <tab> accept|dismiss [--text <reply>]
bx front <tab>
bx close tab <id> --yes
bx cdp <Method> [<json-params>] [--tab <id>]
bx console <tab> [--errors] [--since <id>] [--limit <n>]   # console, exceptions, failed loads
bx network <tab> [--errors] [--since <id>] [--limit <n>]   # requests: status, type, time
bx network <tab> --request <id>           # one request's headers and bodies
bx storage <tab>                          # cookies, localStorage, sessionStorage
bx storage <tab> set|delete|clear cookies|local|session [<name> [<value>]]
                                          # the user must Allow it in a dialog; tell
                                          # them what and why first
bx mock <tab> <url-pattern> [--status <n>] [--body <text>] [--type <ct>]
bx mock <tab> --remove [<url-pattern>]    # mocks last until removed or bx stop
bx performance <tab> [--reload]           # Web Vitals, long frames, slow resources
bx emulate <tab> [--viewport 390x844@3,mobile] [--network offline|slow-3g|fast-3g]
          [--cpu 4] [--geo <lat>,<lon>] [--color dark|light] [--reset]
bx status | bx stop | bx doctor | bx setup | bx launch
bx list browsers                          # installed, running, debugging on, default
bx use <browser>                          # set the default browser
```

An `<el>` is a ref from the tab's latest `bx snapshot` (such as `e12`), a
role and name exactly as a snapshot line shows them (`'button "Next"'`,
`'textbox "Name" #2'` for the second match), or a CSS selector. A role and
name waits up to 10s for the element to appear. `--timeout <dur>` (default 30s) bounds waits.
A snapshot also shows what is inside iframes (an embedded editor, a
document viewer, a payment form), indented under their `Iframe` line.
Refs, role and name, and CSS selectors reach in there; a CSS selector looks
in the tab's own page first. To run a script inside a frame, pass the
`Iframe` line's ref: `bx eval <tab> '<js>' --frame e15`.

## How to work a page

1. `bx snapshot <tab> --interactive` first. It lists what you can click or
   type in, plus headings, with refs, names, values and states like
   `[checked]`. On a content page it is 3-9x smaller than the full snapshot.
   Use the full snapshot, or `--within <ref>` for one region, when you need
   the text around the controls. Prefer either to a screenshot: they are
   text, and their refs are exact.
2. Act with refs: `bx click <tab> e12`, `bx fill <tab> e4 'text' e7 Green e9 true`.
   One fill call sets several fields: text fields are typed into, a select
   takes an option's value or visible text, a checkbox or radio takes true
   or false.
3. Read the action's result. Every action waits for the page to settle,
   then reports `navigated`, `url`, `title`, `new_tabs` and `dialog`, and,
   once the tab has a snapshot, `changes`: what appeared (`+ e61 button
   "Next"`), disappeared (`- e40 e41`) or changed (`~ e27 combobox
   value="India"`). Validation errors show up there too. Refs stay the same
   while an element stays on the page, so you rarely need a new snapshot.
4. Take a new snapshot after a navigation or a big page change. A ref from
   an old snapshot fails with exit 1 and says so.

## Work in few calls

Each call is a round trip through the model, and those round trips, not
the browser, are where most of a task's time goes. So understand the page
once, then send the plan as one call:

- `bx batch <tab> '[...]'` runs steps in order and stops at the first
  failure, reporting `done` (how many ran), `failed` and `error`. Steps:
  `{"action":"click","element":"e12"}`, `{"action":"fill","element":"e4","value":"x"}`,
  `{"action":"type","text":"x","submit":"Enter"}`, `{"action":"key","key":"Tab"}`,
  `{"action":"goto","url":"..."}`, `{"action":"wait","text":"Saved"}`,
  also `hover`. A grid of cells in Sheets is one batch of type and key steps.
- Use `fill` for plain fields. Use `type --into <el>` (or a batch `type`
  step with `element`) for rich text editors (LinkedIn, Slack, Notion,
  Gmail compose), autocompletes and pickers. Text set by `eval` can look
  right yet not count; `fill` and `type` send it the way a paste does.
  In those editors each newline is a new paragraph: type one between
  paragraphs, not two.
  After typing into an autocomplete, `wait` for the suggestion, then click it.
- Elements inside shadow roots (web components, some composers and
  dialogs) work like any other: use their snapshot refs. Don't fall back to
  setting values with `eval`; the app's own state won't see them.
- To get data out of a page, write one `bx eval` that returns just the
  fields you need as JSON, rather than reading the whole page or snapshot.
- Plan across screens in one batch by naming elements by role and name:
  fill step 1, click `button "Next"`, fill step 2's `textbox "Email"`, and
  so on. Each named element is waited for, so you don't need a snapshot
  of the next screen first. Refs (`e12`) only reach what you have seen.
- After a step that changes the page a lot or loads a new one, the result
  carries the new screen (its interactive snapshot) in `changes`.

Typing into canvas apps such as Google Sheets: click a real field first
(for Sheets, `bx fill <tab> '#t-name-box' E5` then `bx key <tab> Enter` to
select a cell), then `bx type <tab> 'text' --submit Enter`. bx keeps every
tab it touches focused in the background, so the tab need not be in front.

On macOS, use Meta for shortcuts: `bx key <tab> Meta+a` selects all.

bx opens new tabs in front, scrolls what it acts on into view, and shows a pointer with a "bx" tag that says what bx is
doing (clicking, filling, pasting, reading the page, running a script,
waiting, taking a screenshot) and, in a batch, which step it is on
("3/32 · Click "Next""). Between your calls it says "Waiting for the agent...", so
the user can see you are still working. When the browser task is
finished, run `bx done "<one-line summary>"` once: the pointer shows it,
then goes away. Don't run it between steps. Begin with
`bx start "<task title>"`, so the pointer shows "Working on: <title>"
between your calls. `done` lists the tabs the task opened; they stay
open, so close the ones the user doesn't need.

When the user asks what bx did ("what did you do in my last session?",
"which pages did you open yesterday?"), read the log instead of guessing:
`bx history` lists recent sessions, `bx history previous` (or `current`,
or a session id) draws one session from start to end: its tasks, the
pages each worked on and the actions on each, with results. Inside Claude
Code or Codex a bx session is the app's own session. Over MCP it is the
`history` tool. Typed values are not in the log. The log settings are
`bx config` (MCP: `settings`); you may raise retention when the user asks,
but lowering logging is the user's call: give them the command.

Pins are tasks saved to repeat. When the user says "pin that as <name>",
run `bx history pin current "<name>"` (MCP: `pins` with action pin). When
they ask to do a pinned task again, read it with `bx history pinned
"<name>"` (MCP: `pins` action show), ask them for every value the steps
fill or choose (values are never logged), then go through its pages in
order: snapshot each and run its steps, in one batch where you can. If a
page changed, do what the step meant rather than failing.

How bx works for a task is two choices, which you make with `start` from
what the user says. Leave out what they didn't ask for: their settings
(`bx config`) then apply, full speed in the background unless they changed it.

- Mode: `fast` leaves the browser where it is, so the user can keep
  working. `watch` brings the tab you work in to the front, and follows
  you from tab to tab and profile to profile. Use watch when the user wants
  to see it: "show me", "let me watch", "in front of me", "bring it up".
  Use fast when they say "in the background", "don't disturb me".
- Pace: `full` acts at once. `human` makes the pointer glide with the real
  mouse, clicks land near the middle, a native dropdown is shown unfolding,
  and batch steps pause. Use it only when the user asks to slow down: "at
  human pace", "slowly", "step by step". Mode and pace are separate: "show
  me" is watch at full pace.

Text is pasted in one go by default (the page gets the same events as a
paste). `--typing keys` (or the `typing` setting) types key by key, for the
rare site that only reacts to key presses.

To change the user's defaults for every task, when they ask for that, use
`bx config set mode watch` (MCP: `settings`). BX_MODE, BX_PACE and BX_TYPING
in the environment override the settings for one process.

Every mode uses the same browser and logins, and all input arrives as real
(trusted) events. Screenshots and snapshots leave the overlay out.

## Dialogs

If an action opens an alert, confirm or prompt, the action returns at once
with `dialog` set, and every other action on that tab fails with exit 1
until you answer it: `bx dialog <tab> accept` or `dismiss` (`--text` fills
a prompt). Ask the user before accepting a confirm that deletes or sends.

## Example

```sh
id=$(bx open https://app.example.com --profile Work -o json | jq -r .id)
bx snapshot "$id"
bx fill "$id" e5 'search text' -o json
bx click "$id" e6 -o json | jq '{navigated, url, new_tabs}'
bx eval "$id" '() => [...document.querySelectorAll("tr")].map(r => r.innerText)'
```

`bx list tabs --profile <name>` may briefly open and close a helper tab in
that profile the first time, to learn which tabs belong to it. In
`bx list tabs` without `--profile`, PROFILE shows `?` for tabs in profiles
bx hasn't seen yet.

## Debugging a page

bx records each tab's console and network from the first time it touches
the tab (and replays console messages from before). To find why something
breaks:

1. Note where the logs end: `bx console "$id" -o json --limit 1` gives the
   last id; do the same for `bx network`.
2. Do the steps that fail (click, fill, ...).
3. `bx console "$id" --errors --since <id>` and
   `bx network "$id" --errors --since <id>` show only what those steps
   caused. `bx network "$id" --request n12` shows the failing request's
   request and response bodies, which usually name the cause.

Requests made before bx touched the tab aren't recorded: `bx goto "$id"
reload` to capture a page load. `bx emulate` lasts until `bx stop`; run
`bx emulate "$id" --reset` when done.

## Escape hatch

`bx cdp` sends any DevTools Protocol method over the same connection and
prints the raw JSON result. Without `--tab` it goes to the browser (Target.*,
Browser.*); with `--tab` it goes to that page (Page.*, Runtime.*, DOM.*).
Use it for what bx has no command for, such as Lighthouse-style audits or
DOM breakpoints.

## When something fails

Run `bx doctor -o json`. It checks that the browser is installed, profiles
are readable (Full Disk Access), remote debugging is on (the browser's
inspect page, such as brave://inspect/#remote-debugging), and the skill is
current. It also reports when a newer bx exists: tell the user, and run
`bx update` if they agree. Pass `--browser <name>` to any command to drive
a browser other than the default.

If clicks time out on a tab where the user has a DevTools window open,
ask them to close DevTools on that tab (or resume it if it is paused in
the debugger); bx reads console and network without it.

To let the user watch, start the task with `--mode watch`: every tab bx
opens or acts in is brought to the front when bx moves to it.
