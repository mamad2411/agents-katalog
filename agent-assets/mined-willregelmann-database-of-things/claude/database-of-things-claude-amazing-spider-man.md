# The Amazing Spider-Man (Vol. 1) — curation hints

## Directory structure

```
amazing-spider-man/
  CLAUDE.md
  item-attributes.schema.json
  _collection.yaml               # Vol. 1 as a whole
  <number>-the-amazing-spider-man-<number>.yaml
```

Flat — Vol. 1 numbering is continuous across the whole run, #1 (March 1963)
through #441 (November 1998), never resetting within the volume. Marvel's
later relaunches (Vol. 2 1999, Vol. 3 2003, and subsequent renumbering
games) are out of scope here and would be separate sibling series
directories if added, not folded into this one — same reasoning as keeping
Batman's pre-New 52 and New 52 runs apart.

**Annuals and the retroactive `#-1` flashback issue are a separate
numbering line, not part of this run.** Don't mix them into the flat
1–441 sequence if added later.

## Identifying items

Issues are identified by number; `name` is `"The Amazing Spider-Man #<N>"`.
Early issues (#1–2 seeded so far) are anthology-style with more than one
distinct story per issue — the `number` still identifies the whole issue as
one entity, don't split an issue into multiple entities per story.

## Naming files

`<number>-the-amazing-spider-man-<number>.yaml`, number zero-padded to 3
digits (e.g. `001`, `441`) — matching the volume's known total run length,
same reasoning as Monstress's per-series digit-width judgment call.

## Release dates

Only month-level cover dates are reliably sourced for the 1963 issues
seeded so far (no verified exact on-sale day) — use `"1963-03"` etc. rather
than fabricating a day. Verify against a second source (mycomicshop,
Marvel Database) before trusting a single listing.

## Creative team

Stan Lee (writer) and Steve Ditko (artist) on #1–5 (seeded so far) — this
was Lee/Ditko's run through #38 before Ditko left the title. Confirm
writer/artist per issue rather than assuming Lee/Ditko holds for later
issues once the run is extended past #38.

## Common pitfalls

- Cover-blurb taglines (e.g. "...the Chameleon Strikes!") aren't
  necessarily the formal indicia story titles — GCD/comics.org has the
  precise indicia titles but returned HTTP 403 on direct fetch during
  seeding. A `title` attribute was deliberately left off issues #1–5 for
  this reason, matching Monstress's number-only approach; add one later
  only once indicia titles are confirmed from a source that actually
  resolves.
- Don't confuse a reprint/facsimile edition's listing with the original
  1963 printing when sourcing cover images or dates.
