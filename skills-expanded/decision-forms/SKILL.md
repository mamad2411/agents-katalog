---
name: decision-forms
description: "Use when the owner answers design questions or prototypes a UI visually: local HTML forms and mockups served by Lavish."
version: 1.1.0
author: coder role of hermes-fleet-apps
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [decisions, questions, visual, html, lavish, planning]
    related_skills: [build-method, plain-words, local-web-ui]
---

# Decision forms

Some owners decide faster by looking than by reading. When a round of design
questions (a proposed shape plus 2-5 choices) would be a wall of terminal text, or
the owner asks to answer "visually", build the round as a local HTML form and collect
the answers from it. The tool is Lavish (`lavish-axi`, MIT, npm, Node >= 22, a
third-party skill listed in docs/third-party-skills.md): it serves a local HTML file and
returns what the owner queues to the agent. It is an aid for deciding, never a
project dependency.

## Procedure

1. **Vet once, state the one risk.** It listens on 127.0.0.1:4387 (check which other
   addresses it binds on your machine, e.g. a VPN interface). Its `share` / Publish
   uploads the page to a PUBLIC third-party host: never run it, and tell the owner
   not to press it.
2. **Pin and run through npx**, nothing installed globally:
   `npx -y lavish-axi@<ver> --help`, then `npx -y lavish-axi@<ver> playbook input`
   before writing any form.
3. **Keep it out of commits.** Put the HTML in the project's private, gitignored tree
   (e.g. `_private/lavish/<topic>.html`); prove it with `git check-ignore -v` and a
   clean `git status`.
4. **Design source: the project's own palette** (its CSS variables), inline CSS and an
   inline SVG diagram, no CDN, so it renders offline.
5. **Layout:** one card for the approved shape (diagram + priority order), then one card
   per question. Each question is a native `<form data-lavish-question="qN">` with
   radios or selects, the recommended option FIRST and labelled, and ONE submit that
   calls `window.lavish.queuePrompt(...)` once with `data: {question, answer}` and adds
   a visible "queued" mark. Free-text boxes ask for the SHAPE with made-up names, never
   real ones. End with "press Send to Agent".
6. **Open and listen:** `npx -y lavish-axi@<ver> <abs-path.html>`, confirm the URL with
   curl (200), then run `npx -y lavish-axi@<ver> poll <file>` as a tracked background
   process with notify on exit. Give the owner the URL and one tip: keep the tab open
   until Send to Agent is pressed. If starting the background poll hangs or times out
   (an unanswered approval prompt), stop and say so, but still hand over the URL:
   queued answers wait on the server until a poll collects them, so the owner can pick
   now and a foreground `poll <file>` run after they say "sent" returns them at once.
7. **Read the answers from the process LOG** (`process_manage log`), not from the exit
   notification: the notification carries only the output tail, which is the DOM
   snapshot, and the prompts sit above it.
8. **Close the loop:** reply once with `poll <file> --agent-reply "got it, continuing
   in the chat"` (background again), then continue in the terminal. Write the decisions
   where the plan lives (the roadmap), not only in chat. Anything the pick carried
   along that the owner did NOT choose (a paired mono font, a warning colour, a
   dropped accent) is written as "default, not picked, revisable" and named to them,
   so a later stage can change it without "reopening" their pick.
9. **Stop the listener before the session ends.** The "got it" reply poll keeps
   running until feedback or disconnect; kill it (or have the owner close the tab)
   before a handoff, and tell the next session no poll is live. Once the pick is
   recorded: `lavish-axi end <file>`, then `lavish-axi stop` (shuts the server on
   4387); confirm with curl returning 000.

## Prototyping a UI

A tool's screens can be prototyped in Lavish before any restyle of the real app.
Same tool, same safety rules as the forms above; the artifact differs:

- **One screen per round.** First a map of the whole flow (every screen as a box, the
  order the owner works in) if the order is undecided; otherwise start at the core loop.
- **2-3 visual directions side by side** for the same screen, each clickable with plain
  inline JS, fed with made-up names and public sample images, never the owner's
  real files.
- **Anchor on what the owner APPROVED, not on what the design doc claims.** Ask which
  artefacts are fixed (an image, a banner) and which axes are open (fonts, layout,
  motion, UI style); write both into the roadmap step. Every direction is a
  variation AROUND the fixed art, never a replacement for it. Then start from the
  project's own design system (its tokens / DESIGN.md) and let the owner depart from
  it; Lavish's CDN fallback is only for projects with none, and breaks the offline rule.
