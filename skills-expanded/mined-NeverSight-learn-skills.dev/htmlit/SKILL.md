---
name: htmlit
description: >
  Turn an HTML artifact into a fast, self-reloading collaborative review
  surface - minimal and fully self-contained. Pure-Python
  daemon (no node, no deps), single-document injection with a shadow-DOM toolbar,
  and live DOM morphing so edits patch the page in place with no full reload.
  Includes Google-Docs-style annotation - select text to leave a persistent
  highlight note (saved with the file, shown in exports) or a comment that reaches
  the agent - a chat/feedback queue, agent replies, a light/dark theme toggle, and
  locally vendored Mermaid + highlight.js (no CDN
  latency). Use whenever you are about to hand the user a rich/visual/interactive
  response - a plan, comparison, report, diagram, table, code or diff review,
  prototype, or any browser-based feedback loop - and whenever the user says
  "htmlit", "/htmlit", "review this html", "open this artifact", "make me a
  review surface", or asks to "resume"/"continue" a kept review (run
  `htmlit resume`).
user-invocable: true
metadata:
  author: auspham
  version: "1.0.0"
  license: MIT
  homepage: https://github.com/auspham/htmlit
  argument-hint: "[what to visualize or review]"
---

# htmlit

A tiny, isolated review surface for HTML artifacts. You write an `.html` file;
`htmlit` serves it with an injected toolbar, streams changes back into the live
page via DOM morphing (no full reload), and hands you the user's annotations and
messages over a long-poll.

It is intentionally minimal and self-contained:

- **Pure Python stdlib daemon** - no Node, no pip installs. Spawned on demand.
- **Self-reload via morphing** - edit the file and save; the page patches in
  place (scroll, form state, rendered diagrams and the toolbar all survive). No
  iframe, no flash, no full reload.
- **Shadow-DOM toolbar** - the chrome lives in a shadow root, so the artifact's
  CSS can never touch it and its CSS never leaks into the artifact.
- **Vendored assets** - on first use the daemon caches Mermaid, highlight.js, and
  Idiomorph locally in the background (from the CDN), so later loads render with no
  CDN round-trip. Set `HTMLIT_AUTO_VENDOR=0` to stay on the CDN.
- **Degrades gracefully** - a zero-specificity base stylesheet gives an unstyled
  artifact readable typography (your own CSS always wins over it), and an invalid
  Mermaid diagram falls back to its source instead of an error graphic. Still ship
  your own CSS and valid Mermaid; these are safety nets, not a substitute.

## Request

$ARGUMENTS

If the request above is non-empty, the user invoked `/htmlit` explicitly - build
an HTML artifact for that request now and run the workflow below. If it is empty,
infer what to visualize from the conversation.

## The `htmlit` command

`htmlit` is on PATH (a pure-Python CLI; no node version juggling).

- `htmlit <file.html>` - open/resume a review session and launch the browser.
  Prints the URL, the session key, and the poll command. On a persisted artifact
  it also prints a **RESUMING** banner (handoff note + conversation).
- `htmlit resume` - **list resumable reviews** (kept artifacts under `./.htmlit`
  and any persisted live sessions), each with its `htmlit resume <file>` command.
  `htmlit resume <file>` reopens that review (same as `htmlit <file>`). This is
  how the user tells a fresh agent to pick a kept review back up.
- `htmlit poll <file.html>` - long-poll for feedback. Stays silent until the
  user annotates, sends a message, ends the session, or the browser reports
  layout warnings. Re-run it to keep listening; queued feedback is never lost.
- `htmlit poll <file> --agent-reply "msg"` - post `msg` into the chat, then poll.
- `htmlit reply <file> "msg"` - just post an agent message (no poll).
- `htmlit context <file> "note"` - save a **handoff note** (workflow state) for a
  future agent that resumes this review. Persists the session (implies Keep) and
  writes the note into the sidecar; it is surfaced when the review is reopened.
- `htmlit end <file>` - end the session. By default this **deletes the
  generated artifact** (any file under a `.htmlit/` directory); pass `--keep` to
  end without deleting.
