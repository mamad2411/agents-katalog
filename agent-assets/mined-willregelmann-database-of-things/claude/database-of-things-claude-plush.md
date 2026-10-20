# Plush — curation hints

## What belongs here

Stuffed/plush toys sold as collectible product lines — branded plush with
their own identification scheme, naming, or series/squad identity
(Squishmallows, Beanie Babies, Jellycat, etc.). Not a one-off promotional
plush with no product line behind it.

**A brand here is curated whole, and a sub-line doesn't leave the category
for being made of something else** — see
[`../CLAUDE.md`](../CLAUDE.md#tree-shape) for the general rule and its
limits. The worked case is Squishmallows' own **Squish-A-Longs**: 1"
squeezable *plastic* figures, not plush at all, filed at
[`squishmallows/squish-a-longs/`](squishmallows/squish-a-longs/) rather than
moved to `figures-and-models/`. They carry the Squishmallows name, use its
characters, and are collected by the same people tracking the plush line;
sorting them by material would just make a collector guess where each
sub-brand went.

The limit that matters most in this category: this keeps *one brand*
together. Jazwares, Kellytoy and the rest make plenty of plastic toys with no
plush line behind them, and those aren't a `plush/` concern.

## Directory structure

```
plush/
  CLAUDE.md
  item-attributes.schema.json  # generic fallback; each brand overrides it
  _collection.yaml               # this domain family's own entity record
  <brand>/                        # e.g. "squishmallows", "pokemon-center"
    CLAUDE.md                    # brand-specific conventions — required
    item-attributes.schema.json  # brand-specific attributes — required
    _collection.yaml             # the brand record — no items beside it
    <line>/                       # e.g. "original-squishmallows"
      _collection.yaml
      ...                        # the line's items, or further sublines
```

**Items live in a line, never at the brand tier.** Even a brand with one
format gets a named line under it — Squishmallows' standard line is
`squishmallows/original-squishmallows/`, using Jazwares' own name for it, so
that adding Squish-A-Longs beside it doesn't leave 2,321 loose items mixed in
with a nested collection (see [`../CLAUDE.md`](../CLAUDE.md), "Collection
shape").

**In this category the `<brand>` tier is the plush brand itself, not its
manufacturer** — `squishmallows/`, not `jazwares/squishmallows/`. That's the
customer-facing-brand rule from [`../CLAUDE.md`](../CLAUDE.md#tree-shape):
Squishmallows is what a collector buys and names, while its maker has changed
hands (Kellytoy → Jazwares) without the brand changing. `pokemon-center/` is
the same rule with a different answer — The Pokémon Company sells Sitting
Cuties under its own retail brand rather than through a third-party
manufacturer. Contrast `figures-and-models/`, where the rule lands on the
manufacturer instead.

Each brand (Squishmallows, etc.) is a full top-level collection in its own
right — identification schemes, manufacturers, and attributes differ by
brand. Follow the shape of
[`squishmallows/CLAUDE.md`](squishmallows/CLAUDE.md) as a worked example, and
see the root [`collections/README.md`](../README.md) for how directory
position determines parentage.

## Adding a new brand or sub-line

A line arrives in **two phases — scaffold it first, author its conventions
when it actually has items.** See
[`../CLAUDE.md`](../CLAUDE.md#scaffolding-a-new-collection) for the rule and
why it works this way; the phases below are this family's version of it.

**Phase 1 — scaffold.** No new conventions needed; anyone (or any automated
curation pass) can do this.

1. Confirm it belongs here at all — judged by **which brand it extends, not
   what it's made of** (see "What belongs here" above). A non-plush sub-line
   of a brand already curated here stays here; an unrelated line from the
   same manufacturer doesn't.
2. Place it. A new brand is `plush/<brand>/`. A sub-line of an existing brand
   **nests under that brand** — `plush/squishmallows/squish-a-longs/`, never
   a hyphenated sibling like `plush/squishmallows-squish-a-longs/`, which
   would split the brand across the category's top level (see
   [`../CLAUDE.md`](../CLAUDE.md#tree-shape)). A sub-line nests even though it
   restarts its own numbering — the restart is why it's a separate
   *collection*, not a reason to move it out from under its brand.
3. Write its `_collection.yaml` (`type: collection`, plus a `description`).
   The line inherits this family's `CLAUDE.md` and `item-attributes.schema.json` for
   now.
4. Run the validator before opening a PR.

**Phase 2 — author its conventions.** Required before the first item is filed
under the line.

5. Write its `CLAUDE.md` — identification scheme, naming convention, known
   pitfalls (many plush lines mix a global catalog number with sub-lines that
   restart their own numbering — check for this explicitly rather than
   assuming a line is flatly numbered).
6. Write its `item-attributes.schema.json` — don't reuse another line's attributes
   as-is; verify against manufacturer listings or a well-maintained fan
   database rather than guessing.
7. Run the validator before opening a PR.
