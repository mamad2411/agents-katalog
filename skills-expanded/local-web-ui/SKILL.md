---
name: local-web-ui
description: "Use when a CLI tool needs a local page or desktop window."
version: 2.0.0
author: coder role of hermes-fleet-apps
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web-ui, cli, http, local-first, no-javascript, csp, verification]
---

# Local Web UI

For the moment a CLI tool has to show the owner something a terminal cannot — an image, a
diff, a grid of things to choose between — and take their answer back. Serve **one page on
127.0.0.1 for the life of one command**. Not a service, not an app, nothing installed,
nothing left listening.

The local-first shape: no account, no CDN, no npm, no build step, and it still works with
the network unplugged. When the page grows into a desktop app, see
`references/desktop-window.md`.

## The shape that works

```
  cli.py ──▶ build the data (read-only)  ──▶ server ──▶ page.py
     │              a fixed list, built             serves    HTML+CSS
     │              BEFORE listening                          as strings
     │                                                 │
     └──▶ writer callable ─────────────────────────────┘
          INJECTED into the server, never imported by it
```

Four pieces, four files. The server is plumbing: it owns routes and nothing else.

## Always on

### CLI first; the page or window is only a mirror

- Every capability ships as a CLI command (with `--json`) and its tests BEFORE any UI
  shows it. The UI calls those same commands and adds UX only: pickers, live progress,
  thumbnails, confirm steps. It never reads the database, walks folders, moves or deletes
  files, or re-implements a decision itself. A second code path silently diverges, and
  agents and the window must see one behaviour.
- **A count with no items behind it is a CLI payload that emits only the NUMBER.** Trace
  the count to the JSON before touching page code. If the CLI drops the items, say so and
  fix it there: emit a named list filled in the same branch that increments the count, and
  test `len(list) == count`. Never rebuild the items in the page from side channels
  (progress lines, set differences): that mislabels every sibling case feeding the same
  counter.
- When the UI needs data the CLI does not emit, extend the CLI's JSON first: add keys,
  never repurpose one, and update any test pinning the exact key set in the same step.
- Make the rule mechanical: a build check that fails if the UI package imports the
  store/engine/file-moving modules, `sqlite3` or `shutil`, deletes or renames a file, or
  reaches the CLI other than through the bridge's one entry point. Before adding UI
  features, audit the existing UI for bypasses as a table (feature | bypass | CLI-first fix).
- **Counts follow the CLI's own lines.** A window word must not merge outcomes the CLI
  keeps apart, and a card's number comes from the same CLI call as the list it links to.
  Need a narrower list? Give the list command a narrowing flag; never recount in the page.
  A count that is WRONG is a counting fix (its own JSON field, its own words), not a
  change to what the tool does. Before proposing to move items between outcomes, grep the
  project log for an owner rule on that outcome: a committed rule wins over a review's
  wording.
- **Parity: the window must eventually do everything the CLI does.** Script/agent-only
  things (`--json`, progress feeds) are n/a with one line why, and the owner confirms
  each. The parity guard reuses the bridge's enforced allow-list plus an n/a dict beside
  it, never a second table. Before coding a new screen, show a static mock in the
  window's real CSS, both themes. Recipe: `references/ui-parity.md`.
- **"For real" runs only the plan the human saw.** Store the preview's args and a change
  counter; refuse `--apply` with no plan, other options, or anything changed since. The
  page greys a stale plan and offers "Preview again".
- **One human action is one journalled, reversible run**, and the page shows the undo
  command.

### Words the window shows

