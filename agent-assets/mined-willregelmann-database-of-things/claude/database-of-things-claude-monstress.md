# Monstress — curation hints

## Directory structure

```
monstress/
  CLAUDE.md
  item-attributes.schema.json
  _collection.yaml               # the whole "Monstress" series
  <number>-monstress-<number>.yaml
```

Flat — issue numbering is continuous across the whole run (#1, #2, #3...,
never resets), so there's no set/arc grouping needed to disambiguate, same
reasoning as Nendoroid's flat catalog.

**Talk-Stories is a separate miniseries, not part of this numbering.**
There's a 2-issue side series, *Monstress: Talk-Stories*, that bridges
story arcs and uses its own independent numbering (#1–2) — it is not yet
curated here. When adding it, file it as `monstress/talk-stories/`, a
sibling directory, not mixed into the main flat numbering — same precedent
as `wizards-black-star-promos` living beside Pokémon TCG's series
directories rather than inside one of them.

**Trade paperback volumes are deliberately not modeled yet.** Individual
issues are the entities; TPB volumes (currently 10, collecting issues
#1–60) repackage issues that already exist here rather than being distinct
collectibles. If volume tracking is wanted later, prefer a per-issue
`volume` attribute over separate volume entities, to avoid duplicating data
that's really just a grouping label — but confirm that approach with a
maintainer before adding it, since it wasn't part of the original design.

## Creative team

Marjorie Liu (writer) and Sana Takeda (artist — she also colors her own
work; there is no separate colorist) have been consistent across the
entire run as of issue #62. Rus Wooton letters throughout. `writer`/`artist`
are still captured per-issue rather than assumed constant — don't skip
setting them, in case a future guest issue breaks the pattern.

## Identifying items

Issues have no individual titles — they're identified by number only.
Entity `name` is `"Monstress #<N>"`.

## Naming files

`<number>-monstress-<number>.yaml`, number zero-padded to 3 digits (e.g.
`001`, `062`). This is an ongoing series with no fixed total — 3 digits is
a judgment call based on current volume (62 issues as of mid-2026), not a
canonical width, same reasoning as Nendoroid's 4-digit choice.

## Release dates

Issues #1–6 carry a full `date: "YYYY-MM-DD"` (see
[`collections/CLAUDE.md`](../../../CLAUDE.md) for the general `date` field
format), sourced from GoCollect (`gocollect.com/comic/monstress-<n>`) and
cross-checked against independent sources (search results, a same-week
review posting) before writing.

**GoCollect's own "Publication Date" field is mislabeled — it's actually
the solicitation date, not when the issue released.** Confirmed on two
issues: #2 lists "Publication Date: Dec 2, 2015" but independent sources
confirm Dec 2 was only the *solicitation* date and the issue actually
released a week later on Dec 9 — which matches GoCollect's own separate
"Store Date" field exactly. Same pattern on #3 ("Publication Date: Jan 13,
2016" vs. the confirmed actual release of Jan 27, again matching "Store
Date", and corroborated by a review posted Jan 26 — the usual day-before
pattern). **Use GoCollect's "Store Date" field, not "Publication Date"**,
when both are present; where a listing shows only one date, verify against
a second independent source before trusting the label.

## Common pitfalls

- Don't confuse issue release/cover dates with the trade-paperback
  collection date that collects them — use the individual issue's own
  release date for its `date`.
- Confirm `writer`/`artist` per issue rather than copy-pasting from the
  previous file — see "Creative team" above.
