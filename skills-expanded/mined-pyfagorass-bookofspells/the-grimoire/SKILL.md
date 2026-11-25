---
name: the-grimoire
description: >-
  The index to a Book of Spells — a large, curated library of ready-made spells
  (skills in the SKILL.md format) gathered from many providers (Google, OpenAI,
  and more), covering cloud platforms, deployment, design tools, PDFs, browser
  automation, security, and much else. The spells are NOT preloaded — there may
  be thousands. Use this whenever the user asks to cast a spell, or for a spell
  to do something, or names a capability, provider, or tool you do not already
  have loaded (e.g. "cast a spell for Figma", "is there a spell for deploying?",
  "use the bigquery spell"), or whenever a task might be served by a specialised,
  ready-made spell. Casting a spell MEANS consulting this index to discover and
  load the right one on demand — do that first, rather than improvising. This is
  also the single entry point to the Book's own keystones: route here to AUTHOR a
  new spell (the-spellwright), to FIND or CONNECT an MCP server / external tool
  (the-emissary), or to INSTALL the Book into a conduit (the-tether).
---

# 📖 The Grimoire — One Spell to Find All Spells

You hold the index to a **Book of Spells**: a large, growing library of skills
("spells") transcribed from many providers. The spells themselves are *not*
loaded into your context — there may be hundreds or thousands of them, far more
than would fit. Instead, this single skill teaches you to **discover and summon**
exactly the spell you need, the moment you need it.

This is how you learn your own magical abilities. When the user bids you **cast a
spell**, or a task smells like something a specialised spell would handle — a
cloud service, a deployment, a design tool, a file format, a third-party API —
**come here first.** To cast a spell *is* to consult this index.

## Companion keystones — this one index routes to them all

You need tether only *this* spell. The Book's other native keystones are reached
straight through the catalogue below — no separate install — so route here first,
then open the one the task calls for:

- **Find a spell** — the rite on this page (discover and load a gathered spell).
- **Author a spell** — read `the-spellwright` (forge a new SKILL.md).
- **Find / connect an MCP server** — an *Emissary of the Pact* — read
  `the-emissary` (search the live MCP Registry and propose a connection).
- **Install the Book** into a conduit — read `the-tether` (symlink this keystone
  into the agent's skills directory).

To open any of them, grep the catalogue for its name and read the path it gives,
exactly as you would any spell.

## Where the Book lies

Relative to this `SKILL.md`, the Book sits one level up. The catalogue is
**hierarchical** so you never need read it whole:

- **`../skills/INDEX.md`** — tiny: just the houses and their spell counts. Safe
  to read whole; stays small no matter how large the Book grows.
- **`../skills/_index/<house>.md`** — one house's spells (e.g. `google.md`,
  `openai.md`), each with a one-line description **and the exact read-path** of
  its `SKILL.md`. Bounded reads, one drawer at a time.
- **`../skills/catalog.json`** — the full machine-readable ledger:
  `[{ "name", "provider", "description", "path" }, …]`. Grep or `jq` it; do not
  read it whole.
- **`../skills/<house>/<spell>/SKILL.md`** — each spell in full, nested under its
  house, alongside any `references/`, `scripts/`, or `assets/` it needs. The
  folder isn't always guessable from the name, so **read the `path` the index
  line gives you** rather than assembling it yourself.

(If this skill was installed by symlink, those paths resolve into the
`book-of-spells` repository it points at.)

## The Rite of Wielding

1. **Seek.** Never read the whole catalogue — it may hold thousands of spells.
   *Grep* the per-house indexes (or the json) for the user's intent:

   ```bash
   grep -ri "bigquery"  ../skills/_index/          # all houses at once
   grep -i  "deploy"    ../skills/_index/google.md  # one house, if known
   ```

   Search by capability ("deploy", "pdf", "screenshot"), by provider
   ("google", "openai"), or by the exact name the user spoke. Read
   `../skills/INDEX.md` (tiny) only to see which houses exist.

2. **Choose.** Read the matching descriptions and pick the best-fitting spell.
   If several fit, prefer the most specific; if none fit, say so plainly and
   proceed without one rather than forcing a poor match.

3. **Read in full.** Open that spell's own file and read it completely before
   acting. Every index line ends with *"read at `…`"* — a transcribed spell at
   `../skills/<house>/<spell>/SKILL.md`, a keystone (e.g. `the-spellwright`) at
   its own root path. Follow that path verbatim; don't assemble one from the
   name. The one-line index description is only a signpost; the spell's true
   instructions, guardrails, and helper scripts live in its own SKILL.md.

4. **Wield.** Follow the spell's instructions faithfully, including any
   `scripts/` or `references/` it directs you to. Honour its safety wards.

5. **Name your source.** When a spell shapes your work, tell the user which one
   you invoked (e.g. *"following the `google-bigquery-basics` spell"*), so they
   can trace and trust the working.

## Wards

- **Discover before improvising.** If a fitting spell exists, read and follow it
  rather than inventing your own approach from memory.
- **A signpost is not the spell.** Never act on the index description alone —
  always open the full SKILL.md.
- **No fitting spell? Say so.** Don't twist an unrelated spell to a task it
  wasn't written for. An honest "the Book holds nothing for this" is a valid
  outcome.

*The Book is large, and you need carry none of it — only the knowing of how to
open it.* 🕯️
