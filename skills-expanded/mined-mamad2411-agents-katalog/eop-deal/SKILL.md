---
name: eop-deal
description: >
  The dealer for a repo-grounded Elevation of Privilege (EoP) threat-modeling game night.
  Use this skill when the user wants to "deal an EoP deck for <repo>", run an EoP / STRIDE
  game session against a real codebase, produce a printable or web threat-modeling deck
  where each card names real files, endpoints, and trust boundaries, or get a dealer's
  diagram plus a score card to play by the original rules. Trigger on "deal me an EoP
  deck", "run a threat-modeling game on this repo", "make a STRIDE card deck for our
  system", or "set up an EoP session". Builds on eop-deck.
license: CC-BY-3.0-US (deck content © 2009 Microsoft Corporation)
metadata:
  version: "0.1.0"
  author: Stacey Vetzal
---

# eop-deal — repo-grounded EoP game night

The dealer. Point it at a repo and it produces everything a team needs to play a real
Elevation of Privilege session: a system diagram, a **playable deck where every card names
the team's actual files, endpoints, and boundaries**, and a score card. The threats are
undeniably *theirs*.

Depends on **`eop-deck`** for the deck data, the grounding procedure, and the bug-test.

## Output format (resolved)

A **single self-contained HTML file** that is both viewable in a browser and
print-friendly (print to PDF for physical cards). No build step, no local dependencies —
fits the publishable, self-contained-repo constraint. A markdown score card is emitted
alongside for recording threats during play.

## Dealing a session — procedure

When asked to deal a deck for `<repo>`:

### 1. Ground the repo (via eop-deck)

Follow `eop-deck`'s grounding procedure (`../eop-deck/references/grounding.md`):

- Survey entry points, data stores, external dependencies, processes, trust boundaries.
- Draw the Mermaid data-flow diagram with boundaries as subgraphs.
- Ground all 74 cards onto named components, or mark them `wild`.

Write the result as a **grounded-deck JSON** conforming to
`../eop-deck/references/grounded-deck-schema.md` (`schema: eop-grounded-deck/1`). Save it
into the repo's **`.threat-model/` folder** (the suite's shared artifact location — see
`eop-deck`'s "Where artifacts go"): `<repo>/.threat-model/eop-<reponame>.grounded.json`.

Do the grounding work yourself (you are the agent) — that is the part that requires
reading the code. Be concrete: name `src/auth/login.ts`, `POST /api/orders`, the `users`
table. Honest `wild` beats a contrived link.

### 2. Render the playable deck — REQUIRED, do not skip

The grounded JSON is an intermediate, **not** the deliverable. You **must** run the bundled
renderer to produce the HTML deck — do not stop at the JSON, and do not hand-author the HTML
yourself (the renderer ships the diagram rendering, styling, and print layout). Python 3.8+,
stdlib only, no install:

```bash
python3 .claude/skills/eop-deal/assets/render_deck.py \
  <repo>/.threat-model/eop-<reponame>.grounded.json
```

With no `--out`, it writes into `<cwd>/.threat-model/` (created if missing). Run it from the
repo root so the artifacts land in `<repo>/.threat-model/`, or pass
`--out <repo>/.threat-model/eop-deck-<reponame>` explicitly.

It reads the grounded deck plus `eop-deck`'s `assets/deck.json` (auto-located) and writes:

- `<out>.html` — the self-contained, printable deck: dealer's diagram (rendered in-page via
  mermaid from a CDN), how-to-play panel, and all 74 cards grouped by suit. Each card shows
  the printed threat **and** the grounded "In `<repo>`: …" statement with component chips and
  the boundary it crosses. Trump, open-threat (Ace), and wild cards are badged.
- `<out>.scorecard.html` — a printable, browser-editable score card (Name / Points / Card /
  Component(s) / Notes) styled to match the deck; fill it in on screen or print it.
- `<out>.scorecard.md` — the same score card as markdown, handy to commit/edit in the repo.

The renderer warns (does not fail) if any of the 74 cards lack a grounding entry — aim for
full coverage so the deck is complete.

**Confirm both files exist** and report their paths before handing off. If only the JSON
was produced, the deal is not done.

### 3. Hand off to the table

Tell the user where the files are and how to use them:

- Open the `.html` in a browser to play on screen, or **print to PDF** for physical cards.
- Deal to 3–6 players; play starts with the **3 of Tampering**; EoP trumps.
- Adjudicate disputes with the bug-test.

Announce the rules from `references/rules.md` (read it first). The original scoring: **1
point** per threat on your card, **+1** for taking the trick.

## The deliverable (plan's "done when")

A playable end-to-end first session: diagram + grounded deck + score card, produced from a
single repo path, playable by the original rules.

## The guardrail

You deal the deck and ground the threats in real code. You do **not** decide whether a
threat is real — the table does, settled by the bug-test. The argument is the learning;
keep the dealer in service of it.

## Provenance

Deck content © 2009 Microsoft Corporation, CC BY 3.0 US, via `eop-deck`.
