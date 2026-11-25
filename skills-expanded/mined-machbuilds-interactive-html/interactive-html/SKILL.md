---
name: interactive-html
version: 1.0.0
author: machbuilds
license: MIT
homepage: https://github.com/machbuilds/interactive-html
tags: [html, generation, design, feedback, annotations, comments, sse, developer-tools, agent-skills]
description: Turn a folder of static HTML into a live commenting surface and act as the agent that responds. Inject a client library, start a local server, watch an on-disk inbox; when the user highlights text, picks an element, drags a region, or asks a question, read it and edit the HTML in response. If the user has no HTML yet, generate a polished self-contained page from their description first, then start the comment loop. Trigger phrases — "make this page interactive", "make these pages interactive", "let me comment on this page", "make this interactive", "add feedback to this page", "comment on this page", "build me a page", "create an html page", "turn this into a page", "make a page about", "design a page for", "make an interactive page from this".
---

# Interactive HTML

Turn any folder of HTML into a place the user can leave inline comments
(text selections, element selections, page-level notes), then **you are the
agent** that responds: comments land in an on-disk inbox, you read them, edit
the HTML, and the page auto-reloads with a walkthrough of what changed.

Because *you* (the current session) do the edits, there is no separate agent
process and no cold-start — the loop is as fast as you can make an edit.

## Runtime location

This skill is self-contained: its runtime ships in this same directory. The
installer bakes the absolute path below in at install time, so every command
here is runnable as written.

```
IH_HOME = __IH_HOME__
```

## When to invoke

- "make this page interactive" / "make these pages interactive" → **Setup flow** (existing HTML)
- "let me comment on this page" / "add feedback to this page" → **Setup flow**
- "build me a page about …" / "create an html page" / "design a page for …" → **Generate flow**, then offer the loop
- "make an interactive page from this" / "I have this content, make it an interactive page" → **Generate flow** → **Setup flow** back-to-back, no second confirmation
- "stop the interactive server" / "shut it down" → **Stop flow**
- "make these pages static again" / "remove the comment layer" → **Removal flow**

## Setup flow

1. **Pick the target directory.** Default to the current working directory
   (the project the user is in). If they name a folder, use that. If it has no
   `*.html`, see the Create-then-setup flow.

2. **Launch** — inject the client tags and start the server in one step, in the
   background (do NOT block the session):

   ```
   python __IH_HOME__/cli/ih.py <dir> --no-watch --no-open
   ```

   `--no-watch` is important: it starts the server only, because **you** are the
   agent — we do not want a second `claude -p` agent competing with you. The
   launcher prints the page URLs (it auto-bumps off a busy port).

3. **Tell the user the URL(s)** it printed, e.g. `http://localhost:5050/index.html`.

4. **Monitor the inbox** so new comments notify you immediately:

   ```
   Monitor on path: <dir>/.ih/comments.jsonl
   ```

   Do NOT poll — let the Monitor notification arrive.

## Responding to a comment batch

When a new line appears in `<dir>/.ih/comments.jsonl`:

- Read the new batch. Each comment has a stable `id`, a `kind`
  (`text` / `element` / `region` / `general`), an `intent`
  (`change` / `question`), and an `anchor` with a CSS `selector`, `tag`,
  `quote`, and `html_snippet`. **Locate the element by its visible text
  or `html_snippet`** — match on content, not on runtime-only attributes.
  `kind: "region"` comments add `anchor.multi` (selectors for every element
  the user circled) and `anchor.region` (the drawn rectangle, page
  coordinates) — treat the set as the target area.

- **`intent: "question"` comments are questions, not edit requests.** Do
  NOT modify the page for them. Answer in the update's `answers` array
  (schema below) — concretely, citing the relevant part of the page. The
  client shows your answer in its Q&A tab, anchored to where they asked.

- For `intent: "change"` comments, edit the relevant `*.html` file(s).
  Keep edits minimal and focused on what was asked.

- Wrap each logical change in `<span data-ih-change="ch-<slug>">…</span>`, or
  add a `data-ih-change="ch-<slug>"` attribute to an existing wrapping element.
  Exactly one anchor per change — the page uses these for the walkthrough.

