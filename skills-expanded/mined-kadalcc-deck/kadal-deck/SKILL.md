---
name: kadal-deck
description: Create, edit, check, screenshot, export and publish presentations with Kadal Deck — slides written in MDX (deck.mdx) with clicks, layouts, animated backgrounds, speaker notes and a live audience room. Use when the user wants slides, a deck, a talk or a presentation made or changed, when a folder contains deck.mdx or depends on @kadal/deck, or when they mention Kadal Deck, deck.kadal.cc or kadal-deck.
license: AGPL-3.0-or-later
compatibility: Node 20.19+ and npm/pnpm/yarn/bun. Screenshots and export need Playwright with Chromium (npm i -D playwright && npx playwright install chromium). Publishing needs a one-time `kadal-deck login` by the user.
metadata:
  homepage: https://deck.kadal.cc
  repository: https://github.com/kadalcc/deck
---

# Kadal Deck

A deck is a folder with one `deck.mdx` (the slides), `deck.config.ts` (engine settings),
`src/components.tsx` (the deck's own components), `src/styles.css`, and `public/` (images,
videos). Everything happens through the `kadal-deck` CLI (from `@kadal/deck`) or, when it is
connected, the `kadal-deck` MCP server, whose tools mirror the CLI and add slide-level editing
and `slide_render` (pictures of slides).

## Workflow

1. **Start.** New deck: `npx @kadal/deck new <dir> --title "Talk title" --yes` (MCP:
   `deck_create`). Existing deck: read the outline first (`deck_outline`, or skim `deck.mdx`).
   A Slidev deck (slides.md): `npx kadal-deck import slidev <folder>` converts it into a new
   folder; a reveal.js deck (index.html): `npx kadal-deck import reveal <folder>`. Then work
   through its `IMPORT-REPORT.md` (errors first) and check as below.
2. **Plan the arc** before writing: title → hook → 3–5 sections, one idea per slide → close with
   the one thing to remember. Roughly one slide per minute. Read
   [references/design-guide.md](references/design-guide.md) once per task.
3. **Write.** Follow [references/authoring.md](references/authoring.md) for the file format and
   MDX rules. Look up every component, layout or background before using it —
   `npx kadal-deck info components <Name>` / `info layouts` / `info backgrounds`, or MCP
   `deck_reference`. With MCP, edit through `slide_update` / `slide_add` / `notes_set` (they
   touch only that slide and lint it); otherwise edit `deck.mdx` directly.
