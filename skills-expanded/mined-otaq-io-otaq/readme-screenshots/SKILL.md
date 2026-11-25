---
name: readme-screenshots
description: Refresh Otaq's README.md and its screenshots in docs/images/ from the real running app. Sets up a throwaway demo project (its own OTAQ_HOME, a small git repo, tickets, a ticket with a Plan of pieces, real Claude Code agents), stages a board with work in every column, captures the app window on macOS, then updates the README text and images to match. Use this whenever the user wants new or updated README screenshots, says the screenshots or README are out of date, wants images of the app for docs, a release, a launch post or the website, or asks to "show the app" in the README, even if they don't mention the demo project or screenshots by name.
---

# README screenshots for Otaq

Real screenshots beat mockups: the README should show the app as it is, with real agents doing real work. The
catch is that a live board takes some staging, and macOS, the sandbox and Claude Code's own environment each have a
trap. This skill is the route that works; the scripts in `scripts/` hold the fiddly parts.

**Cost and duration:** about 15–20 tickets run real `claude` agents on the user's plan (each takes 1–3 minutes),
and the whole session takes 15–45 minutes. Say so before starting if the user hasn't asked for it explicitly.

`S=.claude/skills/readme-screenshots/scripts` below. Demo data lives in `$OTAQ_DEMO` (default `/tmp/otaqdemo`),
never in `~/.otaq`, so the user's own boards are never touched.

## 1. Preconditions

- **macOS only** (`screencapture`, CoreGraphics). Commands that start the service, open the app, click or capture
  need the sandbox off (`dangerouslyDisableSandbox: true`); without it the agents can't save their conversations and
  `screencapture` can't see the screen.
- **Screen Recording permission** for the terminal that runs Claude Code: `swiftc -O $S/window.swift -o
  /tmp/otaqdemo/bin/window && /tmp/otaqdemo/bin/window --access`. If it says NOT allowed, macOS has just shown its
  prompt: ask the user to allow it in System Settings → Privacy & Security → Screen & System Audio Recording. A
  terminal app may need a restart to pick it up (`claude --continue` resumes). Clicking needs no Accessibility
  permission: the scripts post CoreGraphics events.
- The user's `claude` CLI is logged in; Node (24 per `.nvmrc`; 20 has worked too) and Rust are installed (the app
  builds from this checkout).
- Keep `$OTAQ_DEMO` short: the service socket path must fit in ~104 bytes, so a deep scratchpad folder fails
  with "path must be shorter than SUN_LEN".

## 2. Start the app and seed the demo

```sh
zsh $S/start.sh
```

It builds `otaq` and the app, starts the demo service with a clean environment, seeds the demo on the first run
(`seed.sh`: the `pocket-notes` repo, project NOTE, 13 tickets including "Tags" NOTE-7 and "Notebooks" NOTE-13, each
with a Plan of four pieces; nothing starts yet), then starts Vite and opens the window. Seeding comes before the window because the app
chooses between onboarding and the board once, at launch: if you ever see the onboarding wizard, run `start.sh` again.

Why `start.sh` does what it does, in case something needs adjusting by hand:
- **Clean environment** (`env -i`): a service started from inside Claude Code inherits `CLAUDE_CODE_CHILD_SESSION`
  and passes it to every agent; their terminals then say "Transcript saving is off", Resume fails with
  "conversation not found" and token counts stay at 0. If you see that warning in an agent terminal, the service was
  started wrong: stop it and run `start.sh` again.
- **No `npm run tauri dev`**: its watcher restarts the app whenever any file in the repo changes, and other sessions
  commit while you shoot. The app runs from a fixed debug build against the Vite server instead.
- **The service and the app are built from the same tree**, so no "Service update ready" banner appears in shots.

## 3. Stage the board

The board is worth capturing when every column has something in it and something is visibly happening. Agents on
this demo finish in about a minute, so stage it in waves rather than starting everything at once:

There is no Ready for Dev column: a move to `dev` is Start, and a ticket that waits for another (NOTE-3, NOTE-9) waits
at the top of Dev ("Waits for NOTE-1 to merge") and begins by itself once that one is merged. `otaq list` still says
"Ready for Review" for a ticket in Review.