- `htmlit stop` - shut the daemon down (also idle-safe to leave running).
- `htmlit vendor [--force]` - fetch the local Mermaid/highlight.js/Idiomorph
  assets up front (the daemon also does this in the background on first use).
  `--force` refreshes them.

## Workflow

You are the agent that **serves** the review: the same agent that opens the
artifact must keep polling until the user ends it. While you are not polling, the
panel shows **"no agent connected"** and the user's annotations just queue.

1. **Write the artifact.** Default location `~/.htmlit/<name>.html` - i.e. under
   `$HTMLIT_HOME` (which defaults to `~/.htmlit`, the same dir as `server.json`).
   Write it **there, not inside the current repo/worktree**, so a generated review
   never pollutes a project's `git status`. It is a normal standalone HTML file -
   it opens fine on its own; `htmlit` only adds the review toolbar when served.
2. **Open it:** `htmlit <file.html>`.
3. **Serve it - keep polling.** Run `htmlit poll <file.html>`. It blocks (long-
   polls) until the user annotates or messages, then prints the feedback as JSON.
   **Treat this as a loop you stay in: poll -> apply -> reply -> poll again -**
   do not end your turn while the review is open, or the user is left talking to
   nobody (the panel will say "no agent connected"). If your harness caps command
   runtime, run the poll as a background task and re-run it on timeout; queued
   feedback is never lost.
4. **Fix layout first.** If the poll returns `layout_warnings`, fix the overflow
   or clipped/overlapping content and save (the page morphs live), then poll
   again before involving the user further.