4. **Check.** `npx kadal-deck check` (MCP `deck_check`). Fix every error; read the warnings.
   Exit code 1 means errors remain. `npx kadal-deck format` tidies the file (separators,
   frontmatter YAML, each slide's Markdown; code, notes and sugar stay as written); `--check`
   only reports.
5. **Look.** `npx kadal-deck screenshot --slide all` writes `screenshots/slide-NNN.png` (MCP
   `slide_render` returns the images). Open and inspect every picture: text overflowing or
   clipped, crowding, tiny type, low contrast, empty halves, broken images or components. Fix and
   look again. Try `--scheme dark` if the deck allows dark mode.
   Then **measure legibility**: `npx kadal-deck contrast` (or `check --contrast`) checks every
   text on every slide, click step and scheme against what is really behind it and exits 1 below
   WCAG AA (4.5:1; 3:1 from 24px, or 18.66px bold). `--out contrast/` draws the failures. Fix the
   colour per scheme, add a scrim, or go larger and heavier — never dim body text to set a mood.
   `data-contrast="ignore"` is only for purely decorative text (a watermark numeral, a texture).
6. **Ship** when the user asks: `npx kadal-deck build` (static `dist/`; `--base /path/` for a
   sub-path, `pwa: true` to present offline, `bundleRemoteAssets: true` for no network at all,
   `seoMeta.ogImage: auto` for a link-preview picture; `npx kadal-deck ci github-pages` — or
   netlify, vercel, cloudflare, docker — writes the host's deploy files), `npx kadal-deck export
   --png --pptx` (PDF/PNG/PPTX in `export/`; `--format pptx-editable` for a PowerPoint file with
   native, editable text, `--format md` for Markdown with the notes, `--range 1,3-5`, `--dark`),
   or `npx kadal-deck publish` (a URL with a live room on deck.kadal.cc). `download: true` in the
   headmatter adds a Download button and makes `build` write `dist/deck.pdf` for it; any deck
   also exports from the browser at `/<deck>/export`. Publishing needs the user to have run `npx kadal-deck login` once — never
   try to sign in yourself; if `kadal-deck whoami` exits 3, ask them to.

`npx kadal-deck dev` serves the deck with live reload for the user (MCP `deck_preview` returns
the URL); `--tunnel` gives it a public https address (Cloudflare Quick Tunnel, needs `cloudflared`;
the presenter is password-guarded), `--remote <password>` puts it on the network with the
presenter behind a password. `?` in the browser lists keys; `E` opens the side editor (the
slide's source beside it, Cmd/Ctrl+S saves into the file); `S` opens the presenter view; `R` narrates — reads each
`[click]` part of the notes aloud and turns the pages, for rehearsal. `npx kadal-deck narrate`
bakes that speech into `public/narration/` (it needs `kokoro-js`: run it with `--setup` first,
which installs a few hundred MB — only when the user wants recorded narration).

## The format in one screen

```mdx
---
title: Hello, room
author: Ana
theme: minimal
---

# Hello, room

A one-line promise of what they will learn.

<Notes>Welcome everyone. [click] (notes pace with clicks)</Notes>

---
layout: section
---

# Part one

---

## One idea per slide

<Clicks>

- Each item appears on a click
- Speaker notes follow the clicks

</Clicks>

<Notes>Intro. [click] First point. [click] Second point.</Notes>

----

## A vertical slide (beneath the previous one)
```

- `---` starts a slide; `----` starts one beneath the previous (a vertical stack).
- YAML right after a separator, closed by `---`, is that slide's frontmatter. The block at the
  very top is the **headmatter**: deck settings *and* the first slide's frontmatter.
  `deck.config.ts` overrides the headmatter — change a setting where it is actually set.
- Built-in components need no import; the deck's own go in `src/components.tsx`.
- Images and videos live in `public/` and are referenced as `/name.png`.
- Fun media: `<Sticker src x y size />` (over the slide, draggable in dev), `<Emoji name="party-popper" />`,
  `<Gif provider="klipy" src title />` (hot-linked; exports show a link card), `<Meme src captions />` —
  see "Stickers, emoji, GIFs and memes" in references/authoring.md.
- Find media instead of guessing URLs: `npx kadal-deck media search <icon|emoji|sticker|gif|meme|template|kadal> <words>`
  (MCP `media_search` / `media_trending`) and paste the result's `mdx` unchanged; after a KLIPY one,
  `media used klipy <id>` (MCP `media_used`). `credits: true` in the headmatter adds a Credits slide
  and a corner link to it — the credits are automatic.

## Reference (load when needed)

- [references/authoring.md](references/authoring.md) — file format, MDX pitfalls, custom
  components and CSS, code blocks, maths, diagrams, glossary terms, includes.
- [references/components.md](references/components.md) — every built-in component with props,
  defaults and an example; click effects; code-fence options. (Generated from the engine.)
- [references/layouts-and-backgrounds.md](references/layouts-and-backgrounds.md) — layouts,
  backgrounds, themes, transitions, every slide and deck frontmatter key. (Generated.)
- [references/live-room.md](references/live-room.md) — polls, quizzes, questions, reactions and
  how the audience joins.
- [references/design-guide.md](references/design-guide.md) — how to make a talk that works.

`npx kadal-deck info --search <words>` searches all of it; add `--json` for data.

## Web edits and conflicts

A published deck can also be edited on the web (quick edit in the builder, agents through the
remote MCP). `kadal-deck publish` uploads the editable source (deck.mdx, `pages/`, `slides/`, YAML,
`data/`, `drawings/` — privately) so it can, and `.kadal-deck/` remembers the version this folder
last synced with.

- **Always `npx kadal-deck status` before editing a published deck.** "The web has N newer
  versions" → `npx kadal-deck pull` first, then edit.
- **Pull before you publish.** `publish` exits **4** (`error.code: "diverged"`) when the deck
  changed on the web since your last sync. Never answer that with `--force` unless the person says
  so: it replaces their web edits (they stay in the version history; `pull --version N` brings
  them back).
- `pull` merges slide by slide: what only one side changed is taken, both sides' new slides are
  kept. The same lines changed both ways become git-style markers and exit **5**:
  `<<<<<<< local (your files)` … `=======` … `>>>>>>> web v14 (quick edit by Asha, …)`.
- Stickers and images picked in the builder are files named `assets/media/<hash>.<ext>`; `pull`
  downloads the ones the slides name into `public/assets/media/` (leave the path as written).
- Resolve by reading both sides (`npx kadal-deck resolve --list`, or the file): prefer keeping
  both sides' intent — `resolve deck.mdx#3 --both`, then edit the slide to blend them; `--ours` /
  `--theirs` keep one side. Ask the person when the two edits contradict. Never delete either
  side's content silently. Then `check`, then `publish`. `publish` refuses while any marker is left.
- MCP: `deck_sync_status` → `deck_pull` → `deck_conflicts` → `deck_resolve` → `deck_check` →
  `deck_publish` (which returns `{ok:false, reason:"diverged"}` instead of failing).
- `--no-source` keeps the source off the host (quick edit off; it sticks until `--source`).
  `.kadaldeckignore` (gitignore syntax) leaves files out.

## CLI facts for scripts

Every command but `dev`, `build` and `mcp` takes `--json` (one JSON object on stdout, logs on
stderr) and `--dir <path>`. Exit codes: 0 ok · 1 failed (check found errors) · 2 usage ·
3 not signed in · 4 missing prerequisite (no deck.mdx, dependencies or Chromium not installed),
or from `publish`: the deck changed on the web (`error.code` "diverged") · 5 unresolved merge
conflicts (`pull`, `resolve`, `publish`).
`screenshot` flags: `--slide N` (repeatable, or `all`), `--scheme light|dark`, `--theme <name>`,
`--width <px>`, `--dev` (skip the production build). Each picture shows the slide with every click revealed.
`contrast` flags: `--scheme light|dark|both` (both), `--min <ratio>` (4.5), `--min-large <ratio>`
(3), `--percentile <p>` (10: the worst tenth of the background under a line decides), `--range
1,3-5`, `--no-clicks`, `--url <published deck>`, `--out <dir>`, `--json` (`findings[]`: slide, id,
steps, scheme, text, fontSize, ratio, required, fg, bg, path). Exit 1 when any text fails.