1. Wave 1: `NOTE-1`, `NOTE-2`, `NOTE-4`, `NOTE-5` and `NOTE-3` to Dev. Wait:
   `zsh $S/wait.sh "Ready for Review" NOTE-1 NOTE-2 NOTE-4 NOTE-5` (about 5 minutes). An agent may ask a question
   (`wait.sh` stops on "Asks you"): answer it in the app (the card's **Answer**, then **Send answer**).
2. Merge in two passes, because a ticket only starts once the tickets it waits for are merged:
   `zsh $S/merge.sh NOTE-1`, then `wait.sh "Ready for Review" NOTE-3`, then `merge.sh NOTE-3`. Done fills (it shows
   as the link "Done 2 →" under Review). Tickets left in Review fix their conflicts with main by themselves.
3. Move `NOTE-7` (Tags) to Dev. Its agent is in charge: it reads the Plan and may start **helpers**, one per piece,
   each in its own worktree; the card says "Working · 3 helpers" and the ticket's Overview shows each piece's
   status next to the Plan. Open the ticket and capture its Overview while at least one helper is working and one
   is merged, as the plan shot. A helper's question goes to the agent in charge first; one it passes on shows in the
   Needs you strip as "NOTE-7 · 7.2 asks". Leave NOTE-7 running; it reaches Review as one ticket.
4. Wave 2, right before the board shot: `NOTE-8`, `NOTE-9`, `NOTE-10`, `NOTE-12` and `NOTE-13` (Notebooks) to Dev.
   Capture within the next minute or two, while cards still say Working or Checking.

The first approve and first question show one-time hints ("Your turn: review", "That was your flow", "Work starts
here") and a "Help improve Otaq?" banner: press their **Got it** / **No thanks** before the shots.

If a card shows **Start failed**, retry it: `ticket.retry_start {"key":"NOTE-8"}`. `wait.sh` stops early and
names the ticket when that happens.

The requests:

```sh
R=(python3 -I $S/otaq_req.py)                                           # an array: zsh doesn't split strings
"${R[@]}" ticket.move '{"key":"NOTE-1","target":"dev","confirmed":true}'      # dev is Start; also backlog, done
"${R[@]}" ticket.pin '{"key":"NOTE-2"}'
"${R[@]}" ticket.start_from_scratch '{"key":"NOTE-1","confirm":true}'          # after "Resume failed"
python3 $S/otaq_req.py theme otaq-dark                                  # otaq-light, daylight, tokyo-night, dracula, ...
```

`theme <key>` sets Appearance to Light or Dark (whichever the theme is) with that theme, so the shot doesn't follow
the system; put it back to Match system by hand if you care.

"Conflicts with main" on review cards is normal here (the tickets touch the same few files) and looks realistic;
leave it.

## 4. Capture

```sh
zsh $S/shot.sh /tmp/otaqdemo/shots/board.png                       # just capture
zsh $S/shot.sh /tmp/otaqdemo/shots/x.png 1414 70                   # click (1414,70) in the window, then capture
zsh $S/shot.sh /tmp/otaqdemo/shots/x.png scroll 180 600 -15 wait 2 # scroll a column down, wait, capture
```

Coordinates are pixels in an earlier shot of the same window (window-relative; the window is 1440×900 by default
on a 1x display). `shot.sh` first brings the demo app forward by its pid (`osascript`, no click, so an open dialog or
menu stays open); at the end it moves the pointer below the window, because a hovered card dims the rest of the board.
Look at each shot with Read before moving on: a click can still miss, a panel may be open, a tooltip may show, and
once in a while macOS hands back a scaled-down window (`shot.sh` warns about the size): just capture again.

Shots the README uses (keep these names so the README's image links stay valid):

| File | What it shows | How |
|---|---|---|
| `board.png` | the hero: Otaq Dark, cards in every column, a question in Needs you and tickets in Your review, something working (NOTE-13's helpers) | theme `otaq-dark`, all panels closed, right after wave 2 |
| `board-light.png` | the same board in a light theme (Daylight or Otaq Light) | switch theme, capture again |
| `terminal.png` | an agent's Claude Code session | **Review** on a card in Review; the sheet's **Session** tab (Agent) |
| `review.png` | what the agent did, the checker's report, the bar with Approve & merge into main | same sheet, **Overview** tab, top |
| `diff.png` | the code diff with the file list | **Changes** tab; collapse Validation report then Agent summary, then expand the sheet (⤢ in its header) |
| `plan.png` | a ticket's Overview with its Plan: the pieces in order, each with its helper's status | step 3 above |

Useful places in the default 1440×900 window: the sheet's close ✕ at (1234, 116), expand ⤢ at (1194, 116); its tabs
Overview · Session · Changes · History sit on one row at y≈264 (Session x≈400, Changes x≈510). The project's
Settings is at (219, 70) beside Board and Files, the app's Settings is the gear at the foot of the rail (32, 870),
and Running in the header (852, 21). Collapse sections **bottom-up**, so the ones above don't move before you click
them. Recheck against a fresh shot: layouts change between versions, so treat these as hints, not truth.

Things to keep out of shots: the "Service update ready" banner, "Transcript saving is off" in a terminal, personal
paths outside `/tmp/otaqdemo`, one-time hints. The Running popover and the usage chip show the user's real usage;
mention it when you present the shots.

An installed Otaq that is open at the same time is never captured: `shot.sh` and `start.sh` find the window of the
demo's own `otaq-app` by its process.

## 5. Update the README

Copy the picks into `docs/images/` with the names above, then read `README.md` against the shots and the current code:

- Every caption and sentence should describe what the image actually shows (ticket keys, panel names, button labels).
- Check claims against the code, not memory: CLI commands (`target/debug/otaq --help`), themes
  (`crates/otaq-view/src/theme.rs`), setup steps (`crates/otaq-desktop/README.md`). Features change between shoots.
- Link only to files git tracks. `decisions/`, `DESIGN.md`, `SDD.md`, `design-briefs/`, `tickets/` and `prompts/` are
  the maintainer's local notes and are not in the repository. `zsh $S/check_links.sh` checks every link and image.
- Images are ~250 KB each as captured; that's fine for six or so.

## 6. Clean up and hand over

`zsh $S/stop.sh` stops the demo's agents, the app and Vite, so nothing keeps spending the user's plan. It keeps
`/tmp/otaqdemo` for a reshoot; `rm -rf /tmp/otaqdemo` removes it.

The demo stays out of `~/.otaq`, but not entirely out of Claude Code's own config: adding the project records
`/private/tmp/otaqdemo/pocket-notes` as a trusted folder in `~/.claude.json`, and every agent run adds Claude Code's
usual per-folder entries there. They're harmless; mention them when you hand over rather than editing that file,
which every running `claude` (including this session) rewrites.

Tell the user which shots you took and what changed in the README, and flag anything odd you noticed in the app while
shooting: this is a real end-to-end run, and it finds real bugs. Commit or push only when the user asks.