- **Read the render script of every approved image before naming its fonts.**
  An approved image may be drawn with system fonts while the design doc lists
  others; the lettering that was approved is the script's,
  and system fonts cannot ship inside an app. The first direction round then compares
  freely licensed (OFL) look-alikes, licence checked at the source.
- **Fonts are picked FIRST, once, for the art AND the app together** (a step 0
  before directions). If the art is redrawn before the pick, it is redrawn twice.
  Order: font sheet -> owner picks -> a pasteable font list for the art session ->
  art regenerates -> UI directions. The sheet shows each candidate set three ways:
  the banner title, the image's own texture, and one real app card in light AND dark.
  Sourcing and licence recipe: `references/font-sourcing.md`.
- **The app font and the images' title font are two picks, not one "set".** An app
  font is usually a plain, current sans with its own mono for numbers; an image title
  font may be expressive (italic or script). The art's small text (taglines) uses the
  app font so both stay one family.
- **Record the owner's taste as it is learned** (in DESIGN.md or the product notes,
  with the pick it came from), and lead the next round with the class they picked;
  the other directions become the contrast.
- **Alternatives on a sheet must differ at a glance.** No font shared between
  sets and no near-twins (three classical serifs read as "all the same"); 5-6
  options spanning clearly different styles. An ambiguous word from the owner
  ("cursive" = italic OR joined script) is shown as BOTH, labelled, not guessed.
  Say where each option breaks (scripts are unreadable at icon size).
- **Each new round overwrites the page Lavish serves, so copy the old one first**
  (`fonts.html` -> `fonts-roundN.html`) and keep the same session URL; reply with
  `poll --agent-reply "Round N is up: reload"`.
