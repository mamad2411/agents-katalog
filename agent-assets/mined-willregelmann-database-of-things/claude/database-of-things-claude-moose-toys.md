# Moose Toys — curation hints

## What belongs here

Moose Toys' officially licensed and owned character figure lines, organized
by franchise. Bluey is the licensed one; Shopkins, The Trash Pack and Mighty
Beanz are Moose's own properties. Only Bluey has items so far — see
[`bluey/CLAUDE.md`](bluey/CLAUDE.md); the rest are scaffolds awaiting
curation.

## Directory structure

```
moose-toys/
  CLAUDE.md
  _collection.yaml               # Moose Toys itself
  <franchise>/                    # e.g. "bluey", "shopkins"
    CLAUDE.md                     # phase 2 — before the franchise's first item
    item-attributes.schema.json  # phase 2 — same
    _collection.yaml              # phase 1 — the scaffold
    ...
```

Same manufacturer-then-franchise nesting as
[`../re-ment/CLAUDE.md`](../re-ment/CLAUDE.md) and
[`../funism/CLAUDE.md`](../funism/CLAUDE.md) — Moose Toys holds toy licenses
and owns IP across many properties, so the franchise level exists from day
one even where a franchise isn't populated yet. A scaffolded franchise
carries only its `_collection.yaml` and inherits this file until someone
curates its items; see
[`../../CLAUDE.md`](../../CLAUDE.md#scaffolding-a-new-collection).

**Every franchise directory here gets a `tags/franchises/` tag**, whether the
property is licensed (Bluey) or Moose's own (Shopkins, The Trash Pack, Mighty
Beanz). Moose owning the IP doesn't make it any less a franchise to search
for — and several of these do appear outside Moose's own catalog.

## Not yet curated

Moose Toys' catalog is wider than what's scaffolded here. **The Grossery Gang**
(a Trash Pack follow-on) and **Treasure X** are the clearest remaining fits.
Others — Twisty Petz, Wow! Pod, Little Live Pets, Num Noms — need a scope
check against [`../CLAUDE.md`](../CLAUDE.md) before scaffolding, since not all
of them are character *figure* lines and some may belong to a different family
entirely.