- **Append** one batch object to `<dir>/.ih/updates.json`. It is a JSON array
  (newest last) — read it, append, write the whole array back:

  ```json
  {
    "batch_id": "u-<short-slug>",
    "timestamp": "<ISO 8601 UTC, e.g. 2026-06-07T12:00:00Z>",
    "in_response_to_batch": "<batch_id from the inbox line>",
    "changes": [
      {
        "id": "ch-<slug>",
        "anchor": "ch-<slug>",
        "in_response_to": ["<comment id you addressed>"],
        "title": "short, concrete label",
        "description": "one or two sentences for the record"
      }
    ],
    "answers": [
      {
        "id": "a-<slug>",
        "in_response_to": ["<comment id of the question>"],
        "text": "your answer, plain prose"
      }
    ]
  }
  ```

  Omit `changes` or `answers` when empty. An answers-only update doesn't
  reload the page — the client surfaces it in the Q&A tab in place.

The server detects the write and pushes an SSE event; the page reloads with
scroll preserved and offers a tour (or, for answers-only updates, shows the
Q&A tab without reloading). The page's busy banner clears when a change's or
answer's `in_response_to` matches a submitted comment id.

Rules:
- Edit only HTML files and `.ih/updates.json`.
- Every `id` under `changes` must have a matching `data-ih-change` in the HTML,
  and every new `data-ih-change` must appear in updates.json. Answers need no
  HTML anchor.
- Questions never modify the page unless the question explicitly asks for an
  edit too.

## Generate flow (when the user has no HTML yet)

