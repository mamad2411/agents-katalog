---
name: design-and-settings-of-elements
description: "Both natures. The look of an element (design skills tested on a test home page, the approved design, colours and fonts) and its site settings (name, search, languages, menus, cookie banner, switches, the CONFIG link): where each is changed — the core's «Build → Design» and «Build → Site settings» of the element — and how the whole design path runs from the architect's Telegram with `npm run design`. Load it when the person asks to choose or test design skills, to make or compare test pages, to approve a design, to change colours, a font, the title, the menu, «hide sign-in», «turn on the footer», sends a screenshot or a link of a site whose style they like, asks where an element's design or settings are, or asks for a page or a section of one (a hero, pricing, questions, a comparison) and where such sections live."
---

# Design and settings of elements

**Process: working** — data only: the element's agent builds every page; you pass the person's choices through the core's door.

A hint, not a law: models of late 2026 work worse under rigid step-by-step instructions.

## Where things are (node steps 712, 713, 715)

- **Design** — the core's page `/<lang>/<element>/build/design`, three steps: **1 Skills** — the library of design skills of
  third-party developers (each with its GitHub repository), the person saves the ones to test; **2 Brief** — optional; **3 Generate and
  compare** — a carousel (red «not generated», amber «being built», green «generated»), the chosen test page large, «Change the
  reference», «Fine tuning» and «Approve this design for the element». After the approval the person asks the element's agent for every
  important page in turn — it builds them in that design.
- **Site settings** — `/<lang>/<element>/build/site-settings`: the CONFIG link in one line on top, then sections (basics, search, meta and
  media, languages, header, footer, cookie banner, switches, Web4 network). A saved value redraws the pages with no build; only languages
  need a deploy. Linked to CONFIG — the values are read-only there and change in CONFIG.
- A look the settings cannot express (a new token, a new block) is code — hand it to the element's agent (`route-to-element`).

## A page or a section of a page (node step 716)

Every element designs its own pages: its sections are its own code (`components/blocks/` of that element), built by its agent's design
pass in the element's approved design; the node has no shared catalogue of sections and no shared design. A request for a page or a
section of element X goes to X's agent, never to you — `npm run task -- <id> "Build process, design: <the person's words>"` (the node
starts the session of that pass with its own skills) or X's terminal and Telegram bot (`route-to-element`). Why one change needs a build
and another does not, in the person's words: a new section is code — the element is built once (beside the running version, switched in
seconds); a new page made of sections the element already has, other words or another order is page data — no build.

## The design path from Telegram (the owner 2026-11-10: «создания проекта прямо из Telegram в том числе и дизайна»)

The same actions as the tab, through the same door: `npm run design -- <element> <command>`.

- «покажи навыки дизайна» → `library [words]`: say the number, then three to five names — each with its GitHub link and one line of
  what it brings; never the whole list.
- «возьми на тест X» → `choose <mark>`. «убери X» → `drop <mark>`.
- A photo or a link of a site they like → for a photo `download_attachment`, then `ref <mark> <file> --caption "<their words>"`; a link
  — `ref <mark> <https://…>`. Ask which skill only if more than one is saved.
- «сгенерируй» → say the price first (`state` prints it), then `generate <mark>`; it takes about ten minutes; the command puts the element
  under your supervision for one cycle, so its «done» wakes you — then `shots <id>` and send both pictures to the chat with one line each
  and the link of the whole page (on this computer `http://127.0.0.1:<its port>/<lang>/prototypes/<id>`, on its own domain its address).
- «утверди этот» → only on their explicit yes for a named test page: `approve <id>`; then tell them to ask the element's agent for the
  other pages one by one (its terminal or its Telegram bot).
- `state` answers «как там дизайн?» in two lines: what is saved, what is generated, what is approved.

A skill with scripts is installed only after a separate «yes» (`generate … --scripts-yes`). One generation at a time per element.