5. **Apply feedback by editing the file and saving** - changes morph into the
   live page instantly. Then reply and keep the loop going:
   `htmlit poll <file> --agent-reply "Done - enlarged the title and fixed the diagram."`
   Replying re-enables the user's Send button (while you are "working" it is
   disabled) and keeps presence showing "agent connected", so always reply and
   immediately poll again to keep serving. When you answer a **follow-up
   question** by adding content, wrap it in a follow-up block (see
   `data-htmlit-answer` below) so the page shows *"&#8627; You asked: ..."* above
   your answer, and place that block **right next to the element the user
   annotated** (the prompt's `selector`) so the reply is in context rather than a
   separate section; any content a morph adds is briefly flashed and scrolled in.
6. **End** when the review is finished: `htmlit end <file>`. The generated
   artifact (under `.htmlit/`) is **auto-deleted** on end, so nothing is left
   behind - use `htmlit end <file> --keep` if you want to preserve it. The user
   can also flip the panel's **Keep** toggle to persist the artifact themselves:
   when Keep is on, `end` never deletes it, the file stays in `.htmlit/`, and the
   panel shows the exact command to resume the review later.
7. **If the review is kept, leave a handoff.** When Keep is on (or the user asks
   to resume later), before you stop, record your workflow state with
   `htmlit context <file> "what's done, key decisions, next steps, files touched"`.
   This is stored beside the artifact so the **next agent can continue** - htmlit
   restores the artifact and conversation, but not your internal memory, so this
   note is how the workflow carries over.

**Resuming a kept review:** when the user asks to **resume** (e.g. "resume the
htmlit review", "continue that review", "pick the review back up") in a fresh
session, run `htmlit resume` to list the kept reviews, then `htmlit resume <file>`
(or `htmlit <file>`) on the one they mean. That prints a **RESUMING** banner with
the previous agent's handoff note and the full conversation - read the note + the
current artifact, then continue serving (`htmlit poll <file>`) from where it left
off. Do not start over.

## How feedback comes back

`htmlit poll` prints JSON:

```json
{
  "type": "feedback",
  "prompts": [
    { "selector": "#intro > p:nth-of-type(2)", "tag": "text", "text": "the selected words", "prompt": "reword this", "range": { "container": "#intro > p:nth-of-type(2)", "start": 40, "end": 62, "text": "the selected words" }, "commentId": "cmh2k7f3q" },
    { "selector": "#mermaid-17..-flowchart-B-1", "tag": "g", "text": "Anchor", "prompt": "why does this start here?", "range": null, "commentId": "cmr47gg7h1" },
    { "selector": "", "tag": "message", "text": "Freeform message", "prompt": "make the intro punchier", "range": null, "commentId": "" }
  ],
  "layout_warnings": [ { "severity": "error", "kind": "horizontal-overflow", "offenders": [ ... ] } ],
  "domSnapshot": "<!doctype html> ... (artifact DOM at submit time, chrome stripped) ...",
  "chat": [ { "role": "user", "text": "..." }, { "role": "agent", "text": "..." } ]
}
```

Annotation is **Google-Docs-style and always on** (no mode to toggle): the user
just *selects text* anywhere on the artifact and a small floating menu offers two
actions. **Highlight** is a *local note* - it stays as a yellow mark on the page,
is saved with the review, appears in exports, and is **never sent to you**.
**Ask agent** is what reaches you: it targets the exact span and is delivered on
the next poll, and it leaves a persistent "you asked here" **comment anchor** on
that span. A plain click that selects nothing dismisses the menu; clicking an
existing highlight offers Ask agent or Remove. The page stays fully interactive.

Comments live in a **card rail** down the right margin (Google-Docs style), each
card aligned to the span/element it annotates. Annotating **queues** rather than
sends: **Ask agent** drops a draft card plus a **numbered pill** in the composer
(the number matches the pin on the page - click the pill to jump to that spot), and
the panel's **Send** delivers every queued comment/message at once. On a card the
user can **Queue** a follow-up or **edit** an earlier comment (both queue and go out
on the next Send), so one anchor can carry a **thread** - you may therefore see
several `prompts` sharing a single `commentId` in one poll batch; treat them as one
thread and answer the latest (your `data-htmlit-answer-for="<commentId>"` block
links the whole thread).

**Only comments and freeform messages arrive in `prompts` - highlights do not.**

- `prompts[].prompt` is what the user typed.
- `prompts[].tag` is `"text"` (a commented text selection), an element tag like
  `"h1"`/`"img"`/`"g"` (a non-text target such as an image or a Mermaid node,
  where text can't be selected), or `"message"` (freeform chat).
- `prompts[].range` (when present) pins the exact commented span: `container` is
  a CSS selector and `start`/`end` are character offsets into that element's text,
  with the commented `text`. It is `null` for element/diagram targets and freeform
  messages, where `selector` (if any) locates the target.
- `prompts[].commentId` (non-empty for a text-span comment **or a diagram
  node/edge comment**) is the id of the "you asked here" anchor left on that
  target - a purple underline on text, or a purple outline box on the diagram
  element. **When you answer such a comment, set
  `data-htmlit-answer-for="<commentId>"` on your `data-htmlit-answer` block**
  (see below) - the anchor then links to your answer, and clicking it in the page
  scrolls to and flashes that answer. (For a freeform `message` it is empty; just
  answer normally.)
- `prompts[].selector` is a CSS selector for the target (the range's container
  for text, or the element itself). `type` is `feedback`, `ended`, or (with
  `--once`) `timeout`.
- Use `selector`/`range` + `domSnapshot` to locate exactly what the user marked.
  (Note highlights are stripped from `domSnapshot`, so they never leak to you.)
- **When a prompt targets a specific span/element, answer it *in place* in the
  document - never only in the chat.** Every comment carries a `commentId`, and its
  answer belongs in the **document**, not the chat panel: insert a `data-htmlit-answer`
  block tagged `data-htmlit-answer-for="<commentId>"` (see below) right next to the
  annotated element. The client then renders that answer **inline in the comment's
  rail card** (a Google-Docs-style reply thread) *and* lets the user click the anchor
  to jump to it - so the answer is always visible from the document. A chat
  `--agent-reply` is only a short status/notification ("done - see the new section");
  it is **not** a substitute for the in-document answer and does not attach to the
  comment. So: for any prompt with a `commentId`, write the `data-htmlit-answer` block
  (even for action requests - e.g. put the result/outcome there). Only fall back to a
  standalone section, or a chat-only reply, for a freeform `message` with no
  `commentId`.

The panel header shows an honest **presence** that reflects whether an agent is
actually polling: **"agent connected"** (green) while you long-poll, **"working"**
(amber) while you hold feedback to act on, and **"no agent"** (with a banner
"run `htmlit poll`") whenever no agent has polled for ~35s. So if the user ever
sees "no agent connected", it means you stopped serving - resume `htmlit poll`.
The same state also drives a **live favicon** so the browser tab shows it at a
glance: a **yellow spinner** while the agent is connected and waiting for the
user's input (their turn to act), a **green spinner** while the agent is working,
a **grey ring** when no agent is connected, and a **green tick** once the review
is closed. The user can **always type and send** (their composer is only locked
after the session ends); a message sent while you are working simply queues for
your next poll. Replying (`--agent-reply`) returns presence to "agent connected",
so it never sticks on "working".

## Authoring the artifact

**Ship a complete, self-styled page.** htmlit styles only its own toolbar, never
your document, so two things are on you - aim to get them right at the source, not
to lean on the safety nets:

1. **Always include your own CSS.** Put a `<style>` in the artifact that sets
   typography, colour, spacing, and code/diagram framing, and theme **both** light
   and dark (`html.dark ...`). A page with no CSS falls back to plain base
   typography and looks unstyled. Start from `examples/demo.html`, not an empty page.
2. **Always write valid Mermaid.** Quote any node or edge label that contains a
   space, parenthesis, or punctuation, or the diagram fails to parse:
   `A["Big-bang cutover"]`, `B{"Dual-write sessions?"}`, `X -->|"yes (safe)"| Y`.

htmlit does degrade gracefully if you slip (base typography for an unstyled page,
and an invalid diagram shows its source instead of an error graphic), and `htmlit
poll` reports a `no-artifact-css` or `mermaid-syntax` warning when it happens - fix
the source when you see one rather than shipping the fallback.

Prefer **interactive** artifacts so the user can discover content - selectable
option cards that expand a section, a dropdown that switches views, `<details>`
accordions, tabs. Keep interactions **morph-safe** so they survive the live
self-reload:

- **CSS-only state** is best: hidden `<input type="radio">`/`checkbox` + `:checked`
  sibling rules to expand panels, and native `<details>`/`<summary>`. No JS, and
  it always works after a morph. See `examples/demo.html` (the flavour cards).
- **For JS interactivity, use event delegation on `document`** (not per-element
  listeners) and guard init with a flag so it is bound once:

  ```html
  <script>
  if (!window.__wired) { window.__wired = true;
    document.addEventListener("change", function (e) {
      if (e.target.id === "view")
        document.querySelectorAll(".pane").forEach(function (p) { p.hidden = p.dataset.pane !== e.target.value; });
    });
  }
  </script>
  ```

  The listener lives on `document` (never replaced by a morph), so it keeps
  working even when the morphed-in nodes are brand new. htmlit also re-executes
  any `<script>` it adds during a morph, so the guard prevents double-binding.

The injected client auto-renders, on first load and after every morph:

- **Mermaid diagrams** - a fenced/`<pre><code class="language-mermaid">` block,
  e.g.

  ```html
  <pre><code class="language-mermaid">flowchart LR
    A --> B</code></pre>
  ```

  Prefer Mermaid for flows, architecture, state, and sequence diagrams instead
  of hand-built boxes-and-arrows. Each diagram renders inside a **framed canvas**
  (full container width, fixed clamped height, bordered, with a square graph-paper
  grid) so a big diagram never blows out the page - it lives in a pannable
  viewport. The grid behaves like an **infinite map grid**: zoomed out you see big
  squares (each divided into 5); zoom in and finer squares smoothly open up (fade
  in), zoom out and the finest lines fade away, so it never turns to clutter.
  Every diagram is **rearrangeable** so the user can untangle Mermaid's
  auto-layout when boxes or lines overlap: scroll (or the **- / +** buttons) to
  zoom over the grid and drag the background to pan; drag a node and its connected
  edges (and their labels) follow; drag an edge (or its label) to bow it aside.
  Edge labels are not independently draggable - they always ride on their line -
  and dragging never selects the diagram's text. Any htmlit annotation pin on a
  diagram element tracks it as it moves. A minimal zoom control sits at the
  bottom-left showing the current **zoom %** (relative to the fitted view); click
  the percentage to reset to fit. A **Code** button at the top-right toggles the
  diagram for its Mermaid source (read or copy the syntax in place). A diagram
  inside a hidden tab or a closed `<details>` renders **automatically the moment it
  is revealed**, so it is safe to put diagrams in tabs/accordions - they never
  collapse. Manual
  arrangement is remembered per diagram
  source, so it survives a theme switch or a live morph. (A Mermaid node/edge is
  **clicked** to leave a comment - its text can't be text-selected - while a drag
  still pans/moves it, so commenting and rearrange coexist without a mode. The SVG
  shows the normal arrow cursor at rest and switches to a grabbing cursor only
  while you actually drag.)
- **Code** - `<pre><code class="language-python">...</code></pre>` is highlighted
  by highlight.js and rendered in a framed block with a **language-name header**
  and a **line-number gutter** (the gutter stays pinned while long lines scroll
  horizontally). The language shown comes from the `language-xxx` class.
- **Diffs** - write a fenced `diff` block or `<pre><code class="language-diff">...</code></pre>`. htmlit renders it with full-row red and green lines, aligned old and new line numbers, and a Unified/Split toggle. No custom CSS is needed.

- **Theme** - the panel's **Dark** toggle flips `html.dark`, `html[data-theme]`,
  `color-scheme`, the highlight.js theme, and Mermaid's theme. Style your
  artifact for both (e.g. `html.dark body { ... }`); you do not need to build any
  theming UI yourself.
- **Follow-up answers** - when the user asks a follow-up and you add content,
  wrap it so it reads as a Q&A reply:

  ```html
  <section data-htmlit-answer data-question="How does caching work?" data-htmlit-answer-for="cmh2k7f3q">
    <p>The API checks Redis first; on a miss it reads Postgres...</p>
  </section>
  ```

  The client frames it with a **"&#8627; You asked: &lt;question&gt;"** header
  (pure CSS, so it is morph-safe). `data-question` is optional - if omitted, the
  client fills in the user's latest message. `data-htmlit-answer-for` is the
  `commentId` from the prompt you are answering: set it whenever the prompt has a
  non-empty `commentId` so the user's "you asked here" anchor links to this answer
  (their click on the anchor then jumps here) **and the answer is rendered inline in
  that comment's rail card** (an "Agent" reply in the card thread, with a "View in
  document" link) - so it is always visible from the document, never only in the
  chat. Omit it for freeform/diagram prompts. Any content a morph introduces (this
  block included) is briefly **flashed and scrolled into view**, so a new answer is
  never missed.

  **Place it in context.** If the question came from an annotation (the prompt has
  a `selector`), insert this block as the **next sibling right after the annotated
  element**, so the answer sits with what the user pointed at - not off in a
  separate section. The block is styled to hug the element above it, reading as an
  attached reply. For a freeform question with no target, put it wherever it reads
  best (often right after the relevant content).

The review panel is **always visible** (docked right; the artifact reserves
space for it). It carries the **Dark** toggle and a **Keep** toggle (persist the
artifact + conversation on end, with a shown resume command). Annotation needs no
toggle - it is always on: the user **selects any text** (as in Google Docs) and a
small floating menu offers two actions:

- **Highlight** - a **local note**. It becomes a persistent yellow `<mark>` in
  the document, is saved with the review (restored on resume), rides along into
  the **HTML report and Print/PDF exports**, and is **never sent to the agent**.
  Clicking an existing highlight re-opens the menu with **Remove** (and Ask agent).
- **Ask agent** - opens a prompt box and is **sent to you** on Send, pinned to the
  exact span. Only after the prompt is submitted does the span keep a subtle
  **comment anchor** (a light accent underline whose tooltip shows *"You asked: …"*);
  while the user is still selecting text - before choosing Ask agent - there is no
  such marker, just the browser's own selection. Once **you answer** that comment
  (tagging your `data-htmlit-answer` block with its `commentId`), the anchor turns
  into a solid underline and **clicking it scrolls to and flashes your answer**.
  Before it is answered, clicking the anchor offers **Ask agent / Remove**. Anchors
  are saved with the review but are a live-review marker only - stripped from your
  snapshot and from the HTML/PDF exports.

A **Mermaid** node/edge (whose text isn't selectable, since dragging pans the
diagram) is targeted with a **click**, which offers **Ask agent** only (a text
note doesn't apply to a diagram shape). Sending leaves a persistent purple
**outline box** on that node/edge - the diagram equivalent of a text comment
anchor - that re-resolves across Mermaid re-renders and, once you answer, becomes
the clickable jump to your answer. The CSS selector is never shown to the user,
but comments deliver it (and a `commentId`) to you in `prompts[]`; highlights and
anchors stay local.

## Visual guidance

- Lead with the most important decisions, risks, tradeoffs, and next actions.
- Use sections, cards, tables, diagrams, and side-by-side comparisons over long
  prose.
- Prevent horizontal overflow at every nesting level (nested grid/flex children
  need `min-width:0`; wrap or truncate long unbreakable/monospace text). The
  browser reports overflow back to you as `layout_warnings` - fix it.

`htmlit` does not impose a design system. If the user named one, use it; if the
artifact previews a specific app's UI, match that app's design; otherwise keep it
simple and clean. A working starter lives at `examples/demo.html`
(`htmlit examples/demo.html`).

## Notes

- One daemon serves **many concurrent sessions**, each keyed by the artifact's
  absolute path (different files are fully isolated - their reloads, chat, and
  feedback never cross; the same file opened twice shares one session).
  Registered at `~/.htmlit/server.json` (override with `HTMLIT_HOME`).
- It **self-stops when idle** - once no browser is connected and the agent has
  gone quiet for a grace period (default 60s, set `HTMLIT_IDLE_SECS`), the daemon
  exits, so nothing lingers after the page or the Copilot session is closed. A
  closed tab is detected within ~1s; the next `htmlit <file>` just respawns it.
  `htmlit stop` forces it down immediately. Idle-stop **never deletes** the
  artifact (it only stops the daemon) - the file is only removed on an explicit
  `end`.
- **Artifact cleanup is automatic but scoped.** On `end`, htmlit deletes the
  artifact only when it lives under a `.htmlit/` directory (where you should
  generate review files) and tidies the folder if it empties. A user's own
  hand-authored file elsewhere is never deleted. Overrides: `htmlit open
  <file> --keep` (never delete), `htmlit open <file> --clean` or `htmlit end
  <file> --keep` for per-case control. The panel's **Keep** toggle is the
  in-page equivalent: turning it on sets the session to persist, so `end` keeps
  the artifact and writes a `<file>.htmlit.json` sidecar with the chat thread
  (and any `htmlit context` handoff note). Re-running `htmlit <file>` then
  **resumes** the review - the conversation is restored and the CLI surfaces the
  handoff note so a fresh agent can continue; the panel shows the resume command
  whenever Keep is on.
- It binds `127.0.0.1` on an ephemeral port - local only.
- **The page/tab title is the launching Copilot session's name**, so multiple
  reviews from different sessions are easy to tell apart. `htmlit <file>` reads it
  from `~/.copilot/session-state/$COPILOT_AGENT_SESSION_ID/workspace.yaml` and uses
  it for both the panel header and the browser tab `<title>`. Pass `--name` to
  override, or it falls back to the filename outside a Copilot session.
- **The daemon is version-aware**: it hashes its runtime files (the `client/`
  modules and stylesheet plus the `htmlit_core` package) and reports it on `/health`. If you
  edit the skill, the next `htmlit <file>` notices the mismatch and **auto-restarts
  the daemon** so changes always take effect (it prints a one-line notice and the
  new session URL). No more silently reusing a stale server.
- Artifacts stay portable: opened directly (without `htmlit`), the file renders
  normally; the toolbar simply isn't there.