When the user asks you to **build a page** ("build me a page about X", "make
a page from this content", "make an interactive page from this"), generate
the HTML first, then run the Setup flow on it.

### 1. Gather just enough context

If the user gave content or a clear description, don't interrogate them —
infer and build. Only ask when genuinely ambiguous, and at most once:

- **Purpose & audience** — who reads this and what should they do/feel?
- **Visual feel** — light or dark, dense or spacious, serious or playful?
- **Structure** — report, landing page, dashboard, docs, portfolio?

Default when unstated: light theme with `prefers-color-scheme` dark
support, spacious, content-first.

### 2. Write the page

One self-contained `*.html` file. Inline CSS in a `<style>` block. No
external dependencies — no CDNs, no Google Fonts, no frameworks. The file
must render perfectly from `file://` and offline. Save to the current
directory unless the user names one. Filename from the content
(`q3-report.html`, not `page1.html`).

#### Quality baseline (always)

- **Semantic HTML5** — `<header>`, `<nav>`, `<main>`, `<section>`,
  `<article>`, `<footer>`; one `<h1>`; heading levels never skip.
- **System font stack** — `-apple-system, BlinkMacSystemFont, "Segoe UI",
  system-ui, sans-serif` (and a mono stack for code). Crisp everywhere,
  zero network requests.
- **Design tokens as CSS custom properties** — colors, spacing scale, and
  radii defined once in `:root`, used everywhere. Makes later edits (and
  your agent edits via interactive comments) surgical.
- **Responsive by default** — readable at 375px, 768px, 1024px, 1440px.
  Prefer intrinsic layouts (max-width, flex/grid with minmax, `clamp()`
  for type) over breakpoint thickets.
- **Dark mode is mandatory, not optional.** Every page ships both modes:
  define all colors as tokens in `:root`, flip them in a single
  `@media (prefers-color-scheme: dark)` block, and never hardcode a color
  outside the tokens. A page that breaks in either mode is not done.
- **Reduced motion** — wrap animations in `prefers-reduced-motion: no-preference`.
- **Diagrams are inline SVG.** When the content describes structure, flow,
  sequence, comparison, or architecture, draw it — don't describe it in a
  paragraph. Inline `<svg>` only (no external images, no Mermaid script
  dependency). Use `currentColor` for strokes/text and the CSS tokens for
  fills so every diagram adapts to dark mode automatically. Label axes and
  nodes; a diagram that needs the surrounding prose to be understood has
  failed.
- **Accessibility** — visible focus states (`:focus-visible`), ARIA only
  where semantics don't already cover it, alt text, 44px minimum touch
  targets, AA contrast.
- **Real content** — never lorem ipsum. If the user's content is thin,
  write plausible, specific copy from context and mark anything invented
  with an HTML comment `<!-- TODO: verify -->`.

#### Design judgment (apply, don't recite)

- **Users scan, they don't read.** Strong visual hierarchy: prominence =
  importance. Clear sections. Front-load key terms in headings.
- **Don't make them think.** Self-evident beats clever. Use conventions —
  logo/title top-left, nav where people expect it.
- **Omit ruthlessly.** Cut half the words, then cut again. No happy talk,
  no filler introductions, no "Welcome to…".
- **One focal point per screen.** If everything shouts, nothing is heard.
- **Group related things visually; contain nested things.** Whitespace is
  the grouping tool, borders are the fallback.
- **Make clickable things look clickable** without hover — shape, color,
  placement.

#### Anti-slop list (never)

- Purple-to-blue gradient heroes as a default aesthetic
- Generic three-column "feature" grids with icon + blurb
- Decorative blobs, waves, or floating geometric shapes
- "Get Started" / "Learn More" buttons that lead nowhere
- Cookie-cutter testimonial sections with invented names
- Emoji as a substitute for visual design
- Drop-shadow rounded cards as the only component idea
- Center-everything layouts with no hierarchy
- Stock-photo placeholder rectangles

### 3. Self-QA before delivering (mandatory)

Run this checklist against the file you just wrote. Fix failures before
handing the file off — do not deliver a page that fails any of these:

- [ ] **Both color modes** — mentally render light and dark: every text/
      background pair stays readable, no hardcoded colors outside tokens
- [ ] **Heading hierarchy** — exactly one `<h1>`, no skipped levels
- [ ] **No placeholder content** — zero lorem ipsum; invented facts are
      marked `<!-- TODO: verify -->`
- [ ] **Zero network requests** — no CDN links, no Google Fonts, no
      external images; the page works from `file://` with WiFi off
- [ ] **375px sanity** — nothing overflows horizontally; touch targets
      ≥44px
- [ ] **SVGs in both modes** — diagrams use `currentColor`/tokens, legible
      on dark backgrounds
- [ ] **Focus visible** — interactive elements have a `:focus-visible`
      state

### 4. Chain into the comment loop

After saving:

1. Tell the user the file path you wrote.
2. Offer to open it (`open <file>` on macOS).
3. **If the original ask was "make an interactive page…"**, proceed
   immediately into the **Setup flow** above on the file's directory —
   don't make the user re-ask.
4. **Otherwise** offer: *"Want to iterate on it by commenting on the page
   itself? Say make it interactive and I'll start the comment loop."* If
   they accept, run Setup on the file's directory.

### Revision etiquette

When the user iterates later (in chat or via comments on the page):

- Edit the existing file; never regenerate from scratch unless asked —
  regeneration destroys their accumulated tweaks.
- Keep edits scoped to what was asked. The design tokens make global
  changes (colors, spacing) one-line edits.
- If a request conflicts with the quality baseline (e.g. "add a purple
  gradient hero"), do what they asked — the baseline is a default, not a
  veto over the user.

## On startup in a directory that already has `.ih/`

1. Read `.ih/comments.jsonl` for comment ids.
2. Read `.ih/updates.json` and union every `changes[*].in_response_to` —
   those are already handled.
3. If unhandled comments remain, tell the user the count and offer to process.
4. Either way, start the server (Setup step 2) and the Monitor (step 4).

## Stop flow

1. Find the port (the launcher printed it; default 5050). Confirm with
   `curl -s http://localhost:<port>/_ih/info`.
2. `lsof -ti:<port> | xargs kill`
3. Confirm `lsof -i:<port>` is silent.

The server also self-retires on parent-death or idle timeout, so if you simply
end the session it cleans itself up.

## Removal flow

Strip the client tags for a clean, server-independent copy:

```
python __IH_HOME__/cli/inject.py <dir> --remove
```

This leaves the `.ih/` directory in place; delete it manually if unwanted.

## Headless alternative (no live session)

When no Claude session is driving the page (e.g. an automated/background run),
use the standalone watcher instead of this skill — it dispatches batches to an
agent CLI:

```
python __IH_HOME__/cli/ih.py <dir>                  # full loop, claude -p agent
python __IH_HOME__/cli/ih.py <dir> --agent builtin  # bundled agent (ANTHROPIC_API_KEY)
```

## Gotchas

- The injected tags reference `/client/ih.css` and `/client/ih.js`, served by
  the server from the repo's `client/` folder. Pages only work through the
  server, not opened as `file://`.
- `.ih/updates.json` is append-only and order matters — append, don't prepend.
- `anchor` values in updates.json must match a real `data-ih-change` in the
  HTML, or the walkthrough warns "anchor not found".
