# Figures & Models — curation hints

## What belongs here

Manufactured character and model **lines**, curated whole:

- **Figures** — action figures, chibi (Nendoroid), scale, vinyl (Funko Pop),
  blind-box designer (Pop Mart), diorama (Re-Ment).
- **Model kits** — build-it-yourself kits assembled from molded parts into
  one specific, non-reconfigurable model. Gunpla (Bandai's Gundam kits) is
  the worked example; conventional scale-model lines (Tamiya, Revell,
  Airfix) belong here too, none curated yet.
- **Construction sets** — reusable brick systems sold as numbered sets, i.e.
  [`lego/`](lego/CLAUDE.md).

**Whether the buyer assembles the thing is a property of the line, not a
directory axis.** A built Nendoroid, an unbuilt Gunpla runner, and a LEGO
set are all molded-plastic objects sold in numbered product lines; splitting
them into separate families only forced every line near the boundary to be
argued about twice. Record assembly in the line's own `CLAUDE.md` and
`item-attributes.schema.json` where it affects how items are identified (grades,
part counts, instruction numbering) — not by filing the line somewhere else.

**A line is curated whole — don't slice one line by object type.** If an
item shipped as part of the line, it's in, whatever kind of object it is:
the figures plus their companion **vehicles**, **playsets and locations**,
and **role-play pieces** (weapons, morphers, and the like). A buildable
vehicle inside a figure line stays with that line rather than being re-filed
next to standalone kits; the product line is the unit, not the object.

What's out isn't an object category; it's things that aren't the line:

- **Separate non-figure merchandise** — apparel, stationery, homeware, food
  and other consumables. A franchise's t-shirts or erasers are a different
  product line (see [`re-ment/CLAUDE.md`](re-ment/CLAUDE.md)
  and [`funism/CLAUDE.md`](funism/CLAUDE.md) for the same carve-out).
- **Standalone plush lines** — their own top-level family,
  [`plush/`](../plush/CLAUDE.md).
- **One-off items with no product line behind them** — a single promotional
  statue or prop that isn't part of a released line.

`figures-and-models/` is a sibling of the other collecting-domain families
(`plush/`, `trading-cards/`, `comics-and-manga/`, ...). The boundary with
them is which product line an item belongs to, not what the item physically
is.

## How the tree is organized: manufacturer/brand first, franchise via tags

The directory tree under `figures-and-models/` encodes **one** axis: the
manufacturer/brand that makes the item. Franchise/IP is **not** a directory
axis — it's carried by `tags/franchises/` entities (see
[`../CLAUDE.md`](../CLAUDE.md#tags)). Keeping the two separate is what makes
every directory level mean the same thing.

**A top-level directory here is the customer-facing brand under which the
line is sold** — the entity whose own storefront/site presents it, not
necessarily the deepest legal manufacturer. A brand's individual product
lines nest beneath it:

```
figures-and-models/
  good-smile/                    # customer-facing brand (Good Smile Company)
    nendoroid/                    # one of its lines
    figma/                        # another (Max Factory, sold under Good Smile)
  funko/
    pop/
  bandai/
    gashapon/
    gunpla/                       # a model-kit line, same axis as any other
    power-rangers/                # a franchise sold under Bandai's own name
  lego/                           # brand and line are the same entity here
    star-wars/                    # LEGO's own theme/subtheme grouping
```

Model-kit and construction lines sit on this axis unchanged — Gunpla is a
Bandai line, so it's `bandai/gunpla/` alongside `gashapon/`, and LEGO is its
own brand at the top level. Neither needs a separate tier for being
assemble-it-yourself.

- **Cut at the customer-facing brand, not the deepest legal parent.** figma
  is made by Max Factory (a Good Smile subsidiary) but listed on the Good
  Smile Company storefront, so it's `good-smile/figma/`. Sister/subsidiary
  brands fold into the parent that presents them (Banpresto → `bandai/`).
- **A brand with only one line curated still gets its own directory** when
  it's a real manufacturer that plausibly sells others — the directory is a
  stable home for future siblings, not redundant nesting. Worked example:
  [`good-smile/nendoroid/CLAUDE.md`](good-smile/nendoroid/CLAUDE.md) under
  the [`good-smile/`](good-smile/CLAUDE.md) umbrella.

**Franchise may appear as a line-level directory under a manufacturer** — e.g.
`bandai/power-rangers/`, `re-ment/pokemon/` — where the franchise is
functioning as *that maker's* product line. It is never a **top-level** axis
of its own, and cross-cutting franchise discovery always comes from the tag,
never from a franchise directory sitting at the root.

### When a franchise spans manufacturers

Two shapes, decided by whether the franchise's toys carry their own unifying
product-line brand:

- **No unifying brand — sold under each maker's own name → split by
  manufacturer.** Power Rangers toys were made by Bandai (1993–early 2000s)
  and Hasbro (2019 on), each under its own name. They split into
  `bandai/power-rangers/` and `hasbro/power-rangers/`, reunified by a shared
  `power-rangers` franchise tag. **Tag the franchise from the first
  manufacturer's directory onward — don't wait for the second one to
  exist.** The directory does express the franchise, but only to someone
  already browsing that directory; a franchise search resolves from tags
  alone (see [`../CLAUDE.md`](../CLAUDE.md#tags)), so an untagged
  single-manufacturer line is simply invisible to it. Waiting also means the
  tag has to be retrofitted at exactly the moment the tree is being
  restructured, which is the worst time to remember it.
- **Its own unifying brand → stays top-level under that brand.**
  [`firelink/`](firelink/CLAUDE.md) is a licensed label whose products carry
  the "FireLink" brand even though different manufacturers produce different
  series — so it's a single top-level directory, no split. The brand name,
  not the maker, is the constant.

## Adding a new product line

A line arrives in **two phases — scaffold it first, author its conventions
when it actually has items.** See
[`../CLAUDE.md`](../CLAUDE.md#scaffolding-a-new-collection) for the rule and
why it works this way; the phases below are this family's version of it.

**Phase 1 — scaffold.** No new conventions needed; anyone (or any automated
curation pass) can do this.

1. Identify the customer-facing brand and place the line under it:
   `figures-and-models/<brand>/<line>/`. Create the `<brand>/` umbrella
   (`_collection.yaml` + `CLAUDE.md`) if it doesn't exist yet. A line that is
   its own top-level brand goes directly at `figures-and-models/<line>/`.
2. Write its `_collection.yaml` (`type: collection`, plus a `description`).
   The line inherits the nearest ancestor's `CLAUDE.md` and
   `item-attributes.schema.json` for now.
3. Run the validator before opening a PR.

**Phase 2 — author its conventions.** Required before the first item is filed
under the line, unless the parent brand's own `CLAUDE.md` already documents
this tier (as `pop-mart/CLAUDE.md` does for its IP directories).

4. Write the line's `CLAUDE.md` — identification scheme, naming convention,
   known pitfalls (variant/re-release numbering is common in this domain —
   check for it explicitly rather than assuming a line is flatly numbered).
   For a kit or construction line, cover how assembly shapes identification
   (grades, scales, set numbering) here rather than treating it as a reason
   to file the line elsewhere.
5. Write its `item-attributes.schema.json` — don't reuse another line's attributes
   as-is; verify against manufacturer listings or a fan database (e.g.
   MyFigureCollection, Gunpla Wiki, Brickset) rather than guessing.
6. Run the validator before opening a PR.

Deferring phase 2 is not a licence to skip it — it's that a line's
identification scheme is far easier to get right while holding real product
data than in the abstract, and a speculative schema tends to be contradicted
by the first ten items that arrive.
