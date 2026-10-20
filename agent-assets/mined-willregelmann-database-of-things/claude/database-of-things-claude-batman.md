# Batman (Vol. 1) — curation hints

## Directory structure

```
batman/
  CLAUDE.md
  item-attributes.schema.json
  _collection.yaml               # Vol. 1 as a whole
  <number>-batman-<number>.yaml
```

Flat — Vol. 1 ran 713 issues continuously, April 1940 through August 2011,
ending right before DC's New 52 relaunch restarted the series at a new
Vol. 2 #1 in September 2011. The New 52 run (and any later DC Rebirth/
Infinite Frontier relaunches) is out of scope here and would be a separate
sibling series directory if added, not folded into this one.

**A #0 (1994, Zero Hour tie-in) and a #1,000,000 one-shot (1998, DC One
Million event) exist outside the normal 1–713 sequence** — don't treat
them as part of the flat run if added later. **28 Annuals are a separate
numbering line**, also not part of this sequence. Whether any numbers were
skipped or doubled mid-run (1940–2011) hasn't been confirmed — check before
assuming the flat 1–713 count is gap-free when extending past the seeded
issues.

## Identifying items

Issues are identified by number; `name` is `"Batman #<N>"`. Golden Age
issues (#1–4 seeded so far) are anthologies containing several distinct
short stories — the `number` still identifies the whole issue as one
entity, don't split by story.

## Naming files

`<number>-batman-<number>.yaml`, number zero-padded to 3 digits (e.g.
`001`, `713`) — matching the volume's known total run length.

## Release dates

Where a precise on-sale date is sourced (e.g. #1: 1940-04-25, #2:
1940-07-19 — via GoCollect, cross-checked), use it in full. Where only a
cover-date month is reliably sourced (#3, #4), use month precision
(`"1940-09"`, `"1941-01"`) rather than fabricating a day. Grand Comics
Database (comics.org) and DC's own sources return HTTP 403 on direct
fetch as of this writing — mycomicshop.com listings were the working
source for cover dates/images during seeding.

## Creative team

**Credit Bill Finger as writer, not solely Bob Kane**, on Golden Age
issues — Finger's uncredited co-creation and scripting of this era's
stories is now well documented and DC's own credits have included him
(as co-creator) since 2015. Bob Kane, Jerry Robinson, and George Roussos
did pencils/inks across #1–3 in varying combinations; confirm the split
per issue rather than defaulting to "Bob Kane" alone. Leave `artist` off
an issue rather than guessing when the split isn't confirmed (done for
#4 during seeding).

## Common pitfalls

- Batman #1 introduces both the Joker and Catwoman ("the Cat") — don't
  confuse this with Catwoman's first appearance *in costume*, which is
  usually cited as #3.
- Don't confuse a reprint/facsimile edition's listing with the original
  1940s printing when sourcing cover images or dates.
