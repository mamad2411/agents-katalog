---
name: storyteller
description: Written and paper gifts that still have something to touch - pop-up cards, envelopes, letters from objects, poems in fixed forms, short stories, zines, deadpan documents (awards, patents, newspapers, museum labels, reports) and interactive fiction. Emotion and interaction first, a share frame, private names marked, typography, and how to use kit/story, kit/paper and kit/document.
license: MIT
---

# Storyteller

Words are the cheapest medium and the easiest to do badly. Read `gift-director` first: every gift hits the three criteria (emotional effect, delightful interaction, shareability). A flat page with a poem on it is the lazy version of this skill. The writing has to be good, **and** the page has to do something: unfold, peel open, stamp, rustle, reveal a second layer.

## Forms

| Form | Make it touchable | Kit |
|---|---|---|
| Pop-up card | It opens in 3D; the inside pops up; a hidden flap under one fold | `kit/paper/` (pop-up card, envelope) when present, `kit/story/card.js`, `kit/templates/greeting-card.html` |
| Letter | Arrives in an envelope you tear or unseal; a postscript hidden under the stamp | `kit/paper/` envelope, `kit/story/letter.js` |
| Letters from objects | Their kettle, bike or plant writes to them; each letter opens from a different object | `letter.js`, `kit/paper/` |
| Poem in a form | Sonnet, villanelle, haiku sequence, limerick chain, acrostic; lines appear as they scratch, fold or turn | `card.js`, `kit/templates/zine.html` |
| Short story | 600–1500 words, one scene, one turn; pages turn, a map fills in, or a choice at the end | `letter.js`, `booklet.js` |
| Zine | 8 pages, one topic, printable fold; one page has a flap or a pull-tab | `booklet.js`, `kit/templates/zine.html`, `kit/art/print.js` |
| Deadpan document | Award, patent, museum label, annual report, newspaper, horoscope: played completely straight, with one interactive twist (stamp it, sign it, unfold the chart) | `kit/document/` when present, `type.js` |
| Interactive fiction | 8–30 nodes, meaningful choices, at least one ending worth finding; undo and restart | `kit/story/fiction.js` |

If a kit block named here is missing, build the effect yourself (CSS 3D transforms, a clip-path reveal, a canvas scratch layer).

## Craft rules

- **Pick the emotion before the first word** (`funny`, `ridiculous`, `absurd`, `cute` or `touching`) and cut everything that does not serve it. Touching pieces land better from Day 5 on.
- **Name the interaction** before writing (`open`, `unfold`, `peel`, `scratch`, `stamp`, `turn`). The first one is discoverable in under 3 seconds; one surprise sits deeper in.
- Concrete nouns over adjectives. "The kettle, the blue one with the dent" beats "your cosy kitchen".
- A poem in a form must keep the form. Count syllables and check the rhyme scheme before packaging. A broken villanelle is worse than a good free-verse poem.
- Personal facts: from what you legitimately know (memory, profile, history, granted folders). Never invent one. If you know nothing, write about the season, the hour, the door, the act of opening a small envelope.
- Humour: one good joke per piece, placed late. Never jokes about the person's `dislikes` or `avoid` topics.
- Language: the brief's `language`. Write natively when the form depends on sound.
- Deadpan documents must be obviously playful (absurd issuer, impossible dates) so they cannot be mistaken for real paperwork. No real logos, no real institutions presented as issuers.
- Interactive fiction: every choice changes something visible; dead ends say so with grace; the ending screen offers "Start again". Reachable in under 10 minutes.

## The share frame

Design it while you write. A card: opened, the pop-up standing, the best line legible on a phone. A deadpan award: the certificate stamped, title and seal readable. A letter: the envelope half-open with the first line showing. Expose `window.adventCapture.prepare(kind)` that puts the page in that state with the buttons hidden, and declare `"share": { "still": { "capture": "still" } }`.

Salutations, names, addresses and places go in elements with `data-advent-private` (and in `share.privateText`) so the privacy preview can blur them. Anything sensitive stays out of the share frame entirely.

## Typography

- Display: a serif stack (`Georgia, 'Iowan Old Style', 'Palatino Linotype', serif`). Body: `-apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif` or a readable serif at 18–20 px with 1.5–1.6 line height, 60–70 characters per line.
- Handwriting: `kit/story/type.js` gives stacks such as `'Caveat', 'Bradley Hand', 'Segoe Print', cursive`. **No font files are bundled** and gifts never load fonts from the network. If you embed a font file, it must be OFL and credited.
- Paper: warm background (`--milk #FFFAF0`), ink `--ink #243A32`, soft shadow, a paper texture from `kit/paper/` if present. `kit/tokens.css` has the palette; any style is allowed.
- Print: for cards and zines include `@media print` rules from `kit/art/print.js`: page size, margins, no buttons on paper. Print files go in `downloads`.

## Packaging

- `form: "interactive-html"` with the embedded manifest (or `entry: "index.html"` in a folder), `family` (`paper-and-pop-ups`, `deadpan-documents`, `heart`), `emotion`, `interaction`, `tierUsed`, `share`.
- A plain text or markdown gift has nothing to touch and no share frame: use it only when the brief leaves no other option.
- Put a short `note`: why this piece, for them.

## Self-check

Read the whole piece aloud in your head once. Fix anything you stumble on. Confirm form constraints (syllables, rhyme, page count), that no invented fact slipped in, that nothing in `dislikes`/`avoid` appears, that the interaction is found in 3 seconds, and that `prepare("still")` produces the frame you pictured.
