# FireLink — curation hints

## Directory structure

```
firelink/
  CLAUDE.md
  item-attributes.schema.json
  _collection.yaml               # the whole "FireLink" brand
  <game>/
    _collection.yaml             # e.g. "Elden Ring"
    <series>/
      _collection.yaml           # e.g. "Series 1"
      <slugified-name>.yaml
```

Three levels: **game → series → figure**. Unlike Nendoroid, FireLink has no
catalog numbering that spans franchises, and unlike Pokémon TCG, series
names collide across games (multiple unrelated FireLink products are all
informally called "Series 1"). The `<game>/` level exists specifically to
disambiguate that collision — don't flatten it even if a game currently has
only one series.

## Manufacturer is not constant

"FireLink" is a Bandai Namco–licensed brand, not one company's in-house
line. Different series are produced by different manufacturers under the
same FireLink branding (e.g. one Dark Souls series is attributed to a
different manufacturer than the others). Always verify `attributes.manufacturer`
per series rather than assuming it matches an earlier one.

## Series naming is not official

No manufacturer-published series name could be found for any FireLink line
as of this writing — retailers each use their own label ("Series 1", "Vol.
01", a two-character subtitle like "Malenia & Melina Series") for the same
product. Directory names like `series-1` here are an **editorial
convention we chose**, not a sourced fact — document any new series the
same way (sequential `series-<n>`) rather than adopting one retailer's
marketing name as if it were official.

## Character naming also varies by retailer

Cross-check a character's name across at least two sources before filing —
retailers disagree even on individual figure names (e.g. one lists "Vargram
the Raging Wolf", another's product image is filed as "Vargram the Bloody
Wolf"; "Alexander, Warrior Jar" vs. "Iron Fist Alexander" for the same
figure). Prefer the manufacturer/license-holder's own storefront listing
(e.g. Bandai Namco's official store) as canonical when it's available;
otherwise pick the most consistent name across independent retailers and
note the variants you saw in the PR description.

## Identifying items

No official per-figure catalog number exists — series are small (typically
6 standard figures, "no duplicates" in a full set) and figures are
identified by character name within their series directory. Each blind box
includes a character-description "ID card," not a numbered checklist item.

## Secret/chase variants

Blind-box lines in this category commonly include an unannounced rare
"chase" figure beyond the standard lineup. Don't add one speculatively —
only file a chase figure once you have first-hand or clearly corroborated
confirmation it exists for that specific series (a single uncorroborated
mention isn't enough; manufacturers don't advertise these, so official
listings won't confirm or deny them either way).

## Release date

Manufacturers don't publish official release dates for these. Absent a
better source, use a reputable retailer's "date first available" as a
reasonable proxy and note in the PR which listing it came from — store just
the year (`date: "YYYY"`) unless that listing's month/day is itself
reliable enough to trust.
