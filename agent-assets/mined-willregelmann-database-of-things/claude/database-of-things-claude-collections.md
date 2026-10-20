# Collections — curation hints

Cross-cutting rules for anything under `collections/`. Applies everywhere;
a category or line's own `CLAUDE.md` (e.g.
[`trading-cards/pokemon-tcg/CLAUDE.md`](trading-cards/pokemon-tcg/CLAUDE.md))
adds detail on top — it doesn't replace this.

## Collectibles, not products

**The entity is the collectible — the individual physical thing someone owns,
not the product it was sold as.** A sealed booster pack, a multipack, a
regional SKU are commercial units, not entities.

Deduplicate on **physical uniqueness, not product identity**:

- Same physical object, different packaging (loose vs. gift-set, pack vs.
  tin) → one entity.
- Different physical object (paint, foil, colorway, printed number) → a
  distinguishable entity. When it's the exact same printing/number as
  another entity and only a print treatment differs — a Reverse Holo or
  1st Edition/Shadowless/Unlimited stamp on one numbered Pokémon TCG card, a
  variant cover on one numbered comic issue, a Funko Pop chase/glow/flocked
  release sharing its common counterpart's Pop! No. — file it as a
  `variants` sub-entity on that item instead of duplicating a whole new one
  (see [`docs/primitives/ITEM.md`](../docs/primitives/ITEM.md), "Variants").
  Otherwise — when it carries its own independent number or identity in the
  source material — it's a full top-level item.

Follows from it: packaging is never a directory tier; a retail bundle isn't
a collectible — file the figures it contains, not the bundle. Contrast a
LEGO set, which *is* the collectible: its minifigs aren't filed as separate
items, just tracked with a summary attribute (e.g. `attributes.minifigCount`)
when the category cares to. A container only gets its own entity when it's
itself collected.

Where "a variant" vs. "the same thing" falls, and whether a variant becomes
its own item or a `variants` sub-entity, is a **per-category call** — settle
it in that category's own `CLAUDE.md` before filing at scale.

## Tree shape

```
<category>/<brand>[/<line>[/<subline>…]]/<item>
```

- **category** — the domain family under `collections/` (`trading-cards/`,
  `figures-and-models/`, ...). DBoT's own grouping, not something released.
- **brand** — required; whatever name the maker/seller puts on the product
  (manufacturer, publisher, game, or product brand, depending on category —
  each category's `CLAUDE.md` says which). Ownership/appearance on the
  product is the test, not trademark registration.
- **line** / **subline** — optional, subline may repeat. A tier must be
  named by the brand or the collecting community — never invented for
  symmetry.
- **item** — the leaf entity file, at whatever depth its collection sits.

**Never split one brand across sibling directories** (`squishmallows/` and
`squishmallows-squish-a-longs/`) — everything a brand sells nests under its
one directory, subdivided by line, even when a line's objects differ in
kind from the rest of the brand.

A franchise name is fine as a **line** under its own manufacturer
(`re-ment/pokemon/`), never as a **brand** — the franchise itself lives in a
`tags/franchises/` tag, not the tree.

## Collection shape

A collection is usually all nested collections *or* all items, rarely mixed
at one level — a small, distinctly-scoped exception is fine, but mixing
should need a reason. Rarely exceed 1000 items or 100 nested collections;
past that, look for a natural subdivision in the source material (series,
era, product line) rather than piling on.

## Scaffolding a new collection

New lines arrive in two phases:

1. **Scaffold** — directory + `_collection.yaml`, nothing else. It inherits
   `CLAUDE.md`/`item-attributes.schema.json` from the nearest ancestor. An
   itemless `_collection.yaml` is a legitimate record of "exists, not yet
   curated" — don't hold it out of the tree waiting on an ID scheme.
2. **Author conventions** — before the *first item* is filed, give the line
   its own `CLAUDE.md` and `item-attributes.schema.json`, unless the parent
   already documents its conventions explicitly (e.g. POP MART's IP
   directories).

Identification schemes are easier to get right with real product data in
hand than in the abstract — that's why this order, not the reverse.

## Dates

`date` is the entity's **first** release, a quoted string at whatever
precision the source supports (`"1999"`, `"1999-06"`, `"1999-06-30"`) —
never padded beyond it. Applies at every level, including a grouping
collection (series, line, publisher): its `date` matches its earliest
already-sourced child rather than being re-derived independently.
Domain-family directories don't get one — they're organizational, not
released.

## Descriptions

`description` is optional prose, mostly on `_collection.yaml` records. Write
**original synthesis only** — never paste or lightly reword source text
(the catalog is CC0; a wiki's copyleft license isn't compatible). Keep it a
few factual sentences; leave it off when the name and hierarchy already say
enough.

## Tags

`tags` is a flat array of ids referencing `tags/` entities — the fix for
groupings directory position can't express, franchise being the main case.

**Tags accumulate down the hierarchy; `attributes` don't — use that
difference to decide which one a new field belongs in.** A tag placed on
a collection implicitly applies to every collection and item nested under
it, recursively, all the way down — that's the mechanism, not just a
convention: the validator resolves an item's tags from itself *or any
ancestor collection* and flags re-tagging a child with what an ancestor
already carries as a duplicate. An `attributes` field carries no such
propagation — it describes only the one entity it's written on, and says
nothing about that entity's parent, children, or siblings. So the test for
a new field is: **would this value hold uniformly for everything nested
below some point in the tree, and should it apply to all of it
automatically? Tag the root of that subtree once.** **Is it a fact about
just this one collection or item, unrelated to what's nested inside or
around it? That's an `attributes` field** (or, if it's already implied by
where the entity sits, nothing at all — directory position needs no
restating).

- Reference by **id**, always — reuse an existing tag or create its entity
  file first; no ad hoc string tagging. Duplicate ids in one list are an
  error.
- **Franchise always goes in `tags`, never in `attributes`** — even within
  one line, and even the first time it appears (don't wait for it to span
  two collections). It's the recurring instance of the general rule above:
  a franchise is true of everything under it, so it belongs at the
  **highest level where it's uniformly true** — the collection if the
  whole thing is one franchise, individual items if a collection mixes
  franchises — never both an item and its already-tagged ancestor.
- Don't over-tag: skip anything directory position or `attributes` already
  covers, and keep the list short — rarely more than 5.

See [`tags/CLAUDE.md`](../tags/CLAUDE.md) for adding a new tag entity.

## Logos

Add `image` to a `_collection.yaml` when a real official logo/mark exists,
from an authoritative source (rights-holder assets, Wikimedia Commons) —
verify it resolves. Leave it off rather than cropping one out of a
marketing photo, or substituting a franchise's logo for a line merely
licensed from it — the mark must belong to the entity itself.