- **Take the UI accent from the approved art by sampling its pixels**, not a
  stock colour (bucket the image's dominant hues, take the most common).
- **Crop reused images to the art only.** A banner PNG already carries its old
  title; laid beside a new title it shows both.
- **Pin the page to light rendering** (`<meta name="color-scheme" content="light">`,
  `color-scheme: light` on `:root`) and, if the owner's screenshot shows a light card
  rendered dark, say the browser forces dark mode (Chrome auto-dark or an
  extension): it falsifies every light-vs-dark comparison.
- **A whole-app redesign is a staged phase, one pick per stage, no stage reopens
  an earlier one:** directions (3-4 styles on the same 2 screens) -> flow map (all
  screens as grey wireframes: content, tab order, moves) -> full mockup (chosen
  style on every screen) -> motion (a few small moves only) -> lock (DESIGN.md v2 +
  CSS become the house style). Bound it up front: the look, layout and flow can
  reset; what each control DOES cannot, if the project's rule is "the UI mirrors
  the CLI". Fonts and animation ship with the app, no web fonts or CDN libraries.
- **Other workers consuming the style get told before they spend more on it.**
  If another agent or worktree is producing assets in the style under review, write
  the owner a pasteable note for that session (what is fixed, what is open, what to
  stop, which later step realigns it), since agents cannot message each other.
- Files in `_private/lavish/ui/<screen>.html`, assets copied beside them with relative
  paths (root paths `/x` do not resolve under Lavish's server).
- **Embed fonts as base64 `data:` URLs in `@font-face`; never link them as files.**
  Lavish serves the artifact in a sandboxed iframe (CSP `sandbox` without
  `allow-same-origin`), so the page's origin is `null` and every font fetch is a
  cross-origin request its server answers with no `Access-Control-Allow-Origin`: the
  browser drops every font silently and all "different" fonts render as one fallback
  serif. Images still load, which hides it. Check: `curl -D - -H "Origin: null"
  http://127.0.0.1:4387/artifact/<id>/fonts/X.ttf` shows no ACAO header.
  Embedding recipe: `references/font-sourcing.md`.
- **Verify THROUGH Lavish before handing over the URL, never via the file.** A
  `file://` screenshot loads the fonts and proves nothing. Screenshot the session URL
  with local-web-ui's `scripts/cdp_shot.py` (`CDP_WAIT=30 CDP_SIZE=1400,<page height>`):
  Lavish holds the page behind "Checking layout" while fonts load, and one-shot
  `--screenshot` captures only that overlay. The hold grows with the page: a light
  page may need about 12 s, one with embedded fonts and images about 30 s.
  If the shot shows the overlay, re-run with a longer wait;
  never hand over a URL whose render you have not seen. Then zoom (vision `region`) on each
  option and confirm they differ and nothing clips (tall script capitals do).
- **CDP from the top page cannot reach into Lavish's sandboxed iframe.** Take the
  full-page check through the session URL. For scripted interaction frames (clicks,
  mid-animation shots), drive the `file://` build instead. That is valid ONLY
  because the fonts are embedded as base64, and only after the session-URL shot
  has been seen.
- **Directions round** (step 1), **flow-map round** (step 2), **full-mockup
  round** (step 3) and **motion round** (step 4: a working demo with feel presets,
  Slow ×5 and Replay pairs for today's moves): a worked set of 4 contrasting styles,
  the Python build recipe (one build script per round, with a `--dark` flag for the
  dark screenshot), sample-content rules, how to verify dark mode and catch clipped
  side columns behind Lavish's sandbox, grey wireframes whose every control
  names its CLI command, and what the full mockup adds (state tokens, hidden
  command tags, one pick per carried-along default, and a round-2 form when the
  owner's note opens new scope such as Settings):
  `references/ui-directions.md`. The **lock step** (step 5: merge main into the UI
  tree, inventory the old style's consumers, measure contrast, then ONE
  `tokens.json` that generates the CSS block and DESIGN.md's front matter,
  guarded by a drift test, and a style sheet screenshotted from the real CSS)
  is in the same file.
- **A motion round must override "reduce motion" on the owner's machine, from the
  first build.** When the OS has animation effects turned off, the browser reports
  `prefers-reduced-motion: reduce` and a correctly written kill-switch flattens every
  move to 1 ms: the owner sees nothing and asks where the animations are. Scope the
  kill-switch as `body:not(.force) *`, add `.force` from JS when the query matches,
  and show an amber banner naming the OS setting plus an "Obey it instead" toggle, so
  the owner can also judge what such users get. The real app still obeys the query.
  Verify under that condition: `CDP_FLAGS=--force-prefers-reduced-motion` on
  cdp_shot.py, reading `document.getAnimations()` durations back through
  `location.hash` (forced = real durations, obeyed = 1 ms). Frame-freezing recipe:
  local-web-ui pitfall "Verify an animation with a frame frozen...".
- **Build a later round's page by importing the earlier round's builder.** Put
  the step-3 build script's write under `if __name__ == "__main__":` and import
  its header, fonts and CSS into the new round's builder (e.g. build_motion.py
  + motion.css loaded after mockup.css). Rebuild the old page and compare md5
  to prove the guard changed nothing.
- The owner marks up elements and queues prompts; the chosen prototype becomes the
  spec the real UI is ported from (look only: markup and CSS, never the logic or tests).
- Poll: Lavish asks for a foreground poll or a harness-tracked background job that
  notifies on exit; never `&`/nohup. Checked working: `lavish-axi@0.1.79` on Node 26.
- **If the background poll's start times out (approval prompt), do not retry
  it blind — and do not assume it never started.** Check `process_manage list`: a
  timed-out start can still be live, and it will consume the NEXT message the owner
  sends (a chat question, not a form answer) that a later foreground poll never sees.
  Read that process's log before closing the step. Hand over the URL, let the owner
  queue and press Send, then run ONE foreground `poll <file> 2>&1 | head -60`
  (timeout ~120): queued answers are kept and it returns at once. The answer lines
  sit above the DOM snapshot. After recording the pick, `lavish-axi end <file>` so no
  listener or session is left live.
- **A poll that returns only its "Long-polling..." banner means NOTHING was sent**
  (it hit the `timeout` wrapper). Lavish's chat then shows "Your agent is not
  listening". Do not ask for Send again blind: ask the same question once in the
  terminal (clarify tool, recommended option first). A one-pick follow-up round
  rarely needs Lavish at all; the page stays up to look at while the owner answers
  in the terminal.

## Session states

- `browser_disconnected` before any feedback: the tab closed or idled too long. The
  session is resumable and queued answers are kept. Ask "reopen or end?" and do
  neither uninvited. Reopen with `<file> --reopen`, then start a fresh background poll.
- `browser_disconnected` AFTER the answers arrived: the owner closed the tab as told.
  Say so in one line, offer "end", and go back to the open question in the chat.
