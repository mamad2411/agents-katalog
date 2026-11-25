---
name: maple-preview
description: "Use when a MapleStory asset request resolves to more than one plausible candidate: a look described by colour, style, or mood instead of an exact name or ID (a black cap, a white tee, a monster that suits this map), a maple-lookup search returning several close matches, or the user asking to preview, compare, or choose between assets before they are used. Builds a local page the user picks from; when it was not invoked by name, it asks first."
---

# maple-preview

A comparison page for choosing Maple assets by eye. Candidates render as icons or animated
sprites, and for an outfit the current picks are worn on a character. The builder's choice
comes back as a `[MAPLE-PREVIEW]` paste or as card numbers, and the build continues with
exactly those IDs. How assets are looked up, structured, and rendered is the `maple-make`
skill's knowledge — this skill only settles *which* asset.

## When it fires, and the one question

A search for a described look returns several close matches. The search score ranks name and
description similarity, not looks: `Goggled Black Cap 1073` over `Black Baseball Cap 767` says
nothing about which hat the builder pictured. So:

- **Two or more plausible candidates for a described look → never pick silently.** "The top
  score is clear", "the description was specific enough", "no ambiguity here" are judgements
  about names, and the builder has not seen a single pixel yet.
- **Invoked by name, or the builder asked to preview, compare, or choose** → build the page.
- **Not invoked** → ask one line in the builder's language and end the turn, with the counts:
  `5 caps, 4 tops and 4 pants matched. Shall I build a preview page so you can compare them?`
  Build on yes. On no, list the candidates as numbered text and ask which; on "just pick for me",
  take the top match per slot and say which ones you took.
- An exact name or ID, or a single candidate → the skill does not apply.

## Building the page

1. **Candidates** — 2–6 per slot from `search(query, category, tags)`; every result carries
   `id`, `name`, `score`, and a `thumbnail` URL. A query in Korean that returns unrelated names
   usually works as the English item name (`black cap`, `red pants`); a mob search narrows with
   `tags` such as `tier:low`. For a mood with no name ("something that suits this map", "a
   similar vibe"), `search_similar` with a `text` description returns rows from every category
   — keep the ones that carry an `id` in the wanted category. Drop what plainly mismatches the
   description. One slot per requested part (`cap`, `coat`, `pants`, …) or role (`mob`); `pick`
   is `one` for an outfit slot and `many` for a roster.
2. **Sprite data, one call per candidate** — `get_sprite_data(category, id, ["stand1"])` for a
   character part (`["default"]` for a face), `["stand"]` for a mob or NPC. The response is
   `{ info, <action>: [frame, …] }`: paste the action's frame array as `sprite` unchanged, the
   result's `thumbnail` as `thumbnail`, and `info.vslot` as `vslot` when present (hat masking).
   When any character slot exists, fetch the base the same way: body `2000` and head `12000`
   both under category `body`, face `20000` (action `default`), hair `30000`.
3. **The file** — copy `preview.html` (it ships beside this SKILL.md) to
   `.maple-preview/<NN>-<topic>.html` under the project root, `NN` counting up from `01`, and
   replace the one line `/*MAPLE_PREVIEW_DATA*/` with the JSON described below. Nothing else in
   the template changes. Never reuse a filename; a revised set gets the next number.
4. **Open it** — try the OS opener (`open` on macOS, `xdg-open` on Linux, `start` on Windows)
   and print the absolute path in every case; in a remote or container session say it has to
   be opened locally. Suggest `.maple-preview/` for `.gitignore` if it is not there.
5. **End the turn** — the path, what the page shows, and how to answer: the **Copy selection**
   button, or numbers per slot (`cap #2`).

### Data — the JSON inside `#maple-preview-data`

| Field | Meaning |
|---|---|
| `lang` | `ko` or `en` — the page's own labels |
| `title`, `request` | heading, and the request in the builder's words |
| `base.body` `.head` `.face` `.hair` | required when a character slot exists — the base parts' frame arrays |
| `slots[]` | `key` (echoed in the paste), `label`, `category`, `pick` (`one` / `many`), `candidates[]` |
| `candidates[]` | `id`, `name`, `sprite`; optional `thumbnail`, `vslot`, `image` (any PNG URL or CDN path for the card), `note`, `selected: true` (your recommendation, pre-picked) |
| `zmap` | optional `data/zmap.json` key order — only if the game data's layer table changed |

`category` is one of `cap coat longcoat pants shoes glove weapon cape shield accessory hair
face` (worn on the character) or `mob npc` (animated card). The page loads PNGs and nothing
else — the CDN answers no cross-origin JSON request, which is why sprite data is embedded
rather than fetched. It reads the tool's frame arrays, raw CDN frame objects, and
`"0.body"`-style flat keys alike.

```json
{ "lang": "en", "title": "Black cap · white tee · red pants",
  "request": "a character in a black cap, a white tee and red pants",
  "base": { "body": [ { "body": {}, "arm": {}, "delay": 500 } ], "head": [ { "head": {}, "ear": {} } ],
            "face": [ { "face": {} } ], "hair": [ { "hair": {}, "hairOverHead": {} } ] },
  "slots": [
    { "key": "cap", "label": "Cap", "category": "cap", "pick": "one", "candidates": [
      { "id": "1002060", "name": "Black Baseball Cap", "thumbnail": "https://…/icon.png",
        "sprite": [ { "default": {} }, { "default": {} }, { "default": {} } ], "vslot": "CpH1H5", "selected": true },
      { "id": "1002130", "name": "Black Loosecap", "thumbnail": "https://…/icon.png", "sprite": [ { "default": {} } ] } ] },
    { "key": "mob", "label": "Mob", "category": "mob", "pick": "many", "candidates": [
      { "id": "1210102", "name": "Orange Mushroom", "thumbnail": "https://…/stand/0.png",
        "sprite": [ { "cdn_url": "https://…/move/0.png", "origin": {}, "delay": 180 }, { "cdn_url": "https://…/stand/1.png", "origin": {}, "delay": 180 } ] } ] } ] }
```

(`{}` stands for the part data as the tool returned it — `cdn_url`, `origin`, `map`, `z`.)

## Reading the answer

- A `[MAPLE-PREVIEW]` block: one line per slot, `key: id (name)[, id (name)]`. A slot showing
  `(none)` in the page's language → ask about that slot in one line; do not fill it yourself.
- Numbers: `#n` is the card's position within its slot, in the order you listed candidates.
- Then continue with `maple-make` using exactly those IDs — no new search, no substitution, no
  "similar" swap. Rendering the chosen assets is that skill's job.
- "Show me others" → a new file with the next number and new candidates.

## Constraints

- Never build the page when the skill was not invoked and the builder has not said yes.
- Never decide among plausible candidates by score alone.
- The template is verbatim; the only edit is the data line.
- No credential goes into the page: it loads public PNGs only.
