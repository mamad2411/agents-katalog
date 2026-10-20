# Trading Cards — curation hints

## What belongs here

Collectible cards sold in sets — anything printed as a card and collected as
a set belongs here, whether or not it's playable:

- **Trading card games** with a structured ruleset (deck-building, matches,
  official expansions) — Pokémon TCG, Magic: The Gathering, Yu-Gi-Oh!.
- **Sports cards** — Topps, Panini, Upper Deck, and similar.
- **Non-sport card sets** — Garbage Pail Kids, Marvel Universe, movie and TV
  tie-in sets, and other one-off or seasonal card releases.

The distinction that used to gate this family (playable game vs. novelty
card set) is no longer a boundary — it's a property of the individual line,
recorded in that line's own `_collection.yaml` and `CLAUDE.md`. It does
still shape the internal structure, though: see below.

Not card-shaped things that aren't collected as card sets — a board game's
component deck belongs with the product it ships in, not here.

## Directory structure

```
trading-cards/
  CLAUDE.md
  item-attributes.schema.json        # generic fallback; each line overrides it
  collection-attributes.schema.json  # collection-record attributes (total_cards) — see below
  _collection.yaml                   # this domain family's own entity record
  <line>/
    CLAUDE.md                    # line-specific conventions — required
    item-attributes.schema.json  # line-specific attributes — required
    _collection.yaml
    ...                          # line's own internal structure
```

**Every set's `_collection.yaml` carries `attributes.total_cards`** — the
publisher's official card count for that set, inherited from this family's
own `collection-attributes.schema.json` rather than a per-line one, since the concept
and shape (a non-negative integer) are identical across every line here. A
line-level `_collection.yaml` (the whole game, a series/block grouping)
doesn't carry it — only a set/expansion record does, since that's the level
with an actual published count.

Each line is a full top-level collection in its own right, not a thin
subdirectory — it needs its own `CLAUDE.md` and `item-attributes.schema.json` since
card attributes, numbering, and pitfalls vary by line. See the root
[`collections/README.md`](../README.md) for how directory position
determines parentage.

**How deep a line nests depends on how much it publishes.** An ongoing TCG
needs intermediate grouping levels to stay under the size guidelines in
[`../CLAUDE.md`](../CLAUDE.md) — Pokémon TCG uses series → expansion → card,
which is why no single directory holds every card in the game. A line that
released one set, or one set per year, doesn't need that machinery; a flat
set → card layout is correct for it. Follow
[`pokemon-tcg/CLAUDE.md`](pokemon-tcg/CLAUDE.md) as the worked example of
the deep case, and don't manufacture a series tier for a line that has no
real one.

## Adding a new line

A line arrives in **two phases — scaffold it first, author its conventions
when it actually has cards filed.** See
[`../CLAUDE.md`](../CLAUDE.md#scaffolding-a-new-collection) for the rule and
why it works this way; the phases below are this family's version of it.

**Phase 1 — scaffold.** No new conventions needed; anyone (or any automated
curation pass) can do this.

1. Create `trading-cards/<line>/`.
2. Write its `_collection.yaml` (`type: collection`, plus a `description`).
   The line inherits this family's `CLAUDE.md` and `item-attributes.schema.json`
   for now.
3. Run the validator before opening a PR.

**Phase 2 — author its conventions.** Required before the first card is filed
under the line.

4. Write its `CLAUDE.md` — identification scheme, naming convention,
   completeness-checking approach, known pitfalls. Say whether the line is a
   playable game or a non-game set, and what its intermediate grouping
   levels (if any) are.
5. Write its `item-attributes.schema.json`. **Don't inherit this family's
   `item-attributes.schema.json` as-is** — write attributes specific to the
   line (see `pokemon-tcg/item-attributes.schema.json`).
6. Run the validator before opening a PR.

**Phase 2 is not deferrable far in this family.** A card game's set codes,
collector numbering, and rarity ladder are game-specific enough that the
family schema is a placeholder for the scaffold only, never something a real
card should be filed against — expect to author conventions as soon as
curation of the line genuinely starts.