- **No terminal command in any text the window shows; translate at the bridge, once.**
  CLI errors are written for a terminal ("run '<tool> init' first"). Keep the CLI's words;
  give the bridge one `for_window(msg)` table (pattern -> the window's own step) plus a
  fallback that strips any quoted command left over, applied in the single `run()` every
  call goes through. A `--json` refusal that prints `{"error": ...}` on stdout reaches the
  window as "stopped (code 2)" unless `run()` falls back to `data["error"]`.
- **Every reason code the CLI can return needs plain words in the window.** A test parses
  the window's word map and asserts a key for every member of the CLI's status tuple, so a
  new status cannot ship as jargon.
- **A control you must withhold says why it is missing.** An absent button reads as a bug;
  one line of explanation reads as a decision.

### The server

- **Standard library HTTP only.** `ThreadingHTTPServer` on `127.0.0.1`, port `0` for an
  ephemeral port, foreground, dies on Ctrl-C.
- **Zero JavaScript by default, not as dogma.** No-JS makes "works offline" true by
  construction, and a filename cannot become code on a page built out of filenames. It
  costs live updates. When a feature needs real time, name the collision and offer the
  narrowest widening as a question with a recommendation: scripts only from the tool's own
  routes, no remote URLs, no inline handlers, CSP still `'self'`, only on the surface that
  needs it. If the project's instruction file states the rule, the change needs the
  owner's approval.
- **A security header on every response**: `default-src 'self'; form-action 'self';
  base-uri 'none'`, plus `no-store` and `nosniff`. Some directives do not fall back to
  `default-src`: see `references/browser-side-rules.md`.
- **Address items by INDEX into a list the server built itself**, never by a path or name
  the browser sends. An index into a fixed list cannot escape the intended folder by
  construction. Reads and writes alike. A sub-selector (which part of an item) obeys the
  same rule: validate it against the item the server served.
- **Binding to 127.0.0.1 does NOT make the server local.** The bind stops another machine
  reaching the socket and nothing else. Before routing, gate on: loopback client address,
  a `Host:` header naming this machine AND this port, and `Sec-Fetch-Site` not another
  site. See `references/local-server-origin-gate.md`.
- **The write path is injected, never imported.** Hand the server a callable. A server
  built without one serves a read-only page with disabled controls — a real state.
- **The server validates the SHAPE of an answer; the caller owns its MEANING.** Refuse an
  unknown action, a missing field, an out-of-range selector; forward the rest.
- **Validate what the injected callable RETURNS.** The page reads attributes off every
  stored outcome on every render, so one malformed return makes the whole page blank for
  the rest of the session. Refuse it, leave the item waiting. Check by attribute, not
  `isinstance`: importing the result type pulls the writer back into the server's import
  chain.
- **The KIND of action travels in its own hidden field**, matched exactly, never inferred
  from user data. A magic name means a real record with that name can never be chosen.
- **A window that shells a CLI passes every typed name as `--flag=NAME`**, never as two
  argv items: a name like `--apply` would otherwise become a flag. Pin it with a test.
- **The window acts only on items its own last list command returned**, or the native file
  dialog just handed back. Keep a map (key = normalised path) filled only from those, pass
  the STORED path to the CLI, refuse anything else before any command runs. Prove "refused
  before running" with a spy on the run function.
- Escape every interpolated value. The page is built from the user's own filenames and
  the names they typed.

### Data and state

- **The window opens on the CLI's default data folder with no flag.** A required
  `--data-dir` makes a second memory the CLI and the agent never see. Keep the flag as an
  option; Settings shows the folder. From then on, every window test and screenshot must
  point the OS data location at a throwaway folder first.
- **Window preferences that survive a restart live in a small file beside the CLI's data,
  written by a CLI command, never by browser storage.** A page served from a random port
  is a new origin every launch, so `localStorage` forgets. An allow-list of keys and
  values in the config module; a damaged or missing file gives the defaults and never stops
  the app opening; write via temp file + `os.replace`.
- **A tab's redraw puts back every panel the human had open, forms included.** Keep an
  `open` flag in the form's state; reopen from memory, keep what was typed, drop anything
  derived from disk (a plan) because the disk may have changed.

### Controls and layout

- **Check for an open STYLE decision before building any new screen.** Grep the project
  log for the design status. If the look is not final, ask which style the new screen
  wears BEFORE writing its CSS. Keep look and logic in separate files so a restyle
  touches no tests.
- **Porting an approved mockup: the mockup is the LOOK, the brief is the RULES.** List
  every point where they disagree and say which wins (the brief). Map every id the page JS
  reads to KEPT or GONE and grep the tests for each GONE id first; grep scoped selectors
  too.
- **One primary button per screen, decided in one place.** A pure `view(state)` function
  returns labels/hidden/disabled per element and which id is primary; one `paint()`
  applies it, called last in every draw path. Node tests every state without a fake DOM;
  a page test asserts exactly one visible primary.
- **Every prerequisite is a STEP in the strip**, never a header chip plus a footnote. A
  first step parked in a corner reads as optional.
- **The go button of a plan panel stays on screen at any list length.** Put it directly
  under the items it acts on, above secondary lists, in a sticky foot with an opaque
  background. Verify with screenshots at 5+ and ~12 items: a button below the fold reads
  as no button.
- **Show the CLI plan's skips in the list before the click**, not only in the
  after-message, when it is too late to act on.
- **A long job's progress bar is ONE shared component fed by the CLI's own loop.**
  `--progress`: one JSON line per item on STDERR (stdout stays the single `--json`
  document), printed from the loop that builds the result. Count `total` first with a
  cheap walk; count skipped items as done. Work out time left in the host Api (testable
  with a fake clock), label it "about". Emit through a wrapping generator so every
  `continue` still counts as a step. Never add a sleep to product code to make a run long
  enough to screenshot: duplicate the fixture (byte-unique if the tool dedupes by content).
- **A number box with a floor never clamps quietly.** Under the floor: red line, go
  disabled. Warn band: amber line. The Api refuses as the backstop, the CLI refuses the
  flag too. The page's numbers live in one `const` a test compares with the config.
- **While any job runs, ONE page-wide lock makes everything else look and act locked.**
  Hang `lockAll(on)` on the one signal every job reports through: a `locked` class on
  `body` plus `inert` on each zone. `inert` blocks mouse, keys and focus and leaves each
  button's own `disabled` alone, so the end of a job restores exactly what was off before.
  Leave navigation and the theme switch free. Grey it in CSS, including `summary` and
  clickable rows. The running job's own live output stays bright; pin that with a test.
- **Low-value items wait under ONE closed row at the bottom**, never removed. The heading
  still counts the total. Load nothing while the row is closed.

## Procedure

**1. Build the data read-only, first.** A pure function that answers "what is waiting?"
without writing anything. It is also the `--json` contract for scripts and agents.

**2. Serve it.** Routes only: `/`, `/style.css`, `/item/<n>`. Take a private copy of the
list so it cannot mutate under a running server. Generate derived media in memory and never
write a derived file into the user's folders.

**3. The page as strings.** CSS is its own route, not an inline `<style>` block — a strict
CSP blocks inline styles, and widening it weakens the header that makes an injected script
inert.

**4. The write path, injected.** Build it standalone and prove it at the function level
before any HTTP exists: one answer in, one journalled change out, refusals returned as
messages. Wire it into the server last.

- An answer is a plain `<form method="post">` answered with a **303 redirect**, one form
  per button with the button's own `value` carrying the answer. A refresh cannot re-submit.
- Never mutate the list to mark something done — record outcomes in a map beside it, so
  index 3 means the same item for the life of the server.
- **Only a SUCCESSFUL action is final.** Recording a failed one as answered retires the
  item. Keep every control on a failed item, show the error on the live card. Guard the
  double-click by checking the recorded outcome succeeded, not merely that one exists.
- **A decision card asks ONE question in words, and the answer comes first.**
  ```
  [preview]
  Is this X?                                    <- largest text on the card
  [Yes, X] [Y] [None of these]          Skip    <- answers right under it
  > More options (optional)                     <- <details>, closed
  item-0412.ext · close match                   <- filename small, last
  ```
  Scores go in a `title=` hover, not in button text. Offer an explicit Skip to the next
  waiting card. Fold optional actions into a closed `<details>`. Plain words, no engine
  jargon. Keep the POSTed fields unchanged so a re-layout touches render tests only.
  Motion is CSS only, off under `prefers-reduced-motion`.

**Redesigning a page the owner already uses: mark up the current one first.** Screenshot
it with fixture data, draw lettered boxes with a one-line legend per flaw, and let them
confirm or correct before touching the layout. A text critique of a page lands worse than
a marked-up picture.

**5. Verify by looking.** A green unit suite proves the functions you thought of; the bugs
live in the wiring and in what the page actually looks like. First the cheap gate check
against the RUNNING server:

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:$PORT/                      # 200
curl -s -o /dev/null -w "%{http_code}\n" -H "Host: evil.example" http://127.0.0.1:$PORT/   # 403
curl -s -o /dev/null -w "%{http_code}\n" -H "Sec-Fetch-Site: cross-site" \
     -X POST http://127.0.0.1:$PORT/resolve                                            # 403
curl -s -o /dev/null -w "%{content_type} %{size_download}\n" http://127.0.0.1:$PORT/item/0
curl -s http://127.0.0.1:$PORT/ | grep -c '<script\|https://\| on[a-z]*='              # 0
```

Grep the RENDERED output for scripts and remote URLs, never the source: the modules that
implement the no-JS rule contain the words it forbids. A missing `Sec-Fetch-Site` must stay
allowed (curl, tests, agents), so the cross-site check SETS the header.

```bash
chrome --headless=new --disable-gpu --hide-scrollbars \
  --user-data-dir=<empty scratch dir> --incognito \
  --disable-application-cache --disk-cache-size=1 \
  --host-resolver-rules="MAP * ~NOTFOUND, EXCLUDE 127.0.0.1" \
  --window-size=1280,1600 --screenshot=<out.png> http://127.0.0.1:<port>/
```

The empty profile and blocked resolver prove the offline claim. Then **look at the
screenshot**. Drive the real interaction too, and exercise every refusal over real HTTP:
empty field, non-numeric index, out-of-range index, traversal string, oversized body, POST
to another route — asserting the status code AND that nothing on disk moved.

## Pitfalls

**Server output.** Run it unfiltered (`python -u`, no pipe) when you need the port line: a
`grep` pipe buffers it until the process dies.

**Ids.** A per-second timestamp is not unique once one action is one run: two clicks in one
second share a journal path and the first becomes impossible to undo. Make ids
collision-proof against the filesystem.

**Sockets.** A refused POST must drain the body before closing, or the leftover bytes parse
as the next request. A client that vanishes mid-response is not an error: swallow
connection resets. A test past the drain limit must guard the whole socket conversation and
assert only what is promised.

**Demo stubs.** A stub write path must return the real result type. Returning `None` kills
the page on the first click. Return a real failure outcome carrying the reason, and say
which controls are live and what ONE click does before handing over a demo URL.

**Headless `--screenshot` cannot verify a `#fragment` URL** (blank frame). Drive Chrome over
`--remote-debugging-port` instead: navigate, `Runtime.evaluate` for positions, then
`Page.captureScreenshot`. Use `scripts/cdp_shot.py`.

**Timing.** Time a list's first draw on a FIRST visit only; a revisit still holds the old
rows. Measure inside one `Runtime.evaluate` so CDP round-trips stay out of the number.

**Animations.** Freeze a frame in the same JS turn that starts the move
(`getAnimations().forEach(a => {a.pause(); a.currentTime = <ms>})`), read state back via
`location.hash`. Screenshot only after entrance animations finish
(`Promise.all(getAnimations().map(a => a.finished))`). Show the owner motion as a working
page with a slow-down toggle, not as frames.

**Shots per theme.** Live state (a progress bar mid-run) is shot from its own real run in
EACH theme, on a fresh throwaway data folder; replaying a recorded state shows a screen real
code never drew. A style fix after a shot invalidates that shot in every theme.

**Suspect the measuring apparatus before the code.** A screenshot forces a full paint, so
every lazy image looks loaded. Re-measure with the instrument removed. See
`references/browser-side-rules.md`.

**Check the whole import CHAIN.** A test that parses runtime imports of the server only
leaves the hole one level down (the page module). Parse every module on the path. Shared
constants go in an inert config module.

**SQLite and threads.** Open a connection per request: a threaded server hands each request
to another thread, and the command's handle raises on the first real click, not in tests.

**Recoverable order.** Record first, then move the file: a failed move leaves a harmless
extra record; the other order files something under a record that was never created.

**A new request-level gate silently retires tests that used placeholder headers.** They
keep passing while no longer testing their subject. Re-read them and give each an input
valid in every respect but the one it tests.

**A spec line can be impossible rather than unimplemented.** "Refused from another host on
the LAN" cannot happen against a loopback bind. Say so, implement the threat it was
reaching for, and bind wider in the test only if a demonstration needs it.

**Shared stylesheets beat `hidden`.** A design-system `display:` rule overrides `[hidden]`.
Add `[hidden]{display:none!important}`, test that window class names never collide with the
house sheet, and name body state classes after the state (`locked`), never after a
component.

**One field, one shape, across every command the window reads.** One command emitting a box
as text where others emit a list leaves every picture after that step empty, while
hand-built fixtures stay green. A CLI test compares the field across commands; the Api
refuses any other shape.

**Overlays sit on the picture's OWN size**, returned with the picture, not on a stored size
that can be stale. Keep the maths in a pure function; prove it by writing a wrong size into
a scratch database and comparing rects over CDP.

**Check "nothing clipped" by script before every shot, then by eye.** One JS check lists any
visible text element whose scroll size exceeds its client size, and any rect past
`innerWidth`. When shots hold the owner's real data they must never go to a vision model:
then this check is the only machine check, so extend it (no sideways scroll, primary button
inside the viewport) and say you did not look at the PNGs.

**Run the WHOLE suite after a page edit.** Page-wide guards (banned words, typed-in limits,
undefined CSS custom properties) live in other files. Rewrite the copy; never loosen the
guard.

**Write sabotage cases from the live file**, asserting each anchor occurs exactly once
before adding it to the harness.

**Minimum window size:** `Emulation.setDeviceMetricsOverride` over CDP, then clear it. It
sets the viewport, slightly smaller than a real window: say so.

**Labels beat hints.** In a narrow row the hint truncates, never the label. Check every
visible label's `scrollWidth <= clientWidth` at the minimum size.

**A skipped test module is a missing gate, not a pass.** `importorskip` hides every test in
the file. After a merge, diff collected test ids, not totals.

**Fixtures for a visual check are public or synthetic, never the user's files.** Anything
rendered and looked at leaves the machine. Libraries often ship sample media; duplicate it
for volume.

## References

- `references/desktop-window.md` — when the page becomes a desktop app: why pywebview, the
  package shape, the CLI bridge and its allow-list, the mirror check, the queue
  and naming screens, the full plan view, styling as its own phase,
  data safety in a spike, driving the window over CDP to verify it without touching
  the owner's real data.
- `references/ui-parity.md` — "everything the CLI does, the window does too": the
  capability audit, the parity guard test, the shape-first static mock, shaping a
  silent first-run trap, build and close order of an item.
- `references/readme-for-window.md` — once the window exists: README rebuilt around the
  window for non-terminal readers, CLI reference moved to its own doc.
- `references/stdlib-http-server.md` — handler skeleton, header helper, refusal and drain
  logic, the injected-resolver pattern, and the import-guard test.
- `references/browser-side-rules.md` — CSP directives that do not fall back, no-JS form
  patterns, the lazy-load measurement recipe, CSS traps that move controls off-screen.
- `references/local-server-origin-gate.md` — why a 127.0.0.1 bind is not enough, the
  three-check gate, why `Origin` is the wrong header for a form page, a real DNS-rebinding
  test.
- `scripts/cdp_shot.py` — headless Chrome over CDP, stdlib only: navigate, optional
  click/eval, print `scrollY` and hash, save a PNG. `CDP_WAIT` / `CDP_SIZE` / `CDP_FLAGS`
  env vars; never copy and edit the script per use.
